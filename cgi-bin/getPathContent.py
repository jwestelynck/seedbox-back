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

def getPathContent(path):
    result = []
    contents = listdir(path)
    for content in sorted(contents):
        if os.path.isfile("{}/{}".format(path,content)):
    	    result.append({
                    'name':content,
                    'type':'file',
                    'size': os.path.getsize(("{}/{}".format(path,content))),
                    'id': str(base64.b64encode(("{}/{}".format(path,content)).encode("utf-8")), "utf-8"),
                    'link': 'https://{}{}/{}'.format(hostname,path,content)
                })
        elif os.path.isdir("{}/{}".format(path,content)):
            dir = {
                    'name':content,
                    'type':'directory',
                    'size': 0,
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
