# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exo', '0004_auto_20150722_1303'),
    ]

    operations = [
        migrations.CreateModel(
            name='TransformedPicture',
            fields=[
                ('signature', models.OneToOneField(primary_key=True, serialize=False, to='exo.ContentSignature')),
                ('request_width', models.IntegerField(null=True)),
                ('request_height', models.IntegerField(null=True)),
                ('request_rotation', models.IntegerField(null=True)),
                ('result_width', models.IntegerField(null=True)),
                ('result_height', models.IntegerField(null=True)),
                ('result_rotation', models.IntegerField(null=True)),
            ],
        ),
        migrations.DeleteModel(
            name='PictureSimple',
        ),
        migrations.RenameField(
            model_name='picture',
            old_name='rotation',
            new_name='orientation',
        ),
        migrations.AddField(
            model_name='contentkey',
            name='canonical',
            field=models.ForeignKey(related_name='+', null=True, to='exo.ContentSignature', unique=True),
        ),
        migrations.AddField(
            model_name='contentsignature',
            name='derived_from',
            field=models.ForeignKey(to='exo.ContentSignature', null=True),
        ),
        migrations.AddField(
            model_name='contentsignature',
            name='resiliency',
            field=models.IntegerField(null=True, choices=[(1, b'Temporary'), (2, b'Sentimental'), (3, b'Destroy'), (4, b'Limited')]),
        ),
    ]
