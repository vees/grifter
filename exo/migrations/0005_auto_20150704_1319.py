# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exo', '0004_auto_20150704_1242'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContentContainer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('server', models.CharField(max_length=200)),
                ('drive', models.CharField(max_length=200)),
                ('path', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='ContentInstance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('filename', models.CharField(max_length=200)),
                ('relpath', models.CharField(max_length=200)),
                ('stat_hash', models.IntegerField()),
                ('first_seen', models.DateTimeField(null=True)),
                ('verified_on', models.DateTimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ContentKey',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.CharField(max_length=4)),
            ],
        ),
        migrations.CreateModel(
            name='ContentSignature',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('md5', models.CharField(max_length=32)),
                ('sha2', models.CharField(max_length=64)),
                ('content_size', models.IntegerField()),
                ('content_key', models.ForeignKey(to='exo.ContentKey')),
            ],
        ),
        migrations.DeleteModel(
            name='Album',
        ),
        migrations.DeleteModel(
            name='Camera',
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
        migrations.DeleteModel(
            name='Copyright',
        ),
        migrations.DeleteModel(
            name='Event',
        ),
        migrations.DeleteModel(
            name='EXIF',
        ),
        migrations.DeleteModel(
            name='GeoTag',
        ),
        migrations.DeleteModel(
            name='Location',
        ),
        migrations.DeleteModel(
            name='MasterFile',
        ),
        migrations.DeleteModel(
            name='Moment',
        ),
        migrations.DeleteModel(
            name='Old_Camera',
        ),
        migrations.DeleteModel(
            name='Old_Location',
        ),
        migrations.DeleteModel(
            name='Old_Photographer',
        ),
        migrations.DeleteModel(
            name='Old_Picture',
        ),
        migrations.DeleteModel(
            name='Old_Theme',
        ),
        migrations.RemoveField(
            model_name='photographer',
            name='person',
        ),
        migrations.DeleteModel(
            name='PictureSimple',
        ),
        migrations.DeleteModel(
            name='Rating',
        ),
        migrations.DeleteModel(
            name='Rotation',
        ),
        migrations.DeleteModel(
            name='ServerInstance',
        ),
        migrations.DeleteModel(
            name='Situation',
        ),
        migrations.RemoveField(
            model_name='subject',
            name='person',
        ),
        migrations.RemoveField(
            model_name='subject',
            name='picture',
        ),
        migrations.DeleteModel(
            name='Tag',
        ),
        migrations.DeleteModel(
            name='Venue',
        ),
        migrations.DeleteModel(
            name='Person',
        ),
        migrations.DeleteModel(
            name='Photographer',
        ),
        migrations.DeleteModel(
            name='Picture',
        ),
        migrations.DeleteModel(
            name='Subject',
        ),
    ]
