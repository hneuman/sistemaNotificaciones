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
    form_olvido_clave_username =  forms.CharField(label='Nombre de Usuario', max_length=100,required=False,  )

class form_xmlrpc_conexion(ModelForm):
	class Meta:
		model = Conexion_xmlrpc
		exclude = []
