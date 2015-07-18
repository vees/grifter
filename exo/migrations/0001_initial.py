# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ContentContainer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('server', models.CharField(max_length=64)),
                ('drive', models.CharField(max_length=64)),
                ('path', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ContentInstance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('filename', models.CharField(max_length=200)),
                ('relpath', models.CharField(max_length=200)),
                ('stat_hash', models.BigIntegerField(null=True)),
                ('first_seen', models.DateTimeField(null=True)),
                ('verified_on', models.DateTimeField(null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ContentKey',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.CharField(unique=True, max_length=4)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ContentSignature',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('md5', models.CharField(max_length=32)),
                ('sha2', models.CharField(max_length=64)),
                ('content_size', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Picture',
            fields=[
                ('contentinstance_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='exo.ContentInstance')),
                ('rotation', models.IntegerField(null=True, choices=[(90, b'90 CW'), (270, b'90 CCW'), (0, b'None'), (180, b'180')])),
                ('private', models.NullBooleanField()),
            ],
            options={
            },
            bases=('exo.contentinstance',),
        ),
        migrations.CreateModel(
            name='PictureSimple',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('filename', models.CharField(max_length=200)),
                ('directory', models.CharField(max_length=200)),
                ('stamp', models.DateTimeField()),
                ('file_hash', models.CharField(max_length=200)),
                ('rotation', models.IntegerField(default=0, choices=[(90, b'90 CW'), (270, b'90 CCW'), (0, b'None'), (180, b'180')])),
                ('private', models.NullBooleanField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Redirect',
            fields=[
                ('contentkey_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='exo.ContentKey')),
            ],
            options={
            },
            bases=('exo.contentkey',),
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('contentkey_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='exo.ContentKey')),
                ('slug', models.CharField(max_length=32)),
                ('description', models.CharField(max_length=64)),
            ],
            options={
            },
            bases=('exo.contentkey',),
        ),
        migrations.AddField(
            model_name='redirect',
            name='destination',
            field=models.ForeignKey(related_name='+', to='exo.ContentKey'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='contentsignature',
            name='content_key',
            field=models.ForeignKey(to='exo.ContentKey', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='contentinstance',
            name='content_container',
            field=models.ForeignKey(to='exo.ContentContainer'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='contentinstance',
            name='content_signature',
            field=models.ForeignKey(to='exo.ContentSignature', null=True),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='contentcontainer',
            unique_together=set([('server', 'drive', 'path')]),
        ),
    ]
