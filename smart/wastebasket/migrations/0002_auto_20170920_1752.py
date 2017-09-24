# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wastebasket', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='state',
            field=models.IntegerField(default=0, choices=[(0, 'Created'), (1, 'Working'), (2, 'Completed')]),
        ),
        migrations.AlterField(
            model_name='wastebasket',
            name='dry_run',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='wastebasket',
            name='force',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='wastebasket',
            name='max_size',
            field=models.PositiveIntegerField(default=32),
        ),
        migrations.AlterField(
            model_name='wastebasket',
            name='rmdir',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='wastebasket',
            name='wastebasket_path',
            field=models.TextField(default='~/Trash', unique=True),
        ),
    ]
