"""this is a basic code to open a particular 3 phase
report.DAT format file coming from some software (Deltrax),
so it can be formatted and cleaned of unnecessary data and rearranged using pandas data frame before
using it to generate a clean .csv/Excel file for use elsewhere. The raw .dat file has several proprietary codes
for date and time as well as scaling of certain values which we will have to unpick through manipulation in the DF
before it can be used by something other than the original Deltrax software"""
import datetime
import pandas as pd
from datetime import datetime
from numpy import float64
import math

# this first section deals with extracting a CT multiplier value from the top lines of raw.DAT file for use later
raw_dat = pd.read_csv('EAAP6ATV.DAT', delim_whitespace=True, skiprows=1, nrows=1)
# we use the _whitespace option to try and separate the odd data into columns
# this gives us two oddly named column headers ('Begin' and 'Norm:3007,#0,0017')
# then we extract the last two characters in the string contained in the 'Begin' column
raw_dat['Begin'] = raw_dat.Begin.str[-2:]
# now to change this string to an integer value
raw_dat['Begin'] = raw_dat['Begin'].astype(int)
result = (raw_dat .at[0, 'Begin'])
# now we have the multiplier value extracted and stored in the variable 'result', we can move on to main work.

pd.set_option("display.max_columns", None)
# now we read the exported .DAT file transferred from the USB
# (we need to write another piece of code later to locate the file from a designated folder rather than
# this crude way for this demo code)
df = pd.read_csv('EAAP6ATV.DAT', delimiter=',', skiprows=6, dtype='object')
# we skipped the first six rows in the .DAT file as it contained no useful header information, and we create our own

# However the raw .DAT file value sequence is different so we need to change the sequence in our Data frame column names
# to follow as closely as possible that .DAT sequence for simplicity but take account of the extra columns required for
# internal calculations needed for the final report in Excel.
# next  we need to ensure there are no invalid rows in the .DAT file, and we use the PANDAS df.dropna process to
# remove any rows with spurious data which can happen when an inexperienced operator downloads the file to USB
df.dropna(inplace=True)
# this cleans out any spurious data in the CSV that might end up in the data frame
# now we can  set up the data frame column names to match  as closely as possible the raw .DAT data sequence
df.columns = ['date', 'time', 'I1', 'I2', 'I3', 'V1', 'V2', 'V3', 'KW', 'Hz', 'col10', 'In', 'PF',
              'AV_VOLTS', 'Pulse']
df['date'] = df['date'].astype('int64')
df['time'] = df['time'].astype('int64')
df['Hz'] = df['Hz'].astype('float64')
df['KW'] = df['KW'].astype('float64')
df['V1'] = df['V1'].astype('float64')
df['V2'] = df['V2'].astype('float64')
df['V3'] = df['V3'].astype('float64')
df['I1'] = df['I1'].astype('float64')
df['I2'] = df['I2'].astype('float64')
df['I3'] = df['I3'].astype('float64')
df['PF'] = df['PF'].astype('float64')
df['In'] = df['In'].astype('float64')
print(df)
print(df.dtypes)
# change format of 'date' column to be a timedate delta value, so we can use it as part of a calc later
df['date'] = pd.to_timedelta(df['date'], unit='D')
# convert the 'time' value into hours and minutes('to_datetime' process produces a full y/m/d/h/s/ms format)
# so we will need to filter that down to hours and minutes to mimic the report format produced by the Deltrax report
df['time'] = (df['time'] / 10) / 60
df['time'] = pd.to_datetime(df['time'], unit='h')
# we use the 'strftime' function to produce something that matches the original Deltrax report time format
df['time'] = df['time'].dt.strftime('%H-%M')
# now we create a base date to represent the unique base date used by original software to produce a timedelta day count
# value of the days elapsed since that base date and list this in the first data slot of each row as a number
# in the raw exported csv.dat file
# The Deltrax software is customised to process the .dat file in a particular proprietary way to account for these
# code encryption's so that they appear as normal dates and times in any Deltrax report.
# We have to use the base value in a calc with the previous timedelta value to arrive at a readable logged date value.
# The 'date' column value in the df now mimics how it appears in the Deltrax report for use in our own Excel or other
# export process later.
base = datetime(1984, 1, 1)  # this is the base date created line.
df['date'] = df['date'] + base  # this line gives us the correct date for the logged file data
# now we change the result of this calc from year/month/date format to date/month/year format with:
df['date'] = df['date'].dt.strftime('%d/%m/%Y')
# now we apply corrections for scaling column values to reflect odd raw values which seem to be adjusted in side Deltrax
# first lets make sure the columns we are going to multipoly later are all the same type
# df['KVA'] = df['KVA'].astype('float64') we have not defined this yet as it is a  derived calculation
# Handle NaN values (optional: fill with 0) in case there are some non number values in column
df['V1'] = df['V1'].fillna(0)
df['I1'] = df['I1'].fillna(0)
# okay now to adjust offsets and scales for all the columns and phases
multiplier = result  # this is the result we derived from the first section

df['Hz'] = df['Hz'] / 10
df['I1'] = df['I1'] / multiplier
df['I2'] = df['I2'] / multiplier
df['I3'] = df['I3'] / multiplier
df['KW'] = df['KW'] / 10
df['KW'] = df['KW'] / multiplier
df['V1'] = df['V1'] / 10
df['V2'] = df['V2'] / 10
df['V3'] = df['V3'] / 10
df['In'] = df['In'] / 10
# these next lines prepare the calcs needed and the creation of an extra column
df['AV_VOLTS'] = df[['V1', 'V2', 'V3']].sum(axis=1)
df['AV_VOLTS'] = df['AV_VOLTS']/3
df['AV_VOLTS'] = df['AV_VOLTS']*math.sqrt(3)
# now lets round up the values for this new column
df['AV_VOLTS'] = df.apply(lambda row: round(row['AV_VOLTS'], 2), axis=1)
df['PF'] = df.apply(lambda row: round(row['PF'], 9), axis=1)
# the next line was needed to fix problems with long floating point values crashing the KVA calculation
# when I tried to do it the first time. This rounds the result value to the number of places set by "round"
# in this case I had to use "-1" as the number of decimal places after the decimal point.
df['KVA'] = df.apply(lambda row: round(row['V1'] * row['I1'], -1), axis=1)
df['KVA'] = df['KVA'] / 1000
print("this is the base date used in calculation to arrive at  actual logging date")
print(base)
print(df)
print(df.dtypes)
