# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exo', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MasterFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('filename', models.CharField(max_length=200)),
                ('server', models.CharField(max_length=200)),
                ('volume', models.CharField(max_length=200)),
                ('base_directory', models.CharField(max_length=200)),
                ('directory', models.CharField(max_length=200)),
                ('stat_hash', models.IntegerField(null=True)),
                ('hash_md5', models.CharField(max_length=200)),
                ('hash_sha2', models.CharField(max_length=200)),
                ('updated', models.DateTimeField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Old_Picture',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
