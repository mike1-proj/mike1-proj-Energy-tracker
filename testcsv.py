"""this is a basic code to open a particular raw  E_tracker export .dat file and read only a specific row or number
 or rows which have non-standard pandas data frame formats and extract CT multiplier  data from it
 for use in another module"""
import pandas as pd


# first lets read in the raw.DAT file but limit to the rows that have the data we are after


def checkctmultival():
    raw_dat = pd.read_csv('EB6O0QTV.DAT', delim_whitespace=True, skiprows=1, nrows=1)
    # we use the _whitespace option to try and separate the odd data into columns
    # this gives us two oddly named column headers ('Begin' and 'Norm:3007,#0,0017')
    # then we extract the last two characters in the string contained in the 'Begin' column
    raw_dat['Begin'] = raw_dat.Begin.str[-2:]
    # now to change this string to an integer value
    raw_dat['Begin'] = raw_dat['Begin'].astype(int)
    print(raw_dat .at[0, 'Begin'])
    # df = raw_dat .at[0, 'Begin']


checkctmultival()
