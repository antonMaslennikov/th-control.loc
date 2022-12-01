from django import forms
from .models import Project

class ProjectForm(forms.ModelForm): 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['url'].widget.attrs.update({'class': 'form-control'})
        self.fields['types'].widget.attrs.update({'class': 'form-control'})
        self.fields['regions'].widget.attrs.update({'class': 'form-control'})
        self.fields['is_service'].widget.attrs.update({'class': 'form-check-input'})

    class Meta:
        model = Project
        fields = ['name', 'url', 'types', 'regions', 'is_service']
