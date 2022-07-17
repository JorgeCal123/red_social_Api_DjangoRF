from django.contrib import admin

# importamos todos los modelos que creamos en el archivo models
from profiles_api.models import *

#Con esta linea le damos acceso al administrador para que puedea editar estos modelos desde la pagina admin
admin.site.register(UserProfile)

