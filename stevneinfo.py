#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
from xml.etree import ElementTree as ET
from openpyxl import Workbook
from openpyxl.styles import colors
from openpyxl.styles import Font, Color
from tabulate import tabulate

def read_xml_into_tree(infile):
   with open(infile, 'rt') as f:
      tree = ET.parse(f)
   return tree
#print type(tree)
#for node in tree.iter():
#    print node.tag, node.attrib

def extract_competition_data(tree):
   s = tree.find('.//Competition')
   mn = s.attrib['name']
   md = s.attrib['startDate']

   v = s.find('CompetitionVenue')
   mv = v.attrib['startingvenue']
   return{'meet_name' : mn, 'meet_date' : md, 'venue' : mv}

def output_file_name(tree):
   cdata = extract_competition_data(tree)
   mn = cdata['meet_name']
   md = cdata['meet_date']
   mv = cdata['venue']

   sn =  mn.encode('utf-8') + ' ' + mv.encode('utf-8') + ' ' + md.encode('utf-8')
   fname = sn.replace(' ','_')
   return fname

def save_xml_copy(tree):
   fname = output_file_name(tree)
   # save a copy of the element tree
   tree.write(fname+'.xml', encoding="utf-8")

def istrack(event):
    return 'meter' in event

def ishurdles(event):
    return istrack(event) and 'hekk' in event

def isfield(event):
    return 'meter' not in event

def isvjump(event):
    return isfield(event) and event in ['Høyde', 'Stav', 'Høyde uten tilløp']

def ishjump(event):
    return isfield(event) and event in ['Lengde', 'Lengde satssone', 'Tresteg', 'Lengde uten tilløp', 'Tresteg uten tilløp']

def isthrow(event):
    return isfield(event) and event in ['Kule', 'Diskos', 'Slegge', 'Spyd', 'Vektkast']

def sort_athletes_by_class_by_event(tree):
#   events_by_athlete = {}
#   events_by_athlete_by_club = {}
    athlete_by_class_by_event = {}
#   athlete_by_event_by_class = {}
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
#      if athlete_key not in events_by_athlete.keys():
#         events_by_athlete[athlete_key] = {}
#         events_by_athlete[athlete_key]['name'] = name
#         events_by_athlete[athlete_key]['dob'] = dob
#         events_by_athlete[athlete_key]['club'] = club
#         events_by_athlete[athlete_key]['events'] = []
#      events_by_athlete[athlete_key]['events'].append(event + ' ' + klasse)
#      if club not in events_by_athlete_by_club:
#         events_by_athlete_by_club[club] = {}
#      events_by_athlete_by_club[club][athlete_key] = {'name': name, 'dob': dob, 'events' : [] }
#      events_by_athlete_by_club[club][athlete_key]['events'].append(event + ' ' + klasse)
      
       if event not in athlete_by_class_by_event.keys():
          athlete_by_class_by_event[event]={}
       if klasse not in athlete_by_class_by_event[event].keys():
          athlete_by_class_by_event[event][klasse]=[]
       athlete_by_class_by_event[event][klasse].append({'name': name, 'dob': dob, 'club' : club }) 

#   if klasse not in athlete_by_event_by_class.keys():
#       athlete_by_event_by_class[klasse] = {}
#   if event not in athlete_by_event_by_class[klasse].keys():
#       athlete_by_event_by_class[klasse][event] = [] 
#   athlete_by_event_by_class[klasse][event].append({'name': name, 'dob': dob, 'club' : club }) 


    return athlete_by_class_by_event

def sort_athletes_by_event_by_class(tree):
#   events_by_athlete = {}
#   events_by_athlete_by_club = {}
#   athlete_by_class_by_event = {}
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
#      if athlete_key not in events_by_athlete.keys():
#         events_by_athlete[athlete_key] = {}
#         events_by_athlete[athlete_key]['name'] = name
#         events_by_athlete[athlete_key]['dob'] = dob
#         events_by_athlete[athlete_key]['club'] = club
#         events_by_athlete[athlete_key]['events'] = []
#      events_by_athlete[athlete_key]['events'].append(event + ' ' + klasse)
#      if club not in events_by_athlete_by_club:
#         events_by_athlete_by_club[club] = {}
#      events_by_athlete_by_club[club][athlete_key] = {'name': name, 'dob': dob, 'events' : [] }
#      events_by_athlete_by_club[club][athlete_key]['events'].append(event + ' ' + klasse)
      
