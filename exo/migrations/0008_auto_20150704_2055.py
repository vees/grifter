# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exo', '0007_auto_20150704_2032'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contentinstance',
            name='content_container',
            field=models.ForeignKey(default=1, to='exo.ContentContainer'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='contentinstance',
            name='stat_hash',
            field=models.IntegerField(null=True),
        ),
    ]
