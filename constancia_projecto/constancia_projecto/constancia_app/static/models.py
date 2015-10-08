from django.db import models

# Create your models here.
from django.db import models

# Create your models here.

class Usuario(models.Model):
    Nombre = models.CharField(max_length=100,default='Sin Nombre')
    Cedula = models.CharField(max_length=100, default='0000000')
    Direccion = models.TextField()
    Codigo_u = models.CharField(max_length=100,default='no Codigo')
    Telefono =  models.CharField(max_length=100,default='No Telefono')
    Email = models.CharField(max_length=100,default='No Email')
    Genero = models.CharField(max_length=100,default='No Genero')
    def __unicode__(self):
        return self.Nombre



class Conexion_xmlrpc(models.Model):
	xmlrpc_host=models.CharField(max_length=100,default='127.0.0.1',)
	xmlrpc_port=models.CharField(max_length=100,default='8069',) 
	db_host=models.CharField(max_length=100,default='127.0.0.1',)
	db_name = models.CharField(max_length=100,default='db_default',) 
	db_username = models.CharField(max_length=100,default='postgres',)
	db_pwd = models.CharField(max_length=100,default='postgres',) 