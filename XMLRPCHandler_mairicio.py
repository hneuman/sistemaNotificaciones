#!/usr/bin/env python
# -*- coding: utf-8 -*-

import SimpleXMLRPCServer
import threading
import xmlrpclib
import socket
import getopt
import signal
import sys
import os
from hashlib import sha256
import hmac
import uuid
import time
from datetime import datetime
from datetime import date
from xmlrpclib import Fault
import psycopg2
import psycopg2.extras
#~ import settings
from hasher import make_password
from xmlrpclib import Binary     
#~ vals = settings.DATABASES['default']
import psycopg2.extensions
from psycopg2.psycopg1 import cursor as psycopg1cursor
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
import base64
#~ from django.db.models import get_model
import decimal
#~ from django.utils.encoding import smart_str
ip = None
port = None
user = None
password = None
EPOCH = 1293840022



class db_connect(object):
      def __init__(self, user, password, host, port, name):
          self.user = user
          self.password = password
          self.host = host
          self.port = port
          self.name = name
      
      def cursor(self):
          self.con = self.conection()
          return self.con.cursor()
     
      def cursor_read(self):
          self.con = self.conection()
          return self.con.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
        
      def conection(self):
          print self.name
          print self.user
          print self.password
          print self.host
          print self.port

          conex = psycopg2.connect(database= self.name, user=self.user , password=self.password, host=self.host, port=self.port)
          return conex
      
      def execute(self, sql):
          con = self.cursor()  
          con.execute(sql)
          return con
          
      def name_columns(self, tabla):
          sql = "select * from %s limit 1" %tabla
          cur = self.cursor()
          cur.execute(sql)
          colnames = [desc[0] for desc in cur.description]
          return colnames
          
      def search(self, tabla, param):
          sql = 'select id from %s ' %tabla
          cont = 0
          condition_a = " AND %s %s %s "
          condition_o = " OR %s %s %s "
          if param:
            for i in param:
                equal = i[3]
                if isinstance(equal, list):
                   equal = tuple(i[3])
                if cont == 0:
                   if isinstance(equal, tuple):     
                      sql = sql + " where %s %s %s" %(i[1], i[2], equal)
                   else:
                       sql = sql + " where %s %s '%s'" %(i[1], i[2], equal)
               
                elif i[0] == "&":
                    sql = sql + condition_a %(i[1], i[2], equal) 
                else:
                    sql = sql + condition_o %(i[1], i[2], equal) 
                cont = cont + 1
        
          print sql 
          result = self.execute(sql)
          result = result.fetchall()
          if result:
             result = [n for i in result for n in i]
          return result
          
      def write(self, ids, tabla, param):
          if not isinstance(ids, list):
              ids = [ids]
          sql = 'UPDATE %s '%tabla
          cont = 0
          for i in  param:
              if cont == 0: 
                sql = sql + "SET %s = '%s'"%(i, param[i])
              else:
                  sql  = sql +', ' + " %s = '%s'" %(i, param[i])
              cont = cont +1 
          if len(ids) == 1: 
             sql = sql + " WHERE id = '%s'" %ids[0]
          else:
               ids = tuple(ids)
               sql = sql + " WHERE id IN %s" %str(ids) 
          print sql 
          result = self.execute(sql)
          self.con.commit()
          return  ids[0]  
          
      def create(self, tabla, param):
          x = []
          y = []
          for i in param:
              y.append(i)
              
          for i in param:
              x.append(param[i])
          
          x = tuple(x)
          y = tuple(y)
          sql = "INSERT INTO %s  %s "%(tabla, y)
          sql = sql.replace("'", '"')
          sql = sql + 'VALUES %s'%str(x)
          print sql 
          result = self.execute(sql)
          self.con.commit()
          id = self.search(tabla, [])
          id.sort()
          return  id[-1]
      
      def unlink(self, tabla, ids):
          if len(ids) == 1:
              sql = "DELETE FROM %s WHERE id = '%s' "%(tabla, ids[0])
          else:
            sql = "DELETE FROM %s WHERE id in  %s "%(tabla, tuple(ids))
          result = self.execute(sql)
          self.con.commit()
          return  True           

      def read(self, tabla, ids):
          if not ids:
             return [] 
          
          if len(ids) == 1:
             sql = "select * from %s WHERE id = '%s'" %(tabla, ids[0])
          else:
              sql = "select * from %s where id IN %s" %(tabla, tuple(ids))
          print sql 
          Cur = self.cursor_read()
          result = Cur.execute(sql)   
          result = Cur.fetchall()
          return result    
     

