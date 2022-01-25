# -*- coding: utf-8 -*-
import json
import datetime
import re
from openpyxl import Workbook
from openpyxl.styles import colors as xlcolors
from openpyxl.styles import Font, Color

noplace = int(1.e10)-1
def get_category(birthdate, eventdate, gender):
    birthyear = birthdate.year
    eventyear = eventdate.year
    age = int(eventyear)-int(birthyear)

    g = {'F' : 'J', 'M' : 'G' }
    if age > 19:
        g = {'F' : 'K', 'M' : 'M' }
        if age < 35:
           a = 'S'
        else:
           a = 'V' + '%d'%(5*int(age/5))
    elif age in (18,19):
        a = '18/19'
    else:
        a = '%d'%(age)

    cat = g[gender]+a
    return cat

   
def event_name(code):
    event_names = {
            '60'     : '60 meter'          , 
            '80'     : '80 meter'          , 
            '100'    : '100 meter'         , 
            '150'    : '150 meter'         , 
            '200'    : '200 meter'         , 
            '300'    : '300 meter'         , 
            '400'    : '400 meter'         , 
            '600'    : '600 meter'         , 
            '800'    : '800 meter'         , 
            '1000'   : '1000 meter'        , 
            '1500'   : '1500 meter'        , 
            '3000'   : '3000 meter'        , 
            '5000'   : '5000 meter'        , 
            '10000'  : '10000 meter'       , 
            '60H'    : '60 meter hekk'     , 
            '80H'    : '80 meter hekk'     , 
            '100H'   : '100 meter hekk'    , 
            '110H'   : '110 meter hekk'    , 
            '200H'   : '200 meter hekk'    ,
            '300H'   : '300 meter hekk'    , 
            '400H'   : '400 meter hekk'    , 
            '3000SC' : '3000 meter hinder' , 
            '1000W'  : 'Kappgang 1000 meter'        , 
            '3000W'  : 'Kappgang 3000 meter'        , 
            'HJ'     : 'Høyde'             , 
            'PV'     : 'Stav'              , 
            'LJ'     : 'Lengde'            , 
            'TJ'     : 'Tresteg'           , 
            'SP'     : 'Kule'              , 
            'DT'     : 'Diskos'            , 
            'HT'     : 'Slegge'            , 
            'JT'     : 'Spyd'              , 
            'OT'     : 'Liten ball'              , 
            'BT'     : 'Liten ball'              , 
            'DEC'    : 'Tikamp'            , 
            'HEP'    : 'Sjukamp'           ,
            'SHJ'    : 'Høyde uten tilløp' ,
            'SLJ'    : 'Lengde uten tilløp'           
            }
    return event_names[code]

