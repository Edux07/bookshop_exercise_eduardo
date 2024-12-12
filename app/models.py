from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'  # Definimos el email como el campo principal de autenticación
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']


class UserProfile(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name="perfil")   #usamos el campo user como clave foranea para relacionar el perfil con el usuario
    ciudad = models.CharField(max_length=250)
    pais = models.CharField(max_length=250)
    biografía = models.TextField(blank=True,null=True) #Opcional
    fecha_de_nacimiento = models.DateField()

    def __str__(self):
        return self.usuario.username







