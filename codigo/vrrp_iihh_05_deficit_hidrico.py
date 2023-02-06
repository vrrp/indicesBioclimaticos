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
data_path= "C:\Users\Victor\Documents\taller_iibb\data\"    
shapes_path="C:\Users\Victor\Documents\taller_iibb\shapes\"
img_path = "C:\Users\Victor\Documents\taller_iibb\img\"


file_name_etp = "pisco_v2p1_etp_san_martin.nc"
file_name_prcp = "pisco_v2p1_prcp_san_martin.nc"

# leer archivo netcdf
#------------------------------------------------------------------------
fo_prcp = iibb.extraer(data_path, file_name_prcp)
fo_etp  = iibb.extraer(data_path, file_name_etp)
#fo.data_info()

# Extraer variables
#------------------------------------------------------------------------
prcp = fo_prcp.variable(nombre_var="prcp", rango_tiempo=['1998-08-01','1999-07-31']) # yyyy-mm-dd
etp  = fo_etp.variable(nombre_var="etp",   rango_tiempo=['1998-08-01','1999-07-31']) # yyyy-mm-dd

# Determinar indice bioclimatico
#------------------------------------------------------------------------
ii_hh = iibb.indices_hidricos(prcp, etp)

"""
Argumentos de la clase unidades calor
a : acumulado total
ar:acumulado recursivo
d :diario
"""
df_a = ii_hh.deficit_hidrico("a", fc=100, iswc=100)
df_ar = ii_hh.deficit_hidrico("ar", fc=100, iswc=100)
df_m = ii_hh.deficit_hidrico("m", fc=100, iswc=100)
lons = df_a.lons; lats=df_a.lats

#print(np.min(df_m.values), np.max(df_m.values))

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
img_serie_tiempo = dict(data = df_m,
                        punto_grilla = [-76.77, -6.28],
                        titulo_derecha = "AGO 98 - JUL 99",
                        titulo_izquierda = "ÍNDICE BIOCLIMÁTICO: ESTACIÓN PACAYZAPA",
                        nombre_ejey = "Deficit hídrico (mm/mes)",
                        img_path = img_path,
                        img_save_name = "df_m_stiempo_01_21setiembre1999_pacayzapa",
                       )
iibb.graficar_serie_tiempo(img_serie_tiempo, tipo="array")
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
                   titulo_derecha = "AGO 98 - JUL 99",
                   titulo_izquierda ="ÍNDICE BIOCLIMÁTICO",
                   img_path = img_path,
                   img_save_name="df_a_hlines_aws_1999_san_mantin",
                   )
#iiibb.graficar_hlineas(img_hlineas)

# graficar mapa de indice 
#------------------------------------------------------------------------
img_mapa = dict(data=df_m[0,:,:],
                titulo_derecha="AGOSTO 98",
                titulo_izquierda ="ÍNDICE BIOCLIMÁTICO",
                cb_rango= [0, 170,10],
                tipo_cbar=None,
                cb_nombre="Déficit hídrico (mm/mes)",                
                img_path = img_path,
                shp_path = shapes_path,
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
