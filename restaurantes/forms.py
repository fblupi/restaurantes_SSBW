from django import forms

from .models import *

from lxml import etree

class RestaurantForm(forms.Form):
    name    = forms.CharField(required=True, label='Nombre', max_length=80)
    city    = forms.CharField(required=True, label='Ciudad')
    cuisine = forms.CharField(required=True, label='Tipo de cocina')
    borough = forms.CharField(required=True, label='Barrio')
    photo   = forms.FileField(required=False, label='Foto')

    def save(self, commit=True):
        req_url = 'http://maps.googleapis.com/maps/api/geocode/xml?address=' + self.cleaned_data['name'] + ' ' + self.cleaned_data['city']

        tree = etree.parse(req_url)

        addressXML = tree.xpath('//address_component')
        locationXML = tree.xpath('//location')

        buildingXML = addressXML[0].xpath('//long_name/text()')[0]
        streetXML = addressXML[1].xpath('//long_name/text()')[1]
        cityXML = addressXML[2].xpath('//long_name/text()')[2]
        zipcodeXML = int(addressXML[6].xpath('//long_name/text()')[6])
        coordXML = [float(locationXML[0].xpath('//lat/text()')[0]), float(locationXML[0].xpath('//lng/text()')[0])]

        a = addr(building=buildingXML, street=streetXML, city=cityXML, zipcode=zipcodeXML, coord=coordXML)

        r = restaurants()

        r.name = self.cleaned_data['name']
        r.restaurant_id = restaurants.objects.count() + 1
        r.cuisine = self.cleaned_data['cuisine']
        r.borough = self.cleaned_data['borough']
        r.address = a

        if len(request.FILES) != 0:
            r.photo.put(request.FILES['photo'], content_type = request.FILES['photo'].content_type)

        r.save()

        return r
