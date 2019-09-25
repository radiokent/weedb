from django import forms


class SearchForm(forms.Form):
    genes = forms.CharField(widget=forms.Textarea, label='')
