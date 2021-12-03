from . import views
from django.urls import path
from django.conf import settings

app_name = 'api'

urlpatterns = [
	path('', views.index, name='index'),
]