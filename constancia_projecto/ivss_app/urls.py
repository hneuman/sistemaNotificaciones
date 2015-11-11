"""constancia_projecto.ivss_app URL Configuration

"""
from django.contrib import admin
from django.conf.urls import patterns, include, url
#urlpatterns = [
#    url(r'^admin/', include(admin.site.urls)),
#]

urlpatterns = patterns('constancia_projecto.ivss_app.views',


	(r'^ivss/?$',"main")
	
	)
