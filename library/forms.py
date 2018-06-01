from django import forms

class LoginForm(forms.Form):
    caltech_id = forms.IntegerField(widget=forms.TextInput)
