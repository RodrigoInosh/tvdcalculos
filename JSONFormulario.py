# -*- coding: utf-8 -*-
'''
Created on 27-04-2017

@author: RInostroza
'''
import arcpy

class JSONFormulario:
    _data_calculos = {}
    _identificador = ""
    _token = "xxxxxxxxxxxxx"
    _mongo_id = "xxxxxxxxxxxxx"
        
    def __init__(self):
        self.data_calculos = self._data_calculos
        self.identificador = self._identificador
        self.token = self._token
        self.mongo_id = self._mongo_id