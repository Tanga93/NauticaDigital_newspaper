from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Favoritos_Usuario(models.Model):
	usuario = models.ForeignKey(User)
	id_articulo = models.IntegerField(default=0)