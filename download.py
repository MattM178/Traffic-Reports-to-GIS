# This script automates moving count files from the designated drop folder to a working folder, and assigns 
# count ids

import pathlib

year = str(input('Enter year: '))

path_input = str(input('Enter your username. This is usually your first initial and last name (and digits if '
                       'applicable) found in front of your email address @clevelandohio.gov: '))

# commented paths represent testing paths. This is currently formatted for production.
base_path = pathlib.Path(f'C:/Users/{path_input}/OneDrive - City of Cleveland/Shared Documents - City Planning '
                         f'Group/Transportation and Mobility/GIS Workspaces/Traffic Reports to GIS/DOS count files')
# base_path = pathlib.Path(f'C:/Users/{path_input}/OneDrive - City of Cleveland/Shared Documents - City Planning '
#                         f'Group/Transportation and Mobility/GIS Workspaces/Traffic Reports to GIS/dev/DOS count files')

output = f'C:/Users/{path_input}/OneDrive - City of Cleveland/Shared Documents - City Planning Group/Transportation ' \
         f'and Mobility/GIS Workspaces/Traffic Reports to GIS/output'
# output = f'C:/Users/{path_input}/OneDrive - City of Cleveland/Shared Documents - City Planning Group/Transportation ' \
#         f'and Mobility/GIS Workspaces/Traffic Reports to GIS/dev/output'

join_tables = f'C:/Users/{path_input}/OneDrive - City of Cleveland/Shared Documents - City Planning ' \
              f'Group/Transportation and Mobility/GIS Workspaces/Traffic Reports to GIS/join tables'
# join_tables = f'C:/Users/{path_input}/OneDrive - City of Cleveland/Shared Documents - City Planning ' \
#               f'Group/Transportation and Mobility/GIS Workspaces/Traffic Reports to GIS/dev/join tables'

dump_dir_pdf = f'C:/Users/{path_input}/OneDrive - City of Cleveland/Shared Documents - City Planning Group/Transportation ' \
               f'and Mobility/Traffic & Speed Counts/Counts {year}/PDFs'
# dump_dir_pdf = f'C:/Users/{path_input}/OneDrive - City of Cleveland/Shared Documents - City Planning Group/Transportation ' \
#                f'and Mobility/GIS Workspaces/Traffic Reports to GIS/dev/Traffic & Speed Counts/Counts {year}/PDFs'

# added dump directory for xlsx files - this is referenced by main_xlsx
dump_dir_xlsx = f'C:/Users/{path_input}/OneDrive - City of Cleveland/Shared Documents - City Planning Group/Transportation ' \
                f'and Mobility/Traffic & Speed Counts/Counts {year}/XLSXs'
# dump_dir_xlsx = f'C:/Users/{path_input}/OneDrive - City of Cleveland/Shared Documents - City Planning Group/Transportation ' \
#                 f'and Mobility/GIS Workspaces/Traffic Reports to GIS/dev/Traffic & Speed Counts/Counts {year}/XLSXs'

# Set up and confirm existing files

existing = base_path
existing_pdf = existing / year / 'PDFs'
existing_xlsx = existing / year / 'XLSXs'
year_dir = existing / year

year_dir.mkdir(parents=True, exist_ok=True)

existing_pdfs = list(base_path.glob('**/*.pdf'))
existing_names = [path.name.split('_')[-1] for path in existing_pdfs]
existing_nums = [int(path.name.split('_')[0]) for path in existing_pdfs]

existing_pdfs_year = list(base_path.glob(f'{year}/*.pdf'))
existing_names_year = [path.name.split('_')[-1] for path in existing_pdfs]

start_id = max(existing_nums)
id_no_pdf = start_id
id_no_xlsx = start_id
start = str(start_id)

dump_path_pdf = pathlib.Path(dump_dir_pdf)
dump_path_xlsx = pathlib.Path(dump_dir_xlsx)
dump_pdfs = list(dump_path_pdf.glob('*.pdf'))
dump_xlsxs = list(dump_path_xlsx.glob('*.xlsx'))

# Processing download dump names and giving all IDs
for file in dump_pdfs:
    new_name = str(id_no_pdf + 1) + '_' + file.name
    file.rename(existing_pdf / new_name)
    id_no_pdf += 1

for file in dump_xlsxs:
    new_name = str(id_no_xlsx + 1) + '_' + file.name
    file.rename(existing_xlsx / new_name)
    id_no_xlsx += 1

end_id = id_no_xlsx

print("Done moving files")

