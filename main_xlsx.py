# This code is under development to update this code to use xlsx files directly instead of scraping PDFs

import pandas as pd
from datetime import datetime
import pathlib
import download
import time
import csv

start = str(download.start_id + 1)  # the id number to start processing, one after previous max
end = str(download.end_id)
year = str(download.year)

existing_list = list((pathlib.Path(download.base_path) / download.year / 'XLSXs').glob('**/*.xlsx'))
existing_list_pdf = list((pathlib.Path(download.base_path) / download.year / 'PDFs').glob('**/*.pdf'))
process_list_nums = [path.name.split('_')[0] for path in existing_list_pdf]

try:
    start_idx = process_list_nums.index(start)
except ValueError as ex:
    raise

scrape_list = existing_list[start_idx:]  # only XLSXs that haven't been processed yet
scrape_list_pdf = existing_list_pdf[start_idx:] # only PDFs that haven't been processed yet

output = pathlib.Path(f'C:/Users/{download.path_input}/OneDrive - City of Cleveland/Shared Documents - City Planning Group/Transportation and Mobility/'
f'GIS Workspaces/Traffic Reports to GIS/dev/output/output.csv')

strip_path = str(pathlib.Path(f'C:/Users/{download.path_input}/OneDrive - City of Cleveland/Shared Documents - City Planning Group/Transportation and Mobility/'
f'GIS Workspaces/Traffic Reports to GIS/dev')) # used for getting relative paths for join table, but still run the code outside the folder

# Create a new dataframe to interpolate the data. temporary for now, need to add back in UID
columns = ['uid', 'name', 'year', 'start_date', 'end_date', 'lat', 'lon', 'loc1', 'loc2', 'spdperc_15', 'spdperc_50', 'spdperc_85',
           'spdperc_95', 'average_speed', 'adt']
# output_df = pd.DataFrame(columns=columns)
datarows = []

# Read each xlsx into two dataframes - headers and content. Add UID after testing
for file in scrape_list:
    uid = file.name.split('_')[0]
    df = pd.read_excel(file)
    df2 = pd.read_excel(file, header=6)  # this pulls out just the vehicle and speed data
    # Pull out the study name, lat, long, loc1, loc2, and transpose
    info_df = df.iloc[:4, :2].transpose()
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
    loc1 = str(info_df['Location 1:'].iloc[0])
    loc2 = str(info_df['Location 2:'].iloc[0])
    # Ok, now let's extract the actual study data
    # troubleshooting line
    # print(df2)
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
        'uid': uid,
        'name': name,
        'year': year,
        'start_date': startdate,
        'end_date': enddate,
        'lat': latitude,
        'lon': longitude,
        'loc1': loc1,
        'loc2': loc2,
        'spdperc_15': speedperc15,
        'spdperc_50': speedperc50,
        'spdperc_85': speedperc85,
        'spdperc_95': speedperc95,
        'average_speed': avgspeed,
        'adt': ADT
    }
    #print(new_row)
    datarows.append(new_row)

output_df = pd.DataFrame(data=datarows, columns=columns)
output_df.to_csv(output, index=False)

# create join table for alltime all PDFs
join_paths = scrape_list_pdf
# grab the unique ID for each traffic count, the first element before underscore
uids = [pdf.name.split('_')[0] for pdf in join_paths]
# jump out of GIS folder and point back to DOS count files
absolute_paths = ["..\\" + str(pdf.absolute()) for pdf in join_paths]
relative_paths = [path.replace(strip_path, '') for path in absolute_paths]
rows = list(zip(uids, relative_paths))
date = time.strftime('%y_%m_%d')
with open(f'{download.join_tables}/jointable_From{start}_To{end}_{date}.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['uid', 'path'])
    writer.writerows(rows)

print("Script Finished!")

