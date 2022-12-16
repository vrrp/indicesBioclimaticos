"""  INDICES BIOCLIMATICOS PARA MAIZ Y CAFE"""
__author__ = "VR ROJAS"
__license__="GPL"
__version__="0.1"
__email__="vr.rojaspozo@gmail.com"

import numpy as np
import pandas as pd
import xarray as xr
import datetime as dt
from osgeo import gdal, osr, ogr

class guardar_archivo(object):
    """GUARDAR ARRAY EN FORMATO TIF Y NETCDF
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
    """
    def __init__(self, dic):
        self.save_file_name = dic["nombre_guardar"]
        self.ds_data = dic["data"]
                
        self.data = self.ds_data.values
        self.lats = self.ds_data["lats"].values
        self.lons = self.ds_data["lons"].data
        self.ny, self.nx = np.shape(self.data)

    def tif(self,path_out=None):
        extent = [np.min(self.lons), np.min(self.lats),
                  np.max(self.lons), np.max(self.lats),
                  ]
        xres = (extent[2]-extent[0])/self.nx
        yres = (extent[3]-extent[1])/self.ny
        geotransform = (extent[0], xres, 0, extent[3],0,-yres)

        if path_out is None:
            dst_ds = gdal.GetDriverByName('GTiff').Create(self.save_file_name, self.nx, self.ny,1, gdal.GDT_Byte)
        if path_out is not None:
            dst_ds = gdal.GetDriverByName('GTiff').Create(path_out+self.save_file_name, self.nx, self.ny,1, gdal.GDT_Byte)
        dst_ds.SetGeoTransform(geotransform)
        srs = osr.SpatialReference()
        srs.ImportFromEPSG(3857) # WGS84 lats/lons
        dst_ds.SetProjection(srs.ExportToWkt())
        dst_ds.GetRasterBand(1).WriteArray(self.data)
        dst_ds.FlushCache()
        dst_ds=None

class extraer(object):
    """
    Aqui va descripcion

    """
    def __init__(self, data_path, file_name):
        self.ds = xr.open_dataset(data_path+file_name)
    def data_info(self):
        print(self.ds)

    def variable(self, nombre_var= None, rango_tiempo=None):
        if nombre_var is not None:
            if rango_tiempo is None:
                self.ds_data = self.ds[nombre_var]
                return self.ds_data
            else:
                ndim_rango_tiempo = len(rango_tiempo)
                if ndim_rango_tiempo==2:
                    self.ds_data = self.ds[nombre_var].sel(times=slice(rango_tiempo[0], rango_tiempo[1]))
                    return self.ds_data
                else:
                    self.ds_data = self.ds[nombre_var].sel(times=rango_tiempo)
                    return self.ds_data

