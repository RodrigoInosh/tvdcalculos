# -*- coding: iso-8859-15 -*-
'''
Created on 12-02-2014

@author: CRodriguez
'''
import arcpy

class JSONFormulario:
    # PARAMETROS POR DEFECTO - CAMBIAR SEGUN TIPO DE SERVICIO AM,FM, RCC, ISDBT o UHF
    _data_calculos = {}
    _identificador = ""
    _token = "xxxxxxxxxxxxx"
    _mongo_id = "xxxxxxxxxxxxx"
        
    def __init__(self):
        self.data_calculos = self._data_calculos
        self.identificador = self._identificador
        self.token = self._token
        self.mongo_id = self._mongo_id