import sys
import re
from openpyxl import Workbook
from openpyxl import load_workbook
from collections import defaultdict
import datetime
import requests
from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

from stevneinfo import clubs, categories as cats, events

import pprint

gender = {'M':'M', 'K':'F', 'G':'M', 'J':'F'}


def read_isonenxls(f):
    wb = load_workbook(filename=f)
    ws = wb.active

#   columns = ws[1]
#   print(list(columns))
#   sys.exit()
    event_list =  []
    events_by_athlete= {}
    i=1
    for value in ws.iter_rows(min_row=1,min_col=1, max_col=46, values_only=True):
        if i==1:
            columns = value
            i+=1
            continue
        if value[0] is None:
            continue
        if 'Avmeldt' not in value[columns.index('Påmeldingsstatus')] or value[columns.index('Påmeldingsstatus')] is None:
            first_name = value[columns.index('Fornavn')]
            last_name = value[columns.index('Etternavn')]
            dob = value[columns.index('Fødselsdato')]
            g = gender[value[columns.index('Kjønn')]]
            club = value[columns.index('Klubb')]
            ev = value[columns.index('Øvelse')]
            cat = cats.cat_code(value[columns.index('Klasse')])
            #nat = cats.cat_code(value[columns.index('Landskode')])
            nat = value[columns.index('Landskode')]
            athlete_key = (first_name, last_name, dob, g, club, nat)
            event = (ev, events.event_code(ev),  cat)
            print(athlete_key)
            print(event)

            if event[0] is None:
                continue
            if event not in event_list:
                event_list.append(event)
    
            if athlete_key not in events_by_athlete.keys():
                events_by_athlete[athlete_key] = []
            if event not in events_by_athlete[athlete_key]:
                events_by_athlete[athlete_key].append( event )

#   events = sort_event_list(events)
    return event_list, events_by_athlete

def get_stats(event,cat,season):
    event_id = {'100':'4', '200': '5', '400':'7', '800':'9', '1500':'11', '3000':'13', '5000':'14', '10000':'15',
            '100H':'35', '110H':'42', '400H':'59', '2000SC':'65', '3000SC' : '121'}
    catcodes = {'KS': '22', 'MS': '11'}

    if event in event_id.keys():
       url = 'https://www.minfriidrettsstatistikk.info/php/LandsStatistikk.php?showclass=' + cat + '&showevent=' + event_id[event] + '&outdoor=Y&showseason=' + season + '&showclub=0'
       r = requests.get(url)

    
       soup = BeautifulSoup(r.text, 'html.parser')
       tables = [
           [
               [td.get_text(strip=True) for td in tr.find_all('td')]
               for tr in table.find_all('tr')
           ]
           for table in soup.find_all('table')
       ] 
   
       stats = []
       for table in tables:
           for row in table:
               if not row == [] and not row[0] == '-----':
                  name, club  =  row[1].rsplit(',', 1)
                  dob = row[2]
                  perf = row[0]
                  stats.append( (name, dob, perf) )
       return stats



def get_seed_marks(name, dob, event, cat, season): 
    event_id = {'100':'4', '200': 5, '400':'7', 800:'9', '1500':'11', '3000':'13', '5000':'14', '10000':'15',
            '100H':'35', '110H':'42', '400H':'59', '3000SC' : '120' ,
            'HJ':'68', 'PV':'70', 'LJ':'71', 'TJ':'75', } 
    catcodes = {'KS': '22', 'MS': '11',
            'G15':'6', 'G16':'7', 'G17':'8', 'G18/19':'9',
            'J15':'17', 'J16':'18', 'J17':'19', 'J18/19':'20'}

    print(cat,event)
    if cat not in ('MS', 'KS'):
        return ''
    #event = events.event_code(event)
    cat    = catcodes[cat]

    global event_stats
    event_stats = {}

    if event not in event_stats.keys():
        event_stats[event] = {}
    if cat not in event_stats[event]:
        event_stats[event][cat] = {}
    if season not in event_stats[event][cat]:
        event_stats[event][cat][season] = get_stats(event,cat,season)

    res = 'nm'
    s = event_stats.get(event, None)
    if not s is None:
        if not s[cat][season] is None:
           for p in s[cat][season]:
               nme = p[0]

               ratio = fuzz.token_set_ratio(name, nme)
               if ratio>85:
                   if 'Magnus' in name:
                       print(name, nme, ratio, p[2])
                   res = p[2]
                   break

        minsecpat = '(\d?\d)[:.,](\d\d[,.]\d?\d)'
        match1 = re.match(minsecpat,res)
        reswindpat = "(\d?\d[,.]\d\d)[(]([+-]\d[,.]\d)[)]"
        match2 = re.match(reswindpat,res)
        if match1:
            mins = match1.group(1)
            secs = match1.group(2).replace(',','.')
            res = mins + ':' + secs
        elif match2:
            secs = match2.group(1)
            wind = match2.group(2)
            res = secs.replace(',','.')
        else:
            res = res.replace(',','.')
        return res



