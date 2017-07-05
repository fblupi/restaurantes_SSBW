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


@login_required
def aniade(request):
    if request.method == "POST":
        form = RestaurantForm(request.POST, request.FILES)
        if form.is_valid():
            if len(request.FILES) != 0:
                handle_uploaded_file(restaurants.objects.count() + 1, request.FILES['photo'])
            r = form.save()
            if r:
                logger.info("Añadido un nuevo restaurante")
            return redirect('listar')
    else:
        form = RestaurantForm();
    context = {
        'form': form,
    }
    return render(request, 'restaurantes/aniade.html', context)
