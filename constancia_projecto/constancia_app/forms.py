from django import forms
from constancia_projecto.constancia_app.models import *
from django.forms import ModelForm

class cambio_clave(forms.Form):
    username_usuario =  forms.CharField(label='Nombre de Usuario', max_length=100,required=False, widget=forms.TextInput(attrs={'readonly':'readonly'}) )
    nombre_usuario = forms.CharField(label='Nombre', max_length=100,required=False)
    apellido_usuario = forms.CharField(label='Apellido', max_length=100,required=False)
    clave_usuario = forms.CharField(label='Clave', max_length=100,required=False)
    clave_re_usuario = forms.CharField(label='Confirmar Clave', max_length=100,required=False)

    readonly_fields = ('username_usuario',)


class form_olvido_clave(forms.Form):
    form_olvido_clave_username =  forms.CharField(label='Usuario', max_length=100,required=False,  )

class form_xmlrpc_conexion(ModelForm):
	class Meta:
		model = Conexion_xmlrpc
		exclude = []

class form_validar_solicitud(forms.Form):
    form_field_codigo =  forms.CharField(label='Codigo de Solicitud', max_length=100,required=False, help_text="Ingrese el codigo de la Solicitud a validar" )

class form_consultar_carnet(forms.Form):
    codigo_trabajador =  forms.CharField(label='Codigo del Trabajador', max_length=100,required=False, help_text="Ingrese el codigo del Trabajador a validar" )

class form_consultar_cedula(forms.Form):
    cedula_trabajador =  forms.CharField(label='Cedula del Trabajador', max_length=100,required=False, help_text="Ingrese La Cedula del Trabajador a validar" )


class crear_usuario(forms.Form):
    username_usuario =  forms.CharField(label='Numero de Cedula', max_length=100, widget=forms.TextInput(attrs={'readonly':'readonly'}))
    nombre_usuario = forms.CharField(label='Nombre', max_length=100, widget=forms.TextInput(attrs={'readonly':'readonly'}))
    apellido_usuario = forms.CharField(label='Apellido', max_length=100, widget=forms.TextInput(attrs={'readonly':'readonly'}))
    clave_usuario = forms.CharField(label='Clave', max_length=100,required=False)
    clave_re_usuario = forms.CharField(label='Confirmar Clave', max_length=100,)
    correo_usuario = forms.CharField(label='Correo Electronico', max_length=100,)
    correo_re_usuario = forms.CharField(label='Confirmar Correo Electronico', max_length=100,)
    exclude = []
