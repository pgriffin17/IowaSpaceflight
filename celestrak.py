import astroquery.jplhorizons as jpl
import astropy.time as time
import astropy.units as u
import numpy as np
import pandas as pd
import urllib.request
import read_web
from datetime import datetime
import re

'''
Usage:
import celestrak

# Generate list of active spacecraft
celestrak.generate_active_list()

or for a dictionary:
celestrak.generate_active_dict()

'''

def convert_date(date):
    if date is None:
        return "N/A"
    elif "Sept." in date:
        date = date.replace('Sept.', 'Sep.')
    elif re.search(r'\.\d', date):
        date = date.replace('.', '. ')
    try:
        date_obj = datetime.strptime(date, '%Y %b. %d').strftime('%Y-%m-%d')
    except ValueError as e:
        if any(month in str(e) for month in ("May", "June", "July")):
            date_obj = datetime.strptime(date, '%Y %B %d').strftime('%Y-%m-%d')
        else:
            return "N/A"

    return date_obj

def create_mission_table():
    missionTable = read_web.read_website()
    # Send table to dataframe, taking columns from the first row
    missionTable = pd.DataFrame(missionTable[1:], columns=missionTable[0])
    # Uppercase all spacecraft names
    missionTable['Spacecraft'] = missionTable['Spacecraft'].str.upper()

    # Convert dates to astropy time objects
    missionTable['Launch Date (UT)'] = [convert_date(date) for date in missionTable['Launch Date (UT)']]

    # Set spacecraft name in 75-78 as MMS 1-4
    missionTable.loc[75:78, 'Spacecraft'] = ['MMS 1', 'MMS 2', 'MMS 3', 'MMS 4']

    # If spacecraft contains CLUSTER, split at space and take second element
    missionTable.loc[missionTable['Spacecraft'].str.contains('CLUSTER'), 'Spacecraft'] = \
        missionTable.loc[missionTable['Spacecraft'].str.contains('CLUSTER'), 'Spacecraft'].str.split().str[1]

    # 
    clusterDict = {"SAMBA": "CLUSTER II-FM7 (SAMBA)", "SALSA": "CLUSTER II-FM6 (SALSA)", "TANGO": "CLUSTER II-FM8 (TANGO)", "RUMBA": "CLUSTER II-FM5 (RUMBA)"}
    missionTable['Spacecraft'] = missionTable['Spacecraft'].replace(clusterDict)

    # If no launch date, remove
    missionTable = missionTable[~missionTable['Launch Date (UT)'].str.contains("N/A")]

    # If "fail" in second column, remove row
    missionTable = missionTable[~missionTable.iloc[:,1].str.contains("fail")]

    return missionTable

def download_satcat():
    url = "https://celestrak.com/pub/satcat.csv"
    filename = "satcat.csv"
    urllib.request.urlretrieve(url, filename)

def read_satcat():
    satcat = pd.read_csv("satcat.csv")
    return satcat

def generate_active_list(display=False):
    missionList = create_mission_table()
    satcat = read_satcat()

    # Get lines with spacecraft names from satcat
    # add to new dataframe
    missionList = [craft.upper() for craft in missionList['Spacecraft']]
    mask = satcat['OBJECT_NAME'].isin(missionList)
    missionList = satcat[mask]
    
    # Move active spacecraft to new dataframe
    # judging activity by "DECAY_DATE" column
    # if the spacecraft is active, this column is NaN
    activeList = missionList[missionList['DECAY_DATE'].isnull()]
    activeList = activeList.reset_index(drop=True)

    # If display = true, remove certain columns
    if display:
        # Remove all columns except "OBJECT_NAME" "OBJECT_ID" "NORAD_CAT_ID" "LAUNCH_DATE" "OWNER" "ORBIT_CENTER"
        activeList = activeList[['OBJECT_NAME', 'OBJECT_ID', 'NORAD_CAT_ID', 'LAUNCH_DATE', 'OWNER', 'ORBIT_CENTER']]

    return activeList

def generate_active_dict():
    activeList = generate_active_list(display=True)
    active_dict = activeList.to_dict('list')
    return active_dict