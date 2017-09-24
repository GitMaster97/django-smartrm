# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.db import models
from srm.file_operations import get_full_path


class WasteBasket(models.Model):
    name = models.CharField(max_length=50, default="WasteBasket")

    rmdir = models.BooleanField(default=False)
    force = models.BooleanField(default=False)
    dry_run = models.BooleanField(default=False)

    max_size = models.PositiveIntegerField(default=32)
    storage_time = models.DurationField(default=datetime.timedelta(days=30))
    wastebasket_path = models.FilePathField(path=get_full_path('~/'), allow_files=False, allow_folders=True)
    wastebasket_path = models.TextField(default='~/Trash', unique=True)

    def __unicode__(self):
        return self.name

class Task(models.Model):
    CREATED = 0
    WORKING = 1
    COMPLETED = 2

    STATE_CHOISES = (
        (CREATED, 'Created'),
        (WORKING, 'Working'),
        (COMPLETED, 'Completed'),
    )

    name = models.CharField(max_length=50, default="Task")
    state = models.IntegerField(choices=STATE_CHOISES, default=CREATED)

    wastebasket = models.ForeignKey(WasteBasket, on_delete=models.CASCADE)                          #ссылка на другую модель

    rmdir = models.NullBooleanField()
    force = models.NullBooleanField()
    dry_run = models.NullBooleanField()

    restore = models.BooleanField()
    regex = models.BooleanField()

    paths = models.TextField()

    def __unicode__(self):
        return self.name
