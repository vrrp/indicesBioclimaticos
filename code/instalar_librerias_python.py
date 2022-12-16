import os
"""
conda info --envs
for gdal:
	conda install gdal "libgfortran-ng=7.2.0=hdf63c60_3"
	$ python -c "import gdal"
	$ echo $?

	conda create --override-channels -c conda-forge -n OSMNX python=3 osmnx
	conda update --all
"""
def create_env(name_env, python_version):
	os.system("conda create -n "+name_env+" python="+python_version+" anaconda")
	os.system("conda info --envs")
	os.system("source activate geoscience")
	os.system("conda info --envs")

def install_geoscience_py_pkg():
	#os.system("conda config --add channels conda-forge")
	os.system("conda install -c conda-forge numpy matplotlib pyshp -y")
	os.system("conda install -c conda-forge hdf5 -y")
	os.system("conda install -c conda-forge netcdf4 -y")
	os.system("conda install -c conda-forge gdal -y")
	os.system("conda install -c conda-forge pandas geopandas pytables -y")
	os.system("conda install -c conda-forge plotly -y")
	os.system("conda install -c conda-forge ffmpeg -y")
	os.system("conda install -c conda-forge pillow -y")
	os.system("conda install -c conda-forge scipy scikit-learn scikit-image -y")
	os.system("conda install -c conda-forge xarray -y")
	os.system("conda install -c conda-forge cartopy holoviews datashader dill -y")
	os.system("conda install -c conda-forge ipyleaflet gmaps -y")
	os.system("conda install -c conda-forge graphviz python-graphviz -y")
	os.system("conda install -c conda-forge ecmwf-api-client -y")
	os.system("conda install -c conda-forge siphon -y")

#create_env("geoscience","3.9")
install_geoscience_py_pkg()

"""
$ conda update -n base
"""
