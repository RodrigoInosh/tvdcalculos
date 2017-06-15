# -*- coding: utf-8 -*-
'''
Created on 27-04-2017
Last modification 02-05-2017
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
mongo_collection = DBMongo._initMongoConnection("Calculos", "calculosTVD")

def getParameters():
	params.identificador = arcpy.GetParameterAsText(0)
	params.token = arcpy.GetParameterAsText(1)

def getInfoEmpresa(data):
	datos_empresa = data.get("empresa") 
	representante = data.get("representanteLegal") 

	razon_social = datos_empresa.get("razonSocial")
	rut = datos_empresa.get("rut")
	direccion = datos_empresa.get("direccion")
	comuna = datos_empresa.get("comuna")
	region = datos_empresa.get("region")
	email = representante.get("email")
	fono = representante.get("telefonoFijo")
	json_info = {'razon': razon_social, 'rut': rut, 'direccion': direccion, 'comuna': comuna, 'region': region, 'email': email, 'fono': fono}

	return json.dumps(json_info)

getParameters()

user_data = DBMongo.getUserInfo(params.token)
user_name = user_data.get("nombre")
empresa_info = getInfoEmpresa(user_data)

datos = DBMongo.getData(mongo_collection, params.identificador, user_name)

json_values = []
json_values.append({'empresa': json.loads(empresa_info)})
for item in datos:
	mongo_id = item.get('mongo_id')
	nombre = item.get('nombre')
	json_values.append({'mongo_id': mongo_id, 'nombre': nombre})

json_response = json.dumps(json_values)
arcpy.AddMessage(json_response)
arcpy.SetParameterAsText(2, json_response)