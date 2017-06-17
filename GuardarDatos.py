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
mongo_collection = DBMongo._initMongoConnection("Calculos", "calculosTVD")
calculos = {}
inserted_id = 0
status = ""

def getParameters():
	params.data_calculos = arcpy.GetParameterAsText(0)
	params.identificador = arcpy.GetParameterAsText(1)
	params.token = arcpy.GetParameterAsText(2)
	params.mongo_id = arcpy.GetParameterAsText(3)
	params.nombre_calculo = arcpy.GetParameterAsText(4)
	params.action = arcpy.GetParameterAsText(5)
	arcpy.AddMessage(params.action)

def validateValueInCollection(data, user_name, mongo_id):
	arcpy.AddMessage(user_name)
	arcpy.AddMessage(params.action)
	if params.action == "definitive":
		params.codigo_postulacion = arcpy.GetParameterAsText(6)
		global status
		global inserted_id
		status = "saved"
		DBMongo.setDataAsDefinitive(data, mongo_id, user_name, params.codigo_postulacion)
	else:
		if mongo_id == "0":
			global status
			global inserted_id
			status = "saved"
			inserted_id = DBMongo.saveData(data, mongo_collection)
		else:
			global status
			status = "updated"
			DBMongo.updateData(data["calculos"], mongo_collection, mongo_id)

def formatCoordinates(calculos):
	latitud = calculos["pLatitud"]
	arcpy.AddMessage(latitud)
	longitud = calculos["pLongitud"]
	setFormattedCoordinate(latitud, "Latitud")
	setFormattedCoordinate(longitud, "Longitud")

def setFormattedCoordinate(decimal_coordinate, coordinate_name):
	splitted_coordinate = decimal_coordinate.split(" ")
	calculos["p"+coordinate_name+"Degress"] = splitted_coordinate[0][:-1]
	calculos["p"+coordinate_name+"Minutes"] = splitted_coordinate[1][:-1]
	calculos["p"+coordinate_name+"Seconds"] = splitted_coordinate[2][:-2]

getParameters()

#CREAR FUNCIÓN PARA OBTENER LA INFORMACIÓN DEL USUARIO EN BASE AL TOKEN.

user_data = DBMongo.getUserInfo(params.token)
arcpy.AddMessage(user_data)
json_response = []
try:
	user_name = user_data.get("nombre")
	calculos = json.loads(params.data_calculos)
	formatCoordinates(calculos)
	json_request = {"nombre": params.nombre_calculo, "user": user_name, "identificador": params.identificador, "calculos": [calculos], "datos": [json.loads(json.dumps(user_data))]}
	validateValueInCollection(json_request, user_name, params.mongo_id)
	test = {"status": status, "nombre": str(params.nombre_calculo), "mongo_id": str(inserted_id)}
	json_response = json.dumps(test)
except AttributeError:
	test = {"status": "usuario no existe"}
	arcpy.AddMessage("fdgdfh")
	json_response = json.dumps(test)

arcpy.AddMessage("json_response")
arcpy.AddMessage(json_response)
arcpy.SetParameterAsText(7, json_response)