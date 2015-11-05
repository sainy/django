# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deploy', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Webhook',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('post_data', models.CharField(default=b'this is a test', max_length=10000)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='deploys',
            name='Order',
            field=models.CharField(default=b'3', max_length=5),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='deploys',
            name='Status',
            field=models.CharField(default=b'0', max_length=5),
            preserve_default=True,
        ),
    ]
