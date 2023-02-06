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
#fo.data_info()

# Extraer variables
#------------------------------------------------------------------------
temp_min = fo.variable(nombre_var="airtemp_min", rango_tiempo=['1999-01-01','1999-01-31'])
temp_max = fo.variable(nombre_var="airtemp_max", rango_tiempo=['1999-01-01','1999-01-31'])

# Determinar indice bioclimatico
#------------------------------------------------------------------------
ii_tt = iibb.indices_termicos(temp_min, temp_max)
gg, jj = ii_tt.extraer_periodo()

at_acum = ii_tt.amplitud_termica("a")
lons = at_acum.lons; lats=at_acum.lats
at_ar= ii_tt.amplitud_termica("ar")
at_d= ii_tt.amplitud_termica("d")

# graficar mapa de indice 
#------------------------------------------------------------------------
img_mapa = dict(data=at_acum,
                titulo_derecha="01-31 Enero 1999",
                titulo_izquierda ="ÍNDICE BIOCLIMÁTICO",
                cb_rango=[200,420,20],
                tipo_cbar=None,
                cb_nombre="Amplitud Térmica (°C)",                
                img_path = img_path,
                shp_path = shapes_path,
                img_save_name="at_acum_map_01_31enero1999_san_mantin",
                )

iibb.graficar_mapa(img_mapa)

# Guardar indice bioclimatico en formato tif
#------------------------------------------------------------------------
dic = {"data": at_acum, 
       "lats": lats,
       "lons": lons,
       "nombre_guardar": "ihg_01_31enero_1999.tif",
       }
#guardar_archivo = iibb.guardar_archivo(dic)
#guardar_archivo.tif(path_out=img_path+"tif/")

# Extraer valores en punto de grilla de indice bioclimatico
#------------------------------------------------------------------------
path_data_aws = "/home/data/senamhi/indices_bioclimaticos/data/"
cols_names = ['ESTACION','TIPO','LON_DEC', 'LAT_DEC', 'ALTITUD']
df_aws = pd.read_excel(path_data_aws+'codigos_aws_san_martin.xls',
                   usecols = cols_names,
                   sheet_name='Hoja1',
                   )
df = iibb.extraer_indice_punto_grilla(at_acum, df_aws, nombre_iibb="AT")
df = df.loc[34:,:].sort_values(by='AT')
#print(df.loc[0:10,:])
#print(df.size)
# graficar serie de tiempo
#------------------------------------------------------------------------
img_serie_tiempo = dict(data=at_d,
                        punto_grilla=[-76.77, -6.28],
                        titulo_derecha="01-31 Enero 1999",
                        titulo_izquierda ="ÍNDICE BIOCLIMÁTICO: ESTACIÓN PACAYZAPA",
                        nombre_ejey = "AT (°C)",
                        img_path = img_path,
                        img_save_name="at_d_st_01_31enero1999_san_mantin",
                        )

iibb.graficar_serie_tiempo(img_serie_tiempo, tipo="array")
exit()
# graficar lineas horizontales de los indices por aws
#------------------------------------------------------------------------
img_hlineas = dict(data=df,
                   nombre_var = "AT",
                   rango_val = [0,350],
                   nombre_ejex="Amplitud Térmica (°C/día)",
                   titulo_derecha="01-31 Enero 1999",
                   titulo_izquierda ="ÍNDICE BIOCLIMÁTICO",
                   img_path = img_path,
                   img_save_name="at2_aws_1999_san_mantin",
                   )
#df.to_excel(img_path+"excel/at_01_31enero1999.xlsx", header=True,index=False)
iibb.graficar_hlineas(img_hlineas)
exit()

