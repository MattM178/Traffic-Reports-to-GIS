# TRAFFIC REPORTS TO GIS
### Welcome to automating boring stuff with Dro (and Matt).

---

## Setup

### In order to run the update, you need to have ArcGIS Pro installed. This code is designed to work directly with ArcGIS Online (AGO), so an account is required to use this code. If you are running this in a python IDE, your interpeter should be set to the ArcGIS Pro python interpreter, or otherwise have your interperter set up to use the ArcGIS python API.

Python is the programming language and interprets the code. 

ArcGIS Pro comes with its own python envrionment, so when it comes time to run the script you can activate that enviroment and run the script within it.

## Step 1: RUNNING THE MAIN SCRIPT (MAIN_V2.PY)

This script is part of a multi-step process to update a new batch of traffic count data. Running main.py successfuly does 4 things:

* Locate all new reports in PDF and XLSX format from a pre-defined sharepoint directory, accessed through the local user.
* Number them in the numbering system and move them into the DOS count files folder in this project.
* Convert the XLSX files into a dataframe formatted identically to the final feature later in AGO (in our use case, [Cleveland Traffic Count Reports.](https://clevelandgis.maps.arcgis.com/home/item.html?id=41dac8cbf74a4e31bda30a105b53bcc6))
* **Create two new csv tables**. 1 is the traffic data (for troubleshooting). And 2 is a "join table" that describes where the attachments are for each traffic count so the script can attach them to the feature layer.
* Convert the dataframe into a geodataframe, then into a list of features and adds them to the Traffic Count Reports layer. 
* Add the attachments identified in the join table to the newly added features in the previous step.

You need to run main_V2.py using the "arcgispro-py3" environment.
1. First open a command prompt in Windows and navigate to the project root folder on your computer: 
*Transportation and Mobility\GIS Workspaces\Traffic Reports to GIS* by using cd (current directory command). `cd (the path on your drive)`
2. No activate the ArcGIS Pro python enviroment by entering the path to to the enviroment. Paths may vary depending on your installation (like if it is installed system wide or for a specific user), but the default path is: `"C:\Program Files\ArcGIS\Pro\bin\Python\Scripts\proenv"`
3. Execute the script with: `python main_V2.py`

### Going through the script

1. Enter the year of the reports you're processing when prompted.
2. For the username prompt, enter your username. This is typically what you use to log in to your Windows machine. On enterprise systems where usernames are associated with organization email accounts, this is the content before the @ symbol in your email.
3. Once the script moves the files, it will print `Done moving files`. You'll then be prompted to enter your AGO username and password.
4. After entering your login information you will need to enter the item id of the feature layer. Item ids can be found by navigating to the ArcGIS Online page of the target feature layer and pulling the characters from the URL following `?id=`.
5. Now let this script run like the wind. You'll see some feel-good printouts once the features are successfully added, printouts for each successful attachment, and finally `Script Finished!` once fully complete. If you want, you can check for the 2 output CSV files.
   1. One CSV in \output --- Main table that has the coordinates and all speed/count as rows 
   2. One CSV in \join tables --- Table that ArcGIS uses to find the right PDF to upload to each point

6. Lastly, you can double check the feature layer to which you've just added new features and confirm they are there and formatted correctly.

### That concludes all necessary steps to bring data over!

Confirm features are there and in the right place by viewing the feature layer, either through AGO or in an ArcGIS Pro project.

