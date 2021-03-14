# Generated by Django 3.1.7 on 2021-03-14 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Stat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(max_length=500)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('value', models.IntegerField(blank=True, default=0)),
            ],
        ),
    ]
