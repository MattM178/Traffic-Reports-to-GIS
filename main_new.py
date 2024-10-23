# This is a working script to update this code to use xlsx files directly instead of scraping PDFs

import pandas as pd
from datetime import datetime
from arcgis
from pathlib import Path

filename = './dev/3061 Livingston Radar-Vehicles1.xlsx'

# Read the xlsx into a dataframe
df = pd.read_excel(filename)

# First let's extract the metadata
# Pull out the study name, lat, long and transpose
info_df = df.iloc[:2, :2].transpose()

# Set new headers from the first row
info_df.columns = info_df.iloc[0].str.strip()

# Drop header row
info_df = info_df.drop(info_df.index[0])

# troubleshooting line
# print(info_df)

# Extract values
name = info_df.index[0]
latitude = float(info_df['Latitude:'].iloc[0])
longitude = float(info_df['Longitude:'].iloc[0])

# troubleshooting line
# print(name, latitude, longitude)

# Ok, now let's extract the actual study data
df2 = pd.read_excel(filename, header=4)  # this pulls out just the vehicle and speed data

# troubleshooting line
# print(df2)

# Create a new dataframe to interpolate the data. temporary for now, need to add back in UID, year
columns = ['name', 'start_date', 'end_date', 'lat', 'lon', 'spdperc_15', 'spdperc_50', 'spdperc_85',
           'spdperc_95', 'average_speed', 'adt']
output_df = pd.DataFrame(columns=columns)

# Start filling in values. This is where we will do some math
startdate = df2['Date'].iloc[0]  # study start date
enddate = df2['Date'].iloc[-1]  # study end date

# While we're here, let's get the date difference to calculate ADT later
date_format = '%m/%d/%Y'
date1 = datetime.strptime(startdate, date_format)
date2 = datetime.strptime(enddate, date_format)
difference = (date2 - date1).days  # use this to calculate ADT

# Now let's get the quantiles
speedperc15 = df2['Speed'].quantile(0.15)
speedperc50 = df2['Speed'].quantile(0.50)
speedperc85 = df2['Speed'].quantile(0.85)
speedperc95 = df2['Speed'].quantile(0.95)

# Now let's calculate ADT
ADT = int((df2.shape[0] - 1) / difference)

# Next do the average speed
avgspeed = int(df2['Speed'].mean())

# Now append the new row to the DataFrame
new_row = {
    'name': name,
    'start_date': startdate,
    'end_date': enddate,
    'lat': latitude,
    'lon': longitude,
    'spdperc_15': speedperc15,
    'spdperc_50': speedperc50,
    'spdperc_85': speedperc85,
    'spdperc_95': speedperc95,
    'average_speed': avgspeed,
    'adt': ADT
}
output_df = output_df._append(new_row, ignore_index=True)

print(output_df)

output_df.to_csv('./dev/outputtest.csv', index=False)

