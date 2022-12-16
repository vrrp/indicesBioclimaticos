import os

def install_geoscience_py_pkg():
	#os.system("conda config --add channels conda-forge")
	os.system("conda install -c conda-forge numpy matplotlib pyshp -y")
	os.system("conda install -c conda-forge hdf5 -y")
	os.system("conda install -c conda-forge netcdf4 -y")
	os.system("conda install -c conda-forge gdal -y")
	os.system("conda install -c conda-forge pandas geopandas pytables -y")
	os.system("conda install -c conda-forge ffmpeg -y")
	os.system("conda install -c conda-forge xarray -y")
	os.system("conda install -c conda-forge cartopy -y")
	
install_geoscience_py_pkg()

"""
$ conda update -n base
"""
