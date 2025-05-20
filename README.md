# mohid-HDFView
Isto foi editado no VSCode  
A set of Python scripts to plot MOHID outputs in order to avoid using Bentley OpenFlows FLOOD (MOHID Studio replacement).

Author       : Fernando Mendonça  
Organization : CIMA UAlg  
Contact      : hidrotec@ualg.pt

---

This is a package containing three programs:  
1. p_plotHDF.py: plots fields from a MOHID HDF5 file.  
2. p_plotTS.py: plots charts from a MOHID time series file.  
3. p_plotLAGR.py: plots the lagrangian particles of a MOHID HDF5 file.

## Requirements
The programs require the following external Python modules:
    ○ h5py
    ○ imageio
    ○ matplotlib
    ○ numpy
    ○ pandas

If the user does not have a conda environment with the previous modules,
they can be installed individually, or a new environment can be created.

Run the following commands in the conda shell to create a new environment
called "mohid", with all the requirements, from the file mohidenv.yml:
>>> conda update conda
>>> conda env create --file mohidenv.yml

To run one of the programs, activate the environment and run:
>>> python .\p_plotHDF.py

****************************************************************************
p_plotHDF.py

Change the inputs of the group 'HDF' in the file
'init_HDFView.json' to configure a new plot.

List of inputs:
    ○ hdf: name and path to the MOHID HDF5 file to be plotted.
    ○ outdir: path to the output directory where the figures will be saved.
    ○ prefix: prefix to be added to the name of each figure.
    
    ○ field: name of the variable/field inside the HDF5. Common fields in a
        Hydrodynamic.hdf5 file:
            - velocity U
            - velocity V
            - velocity W
            - velocity modulus
            - water level

        Common fields in a WatyerProperties.hdf5 file:
            - density
            - salinity
            - temperature
    ○ layer: layer index where to extract the field. 0 for surface,
        1 for the next layer and so on...
    ○ vectors: switch to plot velocity vectors.
    ○ vec_zoom: controls the density of vectors on the plot.
        1 for the original amount of vectors. The higher the
        number, the lower the density.

    ○ cmap: colorbar name (https://matplotlib.org/stable/users/explain/colors/colormaps.html):
        - RdYlBu: good for temperature
        - Spectral: good for temperature
        - jet: good for temperature
        - plasma : good for salinity
        - RdBu : good for water level
        - Blues: good for velocity
        - Greys: good for velocity
        
        Some colorbars can be reversed by adding
        "_r" to the end of their name.
    ○ label: field label.
    ○ levels: amount of colors in the colorbar.
    ○ timestr: time string format used to write the date and time of
        each field. See
        https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior

****************************************************************************
p_plotTS.py

Change the inputs of the group 'TS' in the file
'init_HDFView.json' to configure a new plot.

List of inputs:
    ○ tsfile: name and path to the MOHID time series file to be plotted.

****************************************************************************
p_plotLAGR.py

Change the inputs of the group 'LAGR' in the file
'init_HDFView.json' to configure a new plot.

List of inputs:
    ○ hdf: name and path to the MOHID HDF5 Lagrangian file to be plotted.
    ○ outdir: path to the output directory where the figures will be saved.
    
    ○ origin_name: value of the keyword 'ORIGIN_NAME', of the block
        '<BeginOrigin> ... <EndOrigin>', in the Lagrangian.dat file.
    ○ propertie_name: value of the keyword 'NAME', of the block
        '<<BeginProperty>> ... <<EndProperty>>', in the Lagrangian.dat file.

    ○ cmap: colorbar name. 'jet' works great here.
    ○ label: field label.
    ○ levels: amount of colors in the colorbar.
    ○ vmax, vmin: maximum and minimum color scale values.
    ○ timestr: time string format used to write
        the date and time of each field.

![cima-logo](https://cima-somathredds.ualg.pt/thredds/fileServer/info/cima-logo.png)
