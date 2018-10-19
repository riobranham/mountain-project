# =====================================================================
# Title: Scrape mountainproject.com
# Author: rbranham
# Date: 10/18/18
# =====================================================================

# %% Setup

import re
import requests

import numpy as np
import pandas as pd

from bs4 import BeautifulSoup

# %% Scrape

base_url = 'https://www.mountainproject.com/'

# Scrape main page
r = requests.get(base_url)
soup = BeautifulSoup(r.text, 'lxml')

# Get links to all areas
areas = soup.find('div', id='route-guide')
links = [a['href'] for a in areas.find_all('a')]

# Loop through all areas
meta = {'description': [],
        'name': [],
        'lat': [],
        'long': [],
        'elevation': [],
        'page_views_total': [],
        'page_view_month': [],
        'n_comments': [],
        'comments': []}
# TODO: Download all photos
for link in links:
    link_r = requests.get(link)
    link_soup = BeautifulSoup(link_r.text, 'lxml')
    desc = link_soup.find('div', {'class': 'fr-view'})
    meta['description'].append(desc.text)
    name = link_soup.find('h1').text.strip()
    meta['name'].append(name)
    desc_table = link_soup.find('table', {'class': 'description-details'}).text
    lat, long = list(map(float, re.findall('-?\d+\.\d+', desc_table)))
    elevation = int(re.findall('\d+', desc_table)[0])

