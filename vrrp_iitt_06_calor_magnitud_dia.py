import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import indices_bioclimaticos as iibb

#print(help(iibb))
#print(iibb.__doc__)
#print(iibb.ih_geslin.__doc__)
#print(iibb.climatologia.__doc__)
data_path= "/home/data/senamhi/pisco_data/"
img_path = "/home/data/senamhi/indices_bioclimaticos/img/"
file_name = "pisco_v2p1_airtemp_san_martin.nc"

# leer archivo netcdf
#------------------------------------------------------------------------
fo = iibb.extraer(data_path, file_name)
#fo.data_info()

# Extraer variables
#------------------------------------------------------------------------
temp_max2quantiles = fo.variable(nombre_var="airtemp_max", rango_tiempo=['1999-01-01','1999-12-31']) # yyyy-mm-dd
temp_max = fo.variable(nombre_var="airtemp_max", rango_tiempo=['1999-09-01','1999-09-21']) # yyyy-mm-dd

# Determinar indice bioclimatico
#------------------------------------------------------------------------
ii_tt = iibb.indices_termicos(temp_max2quantiles, temp_max)
gg, jj = ii_tt.extraer_periodo()

"""
Argumentos de la clase unidades calor
a : acumulado total
ar:acumulado recursivo
d :diario
"""
cmd_a = ii_tt.calor_magnitud_dia("a")
cmd_ar = ii_tt.calor_magnitud_dia("ar")
cmd_d = ii_tt.calor_magnitud_dia("d")
lons = cmd_a.lons; lats=cmd_a.lats
print(lons)
print(np.min(cmd_a.values), np.max(cmd_a.values))

# Extraer valores en punto de grilla de indice bioclimatico
#------------------------------------------------------------------------
path_data_aws = "/home/data/senamhi/indices_bioclimaticos/data/"
cols_names = ['ESTACION','TIPO','LON_DEC', 'LAT_DEC', 'ALTITUD']
df_aws = pd.read_excel(path_data_aws+'codigos_aws_san_martin.xls',
                   usecols = cols_names,
                   sheet_name='Hoja1',
                   )
df = iibb.extraer_indice_punto_grilla(cmd_a, df_aws, nombre_iibb="cmd_01_21sep1999")

# Guardar en archivo excel
#------------------------------------------------------------------------
#df.to_excel(img_path+"excel/cmd_01_21sep1999.xlsx", header=True,index=False)

# Graficar serie de tiempo en punto de grilla
#-------------------------------------------------------------------------------
img_serie_tiempo = dict(data = cmd_d,
                        punto_grilla = [76.77, 6.28],
                        titulo_derecha = "01-21 SETIEMBRE 1999",
                        titulo_izquierda = "ÍNDICE BIOCLIMÁTICO: ESTACIÓN PACAYZAPA",
                        nombre_ejey = "Calor magnitud día (°C)",
                        img_path = img_path,
                        img_save_name = "cmd_d_stiempo_01_21setiembre1999_pacayzapa",
                       )
#iibb.graficar_serie_tiempo(img_serie_tiempo)

# graficar lineas horizontales de los indices por aws
#------------------------------------------------------------------------
df = df.loc[34:,:].sort_values(by='cmd_01_21sep1999')
#print(df.loc[0:10,:])
#print(df.size)
img_hlineas = dict(data=df,
                   nombre_var = "cmd_01_21sep1999",
                   rango_val = [0,900],
                   nombre_ejex="Calor magnitud día (°C)",
                   titulo_derecha="01-31 Enero 1999",
                   titulo_izquierda ="ÍNDICE BIOCLIMÁTICO",
                   img_path = img_path,
                   img_save_name="cmd_a_hlines_aws_1999_san_mantin",
                   )
#iiibb.graficar_hlineas(img_hlineas)

# graficar mapa de indice 
#------------------------------------------------------------------------
print(np.min(cmd_a), np.max(cmd_a))
img_mapa = dict(data=cmd_a,
                titulo_derecha="01-21 SETIEMBRE 1999",
                titulo_izquierda ="ÍNDICE BIOCLIMÁTICO",
                cb_rango= [0, 33, 3],
                cb_nombre="Calor magnitud día (°C)",                
                img_path = img_path,
                shp_path = "/home/data/shape/depart_san_martin/",
                img_save_name="cmd_a_map_01_21sep1999_san_mantin",
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
