# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exo', '0005_auto_20150704_1319'),
    ]

    operations = [
        migrations.AddField(
            model_name='contentinstance',
            name='content_container',
            field=models.ForeignKey(to='exo.ContentContainer', null=True),
        ),
        migrations.AddField(
            model_name='contentinstance',
            name='content_signature',
            field=models.ForeignKey(to='exo.ContentSignature', null=True),
        ),
        migrations.AlterField(
            model_name='contentsignature',
            name='content_key',
            field=models.ForeignKey(to='exo.ContentKey', null=True),
        ),
    ]
