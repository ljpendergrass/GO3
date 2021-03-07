"""
    This file is part of Gig-o-Matic

    Gig-o-Matic is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import logging
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseNotFound
from .models import Band, Assoc, Section
from gig.helpers import update_plan_default_section
from gig.util import GigStatusChoices
from gig.models import Gig
from member.models import Member
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from band.util import AssocStatusChoices
import json
from lib.caldav import make_calfeed, save_calfeed, get_calfeed
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
from django.core.exceptions import ValidationError


def assoc_editor_required(func):
    def decorated(request, ak, *args, **kw):
        a = get_object_or_404(Assoc, pk=ak)
        is_self = (request.user == a.member)
        is_editor = a.band.is_editor(request.user)
        if not (is_self or is_editor):
            return HttpResponseForbidden()

        return func(request, a, *args, **kw)
    return decorated


def band_admin_required(func):
    def decorated(request, *args, **kw):
        band = get_object_or_404(Band, pk=kw['pk'])
        is_editor = band.is_editor(request.user)
        if not is_editor:
            return HttpResponseForbidden()

        return func(request, *args, **kw)
    return decorated


@login_required
@assoc_editor_required
def set_assoc_tfparam(request, a):
    """ set a true/false parameter on an assoc """
    is_self = (request.user == a.member)
    for param, value in request.POST.items():
        # A user cannot set their own admin status, but a superuser can do anything
        if param == 'is_admin' and is_self and not request.user.is_superuser:
            continue

        if hasattr(a, param):
            setattr(a, param, True if value == 'true' else False)
        else:
            logging.error(
                f"Trying to set an assoc property that does not exist: {param}")
    a.save()

    return HttpResponse(status=204)


@login_required
@assoc_editor_required
def set_assoc_section(request, a, sk):
    """ set a default section on an assoc """
    if sk == 0:
        s = None
    else:
        s = get_object_or_404(Section, pk=sk)
        if s.band != a.band:
            logging.error(
                f"Trying to set a section that is not part of band: {s} for {a.band}")
            return HttpResponseNotFound()

    a.default_section = s
    a.save()

    return HttpResponse(status=204)


@login_required
@assoc_editor_required
def set_assoc_color(request, a, colorindex):
    """ set a default section on an assoc """
    a.color = colorindex
    a.save()

    return render(request, 'member/color.html', {'assoc': a})


@login_required
def join_assoc(request, bk, mk):
    b = get_object_or_404(Band, pk=bk)

    if (mk == request.user.id):
        m = request.user
    else:
        m = get_object_or_404(Member, pk=mk)

    # todo make sure this is us, or we're superuser, or band_admin
    is_self = (request.user == m)
    is_super = (request.user.is_superuser)
    # TODO: Should band admins actually be able to create pending associations?
    is_band_admin = Assoc.objects.filter(
        member=request.user, band=b, is_admin=True).count() == 1
    if not (is_self or is_super or is_band_admin):
        raise PermissionError(
            'tying to create an assoc which is not owned by user {0}'.format(request.user.username))

    # OK, create the assoc
    Assoc.objects.get_or_create(
        band=b, member=m, status=AssocStatusChoices.PENDING)

    return HttpResponse(status=204)


@login_required
@assoc_editor_required
def delete_assoc(request, a):
    a.delete()

    return HttpResponse(status=204)


@login_required
def confirm_assoc(request, ak):
    a = get_object_or_404(Assoc, pk=ak)

    is_super = (request.user.is_superuser)
    is_band_admin = (Assoc.objects.filter(member=request.user,
                                          band=a.band, is_admin=True).count() == 1)
    if not (is_super or is_band_admin):
        logging.error(
            f'Trying to confirm an assoc which is not admin by user {request.user.username}')
        return HttpResponseForbidden()

    # OK, confirm the assoc
    a.status = AssocStatusChoices.CONFIRMED
    a.save()

    return HttpResponse()


@login_required
@band_admin_required
def set_sections(request, *args, **kw):
    band = get_object_or_404(Band, pk=kw['pk'])

    # handle the sections as we have them now
    list = json.loads(request.POST['sectionInfo'])
    for i, s in enumerate(list):
        if s[1]:
            the_section = get_object_or_404(Section, pk=s[1])
            the_section.name = s[0].replace(
                '&quot;', '\"').replace('&apos;', "'")
            the_section.order = i
            the_section.save()
        else:
            # this is a new section
            the_section = Section.objects.create(
                name=s[0], order=i, band=band, is_default=False)
            the_section.save()

    # handle the deleted sections
    list = json.loads(request.POST['deletedSections'])
    for s in list:
        if s:
            the_section = get_object_or_404(Section, pk=s)
            if not the_section.is_default:
                the_section.delete()

    return HttpResponse()


def set_calfeeds_dirty(band):
    """ called from gig post_save signal - when gig is updated, set calfeeds dirty for all members """
    Member.objects.filter(assocs__band=band).update(cal_feed_dirty=True)
    band.pub_cal_feed_dirty = True
    band.save()


def prepare_band_calfeed(band):
    # we want the gigs as far back as a year ago
    date_earliest = timezone.now() - timedelta(days=365)

    filter_args = {
        "band": band,
        "hide_from_calendar": False,
        "date__gt": date_earliest,
        "status": GigStatusChoices.CONFIRMED,
    }

    the_gigs = Gig.objects.filter(**filter_args)
    cf = make_calfeed(band, the_gigs, band.default_language, band.pub_cal_feed_id)
    return cf


def update_band_calfeed(id):
    b = Band.objects.get(id=id)
    cf = prepare_band_calfeed(b)
    save_calfeed(b.pub_cal_feed_id, cf)


def band_calfeed(request, pk):
    try:
        if settings.DYNAMIC_CALFEED:
            # if the dynamic calfeed is set, just create the calfeed right now and return it
            tf = prepare_band_calfeed(Band.objects.get(pub_cal_feed_id=pk))
        else:
            # if using the task queue, get the calfeed from the disk cache
            tf = get_calfeed(pk)
    except (ValueError, ValidationError):
        hr = HttpResponse()
        hr.status_code = 404
        return hr

    return HttpResponse(tf)
