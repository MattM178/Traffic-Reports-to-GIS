import re
import pandas as pd
import numpy as np
from download import *

import download


def speedscrape(outtext) -> list:
    # scraping loop
    alttype = re.findall(r'15th Percentile :\s+(\d*) MPH', outtext)  # check for less common format of PDF
    if alttype:
        percs = {'15': np.nan, '50': np.nan, '85': np.nan, '95': np.nan}
        for perc in percs.keys():
            hits = re.findall(f'{perc}th Percentile :\s*(\d*) MPH', outtext)
            hits = [spd for spd in hits if spd != 0]
            out = sum([int(x) for x in hits]) / len(hits)
            percs[perc] = out
        return list(percs.values())

    type1 = re.findall(r'Percentile\s+15th\s+50th', outtext)  # testing whether it is type 1
    if type1:
        hits = re.findall(r'95th\s+Speed\s{1,10}(\d\d?\.?\d?)\s*(\d\d?\.?\d?)?\s*(\d\d?\.?\d?)?\s*(\d\d?\.?\d?)?',
                          outtext)
        hits = [list(item) for item in hits]
        hits = [spd for spd in hits if spd != 0]
        # clean up 0s and nulls
        for group in hits:
            for idx, spd in enumerate(group):
                if spd == '' or spd == '0':
                    group[idx] = np.nan
                else:
                    pass
        # convert to data frame to create a mean
        hits_df: pd.DataFrame = pd.DataFrame(hits, dtype='float')
        outpercs = hits_df.mean().values.tolist()

        nb = re.findall(r'Direction: NB.*?Percentile.*?Mean Speed\s\(Average\)(\d\d?\.?\d?)', flags=re.DOTALL, string=outtext)
        sb = re.findall(r'Direction: SB.*?Percentile.*?Mean Speed\s\(Average\)(\d\d?\.?\d?)', flags=re.DOTALL, string=outtext)
        eb = re.findall(r'Direction: EB.*?Percentile.*?Mean Speed\s\(Average\)(\d\d?\.?\d?)', flags=re.DOTALL, string=outtext)
        wb = re.findall(r'Direction: WB.*?Percentile.*?Mean Speed\s\(Average\)(\d\d?\.?\d?)', flags=re.DOTALL, string=outtext)

        avgs = [nb, sb, eb, wb]
        for idx, result in enumerate(avgs):
            if len(result) == 0:
                avgs[idx] = np.nan
            else:
                avgs[idx] = float(result[0])
        return outpercs + avgs
    else:
        return [np.nan] * 8


def locationscrape(outtext):
    lat = re.findall(r'Latitude:\s(\d\d\.\d*)', outtext)
    lon = re.findall(r'Longitude:\s(-\d\d\.\d*)', outtext)
    loc1 = re.findall(r'Location 1:\s(.*?)\sStart Date\s?:', outtext)
    loc2 = re.findall(r'Location 2:\s(.*?)\sEnd Date\s?:', outtext)
    if loc1 and not loc2:  # if the match is an empty string
        loc1dir = re.findall(r'(\w*) (north|south|east|west) (of) (\w*)', flags=re.IGNORECASE, string=loc1[0]) # check for directional structure
        if loc1dir:
            loc1 = loc1dir[0][0]
            loc2 = loc1dir[0][3]

    def nullify(x):
        if type(x) is list and len(x) >= 1:  # if more than one match, take the first one
            return x[0]
        elif type(x) is str:  # if it is a string, do nothing
            return x
        else:  # otherwise return a null value
            return np.nan

    data = list(map(nullify, [lat, lon, loc1, loc2]))
    return data


def directionscrape(loc1, loc2) -> list:
    direction = []
    from_street = []
    cross_st = []

    dir_patt = re.compile(r'(north|south|east|west) (of) (.*)', re.IGNORECASE)
    nondir_patt = re.compile(r"(between |near )(\w*\.?\s?\w+\.?)\s(and|or|to)\s(\w*\.?\s?\w+\.?)", re.IGNORECASE)

    dir_loc1 = dir_patt.findall(loc1)
    dir_loc2 = dir_patt.findall(loc2)
    if dir_loc1:
        direction.append(dir_loc1[0][0].title())
        from_street.append(dir_loc1[0][-1])
        cross_st.append(loc1 + ' and ' + dir_loc1[0][-1])
        return direction + from_street + cross_st
    elif dir_loc2:
        direction.append(dir_loc2[0][0].title())
        from_street.append(dir_loc2[0][-1])
        cross_st.append(loc1 + ' and ' + dir_loc2[0][-1])
        return direction + from_street + cross_st
    elif not (dir_loc1 or dir_loc2):
        near_loc1 = nondir_patt.findall(loc1)
        near_loc2 = nondir_patt.findall(loc2)
        if not bool(near_loc1 or near_loc2):
            return [np.nan] * 3
        if near_loc1:
            direction.append(near_loc1[0][0])
            from_street.append(near_loc1[0][1])
            cross_st.append(loc1 + ' and ' + near_loc1[0][1])
            return direction + from_street + cross_st
        if near_loc2:
            direction.append(near_loc2[0][0])
            from_street.append(near_loc2[0][2])
            cross_st.append(loc1 + ' and ' + near_loc2[0][1])
            return direction + from_street + cross_st
    else:
        return [np.nan] * 3


# Text extraction
def datescrape(pdftext) -> list:
    outtext = pdftext
    year = download.year
    # scraping loop
    m1 = re.search(r'Start Date:\s*(\d?\d/\d?\d/20\d\d)', outtext)
    m2 = re.search(r'End Date:\s*(\d?\d/\d?\d/20\d\d)', outtext)
    m3 = re.findall(r'\d?\d/\d?\d/\d\d', outtext)
    m4 = re.findall(r'\d?\d-\w\w\w-\d\d*', outtext)
    if re.search(r'Start Date:\s*\d?\d/\d?\d/(20\d\d)', outtext):
        year = re.search(r'Start Date:\s*\d?\d/\d?\d/(20\d\d)', outtext).group(1)
    if m1 and m2:
        return [year, m1.group(1), m2.group(1)]
    elif m3:
        date_series = pd.Series(m3)
        return [year, date_series.min(), date_series.max()]
    elif m4:
        date_series = pd.Series(m4, dtype='datetime64')
        date_series = date_series.dt.strftime('%m/%d/%Y')
        return [year, date_series.min(), date_series.max()]
    else:
        return [year, np.nan, np.nan]

#modifed adtscrape on 4.25.24 to handle reports without ADT fields in them
def adtscrape(pdftext) -> list:
    outtext = pdftext
    matches = re.findall(r'\sADT: (\S*)', string=outtext)
    if matches:
        adt = int(matches[0].replace(',', ''))
        return [adt]
    else:
        return []