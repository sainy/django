# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deploy', '0002_auto_20150605_0901'),
    ]

    operations = [
        migrations.AddField(
            model_name='webhook',
            name='name',
            field=models.CharField(default=b'test', max_length=100),
            preserve_default=True,
        ),
    ]
