# TRAFFIC REPORTS TO GIS
### Welcome to automating boring stuff with Dro (and Matt).

---

## Setup

### In order to run the update, you need to have Python, Miniconda, and ArcGIS Pro installed. Alternatively, you'll need your environment configured to access ArcGIS python API if you do not have ArcGIS Pro. Regardless, this code is designed to work directly with ArcGIS Online (AGO), so an account is required to use this code. If you are running this in a python IDE, your interpeter should be set to the ArcGIS Pro python interpreter, or otherwise have your interperter set up to use the ArcGIS python API.

Python is the programming language and interprets the code. 

Conda will manage the environment of tools Python can use. Basically, Conda installs all (or most) the right "plugins" so this code can run.

1. Install Python for Windows
2. Install Miniconda
3. Clone the trafficreports environment.   
   **You only need to set up the environment once on a machine.**

4. Open Miniconda command prompt
5. Run this command below to clone the environment:

    `conda env create -n trafficreports --file environment.yml`

    It should create an environment in your conda directory (usually in your Windows user home under miniconda)

6. You will need to install the arcgis package through conda to use the API You can do so by opening your conda prompt and running this command:

   `conda install esri::arcgis`

You can use the Anaconda Python interpreter, but you can also use the ArcGIS Python interpreter, which comes with ArcGIS Pro. [This link provides more information on how to set up an IDE, in this case PyCharm, to use the ArcGIS Python interpreter.](https://community.esri.com/t5/python-documents/pycharm-setup-for-arcgis-desktop/ta-p/1125129)


## Step 1: RUNNING THE MAIN SCRIPT (MAIN_V2.PY)

This script is part of a multi-step process to update a new batch of traffic count data. Running main.py successfuly does 4 things:

* Locate all new reports in PDF and XLSX format from a pre-defined sharepoint directory, accessed through the local user.
* Number them in the numbering system and move them into the DOS count files folder in this project.
* Convert the XLSX files into a dataframe formatted identically to the final feature later in AGO (in our use case, [Cleveland Traffic Count Reports.](https://clevelandgis.maps.arcgis.com/home/item.html?id=41dac8cbf74a4e31bda30a105b53bcc6))
* **Create two new csv tables**. 1 is the traffic data (for troubleshooting). And 2 is a "join table" that describes where the attachments are for each traffic count so the script can attach them to the feature layer.
* Convert the dataframe into a geodataframe, then into a list of features and adds them to the Traffic Count Reports layer. 
* Add the attachments identified in the join table to the newly added features in the previous step.

You need to run main_V2.py using the "trafficreports" environment. That requires doing the setup once for the machine above.
1. First activate that environment with: `conda activate trafficreports`

2. Navigate to the project root folder on your computer: 
*Transportation and Mobility\GIS Workspaces\Traffic Reports to GIS* by using cd (current directory command).
`cd (the path on your drive)`
3. Execute the script with: `python main_V2.py`

### Going through the script

1. Enter the year of the reports you're processing when prompted.
2. For the username prompt, enter your username. This is typically what you use to log in to your Windows machine. On enterprise systems where usernames are associated with organization email accounts, this is the content before the @ symbol in your email.
3. Once the script moves the files, it will print `Done moving files`. You'll then be prompted to enter your AGO username and password.
4. Now let this script run like the wind.You'll see some feel-good printouts once the features are successfully added, printouts for each successful attachment, and finally `Script Finished!` once fully complete. If you want, you can check for the 2 output CSV files.
   1. One CSV in \output --- Main table that has the coordinates and all speed/count as rows 
   2. One CSV in \join tables --- Table that ArcGIS uses to find the right PDF to upload to each point

### That concludes all necessary steps to bring data over!

Confirm features are there and in the right place by viewing the feature layer, either through AGO or in an ArcGIS Pro project.

