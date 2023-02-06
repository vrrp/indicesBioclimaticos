import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import indices_bioclimaticos as iibb

# Linux
#------------------------------------------------------------------------
#data_path= "/home/data/senamhi/pisco_data/"                
#shapes_path="/home/data/shape/depart_san_martin/"
#img_path = "/home/data/senamhi/indices_bioclimaticos/img/"

# Windows
#------------------------------------------------------------------------
data_path= "C:/Users/Victor/Documents/taller_iibb/data/"    
shapes_path= "C:/Users/Victor/Documents/taller_iibb/shapes/"
img_path =  "C:/Users/Victor/Documents/taller_iibb/img/"
file_name = "pisco_v2p1_airtemp_san_martin.nc"

# leer archivo netcdf
#------------------------------------------------------------------------
fo = iibb.extraer(data_path, file_name)
fo.data_info()

# Extraer variables
#------------------------------------------------------------------------
temp_min = fo.variable(nombre_var="airtemp_min", rango_tiempo=['1998-07-01','1999-09-21']) # yyyy-mm-dd
temp_max = fo.variable(nombre_var="airtemp_max", rango_tiempo=['1998-07-01','1999-09-21']) # yyyy-mm-dd

# Determinar indice bioclimatico
#------------------------------------------------------------------------
"""
temp umbral
[22, 28]
[22, 26] Robusta
[18, 24] Arabica
"""
ii_tt = iibb.indices_termicos(temp_min, temp_max)
temp_optima, temp_optima_3clases = ii_tt.aptitud_termica_map(temp_umbral=[22,26])

print(np.min(temp_optima.data), np.max(temp_optima.values))
#print(np.min(temp_optima_3clases.data), np.max(temp_optima_3clases.values))

# graficar mapa de indice 
#------------------------------------------------------------------------
img_mapa = dict(data=temp_optima,
                titulo_derecha = "01 Julio 1998 - 21 Setiembre 1999",
                titulo_izquierda =None,
                cb_rango= [5, 35, 5],
                tipo_cbar="hot_r",
                cb_nombre="Índice de aptitud térmica",                
                img_path = img_path,
                shp_path = shapes_path,
                img_save_name =None,#"MAP_TEMP_OPTIMA_JUL1998_SET1999_win",
                )
iibb.graficar_mapa(img_mapa)

# graficar mapa de 3 clases
#------------------------------------------------------------------------
img_mapa_3clases = dict(data=temp_optima_3clases,
                titulo_derecha = "01 Julio 1998 - 21 Setiembre 1999",
                titulo_izquierda =None,
                cb_rango= [0, 3, 1],
                tipo_cbar=None,
                cb_nombre="Índice de aptitud térmica",                
                img_path = img_path,
                shp_path = shapes_path,
                img_save_name ="MAP_TEMP_OPTIMA_3CLASES_JUL1998_SET1999_win",
                )
iibb.graficar_mapa_clases(img_mapa_3clases, clase_cbar=["yellow", "orange","green"])

# Guardar indice bioclimatico en formato tif
#------------------------------------------------------------------------
dic = {"data": temp_optima,
       "nombre_guardar": "map_temp_optima_jul1998_set1999.tif",
       }
guardar_archivo = iibb.guardar_archivo(dic)
guardar_archivo.tif(path_out=img_path+"tif/")

# graficar distribucion de frecuencias
#-------------------------------------------------------------------------------
dic_frecuencias, distrib_prob = ii_tt.aptitud_termica_puntoGrilla(lonlat=[-76.77,-6.28])
img_distrib_frec = dict(data = dic_frecuencias,
                        titulo_derecha = "01 Julio 1998 - 21 Setiembre 1999",
                        titulo_izquierda = "ESTACIÓN PACAYZAPA",
                        nombre_ejex = "Temperatura (°C)",
                        nombre_ejey = "Frecuencia",
                        img_path = img_path,
                        img_save_name =None,# "barra_frecuencia_temp_jul1998_set1999_pacayzapa",
                       )
iibb.graficar_barras(img_distrib_frec)

# Graficar serie de tiempo en punto de grilla
#-------------------------------------------------------------------------------
img_serie_tiempo = dict(data =(temp_min+temp_max)/2 ,
                        punto_grilla = [-76.77, -6.28],
                        titulo_derecha = "01 Julio 1998 - 21 Setiembre 1999",
                        titulo_izquierda = "ESTACIÓN: PACAYZAPA",
                        nombre_ejey = "Temperatura promedio (°C)",
                        img_path = img_path,
                        img_save_name = "serie_tiempo_temp_jul1998_set1999_pacayzapa",
                       )
iibb.graficar_serie_tiempo(img_serie_tiempo, tipo="array")

# Guardar en archivo excel
#------------------------------------------------------------------------
#df.to_excel(img_path+"excel/isc_01_21sep1999.xlsx", header=True,index=False)


# graficar lineas horizontales de los indices por aws
#------------------------------------------------------------------------
#df = df.loc[34:,:].sort_values(by='gddm_01_21sep1999')
#print(df.loc[0:10,:])
#print(df.size)
img_hlineas = dict(data=None,
                   nombre_var = "gddm_01_21sep1999",
                   rango_val = [0,400],
                   nombre_ejex="Grados días de crecimiento mod (°C)",
                   titulo_derecha="01-21 Setiembre 1999",
                   titulo_izquierda ="ÍNDICE BIOCLIMÁTICO",
                   img_path = img_path,
                   img_save_name="gddm_a_hlines_aws_1999_san_mantin",
                   )
#iiibb.graficar_hlineas(img_hlineas)


# Extraer valores en punto de grilla de indice bioclimatico
#------------------------------------------------------------------------
path_data_aws = "/home/data/senamhi/indices_bioclimaticos/data/"
cols_names = ['ESTACION','TIPO','LON_DEC', 'LAT_DEC', 'ALTITUD']
df_aws = pd.read_excel(data_path+'codigos_aws_san_martin.xls',
                   usecols = cols_names,
                   sheet_name='Hoja1',
                   )
#df = iibb.extraer_indice_punto_grilla(gdd_a, df_aws, nombre_iibb="gddm_01_21sep1999")