def event_spec(event, klasse):
    # 18.05.2020 rewrite based om implements.py form athlib
    gender = 'F'
    if klasse[0] in ('M', 'G'):
        gender = 'M'

    weight = ''
    if event == 'SP' or event == 'HT':
        if gender == 'F':
           if klasse in ('J10', 'J11', 'J12', 'J13'):
              weight = '2,0kg'
           elif klasse in ('J14', 'J15', 'J15', 'J16', 'J17'):
               weight = '3,0kg'
           elif klasse in ('J18/19', 'KU20', 'KS', 'KV35', 'KV40', 'KV45'):
               weight = '4,0kg'
           elif klasse >= 'KV50':
               weight = '3,0kg'
        elif gender == 'M':
           if klasse in ('G10', 'G11' ):
              weight = '2,0kg'
           elif klasse in ('G12', 'G13' ):
               weight = '3,0kg'
           elif klasse in ('G14', 'G15', 'MV70', 'MV75' ):
               weight = '4,0kg'
           elif klasse in ('G16', 'G17', 'MV60', 'MV65' ):
               weight = '5,0kg'
           elif klasse in ('G18/19', 'MU20', 'MV50', 'MV55' ):
               weight = '6,0kg'
           elif klasse in ('MS', 'MU23', 'MV35', 'MV40', 'MV45' ):
               weight = '7,26kg'
           elif klasse >= 'MV80':
               weight = '3,0kg'
    elif event == 'DT' :
        if gender == 'F':
           if klasse in ('J10', 'J11', 'J12', 'J13'):
              weight = '0,6kg'
           elif klasse in ('J14', 'J15'):
               weight = '0,75kg'
           elif klasse >= 'KV80':
               weight = '0,75kg'
           else:
               weight = '1,0kg'
        elif gender == 'M':
           if klasse in ('G10', 'G11' ):
              weight = '0,6kg'
           elif klasse in ('G12', 'G13' ):
               weight = '0,75kg'
           elif klasse in ('G14', 'G15' ):
               weight = '1,0kg'
           elif klasse in ('G16', 'G17', 'MV50', 'MV55' ):
               weight = '1,5kg'
           elif klasse in ('G18/19', 'MU20' ):
               weight = '1,75kg'
           elif klasse in ('MS', 'MU23', 'MV35', 'MV40', 'MV45' ):
               weight = '2,0kg'
           elif klasse >= 'MV60':
               weight = '1,0kg'
    elif event == 'JT' :
        if gender == 'F':
           if klasse in ('J10', 'J11', 'J12', 'J13', 'J14'):
              weight = '400g'
           elif klasse in ('J15', 'J16', 'J17', 'KV50', 'KV55'):
               weight = '500g'
           elif klasse in ('J18/19', 'KU20', 'KU23', 'KS', 'KV35', 'KV40', 'KV45'):
               weight = '600g'
           elif klasse >= 'KV60':
               weight = '400g'
        elif gender == 'M':
           if klasse in ('G10', 'G11', 'G13', ):
              weight = '400g'
           elif klasse in ('G14', 'G15', 'MV60', 'MV65' ):
               weight = '600g'
           elif klasse in ('G16', 'G17', 'MV50', 'MV55' ):
               weight = '700g'
           elif klasse in ('G18/19', 'MU20', 'MS', 'MU23', 'MV35', 'MV40', 'MV45' ):
               weight = '800g'
           elif klasse in ('MV70', 'MV75' ):
               weight = '500g'
           elif klasse >= 'MV80':
               weight = '400g'
    elif event == 'OT' :
        weight='150g'


    throws = {}
    throws['SP'] = { 'J10' : '2,0kg', 'J11' : '2,0kg', 'J12' : '2,0kg', 'J13' : '2,0kg', 
                       'J14' : '3,0kg', 'J15' : '3,0kg', 'J16' : '3,0kg', 'J17' : '3,0kg',
                       'J18/19' : '4,0kg', 'KU20' : '4,0kg', 'KU23' : '4,0kg', 'KS' : '4,0kg', 
                       'KV35' : '4,0kg', 'KV40' : '4,0kg', 'KV45' : '4,0kg', 
                       'KV50' : '3,0kg', 'KV55' : '3,0kg', 'KV60' : '3,0kg', 'KV65' : '3,0kg', 
                       'G10' : '2,0kg', 'G11' : '2,0kg', 'G12' : '3,0kg', 'G13' : '3,0kg', 
                       'G14' : '4,0kg', 'G15' : '4,0kg', 'G16' : '5,0kg', 'G17' : '5,0kg',
                       'G18/19' : '6,0kg', 'MU20' : '6,0kg', 'MU23' : '7,26kg', 'MS' : '7,26kg'
                       } 
    throws['DT'] = { 'J10' : '0,6kg', 'J11' : '0,6kg', 'J12' : '0,6kg', 'J13' : '0,6kg', 
                       'J14' : '0,75kg', 'J15' : '0,75kg', 'J16' : '0,75kg', 'J17' : '0,75kg',
                       'J18/19' : '1,0kg', 'KU20' : '1,0kg', 'KU23' : '1,0kg', 'KS' : '1,0kg', 
                       'G10' : '0,6kg', 'G11' : '0,6kg', 'G12' : '0,75kg', 'G13' : '0,75kg', 
                       'G14' : '1,0kg', 'G15' : '1,0kg', 'G16' : '1,5kg', 'G17' : '1,5kg',
                       'G18/19' : '1,75kg', 'MU20' : '1,75kg', 'MU23' : '2,0kg', 'MS' : '2,0kg', 
                       'MV35' : '2,0kg', 'MV40' : '2,0kg', 'MV45' : '2,0kg',
                       'MV50' : '1,5kg', 'MV55' : '1,5kg', 
                       'MV60' : '1,0kg', 'MV65' : '1,0kg', 'MV70' : '1,0kg', 'MV75' : '1,0kg' 
                       } 
    throws['HT'] = { 'J10' : '2,0kg', 'J11' : '2,0kg', 'J12' : '2,0kg', 'J13' : '2,0kg', 
                       'J14' : '3,0kg', 'J15' : '3,0kg', 'J16' : '3,0kg', 'J17' : '3,0kg',
                       'J18/19' : '4,0kg', 'KU20' : '4,0kg', 'KU23' : '4,0kg', 'KS' : '4,0kg', 
                       'G10' : '2,0kg', 'G11' : '2,0kg', 'G12' : '3,0kg', 'G13' : '3,0kg', 
                       'G14' : '4,0kg', 'G15' : '4,0kg', 'G16' : '5,0kg', 'G17' : '5,0kg',
                       'G18/19' : '6,0kg', 'MU20' : '6,0kg', 'MU23' : '7,26kg', 'MS' : '7,26kg'} 
    throws['JT'] = { 'J10' : '400g', 'J11' : '400g', 'J12' : '400g', 'J13' : '400g', 
                       'J14' : '400g', 'J15' : '500g', 'J16' : '500g', 'J17' : '500g',
                       'J18/19' : '600g', 'KU20' : '600g', 'KU23' : '600g', 'KS' : '600g', 
                       'G10' : '400g', 'G11' : '400g', 'G12' : '400g', 'G13' : '400g', 
                       'G14' : '600g', 'G15' : '600g', 'G16' : '700g', 'G17' : '700g',
                       'G18/19' : '800g', 'MU20' : '800g', 'MU23' : '800g', 'MS' : '800g'} 
    throws['OT'] = { 'J10' : '150g', 'J11' : '150g', 'J12' : '150g', 'J13' : '150g', 'J14' : '150g', 
                             'G10' : '150g', 'G11' : '150g', 'G12' : '150g', 'G13' : '150g', 'G14' : '150g' }
    hurdles = {}
    hurdles['60H'] = { 'J10' : '68,0cm', 'J11' : '68,0cm', 'J12' : '76,2cm', 'J13' : '76,2cm', 'J14' : '76,2cm',
                                 'J15' : '76,2cm', 'J16' : '76,2cm', 'J17' : '76,2cm',
                                 'J18/19' : '84,0cm','KU20' : '84,0cm', 'KU23' : '84,0cm', 'KS' : '84,0cm',
                                 'KV50' : '76,2cm',
                                 'G10' : '68,0cm', 'G11' : '68,0cm', 'G12' : '76,2cm', 'G13' : '76,2cm', 'G14' : '84,0cm',
                                 'G15' : '84,0cm', 'G16' : '91,4cm', 'G17' : '91,4cm',
                                 'G18/19' : '100cm','MU20' : '100cm', 'MU23' : '106,7cm', 'MS' : '106,7cm' ,
                                 'MV35':'100cm', 'MV40':'91,4cm', 'MV45':'91,4cm', 'MV50':'91,4cm', 'MV55':'91,4cm', 
                                 'MV60':'84cm', 'MV65':'84cm', 'MV70':'76,2cm', 'MV75':'76,2cm', 
                                 }
    hurdles['80H'] = { 'J15' : '76,2cm', 'J16' : '76,2cm', 'G14' : '84,0cm' } 
    hurdles['100H'] = { 'J16' : '76,2cm', 'J17' : '76,2cm', 'J18/19' : '84,0cm','KU20' : '84,0cm', 'KU23' : '84,0cm', 'KS' : '84,0cm',
                                 'G15' : '84,0cm', 'G16' : '91,4cm'}
    hurdles['110H'] = { 'G17' : '91,4cm', 'G18/19' : '100cm','MU20' : '100cm', 'MU23' : '106,7cm', 'MS' : '106,7cm' }
    hurdles['200H'] = { 'J10' : '68,0cm', 'J11' : '68,0cm', 'J12' : '68,0cm', 'J13' : '68,0cm', 'J14' : '76,2cm',
                                 'J15' : '76,2cm', 'J16' : '76,2cm', 'J17' : '76,2cm',
                                 'J18/19' : '76,2cm','KU20' : '76,2cm', 'KU23' : '76,2cm', 'KS' : '76,2cm',
                                 'G10' : '68,0cm', 'G11' : '68,0cm', 'G12' : '68,0cm', 'G13' : '68,0cm', 'G14' : '76,2cm',
                                 'G15' : '76,2cm', 'G16' : '76,2cm', 'G17' : '76,2cm',
                                 'G18/19' : '76,2cm','MU20' : '76,2cm', 'MU23' : '76,2cm', 'MS' : '76,2cm' }
    hurdles['300H'] = { 'J15' : '76,2cm', 'J16' : '76,2cm', 'J17' : '76,2cm',
                                 'J18/19' : '76,2cm','KU20' : '76,2cm', 'KU23' : '76,2cm', 'KS' : '76,2cm',
                                 'G15' : '76,2cm', 'G16' : '84,0cm', 'G17' : '84,0cm',
                                 'G18/19' : '91,4cm','MU20' : '91,4cm', 'MU23' : '91,4cm', 'MS' : '91,4cm' }
    hurdles['400H'] = { 'J15' : '76,2cm', 'J16' : '76,2cm', 'J17' : '76,2cm',
                                 'J18/19' : '76,2cm','KU20' : '76,2cm', 'KU23' : '76,2cm', 'KS' : '76,2cm',
                                 'G15' : '76,2cm', 'G16' : '84,0cm', 'G17' : '84,0cm',
                                 'G18/19' : '91,4cm','MU20' : '91,4cm', 'MU23' : '91,4cm', 'MS' : '91,4cm' }


    if event in ('SP', 'DT', 'JT', 'HT', 'OT'):
       #e = event + ' ' + throws[event][klasse]
