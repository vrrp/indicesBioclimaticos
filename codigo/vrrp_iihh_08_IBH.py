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
m : mensual
"""
ibh_a = ii_hh.indice_bienestar_hidrico("a", fc=100, iswc=100)
ibh_ar= ii_hh.indice_bienestar_hidrico("ar",fc=100, iswc=100)
ibh_m = ii_hh.indice_bienestar_hidrico("m", fc=100, iswc=100)

lons = ibh_a.lons; lats=ibh_a.lats
print(np.min(ibh_m.values), np.max(ibh_m.values))


# Extraer valores en punto de grilla de indice bioclimatico
#------------------------------------------------------------------------
path_data_aws = "/home/data/senamhi/indices_bioclimaticos/data/"
cols_names = ['ESTACION','TIPO','LON_DEC', 'LAT_DEC', 'ALTITUD']
df_aws = pd.read_excel(path_data_aws+'codigos_aws_san_martin.xls',
                   usecols = cols_names,
                   sheet_name='Hoja1',
                   )
df = iibb.extraer_indice_punto_grilla(ibh_a, df_aws, nombre_iibb="ibh_ago98_jul99")

# Guardar en archivo excel
#------------------------------------------------------------------------
#df.to_excel(img_path+"excel/ibh_sep98_jul99.xlsx", header=True,index=False)


# Graficar serie de tiempo en punto de grilla
#-------------------------------------------------------------------------------
img_serie_tiempo = dict(data = ibh_m,
                        punto_grilla = [-76.77, -6.28],
                        titulo_derecha = "AGO 98 - JUL 99",
                        titulo_izquierda = "ÍNDICE BIOCLIMÁTICO: ESTACIÓN PACAYZAPA",
                        nombre_ejey = "Indice de Bienestar Hídrico",
                        img_path = img_path,
                        img_save_name = "ibh_m_stiempo_ago98_jul98_pacayzapa",
                       )
iibb.graficar_serie_tiempo(img_serie_tiempo, tipo="array")

# graficar lineas horizontales de los indices por aws
#------------------------------------------------------------------------
df = df.loc[34:,:].sort_values(by='ibh_ago98_jul99')
#print(df.loc[0:10,:])
#print(df.size)
img_hlineas = dict(data=df,
                   nombre_var = "ibh_ago98_jul99",
                   rango_val = [0,1],
                   nombre_ejex="Índice de bienestar hidrico",
                   titulo_derecha=" ",
                   titulo_izquierda ="ÍNDICE BIOCLIMÁTICO",
                   img_path = img_path,
                   img_save_name="pme_a_hlines_aws_1999_san_mantin",
                   )
#iiibb.graficar_hlineas(img_hlineas)

# graficar mapa de indice 
#------------------------------------------------------------------------
img_mapa = dict(data=ibh_m[0,:,:],
                titulo_derecha="AGOSTO 98",
                titulo_izquierda ="ÍNDICE BIOCLIMÁTICO",
                cb_rango= [0, 1.2, 0.2],
                tipo_cbar="rainbow",
                cb_nombre="Índice bienestar hídrico",                
                img_path = img_path,
                shp_path = "/home/data/shape/depart_san_martin/",
                img_save_name="ibh_ago98__map_san_mantin",
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
