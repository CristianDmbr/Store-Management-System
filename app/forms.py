from django import forms

class TaskForm(forms.Form):
    title = forms.CharField(max_length = 200)
    status = forms.ChoiceField( choices = [
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('almost_done', 'Almost Done')
    ])
    assistance = forms.CharField(max_length=200, required = False)
    due_date = forms.DateTimeField(required = False)

