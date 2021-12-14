from django.urls import path

from spoc.views import index
from . import views

urlpatterns = [
	path('', views.index, name='spoc-index'),
]