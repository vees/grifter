# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exo', '0008_auto_20150704_2055'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contentinstance',
            name='stat_hash',
            field=models.BigIntegerField(null=True),
        ),
    ]
