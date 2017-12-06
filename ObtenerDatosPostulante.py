import arcpy
import json
import JSONFormulario
import DBMongo
from pymongo import MongoClient
from bson.objectid import ObjectId

params = JSONFormulario.JSONFormulario()
mongo_collection = DBMongo._initMongoConnection("Calculos", "calculosTVD")

def getParameters():
	params.identificador = arcpy.GetParameterAsText(0)
	params.token = arcpy.GetParameterAsText(1)

getParameters()
#CREAR FUNCIÓN PARA OBTENER LA INFORMACIÓN DEL USUARIO EN BASE AL TOKEN.

user_data = DBMongo.getUserInfo(params.token)
user_name = user_data.get("nombre")

arcpy.AddMessage("Token:"+ str(params.token))
datos = DBMongo.getData(mongo_collection, params.identificador, params.token)

json_values = []
for item in datos:
	mongo_id = item.get('str_ident')
	nombre = item.get('nombre')
	json_values.append({'mongo_id': mongo_id, 'nombre': nombre})

json_response = json.dumps(json_values)
arcpy.SetParameterAsText(2, json_response)