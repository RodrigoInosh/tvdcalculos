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
mongo_collection = DBMongo._initMongoConnection("Calculos", "calculosTVD")

def getParameters():
	params.mongo_id = arcpy.GetParameterAsText(0)
	params.token = arcpy.GetParameterAsText(1)
	return params

getParameters()

datos = DBMongo.getDataCalculo(mongo_collection, params.mongo_id)
json = json.dumps(datos)
arcpy.SetParameterAsText(2, json)