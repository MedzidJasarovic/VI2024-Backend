from django.urls import path
from . import views

urlpatterns = [
    path('solve/', views.solve_puzzle, name='solve_puzzle'),
]