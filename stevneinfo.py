#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
from xml.etree import ElementTree as ET
from openpyxl import Workbook
from openpyxl.styles import colors as xlcolors
from openpyxl.styles import Font, Color
#from tabulate import tabulate
from reportlab.lib import colors as rlcolors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas


def read_xml_into_tree(infile):
   with open(infile, 'rt') as f:
      tree = ET.parse(f)
   return tree

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

def issteeple(event):
    return istrack(event) and 'hinder' in event

def isfield(event):
    return 'meter' not in event

def isvjump(event):
    return isfield(event.encode('utf-8')) and event in [u'Høyde', u'Stav', u'Høyde uten tilløp']

def ishjump(event):
    return isfield(event.encode('utf-8')) and event in [u'Lengde', u'Lengde satssone', u'Tresteg', u'Lengde uten tilløp', u'Tresteg uten tilløp']

def isthrow(event):
    return isfield(event.encode('utf-8')) and event in [u'Kule', u'Diskos', u'Slegge', u'Spyd', u'Vektkast', u'Liten ball']

def sort_athletes_by_class_by_event(tree):
    athlete_by_class_by_event = {}
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
      
       if event not in athlete_by_class_by_event.keys():
          athlete_by_class_by_event[event]={}
       if klasse not in athlete_by_class_by_event[event].keys():
          athlete_by_class_by_event[event][klasse]=[]
       athlete_by_class_by_event[event][klasse].append({'name': name, 'dob': dob, 'club' : club }) 

    return athlete_by_class_by_event

def sort_athletes_by_event_by_class(tree):
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
    
    of.write("""</body>
    </html>""")
    of.close()


def write_xlsx_results_template(tree):
    competition_data = extract_competition_data(tree)
    mn = competition_data['meet_name']
    md = competition_data['meet_date']
    mv = competition_data['venue']

    athlete_by_event_by_class = sort_athletes_by_event_by_class(tree)

    #... write template for Results to xlsx workbook
    wb = Workbook()
    ws = wb.active
    
    greenfont = Font(name='Calibri', color=xlcolors.GREEN)
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

           if istrack(event):
               ws["A%(row_counter)d"%vars()] = "<Heat | Finale:>";  arc = ws["A%(row_counter)d"%vars()]; arc.font=greenfont
               ws["C%(row_counter)d"%vars()] = "Vind:";  crc = ws["C%(row_counter)d"%vars()]; crc.font=greenfont
               row_counter +=1
          
           for athlete in athlete_by_event_by_class[klasse][event]:
              ws["C%(row_counter)d"%vars()] = athlete['name']
              ws["D%(row_counter)d"%vars()] = athlete['dob']
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
    wb.save(xlname)

def make_horizontal_protocol(tree, event, classes):
    """make the event protocol sheet for a horizontal jump or throw event
    writes the protocol sheet to a pdf
    Input:
    	tree: ElementTree
    	event: the event (fails if event is not a hjump or throw)
 	classes: list of classes """
    if not ishjump(event) and not isthrow(event):
       sys.exit('make_horizontal_protocol: event is not hjump or throw')
    athlete_by_event_by_class = sort_athletes_by_event_by_class(tree)
    athlete_by_class_by_event = sort_athletes_by_class_by_event(tree)
 
    eventclass = event + ' ' + '+'.join(classes)
 
    fname = output_file_name(tree) + '_' + event + '-' + '+'.join(classes) +'.pdf'
    fname = fname.replace(' ', '_')
    fname = fname.replace('/', '-')
    print fname
    doc = SimpleDocTemplate(fname, pagesize=A4)
    doc.pagesize = landscape(A4)
 
    rows_on_page = 10
    # container for the 'Flowable' objects
    elements = []
    
    styles = getSampleStyleSheet()
 
    data= [ ['Klasse', 'Navn', 'F.dato', 'Klubb', 'Forsøk 1', 'Forsøk 2', 'Forsøk 3', 'Forsøk 4', 'Forsøk 5', 'Forsøk 6', 'Resultat'] ]
    if ishjump(event):
       data[0].append('Vind')
 
    rows = 0
    for c in classes:
       if c in athlete_by_class_by_event[event].keys():
          for athlete in athlete_by_class_by_event[event][c]:
             data.append( [ c, athlete['name'], athlete['dob'], athlete['club'] ] )
             rows +=1
    pages = int(rows/(rows_on_page-1)) + 1
    print pages
 
    if rows%rows_on_page > 3:
       pages +=1
    rows_in_table = pages*rows_on_page 
 
    if rows < rows_in_table:
       for i in range(rows_in_table-rows-1):
          data.append([ ' ' ])
 
 
 
    t=Table(data, [1.9*cm, 6.0*cm, 2.1*cm, 2.6*cm , 1.8*cm, 1.8*cm, 1.8*cm, 1.8*cm, 1.8*cm, 1.8*cm, 1.8*cm, 1.8*cm], rows_in_table*[1.4*cm], repeatRows=1)
 
    t.setStyle(TableStyle([('ALIGN',(0,1),(0,-1),'CENTER'),
                           ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
                           ('ALIGN',(1,1),(1,-1),'LEFT'),
                           ('INNERGRID', (0,0), (-1,-1), 0.25, rlcolors.black),
                           ('BOX', (0,0), (-1,-1), 0.25, rlcolors.black),
                           ]))
    elements.append(t)
    # write the document to disk
    doc.build(elements)
# ...
if len(sys.argv) < 2:
   sys.exit("Usage: %s <infile>" % sys.argv[0])
   
infile = sys.argv[1]
tree = read_xml_into_tree(infile)
save_xml_copy(tree)

write_xlsx_results_template(tree)
write_start_lists_as_html(tree)
event = 'Lengde satssone'
classes = [ 'J11', 'J12', 'J13' ]
make_horizontal_protocol(tree, event, classes)
classes = [ 'G11', 'G12', 'G13' ]
make_horizontal_protocol(tree, event, classes)
classes = [ 'G 9', 'G10', 'J 9', 'J10' ]
make_horizontal_protocol(tree, event, classes)
classes = [ 'B6-8' ]
make_horizontal_protocol(tree, event, classes)
event = 'Lengde'
classes = [ 'J15', 'J16', 'J17', 'J18/19', 'MS' ]
make_horizontal_protocol(tree, event, classes)
classes = [ 'G14' ]
make_horizontal_protocol(tree, event, classes)
event = 'Lengde'
classes = [ 'J14' ]
make_horizontal_protocol(tree, event, classes)
event = 'Kule'
classes = [ 'J11', 'J12', 'J13', 'G11' ]
make_horizontal_protocol(tree, event, classes)
classes = [ 'G13', 'J14' ]
make_horizontal_protocol(tree, event, classes)
classes = [ 'G14' ]
make_horizontal_protocol(tree, event, classes)
event = 'Liten ball'
classes = [ 'J 9', 'J10', 'G 9', 'G10' ]
make_horizontal_protocol(tree, event, classes)
