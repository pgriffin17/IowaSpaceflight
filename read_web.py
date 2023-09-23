# This is python code for Iowa Spaceflight by jake writen on 2023-09-23
# This code copies the Iowa Spaceflight page into a table for querying NASA Horizons

from urllib.request import urlopen
import re # regular expressions
import time # for getting today's date
import os # for file management
from bs4 import BeautifulSoup # for html parsing


def read_website(url = "https://physics.uiowa.edu/history/spaceflight-instruments"):
    # read in data from a site and save a table for querying NASA Horizons
    #print(f'Retrieving {url}')
    with urlopen(url) as response:
        html = response.read()
    # decode the bytes
    html = html.decode('utf-8')
    (table_start,table_end) = find_table(html)
    #print(f"table starts at {table_start} and ends at {table_end}")
    soup = BeautifulSoup(html[table_start:table_end], features='html.parser')
    mission_matches = soup.find_all('tr')
    mission_table = list() # list of lists with string entries for [name, remarks, launch]
    for mission in mission_matches:
        column = mission.find_all('td')
        mission_name = column[0].string
        mission_remarks = ""
        #print(mission_name)
        try:
            if "*" in mission_name:
                mission_remarks = "Currently operating Iowa instruments.  "
                mission_name = mission_name.split("*")[0].strip()+mission_name.split("*")[1].strip()
            if "(" in mission_name:
                remarks = mission_name.split("(")
                mission_remarks = mission_remarks + remarks[1].split(")")[0].strip()
                if len(remarks) > 2:
                    for remark in remarks[2:]:
                        mission_remarks = mission_remarks + ", " + remark.split(")")[0]
                mission_name = mission_name.split("(")[0].strip()
        except TypeError:
            mission_name = ""
            mission_remarks = ""
        mission_launch = column[1].string
        mission_table.append([mission_name, mission_remarks, mission_launch])
    return(mission_table)

def find_table(html):
    # find the table in the html
    # return beginning and end positions

    table_start = re.search(r'<table class="xl679643">', html).start()
    table_end = re.search(r'</table>', html[table_start:]).start()+table_start
    return (table_start, table_end)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    mission_table = read_website()
    print(mission_table[30:35])

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
