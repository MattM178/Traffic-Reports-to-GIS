# This script automates downloading from DOS's sharepoint. This is step 1 before running main Go to
# http://its-sharepoint1/Dept/PRP/TE/Shared%20Documents/Forms/AllItems.aspx and find the right Traffic counts folder
# for your year


# import requests
# import bs4
# import re
import pathlib
# import os

year = str(input('Enter year:'))

path_input = str(input('Enter your username. This is usually your first initial and last name (and digits if '
                       'applicable) found in front of your email address @clevelandohio.gov: '))

base_path = pathlib.Path(f'C:/Users/{path_input}/OneDrive - City of Cleveland/Shared Documents - City Planning '
                         f'Group/Transportation and Mobility/GIS Workspaces/Traffic Reports to GIS/DOS count'
                         f'files')

output = f'C:/Users/{path_input}/OneDrive - City of Cleveland/Shared Documents - City Planning Group/Transportation ' \
         f'and Mobility/GIS Workspaces/Traffic Reports to GIS/output'

join_tables = f'C:/Users/{path_input}/OneDrive - City of Cleveland/Shared Documents - City Planning ' \
              f'Group/Transportation and Mobility/GIS Workspaces/Traffic Reports to GIS/join tables'

dump_dir = f'C:/Users/{path_input}/OneDrive - City of Cleveland/Shared Documents - City Planning Group/Transportation ' \
           f'and Mobility/GIS Workspaces/Traffic Reports to GIS/Counts {year}'

# Set up and confirm existing files

existing = base_path
year_dir = existing / year

year_dir.mkdir(parents=True, exist_ok=True)

existing_pdfs = list(base_path.glob('**/*.pdf'))
existing_names = [path.name.split('_')[-1] for path in existing_pdfs]
existing_nums = [int(path.name.split('_')[0]) for path in existing_pdfs]

existing_pdfs_year = list(base_path.glob(f'{year}/*.pdf'))
existing_names_year = [path.name.split('_')[-1] for path in existing_pdfs]

start_id = max(existing_nums)
id_no = start_id
start = str(start_id)

dump_path = pathlib.Path(dump_dir)
dump_pdfs = list(dump_path.glob('*.pdf'))

# Processing download dump names and giving all IDs
for file in dump_pdfs:
    new_name = str(id_no + 1) + '_' + file.name
    file.rename(existing / year / new_name)
    id_no += 1

end_id = id_no
print("Done moving pdfs")
