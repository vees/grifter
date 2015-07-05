# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exo', '0006_auto_20150704_1331'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='contentcontainer',
            unique_together=set([('server', 'drive', 'path')]),
        ),
    ]
