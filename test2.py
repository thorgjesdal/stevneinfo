# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup

def lookup_seed_results(names, event, cclass, season):
    eventcodes = {'100m':'4'}
    classcodes = {'KS': '22'}
    url = 'https://www.minfriidrettsstatistikk.info/php/LandsStatistikk.php?showclass=' + classcodes[cclass] + '&showevent=' + eventcodes[event] + '&outdoor=Y&showseason=' + season + '&showclub=0'
    r = requests.get(url)
#   print(r.text)

    soup = BeautifulSoup(r.text, 'html.parser')
    tables = [
        [
            [td.get_text(strip=True) for td in tr.find_all('td')]
            for tr in table.find_all('tr')
        ]
        for table in soup.find_all('table')
    ] 
#   print(tables[0])
    seed = []
    for name in names:
        for row in tables[0]:
            if not row == [] and not row[0] == '-----':
               nme, club  =  row[1].split(',')
               if (name == nme):
                   seed.append( (row[0], nme, club) )
                   break
    print (seed)



# ...
event = '100m'
competition_class = 'KS'
names = ['Ezinne Okparaebo', 'Helene Rønningen']
season = '2019'
seed = lookup_seed_results(names, event, competition_class, season)