#       e = event_name(event) + ' ' + throws[event].get(klasse,'')
       e = event_name(event) + ' ' + weight
    elif event in ('60H', '80H', '100H', '110H', '200H', '300H', '400H'): 
       e = event_name(event) + ' ' + hurdles[event][klasse]
    else:
       e = event_name(event)

    return e
#---------------------------------------
with open('downloads.json', 'r') as f: 
    j = json.load(f)

#print(type(j))
#print(j.keys())
#print(j['date'])
d  = j['date']
d2 = j['finishDate']
isodateformat = "%Y-%m-%d"
date = datetime.datetime.strptime(d, isodateformat)
#print(d, date)
date2 = datetime.datetime.strptime(d2, isodateformat)
bdate = datetime.datetime.strptime('2005-06-24', isodateformat)
#print(get_category(bdate,date,'F'))


meetname = j['nameLocal']
slug = j['slug']
if j.get('venue') == None: 
    venue = ''
else:
    venue = j['venue']['formalName']
#print(meetname, venue)

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
#   if 'teamId' in c.keys():
#       t    = c['teamId']
    if 'teamName' in c.keys():
        t    = c['teamName']

    if 'gender' in c.keys():
        g = c['gender']
    if fn=='':
        ignore_bibs.append(bib)
    else:
        competitors[bib] = (fn, ln, dob, g, t)
