# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exo', '0003_auto_20150718_1442'),
    ]
    operations = [
        migrations.CreateModel(
            name='Tag2',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.CharField(max_length=32)),
                ('description', models.CharField(max_length=64, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='tag',
            name='contentkey_ptr',
        ),
        migrations.RemoveField(
            model_name='picture',
           name='instance',
        ),
        migrations.DeleteModel(
            name='Tag',
        ),
        migrations.AddField(
            model_name='contentsignature',
            name='tags',
            field=models.ManyToManyField(to='exo.Tag2'),
        ),
    ]
