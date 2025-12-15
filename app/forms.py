from django.forms import ModelForm
from .models import Task
from django import forms

class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['title','status','assistance','due_date']
    
    def clean_title(self):
        title = self.cleaned_data['title']
        if "bad" in title:
            raise forms.ValidationError("Tittle Cannot contain 'bad'")
        return title