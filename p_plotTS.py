# ###########################################################################
#
# File    : p_plotTS.py
#
# Author  : Fernando Mendonça (CIMA UAlg)
#
# Created : 2025 04 27
#
# Descrp. : Program to plot data from a MOHID time series file.
#
# ###########################################################################

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import axes

from m_inputs import init_plotTS


def main():
    # Inputs:
    #
    tsfile = init_plotTS()
    
    # Read header:
    #
    dat = open(tsfile, "r")
    columns = ""
    readstop = False
    linepos = 0

    while readstop == False:
        line = dat.readline()
        linepos += 1

        if "YY  MM  DD  hh  mm" in line:
            columns = line
        elif "<BeginTimeSerie>" in line:
            readstop = True

    if not columns:
        dat.close()
        print("[ERROR] main: RuntimeError")
        print("\tFields row not found in TS file.")
        raise SystemExit
    
    # Create data frame and read data:
    #
    print("Reading time series...")
    df = pd.DataFrame([], columns=columns.split())
    readstop = False

    while readstop == False:
        line = dat.readline()
        linepos += 1

        if "<EndTimeSerie>" in line:
            readstop = True
            continue

        values = line.split()
        
        # Check line:
        if len(values) != len(df.columns):
            dat.close()
            print("[ERROR] main: RuntimeError")
            print(f"\tError in line {linepos} of the time series file.")
            raise SystemExit
        
        df.loc[len(df)] = values
    
    dat.close

    # Filter dataframe:
    #
    df = df.drop(["Seconds"], axis=1)
    
    if "OpenPoint" in df.columns:
        df = df.drop(["OpenPoint"], axis=1)

    # Create datetime series:
    df = df.rename(columns={
        "YY": "year", "MM": "month", "DD": "day",
        "hh": "hours", "mm": "minutes", "ss": "seconds",
    })

    dtseries = pd.to_datetime(df.loc[:, "year": "seconds"])

    df = df.drop([
        "year", "month", "day", "hours", "minutes", "seconds"
    ], axis=1)

    # Convert to floats:
    df = df.astype("f8")
    columns = df.columns.to_list()

    # Plot data frame:
    #
    readstop = False

    while readstop == False:
        print("Which field would you like to plot?")
        for pos, val in enumerate(columns): print(f"  {pos+1} -", val)
        print("  Any other key to EXIT")
        userop = input()

        # Check input:
        options = [str(val+1) for val in range(pos+1)]

        if userop not in options:
            readstop = True
            continue

        # Plot field:
        fig, ax = plt.subplots()
        ax: axes.Axes
        ax.plot(dtseries, df[columns[int(userop)-1]], "b", lw=3)
        ax.grid(True, "both", "both")
        plt.show()
        plt.close(fig)


if __name__ == "__main__":
    main()