class indices_termicos(object):
    """DETERMINAR EL INDICE HELIOTERMICO DE GESLIN (ihg)
    \t\t igh = f(Tm, N)

    Tm es la temperatura media
    N es el fotoperiodo

    Parametros:
        ds_temp_min: estructura de datos de 3D
        ds_temp_max: estructura de datos de 3D
        ds_lats    : estructura de datos de 1D

    Metodos:
        extraer_periodo : devuelve dos objetos (array 1D)
        extraer_indice  : devuelve un objeto (array 2D)

    Ejemplo:

        import indices_bioclimaticos as iibb

        ii_tt = iibb.indices_termicos(temp_min, temp_max)
        fecha_greg, fecha_jj = ii_tt.extraer_periodo()
        ihg = ii_tt.ihg()
    """
    def __init__(self,ds_temp_min, ds_temp_max):
        self.ds_temp_min = ds_temp_min
        self.ds_temp_max = ds_temp_max
        self.t_mean = (ds_temp_min + ds_temp_max)/2
        self.nlevs, self.nrows, self.ncols = np.shape(self.t_mean)

        self.ds_lons = self.ds_temp_min["lons"].data
        self.ds_lats = self.ds_temp_min["lats"].data
        
        self.ds_times = self.ds_temp_min["times"].values.astype(str).tolist()
        greg_date = [];julian_date=[];jj=[]

        for i in range(len(self.ds_times)):
            greg_date.append(self.ds_times[i].split('T')[0])
            julian_date.append(dt.datetime.strptime(self.ds_times[i].split('T')[0],"%Y-%m-%d").strftime('%Y%j'))
            jj.append(int(dt.datetime.strptime(self.ds_times[i].split('T')[0],"%Y-%m-%d").strftime('%j')))

        self.greg_date = greg_date; self.julian_date = julian_date; self.ds_jj=jj
    
    def gddm(self,tipo, tb):
       
       for ilev in range(self.nlevs):
           for irow in range(self.nrows):
               for icol in range(self.ncols):
                   if self.ds_temp_max[ilev,irow,icol] >30:
                       self.ds_temp_max[ilev,irow,icol]=30
                   elif self.ds_temp_min[ilev,irow,icol]<tb: 
                       self.ds_temp_min[ilev,irow,icol]=tb
       gddm = (self.ds_temp_min+self.ds_temp_max)/2 - tb       
      
       if tipo=="a":
            return  gddm.sum('times')
       elif tipo=="ar":
           return np.cumsum(gddm, axis=0)
       elif tipo=="d":
           return gddm

    def gdd(self,tipo, tb):
       #gdd = np.zeros(np.shape(self.t_mean))
       gdd = self.t_mean - tb
       for ilev in range(self.nlevs):
           for irow in range(self.nrows):
               for icol in range(self.ncols):
                   if self.t_mean[ilev,irow,icol] < tb:
                       gdd[ilev,irow,icol]=0
                   else: pass 
                       #gdd[ilev,irow,icol] = self.t_mean[ilev,irow,icol] - tb
       
       if tipo=="a":
            return  gdd.sum('times')
       elif tipo=="ar":
           return np.cumsum(gdd, axis=0)
       elif tipo=="d":
           return  gdd       


    def indice_estres_calor(self, tipo, tb=10):
        t_max = self.ds_temp_max
        hsi = t_max - tb
        nlevs, nrows, ncols = np.shape(t_max)
        for ilev in range(nlevs):
            for irow in range(nrows):
                for icol in range(ncols):
                    if hsi[ilev, irow,icol]<0:
                        hsi[ilev,irow,icol]=0
                    else:pass
        if tipo=="a":
            return  hsi.sum('times')
        elif tipo=="ar":
            return np.cumsum(hsi, axis=0)
        elif tipo=="d":
            return  hsi


    def calor_magnitud_dia(self,tipo):
        temp2quantil = self.ds_temp_min.values
        temp_max = self.ds_temp_max.values
        t_q1 = np.percentile(temp2quantil, 25, interpolation='midpoint')
        t_q3 = np.percentile(temp2quantil, 75, interpolation='midpoint')
        riq=t_q3-t_q1
        t_q90 = np.percentile(temp2quantil, 90, interpolation='midpoint')
        
        nlevels, nrows, ncols = np.shape(self.ds_temp_max)
        cmd = np.zeros(np.shape(self.ds_temp_max))
        for ilev in range(nlevels):
            for irow in range(nrows):
                for icol in range(ncols):
                    itemp_max = self.ds_temp_max[ilev,irow,icol]
                    if itemp_max>t_q90:
                        cmd[ilev,irow,icol]=(itemp_max - t_q1)/riq
                    else:
                        cmd[ilev,irow,icol]=0        
        ds_cmd = xr.Dataset(data_vars={"cmd":(("times","lats","lons"), cmd),
                                       },
                            coords ={"times": self.ds_temp_max["times"].data,
                                     "lats":self.ds_lats, 
                                     "lons":self.ds_lons},
                           )
        if tipo=="a":
            return  ds_cmd["cmd"].sum('times')
        elif tipo=="ar":
            return np.cumsum(ds_cmd["cmd"],axis=0)
        elif tipo=="d":
            return  ds_cmd["cmd"]

    def unidades_calor(self, tipo):
        nlevels, nrows, ncols = np.shape(self.ds_temp_max)
        chu_min = np.zeros(np.shape(self.ds_temp_min))
        chu_max = np.zeros(np.shape(self.ds_temp_max))

        for ilev in range(nlevels):
            for irow in range(nrows):
                for icol in range(ncols):
                    itemp_min = self.ds_temp_min[ilev,irow,icol].values
                    if itemp_min <4.4:
                        chu_min[ilev,irow,icol]=0
                    else:
                        chu_min[ilev,irow,icol]=1.8*(itemp_min -4.4)

        for ilev in range(nlevels):
            for irow in range(nrows):
                for icol in range(ncols):
                    itemp_max = self.ds_temp_max[ilev,irow,icol].values
                    if itemp_max <10:
                        chu_max[ilev,irow,icol]=0
                    else:
                        chu_max[ilev,irow,icol]=3.33*(itemp_max -10)-0.084*(itemp_max-10)**2
        ds_chu = xr.Dataset(data_vars={"chu_min":(("times","lats","lons"), chu_min),
                                       "chu_max":(("times","lats","lons"),chu_max),
                                       "chu":(("times","lats","lons"),(chu_min+chu_max)/2),
                                       },
                            coords ={"times": self.ds_temp_min["times"].data,"lats":self.ds_lats, "lons":self.ds_lons},
                           )
        if tipo=="a":
            return ds_chu["chu_min"].sum('times'), ds_chu["chu_max"].sum('times'), ds_chu["chu"].sum('times')
        elif tipo=="ar":
            return np.cumsum(ds_chu["chu_min"], axis=0), np.cumsum(ds_chu["chu_max"],axis=0), np.cumsum(ds_chu["chu"],axis=0)
        elif tipo=="d":
            return ds_chu["chu_min"], ds_chu["chu_max"], ds_chu["chu"]

    def indice_termal_general(self, tipo):
        t_med = (self.ds_temp_max + self.ds_temp_min)/2
        gti_veg = 0.043177*t_med**2 - 0.000894*t_med**3
        gti_rep = 5.3581 + 0.011178*t_med**2
        if tipo=="a":
            return gti_veg.sum('times'), gti_rep.sum('times')
        elif tipo=="ar":
            return np.cumsum(gti_veg, axis=0), np.cumsum(gti_rep, axis=0)
        elif tipo=="d":
            return gti_veg, gti_rep

    def tiempo_termico(self, t_base):
        tmed_menos_t_base = (self.ds_temp_max+self.ds_temp_min)/2- t_base 
        tt = tmed_menos_t_base.sum('times')
        return tt

    def extraer_periodo(self):
        """FECHA EN FORMATO GREGORIANO Y JULIANO

        Parametros:
            sin parametros

        Metodos:
            extraer_perido: devuelve dos objetos

        Ejemplo:
            fecha_greg, fecha_jj = clase_ihg.extraer_peridos()
        """
        return self.greg_date, self.julian_date
    
    def amplitud_termica(self, tipo):        
        at = self.ds_temp_max - self.ds_temp_min
        if tipo=="a":
            return at.sum(dim='times')
        elif tipo=="ar":
            return np.cumsum(at, axis=0)
        elif tipo=="d":
            return at
    
    def ihg(self):
        """CALCULO DE igh

        Parametros:
            t_mean: temperatura promedio
            phi   : 
        """
        t_mean = (self.ds_temp_min.values + self.ds_temp_max.values)/2
        phi = np.pi*np.array(self.ds_lats)/180
        delta = 0.409*np.sin(2*np.pi*np.array(self.ds_jj)/365-1.39)
        n_phi= len(phi); n_delta = len(delta)
        nlev, nrows, ncols = np.shape(t_mean)
        ihg = np.zeros((nlevs, nrows, ncols)); ihg[...]=np.nan

        N = 24*np.arccos(-np.tan(phi)*np.tan(delta[0]))/np.pi
        for ilev in range(n_delta):
            for irow in range(n_phi):
                ihg[ilev, irow, :]= t_mean[ilev,irow,: ]*N[irow]

        ihg_data = np.sum(ihg, axis=0)/100
        ds_ihg = xr.Dataset(data_vars={"data":(("lats","lons"), ihg_data)},
                            coords ={"lats":self.ds_lats, "lons":self.ds_lons},
                           )
        return ds_ihg["data"]

