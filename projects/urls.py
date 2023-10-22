from django.urls import path

from .views import home, select_slot, setup

urlpatterns = [
    path('', home, name='projects.index'),
    path('streams/<int:stream_pk>/slots/', select_slot, name='projects.slots'),
    path('setup/', setup, name='projects.setup'),
    # path('invite/', invite, name='projects.invite'),
]
