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
    _nombre_calculo = "xxxxxxxxxxxxx"
    _action = "xxxxxxxxxxxxx"
    _codigo_postulacion = "xxxx"
        
    def __init__(self):
        self.data_calculos = self._data_calculos
        self.identificador = self._identificador
        self.token = self._token
        self.mongo_id = self._mongo_id
        self.nombre_calculo = self._nombre_calculo
        self.action = self._action
        self.codigo_postulacion = self._codigo_postulacion