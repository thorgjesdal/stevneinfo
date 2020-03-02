# -*- coding: utf-8 -*-
import json
import datetime
import re
from openpyxl import Workbook
from openpyxl.styles import colors as xlcolors
from openpyxl.styles import Font, Color

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
d  = j['date']
d2 = j['finishDate']
isodateformat = "%Y-%M-%d"
date = datetime.datetime.strptime(d, isodateformat)
date2 = datetime.datetime.strptime(d2, isodateformat)
bdate = datetime.datetime.strptime('2005-06-24', isodateformat)
print(get_category(bdate,date,'F'))


meetname = j['fullName']
venue = j['venue']['formalName']
print(meetname, venue)

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
        trials = {}
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
                trials[bib]['series'] = s[ij-5:]
            #print(trials)
        #print('T', trials)
#... write template for Results to xlsx workbook
wb = Workbook()
ws = wb.active
    
greenfont = Font(name='Calibri', color=xlcolors.GREEN)
boldfont = Font(name='Calibri', bold=True, underline="single")
    
ws.title = "Resultatliste"
    
ws['a1'] = 'Stevne:';         ws['b1'] = meetname
ws['a2'] = 'Stevnested:';     ws['b2'] = venue
ws['a3'] = 'Stevnedato:';     ws['b3'] = date.strftime('%d.%m.%Y'); ws['c3'] = date2.strftime('%d.%m.%Y')
ws['a4'] = 'Arrangør:';       ws['b4'] = '<arrangør>'; b4=ws['b4']; b4.font=greenfont
ws['a5'] = 'Kontaktperson:';  ws['b5'] = '<navn>'    ; b5=ws['b5']; b5.font=greenfont
ws['a6'] = 'Erklæring*: ';    ws['b6'] = '<J/N>'     ; b6=ws['b6']; b6.font=greenfont
ws['a7'] = 'Telefon:';        ws['b7'] = '<tlf>'     ; b7=ws['b7']; b7.font=greenfont
ws['a8'] = 'Epost:';          ws['b8'] = '<e-post>'  ; b8=ws['b8']; b8.font=greenfont
ws['a9'] = 'Utendørs:';       ws['b9'] = '<J/N>'     ; b9=ws['b9']; b9.font=greenfont
ws['a10'] = 'Kommentar:'

ws['a12'] = 'Resultater';     ws['b12'] = date.strftime('%d.%m.%Y')

row_counter = 14

#print(results)
for event in sorted(results.keys()):
    print(event)
    for cat in sorted(results[event].keys() ):
        ws["A%(row_counter)d"%vars()] = cat; arc = ws["A%(row_counter)d"%vars()]; arc.font=boldfont
        ws["B%(row_counter)d"%vars()] = event ; brc = ws["B%(row_counter)d"%vars()]; brc.font=boldfont
        row_counter +=1
        #print(cat)
        heats = sorted(results[event][cat].keys() )
        for h, heat in zip(range(len(heats)), heats):
            print('Heat: %d'%(h+1))
            ws["A%(row_counter)d"%vars()] = "Heat:";  ws["B%(row_counter)d"%vars()] = h+1;  
            row_counter +=1
            sorted_result = sorted(results[event][cat][heat], key=lambda tup: tup[2])
            for i,r in zip(range(len(sorted_result)),sorted_result):
                bib = r[0]
                perf = r[1]

                fn  = competitors[bib][0]
                ln  = competitors[bib][1]
                dob = competitors[bib][2]
                club = competitors[bib][4]
                print(i+1, fn+' '+ln, club, perf)
                ws["A%(row_counter)d"%vars()] = i+1
                #ws["B%(row_counter)d"%vars()] = bib
                ws["C%(row_counter)d"%vars()] = ' '.join((fn,ln))
                ws["D%(row_counter)d"%vars()] = dob.strftime('%Y')
                ws["E%(row_counter)d"%vars()] = club
                ws["F%(row_counter)d"%vars()] = perf
                row_counter +=1
                ws["A%(row_counter)d"%vars()] = trials[bib]['series']
                row_counter +=1
        row_counter +=1
        


print("done")

"""
class_keys = athlete_by_event_by_class.keys()
class_keys.sort()
for klasse in class_keys:
   event_keys = athlete_by_event_by_class[klasse].keys()
   event_keys.sort()
   for event in event_keys:
           
       e = event_spec(event,klasse)
       ws["A%(row_counter)d"%vars()] = klasse; arc = ws["A%(row_counter)d"%vars()]; arc.font=boldfont
       ws["B%(row_counter)d"%vars()] = e     ; brc = ws["B%(row_counter)d"%vars()]; brc.font=boldfont
       ws["C%(row_counter)d"%vars()] = "<spesiell konkurransestatus>";  crc = ws["C%(row_counter)d"%vars()]; crc.font=greenfont
       row_counter +=1

       if istrack(event):
           ws["A%(row_counter)d"%vars()] = "<Heat | Finale:>";  arc = ws["A%(row_counter)d"%vars()]; arc.font=greenfont
           ws["C%(row_counter)d"%vars()] = "Vind:";  crc = ws["C%(row_counter)d"%vars()]; crc.font=greenfont
           row_counter +=1
          
       for athlete in athlete_by_event_by_class[klasse][event]:
          ws["C%(row_counter)d"%vars()] = athlete['name']
          ws["D%(row_counter)d"%vars()] = athlete['dob'][-4:]
          ws["E%(row_counter)d"%vars()] = athlete['club']
          ws["F%(row_counter)d"%vars()] = "<resultat>"
          if ishjump(event):
             ws["G%(row_counter)d"%vars()] = "<vind>";  grc = ws["G%(row_counter)d"%vars()]; grc.font=greenfont
             ws["H%(row_counter)d"%vars()] = "<resultat>";  hrc = ws["H%(row_counter)d"%vars()]; hrc.font=greenfont
             ws["I%(row_counter)d"%vars()] = "<vind>";  irc = ws["I%(row_counter)d"%vars()]; irc.font=greenfont
          if isfield(event):
             row_counter +=1 # add blank line for series
             ws["A%(row_counter)d"%vars()] = "<hopp-/kastserie>";  arc = ws["A%(row_counter)d"%vars()]; arc.font=greenfont
    
          row_counter +=1
       row_counter +=1
           
    
fname = output_file_name(tree)
xlname = fname+'.xlsx'
"""
wb.save('test.xlsx')
