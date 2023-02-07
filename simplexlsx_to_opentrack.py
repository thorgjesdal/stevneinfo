import sys
import re
from openpyxl import Workbook
from openpyxl import load_workbook
from collections import defaultdict
import datetime
import requests
from bs4 import BeautifulSoup
#from fuzzywuzzy import fuzz
#from fuzzywuzzy import process

import pprint

gender = {'M':'M', 'K':'F', 'G':'M', 'J':'F'}

def read_eventfile(f):
    wb = load_workbook(filename=f)
    ws = wb.active

    event_codes= {}
    for value in ws.iter_rows(min_row=1,min_col=1, max_col=10, values_only=True):
        cat = value[4]
        event = value[1]
        code = value[0]

        key = (cat, event)
        print(key,code)
        event_codes[key] = code
        
    return event_codes


def read_simplexlsx(f):
    wb = load_workbook(filename=f)
    ws = wb.active

    events_by_athlete= {}
    for value in ws.iter_rows(min_row=2,min_col=1, max_col=46, values_only=True):
        if value[2] is not None:
            cat = value[0]
            ev    = value[1]
            first_name = value[2]
            last_name = value[3]
            dob = value[4]
            team = value[5]
            qp = value[6]
            event = (cat, ev, qp)
            athlete_key = (first_name, last_name, dob, team)

            if athlete_key not in events_by_athlete.keys():
                events_by_athlete[athlete_key] = []
            if event not in events_by_athlete[athlete_key]:
                events_by_athlete[athlete_key].append( event )

    return events_by_athlete




def write_opentrack_import(ef, cf):
    event_codes = read_eventfile(ef)
    events_by_athlete = read_simplexlsx(cf)

    isodateformat = "%Y-%m-%d"
    ddmmyyyyformat = "%d.%m.%Y"
    #... write opentrack bulk import to xlsx workbook
    wb = Workbook()
    ws = wb.active
    ws.title = 'Competitors'
    
    row_counter = 1
    ws["A1"] = 'Competitor Id'
    ws["B1"] = 'National Id'
    ws["C1"] = 'First name'
    ws["D1"] = 'Last name'
    ws["E1"] = 'Gender'
    ws["F1"] = 'Date of birth'
    ws["G1"] = 'Team ID'
    ws["H1"] = 'Nationality'
    ws["I1"] = 'Event'
    ws["J1"] = 'Pb'
    ws["K1"] = 'Sb'
    row_counter = 2

    row_counter = 2    
    bib = 0
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(event_codes)
#   pp.pprint(full_events)
    for key in events_by_athlete.keys():
        bib+=1
        fn   = key[0]
        ln   = key[1]
        dob  = key[2]
        #dob = datetime.datetime.strptime(dob,ddmmyyyyformat)
        team = key[3]
        #qp = key[4]
#       print(key)
        for event in events_by_athlete[key]:
            #print(event)
            e = (event[0], event[1])
            qp = event[2]
            #print(e, qp)
#           e = ( event[2], event[1] )

            ws["A%d"%row_counter] = bib
#           ws["B%d"%row_counter] = ident
            ws["C%d"%row_counter] = fn
            ws["D%d"%row_counter] = ln
            ws["E%d"%row_counter] = gender[event[0][0]]
            ws["F%d"%row_counter] = datetime.datetime.strftime(dob,isodateformat)
            ws["G%d"%row_counter] = team
            ws["I%d"%row_counter] = event_codes[e]
            ws["J%d"%row_counter] = qp

            row_counter +=1

    xlname = 'opentrack_input.xlsx'
    wb.save(xlname)
#-----
event_file = 'event_grid_bassen.xlsx'
competitor_file = 'etteranmeldinger_bassen.xlsx'

#if len(sys.argv) < 2:
#   sys.exit("Usage: %s <infile>" % sys.argv[0])
   
#infile = sys.argv[1]
#print(infile)

#pp = pprint.PrettyPrinter(indent=4)
#pp.pprint(event_codes)
#pp.pprint(events_by_athlete)

write_opentrack_import(event_file, competitor_file)

