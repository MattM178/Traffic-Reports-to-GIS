# This is the main script for the Python script portion of updating traffic counts.
# See the readme.txt for instructions
#

import csv
import time
from PyPDF2 import PdfReader
from scrapers import *

import download

start = str(download.start_id + 1)  # the id number to start processing, one after previous max
end = str(download.end_id)
year = str(download.year)

existing_list = list(pathlib.Path(f'./DOS count files').glob('**/*.pdf'))
process_list_nums = [path.name.split('_')[0] for path in existing_list]

try:
    start_idx = process_list_nums.index(start)
except ValueError as ex:
    raise

scrape_list = existing_list[start_idx:]  # only PDFs that haven't been processed yet

datarows = []
columns = ['uid', 'year', 'start_date', 'end_date', 'lat', 'lon',
           'loc1', 'loc2', 'spdperc_15', 'spdperc_50', 'spdperc_85',
           'spdperc_95', 'avgspd_northbound', 'avgspd_southbound', 'avgspd_eastbound', 'avgspd_westbound', "adt",
           'Count_Type']

# troubleshooting block, uncomment for interactive troubleshooting of specific PDFs
# pdf_path = scrape_list[139]
for pdf_path in scrape_list:
    uid = pdf_path.name.split('_')[0]
    # text extraction phase
    text_results = []
    reader = PdfReader(pdf_path)
    number_of_pages = len(reader.pages)
    for page in range(number_of_pages):
        text = reader.pages[page].extract_text()
        text_results.append(text)
    outtext = "\n\n".join(text_results)
    # scraping phase
    # print(outtext)  - Debugging line
    dates = datescrape(outtext)
    loc_list = locationscrape(outtext)
    speed_list = speedscrape(outtext)
    adt = adtscrape(outtext)
    # output phase
    single_row = [uid] + dates + loc_list + speed_list + adt + ['Speed/Count']
    datarows.append(single_row)


df = pd.DataFrame(data=datarows, columns=columns)

# save the DF as .csv manually or write some more code you lazy son of a gun
df.to_csv('./output/' + f"pdfscraped_Start_{start}_End_{end}.csv", index=False)

# create join table for alltime all PDFs
join_paths = scrape_list
# grab the unique ID for each traffic count, the first element before underscore
uids = [pdf.name.split('_')[0] for pdf in join_paths]
# jump out of GIS folder and point back to DOS count files
paths = ["..\\" + str(pdf.relative_to(".")) for pdf in join_paths]
rows = list(zip(uids, paths))
date = time.strftime('%y_%m_%d')
with open(f'./join tables/jointable_From{start}_To{end}_{date}.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['uid', 'path'])
    writer.writerows(rows)