class indices_hidricos(object):
    """DETERMINAR INDICES EN FUNCION DE LA PRECIPITACION
    Y EVAPOTRANSPIRACIÓN
    f(prcp, evt)

    prcp: precipitacion
    evp : evapotranspiracion potencial
    evr : evapotranspircaion de referencia

    Parametros:
        ds_data1: estructura de datos de 3D
        ds_data2: estructura de datos de 3D
        ds_lats    : estructura de datos de 1D

    Metodos:
        extraer_periodo : devuelve dos objetos (array 1D)
        extraer_indice  : devuelve un objeto (array 2D)

    Ejemplo:

        import indices_bioclimaticos as iibb

        clase_ihg = iibb.ig_geslin(temp_min, temp_max)
        fecha_greg, fecha_jj = clase_ihg.extraer_periodo()
        ihg = clase_ihg.extraer_indice()
    """
    def __init__(self, ds_data1, ds_data2=None):
        self.ds_data1 = ds_data1
        self.ds_times = self.ds_data1["times"].values
        self.ds_lats = self.ds_data1["lats"].values
        self.ds_lons = self.ds_data1["lons"].values
        self.nlevs, self.nrows, self.ncols = np.shape(self.ds_data1)
        
        if ds_data2 is not None:
            self.ds_data2 = ds_data2


    def indice_bienestar_hidrico(self,tipo, iswc):
        prcp = self.ds_data1
        evap = self.ds_data2
        start_time = prcp['times'].values[0]
        
        df_time = pd.DataFrame(columns=['date'], 
                               data=pd.date_range(start_time, periods=12, freq='MS').to_pydatetime())
        times= df_time['date'].to_numpy()
        
        prcp_month = prcp.groupby('times.month').sum(dim='times').data
        evap_month = evap.groupby('times.month').sum(dim='times').values
        
        pme = prcp_month - evap_month
        nlevs, nrows, ncols = np.shape(prcp_month)

        swc = np.zeros(np.shape(prcp_month))
        delta = np.zeros(np.shape(prcp_month))
        ae = np.zeros(np.shape(prcp_month))
        
        # calculo de swc
        for ilev in range(nlevs):
            for irow in range(nrows):
                for icol in range(ncols):
                    if ilev==0:
                        condition=iswc-pme[ilev,irow,icol]
                        if condition>=iswc:
                            swc[ilev,irow,icol]=iswc
                        elif condition<=0:
                            swc[ilev,irow,icol]=0
                        else:
                            swc[ilev,irow,icol]=condition
                    else:
                        condition=swc[ilev,irow,icol] - pme[ilev,irow,icol]
                        if condition>=iswc:
                            swc[ilev,irow,icol]=iswc
                        elif condition<=0:
                            swc[ilev,irow,icol]=0
                        else:
                            swc[ilev,irow,icol]=condition

        # calculo de delta
        for ilev in range(nlevs):
            for irow in range(nrows):
                for icol in range(ncols):
                    if ilev==0:
                        delta[ilev,irow,icol] = swc[ilev,irow,icol]-iswc
                    else:
                        delta[ilev,irow,icol] = swc[ilev,irow,icol] - swc[ilev-1, irow-1, icol-1]

        # calculo de evapotranspiracion actual
        for ilev in range(nlevs):
            for irow in range(nrows):
                for icol in range(ncols):
                    if swc[ilev,irow,icol] >= evap_month[ilev,irow,icol]:
                        ae[ilev,irow,icol] = evap_month[ilev,irow,icol]

                    elif (prcp_month[ilev,irow,icol]+abs(delta[ilev,irow,icol])) >= evap_month[ilev,irow,icol]:
                        ae[ilev,irow,icol] = evap_month[ilev,irow,icol]

                    else:
                        ae[ilev,irow,icol] = prcp_month[ilev,irow,icol] + abs(delta[ilev,irow,icol])

        ibh = ae/evap_month

        ds_ibh = xr.Dataset(data_vars={"ibh":(("times","lats","lons"), ibh),
                                       },
                            coords ={"times": times,
                                     "lats":self.ds_lats, 
                                     "lons":self.ds_lons},
                           )
        if tipo=="a":
            return  ds_ibh["ibh"].sum('times')
        elif tipo=="ar":
            return np.cumsum(ds_ibh["ibh"], axis=0)
        elif tipo=="m":
            return ds_ibh["ibh"]

    def indice_humedad(self, tipo):
        prcp = self.ds_data1
        evap = self.ds_data2
        ih=prcp/evap
        if tipo=="a":
            return  ih.sum('times')
        elif tipo=="ar":
            return np.cumsum(ih, axis=0)
        elif tipo=="d":
            return ih

    def deficit_hidrico(self, tipo, kc):
        evap = self.ds_data1
        df = (1 - kc)*evap 

        if tipo=="a":
            return  df.sum('times')
        elif tipo=="ar":
            return np.cumsum(df, axis=0)
        elif tipo=="d":
            return df

    def exceso_hidrico(self, tipo):
        prcp = self.ds_data1.data
        evap = self.ds_data2.data
        
        a = prcp - evap
                
        for ilev in range(self.nlevs):
            for irow in range(self.nrows):
                for icol in range(self.ncols):
                    if a[ilev, irow, icol]<0:
                        a[ilev, irow, icol]=0
                    else:pass
        ds_a = xr.Dataset(data_vars={"a":(("times","lats","lons"), a),
                                       },
                            coords ={"times": self.ds_times,
                                     "lats":self.ds_lats, 
                                     "lons":self.ds_lons},
                           )
        if tipo=="a":
            return  ds_a["a"].sum('times')
        elif tipo=="ar":
            return np.cumsum(ds_a["a"], axis=0)
        elif tipo=="d":
            return ds_a["a"]

    def prcp_menos_evap(self, tipo):
        prcp = self.ds_data1
        evap = self.ds_data2
        a = prcp - evap

        if tipo=="a":
            return  a.sum('times')
        elif tipo=="ar":
            return np.cumsum(a, axis=0)
        elif tipo=="d":
            return a

    def lluvia_acumulada(self, tipo):
        prcp = self.ds_data1
        if tipo=="a":
            return  prcp.sum('times')
        elif tipo=="ar":
            return np.cumsum(prcp, axis=0)
        elif tipo=="d":
            return prcp

    
    def et_referencia(self, tipo):
        et_ref = self.ds_data1
        
        if tipo=="a":
            return  et_ref.sum('times')
        elif tipo=="ar":
            return np.cumsum(et_ref, axis=0)
        elif tipo=="d":
            return et_ref


