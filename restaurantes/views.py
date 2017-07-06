from django.shortcuts import render, HttpResponse, redirect
from .models import restaurants
from .forms import RestaurantForm
from django.contrib.auth.decorators import login_required


import logging

logger = logging.getLogger(__name__)

# Create your views here.

def index(request):
    logger.info("Consultada pagina de indice")
    return render (request, 'restaurantes/main.html')

def listar(requests):
    logger.info("Consultada lista de restaurantes")
    context = {
        "title": "Lista de restaurantes",
        "resta": restaurants.objects
    }
    return render (requests, 'restaurantes/list.html', context)

def buscar(request):
    logger.info("Realizada busqueda de restaurantes")

    name = request.GET.get('name')
    lista = restaurants.objects
    lista = restaurants.objects(name__icontains=name)
    context = {
        "title": "Resultado de busqueda",
        "resta": lista
    }
    return render(request, 'restaurantes/list.html', context)

def handle_uploaded_file(n, f):
    logger.info("Subido fichero")

    with open('static/img/restaurants/' + str(n) + '.jpg', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def restaurante(request, id):
    logger.info("Consultada pagina de restaurante")

    restaurant = restaurants.objects(restaurant_id=id)[0]
    context = {
     "resta": restaurant,
     "photo": str(restaurant.restaurant_id)
    }
    return render(request, 'restaurantes/restaurante.html', context)

def show_image(request, id):
    r = restaurants.objects(restaurant_id=id)[0]
    image = r.photo.read()
    return HttpResponse(image, content_type="image/" + r.photo.format)

@login_required
def aniade(request):
    if request.method == "POST":
        form = RestaurantForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data['name']
            city = form.cleaned_data['city']
            cuisine = form.cleaned_data['cuisine']
            borough = form.cleaned_data['borough']


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

            return redirect('listar')
    else:
        form = RestaurantForm();
    context = {
        'form': form,
    }
    return render(request, 'restaurantes/aniade.html', context)
