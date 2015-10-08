from django.shortcuts import render
from django.shortcuts import render_to_response
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from constancia_projecto.constancia_app.models import *
from constancia_projecto.constancia_app.forms import *

import time
from calendar import month_name
from django.forms import ModelForm
from django.core.context_processors import csrf
from django.http import HttpResponseRedirect
from django.template import RequestContext

from django.shortcuts import render_to_response
from django.template.context_processors import csrf
import constancia_projecto.constancia_app.forms

#---------------- para LOGIN

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

#--------------------------para XMLRPC
import re
import time
import base64
import xmlrpclib
import csv
import psycopg2
import sys
import os
#-------------------------------General
from datetime import date
from hasher import make_password
from hasher import test_hasher

import hasher

# Create your views here.
def main(request):
	print RequestContext(request)
	return render_to_response("main.html",context_instance=RequestContext(request))

def usuario(request,id):
	#hacer busqueda para el nombre
	print id
	usuario = Usuario.objects.get(pk=int(id))
	#usuario={}
	#usuario['Nombre']=u.Nombre
	#print usuario
	d = {}
	d['usuario']=usuario
	#for i in d:
	#	print i,d[i]

	return render_to_response("usuario.html",d,context_instance=RequestContext(request))

def usuario_nuevo(request):
	return render_to_response("usuario_nuevo.html",context_instance=RequestContext(request))

def Constancia(request,id):
	print "constancia %s" %id
	usuario = User.objects.get(pk=int(id))
	d = {}
	d['usuario']=usuario
	return render_to_response("constancia.html",d,context_instance=RequestContext(request))


def Recibo(request,id):
	print "Recibo %s" %id
	usuario = User.objects.get(pk=int(id))
	d = {}
	d['usuario']=usuario
	return render_to_response("recibo.html",d,context_instance=RequestContext(request))	

def test(request,algo):
	print "request === %s"%request
	try:
		print request.GET['Meses']

	except Exception,e:
		print e
	print "request session %s" %request.session	
	for i in request:
		print i
	print "test == %s "%algo
	return render_to_response("main.html",context_instance=RequestContext(request))	


def nuevo_usuario(request):
	print "hola joe"
	if request.method == 'POST':
		formulario = UserCreationForm(request.POST)
		if formulario.is_valid():
			formulario.save()
			return HttpResponseRedirect('/main')
	else:
		formulario = UserCreationForm()
	return render_to_response('nuevo_usuario.html',{'formulario':formulario}, context_instance=RequestContext(request))
			

def ingresar(request):
	print request

 	print "llego a ingresar"
	if request.method == 'POST':
		print "es POST"
		formulario = AuthenticationForm(request.POST)
		if formulario.is_valid:
			print "Es valido"
			usuario = request.POST['username']
			clave = request.POST['password']
			acceso = authenticate(username=usuario,password=clave)
			print acceso
			print usuario,clave
			
			try:
				user_user = User.objects.get(username=request.POST['username'])
			except Exception,e:
				user_user=""
				acceso=None

			d = {}
			d['usuario']=user_user
			
			if acceso is not None:
				print "tiene acceso"
				if acceso.is_active:
					print "esta activo"
					login(request, acceso)
					usuario=str(usuario)
					print "<<<<<<<<<<<<<<<<<<< %s >>>>>>>>>>>>>>>>" %usuario

					try:
						#usuario = Usuario.objects.get(Nombre=usuario)
						
						is_staff = user_user.is_staff
					except Exception,e:
						print e						
						is_staff=False

					print user_user
					if not is_staff:
						return render_to_response("usuario.html",d,context_instance=RequestContext(request))
					else:
						return render_to_response("administrador.html",d,context_instance=RequestContext(request))
				else:
					d['formulario'] = cambio_clave(initial={'username_usuario': user_user.username})

					return render_to_response('noactivo.html',d,context_instance=RequestContext(request))
				    #return render(request, 'noactivo.html', d)

			else:
				return render_to_response('nousuario.html',context_instance=RequestContext(request))
	else:
		formulario = AuthenticationForm()
	return render_to_response('ingresar.html',{'formulario':formulario}, context_instance=RequestContext(request))
		


