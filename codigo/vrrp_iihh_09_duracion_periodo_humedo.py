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

"""
On Windows, with Python >= 3.8, DLLs are no longer imported from the PATH.
If gdalXXX.dll is in the PATH, then set the USE_PATH_FOR_GDAL_PYTHON=YES environment variable
to feed the PATH into os.add_dll_directory().

gdal, fiona, geopandas

Figures now render in the Plots pane by default. To make them also appear inline in the Console, uncheck "Mute Inline Plotting" under the Plots pane options menu.
"""

file_name_etp = "pisco_v2p1_etp_san_martin.nc"
file_name_prcp = "pisco_v2p1_prcp_san_martin.nc"

# leer archivo netcdf
#------------------------------------------------------------------------
fo_prcp = iibb.extraer(data_path, file_name_prcp)
fo_etp  = iibb.extraer(data_path, file_name_etp)
#fo.data_info()

# Extraer variables
#------------------------------------------------------------------------
prcp = fo_prcp.variable(nombre_var="prcp", rango_tiempo=['1990-01-01','2015-12-31']) # yyyy-mm-dd
evap = fo_etp.variable(nombre_var="etp",   rango_tiempo=['1990-01-01','2015-12-31'])

ii_hh = iibb.indices_hidricos(prcp, evap)
df_frec= ii_hh.duracion_periodo_humedo(punto_grilla = [-76.77, -6.28])

# Graficar serie de tiempo en punto de grilla
#-------------------------------------------------------------------------------
img_serie_tiempo = dict(data = df_frec,
                        punto_grilla = None,
                        titulo_derecha = "CLIMATOLOGÍA DECADIARIA: 1990 - 2015 ",
                        titulo_izquierda = "ESTACIÓN: PACAYZAPA",
                        nombre_ejey = "Frecuencia",
                        img_path = img_path,
                        img_save_name = None,#"dphumedo_stiempo_1990_2015_pacayzapa",
                        )


iibb.graficar_serie_tiempo(img_serie_tiempo, tipo="dataframe")
