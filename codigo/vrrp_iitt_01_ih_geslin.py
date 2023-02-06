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
temp_min = fo.variable(nombre_var="airtemp_min", rango_tiempo=['1999-09-01','1999-09-21'])
temp_max = fo.variable(nombre_var="airtemp_max", rango_tiempo=['1999-09-01','1999-09-21'])

# Determinar indice bioclimatico
#------------------------------------------------------------------------
ii_tt = iibb.indices_termicos(temp_min, temp_max)
gg, jj = ii_tt.extraer_periodo()
ihg = ii_tt.ihg()
greg_date, julian_date, fotoperiod = ii_tt.ihg(tipo="fotoperiod")
print(len(greg_date), len(julian_date), len(fotoperiod))

# graficar mapa de indice bioclimatico
#------------------------------------------------------------------------
img_mapa = dict(data=ihg,
               titulo_derecha="01-21 Setiembre 1999",
               titulo_izquierda="ÍNDICE BIOCLIMÁTICO",
               cb_rango = [0,140,20],
               tipo_cbar=None,
               cb_nombre= "Índice Heliotérmico Geslin (°C x hora)",
               img_path = img_path,
               shp_path = shapes_path,
               img_save_name=None,#"ihg_01_21setiembre1999_san_martin",
               )
iibb.graficar_mapa(img_mapa)

# Guardar indice bioclimatico en formato tif
#------------------------------------------------------------------------
dic = {"data": ihg, 
       "nombre_guardar": "ihg_01_31enero_1999.tif",
       }

guardar_archivo = iibb.guardar_archivo(dic)
#guardar_archivo.tif(path_out=img_path+"tif/")

# Extraer valores en punto de grilla de indice bioclimatico
#------------------------------------------------------------------------
cols_names = ['ESTACION','TIPO','LON_DEC', 'LAT_DEC', 'ALTITUD']
df_aws = pd.read_excel(data_path+'codigos_aws_san_martin.xls',
                   usecols = cols_names,
                   sheet_name='Hoja1',
                   )

df = iibb.extraer_indice_punto_grilla(ihg, df_aws, nombre_iibb="ihg")
df = df.loc[34:,:].sort_values(by='ihg')

df.to_excel(data_path+"ihg_01_31enero1999.xlsx",header=True,index=False)

# graficar lineas horizontales de los indices por aws
#------------------------------------------------------------------------
img_hlineas = dict(data=df,
                   nombre_var="ihg",
                   rango_val=[0,110],
                   nombre_ejex="Indice Heliotérmico Geslin (°C/hora)",
                   titulo_derecha="01-31 Enero 1999",
                   titulo_izquierda ="ÍNDICE BIOCLIMÁTICO",
                   img_path = img_path,
                   img_save_name="ihg2_aws_1999_san_mantin",
                    )
iibb.graficar_hlineas(img_hlineas)