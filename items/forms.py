from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column
from django_countries.fields import CountryField

class AddToCartForm(forms.Form):
    pass

class UserProfileForm(forms.Form):
    Name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    LastName = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    CardID = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    Address = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    Country = CountryField(blank_label=('Select Country')).formfield(attrs={
        'class': 'custom-select d-block w-100'
    })