def write_opentrack_import(f):
    event_list, events_by_athlete = read_isonenxls(f)

    isodateformat = "%Y-%m-%d"
    ddmmyyyyformat = "%d.%m.%Y"
    #... write opentrack bulk import to xlsx workbook
    wb = Workbook()
    ws = wb.active
    ws.title = 'Competitors'
    ws1 = wb.create_sheet('Events')
    
    row_counter = 1
    ws["A1"] = 'Competitor Id'
    ws["B1"] = 'National Id'
    ws["C1"] = 'First name'
    ws["D1"] = 'Last name'
    ws["E1"] = 'Gender'
    ws["F1"] = 'Date of birth'
    ws["G1"] = 'Team ID'
    ws["H1"] = 'Event'
    ws["J1"] = 'Pb'
    ws["K1"] = 'Sb'
#   ws1["A1"] = 'Event selection'
    row_counter = 2

    jf = 0
    jt = 0
    jm = 0
    full_events = {}
    for e in event_list:
        event  = e[0]
        evcode = e[1]
        cat    = e[2]
        if events.isfield(event):
            jf +=1
            event_ref = "F%02d"%jf
        elif events.ismulti(event):
            jm +=1
            event_ref = "M%02d"%jm
        else:
            jt +=1
            event_ref = "T%02d"%jt

        #print(e)
        full_events[ ( cat , evcode ) ]  = event_ref + ' - ' + ' '.join(( cat, events.event_spec(event, cat) ))
        ws1["A%d"%row_counter] = event_ref + ' - '  + ' '.join([e[0], events.event_spec(e[1], cat)])
        ws1["B%d"%row_counter] = event_ref
        ws1["C%d"%row_counter] = evcode
        ws1["D%d"%row_counter] = cats.age_group(cat)
        ws1["E%d"%row_counter] = cats.get_gender(cat)
        ws1["F%d"%row_counter] = cat
#       ws1["G%d"%row_counter] = age_group(class_code(e[0]))

        ws1["H%d"%row_counter] = ' '.join(( cat, events.event_spec(event, cat) ))
        ws1["I%d"%row_counter] = '1'
        ws1["J%d"%row_counter] = '1'
        ws1["K%d"%row_counter] = '12:00'
        
        row_counter +=1
    ws1.delete_cols(1,1)
#   ws.insert_cols(13)
#   print (full_events)
    row_counter = 2    
    bib = 0
    pp = pprint.PrettyPrinter(indent=4)
#   pp.pprint(events_by_athlete)
#   pp.pprint(full_events)
    for key in events_by_athlete.keys():
        bib+=1
        maxname = 30
        fn   = key[0]
        fn   = fn[0:min(len(fn),maxname)]
        ln   = key[1]
        ln   = ln[0:min(len(ln),maxname)]
        dob  = key[2]
        dob = datetime.datetime.strptime(dob,ddmmyyyyformat)
        g    = key[3]
        club = key[4]
        nat  = key[5]
        for e in events_by_athlete[key]:
            #print(e)
            event     = e[0]
            eventcode = e[1]
            cat       = e[2]
            #e = ( event[2], event[1] )

            ws["A%d"%row_counter] = bib
#           ws["B%d"%row_counter] = ident
            ws["C%d"%row_counter] = fn
            ws["D%d"%row_counter] = ln
            ws["E%d"%row_counter] = g
            ws["F%d"%row_counter] = datetime.datetime.strftime(dob,isodateformat)
            ws["G%d"%row_counter] = clubs.club_code(club)
            ws["H%d"%row_counter] = full_events[ (e[2], e[1]) ]

            #event = e[1]
            if not events.isfield(event):
                if eventcode == "60": # for Bassen sprint
                    eventcode = "100"
                res1 = get_seed_marks(' '.join((fn, ln)), dob, eventcode, cat, '2022' )
                res = res1
                if res=='nm':
                    res=''
                if e[1] == '10 000 meter':
                    res3 = get_seed_marks(' '.join((fn, en)), dob, '5000 meter', e[0], '2021' )
                    res4 = get_seed_marks(' '.join((fn, en)), dob, '5000 meter', e[0], '2020' )
                    res3 = min(res3,res4)
                    if res3 == 'nm':
                        res3 = ''
                    ws["M%d"%row_counter] = res3
            else:
                res = ''
            ws["K%d"%row_counter] = res
            row_counter +=1

    xlname = 'opentrack_input.xlsx'
    wb.save(xlname)
#-----

if len(sys.argv) < 2:
   sys.exit("Usage: %s <infile>" % sys.argv[0])
   
infile = sys.argv[1]
print(infile)
#events, events_by_athlete = read_isonenxls(infile)
write_opentrack_import(infile)
#print(events)
#pp = pprint.PrettyPrinter(indent=4)
#pp.pprint(events_by_athlete)
