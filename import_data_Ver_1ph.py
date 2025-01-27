"""this is a basic code to open a particular 1 phase report.DAT format file coming from some on board software
on an Energy tracker logger via USB export,so it can be formatted and cleaned and rearranged using pandas data frame
before using it to generate a clean .csv file export which replicates  what Deltrax software package would have
done (it is now no longer available) for use elsewhere in Excel or similar reports.
The raw .dat file has several proprietary codes
for date and time as well as scaling of certain values which we will have to unpick through manipulation in the DF
before it can be used by something other than the original Deltrax software
If the report is for 3 phase then, use the other version which has more column outputs"""
# import datetime
import pandas as pd
from datetime import datetime

from numpy import float64

pd.set_option("display.max_columns", None)
# now we read the exported .DAT file transferred from the USB
# (we need to write another piece of code later to locate the file from a designated folder rather than
# this crude way for this demo code)
df = pd.read_csv('E8046ITV.DAT', delimiter=',', skiprows=6)
# we skipped the first six rows in the .DAT file as it contained no useful header information, and we create our own
# header names for the columns (based on the original Deltrax report format)
df.columns = ['date', 'time', 'I1', 'I2', 'I3', 'V1', 'KVA', 'KVAR', 'KW', 'Hz', 'col10', 'col11', 'col12',
              'col13', 'col14']
# change format of 'date' column to be a timedate delta value, so we can use it as part of a calc later
df['date'] = pd.to_timedelta(df['date'], unit='D')
# convert the 'time' value into hours and minutes('to_datetime' process produces a full y/m/d/h/s/ms format)
# so we will need to filter that down to hours and minutes to mimic the report format produced by the Deltrax report
df['time'] = (df['time']/10)/60
df['time'] = pd.to_datetime(df['time'], unit='h')
# we use the 'strftime' function to produce something that matches the Deltrax report format
df['time'] = df['time'].dt.strftime('%H-%M-%S')
# now we create a base date to represent the unique base date used by original software to produce a coded day count
# value meant to represent the date of the logged value in the raw exported csv .dat file the logger itself produces.
# The Deltrax software is customised to process the .dat file in a particular proprietary way to account for these
# code encryption's so that they appear as normal dates and times in any Deltrax report.
# We have to use the base value in a calc with the previous timedelta value to arrive at a readable logged date value.
# The 'date' column in the df now mimics how it appears in the Deltrax report for use in our own Excel or other
# process later.
base = datetime(1984, 1, 1)  # this is the base date created line.
df['date'] = df['date'] + base  # this line gives us the correct date for the logged file data

# corrections for scaling column values to reflect odd raw values which seem to be adjusted in side Deltrax
# first lets make sure the columns we are going to multipoly later are all the same type
df['I1'] = df['I1'].astype('float64')
df['V1'] = df['V1'].astype('float64')
df['KVA'] = df['KVA'].astype(float64)
# Handle NaN values (optional: fill with 0) in case there are some non number values in column
df['V1'] = df['V1'].fillna(0)
df['I1'] = df['I1'].fillna(0)
# okay now to adjust offsets and scales
df['Hz'] = df['Hz']/10
df['I1'] = df['I1']/10
df['KW'] = df['KW']/100
df['V1'] = df['V1']/10
# the next line was needed to fix problems with long floating point values crashing the KVA calculation
# when I tried to do it the first time. This rounds the result value to the number of places set by "round"
# in this case I had to use "-1" as the number of decimal places after the decimal point.
df['KVA'] = df.apply(lambda row: round(row['V1'] * row['I1'], -1), axis=1)
df['KVA'] = df['KVA']/1000
print("this is the base date used in calculation to arrive at  actual logging date")
print(base)
print(df)
# print(df.dtypes)

