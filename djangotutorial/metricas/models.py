from django.db import models

class ErrorMetrica(models.Model):
    nombre_error = models.CharField(max_length=200)
    fecha_error = models.DateField()
    cantidad_errores = models.IntegerField()

class MetricaResultados(models.Model):
    fecha_resultados = models.DateField()
    estadisticas = models.IntegerField()

class MetricaFront(models.Model):
    titulos = models.CharField(max_length=200)
    parrafos = models.TextField()
    botones = models.IntegerField()
