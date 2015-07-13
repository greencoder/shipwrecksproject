# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Wreck',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, blank=True)),
                ('history', models.TextField(blank=True)),
                ('year_sunk', models.SmallIntegerField(null=True, blank=True)),
                ('source', models.SmallIntegerField(choices=[(0, b'NOAA Automated Wrecks and Obstructions Information System (AWOIS)'), (1, b'NOAA Electronic Navigational Charts (ENC)')])),
                ('source_id', models.IntegerField(null=True, blank=True)),
                ('depth_meters', models.FloatField(null=True, blank=True)),
                ('location', django.contrib.gis.db.models.fields.PointField(srid=4326)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='WreckType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='wreck',
            name='wreck_type',
            field=models.ForeignKey(to='wrecks.WreckType'),
            preserve_default=True,
        ),
    ]
