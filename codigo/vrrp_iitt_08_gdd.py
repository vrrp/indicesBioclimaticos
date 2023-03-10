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
temp_min = fo.variable(nombre_var="airtemp_min", rango_tiempo=['1999-09-01','1999-09-21']) # yyyy-mm-dd
temp_max = fo.variable(nombre_var="airtemp_max", rango_tiempo=['1999-09-01','1999-09-21']) # yyyy-mm-dd

# Determinar indice bioclimatico
#------------------------------------------------------------------------
ii_tt = iibb.indices_termicos(temp_min, temp_max)
gg, jj = ii_tt.extraer_periodo()

"""
Argumentos de la clase unidades calor
a : acumulado total
ar:acumulado recursivo
d :diario
"""
gdd_a = ii_tt.gdd("a", tb=10)
gdd_ar = ii_tt.gdd("ar", tb=10)
gdd_d = ii_tt.gdd("d", tb=10)
lons = gdd_a.lons; lats=gdd_a.lats

#print(lons)
print(np.min(gdd_a.values), np.max(gdd_a.values))

# Extraer valores en punto de grilla de indice bioclimatico
#------------------------------------------------------------------------
path_data_aws = "/home/data/senamhi/indices_bioclimaticos/data/"
cols_names = ['ESTACION','TIPO','LON_DEC', 'LAT_DEC', 'ALTITUD']
df_aws = pd.read_excel(path_data_aws+'codigos_aws_san_martin.xls',
                   usecols = cols_names,
                   sheet_name='Hoja1',
                   )
df = iibb.extraer_indice_punto_grilla(gdd_a, df_aws, nombre_iibb="gdd_01_21sep1999")

# Guardar en archivo excel
#------------------------------------------------------------------------
#df.to_excel(img_path+"excel/isc_01_21sep1999.xlsx", header=True,index=False)

# Graficar serie de tiempo en punto de grilla
#-------------------------------------------------------------------------------
img_serie_tiempo = dict(data = gdd_ar,
                        punto_grilla = [-76.77, -6.28],
                        titulo_derecha = "01-21 SETIEMBRE 1999",
                        titulo_izquierda = "??NDICE BIOCLIM??TICO: ESTACI??N PACAYZAPA",
                        nombre_ejey = "Grados d??as de crecimiento (??C)",
                        img_path = img_path,
                        img_save_name = "gdd_ar_stiempo_01_21setiembre1999_pacayzapa",
                       )
iibb.graficar_serie_tiempo(img_serie_tiempo, tipo="array")
exit()

# graficar lineas horizontales de los indices por aws
#------------------------------------------------------------------------
df = df.loc[34:,:].sort_values(by='gdd_01_21sep1999')
#print(df.loc[0:10,:])
#print(df.size)
img_hlineas = dict(data=df,
                   nombre_var = "gdd_01_21sep1999",
                   rango_val = [0,400],
                   nombre_ejex="Grados d??as de crecimiento (??C)",
                   titulo_derecha="01-21 Setiembre 1999",
                   titulo_izquierda ="??NDICE BIOCLIM??TICO",
                   img_path = img_path,
                   img_save_name="gdd_a_hlines_aws_1999_san_mantin",
                   )
#iiibb.graficar_hlineas(img_hlineas)

# graficar mapa de indice 
#------------------------------------------------------------------------

img_mapa = dict(data=gdd_a,
                titulo_derecha="01-21 SETIEMBRE 1999",
                titulo_izquierda ="??NDICE BIOCLIM??TICO",
                cb_rango= [0, 450, 50],
                tipo_cbar=None,
                cb_nombre="Grados d??as de crecimiento (??C)",                
                img_path = img_path,
                shp_path = "/home/data/shape/depart_san_martin/",
                img_save_name="gdd_a_map_01_21sep1999_san_mantin",
                )
iibb.graficar_mapa(img_mapa)
exit()

# Guardar indice bioclimatico en formato tif
#------------------------------------------------------------------------
dic = {"data": gti_veg,
       "nombre_guardar": "gti_rep_01_31enero_1999.tif",
       }
guardar_archivo = iibb.guardar_archivo(dic)
guardar_archivo.tif(path_out=img_path+"tif/")
