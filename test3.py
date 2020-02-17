# -*- coding: utf-8 -*-
import json
import datetime
import re

def get_category(birthdate, eventdate, gender):
    birthyear = birthdate.year
    eventyear = eventdate.year
    age = int(eventyear)-int(birthyear)
    print(birthyear,eventyear,age)

    g = {'F' : 'J', 'M' : 'G' }
    if age > 19:
        a = 'S'
        g = {'F' : 'K', 'M' : 'M' }
    elif age in (18,19):
        a = '18/19'
    else:
        a = '%d'%(age)

    cat = g[gender]+a
    return cat

f= open('downloads.json', 'r')

j = json.load(f)

print(type(j))
print(j.keys())
print(j['date'])
d = j['date']
isodateformat = "%Y-%M-%d"
date = datetime.datetime.strptime(d, isodateformat)
print(date)

venue = j['venue']['formalName']
print(venue)

ignore_bibs = []
competitors = {}
print(j['competitors'][0])
for c in j['competitors']:
    fn = ''; ln = ''; dob= ''; t=''
    bib  = c['competitorId']
    if 'firstName' in c.keys():
        fn   = c['firstName']
    if 'lastName' in c.keys():
        ln   = c['lastName']
    if 'dateOfBirth' in c.keys():
        d    = c['dateOfBirth']
        dob  = datetime.datetime.strptime(d, isodateformat)
    if 'teamId' in c.keys():
        t    = c['teamId']
    if 'gender' in c.keys():
        g = c['gender']
    if fn=='':
        ignore_bibs.append(bib)
    else:
        competitors[bib] = (fn, ln, dob, g, t)
    #print(bib, competitors[bib])
#print(competitors)



#print(type(j['events']))
#print(type(j['events'][0]))
#print(j['events'][0].keys())
#print(j['events'][0]['units'][0])

results = {}
for e in j['events']:
    eventcode = e['eventCode']
    if eventcode not in results:
        results[eventcode] = {}
    #print(eventcode)
    for u in e['units']:
        #print(u.keys())
        for r in u['results']:
            bib = r['bib']
            if bib not in ignore_bibs:
                print(r)
                d = competitors[bib][2]
                g = competitors[bib][3]
                cat = get_category(d,date,g)
                print(d, date, cat)
                if cat not in results[eventcode].keys():
                    results[eventcode][cat] = []
                # might want to add a dict of performance attributes to this tuple
                # e.g. jump series, sort keys ...
                results[eventcode][cat].append( (bib, r['performance']) )    
print(results)
