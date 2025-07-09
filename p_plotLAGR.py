# ###########################################################################
#
# File    : p_plotLAGR.py
#
# Author  : Diogo Moreira (CIMA UAlg)
#
# Created : 2025 04 29
#
# Updated : 2025 05 06 - Fernando Mendonça (CIMA UAlg)
#
# Descrp. : Program to plot a Lagrangian field of a MOHID HDF5 file.
#
# NOTE    : 3D lagrangian still need to be tested!
#
# ###########################################################################

from glob import glob
from os import path

import imageio.v3 as iio
import matplotlib.pyplot as plt
import numpy as np
from h5py import File
from matplotlib import axes, colors

from m_inputs import init_plotLAGR
from m_readhdf import getbatim, getgrid, getTime


def main():
    # Inputs:
    #
    inpts = init_plotLAGR()
    
    hdfin = inpts.get("hdf")
    outdir = inpts.get("outdir")
    origin_name = inpts.get("origin_name")
    propertie_name = inpts.get("propertie_name")

    cmap = inpts.get("cmap")
    label =  inpts.get("label")
    levels = inpts.get("levels")
    vmax, vmin = inpts.get("vmax"), inpts.get("vmin")
    timestr = inpts.get("timestr")

    del inpts

    # Check lagrangian inputs:
    # 
    hdf = File(hdfin, "r")
    hdfgrp = "/Results/" + origin_name

    if not hdfgrp in hdf:
        hdf.close()
        print("[ERROR] main: KeyError")
        print(f"\t'{hdfgrp}' not found in '{hdfin}' .")
        raise SystemExit
    
    grpfld = hdfgrp + "/" + propertie_name

    if not grpfld in hdf:
        hdf.close()
        print("[ERROR] main: KeyError")
        print(f"\t'{grpfld}' not found in '{hdfin}' .")
        raise SystemExit
    
    # Just to be safe:
    hdf.close()

    # Get grid, time and bathymetry from the HDF:
    #
    dtout = getTime(hdfin)
    lat, lon = getgrid(hdfin)
    batim = getbatim(hdfin)

    # Remove last column and last row boundary:
    lon, lat = lon[:-1], lat[:-1]

    # Make all water cells as 1 and land cells 0:
    batim = (batim/batim).astype("i2")
    
    # Iterate time steps:
    #
    bounds = np.linspace(vmin, vmax, levels)
    hdf = File(hdfin, "r")

    for pos, inst in enumerate(dtout):
        # Output file:
        fout = path.join(outdir, origin_name)
        fout+= inst.strftime("-%Y%m%dT%H%M.png")
        print(fout)

        # Read lagrangian data (latitude, longitude, concentration):
        grp = hdf[hdfgrp + "/Latitude"]
        key = [key for key in grp.keys()][pos]
        lglat = grp[key][...].astype("f8")

        grp = hdf[hdfgrp + "/Longitude"]
        key = [key for key in grp.keys()][pos]
        lglon = grp[key][...].astype("f8")

        grp = hdf[grpfld]
        key = [key for key in grp.keys()][pos]
        lgdata = grp[key][...].astype("f8")

        # Remove particles with insignificant concentration:
        mask = lgdata >= vmin
        lglon, lglat, lgdata = lglon[mask], lglat[mask], lgdata[mask]
        
        # Create time step figure:
        fig, ax = plt.subplots()
        ax: axes.Axes
        ax.set_title(inst.strftime(timestr), weight="bold")
        ax.set_facecolor("silver")
        ax.set_xlabel("Longitude [°E]")
        ax.set_ylabel("Latitude [°N]")

        # Colorbar normalization:
        norm = colors.BoundaryNorm(
            boundaries=bounds, ncolors=256, extend="neither",
        )

        # Add bathymetry and make plot:
        ax.pcolormesh(lon, lat, batim, cmap="Greys")
        sct = ax.scatter(lglon, lglat, c=lgdata, cmap=cmap, s=10, norm=norm)

        cbar = fig.colorbar(sct, ax=ax, label=label)
        cbar.ax.yaxis.set_label_position("left")

        # Save figure:
        fig.savefig(fout, dpi=600)
        plt.close(fig)
    
    hdf.close()

    # Make animation:
    #
    pngs = sorted(glob(path.join(outdir, origin_name + "*.png")))

    if len(pngs) < 2:
        return
    
    print("Making animation...")
    pngs = np.array([iio.imread(png) for png in pngs])
    fout = path.join(outdir, origin_name + "-animation.gif")
    iio.imwrite(fout, pngs, fps=1, loop=0)


if __name__ == "__main__":
    main()
