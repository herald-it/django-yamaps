from django.shortcuts import render

from .models import Address


def index(request):
    addresses = Address.objects.all()
    return render(request, "index.html", {"addresses": addresses})
