# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exo', '0002_masterfile_old_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='masterfile',
            name='updated',
            field=models.DateTimeField(auto_now=True),
            preserve_default=True,
        ),
    ]
