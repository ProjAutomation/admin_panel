from django.urls import path

from .views import home, slots, setup, invite

urlpatterns = [
    path('', home, name='projects.index'),
    path('slots/', slots, name='projects.slots'),
    path('setup/', setup, name='projects.setup'),
    path('invite/', invite, name='projects.invite'),
]
