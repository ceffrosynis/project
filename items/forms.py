from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column
from django_countries.fields import CountryField

CATEGORIES = (
        ('T', 'Technology'),
        ('C', 'Comedy'),
        ('A', 'Adventure'),
        ('H', 'Horror'),
        ('R', 'Romance'),
        ('O', 'Other'),
        ('M', 'Mystery')
)


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

class InsertProductForm(forms.Form):
    ProductName = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    Price = forms.FloatField(widget=forms.NumberInput(attrs={
        'class': 'form-control'
    }))
    Discount = forms.FloatField(widget=forms.NumberInput(attrs={
        'class': 'form-control'
    }), initial=0)
    Description = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control'
    }))
    Image = forms.ImageField(required=False, initial='default.png')
    Stock = forms.IntegerField(widget=forms.NumberInput(attrs={
        'class': 'form-control'
    }))
    slug = forms.SlugField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    ProductType = forms.ChoiceField(choices=CATEGORIES)

class Filter(forms.Form):
    Technology = forms.BooleanField(widget=forms.CheckboxInput(attrs={
        'class': 'custom-control-input',
        'onclick':'this.form.submit();',
        'id': 'check1'
    }), required=False)
    Comedy = forms.BooleanField(widget=forms.CheckboxInput(attrs={
        'class': 'custom-control-input',
        'onclick':'this.form.submit();',
        'id': 'check2'
    }), required=False)
    Adventure = forms.BooleanField(widget=forms.CheckboxInput(attrs={
        'class': 'custom-control-input',
        'onclick':'this.form.submit();',
        'id': 'check3'
    }), required=False)
    Horror = forms.BooleanField(widget=forms.CheckboxInput(attrs={
        'class': 'custom-control-input',
        'onclick':'this.form.submit();',
        'id': 'check4'
    }), required=False)
    Romance = forms.BooleanField(widget=forms.CheckboxInput(attrs={
        'class': 'custom-control-input',
        'onclick':'this.form.submit();',
        'id': 'check5'
    }), required=False)
    Other = forms.BooleanField(widget=forms.CheckboxInput(attrs={
        'class': 'custom-control-input',
        'onclick':'this.form.submit();',
        'id': 'check6'
    }), initial=True, required=False)
    Mystery = forms.BooleanField(widget=forms.CheckboxInput(attrs={
        'class': 'custom-control-input',
        'onclick':'this.form.submit();',
        'id': 'check7'
    }), initial=True, required=False)


    