import arcpy
import JSONFormulario
import json
import sys
from pymongo import MongoClient
from bson.objectid import ObjectId

#Tirar a otra clase
def _initMongoConnection(database_name):
	mongoClient = MongoClient('172.30.10.203', 27017)
	db = mongoClient[database_name]
	return db

params = JSONFormulario.JSONFormulario()
mongo_connection = _initMongoConnection("Calculos")

#Tirar a otra clase
def saveData(data):
	collection = mongo_connection[params.identificador]
	collection.insert(data)
	# doc_id = collection.insert_one(data).inserted_id

#Tirar a otra clase
def updateData(data, mongo_id):
	collection = mongo_connection[params.identificador]
	arcpy.AddMessage(data)
	collection.update({"_id": ObjectId(mongo_id)}, {"$set": {"calculos": data}})
	# doc_id = coll.insert_one(doc).inserted_id

def getParameters():
	params.data_calculos = arcpy.GetParameterAsText(0)
	params.identificador = arcpy.GetParameterAsText(1)
	params.token = arcpy.GetParameterAsText(2)
	params.mongo_id = arcpy.GetParameterAsText(3)

def validateValueInCollection(data, mongo_id):
	arcpy.AddMessage(mongo_id)
	if mongo_id == "0":
		saveData(data)
	else:
		updateData(data["calculos"], mongo_id)

getParameters()


#CREAR FUNCIÓN PARA OBTENER LA INFORMACIÓN DEL USUARIO EN BASE AL TOKEN.
#user_data = getUserInfo(token)
arcpy.AddMessage(params.data_calculos)
arcpy.AddMessage(params.identificador)
arcpy.AddMessage(params.token)
arcpy.AddMessage(params.mongo_id)

json = {"user": "user1", "identificador": "dfsdfd", "calculos": [json.loads(params.data_calculos)]}
validateValueInCollection(json, params.mongo_id)

# insertData(json, params.identificador)
# insertData(json.loads(params.form_general_concurso))
# insertData(json.loads(params.form_general_modificacion))

arcpy.SetParameterAsText(3, "params")