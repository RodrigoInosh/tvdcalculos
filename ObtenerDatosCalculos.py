# -*- coding: utf-8 -*-
'''
Created on 02-05-2017

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
	params.mongo_id = arcpy.GetParameterAsText(0)
	params.token = arcpy.GetParameterAsText(1)
	return params

getParameters()
#CREAR FUNCIÓN PARA OBTENER LA INFORMACIÓN DEL USUARIO EN BASE AL TOKEN.

user_data = "RodrigoInostroza"#getUserInfo(token)

datos = DBMongo.getDataCalculo(mongo_connection, user_data, params.mongo_id)
json = json.dumps(datos)
arcpy.SetParameterAsText(2, json)