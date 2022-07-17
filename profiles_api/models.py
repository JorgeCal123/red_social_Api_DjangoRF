from enum import unique
from django.db import models
# AbstractBaseUser : Es una clase basica de Django para crear un usuario y poder heredar algunas cosas ya hechas
from django.contrib.auth.models import AbstractBaseUser
# PermissionsMixin : Es una clase de Django que permite establecer unos permisos de acuerdo a una jerarquia ya establecida
from django.contrib.auth.models import PermissionsMixin
# BaseUserManager : Es una Clase de Django que permite usar unas funciones ya establecidas para manipular los objetos del usuario
from django.contrib.auth.models import BaseUserManager

class UserProfileManager(BaseUserManager):
    """ Modelo que gestiona los perfiles del usuario (en este caso class: UserProfile)"""

    def create_User(self, email, name, password=None):
        """Metodo que crea un nuevo usuario (UserProfile)"""
        if not email:
            raise ValueError("Usuario debe tener un Email")
        # normalizacion del correo - despues del @ se coloca en minuscula
        email = self.normalize_email(email)
        # Crea la estructura u objeto de lo que debe tener un usuario
        user = self.model(email=email, name=name)
        # Crea una contraseña al objeto de usuario
        user.set_password(password)
        # Guarda el usuario en la base de datos
        user.save(using=self._db)

        return user


    def create_superuser(self, email, name, password=None):
        """" Metodo para crear los administradores """
        user = self.create_User(email, name, password)
        # define si es un super Usuario o Administrador (Atributo de la clase PermissionMixion - heredado en UserProfile)
        user.is_superuser = True
        # define si es parte del equipo
        user.is_staff = True
        # Guarda el usuario en la base de datos
        user.save(using=self._db)
        
        return user

class UserProfile(AbstractBaseUser, PermissionsMixin):
    """ Modelo Base que contiene toda la informacion de los usuarios en el sistema """
#Atributos

    # correo unico del usuario
    email = models.EmailField(max_length=255, unique=True)
    # nombre del usuario
    name = models.CharField(max_length=255)
    # estado del usuario si esta usando la cuenta o no la ha usado
    is_active = models.BooleanField(default=True)
    # estado del usuario si son miembros del equipo
    is_staff = models.BooleanField(default=False)
    # La manera en como se procesan o se gestionan los usuarios
    objects = UserProfileManager()
    # Campo que el usuario va a especificar para hacer el login
    USERNAME_FIELD = 'email'
    # Son los campos que son obligatorios para el registro de los usuarios
    REQUIRED_FIELDS = ['name']

    """ Metodo que me muestra el nombre completo del usuario """
    def get_full_name(self):
        return self.name

    """ Metodo que muestra solo el nombre del usuario """
    def get_short_name(self):
        return self.name

    """representacion del modelo de Usuario en cadena de texto"""
    def __str__(self):
        return "Usuario: " + self.name + " " + self.email