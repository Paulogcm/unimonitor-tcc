from django.shortcuts import render
from . main import init

init()

def index(request):
	init()
	return render(request, "api/index.html")


# Create your views here.
