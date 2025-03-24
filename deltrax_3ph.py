""" Code by Michael McNerney.
this is a code to open a particular 3 phase report.DAT format file coming from an E-Tracker data logger.
the data was processed by obsolete software (Deltrax) no longer available.
I have reverse engineered old Deltrax report output so it can be handled by this code which has formatted and cleaned
of unnecessary data the raw.DAT file from the logger and rearranged it using pandas data frame before
using it to generate a clean Excel file for use elsewhere. The raw .dat file has several proprietary codes
for date and time as well as scaling of certain values which we will had to unpick through manipulation in the DF
before it could be used by this software to deliver a meme result as the original Deltrax software"""
import tkinter as tk
from tkinter import filedialog
import pandas as pd
from datetime import datetime
from tkinter import messagebox as mb
import math
import numpy as np


# now set up the file path variable to be used by the process later.
# we create the file location dialog graphic function to ask for the user to provide a location to find the .DAT file.
# we store the result in a variable called "selected_file" for use later.


def get_file_path():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    file_path = filedialog.askopenfilename(title="Select a .DAT File from your USB", filetypes=[("CSV Files", "*.DAT")])
    return file_path


selected_file = get_file_path()  # call function and store the result in a variable


# now to create a number of GUI functions to save processed file in Excel format in the users chosen location and
# provide some feed back to the user via a tkinter message box (depending on how the process goes).

def callback():
    mb.showinfo('Success', 'File has been saved to your location')


def error_msg():
    mb.showinfo('Error', 'File has not been saved')


def save_file(df):
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    file_path = filedialog.asksaveasfilename(
        title="Save file as xlsx Excel File",
        defaultextension=".xlsx",  # Ensures the file has a .xlsx extension
        filetypes=[("XLSX", "*.xlsx"), ("All Files", "*.*")]
    )

    if file_path:  # Check if the user selected a file
        try:
            df.to_excel(file_path, index=False)  # Save without the index column
            callback()  # deliver process success message
        except FileNotFoundError:
            error_msg()  # deliver process failure message
    else:
        print("Save operation canceled.")


# now we are ready to process the .DAT file located at the file path variable created earlier by "get_file_path"

# this first section deals with extracting a CT multiplier value from the top lines of raw.DAT file on the USB file
# for use later in amps calculations results.


raw_dat = pd.read_csv(selected_file, delim_whitespace=True, skiprows=1, nrows=1)

# we use the _whitespace option to try and separate the odd data into columns
# this gives us two oddly named column headers ('Begin' and 'Norm:3007,#0,0017')
# then we extract the last two characters in the string contained in the 'Begin' column
raw_dat['Begin'] = raw_dat.Begin.str[-2:]
# now to change this string to an integer value
raw_dat['Begin'] = raw_dat['Begin'].astype(int)
factor = (raw_dat.at[0, 'Begin'])
# now we have the VI factor value extracted and stored in the variable 'factor', we can move on to main work
# which involves reading the .DAT file again to process the main data rows in the file into a pandas data frame.

pd.set_option("display.max_columns", None)
# now we read the exported .DAT file transferred from the USB
# (we need to write another piece of code later to locate the file from a designated folder rather than
# this crude way for this demo code)
df = pd.read_csv(selected_file, delimiter=',', skiprows=6, dtype='object')
# we skip the first six rows in the .DAT file as it contained no useful information for the data frame,
# and we create a data frame.

# However the raw .DAT file column value sequence is different, so we need to change the sequence
# in our new Data frame column names to follow as closely as possible the .DAT sequence for simplicity
# but take account of the extra columns required for internal calculations needed for the final report in Excel.
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

df['Hz'] = df['Hz'] / 10
df['I1'] = df['I1'] / factor  # this is the ct factor result we derived from the first csv read section
df['I2'] = df['I2'] / factor
df['I3'] = df['I3'] / factor
df['KW'] = df['KW'] / 100  # KW is reported by the tracker
df['V1'] = df['V1'] / 10
df['V2'] = df['V2'] / 10
df['V3'] = df['V3'] / 10
df['In'] = df['In'] / factor
# these next lines prepare the calcs needed and the creation of an extra column for avg 3 phase volts value.
df['AV_VOLTS'] = df[['V1', 'V2', 'V3']].sum(axis=1)
df['AV_VOLTS'] = df['AV_VOLTS'] / 3
df['AV_VOLTS'] = df['AV_VOLTS'] * math.sqrt(3)
# now lets round up the values for this new column
df['AV_VOLTS'] = df.apply(lambda row: round(row['AV_VOLTS'], 2), axis=1)

# Now we have to do an internal calculation sequence to get a "KVA" value to mimic what appears in the Deltrax report
step1 = df['V1'] * df['I1']
step2 = df['V2'] * df['I2']
step3 = df['V3'] * df['I3']
step4 = (step1 + step2 + step3) / 1000
df['KVA'] = step4
# now lets round up the values for this new column
df['KVA'] = df.apply(lambda row: round(row['KVA'], 2), axis=1)

# Now lets deal with producing the power factor value column that mimics what the Deltrax report produces.
# the raw.DAT does not provide this. Deltrax report derives it by a calculation.
df['PF'] = (100 - (df['KW'] / df['KVA'])) / 100
df['PF'] = df.apply(lambda row: round(row['PF'], 2), axis=1)

# Now lets deal with producing the KVAR value column that mimics what the Deltrax report produces.
# the raw.DAT does not provide this value. Deltrax report appears to derive it by a calculation.
# the calculation involves subtracting the squares of KVA and KW and getting the square root of the result
step5 = df['KVA'] ** 2
step6 = df['KW'] ** 2
step7 = (step5 - step6)
df['KVAR'] = step7
# this calc can produce negative values which numpy square root may throw a non-fatal error. So, to resolve this
# we introduce a mask and substitute process on the next line to make sure any negatives end up as zero
# so numpy does not throw and error message.
df['KVAR'] = df['KVAR'].mask(df['KVAR'] < 0).fillna(0)
df['KVAR'] = np.sqrt(df['KVAR'])
df['KVAR'] = df.apply(lambda row: round(row['KVAR'], 4), axis=1)
# This now gives us a completed data frame configured in a way that we can export to an Excel file

# now we can finally move on to saving an Excel version of the created DF to the users chosen location
# using the "save_file" function created earlier.
save_file(df)
