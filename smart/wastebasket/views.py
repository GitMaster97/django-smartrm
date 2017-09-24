# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import(
    render_to_response,
    render,
    redirect
)
from django.views import generic
from django.views.generic import ListView

from srm.wastebasket_manager import WasteBasketManager
from srm.move_error import MoveError
from srm.file_operations import cut_leafs

from wastebasket.models import WasteBasket, Task
from wastebasket.forms import TaskForm, WasteBasketForm

import multiprocessing


def home_page(request):
    return render(request, 'wastebasket/home.html')


def wastebasket_list(request):
    wastebaskets = {
        'wastebaskets': WasteBasket.objects.order_by('name')
        }

    return render(request, 'wastebasket/wastebasket_list.html', wastebaskets)


def wastebasket_detail(request, pk):
    wastebasket = WasteBasket.objects.get(pk=int(pk))
    form = WasteBasketForm(instance=wastebasket)

    if request.method == "POST":
        form = WasteBasketForm(request.POST, instance=wastebasket)
       
        if form.is_valid():
            form.save()
            return redirect('/wastebasket/')

    wb = WasteBasketManager(
        rmdir=wastebasket.rmdir,
        force=wastebasket.force,
        dry_run=wastebasket.dry_run,
        max_size=wastebasket.max_size,
        storage_time=wastebasket.storage_time,
        wastebasket_path=wastebasket.wastebasket_path,
    )

    context = {
        'form': form,
        'wastebasket': wb,
        'wastebaskets': WasteBasket.objects.all()
        }    

    return render(request, 'wastebasket/wastebasket_detail.html', context)


def wastebasket_new(request):
    form = WasteBasketForm()

    if request.method == "POST":
        form = WasteBasketForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('/wastebasket/')

    return render(request, 'wastebasket/wastebasket_new.html', {'form': form})
    

def task_list(request):
    tasks = {
        'tasks': Task.objects.order_by('name'),
    }

    return render(request, 'wastebasket/task_list.html', tasks)


def task_detail(request, pk):
    task = Task.objects.get(pk=int(pk))
    form = TaskForm(instance=task)

    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)

        if form.is_valid:
            form.save()
            return redirect('/task/')

    return render(request, 'wastebasket/task_detail.html', {'form': form})
    

def task_new(request):
    form = TaskForm()

    if request.method == 'POST':
        form = TaskForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('/task/')
    
    return render(request, 'wastebasket/task_new.html', {'form': form})


def task_result(request, pk):
    task = Task.objects.get(pk=pk)
    working_tasks = wastebasket_working_tasks(task.wastebasket)

    context = {}
    if working_tasks:
        context = { 'task': working_tasks[0] }
    else:
        task.state = Task.WORKING
        task.save()
        
        context = parallel_execution_of_task(task)

        task.state = Task.COMPLETED
        task.save()

    return render(request,'wastebasket/task_result.html', context)


def parallel_execution_of_task(task, num_process=None):
    mgr = multiprocessing.Manager()
    result = mgr.list()

    wb = wastebasket_from_task(task)
    paths = task.paths.split()
    
    if num_process is None:
        num_process = multiprocessing.cpu_count() * 2

    action, error_object = None, None

    if task.restore:
        action = 'Restore'

        splited_paths = [ [] for i in xrange(num_process)]
        for i in xrange(len(paths)):
            splited_paths[i % num_process].append(paths[i])

        jobs = []
        for i in xrange(num_process):
            j = multiprocessing.Process(target=restore_worker,
                                        args=(result, wb, splited_paths[i]))
            jobs.append(j)

        for j in jobs:
            j.start()

        for j in jobs:
            j.join()
    elif task.regex:
        action = 'Remove'
        result = wb.remove_regex(paths[0], search_dirs=True)
    else:
        action = 'Remove'

        while paths:
            paths, leafs = cut_leafs(*paths)

            splited_paths = [ [] for i in xrange(num_process)]
            for i in xrange(len(leafs)):
                splited_paths[i % num_process].append(leafs[i])
            
            jobs = []
            for i in xrange(num_process):
                j = multiprocessing.Process(target=remove_worker,
                                            args=(result, wb, splited_paths[i]))
                jobs.append(j)

            for j in jobs:
                j.start()

            for j in jobs:
                j.join()
    
    context = {
        'result': result,
        'action': action,
        'error_object': error_object,
    }

    return context

def wastebasket_from_task(task):
    """
    Creates and returns WasteBasketManager object from task.
    Task flags overlap WasteBaskeModel flags.
    """
    wastebasket_model = task.wastebasket
   
    wb = WasteBasketManager(
        rmdir=wastebasket_model.rmdir,
        force=wastebasket_model.force,
        dry_run=wastebasket_model.dry_run,
        max_size=wastebasket_model.max_size,
        storage_time=wastebasket_model.storage_time,
        wastebasket_path=wastebasket_model.wastebasket_path,
    )

    if task.rmdir is not None:
        wb.rmdir = task.rmdir

    if task.force is not None:
        wb.force = task.force
    
    if task.dry_run is not None:
        wb.dry_run = task.dry_run

    return wb


def wastebasket_working_tasks(wastebasket_model):
    """
    Checks if wastebasket_model has a working tasks.
    Returns the list of running task.
    """
    tasks = Task.objects.filter(wastebasket__exact=wastebasket_model)
    
    working_tasks = []
    for task in tasks:
        if task.state == Task.WORKING:
            working_tasks.append(task)
    
    return working_tasks


def restore_worker(result, wb, paths):
    """
    Function for parallel restoring files.
    """
    result.extend(wb.restore(*paths))


def remove_worker(result, wb, paths):
    """
    Function for restoring files.
    """
    result.extend(wb.remove(*paths))