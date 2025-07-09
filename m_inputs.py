# ###########################################################################
#
# File    : m_inputs.py
#
# Author  : Fernando Mendonça (CIMA UAlg)
#
# Created : 2025 04 26
#
# Updated : 2025 04 30
#
# Descrp. : Module with initialization functions.
#
# ###########################################################################

from json import load
from os import path


def init_file(grp: str) -> dict:
    """Check initialization file 'init_HDFView.json'.
    
    Keyword argument:
    - grp: name of the group inside the initialization file.
    """

    fipt = "init_HDFView.json"
    
    if not path.isfile(fipt):
        print("[ERROR] m_inputs.init_file: FileNotFoundError")
        print(f"\tMissing input file '{fipt}' .")
        raise SystemExit
    
    # Read file:
    with open(fipt, "rb") as dat:
        inpts = load(dat)

    if isinstance(inpts, dict): inpts = inpts.get(grp)

    if not inpts or not isinstance(inpts, dict):
        print("[ERROR] m_inputs.init_file: FileNotFoundError")
        print(f"\tInputs not found for the group '{grp}' .")
        raise SystemExit
    
    return inpts


def init_plotTS() -> str:
    """Reads and checks the inputs from the file 'init_HDFView.json'
    for plotting MOHID time series files.
    """

    # Check input file:
    inpts = init_file("TS")

    # Check inputs:
    key = "tsfile"
    val = inpts.get(key)

    if not isinstance(val, str) or not path.isfile(val):
        print("[ERROR] m_inputs.init_plotTS: FileNotFoundError")
        print(f"\tTime series file not found: '{val}' .")
        raise SystemExit
    
    return val
    

def init_plotHDF() -> dict:
    """Reads and checks the inputs from the file 'init_HDFView.json'
    for plotting MOHID HDF5 fields.
    """

    # Check input file:
    inpts = init_file("HDF")

    # Check inputs:
    key = "hdf"
    val = inpts.get(key)

    if not isinstance(val, str) or not path.isfile(val):
        print("[ERROR] m_inputs.init_plotHDF: FileNotFoundError")
        print(f"\tHDF5 file not found: '{val}' .")
        raise SystemExit
    
    key = "outdir"
    val = inpts.get(key)

    if not isinstance(val, str) or not path.isdir(val):
        print("[ERROR] m_inputs.init_plotHDF: FileNotFoundError")
        print(f"\tOutput directory not found: '{val}'.")
        raise SystemExit
    
    key = "prefix"
    val = inpts.get(key)

    if not isinstance(val, str):
        print("[ERROR] m_inputs.init_plotHDF: TypeError")
        print(f"\t'{key}' should contain a string.")
        raise SystemExit
      
    key = "field"
    val = inpts.get(key)

    if not isinstance(val, str) or val == "":
        print("[ERROR] m_inputs.init_plotHDF: ValueError")
        print(f"\t'{key}' should contain the name of a MOHID HDF5 field.")
        raise SystemExit
    
    key = "layer"
    val = inpts.get(key)

    if not isinstance(val, int):
        print("[ERROR] m_inputs.init_plotHDF: TypeError")
        print(f"\t'{key}' should contain an integer >= 0.")
        raise SystemExit
    
    key = "vectors"
    val = inpts.get(key)

    if not isinstance(val, bool):
        print("[ERROR] m_inputs.init_plotHDF: TypeError")
        print(f"\t'{key}' is boolean variable.")
        raise SystemExit
    
    key = "vec_zoom"
    val = inpts.get(key)

    if not isinstance(val, int):
        print("[ERROR] m_inputs.init_plotHDF: TypeError")
        print(f"\t'{key}' should contain an integer >= 1.")
        raise SystemExit
    
    key = "cmap"
    val = inpts.get(key)

    if not isinstance(val, str):
        print("[ERROR] m_inputs.init_plotHDF: TypeError")
        print(f"\t'{key}' should contain a string.")
        raise SystemExit
    
    key = "label"
    val = inpts.get(key)

    if not isinstance(val, str):
        print("[ERROR] m_inputs.init_plotHDF: TypeError")
        print(f"\t'{key}' should contain a string.")
        raise SystemExit
    
    key = "levels"
    val = inpts.get(key)

    if not isinstance(val, int):
        print("[ERROR] m_inputs.init_plotHDF: TypeError")
        print(f"\t'{key}' should contain an integer >= 1.")
        raise SystemExit
    
    key = "timestr"
    val = inpts.get(key)

    if not isinstance(val, str):
        print("[ERROR] m_inputs.init_plotHDF: TypeError")
        print(f"\t'{key}' should contain a time string format.")
        raise SystemExit
    return inpts


def init_plotLAGR() -> dict:
    """Reads and checks the inputs from the file 'init_HDFView.json'
    for plotting lagrangian particles.
    """

    # Check input file:
    inpts = init_file("LAGR")

    # Check inputs:
    key = "hdf"
    val = inpts.get(key)

    if not isinstance(val, str) or not path.isfile(val):
        print("[ERROR] m_inputs.init_plotLAGR: FileNotFoundError")
        print(f"\tHDF5 file not found: '{val}' .")
        raise SystemExit
    
    key = "outdir"
    val = inpts.get(key)

    if not isinstance(val, str) or not path.isdir(val):
        print("[ERROR] m_inputs.init_plotLAGR: FileNotFoundError")
        print(f"\tOutput directory not found: '{val}'.")
        raise SystemExit
    
    key = "origin_name"
    val = inpts.get(key)

    if not isinstance(val, str):
        print("[ERROR] m_inputs.init_plotLAGR: TypeError")
        print(f"\t'{key}' should contain a string.")
        raise SystemExit
      
    key = "propertie_name"
    val = inpts.get(key)

    if not isinstance(val, str) or val == "":
        print("[ERROR] m_inputs.init_plotLAGR: ValueError")
        print(f"\t'{key}' is not a name of a Lagrangian field.")
        raise SystemExit
    
    
    key = "cmap"
    val = inpts.get(key)

    if not isinstance(val, str):
        print("[ERROR] m_inputs.init_plotLAGR: TypeError")
        print(f"\t'{key}' should contain a string.")
        raise SystemExit
    
    key = "label"
    val = inpts.get(key)

    if not isinstance(val, str):
        print("[ERROR] m_inputs.init_plotLAGR: TypeError")
        print(f"\t'{key}' should contain a string.")
        raise SystemExit
    
    key = "levels"
    val = inpts.get(key)

    if not isinstance(val, int):
        print("[ERROR] m_inputs.init_plotLAGR: TypeError")
        print(f"\t'{key}' should contain an integer >= 1.")
        raise SystemExit
    
    key = "vmax"
    val = inpts.get(key)

    if not isinstance(val, (int,float)):
        print("[ERROR] m_inputs.init_plotLAGR: TypeError")
        print(f"\t'{key}' is not a number.")
        raise SystemExit
    
    key = "vmin"
    val = inpts.get(key)

    if not isinstance(val, (int,float)):
        print("[ERROR] m_inputs.init_plotLAGR: TypeError")
        print(f"\t'{key}' is not a number.")
        raise SystemExit
    
    key = "timestr"
    val = inpts.get(key)

    if not isinstance(val, str):
        print("[ERROR] m_inputs.init_plotLAGR: TypeError")
        print(f"\t'{key}' should contain a time string format.")
        raise SystemExit
    return inpts
