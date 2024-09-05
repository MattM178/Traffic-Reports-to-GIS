# TRAFFIC REPORTS TO GIS
### Welcome to automating boring stuff with Dro (and Matt).

---

## Setup

### In order to run the update, you need to have Python, Miniconda, and ArcGIS Pro installed.

Python is the programming language and interprets the code.

Conda will manage the environment of tools Python can use. Python by itself doesn't have the ability to process PDFs.
Basically, Conda installs all the right "plugins" so this code can run.

1. Install Python for Windows
2. Install Miniconda
3. Clone the trafficreports environment.   
   **You only need to set up the environment once on a machine.**

4. Open Miniconda command prompt
5. Run this command below to clone the environment

    `conda env create -n trafficreports --file environment.yml`
It should create an environment in your conda directory (usually in your Windows user home under miniconda)


## Step 1: RUNNING THE MAIN SCRIPT (MAIN.PY)

This script is part of a multi-step process to update a new batch of traffic count data. Running main.py successfuly does 4 things:

* Download all the new reports from a single page of the sharepoint directory where TE dumps reports
* Number them in the numbering system and move them into the DOS count files folder in this project
* Scrape location and speed data out of them
* **Create two new csv tables**. 1 is the traffic data. And 2 is a "join table" that describes where the attachments
   are for each traffic count so ArcGIS Pro can find them and attach.

You need to run main.py using the "trafficreports" environment. That requires doing the setup once for the machine above.
1. First activate that environment with: `conda activate trafficreports`
2. Navigate to the project root folder on your computer: 
*Transportation and Mobility\GIS Workspaces\Traffic Reports to GIS* by using cd (current directory command).
`cd (the path on your drive)`
3. Execute the script with: `python main.py`

### Going through the script

1. Enter the year of the reports you're processing when prompted.
2. For the username prompt, enter your username. This is typically what you use to log in to your Windows machine. On enterprise systems where usernames are associated with organization email accounts, this is the content before the @ symbol in your email.
4. Let this script run like the wind. Check for the 2 output CSV files.
   1. One CSV in \output --- Main table that has the coordinates and all speed/count as rows 
   2. One CSV in \join tables --- Table that ArcGIS uses to find the right PDF to upload to each point

## Step 2: Posting edits to feature service
After successfully running Python script, you go into ArcGIS Pro project for managing traffic count reports.  

### Traffic Reports GIS Project 
* Location
  * City Planning SharePoint\Transportation and Mobility\GIS Workspaces\Traffic Reports to GIS\GIS_project
* Layers
  * It should have the internal Traffic Counts layer loaded. 
* Toolbox
  * There is a toolbox tool called "Update Traffic Counts". This tool has two inputs, which are the two csv tables from this script. Browse to those files to use as inputs.

When you run, it will append the new traffic count points to the internal Traffic Count service on ArcGIS Online and
PDF attachments to each point using the join table

### That concludes all necessary steps to bring data over!