def login_login(URL, dbname, username, pwd):
	sock = xmlrpclib.ServerProxy(URL+'common')
	uid = sock.login(dbname, username, pwd)
	return uid 

def execute(URL, object, func, args, dbname, username, uid, pwd):
	sock = xmlrpclib.ServerProxy(URL+'object')
	result = sock.execute(dbname, uid, pwd, object, func, args)
	return result 

def create_file(ruta,file_name, text):
	file_name = os.path.join(ruta, file_name)
	fp = open(file_name, 'w')
	string = base64.decodestring(text)
	fp.write(string)
	fp.close()

def error(request):
	return 	render_to_response('error.html')

def enviar_xmlrpc(configuracion_xmlrpc,funcion_xmlrpc,parametro):
	print "--___----- %s -.-.--.- "%parametro
	try:
		if configuracion_xmlrpc == "defaul" or configuracion_xmlrpc =="":
			configuracion_xmlrpc = 'notificaciones.configuracion'
		try:	
			xmlrpc_conexion = Conexion_xmlrpc.objects.get(pk=1)
		except Exception,e:

			d={}
			d['error']=" DIGALE AL ADMINISTRADOR QUE CONFIGURE LOS DATOS DE Conexion_xmlrpc "
			print "*/*/*/*/*/*/*/*/*/*/* XMLRPC \n %s \n */*/*/*/*/*/*/**/*/*/" %e
			return 	render_to_response('error.html',d,context_instance=RequestContext(request))

		HOST= xmlrpc_conexion.xmlrpc_host
		PORT= int(xmlrpc_conexion.xmlrpc_port)
		
		HOSTDB= xmlrpc_conexion.db_host
		dbname = xmlrpc_conexion.db_name
		username = xmlrpc_conexion.db_username
		pwd = xmlrpc_conexion.db_pwd

		print HOST
		print PORT
		print HOSTDB
		print dbname
		print username
		print pwd


		URL='http://%s:%d/xmlrpc/'%(HOST,PORT)
		uid = login_login(URL, dbname, username, pwd)
		sock = xmlrpclib.ServerProxy(URL+'object')
		print uid
		print sock
	#	result = sock.execute(dbname, uid, pwd, 'notificaciones.configuracion', 'recuperar_correo', 1,(lista_peticiones))
		result = sock.execute(dbname, uid, pwd, configuracion_xmlrpc, funcion_xmlrpc, 1,(parametro))
		#recuperar_correo(cr, uid, ids, cedula, context=None)

		return True
	except Exception,e:
		print " */*/*/*/*/*/*/*/*/*/* ERROR \n %s \n */*/*/*/*/*/*/**/*/*/ *"%e
		return 	render_to_response('error.html',context_instance=RequestContext(request))



def enviar_solicitud(request,id,tipo):
	#Para enviar la solicitud de constancia o recibo, via XMLRPC

	print "tipo === %s " %tipo 
	print id


	
	#[{'descripcion': 'basica', 'telefono_trabajador': '04145795060', 'valido': True, 'tipo': 'constancy', 'cedula': '20698409'}]
	#diana_10_09_2015
	#[{'descripcion': '05/2015', 'telefono_trabajador': '04145795060', 'valido': True, 'tipo': 'receipt', 'cedula': '20698409'}] 
	print type(id)
	print int(id)

	try:
		usuario = User.objects.get(pk=int(id))
		peticion={}

		if not (isinstance(tipo,basestring)):
			peticion['descripcion']= str(tipo['mes'] + "/" + tipo['anno'])
			peticion['tipo']='receipt'
		else:	
			peticion['descripcion']='basica'
			peticion['tipo']='constancy'
		
		peticion['telefono_trabajador']=""
		peticion['valido']='True'
		peticion['cedula']=str(usuario.username)
		lista_peticiones=[]
		lista_peticiones.append(peticion)
		print lista_peticiones

		result = enviar_xmlrpc('','peticion_gammu',lista_peticiones) 

	except Exception,e:
		print "#HUBO UN ERROR"
		print e	


	return render_to_response('main.html')

def enviar_solicitud_recibo(request,id,mes,anno):	
	#preparar solicitud recibo
	print "modificar Solcitud"
	test_hasher()

	tipo={}
	tipo['mes']=mes
	tipo['anno']=anno
	print " >>>>>  %s  <<<<<" %make_password("123")

	return enviar_solicitud(request,id,tipo)

