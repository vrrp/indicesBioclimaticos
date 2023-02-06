#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 26 14:45:20 2023

@author: victor
"""
# TIPOS DE DATOS
#---------------------------------------------------------------
# Cadena de caracteres (str, no numericos)
var1 = "hola"
var2 = "2023"
print(type(var1), type(var2))
print(var1, var2)

var3 = var1+var2
print(type(var3))
var3

# Numericos (int, float)
num1 = 2023
num2 = 0.5
print(type(num1), type(num2))
print(num1, num2)

num3 = num1+num2
print(type(num3))
print(num3)

# ESTRUCTURA DE DATOS DE DATOS
#---------------------------------------------------------------
# Listas
l1 = ["hola", "2023"]
l2 = ["feliz", "año", 2023]
l3 = [1981, 2016]
print(type(l2))
print(l2)
print(len(l2), len(l3))

# arrays
import numpy as np

ar1D = np.arange(24)
ar2D = ar1D.reshape(4,6)
ar3D = ar1D.reshape(3,4,2)
print(type(ar1D), type(ar2D), type(ar3D))
print(np.shape(ar1D), np.shape(ar2D), np.shape(ar3D))

# data frames
import pandas as pd
"""
path_excel_file = "/home/data/senamhi/indices_bioclimaticos/data/" # Linux
cols_names = ["ESTACION", "TIPO", "LON_DEC", "LAT_DEC", "ALTITUD"]

df_aws = pd.read_excel(path_excel_file+"codigos_aws_san_martin.xls",
                       usecols=cols_names,
                       sheet_name="Hoja1")
print(type(df_aws))
print(df_aws)
"""
# Diccionarios
dic = dict(#data = df_aws,
           proyecto = "SENAMHI ENANDES",
           lista1 = l1,
           array = ar3D,
          )

print(dic)
print(type(dic))
print(dic["proyecto"])
print(dic["array"])


# EXPLORAR: MODULOS Y PAQUETES
#---------------------------------------------------------------
# numpy
print(np.__doc__)

# pandas
print(pd.__doc__)

# indices_bioclimaticos
import indices_bioclimaticos as iibb

print(iibb.__doc__)
print(iibb.extraer.__doc__)

print(iibb.indices_termicos.__doc__)

print(iibb.indices_hidricos.__doc__)