#        print(bib, competitors[bib])



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
series = {}
for e in j["events"]:
    event_code = e["eventCode"]
    category = e["category"]
    event_key = (category, event_code)
    series[event_key] = {}
    if event_key not in e.keys():
        results[event_key] = {}
#       for u in e["units"]:
        trials = {}
        for pool, u in zip(range(len(e["units"])),e["units"]):
            #results[event_code] ={}
            if "windAssistance" in u.keys():
                wind = u["windAssistance"]
            else:
                wind = None
            #print(wind)

            for r in u["results"]:
                #print(r)
                if "bib" in r.keys():
                    bib = r["bib"]
                
                if bib not in ignore_bibs:
                     bdate = competitors[bib][2]
                     g = competitors[bib][3]
                     cat = get_category(bdate,date,g)
                     if results[event_key].get(cat) == None:
                         results[event_key][cat] = {}
                     if results[event_key][cat].get(pool) == None:
                         #results[event_code][cat][pool] = []
                         results[event_key][cat][pool] = {'marks' : []}
                     if not wind == None:
                         results[event_key][cat][pool]['wind'] = wind
#                    x
                     if "performance" in r.keys():
                         res = r["performance"]
                     else:
                         res = ''

                     if "place" in r.keys():
                         pl = r["place"]
                     else:
                         pl = noplace
                   
#                    if "order" in r.keys():
#                        pl = r["order"]
                    
                     print (event_code, bib, res, pl, pool)
                     #results[event_code][cat][pool].append((bib, res, pl))
                     results[event_key][cat][pool]['marks'].append((bib, res, pl))
                     #print (bib, res, pl, pool)