#      if event not in athlete_by_class_by_event.keys():
#         athlete_by_class_by_event[event]={}
#      if klasse not in athlete_by_class_by_event[event].keys():
#         athlete_by_class_by_event[event][klasse]=[]
#      athlete_by_class_by_event[event][klasse].append({'name': name, 'dob': dob, 'club' : club }) 

       if klasse not in athlete_by_event_by_class.keys():
           athlete_by_event_by_class[klasse] = {}
       if event not in athlete_by_event_by_class[klasse].keys():
           athlete_by_event_by_class[klasse][event] = [] 
       athlete_by_event_by_class[klasse][event].append({'name': name, 'dob': dob, 'club' : club }) 


    return athlete_by_event_by_class

def write_start_lists_as_html(tree):
    competition_data = extract_competition_data(tree)
    mn = competition_data['meet_name']
    md = competition_data['meet_date']
    mv = competition_data['venue']

    athlete_by_class_by_event = sort_athletes_by_class_by_event(tree)

    fname = output_file_name(tree)
    of = open (fname+"_deltagere_pr_ovelse.html".encode('utf-8'), 'w')
    of.write(""" <!DOCTYPE html>
    <meta charset="UTF-8">
    <html>
    <body>
    <title> %(mn)s </title>
    <h1> %(mn)s </h1>
    """ % vars() )
    of.write("%s, %s" % ( md, mv.encode('utf-8') ) )
    event_keys = athlete_by_class_by_event.keys() 
    event_keys.sort()
    for event_key in event_keys:
        class_keys = athlete_by_class_by_event[event_key].keys()
        class_keys.sort()
        for class_key in  class_keys:
           of.write( "<h2>%s %s </h2>\n<ul style=\"list-style-type:none\">\n"% (event_key.encode('utf-8'), class_key) )
           for athlete in athlete_by_class_by_event[event_key][class_key]:
                of.write("<li>" +athlete['name'].encode('utf-8') + ' (' + athlete['dob'] +'), ' + athlete['club'].encode('utf-8') +  "</li>\n" )
           of.write("</ul>\n")
    
    #  print athlete_by_class_byevent[event_key]['name'], '('+events_by_athlete[athlete_key]['dob']+')', events_by_athlete[athlete_key]['club']
    #  for e in events_by_athlete[athlete_key]['events']:
    #     print '   ', e
    
    
       
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
    of.write("""</body>
    </html>""")
    of.close()


def write_xlsx_results_template(tree):
    competition_data = extract_competition_data(tree)
    mn = competition_data['meet_name']
    md = competition_data['meet_date']
    mv = competition_data['venue']

    athlete_by_event_by_class = sort_athletes_by_event_by_class(tree)
#   athlete_by_class_by_event = sort_athletes_by_class_by_event(tree)

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

           if 'meter' in event: # is a track event
               ws["A%(row_counter)d"%vars()] = "<Heat | Finale:>";  arc = ws["A%(row_counter)d"%vars()]; arc.font=greenfont
               ws["C%(row_counter)d"%vars()] = "Vind:";  crc = ws["C%(row_counter)d"%vars()]; crc.font=greenfont
               row_counter +=1
          
           for athlete in athlete_by_event_by_class[klasse][event]:
              ws["C%(row_counter)d"%vars()] = athlete['name']
              ws["D%(row_counter)d"%vars()] = athlete['dob']
              ws["E%(row_counter)d"%vars()] = athlete['club']
              ws["F%(row_counter)d"%vars()] = "<resultat>"
              ws["G%(row_counter)d"%vars()] = "<vind>";  grc = ws["G%(row_counter)d"%vars()]; grc.font=greenfont
              ws["H%(row_counter)d"%vars()] = "<resultat>";  hrc = ws["H%(row_counter)d"%vars()]; hrc.font=greenfont
              ws["I%(row_counter)d"%vars()] = "<vind>";  irc = ws["I%(row_counter)d"%vars()]; irc.font=greenfont
              if 'meter' not in event: # is a field event
                 row_counter +=1 # add blank line for series
                 ws["A%(row_counter)d"%vars()] = "<hopp-/kastserie>";  arc = ws["A%(row_counter)d"%vars()]; arc.font=greenfont
    
              row_counter +=1
           row_counter +=1
           
    
    fname = output_file_name(tree)
    xlname = fname+'.xlsx'
    wb.save(xlname)

# ...
if len(sys.argv) < 2:
   sys.exit("Usage: %s <infile>" % sys.argv[0])
   
infile = sys.argv[1]
#infile = 'NIF'
tree = read_xml_into_tree(infile)
save_xml_copy(tree)

write_xlsx_results_template(tree)
write_start_lists_as_html(tree)