try:
    import constancia_projecto.settings

    configuracion = constancia_projecto.settings.DATABASES['default']

    print "name == ",configuracion['NAME']
    print "host == ",configuracion['HOST']
    print "port == ",configuracion['PORT']
    print "user == ",configuracion['USER']
    print "pass == ",configuracion['PASSWORD']


    vals = {
    "USER":configuracion['USER'],
    "PASSWORD":configuracion['PASSWORD'],
    "HOST":configuracion['HOST'],
    "PORT":configuracion['PORT'],
    "NAME":configuracion['NAME'],
    }

    db = db_connect(vals['USER'], vals['PASSWORD'], vals['HOST'], vals['PORT'], vals['NAME'])
    db.conection()

except Exception,e:
    print "Error ==>> %s <<==" %e
    print "Error al importar configuracion desde el archivo settings.py"


def require_login(decorated_function):
    def wrapper(self, session_id, *args, **kwargs):
        print decorated_function
        if not self.sessions.has_key(session_id):
            self._clear_expired_sessions() # clean the session dict
            raise Fault("Session ID invalid", "Call login(user, pass) to aquire a valid session")

        last_visit = self.sessions[session_id]["last_visit"]
        
        if is_timestamp_expired(last_visit):
            self._clear_expired_sessions() # clean the session dict
            raise Fault("Session ID expired", "Call login(user, pass) to aquire a valid session")

        self.sessions[session_id]["last_visit"] = get_timestamp()
        return decorated_function(self, session_id, *args, **kwargs)

    return wrapper

def timestamp_to_datetime(timestamp):

    return datetime.utcfromtimestamp(timestamp + EPOCH)

def is_timestamp_expired(timestamp, max_age = 2700): # maxage in seconds (here: 2700 = 45 min)
    age = get_timestamp() - timestamp
    if age > max_age:
        return True
    return False

def get_timestamp():
    return int(time.time() - EPOCH)