class climatologia(object):
    """DETERMINAR CLIMATOLOGIAS

    Parametros:
        ds  : dataset, estructura de datos 
        tipo: str, cadena de caracteres ["mensual", "estacional", "all"]
        
    Metodos:
        temp: Determina climatologia (media aritmetica) de temperatura
        prcp: Determina climatologia de precipitación acumulada
        pet : Determina climatologia de evapotranspiracion potencial acumulada

    Ejemplo: determinar climatología mensual de tres años

        import indices_bioclimaticos as iibb
        
        clim = iibb.climatologia(ds)
        clim_temp = clim.prcp(tipo="mensual")

        [clim_temp], será un objeto con 12 array
    """
    def __init__(self, ds):
        self.ds_data = ds
        
    def temp(self, tipo=None):
        print(self.ds_data)
        if tipo is not None:
            if tipo=="mensual":
                ps = self.ds_data.groupby('times.month').mean(dim='times')
                return ps

            elif tipo=="estacional":
                self.s = self.ds_data.groupby('times.season').mean(dim='times')
                return ps

            elif tipo=="all":
                ps = self.ds_data.mean(dim='times')
                return ps

    def prcp(self, tipo=None):
        print(self.ds_data)
        if tipo is not None:
            if tipo=="mensual":
                ps = self.ds_data.groupby('times.month').sum(dim='times')
                return ps

            elif tipo=="estacional":
                self.s = self.ds_data.groupby('times.season').sum(dim='times')
                return ps

            elif tipo=="all":
                ps = self.ds_data.sum(dim='times')
                return ps

    def pet(self, tipo=None):
        print(self.ds_data)
        if tipo is not None:
            if tipo=="mensual":
                ps = self.ds_data.groupby('times.month').sum(dim='times')
                return ps

            elif tipo=="estacional":
                self.s = self.ds_data.groupby('times.season').sum(dim='times')
                return ps

            elif tipo=="all":
                ps = self.ds_data.sum(dim='times')
                return ps

    def serie_tiempo(self,punto_grilla=None):
        st = self.ds_data.sel(lons=punto_grilla[0], lats=punto_grilla[1], method='nearest')
        return st
    def acumulado_total(self,):
        return np.sum(self.ds_data, axis=0)

