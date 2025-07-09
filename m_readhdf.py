# ###########################################################################
#
# File    : m_readhdf.py
#
# Author  : Fernando Mendonça - fmmendonca@ualg.pt (CIMA UAlg)
#
# Created : 2025 04 25
#
# Descrp. : Module with functions to extract data from MOHID HDF5 files.
#
# ###########################################################################

from datetime import datetime
from typing import Tuple

import numpy as np
from h5py import File


def getTime(hdfin: str) -> Tuple[datetime]:
    """Extracs the time array from a MOHID HDF5 file.
    Returns a tuple with datetime objects.

    Keyword argument:
    - hdfin: name and path of the MOHID HDF5 file.
    """

    # MOHID HDF5 files store the time dimension in array like the following:
    # time = [
    #     [2025., 4., 25., 12., 0., 0.],
    #     [2025., 4., 25., 13., 0., 0.],
    # ]
    # All the values in one step time are floats, so the extraction is done
    # by converting them to 16 bit integers.

    hdf = File(hdfin, "r")
    grp = hdf["Time"]
    data = [grp[key][...].astype("i2") for key in grp.keys()]
    data = tuple([datetime(*tuple(val)) for val in data])
    hdf.close()
    return data


def getgrid(hdfin: str) -> Tuple[np.ndarray, np.ndarray]:
    """Extracts the 2D grid data from a MOHID HDF5 file. Returns
    one array for the latitudes and another for longitudes.
    
    Keyword arguments:
    - hdfin: name and path of the MOHID HDF5 file.
    """
    
    # MOHID HDF5 files store the boundary values for the cells in the grid.
    # So, the shape of latitude array (lat) and the longitude one (lon) is
    # always bigger than of of a field (depth, lon-1, lat-1).
    # Also, the arrays are stored as meshgrids (check numpy.meshgrid).
    # Thats why for the latitude only the first column is extracted and,
    # for the longitude, only the first row.

    hdf = File(hdfin, "r")
    lat = hdf["/Grid/Latitude"][...][0]
    lon = np.transpose(hdf["/Grid/Longitude"][...])[0]
    hdf.close()

    return lat, lon


def getbatim(hdfin: str) -> np.ma.MaskedArray:
    """Extracts the bathymetry field of a MOHID HDF5 file.
    
    Keyword arguments:
    - hdfin: name and path of the MOHID HDF5 file.
    """

    hdf = File(hdfin, "r")
    data = hdf["Grid/Bathymetry"][...].astype("f8")
    # Transpose to (lat, lon)
    data = np.ma.masked_less(np.transpose(data), -98)
    hdf.close()
    return data


def get2Ddata(hdfin: str, fldgrp: str, layerid: int) -> np.ma.MaskedArray:
    """Extracts all the time steps from a single field at a specific
    layer, of a MOHID HDF5 file, into a masked array. Returns a
    masked array with shape (time, latitude, longitude).

    Keyword arguments:
    - hdfin: name and path of the MOHID HDF5 file;
    - fldgrp: path of the HDF5 group to be extracted
        (e.g.: '/Results/temperature');
    - layerid: vertical layer index. The first value is zero and at the
        surface. If the extracted field is 2D this input is ignored.
    """
    
    # Open HDF5 and check the field group:
    #
    hdf = File(hdfin, "r")

    if fldgrp not in hdf:
        hdf.close()
        print("[ERROR] m_readhdf.getdata: KeyError")
        print(f"\t'{fldgrp}' is not a group inside the file '{hdfin}'")
        raise SystemExit
    
    # Create data container and extract each time step:
    #
    hdfgrp = hdf[fldgrp]
    data = []

    for key in hdfgrp.keys():
        data.append(hdfgrp[key][...])

    data = np.array(data)

    # The last line adds one dimention to the array. So, 3D fields
    # should have the shape (time, depth, longitude, latitude),
    # and 2D fields (time, longitude, latitude).

    # Check depth dimention:
    #
    if data.ndim > 3 and not (0 <= layerid < data.shape[1]):
        hdf.close()
        print("[ERROR] m_readhdf.getdata: IndexError\n\tThe vertical", end=" ")
        print(f"dimension of the file '{hdfin}' contains only", end=" ") 
        print(f"{data.shape[1]} layer(s)")
        raise SystemExit
    
    if data.ndim > 3: 
        # MOHID HDF5 files are saved from bottom to surface.
        # So, revert to surface to bottom:
        data = data[:, ::-1]
        # Select layer:
        data = data[:, layerid]

    # Extract land/sea mask (in MOHID HDFs 1=water,0=land).
    # Then water=false, land=True:
    #
    hdfgrp = hdf["Grid/OpenPoints"]
    mask = []

    for key in hdfgrp.keys():
        mask.append(hdfgrp[key][...])

    # Convert to integer 16 bits (2 bytes) to make
    # sure the array contains only zeros and ones:
    mask = np.array(mask).astype("i2")
    mask = np.ma.masked_less(mask, 1).mask
    
    if mask.ndim > 3:
        mask = mask[:, ::-1]
        mask = mask[:, layerid]
    
    data = np.ma.masked_array(data, mask=mask)
    del mask
    hdf.close()

    # Transpose from (longitude, latitude) to (latitude, longitude):
    return np.transpose(data, (0,2,1))
