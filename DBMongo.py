# -*- coding: utf-8 -*-
import arcpy
import json
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson import json_util
from bson.json_util import dumps

def _initMongoConnection(database_name, collection_name):
	mongoClient = MongoClient('172.30.10.203', 27017)
	db = mongoClient[database_name]
	collection = db[collection_name]
	return collection

def saveData(data, mongo_collection):
	doc_id = mongo_collection.insert(data)
	arcpy.AddMessage(doc_id)
	mongo_collection.update({"_id": doc_id}, {"$set": {"mongo_id": str(doc_id)}})
	return doc_id

def updateData(data, mongo_collection, mongo_id):
	mongo_collection.update({"_id": ObjectId(mongo_id)}, {"$set": {"calculos": data}})

def getData(mongo_collection, identificador, user_name):
	arcpy.AddMessage(user_name);
	data = mongo_collection.find({"user": user_name, "identificador": identificador}, {'mongo_id': 1, 'nombre': 1})
	return data

def getDataCalculo(mongo_collection, mongo_id):
	data = mongo_collection.find_one({"_id": ObjectId(mongo_id)}, {'_id': 0})
	return data

def getUserInfo(token):
	mongo_collection = _initMongoConnection("Calculos", "usuariosTVD")
	data = mongo_collection.find_one({"id": int(token)}, {"_id": 0})
	return data

def setDataAsDefinitive(data, mongo_id, user_name, codigo_postulacion):
	mongo_collection = _initMongoConnection("Calculos", "datosTecnicosCNTV")

	datos_calculos = data.get("calculos")[0]
	identificador = data.get("identificador")
	intensidad = datos_calculos.get("pIntensidad")
	sist_radiante = datos_calculos.get("form_data").get("carac_tecnicas").get("sist_radiante")
	estudio = getTipoEstudio(datos_calculos.get("form_data"))

	data["definitivo"] = "1";
	data["estudio"] = estudio
	data["codigo_postulacion"] = codigo_postulacion

	query_conditions = {"identificador": identificador, "user": user_name, "definitivo": "1", "estudio": estudio, "calculos.form_data.carac_tecnicas.sist_radiante": sist_radiante, 
		"calculos.pIntensidad": intensidad, "codigo_postulacion": codigo_postulacion}
	arcpy.AddMessage(query_conditions)
	try:
		sistema_radiante = datos_calculos.get("form_data").get("carac_tecnicas").get("sist_radiante")
	except:
		sistema_radiante = ""
		arcpy.AddMessage("Sistema radiante no guardado")

	data_exists = validarExisteDefinitivo(mongo_collection, query_conditions)
	eliminarValorDefinitivo(mongo_collection, query_conditions, data_exists)
	guardarDatosCalculoDefinitivo(mongo_id, data, mongo_collection, query_conditions, data_exists)

def validarExisteDefinitivo(mongo_collection, query_conditions):
	data_exists = ""
	data = mongo_collection.find_one(query_conditions, {'_id': 0, 'user': 1})

	try:
		data.get("user")
		data_exists = "existe"
	except:
		data_exists = ""

	return data_exists

def eliminarValorDefinitivo(mongo_collection, query_conditions, data_exists):

	if data_exists == "existe":
		arcpy.AddMessage("Hay que eliminar valor")
		query_execute = mongo_collection.delete_one(query_conditions)
		# query_execute = mongo_collection.update(query_conditions, {"$unset": {"calculos.$.definitivo": "true"}})
	else:
		arcpy.AddMessage("No existia un definitivo previo")

def guardarDatosCalculoDefinitivo(mongo_id, data, mongo_collection, query_conditions, data_exists):
	# if mongo_id == '0':
		saveData(data, mongo_collection)
	# else:
	# 	mongo_collection.update({"_id": ObjectId(mongo_id)}, data)

def getTipoEstudio(form_data):
	tipo_estudio = "estudio_principal"
	estudio_principal_lng = form_data.get("estudio_principal").get("longitud")
	estudio_alternativo_lng = form_data.get("estudio_alternativo").get("longitud")

	if estudio_principal_lng != '':
		arcpy.AddMessage("Is principal")
		tipo_estudio = 'estudio_principal'

	elif estudio_alternativo_lng != '':
		arcpy.AddMessage("Is alternativo")
		tipo_estudio = 'estudio_alternativo'

	else:
		arcpy.AddMessage("Is empty")
		tipo_estudio = 'estudio_principal'

	return tipo_estudio