#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
from os import listdir
import json
import base64
import cgi
import re

hostname = 'kimsuffi1-api.westelynck.fr'

arguments = cgi.FieldStorage()
rootDir = '/download'

pattern1 = re.compile(rootDir)

def get_size(start_path = '.'):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size

def getPathContent(path):
    result = []
    contents = listdir(path)
    for content in sorted(contents):
        if os.path.isfile("{}/{}".format(path,content)):
    	    result.append({
                    'name':content,
                    'type':'file',
                    'last_modification': os.path.getmtime("{}/{}".format(path,content)),
                    'size': os.path.getsize(("{}/{}".format(path,content))),
                    'id': str(base64.b64encode(("{}/{}".format(path,content)).encode("utf-8")), "utf-8"),
                    'link': 'https://{}{}/{}'.format(hostname,path,content)
                })
        elif os.path.isdir("{}/{}".format(path,content)):
            dir = {
                    'name':content,
                    'type':'directory',
                    'last_modification': os.path.getmtime("{}/{}".format(path,content)),
                    'size': self.get_size("{}/{}".format(path,content)),
                    'id': str(base64.b64encode(("{}/{}".format(path,content)).encode("utf-8")), "utf-8"),
                    'content' : getPathContent("{}/{}".format(path,content))
                }
            result.append(dir)
    return result

def getParents(path):
    parents = {}
    splitPath =  re.sub(rootDir,'',path).split('/')
    pathToID = rootDir
    for rep in splitPath:
        if rep != '':
            pathToID = "{}/{}".format(pathToID,rep)
            parents[rep] = {'id': str(base64.b64encode(pathToID.encode("utf-8")),"utf-8")}
    return parents
	
	
if( 'id' in arguments.keys()):
    try:
        path= str(base64.b64decode(arguments['id'].value),"utf-8")
        if not os.path.isdir(path):
            path = rootDir
    except:
        path = rootDir
else:
    path = rootDir


result = {'parents' : getParents(path), 'content' : getPathContent(path)}

print('Content-Type: application/json\nAccess-Control-Allow-Origin: *\n') 
print(json.dumps(result))
