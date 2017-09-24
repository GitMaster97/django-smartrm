# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import WasteBasket, Task


admin.site.register(WasteBasket)
admin.site.register(Task)
