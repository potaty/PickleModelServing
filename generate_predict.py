#!/usr/bin/env python
import os
import sys
import json
import random
import subprocess

x = '''
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path(\''''

y = '''/', include(\''''

z = '''.urls')),
    path('admin/\', admin.site.urls),
]
'''

appsx = '''

from django.apps import AppConfig


class '''

appsy = '''Config(AppConfig):
    name = \''''

appsz = '\''

urls = '''
from djangoserving.urls import path

from . import views

urlpatterns = [
     path('', views.index, name='index')
]
'''

viewsx = '''
from django.http import HttpResponse
import json
import pickle
import pandas as pd
from django.views.decorators.csrf import ensure_csrf_cookie

@ensure_csrf_cookie
def index(request):
    a = {}
    if request.method == 'POST':
        a = json.loads(request.body.decode())
    load_model = pickle.load( open( "'''
viewsy = '''/model.pk", "rb" ) )
    ans = load_model.predict(pd.DataFrame.from_dict(a)) 
    a = HttpResponse(json.dumps('{ "response": ' + str(ans) + '}'))
    a["Access-Control-Allow-Origin"] = "*" 
    a["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS" 
    a["Access-Control-Max-Age"] = "1000"
    a["Access-Control-Allow-Headers"] = "*"
    return a
'''

admin = '''
from django.contrib import admin

# Register your models here.
'''

models = '''
from django.db import models

# Create your models here.
'''

tests = '''
from django.test import TestCase

# Create your tests here.
'''

def write_file(filename, filecontent):
    file = open(filename, "w")
    file.write(filecontent)

def read_json(filename):
    if filename:
        with open(filename, 'r') as f:
            return json.load(f)

if __name__ == "__main__":
    model_name = read_json(sys.argv[1] + '/feature_names.json')["model_name"]
    print(model_name)
    try:
        os.makedirs(model_name)
        os.makedirs(model_name + '/migrations')
    except:
        print("Sorry, this model name is in use now")
    write_file(model_name + "/__init__.py", "")
    write_file(model_name + "/" + "migrations" + "/__init__.py", "")
    write_file("djangoserving/" + "urls.py", x + model_name + y + model_name + z)
    write_file(model_name + "/apps.py", appsx + model_name.capitalize() + appsy + model_name + appsz)
    write_file(model_name + "/urls.py", urls)
    write_file(model_name + "/views.py", viewsx + sys.argv[1] + viewsy)
    write_file(model_name + "/admin.py", admin)
    write_file(model_name + "/models.py", models)
    write_file(model_name + "/tests.py", models)
    port = 8221
    run_wsgi = ['uwsgi', '--http', ':' + str(port), '--module', 'djangoserving.wsgi']
    write_file(sys.argv[2], ":" + str(port) + "/" + model_name + "/")
    print(port)
    subprocess.Popen(run_wsgi).wait()
