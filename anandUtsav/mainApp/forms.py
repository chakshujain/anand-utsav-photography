from django import forms
from .models import *


class UploadFileForm(forms.Form):
    file = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={'multiple': True}),label='')
