import numpy as np
from scipy.odr import odrpack
import os
import pandas as pd
import xarray as xr
import sys
import math

def fit_tls(x: np.ndarray, y: np.ndarray) -> float:
	"""Fit total least squares model to data
	This function fits a total least squares (also known as orthogonal distance regression) model to 2-dimensional data.
	The model has the form `y = m * x`, where m is the "slope". (It has an intercept at y==0).
	See Also:
			At its core, the function uses scipy's `Orthogonal Distance Regression`_ module
			.. _Orthogonal Distance Regression:
					https://docs.scipy.org/doc/scipy/reference/odr.html
			Args:
					x: 1-dimensional Numpy array
					y: 1-dimensional Numpy array of the same size as `x`

			Returns:
					The slope of the fitted model

			"""
	odr_data = odrpack.RealData(x, y)
	model = odrpack.Model(lambda beta, x_: beta[0] * x_)
	odr_container = odrpack.ODR(odr_data, model, beta0=[1.0])
	slope = odr_container.run().beta[0]
	#TODO PLOT SECTOR 0 some pairs (weird results)
	return slope

def direccio(u, v):
	d = np.arctan2(u, v)*180/math.pi + 180
	return d


def wind_speed(u, v):
	ws = np.sqrt(u**2, v**2)
	return ws

def read_netcdf(filename):
	if os.path.isfile(filename):
		#print('\nLoad: '+filename )
		xr_mast = xr.open_dataset(filename)
		xr_mast['M'] = xr.apply_ufunc(wind_speed, xr_mast['U'], xr_mast['V'])
		xr_mast['M'].name = 'Wind Speed'
		xr_mast['Dir'] = xr.apply_ufunc(direccio, xr_mast['U'], xr_mast['V'])
		xr_mast['Dir'].name = 'Wind Direction'
		return xr_mast
	else:
		print ('File' + filename + ' not found')
		return -1
