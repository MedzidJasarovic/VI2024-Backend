from django.urls import path
from . import views

urlpatterns = [
    path('getMove/', views.get_move, name='get_move'),
]