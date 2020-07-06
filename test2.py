# -*- coding: utf-8 -*-
import re
import math
import requests
from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

def lookup_seed_results(names, event, cclass, season):
    eventcodes = {'100':'4', '200': 5}
    classcodes = {'KS': '22', 'MS': '11'}
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
               r = fuzz.ratio(name, nme)
               p = fuzz.partial_ratio(name, nme)
               #print( name , ', ' , nme , ', ' , r , ', ' , p )
               #if (name == nme):
               if (p > 90):
                   #print(nme)
                   pattern = "(\d\d[,.]\d\d)[(]([+-]\d[,.]\d)[)]"
                   match = re.match(pattern, row[0])
                   #print(match)
                   if match:
                       time = float(match.group(1).replace(',','.'))
                       wind = float(match.group(2).replace(',','.'))
                       #corrtime = round( time + 0.071*wind - 0.0042*wind*wind, 2 )
                       corrtime = 0.01*math.ceil(100*( time + 0.071*wind - 0.0042*wind*wind ))
                   seed.append( (time, nme, club) )
                   break
    return(seed)


# ...
event = '100'
competition_class = 'KS'
names = ['Helene Rønningen', 'Anna Linnea Malmquist Gateman', 'Angelica Okparaebo', 'Helene Kjær', 'Tora Bøgeberg Lilleaas' ]
season = '2020'
seed = lookup_seed_results(names, event, competition_class, season)
print (seed)
