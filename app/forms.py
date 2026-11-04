from django import forms
from .models import Note
class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'e.g. Learn Docker Compose'}),
            'content': forms.Textarea(attrs={'placeholder': 'Write your note...', 'rows': 5}),
        }