def graficar_serie_tiempo(dic):
    import matplotlib.pyplot as plt
    from matplotlib.dates import DateFormatter

    if isinstance(dic["data"], list):
       prcp = dic["data"][0]; evap=dic["data"][1]
       tiempo=prcp.times.data
       ds_times = tiempo.astype(str).tolist()
       greg_date = []
       for i in range(len(ds_times)):
           greg_date.append(ds_times[i].split('T')[0])
       greg_date = np.array(greg_date, dtype="datetime64"); julian_date = julian_date; ds_jj=jj

       st_prcp = prcp.sel(lons=dic["punto_grilla"][0], lats=dic["punto_grilla"][1], method='nearest')
       st_evap = evap.sel(lons=dic["punto_grilla"][0], lats=dic["punto_grilla"][1], method='nearest')

    elif len(dic["data"].times.data)==12:
        ds=dic["data"]; tiempo = ds.times.data
        st = ds.sel(lons=dic["punto_grilla"][0], lats=dic["punto_grilla"][1], method='nearest')
        ds_times = tiempo.astype(str).tolist()
        greg_date = []
        for i in range(len(ds_times)):
            #greg_date.append(dt.datetime.strptime(ds_times[i].split('T')[0])
            greg_date.append(ds_times[i].split('T')[0])
        greg_date = np.array(greg_date, dtype="datetime64")
    else:
        ds=dic["data"]; tiempo = ds.times.data
        st = ds.sel(lons=dic["punto_grilla"][0], lats=dic["punto_grilla"][1], method='nearest')
        ds_times = tiempo.astype(str).tolist()
        greg_date = []
        for i in range(len(ds_times)):
            greg_date.append(ds_times[i].split('T')[0])
        greg_date = np.array(greg_date, dtype="datetime64")

    #fig = plt.figure(figsize=(9,6))
    #ax = fig.add_axes([0.08, 0.05, 0.88, 0.9])
    fig = plt.figure(figsize=(9,5))
    ax = fig.add_axes([0.08, 0.05, 0.9, 0.9])
    #ax.plot(st.times.data, st.data, "bo-")
    if isinstance(dic["data"], list):
        ax.plot(greg_date, st_prcp, color="blue", lw=1.5, label="Precp")
        ax.plot(greg_date, 0.37*st_evap, color="red", label="0.37xETo")
        ax.plot(greg_date, 0.5*st_evap, color="yellow", label="0.5xETo")
        ax.plot(greg_date, st_evap, color="green", label="ETo")
        ax.legend(borderpad=0.2, prop={"size":15})
        date_form =DateFormatter("%d-%m-%y")
    elif len(dic["data"].times.data):
        ax.plot(greg_date, st.data, "bo-")
        date_form =DateFormatter("%b-%y")
    else:
        ax.plot(greg_date, st.data, "bo-")
        date_form =DateFormatter("%d-%m")

    #ax.set_xlabel(dic["nombre_ejex"], fontsize=15, fontweight='black', color = '#333F4B')
    ax.set_ylabel(dic["nombre_ejey"], fontsize=15, fontweight='black', color = '#333F4B')
    #date_form =DateFormatter("%d-%m")
    ax.xaxis.set_major_formatter(date_form)
    ax.tick_params(axis='both', which='major', labelsize=12)
    ax.set_title(dic["titulo_izquierda"], fontsize=15, loc='left')
    ax.set_title(dic["titulo_derecha"], fontsize=15, loc='right')
    #ax.grid(True, color='green', linestyle='--', linewidth=0.5, zorder=0)
    ax.grid(True, color='green', linestyle='--', linewidth=0.5)
    plt.savefig(dic["img_path"]+dic["img_save_name"]+".png", format="png", transparent=False)


