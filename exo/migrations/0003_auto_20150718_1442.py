# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exo', '0002_auto_20150718_1230'),
    ]

    operations = [
        migrations.AddField(
            model_name='picture',
            name='signature',
            field=models.OneToOneField(primary_key=True, default=1, serialize=False, to='exo.ContentSignature'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='picture',
            name='taken_on',
            field=models.DateTimeField(null=True),
            preserve_default=True,
        ),
    ]
