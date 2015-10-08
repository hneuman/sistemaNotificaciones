"""constancia_projecto URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.contrib import admin
from django.conf.urls import patterns, include, url
#urlpatterns = [
#    url(r'^admin/', include(admin.site.urls)),
#]

urlpatterns = patterns('constancia_projecto.constancia_app.views',
	(r"^usuario/(\d+)+/?$","usuario"),
	(r"^usuario/nuevo/test?$","usuario_nuevo"),
	(r"^usuario/constancia/(\d*)/?$","Constancia"),
	(r"^usuario/recibo/(\d*)/?$","Recibo"),
	(r"^test/(?P<algo>\w*)","test"),
	(r"^prueba/?","prueba"),
	(r'^usuario/nuevo$','nuevo_usuario'),
	(r'^ingresar/?$','ingresar'),
	(r'^cargar_usuarios/?$','cargar_usuarios'),
	(r'^enviar_solicitud/(\d*)/(\w*)/?$','enviar_solicitud'),
	(r'^enviar_solicitud_recibo/(\d*)/(\d*)/(\d*)/?$','enviar_solicitud_recibo'),
	(r'^cambiar_clave/?$','cambiar_clave'),
	(r'^olvido_clave/?$','olvido_clave'),
	(r'^error/?$','error'),
	(r'^definir_xmlrpc_conexion/?$','definir_xmlrpc_conexion'),
	(r'^validar_solicitud/?$','validar_solicitud'),
	(r'^multiple/(\d*,)*/?$','multiple'),
    (r'^multiple/(?P<lista>(?:.+/?)+)/?$', 'multiple'),
   
    (r'^carnet_trabajador/(\w*)/?$', 'carnet_trabajador'),
	(r'^carnet_trabajador/?$', 'carnet_trabajador'),
	(r'^cerrar_sesion/?$', 'cerrar_sesion'),

	(r"","ingresar"),

	)
