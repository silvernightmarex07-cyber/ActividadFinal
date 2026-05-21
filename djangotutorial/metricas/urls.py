from django.urls import path
from . import views

urlpatterns = [
    path("", views.raiz, name="raiz"),
    path("resultados/", views.resultados, name="resultados"),
    path("errores/", views.errores, name="errores"),
]