def extraer_indice_punto_grilla(data_indice, df, nombre_iibb):
    aws_lats = df.LAT_DEC; aws_lons = df.LON_DEC; iibb_vals=[]
    
    for ilon,ilat in zip(aws_lons, aws_lats):
        st = data_indice.sel(lons=ilon, lats=ilat, method='nearest')
        iibb_vals.append(st.values.astype(float).tolist())
    df[nombre_iibb] = iibb_vals
    return df
    
def graficar_hlineas(dic):
    import matplotlib.pyplot as plt
    df=dic["data"]       
    my_range=list(range(1,len(df.index)+1))
    fig = plt.figure(figsize=(9,16))
    ax = fig.add_axes([0.3, 0.04, 0.65, 0.94])
    # create for each expense type an horizontal line that starts at x = 0 with the length 
    # represented by the specific expense percentage value.
    ax.hlines(y=my_range, xmin=0, xmax=df[dic["nombre_var"]], color='#007ACC', alpha=0.2, linewidth=5)

    # create for each expense type a dot at the level of the expense percentage value
    ax.plot(df[dic["nombre_var"]], my_range, "o", markersize=5, color='#007ACC', alpha=0.6,axes=ax)

    # set labels
    ax.set_xlabel(dic["nombre_ejex"], fontsize=15, fontweight='black', color = '#333F4B')
    ax.set_ylabel('')

    # set axis
    ax.tick_params(axis='both', which='major', labelsize=12)
    #plt.yticks(my_range, df.index)
    plt.yticks(my_range, df.ESTACION)

    ax.set_title(dic["titulo_izquierda"], fontsize=15, loc='left')
    ax.set_title(dic["titulo_derecha"], fontsize=15, loc='right')

    # change the style of the axis spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    ax.spines['left'].set_bounds((1, len(my_range)))
    ax.set_xlim(dic["rango_val"][0], dic["rango_val"][1])

    ax.spines['left'].set_position(('outward', 8))
    ax.spines['bottom'].set_position(('outward', 5))
    plt.savefig(dic["img_path"]+dic["img_save_name"]+".png", format="png", transparent=False)

