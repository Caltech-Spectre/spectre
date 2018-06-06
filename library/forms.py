from django import forms


class LoginForm(forms.Form):
    caltech_id = forms.IntegerField(widget=forms.TextInput(attrs={'autocomplete':'off'}))


class SearchForm(forms.Form):
    filter = forms.CharField()
