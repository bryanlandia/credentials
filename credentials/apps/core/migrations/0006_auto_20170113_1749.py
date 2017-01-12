# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20170112_2126'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='siteconfiguration',
            name='theme_scss_path',
        ),
        migrations.AlterField(
            model_name='siteconfiguration',
            name='tos_url',
            field=models.URLField(null=True, verbose_name='Terms of Service URL'),
        ),
        migrations.AlterField(
            model_name='siteconfiguration',
            name='verified_certificate_url',
            field=models.URLField(help_text='URL of page for information on verified certificates', null=True, verbose_name='Verified Certificate URL'),
        ),
    ]
