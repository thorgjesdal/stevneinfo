# -*- coding: utf-8 -*-
import json
import datetime
import re

def get_category(birthdate, eventdate, gender):
    birthyear = birthdate.year
    eventyear = eventdate.year
    age = int(eventyear)-int(birthyear)

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


with open('downloads.json', 'r') as f: 
    j = json.load(f)

print(type(j))
print(j.keys())
print(j['date'])
d = j['date']
isodateformat = "%Y-%M-%d"
date = datetime.datetime.strptime(d, isodateformat)
bdate = datetime.datetime.strptime('2005-06-24', isodateformat)
print(get_category(bdate,date,'F'))



venue = j['venue']['formalName']
print(venue)

ignore_bibs = []
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



#print(type(j['events']))
#print(type(j['events'][0]))
#print(j['events'][0].keys())
#print(j['events'][0]['units'][0])

"""
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
                #print(r)
                d = competitors[bib][2]
                g = competitors[bib][3]
                cat = get_category(d,date,g)
                #print(d, date.strftime('%d.%m.%Y'), cat)
                if cat not in results[eventcode].keys():
                    results[eventcode][cat] = []
                # might want to add a dict of performance attributes to this tuple
                # e.g. jump series, sort keys ...
                results[eventcode][cat].append( (bib, r['performance']) )    
 
    print( bib, (fn, ln, dob.strftime('%d.%m.%Y'), t) )
    competitors[bib] = (fn, ln, dob, t)
#print(competitors)
"""
#print(competitors)




poolnr = 0
results ={}
for e in j["events"]:
    event_code = e["eventCode"]
    if event_code not in e.keys():
        results[event_code] = {}
#       for u in e["units"]:
        for pool, u in zip(range(len(e["units"])),e["units"]):
            #results[event_code] ={}
            for r in u["results"]:
                if "bib" in r.keys():
                    bib = r["bib"]
                
                if bib not in ignore_bibs:
                     bdate = competitors[bib][2]
                     g = competitors[bib][3]
                     cat = get_category(bdate,date,g)
                     if results[event_code].get(cat) == None:
                         results[event_code][cat] = {}
                     if results[event_code][cat].get(pool) == None:
                         results[event_code][cat][pool] = []
#                    x
                     if "performance" in r.keys():
                         res = r["performance"]

                     if "place" in r.keys():
                         pl = r["place"]
                    
#               print (bib, res, pl, poolnr)
                     results[event_code][cat][pool].append((bib, res, pl))
                     #print (bib, res, pl, pool)
#           poolnr = poolnr + 1
#           print (type(u['trials']))
#           print (u['trials'])
            trials = {}
            for t in u['trials']:
                bib = t['bib']
                if trials.get(bib)==None:
                    trials[bib] = {}
                height = t['height']
                if trials[bib].get(height)==None:
                    trials[bib][height] = []
                trials[bib][height].append(t['result'])
            #print(trials)
            for bib in trials.keys():
                s = ''
                for height in sorted(trials[bib].keys() ):
                    #print(trials[bib][height])
                    s += height + '(' + ''.join(trials[bib][height]) + ') ' 
                s = s.replace('.',',')
                i = s.index('x')
                j = s.index('o')
                ij = min(i,j)
                #print(s.index('x'), s.index('o') )
                print(s[ij-5:])


#print(results)
for event in sorted(results.keys()):
    print(event)
    for cat in sorted(results[event].keys() ):
        print(cat)
        heats = sorted(results[event][cat].keys() )
        #for heat in sorted(results[event][cat].keys() ):
        for h, heat in zip(range(len(heats)), heats):
            print('Heat: %d'%(h+1))
            #print(sorted(results[event][cat][heat], key=lambda tup: tup[2]))
            sorted_result = sorted(results[event][cat][heat], key=lambda tup: tup[2])
            for i,r in zip(range(len(sorted_result)),sorted_result):
                #print(r)
                bib = r[0]
                perf = r[1]

                fn = competitors[bib][0]
                ln = competitors[bib][1]
                club = competitors[bib][4]
                print(i+1, fn+' '+ln, club, perf)
        


print("done")

#"""
#print(type(j['events']))
#print(type(j['events'][0]))
#print(j['events'][0].keys())
#print(j['events'][0]['units'][0])
#"""
