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
	mongo_collection.update({"_id": doc_id}, {"$set": {"str_ident": str(doc_id)}})
	return doc_id

def updateData(data, mongo_collection, mongo_id):
	mongo_collection.update({"_id": ObjectId(mongo_id)}, {"$set": {"calculos": data}})

def getData(mongo_collection, identificador, user_name):
	arcpy.AddMessage(user_name)
	arcpy.AddMessage(identificador)
	data = mongo_collection.find({"user": user_name, "identificador": identificador})
	return data

def getDataCalculo(mongo_connection, collection_name, mongo_id):
	collection = mongo_connection[collection_name]
	data = collection.find_one({"_id": ObjectId(mongo_id)}, {'_id': 0})
	return data

def getUserInfo(token):
	mongo_collection = _initMongoConnection("Calculos", "usuariosTVD")
	data = mongo_collection.find({"_id": ObjectId(token)}, {"_id": 0})
	json_cursor = cursorToJSON(data)
	return json_cursor

def cursorToJSON(data):
	doc = []
	for document in data:
		return document