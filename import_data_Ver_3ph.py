"""this is a basic code to open a particular 3 phase
report.DAT format file coming from some software (Deltrax),
so it can be formatted and cleaned of unnecessary data and rearranged using pandas data frame before
using it to generate a clean .csv/Excel file for use elsewhere. The raw .dat file has several proprietary codes
for date and time as well as scaling of certain values which we will have to unpick through manipulation in the DF
before it can be used by something other than the original Deltrax software"""
import datetime
import pandas as pd
from datetime import datetime
pd.set_option("display.max_columns", None)
df = pd.read_csv('E8046ITV.DAT', delimiter=',', skiprows=6)
# we skipped the first six rows in the .DAT file as it contained no useful header information, and we create our own
# header names for the columns based on the original Deltrax Excel export report format look like this:
# Date	Time	I1	I2	I3	KW	KVA	KVAR	PF	AV_VOLTS	In	V1	V2	V3	Hz	Pulse: (these are the final column names in the exported report)
# However the raw .DAT file value sequence is different so we need to set up the sequence in our Data frame column names
# to follow as closley as possible that sequence for simplicity but take account of the extra columns required for internal calculations needed for the final report in Excel.
df.columns = ['date', 'time', 'I1', 'I2', 'I3', 'V1', 'V2', 'V3', 'KW', 'KVA', 'KVAR', 'PF', '', 'col10', 'col11', 'col12',
              'col13', 'col14']
# change format of 'date' column to be a timedate delta value, so we can use it as part of a calc later
df['date'] = pd.to_timedelta(df['date'], unit='D')
# convert the 'time' value into hours and minutes('to_datetime' process produces a full y/m/d/h/s/ms format)
# so we will need to filter that down to hours and minutes to mimic the report format produced by the Deltrax report
df['time'] = (df['time']/10)/60
df['time'] = pd.to_datetime(df['time'], unit='h')
# we use the 'strftime' function to produce something that matches the Deltrax report format
df['time'] = df['time'].dt.strftime('%H-%M')
# now we create a base date to represent the unique base date used by original software to produce a coded day count
# value meant to represent the date of the logged value in the raw exported csv .dat file the logger itself produces.
# The Deltrax software is customised to process the .dat file in a particular proprietary way to account for these
# code encryption's so that they appear as normal dates and times in any Deltrax report.
# We have to use the base value in a calc with the previous timedelta value to arrive at a readable logged date value.
# The 'date' column in the df now mimics how it appears in the Deltrax report for use in our own Excel or other
# process later.
base = datetime(1984, 1, 1)  # this is the base date created line.
df['date'] = df['date'] + base  # this line gives us the correct date for the logged file data

# corrections for scaling column values to reflect odd raw values which  seem to be adjusted in side Deltrax
df['Hz'] = df['Hz']/10
# the next few lines print some check data for us to review. not needed for final  version.
print(base)
print(df)