class myServerFunction(object):
    
    def __init__(self, args):
        self.users  = args
        self.sessions  = dict()
        self.session_key = os.urandom(32)
    
    def _find_session_by_username(self, username):

        for session in self.sessions.itervalues():
            if session["username"] == username:
                return session

    def _invalidate_session_id(self, session_id):

        try:
            del self.sessions[session_id]
        except KeyError:
            pass

    def _clear_expired_sessions(self):
       

        for session_id in self.sessions.keys():
            last_visit = self.sessions[session_id]["last_visit"]
            if is_timestamp_expired(last_visit):
                self._invalidate_session_id(session_id)

    def _generate_session_id(self, username):
        return hmac.new(self.session_key, username + str(uuid.uuid4()), sha256).hexdigest()

    def login(self, username, password):
        session = self._find_session_by_username(username)
	if session:
            if is_timestamp_expired(session["last_visit"]):
                self._invalidate_session_id(session["session_id"])
            else:
                return session["session_id"]
 	
	if self.users.has_key(username):
	   if self.users[username] == password:
                session_id = self._generate_session_id(username)
                self.sessions[session_id] = {"username"  : username,
                                             "session_id": session_id,
                                             "last_visit": get_timestamp()}
                
                return session_id

        raise Fault("unknown username or password", "Please check your username and password")    
    
        
    
    @require_login   
    def search(self,  session_id, tabla, args):
        ids = db.search(tabla, args)
        return ids
        
    @require_login   
    def write(self,  session_id, ids, tabla, args):
        #~ try:
        result = db.write(ids, tabla, args) 
        return result
        #~ except:
            #~ return False     
        
    @require_login   
    def create(self,  session_id, tabla, args):
        cr =  db.create(tabla, args)
        return cr
        
    @require_login   
    def read(self,  session_id, tabla, ids):
        l = []
        l_result = []
        colms = db.name_columns(tabla)
        result =  db.read(tabla, ids)
        try:
            for r in result:
                d = {}
                for c in colms:
                    d.update({c:getattr(r, c)})
                l.append(d)    
        except:
            pass
        for i in l:
            for d in i:
                if isinstance(i[d], decimal.Decimal):
                   i[d] = round(i[d], 2)
                if isinstance(i[d], psycopg2.tz.FixedOffsetTimezone):
                   i[d] = i[d].tzname('UTC')
                if isinstance(i[d], datetime):
                   i[d] = i[d].strftime('%Y-%m-%d')
                
                if isinstance(i[d], date):
                   i[d] = i[d].strftime('%Y-%m-%d')
                
                if i[d] == None:
                   i[d] = str(i[d])
                   
            l_result.append(i)
        return l_result
        
    @require_login   
    def name_columns(self,  session_id, tabla):
        result =  db.name_columns(tabla)
        return result 
        
    @require_login   
    def unlink(self,  session_id,  ids, tabla):
        result =  db.unlink(tabla, ids)
        return result 
        
    @require_login   
    def send_back_binary(self,  session_id,  bin, name, ext):
        result =  db.send_back_binary(bin, name, ext)
        if result:
           return result[1:] 
        return result
    
    #~ @require_login   
    #~ def status_oscar( self,  session_id):
        #~ result =  settings.OSCAR_STATUS_SPANISH
        #~ return result
    
    @require_login   
    def hola_mundo(self, session_id):
        print session_id
        print "oh may gad, eres mai foquing jirou"    
        return "oh may gad, eres mai foquing jirou"
    
    @require_login   
    def notificar_procesado(self,session_id,solicitud):

        try:
            conn = psycopg2.connect("dbname='%s' user='%s' host='%s' password='%s' port='%s' "%(vals['NAME'],vals['USER'],vals['HOST'],vals['PASSWORD'],vals['PORT']))
            print "conectado"
            cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
            
            print solicitud
            for s in solicitud:
                print s
                cur.execute("INSERT INTO outbox(\"DestinationNumber\", \"TextDecoded\", \"CreatorID\", \"Class\") VALUES ('%s', '%s', 'Gammu', '-1')"%(s['telefono'],s['texto'])) 
                cur.execute("UPDATE solicitudes_pendientes SET \"Procesado\" = 'False' WHERE \"cedula\" = '%s'"%str(s['cedula']))
            conn.commit()
        except Exception,e:
            print "No se pudo notificar via Telefonica"
            print e	
            return False
        return True

        

class serverThread(threading.Thread):
    def __init__(self, ip, port, args):
        self.ip = ip
        self.port = port 
        self.args = args
        threading.Thread.__init__(self)
        self.timeToQuit = threading.Event()
        self.timeToQuit.clear()      
    
    def check(self,ip, port):
        gotod = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            gotod.settimeout(5)
            gotod.connect((ip, int(port)))
            gotod.shutdown(2)
            gotod.close()
            return True
        except:
            return False
    
    
    def stop(self):    
        self.server.server_close()
        self.timeToQuit.set()

    def run(self):
        print "running server XML-RPC %s %s" %(self.ip, self.port)
        self.server = SimpleXMLRPCServer.SimpleXMLRPCServer( (str(self.ip), self.port), logRequests=False )
        self.server.register_function(make_password, 'create_password')
        #self.server.register_function(restart_server)
        self.server.register_instance(myServerFunction(self.args))
        while not self.timeToQuit.isSet():
            self.server.handle_request()
    

def init(ip, port, args):
    t = serverThread(ip, port, args)
    if not t.check(ip, port):
        #~ t.daemon = True
        t.start()
    else:
        print "servidor corriendo"
try:
   ids = db.search('constancia_app_apps_web_service', [('&', 'valido', '=', True)])
except:
    ids = [] 
print ids
    
if  ids:
    read = db.read('constancia_app_apps_web_service', ids)[0]
    user = read.user_web  
    passwd = read.password
    active = read.valido
    ip = read.ip
    port = read.port
    login = {user:passwd}
    init(ip, int(port), login)
    
  
    
