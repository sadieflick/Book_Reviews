# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-04-21 20:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0002_auto_20180421_1748'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='author',
            name='book_author',
        ),
        migrations.AddField(
            model_name='book',
            name='author',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='books', to='application.Author'),
            preserve_default=False,
        ),
    ]