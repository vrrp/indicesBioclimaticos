<H1 align="center"><span style="font-family:Times New Roman;font-size:160%;color:#008080"><b>Índices Bioclimáticos</b></span></H1>
<H6 align="center"><span style="font-family:Times New Roman;font-size:20%;color:black">VR ROJAS</span></H6>
<H6 align="center"><span style="font-family:Times New Roman;font-size:20%;color:purple">Web : <a href="https://vrrp.github.io/">https://vrrp.github.io/</a></span></H6>

## Instalar Anaconda

## Librerias de Python
```sh
python instalar_librerias_necesarias.py
```

## Módulo de índices bioclimáticos en Python
``` sh
indices_bioclimaticos.py
```
## Explorar las clases del módulo de índices bioclimáticos
``` py
import indices_bioclimaticos as iibb
print(iibb.__doc__)
```
``` sh
GUARDAR ARRAY EN FORMATO TIF Y NETCDF
    Parametros:
        self.save_file_name: cadena de caracteres, 
        self.data          : array 2D, 3D 
        self.lats          : array 1D
        self.lons          : array 1D        

    Metodos:
        tif    : Guardar array de 2D en formato tif
        netcdf : Guardar array de 3D en formato netcdf

    Ejemplo:
        import indices_bioclimaticos as iibb

        guardar_archivo = iibb.guardar_archivo(dic)
        guardar_archivo.tif()

        donde, [dic] es un diccionario que contiene los datos y atributos 
        para generar el archivo en formato tif y netcdf.
```

## Índices Térmicos
| Archivo Python | Nombre de índice |
| ------ | ----------- |
| ```vrrp_iitt_01_ih_geslin.py ```| [Indice Heliotérmico de Geslin.]() |
| ```vrrp_iitt_02_amplitud_termica.py ```| [Ampmlitud térmica.]() |
| ```vrrp_iitt_03_tiempo_termico.py ```| [Tiempo térmico.]() |
| ```vrrp_iitt_04_indice_termal_general.py ```| [Índice termal general.]() |
| ```vrrp_iitt_05_unidades_calor.py ```| [Unidades de calor.]() |
| ```vrrp_iitt_06_calor_magnitud_dia.py ```| [Calor magnitud día.]() |
| ```vrrp_iitt_07_indice_estres_calor.py ```| [Índice de estrés por calor.]() |
| ```vrrp_iitt_08_gdd.py ```| [Grados días de crecimiento.]() |
| ```vrrp_iitt_09_gddm.py ```| [Grados días de crecimiento modificado.]() |

## Índices Hidrológicos
| Archivo Python | Nombre de índice |
| ------ | ----------- |
| ```vrrp_iihh_01_et_referencia.py```| [Evapotranspiracion de referencia.]() |
| ```vrrp_iihh_02_lluvia_acumulada.py ```| [Precipitación acumulada.]() |
| ```vrrp_iihh_03_prcp_menos_evap.py ```| [Precipitación menos evapotranspiración de referencia]() |
| ```vrrp_iihh_04_relacion_prcp_evap.py ```| [Relación Precipitación entre evapotranspiración de referencia.]() |
| ```vrrp_iihh_05_deficit_hidrico.py ```| [Déficit hídrico.]() |
| ```vrrp_iihh_06_exceso_hidrico.py ```| [Exceso hídrico.]() |
| ```vrrp_iihh_07_indice_humedad.py ```| [Índice de humedad.]() |
| ```vrrp_iihh_08_IBH.py ```| [Índice de bienestar hídrico.]() |
