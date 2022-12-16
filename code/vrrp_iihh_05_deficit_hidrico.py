import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import indices_bioclimaticos as iibb

data_path= "/home/data/senamhi/pisco_data/"
img_path = "/home/data/senamhi/indices_bioclimaticos/img/"
file_name_etp = "pisco_v2p1_etp_san_martin.nc"
file_name_prcp = "pisco_v2p1_prcp_san_martin.nc"

# leer archivo netcdf
#------------------------------------------------------------------------
fo_prcp = iibb.extraer(data_path, file_name_prcp)
fo_etp  = iibb.extraer(data_path, file_name_etp)
#fo.data_info()

# Extraer variables
#------------------------------------------------------------------------
etp = fo_etp.variable(nombre_var="etp", rango_tiempo=['1999-09-01','1999-09-21']) # yyyy-mm-dd

# Determinar indice bioclimatico
#------------------------------------------------------------------------
ii_hh = iibb.indices_hidricos(etp)

"""
Argumentos de la clase unidades calor
a : acumulado total
ar:acumulado recursivo
d :diario
"""
df_a = ii_hh.deficit_hidrico(tipo="a", kc=0.98)
df_ar = ii_hh.deficit_hidrico(tipo="ar", kc=0.98)
df_d = ii_hh.deficit_hidrico("d", kc=0.98)
lons = df_a.lons; lats=df_a.lats

print(np.min(df_a.values), np.max(df_a.values))

# Extraer valores en punto de grilla de indice bioclimatico
#------------------------------------------------------------------------
path_data_aws = "/home/data/senamhi/indices_bioclimaticos/data/"
cols_names = ['ESTACION','TIPO','LON_DEC', 'LAT_DEC', 'ALTITUD']
df_aws = pd.read_excel(path_data_aws+'codigos_aws_san_martin.xls',
                   usecols = cols_names,
                   sheet_name='Hoja1',
                   )
df = iibb.extraer_indice_punto_grilla(df_a, df_aws, nombre_iibb="df_01_21sep1999")

# Guardar en archivo excel
#------------------------------------------------------------------------
#df.to_excel(img_path+"excel/df_01_21sep1999.xlsx", header=True,index=False)

# Graficar serie de tiempo en punto de grilla
#-------------------------------------------------------------------------------
img_serie_tiempo = dict(data = df_d,
                        punto_grilla = [-76.77, -6.28],
                        titulo_derecha = "01-21 SETIEMBRE 1999",
                        titulo_izquierda = "ÍNDICE BIOCLIMÁTICO: ESTACIÓN PACAYZAPA",
                        nombre_ejey = "Deficit hídrico (mm/día)",
                        img_path = img_path,
                        img_save_name = "df_d_stiempo_01_21setiembre1999_pacayzapa",
                       )
iibb.graficar_serie_tiempo(img_serie_tiempo)
exit()
# graficar lineas horizontales de los indices por aws
#------------------------------------------------------------------------
df = df.loc[34:,:].sort_values(by='df_01_21sep1999')
#print(df.loc[0:10,:])
#print(df.size)
img_hlineas = dict(data=df,
                   nombre_var = "df_01_21sep1999",
                   rango_val = [0,3],
                   nombre_ejex="Deficit hídrico acumulada (mm)",
                   titulo_derecha="01-21 Setiembre 1999",
                   titulo_izquierda ="ÍNDICE BIOCLIMÁTICO",
                   img_path = img_path,
                   img_save_name="df_a_hlines_aws_1999_san_mantin",
                   )
#iiibb.graficar_hlineas(img_hlineas)

# graficar mapa de indice 
#------------------------------------------------------------------------
img_mapa = dict(data=df_a,
                titulo_derecha="01-21 SETIEMBRE 1999",
                titulo_izquierda ="ÍNDICE BIOCLIMÁTICO",
                cb_rango= [0, 3.2, 0.2],
                tipo_cbar=None,
                cb_nombre="Déficit hídrico acumulada (mm)",                
                img_path = img_path,
                shp_path = "/home/data/shape/depart_san_martin/",
                img_save_name="df_a_map_01_21sep1999_san_mantin",
                )
iibb.graficar_mapa(img_mapa)
exit()

# Guardar indice bioclimatico en formato tif
#------------------------------------------------------------------------
dic = {"data": etp_a,
       "nombre_guardar": "etp_ac_01_21setiembre_1999.tif",
       }
guardar_archivo = iibb.guardar_archivo(dic)
guardar_archivo.tif(path_out=img_path+"tif/")
