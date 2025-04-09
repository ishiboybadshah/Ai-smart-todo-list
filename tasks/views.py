from django.shortcuts import render, redirect
from .models import Task
from .forms import TaskForm
from .utils import get_priority_from_ai

def home(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        due_date = request.POST.get('due_date')

        
        priority = get_priority_from_ai(title, description)

        
        Task.objects.create(
            title=title,
            description=description,
            due_date=due_date or None,
            priority=priority
        )

        return redirect('home')  

    tasks = Task.objects.all()
    return render(request, 'home.html', context={'tasks': tasks})


from django.shortcuts import redirect, get_object_or_404

def toggle_complete(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.completed = not task.completed
    task.save()
    return redirect('home')

def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    return redirect('home')