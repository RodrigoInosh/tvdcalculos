# -*- coding: utf-8 -*-
'''
Created on 27-04-2017

@author: RInostroza
'''

import arcpy
import json
import JSONFormulario
import sys
import DBMongo
from pymongo import MongoClient
from bson.objectid import ObjectId

params = JSONFormulario.JSONFormulario()
mongo_connection = DBMongo._initMongoConnection("Calculos")

def getParameters():
	params.identificador = arcpy.GetParameterAsText(0)
	params.token = arcpy.GetParameterAsText(1)

getParameters()
#CREAR FUNCIÓN PARA OBTENER LA INFORMACIÓN DEL USUARIO EN BASE AL TOKEN.

user_data = "RodrigoInostroza"#getUserInfo(token)

datos = DBMongo.getData(mongo_connection, user_data, params.identificador)

json_response = []
for item in datos:
	mongo_id = item.get('str_ident')
	nombre = item.get('nombre')
	json_response.append({'mongo_id': mongo_id, 'nombre': nombre})

json = json.dumps(json_response)
arcpy.SetParameterAsText(2, json)