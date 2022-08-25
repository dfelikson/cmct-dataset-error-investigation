import h5py
import numpy as np
from matplotlib import pyplot as plt
from netCDF4 import Dataset
from pathlib import Path


def h5_validate_data(data):
    # Remove the invalid data
    valid = (data['lat'] < 1e8) & (data['lon'] < 1e8)
    data['lat'] = data['lat'][valid]
    data['lon'] = data['lon'][valid]
    data['elev'] = data['elev'][valid]
    data['dem_elv'] = data['dem_elv'][valid]
    data['alt'] = data['alt'][valid]

    return data


def h5_extract_data(file, bbox: tuple):
    f = h5py.File(file, 'r')

    # # Show the contents of the file
    # print(f.keys())
    #
    # # Show the contents of the Data_40HZ group
    # print(f['Data_40HZ'].keys())
    #
    # # Show the contents of the Elevation_Surfaces group
    # print(f['Data_40HZ']['Elevation_Surfaces'].keys())
    #
    # # Show the contents of the Geolocation group
    # print(f['Data_40HZ']['Geolocation'].keys())
    #
    # # Show the contents of the Geophysical group
    # print(f['Data_40HZ']['Geophysical'].keys())

    # TODO: (MAYBE) SAVE (LAT, LON) AS TUPLES INTO 'coords'?

    data = dict()

    # Extract the latitude, longitude, and elevation
    lat = f['Data_40HZ']['Geolocation']['d_lat'][:]
    lon = f['Data_40HZ']['Geolocation']['d_lon'][:]

    # Select the data within a bounding box
    bbox = (lat > bbox[0]) \
           & (lat < bbox[1]) \
           & (lon > bbox[2]) \
           & (lon < bbox[3])

    data['lat'] = lat[bbox]
    data['lon'] = lon[bbox]
    data['elev'] = f['Data_40HZ']['Elevation_Surfaces']['d_elev'][bbox]
    data['dem_elv'] = f['Data_40HZ']['Geophysical']['d_DEM_elv'][bbox]
    # Subtract Geophysical from Elevation_Surfaces; altimeter
    data['alt'] = data['elev'] - data['dem_elv']

    return h5_validate_data(data)


def plot_h5(data, ax):
    """
    Plots the h5 files
    :param files:
    :param bbox: a 4 element tuple of lat/lon constraints where
      (lat_left, lat_right, lon_bot, lon_top)
    :return: None
    """
    # for file in files:
    #     data = h5_extract_data(file, bbox)
    #
    #     # Plot a scatter plot of the elevation data
    #     ax.scatter(data['lon'], data['lat'], 3., c=data['alt'], cmap='coolwarm', vmin=-100, vmax=+100)
    #
    #     ax.title('ICESat Tracks')
    #     ax.xlabel('Longitude')
    #     ax.ylabel('Latitude')
    #
    # plt.colorbar()

    alt = ax.scatter(data['lon'], data['lat'], 3., c=data['alt'], cmap='coolwarm', vmin=-100, vmax=+100)

    ax.set_title('ICESat Tracks')
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')

    return alt


def cmct_extract_data(file, bbox):
    """

    :param file: file name
    :param bbox: a 4 element tuple of lat/lon constraints where
      (lat_left, lat_right, lon_bot, lon_top)
    """

    data = dict()

    ncfile = Dataset(file, 'r')

    if bbox:
        idx = (ncfile['LAT_DEGN'][:] > bbox[0]) & (ncfile['LAT_DEGN'][:] < bbox[1]) & \
              (ncfile['LON_DEGE'][:] > bbox[2]) & (ncfile['LON_DEGE'][:] < bbox[3])
    else:
        idx = np.arange(len(ncfile['LON_DEGE'][:]))

    if np.sum(idx) > 0:
        data['lon'] = ncfile['LON_DEGE'][idx]
        data['lat'] = ncfile['LAT_DEGN'][idx]
        data['elev'] = ncfile['WGS84ELEV_M'][idx]
        data['dem_elv'] = ncfile['DEM_M'][idx]
        data['alt'] = ncfile['WGS84ELEV_M'][idx] - ncfile['DEM_M'][idx]

    return data


def plot_cmct(data: dict, ax):
    alt = ax.scatter(data['lon'], data['lat'], 3., c=data['alt'], cmap='coolwarm', vmin=-100, vmax=+100)

    # sc_diff = ax.scatter(LON_DEGE, LAT_DEGN, 3., c=WGS84ELEV_M - DEM_M, cmap='coolwarm', vmin=-100, vmax=+100)
    # diff_cb = fig_diff.colorbar(sc_diff)

    ax.set_title('CmCt Tracks')
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')

    return alt


def equal_data_ice_cmct(ice_data: dict, cmct_data: dict):
    h5_coords = set(zip(ice_data['lat'], ice_data['lon']))
    ct_coords = set(zip(cmct_data['lat'], cmct_data['lon']))

