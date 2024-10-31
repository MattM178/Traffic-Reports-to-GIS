# This code is under development to update this code to use xlsx files directly instead of scraping PDFs
# Paths must be updated once pushed to production to remove "dev" routing

import pandas as pd
from datetime import datetime as dt
import pathlib
import download
import time
import csv
from arcgis.gis import GIS
from arcgis.features import GeoAccessor

# Connect to ArcGIS Online Account.
gis_username = input("Enter your GIS account username: ")
gis_password = input("Enter your password: ")

gis = GIS("https://clevelandgis.maps.arcgis.com/", gis_username, gis_password)

start = str(download.start_id + 1)  # the id number to start processing, one after previous max
end = str(download.end_id)
year = str(download.year)

existing_list = list((pathlib.Path(download.base_path) / download.year / 'XLSXs').glob('**/*.xlsx'))
existing_list_pdf = list((pathlib.Path(download.base_path) / download.year / 'PDFs').glob('**/*.pdf'))
process_list_nums = [path.name.split('_')[0] for path in existing_list_pdf]

# Adjust process_list_nums to account for missing pdfs in DOS count files. This is janky but it works
# additional_numbers = [str(i) for i in range(0, 640)]
# process_list_nums = additional_numbers + process_list_nums

try:
    start_idx = process_list_nums.index(start)
except ValueError as ex:
    raise

scrape_list = existing_list[start_idx:]  # only XLSXs that haven't been processed yet
scrape_list_pdf = existing_list_pdf[start_idx:] # only PDFs that haven't been processed yet

output = pathlib.Path(f'C:/Users/{download.path_input}/OneDrive - City of Cleveland/Shared Documents - City Planning Group/Transportation and Mobility/'
f'GIS Workspaces/Traffic Reports to GIS/output')

strip_path = str(pathlib.Path(f'C:/Users/{download.path_input}/OneDrive - City of Cleveland/Shared Documents - City Planning Group/Transportation and Mobility/'
f'GIS Workspaces/Traffic Reports to GIS')) # used for getting relative paths for join table, but still run the code outside the folder

# Create a new dataframe to interpolate the data. temporary for now
columns = ['uid', 'year', 'start_date', 'end_date', 'lat', 'lon', 'loc1', 'loc2', 'spdperc_15', 'spdperc_50', 'spdperc_85',
           'spdperc_95', 'average_speed', 'adt', 'speed_table']
# output_df = pd.DataFrame(columns=columns)
datarows = []

# Read each xlsx into two dataframes - headers and content.
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
    starttime = df2['Time'].iloc[0]  # study start time
    endtime = df2['Time'].iloc[-1]  # study end time
    startdatetime = startdate + " " + starttime
    enddatetime = enddate + " " + endtime
    datetime_format = '%m/%d/%Y %I:%M:%S %p'
    date1 = dt.strptime(startdatetime, datetime_format)
    date2 = dt.strptime(enddatetime, datetime_format)
    difference = (date2 - date1).total_seconds() / (24 * 3600)  # use this to calculate ADT
    ADT = int((df2.shape[0] - 1) / difference)
    # Now let's get the quantiles
    speedperc15 = df2['Speed'].quantile(0.15)
    speedperc50 = df2['Speed'].quantile(0.50)
    speedperc85 = df2['Speed'].quantile(0.85)
    speedperc95 = df2['Speed'].quantile(0.95)

    # Next do the average speed
    avgspeed = int(df2['Speed'].mean())

    # Now calcuate if report qualifies the location for a speed table
    if 1000 <= ADT <= 4000 and avgspeed >= 25 and speedperc85 >= 31:
        speed_table = "Yes"
    else:
        speed_table = "No"

    # Now append the new row to the DataFrame
    new_row = {
        'uid': uid,
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
        'adt': ADT,
        'speed_table': speed_table
    }
    print(new_row) # Debugging
    datarows.append(new_row)

output_df = pd.DataFrame(data=datarows, columns=columns)
output_df.to_csv(output / f"Radar_Report_Start_{start}_End_{end}.csv", index=False)

# create join table for PDFs
join_paths = scrape_list_pdf
# grab the unique ID for each traffic count, the first element before underscore
uids = [pdf.name.split('_')[0] for pdf in join_paths]
# This works, but may only need absolute paths now that the script just pulls them directly into the feature layer
absolute_paths = [str(pdf.absolute()) for pdf in join_paths]
relative_paths = [path.replace(strip_path, '') for path in absolute_paths]
rows = list(zip(uids, relative_paths))
date = time.strftime('%y_%m_%d')
with open(f'{download.join_tables}/jointable_From{start}_To{end}_{date}.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['uid', 'path'])
    writer.writerows(rows)

# Save the result data to a csv
# output_df = pd.DataFrame(data=datarows, columns=columns)
# output_df.to_csv(output / f"Radar_Report_Start_{start}_End_{end}.csv", index=False)

# Convert DataFrame to GeoDataFrame
gdf_output = output_df.copy()
gdf_output['SHAPE'] = gdf_output.apply(lambda row: {'x': row['lon'], 'y': row['lat'], 'spatialReference': {'wkid': 4326}}, axis=1)
gdf_output = GeoAccessor.from_df(gdf_output, geometry_column='SHAPE')

# Convert GeoDataFrame to a list of features
feature_set = gdf_output.spatial.to_featureset().features

# Update Existing Traffic Counts layer
Traffic_Counts = gis.content.get("22856c861b20448da86192816e8020a5") # add id
layer = Traffic_Counts.layers[0]
layer.edit_features(adds=feature_set)
print("Features added successfully to the existing layer.")

# Add attachments using join table
for uid, rel_path in rows:
    # Fetch the object ID for each uid (you may need to adjust this to match your setup)
    matching_feature = layer.query(where=f"uid = '{uid}'").features[0]
    oid = matching_feature.attributes['OBJECTID']
    
    # Full path for attachment
    attachment_path = strip_path + rel_path
    
    # Add attachment
    attachment_result = layer.attachments.add(oid, attachment_path)
    print(f"Added attachment to feature UID {uid}: {attachment_result}")

print("All attachments added successfully to the existing layer!")

print("Script Finished!")

