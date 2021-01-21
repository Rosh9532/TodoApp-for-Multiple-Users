from django.forms import ModelForm
from app.models import TODO
from django.forms import TextInput, Textarea
from django import forms


class TODOForm(ModelForm):
    class Meta:
        model=TODO
        fields=['title','note','status','priority']

