
from django.urls import path

from .views import home, slots

urlpatterns = [
    path('', home, name='projects:index'),
    path('slots/', slots, name='projects:slots'),
]
