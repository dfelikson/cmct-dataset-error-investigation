#!/usr/bin/env python

from netCDF4 import Dataset

import glob

import numpy as np
from matplotlib import pyplot as plt

cmct_dir = 'data/GLAS_Data/2005'
cmct_files = glob.glob(cmct_dir + '/*final.nc')

zoom_bounds = None
zoom_bounds = [310, 320, 75, 80]
#zoom_bounds = [312.0, 312.1, 78.05, 78.10]

LON_DEGE = list()
LAT_DEGN = list()
WGS84ELEV_M = list()
DEM_M  = list()
for i_file, cmct_file in enumerate(cmct_files):
    #print('plotting file {:4d} / {:4d}: {:s}'.format(i_file, len(cmct_files), cmct_file))
    ncfile = Dataset(cmct_file, 'r')

    if zoom_bounds:
        idx = (ncfile['LON_DEGE'][:] > zoom_bounds[0]) & (ncfile['LON_DEGE'][:] < zoom_bounds[1]) & \
              (ncfile['LAT_DEGN'][:] > zoom_bounds[2]) & (ncfile['LAT_DEGN'][:] < zoom_bounds[3])
    else:
        idx = np.arange(len(ncfile['LON_DEGE'][:]))

    if np.sum(idx) > 0:
        LON_DEGE.extend(ncfile['LON_DEGE'][idx])
        LAT_DEGN.extend(ncfile['LAT_DEGN'][idx])
        WGS84ELEV_M.extend(ncfile['WGS84ELEV_M'][idx])
        DEM_M.extend(ncfile['DEM_M'][idx])
        #for i in np.where(idx)[0]:
        #    print('{:5.0f} {:5.0f} {:5.0f}'.format(ncfile['WGS84ELEV_M'][i], ncfile['DEM_M'][i], ncfile['WGS84ELEV_M'][i]-ncfile['DEM_M'][i]))

LON_DEGE = np.array(LON_DEGE)
LAT_DEGN = np.array(LAT_DEGN)
WGS84ELEV_M = np.array(WGS84ELEV_M)
DEM_M = np.array(DEM_M)

fig_height, ax_height = plt.subplots()
fig_diff, ax_diff = plt.subplots()
fig_dem, ax_dem = plt.subplots()
sc_height = ax_height.scatter(LON_DEGE, LAT_DEGN, 3., c=WGS84ELEV_M,       cmap='magma')
sc_diff   = ax_diff.scatter(  LON_DEGE, LAT_DEGN, 3., c=WGS84ELEV_M-DEM_M, cmap='coolwarm', vmin=-100, vmax=+100)
sc_dem    = ax_dem.scatter(   LON_DEGE, LAT_DEGN, 3., c=DEM_M,             cmap='magma')
fig_height.colorbar(sc_height)
fig_diff.colorbar(sc_diff)
fig_dem.colorbar(sc_dem)

if False:
    if zoom_bounds:
        fig_height.savefig('height_zoom.png', bbox_inches='tight')
        fig_diff.savefig('diff_zoom.png', bbox_inches='tight')
        fig_dem.savefig('dem_zoom.png', bbox_inches='tight')
    else:
        fig_height.savefig('height.png', bbox_inches='tight')
        fig_diff.savefig('diff.png', bbox_inches='tight')
        fig_dem.savefig('dem.png', bbox_inches='tight')
