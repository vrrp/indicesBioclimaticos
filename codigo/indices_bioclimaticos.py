"""  INDICES BIOCLIMATICOS PARA MAIZ Y CAFE

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
"""
__author__ = "VR ROJAS"
__license__="GPL"
__version__="0.1"
__email__="vr.rojaspozo@gmail.com"

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import xarray as xr
import datetime as dt
#from osgeo import gdal, osr, ogr

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
    Clase:
        extrar(arg1, arg2)
    
    Metodo:
        variable(arg3, arg4)
        
    Parametros:
        arg1: ruta de directorio data
        arg2: nombre de archivo netcdf
        arg3: nombre variable
        arg4: rango tiempo
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
    """
    Clase:
        indices_termicos
        
    Metodos:
        ihg() : indice heliotermico de geslim
        amplitud_termica(arg2)
        tiempo_termico(arg1)
        indice_termal_general(arg1)
        unidades_calor(arg1)
        calor_magnitud_dia(arg1)
        indice_estres_calor(arg1, arg2)
        gdd(arg1, arg2): grados dias de crecimiento
        gddm(arg1, arg2): grados dias de crecimiento modificado
        aptitud_termica_map(arg3)
        aptitud_termica_puntoGrilla(arg4)
        heliotermico_huglin(arg1, arg2)        
    
    Parametros:
        arg1: "a", "ar", "d"
        arg2: t_base = [valor numerico]
        arg3: temp_umbral=[t1,t2]
        arg4: lonlat=[lon, lat]
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

    def heliotermico_huglin(self,tipo, tb):
        k=1
        ihh = ((self.t_mean-tb)+(self.ds_temp_max-tb))/2*k
        if tipo=="a":
            return  ihh.sum('times')
        elif tipo=="ar":
            return np.cumsum(ihh, axis=0)
        elif tipo=="d":
            return ihh

    def aptitud_termica_map(self,temp_umbral):
        temp_mean = self.t_mean
        matriz_umbral = np.zeros((self.nrows, self.ncols)); matriz_umbral[...]=np.nan
        matriz_3clases = np.zeros((self.nrows, self.ncols)); matriz_3clases[...]=np.nan
        for irow in range(self.nrows):
            for icol in range(self.ncols):
                i_values,i_frecuencias = np.unique(np.round(temp_mean[:,irow,icol].values, 0), return_counts=True)
                dic={}
                for i in range(len(i_values)):
                    dic[i_frecuencias[i]]=i_values[i]
                i_temp = [k for k in dic.values()]
                i_frec = [k for k in dic.keys()]
                matriz_umbral[irow,icol] = dic[np.max(i_frec)]
                
        for irow in range(self.nrows):
            for icol in range(self.ncols):
                count = matriz_umbral[irow,icol]
                if 10<=count and count<temp_umbral[0]:
                    matriz_3clases[irow, icol]=0
                elif temp_umbral[0]<=count and count<=temp_umbral[1]:
                    matriz_3clases[irow, icol]=1
                elif temp_umbral[1]<count:
                    matriz_3clases[irow, icol]=2     

        ds_temp_optima = xr.Dataset(data_vars={"temp_optima":(("lats","lons"), matriz_umbral),
                                               "temp_optima_3clases":(("lats","lons"), matriz_3clases),
                                       },
                            coords ={"lats":self.ds_lats, 
                                     "lons":self.ds_lons},
                           )
        return ds_temp_optima["temp_optima"], ds_temp_optima["temp_optima_3clases"]                
                    
    def aptitud_termica_puntoGrilla(self,lonlat):
        temp_mean = self.t_mean
        it = temp_mean.sel(lons=lonlat[0], lats=lonlat[1], method='nearest')
        values,frecuencias = np.unique(np.round(it.values, 0), return_counts=True)
        n_elements = len(it)
        distrib_prob = frecuencias/n_elements
        dic={}
        for i in range(len(values)):
            dic[frecuencias[i]]=values[i]
        return dic, distrib_prob
    
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
        for irow in range(self.nrows):
            for icol in range(self.ncols):
                if tt[irow,icol]<0:
                    tt[irow, icol]=0
                else: pass
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
    
    def ihg(self, tipo=None):
        """CALCULO DE igh

        Parametros:
            t_mean: temperatura promedio
            phi   : 
        """
        t_mean = (self.ds_temp_min.values + self.ds_temp_max.values)/2
        phi = np.pi*np.array(self.ds_lats)/180 # espacial dims

        delta = 0.409*np.sin(2*np.pi*np.array(self.ds_jj)/365-1.39) # tiempo dims
        
        n_phi= len(phi); n_delta = len(delta)
        nlevs, nrows, ncols = np.shape(t_mean)
        ihg = np.zeros((nlevs, nrows, ncols)); ihg[...]=np.nan

        N = 24*np.arccos(-np.tan(phi)*np.tan(delta[0]))/np.pi # fotoperiodo
        for ilev in range(n_delta):
            for irow in range(n_phi):
                ihg[ilev, irow, :]= t_mean[ilev,irow,: ]*N[irow]

        #ihg_data = np.sum(ihg, axis=0)/100
        ds_ihg = xr.Dataset(data_vars={"data":(("times","lats","lons"), ihg)},
                            coords ={"times":self.greg_date ,"lats":self.ds_lats, "lons":self.ds_lons},
                           )
        #return ds_ihg["data"]
        if tipo is None:
            return ds_ihg["data"].sum(dim='times')/100
        else:
            return self.greg_date, self.julian_date , N
            

class indices_hidricos(object):
    """
    Clase:
        indices_hidricos
        
    Metodos:
        et_referencia(arg1)
        lluvia_acumulada(arg1)
        prcp_menos_evap(arg1)
        deficit_hidrico(arg1, arg2, arg2)
        exceso_hidrico(arg1, arg2, arg2)
        indice_humedad(arg1)
        indice_bienestar_hidrico(arg1, arg2, arg2)
        duracion_periodo_humedo(arg3)       
    
    Parametros:
        arg1: "a", "ar", "d", "m"
        arg2: [valor numerico]
        arg3: punto_grilla=[lon, lat]
    """
    
    def __init__(self, ds_data1, ds_data2=None):
        self.ds_data1 = ds_data1
        self.ds_times = self.ds_data1["times"].values
        self.ds_lats = self.ds_data1["lats"].values
        self.ds_lons = self.ds_data1["lons"].values
        self.nlevs, self.nrows, self.ncols = np.shape(self.ds_data1)
        
        if ds_data2 is not None:
            self.ds_data2 = ds_data2
            
    def duracion_periodo_humedo(self, punto_grilla):
        prcp = self.ds_data1; evap = self.ds_data2
        start_time, end_time = (self.ds_times[0].astype(str).tolist().split("T")[0],
                                self.ds_times[-1].astype(str).tolist().split("T")[0])
        time_decadiario = pd.date_range(start_time, periods=37, freq='10D')#.to_pydatetime()
        #times_np= df_time['date'].to_numpy()
        
        list_time_decadiario=[]
        for i in time_decadiario:
            list_time_decadiario.append(i.strftime("%d-%b"))
                        
        drange = pd.date_range(start_time, end_time, freq='1D')
        
        xi = prcp.sel(lons=punto_grilla[0], lats=punto_grilla[1], method='nearest').data
        yi= evap.sel(lons=punto_grilla[0], lats=punto_grilla[1], method='nearest').values               
        df = pd.DataFrame(data={'pp':xi, 'eto':yi},
                          index=drange,
                          )
        
        dz = df.groupby(df.index.year, group_keys=True).apply(lambda x:x.groupby(pd.Grouper(freq='10D')).sum()).reset_index().drop('level_0',axis=1).rename({'level_1':'date'},axis=1).set_index('date')
        def countGroups(dx):
            N = len(dx)
            dx.loc[(dx['pp']>dx['eto']),'ni'] = 1
            dx['frec'] = dx['ni'].sum()/N
            return dx
        def countGroups2(dx):
            N = len(dx)
            dx.loc[(dx['pp']>dx['eto']*0.5),'ni'] = 1
            dx['frec'] = dx['ni'].sum()/N
            return dx
        dz1 = dz.groupby(dz.index.strftime('%j'), group_keys=False).apply(countGroups)
        dz2 = dz1.groupby(dz1.index.strftime('%j')).mean()
        
        dy1 = dz.groupby(dz.index.strftime('%j'), group_keys=False).apply(countGroups2)
        dy2 = dy1.groupby(dy1.index.strftime('%j')).mean()
        
        df_frec = pd.DataFrame(data={'frec_etp':np.array(dz2["frec"]), 'frec_0.5etp':np.array(dy2["frec"])},
                          index=list_time_decadiario,
                          )
        return df_frec

    def indice_bienestar_hidrico(self,tipo,fc,iswc):
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
                        condition=iswc - pme[ilev,irow,icol]
                        if condition>=fc:
                            swc[ilev,irow,icol]=fc
                        elif condition<=0:
                            swc[ilev,irow,icol]=0
                        else:
                            swc[ilev,irow,icol]=condition
                    else:
                        condition=swc[ilev,irow,icol] - pme[ilev,irow,icol]
                        if condition>=fc:
                            swc[ilev,irow,icol]=fc
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

    def deficit_hidrico(self,tipo,fc,iswc):
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
                        condition=iswc - pme[ilev,irow,icol]
                        if condition>=fc:
                            swc[ilev,irow,icol]=fc
                        elif condition<=0:
                            swc[ilev,irow,icol]=0
                        else:
                            swc[ilev,irow,icol]=condition
                    else:
                        condition=swc[ilev,irow,icol] - pme[ilev,irow,icol]
                        if condition>=fc:
                            swc[ilev,irow,icol]=fc
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
        
        df = evap_month - ae
        ds_df = xr.Dataset(data_vars={"df":(("times","lats","lons"), df),
                                       },
                            coords ={"times": times,
                                     "lats":self.ds_lats, 
                                     "lons":self.ds_lons},
                           )
        if tipo=="a":
            return  ds_df["df"].sum('times')
        elif tipo=="ar":
            return np.cumsum(ds_df["df"], axis=0)
        elif tipo=="m":
            return ds_df["df"]

    def exceso_hidrico(self,tipo,fc,iswc):
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
        eh = np.zeros(np.shape(prcp_month))
                 
        # calculo de swc
        for ilev in range(nlevs):
            for irow in range(nrows):
                for icol in range(ncols):
                    if ilev==0:
                        condition = iswc - pme[ilev,irow,icol]
                        if condition>=fc:
                            swc[ilev,irow,icol] = fc
                        elif condition<=0:
                            swc[ilev,irow,icol] = 0
                        else:
                            swc[ilev,irow,icol] = condition
                    else:
                        condition= swc[ilev,irow,icol] - pme[ilev,irow,icol]
                        if condition>=fc:
                            swc[ilev,irow,icol] = fc
                        elif condition<=0:
                            swc[ilev,irow,icol] = 0
                        else:
                            swc[ilev,irow,icol] = condition

        # calculo de delta
        for ilev in range(nlevs):
            for irow in range(nrows):
                for icol in range(ncols):
                    if ilev==0:
                        delta[ilev,irow,icol] = swc[ilev,irow,icol] - iswc
                    else:
                        delta[ilev,irow,icol] = swc[ilev,irow,icol] - swc[ilev-1, irow-1, icol-1]
        
        # calculo de estres hidrico
        for ilev in range(nlevs):
            for irow in range(nrows):
                for icol in range(ncols):
                    condition = prcp_month[ilev,irow,icol] - evap_month[ilev,irow,icol]                
                    if  condition>=0:
                        eh[ilev,irow,icol] = prcp_month[ilev,irow,icol]-evap_month[ilev,irow,icol]-delta[ilev,irow,icol]

                    else:
                        eh[ilev,irow,icol] = 0
        
        ds_eh = xr.Dataset(data_vars={"eh":(("times","lats","lons"), eh),
                                       },
                            coords ={"times": times,
                                     "lats":self.ds_lats, 
                                     "lons":self.ds_lons},
                           )
        if tipo=="a":
            return  ds_eh["eh"].sum('times')
        elif tipo=="ar":
            return np.cumsum(ds_eh["eh"], axis=0)
        elif tipo=="m":
            return ds_eh["eh"]

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

def graficar_serie_tiempo(dic, tipo):
    import matplotlib.pyplot as plt
    from matplotlib.dates import DateFormatter
    #fig = plt.figure(figsize=(9,5))
    #ax = fig.add_axes([0.08, 0.12, 0.9, 0.85])
    #if isinstance(list(dic["data"].columns), list):
    if tipo=="dataframe":
        fig = plt.figure(figsize=(10,6))
        ax = fig.add_axes([0.08, 0.12, 0.9, 0.8])
        
        ax.plot(dic["data"]["frec_etp"], "o-",color="blue", lw=3.5, alpha=0.5, label="Prcp > Etp")
        ax.plot(dic["data"]["frec_0.5etp"], "o-",color="red", lw=3.5, alpha=0.8, label="Prcp > 0.5Etp")
        plt.xticks(rotation=60)
        ax.legend(borderpad=0.2, prop={"size":15})

    elif tipo=="array":
        fig = plt.figure(figsize=(9,5))
        ax = fig.add_axes([0.08, 0.12, 0.9, 0.85])
        ds=dic["data"]; tiempo = ds.times.data
        st = ds.sel(lons=dic["punto_grilla"][0], lats=dic["punto_grilla"][1], method='nearest')
        ds_times = tiempo.astype(str).tolist()
        greg_date = []
        for i in range(len(ds_times)):
            greg_date.append(ds_times[i].split('T')[0])
        greg_date = np.array(greg_date, dtype="datetime64")
        ax.plot(greg_date, st.data, "bo-")
        date_form =DateFormatter("%d-%m")
        ax.xaxis.set_major_formatter(date_form)

    #ax.set_xlabel(dic["nombre_ejex"], fontsize=15, fontweight='black', color = '#333F4B')
    ax.set_ylabel(dic["nombre_ejey"], fontsize=15, fontweight='black', color = '#333F4B')
    #date_form =DateFormatter("%d-%m")
    ax.tick_params(axis='both', which='major', labelsize=11)
    ax.set_title(dic["titulo_izquierda"], fontsize=14, loc='left')
    ax.set_title(dic["titulo_derecha"], fontsize=14, loc='right')
    ax.grid(True, color='green', linestyle='--', linewidth=0.5)
    if dic["img_save_name"] is not None:
        plt.savefig(dic["img_path"]+dic["img_save_name"]+".png", format="png", transparent=False)

def extraer_indice_punto_grilla(data_indice, df, nombre_iibb):
    aws_lats = df.LAT_DEC; aws_lons = df.LON_DEC; iibb_vals=[]
    
    for ilon,ilat in zip(aws_lons, aws_lats):
        st = data_indice.sel(lons=ilon, lats=ilat, method='nearest')
        iibb_vals.append(st.values.astype(float).tolist())
    df[nombre_iibb] = iibb_vals
    return df
    
def graficar_barras(dic):
    import matplotlib.pyplot as plt
    data_dic=dic["data"]       
    x_values=[k for k in data_dic.values()]
    y_frec  =[k for k in data_dic.keys()]
    
    fig = plt.figure(figsize=(8,10))
    ax = fig.add_axes([0.1, 0.07, 0.88, 0.88])

    bar_plot=ax.bar(x_values, y_frec)
    
    for ival in bar_plot:
        height = ival.get_height()
        ax.text(ival.get_x()+ival.get_width()/2, 1.002*height,
                '%d'%int(height),size=16, ha='center',va='bottom')

    ax.set_xlabel(dic["nombre_ejex"], fontsize=15, fontweight='black', color = '#333F4B')
    ax.set_ylabel(dic["nombre_ejey"], fontsize=15, fontweight='black', color = '#333F4B')
    ax.tick_params(axis='both', which='major', labelsize=14)
    ax.set_title(dic["titulo_izquierda"], fontsize=15, loc='left')
    ax.set_title(dic["titulo_derecha"], fontsize=15, loc='right')
    ax.grid(True, color='green', linestyle='--', linewidth=0.5, zorder=0)
    if dic["img_save_name"] is not None:
        plt.savefig(dic["img_path"]+dic["img_save_name"]+".png", format="png", transparent=False)

def graficar_hlineas(dic):
    import matplotlib.pyplot as plt
    df=dic["data"]       
    my_range=list(range(1,len(df.index)+1))
    fig = plt.figure(figsize=(9,16))
    ax = fig.add_axes([0.3, 0.04, 0.65, 0.94])    
    ax.hlines(y=my_range, xmin=0, xmax=df[dic["nombre_var"]], color='#007ACC', alpha=0.2, linewidth=5)
    ax.plot(df[dic["nombre_var"]], my_range, "o", markersize=5, color='#007ACC', alpha=0.6,axes=ax)
    # set labels
    ax.set_xlabel(dic["nombre_ejex"], fontsize=15, fontweight='black', color = '#333F4B')
    ax.set_ylabel('')
    # set axis
    ax.tick_params(axis='both', which='major', labelsize=12)
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
        
    if dic["img_save_name"] is not None:
        plt.savefig(dic["img_path"]+dic["img_save_name"]+".png", format="png", transparent=False)
    
def xy2latlon(x,y):
    import pyproj
    
    inproj = pyproj.Proj(init = "epsg:32718")
    outproj = pyproj.Proj(init = "epsg:4326")
    xlon, ylat = pyproj.transform(inproj, outproj, x, y)
    return xlon, ylat

def plot_shp(shpFile, color= None, convert=None):

        import shapefile as shp
        sf = shp.Reader(shpFile)
        for shape in sf.shapeRecords():
                # indexando cada componente del mapa 
                l = shape.shape.parts
    
                len_l = len(l)  # cantidad de paises i.e. islas y continentes
                xsh = [i[0] for i in shape.shape.points[:]] # lista de latitudes
                ysh = [i[1] for i in shape.shape.points[:]] # lista de longitudes
                l.append(len(xsh)) # asegurar el cierre del Ãºltimo componente

                if convert is not None:
                        xx, yy =[],[]
                        for ix, iy in zip(xsh, ysh):
                                ix, iy = xy2latlon(ix, iy)
                                xx.append(ix); yy.append(iy)
                        xsh=xx; ysh=yy

                        for k in range(len_l):
                                # graficar cada componente del mapa
                                # l[k] a l[k + 1] es el conjunto de puntos que forman cada componente
                                plt.plot(xsh[l[k]:l[k + 1]], ysh[l[k]:l[k + 1]],
                                        linewidth=3, 
                                        #markersize=0.1,
                                        linestyle="-", 
                                        #marker="o",
                                        color=color
                                        )
                else:
                        for k in range(len_l):
                                # graficar cada componente del mapa
                                # l[k] a l[k + 1] es el conjunto de puntos que forman cada componente
                                plt.plot(xsh[l[k]:l[k + 1]], ysh[l[k]:l[k + 1]],
                                        linewidth=1.1, 
                                        #markersize=0.1,
                                        linestyle="-", 
                                        #marker="o",
                                        color=color ,
                                        alpha=0.8)
def put_shapes(shape_dic):
    shape_names = list(shape_dic.keys())[:-1]
    colors4shapes = shape_dic[list(shape_dic.keys())[-1]]

    for i in range (len(shape_names)):
        if shape_names[i]=="cuenca_vilcanota":
            plot_shp(shape_dic[shape_names[i]], color=colors4shapes[i], convert="yes")

        else:
            plot_shp(shape_dic[shape_names[i]], color=colors4shapes[i])

def graficar_mapa(dic, clase_cbar=None):
    lats=dic["data"].lats.data;lons=dic["data"].lons.values;data=dic["data"].values

    labelfont = {
			'family' : 'serif',  # (cursive, fantasy, monospace, serif)
			'color'  : 'black',       # html hex or colour name
			'weight' : 'heavy',      # (normal, bold, bolder, lighter)
			'size'   : 14,            # default value:12
			    }

    fig = plt.figure("map",facecolor='w', figsize=(7.0, 10.0))
    ax = fig.add_axes([0.14, 0.14, 0.83, 0.83])

    if dic["tipo_cbar"] is not None:
        cmap=dic["tipo_cbar"]
    else: cmap="YlOrBr" #["YlGnBu","YlGn","BuGn","RdPu","YlOrBr"]
    
    rango_cb = dic["cb_rango"]
    ticks = np.arange(rango_cb[0], rango_cb[1], rango_cb[2]) #
    x, y = (lons, lats)
    img = plt.pcolormesh(x, y, data, alpha=None, cmap=cmap,
    			     vmin=np.min(ticks),
    			     vmax=np.max(ticks),
    			     )
    if dic["shp_path"] is not None:
        shape ={"sm_dep":dic["shp_path"]+"san_martin_departamento.shp",
                "sm_pro":dic["shp_path"]+"san_martin_provincias.shp",
                "color4shapes":["k","k"]
                }
        #plot_shp(shp_peru)
        shape_names = list(shape.keys())[:-1]
        colors4shapes = shape[list(shape.keys())[-1]]
                               
        for i in range (len(shape_names)):
            if shape_names[i]=="cuenca_vilcanota":
                plot_shp(shape[shape_names[i]], color=colors4shapes[i], convert="yes")
            else:
                plot_shp(shape[shape_names[i]], color=colors4shapes[i])
    
    def get_ticksAxis(data_axis, axis_type):
    	ticks_values=data_axis
    	ticks_labels =['%.1f'%i+axis_type for i in ticks_values]
    	return ticks_values, ticks_labels
    xticks_values, xticks_labels = get_ticksAxis(lons, "°W")
    yticks_values, yticks_labels = get_ticksAxis(lats, "°S")
    
    ax.set_xticks(xticks_values[::5])
    ax.set_xticklabels(xticks_labels[::5], rotation=0)
    
    ax.set_yticks(yticks_values[::5])
    ax.set_yticklabels(yticks_labels[::5], rotation=0)
    
    ax.set_xlabel('LONGITUD', fontsize=12, fontweight="heavy")
   
    ax.set_ylabel('LATITUD', fontsize=12, fontweight="bold")
    ax.set_title(dic["titulo_izquierda"], fontsize=12, loc='left')
    ax.set_title(dic["titulo_derecha"], fontsize=12, loc='right')
    ax.tick_params(axis="both", labelcolor="k", labelsize=14, labelrotation=0)
    ax.grid(True, which='major', color='grey', linestyle='--', alpha=1)
    
    cb = plt.colorbar(img, ticks=ticks, orientation='horizontal', extend=None,#'both',
    	              cax=fig.add_axes([0.11, 0.05, 0.86, 0.02]))
    cb.ax.tick_params(labelsize=12, labelcolor='black', width=0.5, length=1.5, direction='out', pad=1.0)
    cb.set_label(label='{}'.format(dic["cb_nombre"]), size=12, color='black', weight='normal')
    cb.outline.set_linewidth(0.5) 
             
    if dic["img_save_name"] is not None:
        plt.savefig(dic["img_path"]+dic["img_save_name"]+".png", format="png", dpi=150)

def graficar_mapa_clases(dic, clase_cbar=None):
    lats=dic["data"].lats.data;lons=dic["data"].lons.values;data=dic["data"].values
    labelfont = {
			'family' : 'serif',  # (cursive, fantasy, monospace, serif)
			'color'  : 'black',       # html hex or colour name
			'weight' : 'heavy',      # (normal, bold, bolder, lighter)
			'size'   : 14,            # default value:12
			    }

    fig = plt.figure("map",facecolor='w', figsize=(7.0, 10.0))
    ax = fig.add_axes([0.14, 0.14, 0.83, 0.83])

    if dic["tipo_cbar"] is not None:
        cmap=dic["tipo_cbar"]
    else: cmap="YlOrBr" #["YlGnBu","YlGn","BuGn","RdPu","YlOrBr"]
    
    rango_cb = dic["cb_rango"]
    ticks = np.arange(rango_cb[0], rango_cb[1], rango_cb[2]) #
    x, y = (lons, lats)
    import matplotlib
    from matplotlib.colors import ListedColormap
    col_dict={0:clase_cbar[0],
    	      1:clase_cbar[1],
    	      2:clase_cbar[2],
    	      }
    cm = ListedColormap([col_dict[x] for x in col_dict.keys()])
    labels = np.array(["MÃ­nimo","Moderado","MÃ¡ximo"])
    len_lab=len(labels)
    norm_bins = np.sort([*col_dict.keys()])+0.5
    norm_bins = np.insert(norm_bins, 0, np.min(norm_bins)-1.0)
    norm = matplotlib.colors.BoundaryNorm(norm_bins, len_lab,clip=True)
    fmt = matplotlib.ticker.FuncFormatter(lambda x, pos: labels[norm(x)])
    
    img = plt.pcolormesh(x, y, data, alpha=None, cmap=cm,
    		         norm=norm,
    		         )
    diff = norm_bins[1:]-norm_bins[:-1]
    tickz = norm_bins[:-1]+diff/2
       
    if dic["shp_path"] is not None:
        shape ={"sm_dep":dic["shp_path"]+"san_martin_departamento.shp",
                "sm_pro":dic["shp_path"]+"san_martin_provincias.shp",
                "color4shapes":["k","k"]
                }
        #plot_shp(shp_peru)
        shape_names = list(shape.keys())[:-1]
        colors4shapes = shape[list(shape.keys())[-1]]
                               
        for i in range (len(shape_names)):
            if shape_names[i]=="cuenca_vilcanota":
                plot_shp(shape[shape_names[i]], color=colors4shapes[i], convert="yes")
            else:
                plot_shp(shape[shape_names[i]], color=colors4shapes[i])

    def get_ticksAxis(data_axis, axis_type):
    	ticks_values=data_axis
    	ticks_labels =['%.1f'%i+axis_type for i in ticks_values]
    	return ticks_values, ticks_labels
    xticks_values, xticks_labels = get_ticksAxis(lons, "°W")
    yticks_values, yticks_labels = get_ticksAxis(lats, "°S")
    
    ax.set_xticks(xticks_values[::5])
    ax.set_xticklabels(xticks_labels[::5], rotation=0)
    
    ax.set_yticks(yticks_values[::5])
    ax.set_yticklabels(yticks_labels[::5], rotation=0)
    
    ax.set_xlabel('LONGITUD', fontsize=12, fontweight="heavy")
    ax.set_ylabel('LATITUD', fontsize=12, fontweight="bold")
    ax.set_title(dic["titulo_izquierda"], fontsize=12, loc='left')
    ax.set_title(dic["titulo_derecha"], fontsize=12, loc='right')
    ax.tick_params(axis="both", labelcolor="k", labelsize=14, labelrotation=0)
    ax.grid(b=True, which='major', color='grey', linestyle='--', alpha=1)
    cb = plt.colorbar(img, ticks=tickz, format=fmt, orientation='horizontal', extend=None,#'both',
    		      shrink=0.5, aspect=5, pad=0.3,
    		      cax=fig.add_axes([0.11, 0.06, 0.86, 0.02]))
    cb.ax.tick_params(labelsize=12, labelcolor='black', width=0.5, length=1.5, direction='out', pad=1.0)
    cb.set_label(label='{}'.format(dic["cb_nombre"]), size=12, color='black', weight='normal')
    cb.outline.set_linewidth(0.5)             
    if dic["img_save_name"] is not None:
        plt.savefig(dic["img_path"]+dic["img_save_name"]+".png", format="png", dpi=150)
