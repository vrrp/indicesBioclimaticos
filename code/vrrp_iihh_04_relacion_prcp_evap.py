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
prcp = fo_prcp.variable(nombre_var="prcp", rango_tiempo=['1998-08-01','1999-10-21']) # yyyy-mm-dd
evap = fo_etp.variable(nombre_var="etp",   rango_tiempo=['1998-08-01','1999-10-21']) # yyyy-mm-dd

# Graficar serie de tiempo en punto de grilla
#-------------------------------------------------------------------------------
img_serie_tiempo = dict(data = [prcp,evap],
                        punto_grilla = [76.77, 6.28],
                        titulo_derecha = "01 AGO 1998 - 21 OCT 1999 ",
                        titulo_izquierda = "ÍNDICE BIOCLIMÁTICO: ESTACIÓN PACAYZAPA",
                        nombre_ejey = "(mm/día)",
                        img_path = img_path,
                        img_save_name = "relacion_prcp_evap_d_stiempo_01_21setiembre1999_pacayzapa",
                       )
iibb.graficar_serie_tiempo(img_serie_tiempo)
exit()
#Extraer valores en punto de grilla de indice bioclimatico
#------------------------------------------------------------------------
path_data_aws = "/home/data/senamhi/indices_bioclimaticos/data/"
cols_names = ['ESTACION','TIPO','LON_DEC', 'LAT_DEC', 'ALTITUD']
df_aws = pd.read_excel(path_data_aws+'codigos_aws_san_martin.xls',
                   usecols = cols_names,
                   sheet_name='Hoja1',
                   )
df = iibb.extraer_indice_punto_grilla(pme_a, df_aws, nombre_iibb="pme_01_21sep1999")

# Guardar en archivo excel
#------------------------------------------------------------------------
#df.to_excel(img_path+"excel/pme_01_21sep1999.xlsx", header=True,index=False)


