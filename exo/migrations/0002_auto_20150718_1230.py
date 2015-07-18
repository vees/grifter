# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exo', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='picture',
            name='contentinstance_ptr',
        ),
        migrations.RemoveField(
            model_name='picture',
            name='private',
        ),
        migrations.AddField(
            model_name='picture',
            name='height',
            field=models.IntegerField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='picture',
            name='instance',
            field=models.OneToOneField(primary_key=True, default=1, serialize=False, to='exo.ContentInstance'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='picture',
            name='rating',
            field=models.IntegerField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='picture',
            name='width',
            field=models.IntegerField(null=True),
            preserve_default=True,
        ),
    ]
