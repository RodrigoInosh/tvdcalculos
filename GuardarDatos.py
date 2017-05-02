# -*- coding: utf-8 -*-
'''
Created on 27-04-2017

@author: RInostroza
'''

import arcpy
import JSONFormulario
import json
import sys
import DBMongo
from pymongo import MongoClient
from bson.objectid import ObjectId

params = JSONFormulario.JSONFormulario()
mongo_connection = DBMongo._initMongoConnection("Calculos")

def getParameters():
	params.data_calculos = arcpy.GetParameterAsText(0)
	params.identificador = arcpy.GetParameterAsText(1)
	params.token = arcpy.GetParameterAsText(2)
	params.mongo_id = arcpy.GetParameterAsText(3)
	params.nombre_calculo = arcpy.GetParameterAsText(4)
	params.action = arcpy.GetParameterAsText(5)

def validateValueInCollection(data, collection_name, mongo_id):
	arcpy.AddMessage(collection_name)
	if mongo_id == "0":
		DBMongo.saveData(data, mongo_connection, collection_name)
	else:
		DBMongo.updateData(data["calculos"], mongo_connection, collection_name, mongo_id)

getParameters()


#CREAR FUNCIÓN PARA OBTENER LA INFORMACIÓN DEL USUARIO EN BASE AL TOKEN.
user_data = "RodrigoInostroza"#getUserInfo(token)

json = {"nombre": params.nombre_calculo, "user": user_data, "identificador": params.identificador, "calculos": [json.loads(params.data_calculos)]}
validateValueInCollection(json, user_data, params.mongo_id)

arcpy.SetParameterAsText(6, "ok")