from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from .forms import NoteForm
from .models import Note

def home(request):
    return render(request, 'notes/home.html', {'notes': Note.objects.all(), 'form': NoteForm()})

def create_note(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Note created.')
        else:
            messages.error(request, 'Please provide a title.')
    return redirect('home')

def edit_note(request, pk):
    note = get_object_or_404(Note, pk=pk)
    form = NoteForm(request.POST or None, instance=note)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Note updated.')
        return redirect('home')
    return render(request, 'notes/edit.html', {'form': form, 'note': note})

def delete_note(request, pk):
    note = get_object_or_404(Note, pk=pk)
    if request.method == 'POST':
        note.delete()
        messages.success(request, 'Note deleted.')
    return redirect('home')

def health(request):
    return JsonResponse({'status': 'ok', 'service': 'devops-notes'})