def cargar_usuarios(request):
	return render_to_response('administrador.html',context_instance=RequestContext(request))


def cambiar_clave(request):
	#print request
	context_instance=RequestContext(request)

	if request.method == "POST":
		print " ------- %s -------" %context_instance
		
		print request.POST
		form_cambio_clave = cambio_clave(request.POST)
		print form_cambio_clave
		
		#print " ********* %s ********" %form_cambio_clave.cleaned_data


		if form_cambio_clave.is_valid():
			print " ********* %s ********" %form_cambio_clave.cleaned_data
			print form_cambio_clave.cleaned_data['username_usuario']
			username_clave = form_cambio_clave.cleaned_data['username_usuario']
			usuario=User.objects.get(username=username_clave)
			print "****-*- %s *-*-*-*-* "%form_cambio_clave.cleaned_data['clave_usuario']
			print "****-*- %s *-*-*-*-* "%make_password(form_cambio_clave.cleaned_data['clave_usuario'])
			usuario.password = make_password(form_cambio_clave.cleaned_data['clave_usuario'])
			usuario.is_active = True
			usuario.save()	
 			#{'clave_usuario': u'123', 'clave_re_usuario': u'123', 'apellido_usuario': u'', 'nombre_usuario': u'', 'username_usuario': u'hneuman'} 


	return HttpResponseRedirect('ingresar.html')

def recuperar_clave(usuario_cedula):
	print "recuperar_clave"

	parametros=[]
	d={}
	d['cedula']=usuario_cedula
	#[{'descripcion': '05/2015', 'telefono_trabajador': '04145795060', 'valido': True, 'tipo': 'receipt', 'cedula': '20698409'}]
	parametros.append(d)

	result = enviar_xmlrpc('','recuperar_correo',parametros) 

	if result:
		return True
	else:
		return False	

def olvido_clave(request):
	print "wtff"
	if request.method == "POST":
		
		print request.POST
		form = form_olvido_clave(request.POST)
		print form
		
		#print " ********* %s ********" %form_cambio_clave.cleaned_data


		if form.is_valid():
			print " ********* %s ********" %form.cleaned_data
			print form.cleaned_data['form_olvido_clave_username']
			usuario_username = form.cleaned_data['form_olvido_clave_username']
			usuario=User.objects.get(username=usuario_username)
			#Se genera un Password aleatorio, se envia al correo y se desactiva el usuario
			#usuario.password = make_password(form_cambio_clave.cleaned_data['clave_usuario'])
			print usuario
			print usuario_username
			recuperar_clave(usuario_username)
			#usuario.is_active = False
			#usuario.save()	
			return HttpResponseRedirect('ingresar.html') 
 			#{'clave_usuario': u'123', 'clave_re_usuario': u'123', 'apellido_usuario': u'', 'nombre_usuario': u'', 'username_usuario': u'hneuman'} 
	d={}
	d['formulario'] = form_olvido_clave()

	return render_to_response('olvido_clave.html',d,context_instance=RequestContext(request))

def definir_xmlrpc_conexion(request):
	print "definir_xmlrpc_conexion"
	if request.method == "POST":
		
		print request.POST
		form = form_xmlrpc_conexion(request.POST)
		print " *-*-*-*-*-*-*-\n \n \n  %s \n \n \n -*-*-*-*-*-*"%form
		print " *-*-*-*-*-*-*-\n \n \n  %s \n \n \n -*-*-*-*-*-*"%form.cleaned_data
		if form.is_valid():
			guardar=form.save(commit=False)

			form.cleaned_data
			guardar.save()

			return HttpResponseRedirect('ingresar.html') 
 			#{'clave_usuario': u'123', 'clave_re_usuario': u'123', 'apellido_usuario': u'', 'nombre_usuario': u'', 'username_usuario': u'hneuman'} 
 		else:
 			print "form no valido \n \n \n \n \n "
	d={}
	d['formulario'] = form_xmlrpc_conexion()
	print d['formulario'] 
	return render_to_response('definir_xmlrpc_conexion.html',d,context_instance=RequestContext(request))