#           poolnr = poolnr + 1
#           print (type(u['trials']))
#           print (u['trials'])
            if event_code in ('HJ', 'SHJ', 'PV'):
                for t in u['trials']:
                    bib = t['bib']
                    if trials.get(bib)==None:
                        trials[bib] = {}
                    height = t['height']
                    if trials[bib].get(height)==None:
                        trials[bib][height] = []
                    trials[bib][height].append(t['result'])
                for bib in trials.keys():
                    s = ''
                    for height in sorted(trials[bib].keys() ):
                        s += height + '(' + ''.join(trials[bib][height]) + ') ' 
                    s = s.replace('.',',')
#                    print(s)
                    i = j = len(s)
                    if 'x' in s:
                        i = s.index('x')
                    if 'o' in s:
                        j = s.index('o')
                    ij = min(i,j)
                    if ij < len(s):
                        series[event_key][bib] = s[ij-5:]
                    else:
                        series[event_key][bib] = ''
            elif event_code in ('LJ', 'TJ', 'SP', 'DT', 'HT', 'JT', 'OT', 'BT'):
                for t in u['trials']:
                    bib = t['bib']
                    if trials.get(bib)==None:
                        trials[bib] = {}
#                   print(event_code, t)
                    rond = t['round']
                    if trials[bib].get(rond)==None:
                        trials[bib][rond] = {}
                    trials[bib][rond]['result'] = t['result']
                    if 'wind' in t.keys():
                        trials[bib][rond]['wind'] = t['wind']

                for bib in trials.keys():
                    s = ''
                    for rond in sorted(trials[bib].keys() ):
                        s += trials[bib][rond]['result'] 
                        if 'wind' in trials[bib][rond].keys():
                            s += "(%3.1f)" % (trials[bib][rond]['wind'])
                        s += '/'    
                    s = s.replace('.',',')
                    series[event_key][bib] = s[:-1]

#... write template for Results to xlsx workbook
wb = Workbook()
ws = wb.active
    
greenfont = Font(name='Calibri', color="0000FF00")
#greenfont = Font(name='Calibri', color=xlcolors.GREEN)
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
for event_key in sorted(results.keys()):
    print(event_key)
    event = event_key[1]
    for cat in sorted(results[event_key].keys() ):
        ws["A%(row_counter)d"%vars()] = cat; arc = ws["A%(row_counter)d"%vars()]; arc.font=boldfont
        ws["B%(row_counter)d"%vars()] = event_spec(event,cat) ; brc = ws["B%(row_counter)d"%vars()]; brc.font=boldfont
        row_counter +=1
#       print(cat)
        heats = sorted(results[event_key][cat].keys() )
        for h, heat in zip(range(len(heats)), heats):
#           print('Heat: %d'%(h+1))
            ws["A%(row_counter)d"%vars()] = "Heat:";  ws["B%(row_counter)d"%vars()] = h+1;  
            if 'wind' in results[event_key][cat][heat].keys():
                ws["C%(row_counter)d"%vars()] = "Vind:";  ws["D%(row_counter)d"%vars()] = results[event_key][cat][heat]['wind']
            row_counter +=1
            sorted_result = sorted(results[event_key][cat][heat]['marks'], key=lambda tup: tup[2])
#           print(sorted_result)
            for i,r in zip(range(len(sorted_result)),sorted_result):
                bib = r[0]
                perf = r[1].replace('.',',')
                place = r[2]

                fn  = competitors[bib][0]
                ln  = competitors[bib][1]
                dob = competitors[bib][2]
                club = competitors[bib][4]
#               print(fn,ln,club,perf)

                if place == noplace:
                    pl = ''
                else:
                    pl = i+1
                ws["A%(row_counter)d"%vars()] = pl
                #ws["B%(row_counter)d"%vars()] = bib
                ws["C%(row_counter)d"%vars()] = ' '.join((fn,ln))
                ws["D%(row_counter)d"%vars()] = dob.strftime('%Y')
#               ws["E%(row_counter)d"%vars()] = club_name(club)
                ws["E%(row_counter)d"%vars()] = club
                ws["F%(row_counter)d"%vars()] = perf

#--- extract wind for best performance from series
                s = series[event_key].get(bib, 'no_series')
                if event in ('LJ', 'TJ') and not s == 'no_series':
                    pat = r'/?%(perf)s\(([+-]?\d,\d)\)/?' % vars()
                    match = re.search(pat,s)
                    if match:
                        ws["G%(row_counter)d"%vars()] = match.group(1)

                if not s=='no_series':
                    row_counter +=1
                    ws["A%(row_counter)d"%vars()] = s
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
xlname = slug + '-' + date.strftime(isodateformat) + '.xlsx'
wb.save(xlname)
