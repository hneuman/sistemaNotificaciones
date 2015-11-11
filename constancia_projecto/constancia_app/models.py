from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
import datetime
# Create your models here.

class Usuario(models.Model):
    """
    Description: Modelo Usuario
    """
   
    nombre = models.CharField(max_length=100,default='Sin Nombre')
    cedula = models.CharField(max_length=100, default='0000000')
    direccion = models.TextField()
    codigo_u = models.CharField(max_length=100,default='no Codigo')
    telefono =  models.CharField(max_length=100,default='No Telefono')
    email = models.CharField(max_length=100,default='No Email')
    genero = models.CharField(max_length=100,default='No Genero')
    fecha_nacimiento = models.DateField(auto_now=True)
    nacionalidad = models.CharField(max_length=20, default='V')

    def __unicode__(self):
        return self.cedula



class Conexion_xmlrpc(models.Model):
    """
    Description: Modelo 
    """
   
    xmlrpc_host=models.CharField(max_length=100,default='127.0.0.1',)
    xmlrpc_port=models.CharField(max_length=100,default='8069',) 
    db_host=models.CharField(max_length=100,default='127.0.0.1',)
    db_name = models.CharField(max_length=100,default='db_default',) 
    db_username = models.CharField(max_length=100,default='postgres',)
    db_pwd = models.CharField(max_length=100,default='postgres',) 
    def __unicode__(self):
        return self.xmlrpc_host


class historial_solicitudes(models.Model):
    """
    Description: Model Description
    """
    fecha_solicitud = models.DateField()
    codigo_impresion = models.CharField(max_length=100,default='',) 
    tipo_solicitud = models.CharField(max_length=100,default='',) 

    def __unicode__(self):
        return self.codigo_impresion


class apps_web_service(models.Model):

    user_web = models.CharField(max_length=100,default='NULL',) 
    valido = models.BooleanField(default=False,) 
    password = models.CharField(max_length=100,default='NULL',) 
    ip = models.CharField(max_length=100,default='NULL',) 
    port = models.IntegerField(default=0000,) 
