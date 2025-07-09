# ###########################################################################
#
# File    : p_plotHDF.py
#
# Author  : Fernando Mendonça (CIMA UAlg)
#
# Created : 2025 04 26
#
# Updated : 2025 05 06
#
# Descrp. : Program to plot a field of a MOHID HDF5 file.
#
# ###########################################################################

from glob import glob
from os import path

import imageio.v3 as iio
import numpy as np
from matplotlib import axes, colors
from matplotlib import pyplot as plt

from m_inputs import init_plotHDF
from m_readhdf import get2Ddata, getgrid, getTime


def main():
    # Inputs:
    #
    inpts = init_plotHDF()

    hdf = inpts.get("hdf")
    outdir = inpts.get("outdir")
    prefix = inpts.get("prefix")

    fld = inpts.get("field")
    layer = inpts.get("layer")
    vectors = inpts.get("vectors")
    vec_zoom = inpts.get("vec_zoom")

    cmap = inpts.get("cmap")
    label = inpts.get("label")
    levels = inpts.get("levels")
    timestr = inpts.get("timestr")

    del inpts

    # Get data from HDF file:
    #
    data = get2Ddata(hdf, "Results/" + fld, layer)
    lat, lon = getgrid(hdf)
    dtout = getTime(hdf)
    
    if vectors:
        vx = get2Ddata(hdf, "Results/velocity U", layer)
        vy = get2Ddata(hdf, "Results/velocity V", layer)

    # Set plots elements:
    #
    lonx, laty = lon[:-1], lat[:-1]
    vmax, vmin = data.max(), data.min()
    bounds = np.linspace(vmin, vmax, levels)
    if vectors: xax, yax = np.meshgrid(lonx, laty)

    # Iterate each time step. One figure is created in each
    # iteration for better RAM management and to enable the
    # plot of different colorbars.
    #
    for pos, inst in enumerate(dtout):
        fout = path.join(outdir, prefix + inst.strftime("%Y%m%dT%H%M.png"))
        print(fout)

        # Create figure and general elements:
        fig, ax = plt.subplots(figsize=(8, 4.5))
        ax: axes.Axes
        ax.set_title(inst.strftime(timestr), weight="bold")
        ax.set_facecolor("silver")
        ax.set_xlabel("Longitude [°E]")
        ax.set_ylabel("Latitude [°N]")

        # Create plot:
        norm = colors.BoundaryNorm(
            boundaries=bounds, ncolors=256, extend="both",
        )
        pcm = ax.pcolormesh(lonx, laty, data[pos], norm=norm, cmap=cmap)

        # NOTE: improve plot with cartopy.

        if vectors:
            ax.quiver(
                xax[::vec_zoom, ::vec_zoom],
                yax[::vec_zoom, ::vec_zoom],
                vx[pos][::vec_zoom, ::vec_zoom],
                vy[pos][::vec_zoom, ::vec_zoom],
                scale=10, width=0.002,
            )
            
        # NOTE: quiver options:
        # 1. Use scipy.ndimage.zoom to interpolate vectors.
        # 2. Create arrows with the same size, just show flow direction.
        # The user can always plot velocity modulus.
        
        # NOTE: Can't overwrite colorbars between opened figures.
        # Make colorbar:
        cbar = fig.colorbar(pcm, ax=ax, label=label)
        cbar.ax.yaxis.set_label_position("left")
        
        # Save figure:
        fig.savefig(fout, dpi=600)
        plt.close(fig)
    
    # Make animation:
    #
    pngs = sorted(glob(path.join(outdir, prefix + "*.png")))
    
    if len(pngs) < 2:
        return
    
    print("Making animation...")
    pngs = np.array([iio.imread(png) for png in pngs])
    fout = path.join(outdir, prefix + "animation.gif")
    iio.imwrite(fout, pngs, fps=1, loop=0)


if __name__ == "__main__":
    main()
