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
temp_min = fo.variable(nombre_var="airtemp_min", rango_tiempo=['1999-01-01','2000-12-31'])
temp_max = fo.variable(nombre_var="airtemp_max", rango_tiempo=['1999-01-01','2000-12-31'])

pg_temp_min = iibb.extraer_data_punto_grilla(temp_min, lonlat=[-76.77, -6.28]).data
pg_temp_max = iibb.extraer_data_punto_grilla(temp_max, lonlat=[-76.77, -6.28]).values
pg_temp_prom= iibb.extraer_data_punto_grilla((temp_min+temp_max)/2, lonlat=[-76.77, -6.28]).data
dic_df = {"times":temp_min["times"].values,
          "temp_min": pg_temp_min,
          "temp_max": pg_temp_max,
          "temp_prom":pg_temp_prom}
df = pd.DataFrame(dic_df)
df.to_excel(img_path+"excel/temp_1999_2000.xlsx")
exit()
# Determinar indice bioclimatico
#------------------------------------------------------------------------
ii_tt = iibb.indices_termicos(temp_min, temp_max)

tt = ii_tt.tiempo_termico(t_base=10)
lons = tt.lons; lats=tt.lats
print(np.min(tt.data), np.max(tt.data))

# Extraer valores en punto de grilla de indice bioclimatico
#------------------------------------------------------------------------
path_data_aws = "/home/data/senamhi/indices_bioclimaticos/data/"
cols_names = ['ESTACION','TIPO','LON_DEC', 'LAT_DEC', 'ALTITUD']
df_aws = pd.read_excel(path_data_aws+'codigos_aws_san_martin.xls',
                   usecols = cols_names,
                   sheet_name='Hoja1',
                   )
df = iibb.extraer_indice_punto_grilla(tt, df_aws, nombre_iibb="TT_01_31ENE1999")
df = df.loc[34:,:].sort_values(by='TT_01_31ENE1999')
#print(df.loc[0:10,:])
#print(df.size)

# graficar lineas horizontales de los indices por aws
#------------------------------------------------------------------------
img_hlineas = dict(data=df,
                   nombre_var = "TT_01_31ENE1999",
                   rango_val = [0,600],
                   nombre_ejex="Tiempo Térmico (°C)",
                   titulo_derecha="01-31 Enero 1999",
                   titulo_izquierda ="ÍNDICE BIOCLIMÁTICO",
                   img_path = img_path,
                   img_save_name="tt2_aws_1999_san_mantin",
                   )
#df.to_excel(img_path+"excel/at_01_31enero1999.xlsx", header=True,index=False)
#iibb.graficar_hlineas(img_hlineas)

# graficar mapa de indice 
#------------------------------------------------------------------------
img_mapa = dict(data=tt,
                titulo_derecha="01-31 Enero 1999",
                titulo_izquierda ="ÍNDICE BIOCLIMÁTICO",
                cb_rango=[0 ,630,50],
                tipo_cbar=None,
                cb_nombre="Tiempo Térmico (°C)",                
                img_path = img_path,
                shp_path = "/home/data/shape/depart_san_martin/",
                img_save_name="tt_map_01_31enero1999_san_mantin",
                )
iibb.graficar_mapa(img_mapa)

# Guardar indice bioclimatico en formato tif
#------------------------------------------------------------------------
dic = {"data": tt,
       "nombre_guardar": "tt_01_31enero_1999.tif",
       }
guardar_archivo = iibb.guardar_archivo(dic)
guardar_archivo.tif(path_out=img_path+"tif/")
