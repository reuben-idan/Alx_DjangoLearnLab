from django import forms

class ExampleForm(forms.Form):
    title = forms.CharField(label="Title", max_length=100)