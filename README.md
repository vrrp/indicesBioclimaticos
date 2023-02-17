<H1 align="center"><span style="font-family:Times New Roman;font-size:160%;color:#008080"><b>Índices Bioclimáticos</b></span></H1>
<H6 align="center"><span style="font-family:Times New Roman;font-size:20%;color:black">VR ROJAS</span></H6>
<H6 align="center"><span style="font-family:Times New Roman;font-size:20%;color:purple">Web : <a href="https://vrrp.github.io/">https://vrrp.github.io/</a></span></H6>

## Instalar: Python y Anaconda
[Descargar Python](https://www.python.org/)

[Descargar Anaconda](https://www.anaconda.com/products/distribution)

[//][Descargar datos climáticos](https://mega.nz/folder/OQxRUTgI#4vwaVC7fj9MMXjLQCakEqg)

Instalar Python y Anaconda en [Linux](https://github.com/vrrp/Workshop2018Python/blob/master/Modulo1/1%20-%20Introducci%C3%B3n.ipynb)

## Librerias de Python
El scritp ```instalar_librerias_python.py```, permite instalar todas las librerias
necesarias para usar el módulo ```indices_bioclimaticos.py ```

## Módulo: índices bioclimáticos
``` sh
indices_bioclimaticos.py
```
## Explorar: clases y métodos del módulo índices bioclimáticos
### Explorar: módulo
``` py
import indices_bioclimaticos as iibb

print(iibb.__doc__)
```

``` sh
Modulo:
    indices_bioclimaticos.py

Clases:
    extraer
    indices_termicos
    indices_hidricos
    guardar_archivo
Metodos:
    graficar_serie_tiempo
    graficar_hlineas
    graficar_mapa
```
### Explorar: Clases
``` py
import indices_bioclimaticos as iibb

print(iibb.extraer.__doc__)
```
``` sh
Clase:
    extrar
Metodo:
    variable(arg1, arg2)
Parametros:
    arg1: ruta de directorio data
    arg2: nombre de archivo netcdf
```


``` py
import indices_bioclimaticos as iibb

print(iibb.indices_termicos.__doc__)
```
``` sh
Clase:
    indices_termicos
Metodo:
    ihg() : indice heliotermico de geslim
    amplitud_termica(arg2)
    tiempo_termico(arg1)
    indice_termal_general(arg1)
    unidades_calor(arg1)
    calor_magnitud_dia(arg1)
    indice_estres_calor(arg1, arg2)
    gdd(arg1, arg2): grados dias de crecimiento
    gddm(arg1, arg2): grados dias de crecimiento modificado
 Parametros:
    arg1: "a", "ar", "d"
    arg2: t_bae = [valor numerico]
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