def graficar_mapa(dic):
    import matplotlib.pyplot as plt
    import cartopy.crs as ccrs
    from cartopy.feature import NaturalEarthFeature
    from cartopy.mpl.ticker import LatitudeFormatter, LongitudeFormatter

    # shapes
    import geopandas as gpd
    import cartopy.io.shapereader as shpreader
    from cartopy.feature import ShapelyFeature
    ds=dic["data"]; data=ds.data;lons=ds.lons.data;lats=ds.lats.values

    # colors color bar
    #----------------------------------------------------------------------------------------------------------------
    # import packages
    # creating colorbar labels
    rango_cb = dic["cb_rango"]
    ticks = np.arange(rango_cb[0], rango_cb[1], rango_cb[2]) #
    # plot
    #----------------------------------------------------------------------------------------------------------------
    shapefile_san_martin_depart=dic["shp_path"]+"san_martin_departamento.shp"
    shapefile_san_martin_depart_prov=dic["shp_path"]+"san_martin_provincias.shp"
    shape_san_martin = gpd.read_file(shapefile_san_martin_depart)
    shape_san_martin_prov = gpd.read_file(shapefile_san_martin_depart_prov)

    # read shape using cartopy
    shape_feature_san_martin = ShapelyFeature(shape_san_martin.geometry,
                                    ccrs.PlateCarree(), edgecolor='black')
    shape_feature_san_martin_prov = ShapelyFeature(shape_san_martin_prov.geometry,
                                    ccrs.PlateCarree(), edgecolor='black')
    # calculates the central longitude of the plot
    domain = [np.min(lons), np.max(lons), np.min(lats), np.max(lats)]
    lon_cen = 360.0+(domain[0]+domain[1])/2.0

    # creates the figure
    fig = plt.figure('map', figsize=(3, 4.65), dpi=200)
    ax = fig.add_axes([0.06, 0.15, 1, 0.8], projection=ccrs.PlateCarree(lon_cen))
    #ax.outline_patch.set_linewidth(0.3)
    ax.spines["geo"].set_linewidth(0.3)

    # add the geographic boundaries
    ax.add_feature(shape_feature_san_martin, facecolor="none", edgecolor='k', lw=0.5)
    ax.add_feature(shape_feature_san_martin_prov, facecolor="none", edgecolor='k', lw=0.3)

    if dic["tipo_cbar"] is not None:
        cmap = dic["tipo_cbar"]
    else: cmap = "RdPu"

    # plot the data
    img = ax.pcolormesh(lons, lats, data, 
                        cmap = cmap, #["YlGnBu","YlGn","BuGn","RdPu","YlOrBr"]
                        vmin=np.min(ticks), 
                        vmax=np.max(ticks),
                        transform=ccrs.PlateCarree())

    # add the colorbar
    #cb = plt.colorbar(img, ticks=ticks, orientation='horizontal', extend='both',
    #                  cax=fig.add_axes([0.12, 0.06, 0.76, 0.02]))
    cb = plt.colorbar(img, ticks=ticks, orientation='horizontal', extend=None,#'both',
                      cax=fig.add_axes([0.11, 0.06, 0.86, 0.02]))
    cb.ax.tick_params(labelsize=6, labelcolor='black', width=0.5, length=1.5, direction='out', pad=1.0)
    #cb.set_label(label='{} [{}]'.format(CMI.standard_name, CMI.units), size=5, color='black', weight='normal')
    cb.set_label(label='{}'.format(dic["cb_nombre"]), size=5, color='black', weight='normal')
    cb.outline.set_linewidth(0.5)

    # set the title
    #ax.set_title('{} - C{:02d} [{:.1f} μm]'.format(sat,band, wl), fontsize=7, loc='left')
    ax.set_title(dic["titulo_izquierda"], fontsize=7, loc='left')
    #ax.set_title(CMI.time_bounds.data[0].strftime('%Y/%m/%d %H:%M UTC'), fontsize=7, loc='right')
    ax.set_title(dic["titulo_derecha"], fontsize=7, loc='right')

    # Sets X axis characteristics
    dx = 0.5
    xticks = np.arange(domain[0], domain[1]+dx, dx)
    ax.set_xticks(xticks, crs=ccrs.PlateCarree())
    ax.xaxis.set_major_formatter(LongitudeFormatter(dateline_direction_label=True, 
                                 number_format = ".1f",
                                                    ))
    ax.set_xlabel("LONGITUD", color='black', fontsize=7, labelpad=3.0)

    # Sets Y axis characteristics
    dy = 0.3
    yticks = np.arange(domain[2], domain[3]+dy, dy)
    ax.set_yticks(yticks, crs=ccrs.PlateCarree())
    ax.yaxis.set_major_formatter(LatitudeFormatter(number_format = ".1f",
                                                   degree_symbol=" "))
    ax.set_ylabel("LATITUD", color='black', fontsize=7, labelpad=3.0)
    # Sets tick characteristics
    ax.tick_params(left=True, right=True, bottom=True, top=True,
                   labelleft=True, labelright=False, labelbottom=True, labeltop=False,
                   length=0.0, width=0.05, labelsize=6, labelcolor='black')

    # Sets grid characteristics
    ax.gridlines(xlocs=xticks, ylocs=yticks, alpha=0.6, color='gray',
                 draw_labels=False, linewidth=0.25, linestyle='--')

    # set the map limits
    ax.set_extent([domain[0]+360.0, domain[1]+360.0, domain[2], domain[3]], crs=ccrs.PlateCarree())
    plt.savefig(dic["img_path"]+dic["img_save_name"]+".png", format="png", transparent=True)
    

