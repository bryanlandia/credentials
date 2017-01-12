# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('credentials', '0004_auto_20161129_0627'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usercredential',
            name='download_url',
            field=models.CharField(help_text='URL at which the credential can be downloaded', max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='usercredential',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, unique=True, editable=False),
        ),
    ]
