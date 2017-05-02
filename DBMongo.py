# -*- coding: utf-8 -*-
import arcpy
from pymongo import MongoClient
from bson.objectid import ObjectId

def _initMongoConnection(database_name):
	mongoClient = MongoClient('172.30.10.203', 27017)
	db = mongoClient[database_name]
	return db

def saveData(data, mongo_connection, collection_name):
	collection = mongo_connection[collection_name]
	doc_id = collection.insert(data)
	collection.update({"_id": doc_id}, {"$set": {"str_ident": str(doc_id)}})
	return doc_id

def updateData(data, mongo_connection, collection_name, mongo_id):
	collection = mongo_connection[collection_name]
	collection.update({"_id": ObjectId(mongo_id)}, {"$set": {"calculos": data}})

def getData(mongo_connection, collection_name, identificador):
	collection = mongo_connection[collection_name]
	data = collection.find({"identificador": identificador})
	return data

def getDataCalculo(mongo_connection, collection_name, mongo_id):
	collection = mongo_connection[collection_name]
	data = collection.find_one({"_id": ObjectId(mongo_id)}, {'_id': 0})
	return data