import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import indices_bioclimaticos as iibb

data_path= "/home/data/senamhi/pisco_data/"
img_path = "/home/data/senamhi/indices_bioclimaticos/img/"
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

"""
Argumentos de la clase indice_termal_general()
a: acumulado total
ar:acumulado recursivo
d:diario
"""
gti_veg_acum, gti_rep_acum = ii_tt.indice_termal_general("a")
#gti_veg_acum, gti_rep_acum = ii_tt.indice_termal_general("a")
gti_veg_diario, gti_rep_diario = ii_tt.indice_termal_general("d")
lons = gti_veg_acum.lons; lats=gti_rep_acum.lats
print("GTI VEG:", np.min(gti_veg_acum.data), np.max(gti_veg_acum.data))
print("GTI REP:", np.min(gti_rep_acum.data), np.max(gti_rep_acum.data))
print(np.shape(gti_veg_acum), np.shape(gti_rep_acum))

# Extraer valores en punto de grilla de indice bioclimatico
#------------------------------------------------------------------------
path_data_aws = "/home/data/senamhi/indices_bioclimaticos/data/"
cols_names = ['ESTACION','TIPO','LON_DEC', 'LAT_DEC', 'ALTITUD']
df_aws = pd.read_excel(path_data_aws+'codigos_aws_san_martin.xls',
                   usecols = cols_names,
                   sheet_name='Hoja1',
                   )
df = iibb.extraer_indice_punto_grilla(gti_veg_acum, df_aws, nombre_iibb="gti_veg_01_31ENE1999")
df = iibb.extraer_indice_punto_grilla(gti_rep_acum, df, nombre_iibb="gti_rep_01_31ENE1999")

# Guardar en archivo excel
#------------------------------------------------------------------------
#df.to_excel(img_path+"excel/gti_01_31enero1999.xlsx", header=True,index=False)

# Graficar serie de tiempo
#-------------------------------------------------------------------------------
img_serie_tiempo = dict(data=gti_veg_diario,
                        punto_grilla=[-76.77, -6.28],
                        titulo_derecha="01-31 ENERO 1999",
                        titulo_izquierda="ÍNDICE BIOCLIMÁTICO: ESTACIÓN PACAYZAPA",
                        nombre_ejey="GTI (°C)",
                        img_path=img_path,
                        img_save_name="gti_veg_st_01_31enero1999_pacayzapa",
                       )
iibb.graficar_serie_tiempo(img_serie_tiempo, tipo="array")
exit()
# graficar lineas horizontales de los indices por aws
#------------------------------------------------------------------------
df = df.loc[34:,:].sort_values(by='gti_rep_01_31ENE1999')
#print(df.loc[0:10,:])
#print(df.size)
img_hlineas = dict(data=df,
                   nombre_var = "gti_rep_01_31ENE1999",
                   rango_val = [0,900],
                   nombre_ejex="Índice termal general rep(°C)",
                   titulo_derecha="01-31 Enero 1999",
                   titulo_izquierda ="ÍNDICE BIOCLIMÁTICO",
                   img_path = img_path,
                   img_save_name="gti_rep2_aws_1999_san_mantin",
                   )
#iibb.graficar_hlineas(img_hlineas)

# graficar mapa de indice 
#------------------------------------------------------------------------
img_mapa = dict(data=gti_rep,
                titulo_derecha="01-31 Enero 1999",
                titulo_izquierda ="ÍNDICE BIOCLIMÁTICO",
                cb_rango= [200, 950, 50],#gti_veg[300 , 3300, 300],
                tipo_cbar=None,
                cb_nombre="Indice termal general rep (°C)",                
                img_path = img_path,
                shp_path = "/home/data/shape/depart_san_martin/",
                img_save_name="gti_rep_map_01_31enero1999_san_mantin",
                )
iibb.graficar_mapa(img_mapa)

# Guardar indice bioclimatico en formato tif
#------------------------------------------------------------------------
dic = {"data": gti_veg,
       "nombre_guardar": "gti_rep_01_31enero_1999.tif",
       }
guardar_archivo = iibb.guardar_archivo(dic)
guardar_archivo.tif(path_out=img_path+"tif/")
