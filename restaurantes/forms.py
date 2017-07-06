from django import forms

from .models import *

from lxml import etree

class RestaurantForm(forms.Form):
    name    = forms.CharField(required=True, label='Nombre', max_length=80)
    city    = forms.CharField(required=True, label='Ciudad')
    cuisine = forms.CharField(required=True, label='Tipo de cocina')
    borough = forms.CharField(required=True, label='Barrio')
    photo   = forms.FileField(required=False, label='Foto')
