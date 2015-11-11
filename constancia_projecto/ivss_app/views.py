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
from django.contrib.auth.decorators import login_required
#para "ASEGURAR LAS COOKIES"
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.csrf import csrf_protect





# Create your views here.

def main(request):
	return render_to_response("main.html",context_instance=RequestContext(request))
