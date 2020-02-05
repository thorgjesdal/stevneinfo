# -*- coding: utf-8 -*-
import json
import datetime

def get_category(dob,gender):
    today = datetime.datetime.now()
    thisyear = today.year
    birthyear = dob[-4:]
    age = int(thisyear)-int(birthyear)

    g = {'F' : 'J', 'M' : 'G' }
    if age > 20:
        a = 'S'
        g = {'F' : 'K', 'M' : 'M' }
    elif age in (18,19):
        a = '18/19'
    else:
        a = '%d'%(age)

    cat = g[gender]+a
    return cat

print(get_category('24.06.2001','F'))



with open('downloads.json', 'r') as f: 
    j = json.load(f)

print(type(j))
print(j.keys())
print(j['date'])
d = j['date']
date = '.'.join(( d[8:10], d[5:7], d[0:4] ))
print(date)

venue = j['venue']['formalName']
print(venue)

competitors = {}
#print(j['competitors'][0])
for c in j['competitors']:
    fn = ''; ln = ''; dob= ''; t=''
    bib  = c['competitorId']
    if 'firstName' in c.keys():
        fn   = c['firstName']
    if 'lastName' in c.keys():
        ln   = c['lastName']
    if 'dateOfBirth' in c.keys():
        d    = c['dateOfBirth']
        dob  = '.'.join(( d[8:10], d[5:7], d[0:4] ))
    if 'teamId' in c.keys():
        t    = c['teamId']
    print( bib, (fn, ln, dob, t) )
    competitors[bib] = (fn, ln, dob, t)
#print(competitors)



"""
print(type(j['events']))
print(type(j['events'][0]))
print(j['events'][0].keys())
print(j['events'][0]['units'][0])
"""
