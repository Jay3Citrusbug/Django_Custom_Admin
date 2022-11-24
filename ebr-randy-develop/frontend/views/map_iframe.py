from django.views.decorators.clickjacking import xframe_options_exempt
from django.shortcuts import render


@xframe_options_exempt
def shops_nearby(request):
    return render(request, 'dashboard-integration/shops-nearby/shops-nearby.html')


@xframe_options_exempt
def shops_osm(request):
    return render(request, 'dashboard-integration/shops-osm/directory-map.html')


@xframe_options_exempt
def shops_carrying(request):
    return render(request, 'dashboard-integration/shops-carrying/shops-carrying.html')
