#!/usr/bin/python
# -*- coding: utf-8 -*-
from xml.etree import ElementTree as ET
from openpyxl import Workbook
from openpyxl.styles import colors
from openpyxl.styles import Font, Color

with open('NIF', 'rt') as f:
    tree = ET.parse(f)
#print type(tree)

#for node in tree.iter():
#    print node.tag, node.attrib

def etree_to_dict(t):
    d = {t.tag : map(etree_to_dict, t.getchildren())}
    d.update(('@' + k, v) for k, v in t.attrib.iteritems())
    d['text'] = t.text
    return d

s = tree.find('.//Competition')
mn = s.attrib['name']
md = s.attrib['startDate']

v = s.find('CompetitionVenue')
mv = v.attrib['startingvenue']
sn =  mn + ' ' + mv + ' ' + md
fname = sn.replace(' ','_')

events_by_athlete = {}
events_by_athlete_by_club = {}
athlete_by_class_by_event = {}
athlete_by_event_by_class = {}
for c in tree.findall('.//Competitor'):
   p = c.find('Person')
   club = p.attrib['clubName']
   cs = club.split(',')
   if len(cs) > 1:
      club = cs[1].strip() + ' ' + cs[0].strip()
   n = p.find('./Name')
   name = "Name"
   fn = n.find('Given')
   en = n.find('Family')
   bd = p.find('BirthDate')
   name = fn.text + ' ' + en.text
   dd = int(bd.attrib['day'])
   mm = int(bd.attrib['month'])
   yyyy = int(bd.attrib['year'])
   dob = "%(dd)02d.%(mm)02d.%(yyyy)04d" % vars()
   ec = c.find('./Entry/EntryClass')
   klasse = ec.attrib['classCode']
   ec = c.find('./Entry/Exercise')
   event = ec.attrib['name'] 
   athlete_key = name + dob + club
   if athlete_key not in events_by_athlete.keys():
      events_by_athlete[athlete_key] = {}
      events_by_athlete[athlete_key]['name'] = name
      events_by_athlete[athlete_key]['dob'] = dob
      events_by_athlete[athlete_key]['club'] = club
      events_by_athlete[athlete_key]['events'] = []
   events_by_athlete[athlete_key]['events'].append(event + ' ' + klasse)
   if club not in events_by_athlete_by_club:
      events_by_athlete_by_club[club] = {}
   events_by_athlete_by_club[club][athlete_key] = {'name': name, 'dob': dob, 'events' : [] }
   events_by_athlete_by_club[club][athlete_key]['events'].append(event + ' ' + klasse)
  
   if event not in athlete_by_class_by_event.keys():
      athlete_by_class_by_event[event]={}
   if klasse not in athlete_by_class_by_event[event].keys():
      athlete_by_class_by_event[event][klasse]=[]
   athlete_by_class_by_event[event][klasse].append({'name': name, 'dob': dob, 'club' : club }) 

   if klasse not in athlete_by_event_by_class.keys():
      athlete_by_event_by_class[klasse] = {}
   if event not in athlete_by_event_by_class[klasse].keys():
      athlete_by_event_by_class[klasse][event] = [] 
   athlete_by_event_by_class[klasse][event].append({'name': name, 'dob': dob, 'club' : club }) 

   
"""for athlete_key in events_by_athlete.keys().sort():
   print events_by_athlete[athlete_key]['name'], '('+events_by_athlete[athlete_key]['dob']+')', events_by_athlete[athlete_key]['club']
   for e in events_by_athlete[athlete_key]['events']:
      print '   ', e
"""
"""for club in events_by_athlete_by_club.keys():
   print club
   for athlete_key in events_by_athlete_by_club[club].keys():
      print '   '+events_by_athlete_by_club[club][athlete_key]['name'], '('+events_by_athlete_by_club[club][athlete_key]['dob']+')'
      for e in events_by_athlete_by_club[club][athlete_key]['events']:
          print '      ', e
"""
#... write template for Results to xlsx workbook
wb = Workbook()
ws = wb.active

greenfont = Font(name='Calibri', color=colors.GREEN)
boldfont = Font(name='Calibri', bold=True, underline="single")

ws.title = "Resultatliste"

ws['a1'] = 'Stevne:';         ws['b1'] = mn
ws['a2'] = 'Stevnested:';     ws['b2'] = mv
ws['a3'] = 'Stevnedato:';     ws['b3'] = md          ; ws['c3'] = '<til dato>'; c3=ws['c3']; c3.font=greenfont
ws['a4'] = 'Arrangør:';       ws['b4'] = '<arrangør>'; b4=ws['b4']; b4.font=greenfont
ws['a5'] = 'Kontaktperson:';  ws['b5'] = '<navn>'    ; b5=ws['b5']; b5.font=greenfont
ws['a6'] = 'Erklæring*: ';    ws['b6'] = '<J/N>'     ; b6=ws['b6']; b6.font=greenfont
ws['a7'] = 'Telefon:';        ws['b7'] = '<tlf>'     ; b7=ws['b7']; b7.font=greenfont
ws['a8'] = 'Epost:';          ws['b8'] = '<e-post>'  ; b8=ws['b8']; b8.font=greenfont
ws['a9'] = 'Utendørs:';       ws['b9'] = '<J/N>'     ; b9=ws['b9']; b9.font=greenfont
ws['a10'] = 'Kommentar:'

ws['a12'] = 'Resultater';     ws['b12'] = md

row_counter = 14
class_keys = athlete_by_event_by_class.keys()
class_keys.sort()
for klasse in class_keys:
   event_keys = athlete_by_event_by_class[klasse].keys()
   event_keys.sort()
   for event in event_keys:
       
       ws["A%(row_counter)d"%vars()] = klasse; arc = ws["A%(row_counter)d"%vars()]; arc.font=boldfont
       ws["B%(row_counter)d"%vars()] = event ; brc = ws["B%(row_counter)d"%vars()]; brc.font=boldfont
       ws["C%(row_counter)d"%vars()] = "<spesiell konkurransestatus>";  crc = ws["C%(row_counter)d"%vars()]; crc.font=greenfont
       row_counter +=1
      
       for athlete in athlete_by_event_by_class[klasse][event]:
#         print athlete
          ws["C%(row_counter)d"%vars()] = athlete['name']
          ws["D%(row_counter)d"%vars()] = athlete['dob']
          ws["E%(row_counter)d"%vars()] = athlete['club']
          row_counter +=1

       row_counter +=1
       

xlname = fname+'.xlsx'
wb.save(xlname)
