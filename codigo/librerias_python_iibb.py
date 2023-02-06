import os

def create_env(name_env, python_version):
	os.system("conda create -n "+name_env+" python="+python_version+" anaconda")
	os.system("conda info --envs")
	#os.system("source activate geoscience")
    #os.system("conda activate geoscience")
	#os.system("conda info --envs")

def instalar_pkg(pkg):
    for ipkg in pkg:
        os.system("conda install -c conda-forge "+ipkg+" -y")
        
def update_anaconda():
    os.system("conda update anaconda -y")
    os.system("conda install spyder=5.3.3")


# paquetes
pkg_iibb=["numpy==1.21.5", "matplotlib==3.6.2", "scipy==1.5.3", "pandas==1.5.2", "xarray==2022.12.0",
            "geopandas", "pyproj", "hdf5","pyshp", "netcdf4", "gdal", "cartopy", "fiona"]

pkg_iibb_1=["numpy", "matplotlib", "scipy", "pandas", "xarray",
            "geopandas", "pyproj", "hdf5","pyshp", "netcdf4", "gdal", "cartopy", "fiona"]


# Instalar
instalar_pkg(pkg_iibb_1)
update_anaconda()
create_env("geoscience","3.9")
