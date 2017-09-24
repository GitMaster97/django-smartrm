# -*- coding: utf-8 -*-
from django import forms
from .models import WasteBasket, Task


class TaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ('name', 'wastebasket', 
            'rmdir', 'force', 'dry_run', 
            'restore', 'regex', 'paths')


class WasteBasketForm(forms.ModelForm):

    class Meta:
        model = WasteBasket
        fields = ('name', 'rmdir', 'force', 'dry_run', 
            'max_size', 'storage_time', 'wastebasket_path')
