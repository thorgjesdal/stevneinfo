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

import pprint

gender = {'M':'M', 'K':'F', 'G':'M', 'J':'F'}

def istrack(event):
    return 'meter' in event

def ishurdles(event):
    return istrack(event) and 'hekk' in event

def issteeple(event):
    return istrack(event) and 'hinder' in event

def isfield(event):
    #return event in ('HJ', 'PV', 'LJ', 'TJ', 'SHJ', 'SLJ', 'STJ',
    #                 'SP', 'DT', 'HT', 'JT', 'BT', 'OT' )
    return isvjump(event) or ishjump(event) or isthrow(event)

def isvjump(event):
    return event in [u'Høyde', u'Stav', u'Høyde uten tilløp']

def ishjump(event):
    return event in [u'Lengde', u'Lengde satssone', u'Tresteg', u'Lengde uten tilløp', u'Tresteg uten tilløp']

def isthrow(event):
    return event in [u'Kule', u'Diskos', u'Slegge', u'Spyd', u'Vektkast', u'Liten ball']

def ismulti(event):
    return 'kamp' in event

def event_code(event):
    event_codes = {
            u'60 meter'          : '60', 
            u'80 meter'          : '80', 
            u'100 meter'         : '100', 
            u'150 meter'         : '150', 
            u'200 meter'         : '200', 
            u'300 meter'         : '300', 
            u'400 meter'         : '400', 
            u'600 meter'         : '600', 
            u'800 meter'         : '800', 
            u'1000 meter'        : '1000', 
            u'1500 meter'        : '1500', 
            u'3000 meter'        : '3000', 
            u'5000 meter'        : '5000', 
            u'10 000 meter'       : '10000', 
            u'60 meter hekk'     : '60H', 
            u'80 meter hekk'     : '80H', 
            u'100 meter hekk'    : '100H', 
            u'110 meter hekk'    : '110H', 
            u'200 meter hekk'    : '200H', 
            u'300 meter hekk'    : '300H', 
            u'400 meter hekk'    : '400H', 
            u'2000 meter hinder' : '2000SC', 
            u'3000 meter hinder' : '3000SC', 
            u'Kappgang 1000 meter' : '1000W', 
            u'Kappgang 3000 meter' : '3000W', 
            u'Kappgang 5000 meter' : '5000W', 
            u'Kappgang 5 km'     : '5000W', 
            u'Kappgang'          : '1500W', 
            u'Høyde'             : 'HJ', 
            u'Høyde uten tilløp' : 'SHJ', 
            u'Stav'              : 'PV', 
            u'Lengde'            : 'LJ', 
            u'Lengde satssone'   : 'LJ', 
            u'Lengde uten tilløp': 'SLJ', 
            u'Tresteg'           : 'TJ', 
            u'Tresteg satssone'  : 'TJ', 
            u'Tresteg uten tilløp'  : 'STJ', 
            u'Kule'              : 'SP', 
            u'Diskos'            : 'DT', 
            u'Slegge'            : 'HT', 
            u'Spyd'              : 'JT', 
            u'Liten ball'        : 'OT', 
            u'Tikamp'            : 'DEC', 
            u'Sjukamp'           : 'HEP' ,
            u'10-kamp'           : 'DEC' ,
            u'9-kamp'           : 'ENN' ,
            u'7-kamp'           : 'HEP' ,
            u'6-kamp'           : 'HEX' ,
            u'5-kamp'           : 'PEN' ,
            u'4x200 meter stafett' : '4x200' 
            }
    return event_codes.get(event, '')

def cat_code(name):
    cat_codes = {
            u'6 år Fellesklasse' : u'F6' ,
            u'7 år Fellesklasse' : u'F7' ,
            u'Gutter Rekrutt'    : u'G6-7'          , 
            u'Gutter 6 - 7'      : u'G6-7'          , 
            u'Gutter 8'     : u'G8'          , 
            u'Gutter 9'     : u'G9'          , 
            u'Gutter 10'    : u'G10'          , 
            u'Gutter 11'    : u'G11'          , 
            u'Gutter 11-14' : u'G11-14'       , 
            u'Gutter 12'    : u'G12'          , 
            u'Gutter 13'    : u'G13'          , 
            u'Gutter 14'    : u'G14'          , 
            u'Gutter 15'    : u'G15'          , 
            u'Gutter 16'    : u'G16'          , 
            u'Gutter 17'    : u'G17'          , 
            u'Gutter 18/19' : u'G18/19'       , 
            u'Gutter 18-19' : u'G18-19'       , 
            u'Gutter alle klasser' : u'GALLE'       , 
            u'Menn junior'  : u'MJ'           , 
            u'Menn U20'     : u'MU20'         , 
            u'Menn u20'     : u'MU20'         , 
            u'Menn U23'     : u'MU23'         , 
            u'Menn senior'  : u'MS'           , 
            u'Menn alle klasser'  : u'MALLE'           , 
            u'Menn veteraner' : u'MV'         , 
            u'Menn veteran 35-39' : u'MV35'         , 
            u'Menn veteran 40-44' : u'MV40'         , 
            u'Menn veteran 45-49' : u'MV45'         , 
            u'Menn veteran 50-54' : u'MV50'         , 
            u'Menn veteran 55-59' : u'MV55'         , 
            u'Menn veteran 60-64' : u'MV60'         , 
            u'Menn veteran 65-69' : u'MV65'         , 
            u'Menn veteran 70-75' : u'MV70'         , 
            u'Menn veteran 75-79' : u'MV75'         , 
            u'Jenter Rekrutt'    : u'J6-7'          , 
            u'Jenter 6 - 7'     : u'J 6-7'          , 
            u'Jenter 8'     : u'J8'          , 
            u'Jenter 9'     : u'J9'          , 
            u'Jenter 10'    : u'J10'          , 
            u'Jenter 11'    : u'J11'          , 
            u'Jenter 11-14' : u'J11-14'          , 
            u'Jenter 12'    : u'J12'          , 
            u'Jenter 13'    : u'J13'          , 
            u'Jenter 14'    : u'J14'          , 
            u'Jenter 15'    : u'J15'          , 
            u'Jenter 16'    : u'J16'          , 
            u'Jenter 17'    : u'J17'          , 
            u'Jenter 18/19' : u'J18/19'       , 
            u'Jenter 18-19' : u'J18-19'       , 
            u'Jenter alle klasser' : u'JALLE'       , 
            u'Kvinner junior'  : u'KJ'        , 
            u'Kvinner U20'     : u'KU20'      , 
            u'Kvinner u20'     : u'KU20'      , 
            u'Kvinner U23'     : u'KU23'      , 
            u'Kvinner u23'     : u'KU23'      , 
            u'Kvinner senior'  : u'KS'        , 
            u'Kvinner Senior'  : u'KS'        , 
            u'Kvinner alle klasser'  : u'KALLE'           , 
            u'Kvinner veteraner' : u'KV'      ,
            u'Kvinner veteran 35-39' : u'KV35'         , 
            u'Kvinner veteran 40-44' : u'KV40'         , 
            u'Kvinner veteran 45-49' : u'KV45'         , 
            u'Kvinner veteran 50-54' : u'KV50'         , 
            u'Kvinner veteran 55-59' : u'KV55'         , 
            u'Kvinner veteran 60-64' : u'KV60'         , 
            u'Kvinner veteran 65-69' : u'KV65'         , 
            u'Kvinner veteran 70-75' : u'KV70'         , 
            u'Kvinner veteran 75-79' : u'KV75'         , 
            u'Funksjonshemmede' : u'FH'      ,
            u'Ikke valgt klasse' : u'IVK'
            }
#   print(name)
    code = ''
    if name is not None:
        code = cat_codes.get(name.strip(), name.strip())
    return code

def get_gender(cat):
    if cat[0] in ('G', 'M'):
        g = 'M'
    elif cat[0] in ('J', 'K'):
        g = 'F'
    else:
        g = 'MF'
    return g

def age_group(cat):
    age_groups = {
            'F6'    : '6',
            'F7'    : '7',
            'G6-7'    : '6-7',
            'G8'    : '8',
            'G9'    : '9',
            'G10'    : '10',
            'G11'    : '11',
            'G11-14'    : '11-14',
            'G12'    : '12',
            'G13'    : '13',
            'G14'    : '14',
            'G15'    : '15',
            'G16'    : '16',
            'G17'    : '17',
            'G18/19' : '18-19',
            'G18-19' : '18-19',
            'GALLE' : 'ALL',
            'MJ'     : 'U20' ,
            'MU20'     : 'U20' ,
            'MU23'     : 'U23' ,
            'MS'     : 'SEN' ,
            'MALLE'     : 'ALL' ,
            'MV'     : 'V35' ,
            'MV35'   : 'V35' ,
            'MV40'   : 'V40' ,
            'MV45'   : 'V45' ,
            'MV50'   : 'V50' ,
            'MV55'   : 'V55' ,
            'MV60'   : 'V60' ,
            'MV65'   : 'V65' ,
            'MV70'   : 'V70' ,
            'MV75'   : 'V75' ,
            'J6-7'    : '6-7',
            'J8'    : '8',
            'J9'    : '9',
            'J10'    : '10',
            'J11'    : '11',
            'J11-14'    : '11-14',
            'J12'    : '12',
            'J13'    : '13',
            'J14'    : '14',
            'J15'    : '15',
            'J16'    : '16',
            'J17'    : '17',
            'J18/19' : '18-19',
            'J18-19' : '18-19',
            'JALLE' : 'ALL',
            'KJ'     : 'U20',
            'KU20'     : 'U20' ,
            'KU23'     : 'U23' ,
            'KS'     : 'SEN' ,
            'KV'     : 'V35' ,
            'KV35'   : 'V35' ,
            'KV40'   : 'V40' ,
            'KV45'   : 'V45' ,
            'KV50'   : 'V50' ,
            'KV55'   : 'V55' ,
            'KV60'   : 'V60' ,
            'KV65'   : 'V65' ,
            'KV70'   : 'V70' ,
            'KV75'   : 'V75' ,
            'KALLE'     : 'ALL' ,
            'FH'   : 'ALL' ,
            'IVK'    : 'ALL'  
            }
    return age_groups.get(cat, cat)

def event_spec(event, klasse):
    throws = {}
    throws['Kule'] = { 'J10' : '2,0kg', 'J11' : '2,0kg', 'J12' : '2,0kg', 'J13' : '2,0kg', 
                       'J14' : '3,0kg', 'J15' : '3,0kg', 'J16' : '3,0kg', 'J17' : '3,0kg',
                       'J18/19' : '4,0kg', 'KU20' : '4,0kg', 'KU23' : '4,0kg', 'KS' : '4,0kg', 
                       'G10' : '2,0kg', 'G11' : '2,0kg', 'G12' : '3,0kg', 'G13' : '3,0kg', 
                       'G14' : '4,0kg', 'G15' : '4,0kg', 'G16' : '5,0kg', 'G17' : '5,0kg',
                       'G18/19' : '6,0kg', 'MU20' : '6,0kg', 'MU23' : '7,26kg', 'MS' : '7,26kg', 
                       'default' : ''} 
    throws['Diskos'] = { 'J10' : '0,6kg', 'J11' : '0,6kg', 'J12' : '0,6kg', 'J13' : '0,6kg', 
                       'J14' : '0,75kg', 'J15' : '0,75kg', 'J16' : '0,75kg', 'J17' : '0,75kg',
                       'J18/19' : '1,0kg', 'KU20' : '1,0kg', 'KU23' : '1,0kg', 'KS' : '1,0kg', 
                       'G10' : '0,6kg', 'G11' : '0,6kg', 'G12' : '0,75kg', 'G13' : '0,75kg', 
                       'G14' : '1,0kg', 'G15' : '1,0kg', 'G16' : '1,5kg', 'G17' : '1,5kg',
                       'G18/19' : '1,75kg', 'MU20' : '1,75kg', 'MU23' : '2,0kg', 'MS' : '2,0kg',
                       'default': ''} 
    throws['Slegge'] = { 'J10' : '2,0kg', 'J11' : '2,0kg', 'J12' : '2,0kg', 'J13' : '2,0kg', 
                       'J14' : '3,0kg', 'J15' : '3,0kg', 'J16' : '3,0kg', 'J17' : '3,0kg',
                       'J18/19' : '4,0kg', 'KU20' : '4,0kg', 'KU23' : '4,0kg', 'KS' : '4,0kg', 
                       'G10' : '2,0kg', 'G11' : '2,0kg', 'G12' : '3,0kg', 'G13' : '3,0kg', 
                       'G14' : '4,0kg', 'G15' : '4,0kg', 'G16' : '5,0kg', 'G17' : '5,0kg',
                       'G18/19' : '6,0kg', 'MU20' : '6,0kg', 'MU23' : '7,26kg', 'MS' : '7,26kg',
                       'default': ''} 
    throws['Spyd'] = { 'J10' : '400g', 'J11' : '400g', 'J12' : '400g', 'J13' : '400g', 
                       'J14' : '400g', 'J15' : '500g', 'J16' : '500g', 'J17' : '500g',
                       'J18/19' : '600g', 'KU20' : '600g', 'KU23' : '600g', 'KS' : '600g', 
                       'G10' : '400g', 'G11' : '400g', 'G12' : '400g', 'G13' : '400g', 
                       'G14' : '600g', 'G15' : '600g', 'G16' : '700g', 'G17' : '700g',
                       'G18/19' : '800g', 'MU20' : '800g', 'MU23' : '800g', 'MS' : '800g',
                       'default': ''} 
#    throws['Liten ball'] = { 'J10' : '150g', 'J11' : '150g', 'J12' : '150g', 'J13' : '150g', 'J14' : '150g', 
#                             'G10' : '150g', 'G11' : '150g', 'G12' : '150g', 'G13' : '150g', 'G14' : '150g' 
#                             }
    throws['Liten ball'] = defaultdict(lambda : '150g') 
    hurdles = {}
    hurdles['60 meter hekk'] = { 'J10' : '68,0cm', 'J11' : '68,0cm', 'J12' : '76,2cm', 'J13' : '76,2cm', 'J14' : '76,2cm',
                                 'J15' : '76,2cm', 'J16' : '76,2cm', 'J17' : '76,2cm',
                                 'J18/19' : '84,0cm','KJ' : '84,0cm','KU20' : '84,0cm', 'KU23' : '84,0cm', 'KS' : '84,0cm',
                                 'G10' : '68,0cm', 'G11' : '68,0cm', 'G12' : '76,2cm', 'G13' : '76,2cm', 'G14' : '84,0cm',
                                 'G15' : '84,0cm', 'G16' : '91,4cm', 'G17' : '91,4cm',
                                 'G18/19' : '100cm','MU20' : '100cm', 'MU23' : '106,7cm', 'MS' : '106,7cm', 'default':'' }
    hurdles['80 meter hekk'] = { 'J15' : '76,2cm', 'J16' : '76,2cm', 'G14' : '84,0cm' } 
    hurdles['100 meter hekk'] = { 'J16' : '76,2cm', 'J17' : '76,2cm', 'J18/19' : '84,0cm','KJ' : '84,0cm','KU20' : '84,0cm', 'KU23' : '84,0cm', 'KS' : '84,0cm',
                                 'G15' : '84,0cm', 'G16' : '91,4cm'}

    hurdles['110 meter hekk'] = { 'G17' : '91,4cm', 'G18/19' : '100cm','MJ' : '100cm', 'MU20' : '100cm', 'MU23' : '106,7cm', 'MS' : '106,7cm' }
    hurdles['200 meter hekk'] = { 'J10' : '68,0cm', 'J11' : '68,0cm', 'J12' : '68,0cm', 'J13' : '68,0cm', 'J14' : '76,2cm',
                                 'J15' : '76,2cm', 'J16' : '76,2cm', 'J17' : '76,2cm',
                                 'J18/19' : '76,2cm','KJ' : '76,2cm','KU20' : '76,2cm', 'KU23' : '76,2cm', 'KS' : '76,2cm',
                                 'G10' : '68,0cm', 'G11' : '68,0cm', 'G12' : '68,0cm', 'G13' : '68,0cm', 'G14' : '76,2cm',
                                 'G15' : '76,2cm', 'G16' : '76,2cm', 'G17' : '76,2cm',
                                 'G18/19' : '76,2cm','MJ' : '76,2cm', 'MU20' : '76,2cm', 'MU23' : '76,2cm', 'MS' : '76,2cm' }
    hurdles['300 meter hekk'] = { 'J15' : '76,2cm', 'J16' : '76,2cm', 'J17' : '76,2cm',
                                 'J18/19' : '76,2cm','KJ' : '76,2cm','KU20' : '76,2cm', 'KU23' : '76,2cm', 'KS' : '76,2cm',
                                 'G15' : '76,2cm', 'G16' : '84,0cm', 'G17' : '84,0cm',
                                 'G18/19' : '91,4cm','MJ' : '91,4cm', 'MU20' : '91,4cm', 'MU23' : '91,4cm', 'MS' : '91,4cm' }
    hurdles['400 meter hekk'] = { 'J15' : '76,2cm', 'J16' : '76,2cm', 'J17' : '76,2cm',
                                 'J18/19' : '76,2cm','KJ' : '76,2cm','KU20' : '76,2cm', 'KU23' : '76,2cm', 'KS' : '76,2cm',
                                 'G15' : '76,2cm', 'G16' : '84,0cm', 'G17' : '84,0cm',
                                 'G18/19' : '91,4cm','MJ' : '91,4cm','MU20' : '91,4cm', 'MU23' : '91,4cm', 'MS' : '91,4cm' }

    if isthrow(event):
       #e = event + ' ' + throws[event][klasse]
       t = throws[event].get(klasse,None)
       if t == None:
           t = throws[event]['default']
       e = event + ' ' + t
    elif ishurdles(event):
       h = hurdles[event].get(klasse,None)
       if h == None:
           h = hurdles[event]['default']
       e = event + ' ' + h
    else:
       e = event

    return e


def club_code(club_name):
    if club_name is None:
       club_code=u''
    elif club_name in (u'ÅLEN IDRETTSLAG'):
       club_code=u'AALEN'
    elif club_name in (u'Ålesund Friidrettsklubb', u'Ålesund FIK'):
       club_code=u'AASUN'
    elif club_name in (u'Adamstuen Løpeklubb'):
       club_code=u'ADAMS'
    elif club_name in (u'Allianseidrettslaget Ik Våg'):
       club_code=u'IKV'
    elif club_name in (u'Almenning Il'):
       club_code=u'ALM'
    elif club_name in (u'Alsvåg Idrettslag'):
       club_code=u'ALSV'
    elif club_name in (u'Alta Idrettsforening'):
       club_code=u'ALTA'
    elif club_name in (u'Åndalsnes Idrettsforening'):
       club_code=u'ANDAL'
    elif club_name in (u'Andebu Idrettslag'):
       club_code=u'ANDE'
    elif club_name in (u'Andørja Sportsklubb'):
       club_code=u'ANDSK'
    elif club_name in (u'Aremark Idrettsforening', u'Aremark IF'):
       club_code=u'ARE'
    elif club_name in (u'Arna Turn & Idrettslag'):
       club_code=u'ARNA'
    elif club_name in (u'Ås Idrettslag', u'Ås IL'):
       club_code=u'ASIL'
    elif club_name in (u'Åsen Idrettslag'):
       club_code=u'AASEN'
    elif club_name in (u'Åseral idrettslag'):
       club_code=u'AASER'
    elif club_name in (u'Ask Friidrett'):
       club_code=u'ASK'
    elif club_name in (u'Asker Fleridrettslag'):
       club_code=u'ASKFL'
    elif club_name in (u'Asker Skiklubb', u'Asker Sk. Friidrett'):
       club_code=u'ASKSK'
    elif club_name in (u'Askim Idrettsforening', u'Askim IF'):
       club_code=u'ASKIM'
    elif club_name in (u'Atna Idrettslag'):
       club_code=u'ATNA'
    elif club_name in (u'Aure Idrettslag'):
       club_code=u'AURE'
    elif club_name in (u'Aurland Idrettslag'):
       club_code=u'AURL'
    elif club_name in (u'Aurskog-Høland Friidrettslag', u'Aurskog - Høland Friidrettslag - Friidrett'):
       club_code=u'AURS'
    elif club_name in (u'Austefjord Idrettslag'):
       club_code=u'AUFJ'
    elif club_name in (u'Austevoll Idrettsklubb'):
       club_code=u'AUST'
    elif club_name in (u'Austrheim Idrettslag'):
       club_code=u'AUSTR'
    elif club_name in (u'Bagn Idrettslag'):
       club_code=u'BAGN'
    elif club_name in (u'Bakke IF'):
       club_code=u'BAKKE'
    elif club_name in (u'Balestrand Idrettslag', u'Balestrand IL'):
       club_code=u'BALE'
    elif club_name in (u'Bardu Idrettslag'):
       club_code=u'BARD'
    elif club_name in (u'Båtsfjord Sportsklubb'):
       club_code=u'BTSFJ'
    elif club_name in (u'Begnadalen Idrettslag'):
       club_code=u'BGND'
    elif club_name in (u'Beitstad Idrettslag'):
       club_code=u'BEIT'
    elif club_name in (u'Bergen Cykleklubb'):
       club_code=u'BCK'
    elif club_name in (u'Bergen Triathlon Club'):
       club_code=u'BTC'
    elif club_name in (u'Bergens Turnforening', u'Bergens TF'):
       club_code=u'BTU'
    elif club_name in (u'Berger Idrettslag'):
       club_code=u'BERGE'
    elif club_name in (u'BFG Bergen Løpeklubb'):
       club_code=u'BFGL'
    elif club_name in (u'Bjerkreim Idrettslag'):
       club_code=u'BJERR'
    elif club_name in (u'Bjerkvik Idrettsforening'):
       club_code=u'BJERV'
    elif club_name in (u'Blaker IL'):
       club_code=u'BLA'
    elif club_name in (u'Blefjell Idrettslag'):
       club_code=u'BLEFJ'
    elif club_name in (u'Bodø & Omegn IF Friidrett'):
       club_code=u'BODO'
    elif club_name in (u'Bodø Bauta Løpeklubb'):
       club_code=u'BODL'
    elif club_name in (u'Bodø Friidrettsklubb'):
       club_code=u'BODF'
    elif club_name in (u'Bokn Idrettslag'):
       club_code=u'BOKN'
    elif club_name in (u'Bossekop Ungdomslag'):
       club_code=u'BOS'
    elif club_name in (u'Botnan Idrettslag'):
       club_code=u'BOTNA'
    elif club_name in (u'Botne Skiklubb'):
       club_code=u'BOT'
    elif club_name in (u'Brandbu Idretsforening', u'Brandbu IF'):
       club_code=u'BRNDB'
    elif club_name in (u'Bratsberg Idrettslag'):
       club_code=u'BRATS'
    elif club_name in (u'Brattvåg Idrettslag'):
       club_code=u'BRATTV'
    elif club_name in (u'Breimsbygda IL'):
       club_code=u'BREIM'
    elif club_name in (u'Brekke Idrettslag'):
       club_code=u'BREKK'
    elif club_name in (u'Bremanger Idrettslag'):
       club_code=u'BREMA'
    elif club_name in (u'Bremnes Idrettslag'):
       club_code=u'BREM'
    elif club_name in (u'Brevik Idrettslag'):
       club_code=u'BRE'
    elif club_name in (u'Bromma Idrettslag'):
       club_code=u'BROMM'
    elif club_name in (u'Bryne Friidrettsklubb'):
       club_code=u'BRYF'
    elif club_name in (u'BRYNE TRIATLONKLUBB'):
       club_code=u'BRYT'
    elif club_name in (u'Bud Idrettslag'):
       club_code=u'BUD'
    elif club_name in (u'Byaasen Skiklub'):
       club_code=u'BYS'
    elif club_name in (u'Byåsen Idrettslag'):
       club_code=u'BYI'
    elif club_name in (u'Byneset IL Hovedlaget'):
       club_code=u'BYN'
    elif club_name in (u'Bøler IF'):
       club_code=u'BIF'
    elif club_name in (u'Bækkelagets SK', u'Bækkelagets Sportsklub'):
       club_code=u'BSK'
    elif club_name in (u'Bærums Verk Hauger Idrettsforening'):
       club_code=u'BRVHA'
    elif club_name in (u'Bæverfjord Idrettslag'):
       club_code=u'BVRFJ'
    elif club_name in (u'Bøler Idrettsforening'):
       club_code=u'BIF'
    elif club_name in (u'Bømlo Idrettslag'):
       club_code=u'BMLO'
    elif club_name in (u'Børsa Idrettslag', u'Børsa IL'):
       club_code=u'BRSA'
    elif club_name in (u'Dale Idrettslag'):
       club_code=u'DALE'
    elif club_name in (u'Dalen Idrettslag'):
       club_code=u'DLN'
    elif club_name in (u'Dimna IL'):
       club_code=u'DIM'
    elif club_name in (u'Dombås Idrettslag'):
       club_code=u'DMB'
    elif club_name in (u'Driv Idrettslag', u'Driv Idrettslag - Friidrett ' ):
       club_code=u'DRIV'
    elif club_name in (u'Driva IL'):
       club_code=u'DRIVA'
    elif club_name in (u'Drøbak-Frogn Idrettslag', u'Drøbak-Frogn IL'):
       club_code=u'DRFR'
    elif club_name in (u'Dypvåg Idrettsforening'):
       club_code=u'DPVG'
    elif club_name in (u'Egersunds Idrettsklubb'):
       club_code=u'EGRSU'
    elif club_name in (u'Eid Idrettslag'):
       club_code=u'EIDIL'
    elif club_name in (u'Eidanger Idrettslag'):
       club_code=u'EIDA'
    elif club_name in (u'Eidfjord Idrettslag'):
       club_code=u'EIDF'
    elif club_name in (u'Eidsberg Idrettslag'):
       club_code=u'EIDSB'
    elif club_name in (u'Eidsvåg Idrettslag'):
       club_code=u'EIDS'
    elif club_name in (u'Eidsvold Turnforening Friidrett'):
       club_code=u'EIDTU'
    elif club_name in (u'Eikanger Idrettslag'):
       club_code=u'EIK'
    elif club_name in (u'Ekeberg Sports Klubb'):
       club_code=u'ESK'
    elif club_name in (u'Espa Idrettslag'):
       club_code=u'ESPA'
    elif club_name in (u'Etne Idrettslag'):
       club_code=u'ETNE'
    elif club_name in (u'Fagernes Idrettslag N'):
       club_code=u'FAGIL'
    elif club_name in (u'Fagernes Idrettslag O', u'Fagernes IL'):
       club_code=u'FAG'
    elif club_name in (u'Falkeid idrettslag'):
       club_code=u'FALK'
    elif club_name in (u'Fana Idrettslag', u'Fana IL'):
       club_code=u'FANA'
    elif club_name in (u'Feiring Idrettslag'):
       club_code=u'FEIR'
    elif club_name in (u'Fet Friidrettsklubb'):
       club_code=u'FET'
    elif club_name in (u'FIL AKS-77'):
       club_code=u'FA77'
    elif club_name in (u'Finnøy Idrettslag'):
       club_code=u'FINNY'
    elif club_name in (u'Fiskå Idrettsforening'):
       club_code=u'FISIF'
    elif club_name in (u'Fiskå Idrettslag', u'Fiskå IL'):
       club_code=u'FISIL'
    elif club_name in (u'Fitjar Idrettslag'):
       club_code=u'FITJ'
    elif club_name in (u'Fjellhug/Vereide IL'):
       club_code=u'FJVE'
    elif club_name in (u'Flatås Idrettslag'):
       club_code=u'FLATS'
    elif club_name in (u'Florø Turn og Idrettsforening', u'Florø T og IF', u'Florø T&IF'):
       club_code=u'FLOR'
    elif club_name in (u'Follafoss Idrettslag'):
       club_code=u'FOLFO'
    elif club_name in (u'Folldal Idrettsforening'):
       club_code=u'FOL'
    elif club_name in (u'Follo Løpeklubb'):
       club_code=u'FOLLO'
    elif club_name in (u'Forra Idrettslag'):
       club_code=u'FORRA'
    elif club_name in (u'Fossum Idrettsforening', u'Fossum IF'):
       club_code=u'FOSSU'
    elif club_name in (u'Fredrikstad Idrettsforening', u'Fredrikstad IF'):
       club_code=u'FRED'
    elif club_name in (u'Freidig Sportsklubben'):
       club_code=u'FREI'
    elif club_name in (u'Friidretsklubben Orion', u'FIK Orion'):
       club_code=u'ORION'
    elif club_name in (u'Friidrettsklubben Ren-Eng'):
       club_code=u'REN'
    elif club_name in (u'Friidrettslaget Bamse'):
       club_code=u'BAMSE'
    elif club_name in (u'Friidrettslaget Borg'):
       club_code=u'BORG'
    elif club_name in (u'Friidrettslaget Frisk'):
       club_code=u'FRISK'
    elif club_name in (u'Frognerparken Idrettslag'):
       club_code=u'FRO'
    elif club_name in (u'Frol Idrettslag'):
       club_code=u'FROL'
    elif club_name in (u'Frosta Idrettslag'):
       club_code=u'FROSTA'
    elif club_name in (u'Frøyland Idrettslag'):
       club_code=u'FRLND'
    elif club_name in (u'Furuset Allidrett IF'):
       club_code=u'FUR'
    elif club_name in (u'Fyllingen Idrettslag'):
       club_code=u'FYLL'
    elif club_name in (u'Førde Idrettslag', u'Førde IL'):
       club_code=u'FRDE'
    elif club_name in (u'Gaular IL'):
       club_code=u'GAULA'
    elif club_name in (u'Gausdal Friidrettsklubb'):
       club_code=u'GAU'
    elif club_name in (u'Geilo Idrettslag'):
       club_code=u'GEI'
    elif club_name in (u'Geiranger Idrettslag'):
       club_code=u'GEIR'
    elif club_name in (u'Gjerpen Idrettsforening'):
       club_code=u'GJER'
    elif club_name in (u'Gjerstad Idrettslag'):
       club_code=u'GJERS'
    elif club_name in (u'Gjesdal Idrettslag' , 'Gjesdal IL'):
       club_code=u'GJDAL'
    elif club_name in (u'Gjøvik Friidrettsklubb'):
       club_code=u'GJFK'
    elif club_name in (u'Gjøvik Friidrettsklubb 2'):
       club_code=u'GJVIK'
    elif club_name in (u'Gloppen Friidrettslag'):
       club_code=u'GLO'
    elif club_name in (u'Gol Idrettslag'):
       club_code=u'GOL'
    elif club_name in (u'Grong Idrettslag'):
       club_code=u'GRON'
    elif club_name in (u'Groruddalen Friidrettsklubb'):
       club_code=u'GRO'
    elif club_name in (u'Grue Idrettslag'):
       club_code=u'GRUE'
    elif club_name in (u'GTI Friidrettsklubb', u'GTI Friidrettsklubb - gr.  '):
       club_code=u'GTI'
    elif club_name in (u'Gui Sportsklubb - Friidrett'):
       club_code=u'GUI'
    elif club_name in (u'Gulset Idrettsforening'):
       club_code=u'GUL'
    elif club_name in (u'HAB IL'):
       club_code=u'HAB'
    elif club_name in (u'Hadeland Friidrettsklubb'):
       club_code=u'HADE'
    elif club_name in (u'Haga Idrettsforening '):
       club_code=u'HAGA'
    elif club_name in (u'Halden Idrettslag', u'Halden IL'):
       club_code=u'HAL'
    elif club_name in (u'Halmsås & Omegn Skilag'):
       club_code=u'HALMO'
    elif club_name in (u'Halsa Idrettslag'):
       club_code=u'HALSA'
    elif club_name in (u'Hamar Idrettslag Hovedlaget', u'Hamar IL'):
       club_code=u'HIL'
    elif club_name in (u'Hannevikas Idrettslag'):
       club_code=u'HANNEV'
    elif club_name in (u'Hardbagg Idrettslag'):
       club_code=u'HARDB'
    elif club_name in (u'Hareid Idrettslag'):
       club_code=u'HAREI'
    elif club_name in (u'Harestua Idrettslag'):
       club_code=u'HARE'
    elif club_name in (u'Hattfjelldal Idrettslag', u'Hattfjelldal IL'):
       club_code=u'HATT'
    elif club_name in (u'Haugen Idrettslag'):
       club_code=u'HAUGN'
    elif club_name in (u'Haugerud Idrettsforening'):
       club_code=u'HAUGR'
    elif club_name in (u'Haugesund Idrettslag Friidrett', u'Haugesund Idrettslag Friidrett - gr'):
       club_code=u'HAUGF'
    elif club_name in (u'Haugesund Triathlon Klubb'):
       club_code=u'HAUGT'
    elif club_name in (u'Havørn Allianseidrettslag'):
       club_code=u'HAV'
    elif club_name in (u'Heggedal Friidrettsklubb'):
       club_code=u'HEGGF'
    elif club_name in (u'Heggedal Idrettslag'):
       club_code=u'HEGGI'
    elif club_name in (u'Hell Ultraløperklubb'):
       club_code=u'HELLU'
    elif club_name in (u'Heming Idrettslaget', u'IL Heming'):
       club_code=u'HEM'
    elif club_name in (u'Henning I L'):
       club_code=u'HENN'
    elif club_name in (u'Herand Idrettslag'):
       club_code=u'HERA'
    elif club_name in (u'Herkules Friidrett'):
       club_code=u'HERK'
    elif club_name in (u'Herøy Idrettslag'):
       club_code=u'HERY'
    elif club_name in (u'Hinna Friidrett'):
       club_code=u'HIN'
    elif club_name in (u'Hitra Friidrettsklubb'):
       club_code=u'HITF'
    elif club_name in (u'Hitra Løpeklubb'):
       club_code=u'HITL'
    elif club_name in (u'Hobøl Idrettslag'):
       club_code=u'HOB'
    elif club_name in (u'Hof Idrettslag'):
       club_code=u'HOF'
    elif club_name in (u'Hol Idrettslag'):
       club_code=u'HOL'
    elif club_name in (u'Holmemstranda Idrettslag'):
       club_code=u'HOLMS'
    elif club_name in (u'Holum Idrettslag'):
       club_code=u'HOLUM'
    elif club_name in (u'Hommelvik Idrettslag', u'Hommelvik IL'):
       club_code=u'HMLV'
    elif club_name in (u'Hope Idrettslag'):
       club_code=u'HOPE'
    elif club_name in (u'Hornindal Idrettslag'):
       club_code=u'HORNI'
    elif club_name in (u'Horten Friidrettsklubb'):
       club_code=u'HORFR'
    elif club_name in (u'Huglo Idrettslag'):
       club_code=u'HUG'
    elif club_name in (u'Hurdal Idrettslag'):
       club_code=u'HURD'
    elif club_name in (u'Hvam Idrettslag', u'Hvam IL'):
       club_code=u'HVAM'
    elif club_name in (u'Hvittingfoss Idrettslag'):
       club_code=u'HVFO'
    elif club_name in (u'Hyen Idrettslag'):
       club_code=u'HYEN'
    elif club_name in (u'Hyllestad Idrettslag'):
       club_code=u'HYLLS'
    elif club_name in (u'Høybråten og Stovner IL'):
       club_code=u'HSI'
    elif club_name in (u'Høydalsmo Idrottslag'):
       club_code=u'HDMO'
    elif club_name in (u'I.l Fjellørnen'):
       club_code=u'FJELLO'
    elif club_name in (u'I.L. Framsteg'):
       club_code=u'FRAMS'
    elif club_name in (u'I.L. Norna Salhus', u'Norna-Salhus IL'):
       club_code=u'NORSA'
    elif club_name in (u'I.L. Nybrott'):
       club_code=u'NYBR'
    elif club_name in (u'Idd Sportsklubb'):
       club_code=u'IDD'
    elif club_name in (u'Idrettsforeningen Birkebeineren'):
       club_code=u'BIRK'
    elif club_name in (u'Idrettsforeningen Fram'):
       club_code=u'FRAM'
    elif club_name in (u'Idrettsforeningen Hellas', u'IF Hellas'):
       club_code=u'HELLA'
    elif club_name in (u'Idrettsforeningen Njaal'):
       club_code=u'NJAAL'
    elif club_name in (u'Idrettsforeningen Sturla', u'Sturla IF'):
       club_code=u'STUR'
    elif club_name in (u'Idrettsforeningen Ørn'):
       club_code=u'IFORN'
    elif club_name in (u'Idrettslaget Bjarg'):
       club_code=u'BJARG'
    elif club_name in (u'Idrettslaget Bjørn'):
       club_code=u'ILBJ'
    elif club_name in (u'Idrettslaget Dalebrand'):
       club_code=u'DLBR'
    elif club_name in (u'Idrettslaget Dyre Vaa'):
       club_code=u'DYREV'
    elif club_name in (u'Idrettslaget Express'):
       club_code=u'EXPR'
    elif club_name in (u'Idrettslaget Forsøk'):
       club_code=u'FORSK'
    elif club_name in (u'Idrettslaget Fri'):
       club_code=u'FRI'
    elif club_name in (u'Idrettslaget Gneist' u'IL Gneist'):
       club_code=u'GNE'
    elif club_name in (u'Idrettslaget Holeværingen'):
       club_code=u'HOLE'
    elif club_name in (u'Idrettslaget I Bondeungdomslaget I Tromsø'):
       club_code=u'BULT'
    elif club_name in (u'Idrettslaget Ilar'):
       club_code=u'ILAR'
    elif club_name in (u'Idrettslaget Ivrig'):
       club_code=u'IVRIG'
    elif club_name in (u'Idrettslaget Jardar', u'IL Jardar'):
       club_code=u'JARD'
    elif club_name in (u'IL Jutul', u'Idrettslaget Jutul'):
       club_code=u'JUT'
    elif club_name in (u'Idrettslaget Ros'):
       club_code=u'ILROS'
    elif club_name in (u'Idrettslaget Runar', u'IL Runar'):
       club_code=u'RUNAR'
    elif club_name in (u'Idrettslaget Sand'):
       club_code=u'ILSAN'
    elif club_name in (u'Idrettslaget Sandvin', u'IL Sandvin'):
       club_code=u'SANDV'
    elif club_name in (u'Idrettslaget Skade'):
       club_code=u'SKADE'
    elif club_name in (u'Idrettslaget Skjalg'):
       club_code=u'SKJA'
    elif club_name in (u'Idrettslaget Syril'):
       club_code=u'SYR'
    elif club_name in (u'Idrettslaget Trysilgutten'):
       club_code=u'TRY'
    elif club_name in (u'Idrottslaget Gular Bygdeungdomen I Bergen', u'IL Gular', u'Idrottslaget Gular'):
       club_code=u'GULA'
    elif club_name in (u'IDROTTSLAGET I BUL', u'IL i BUL'):
       club_code=u'ILBUL'
#   elif club_name in (u'IDROTTSLAGET I BUL 2'):
#      club_code=u'ILBUL'
    elif club_name in (u'Idrottslaget Jotun', u'Jotun IL', u'Jotun'):
       club_code=u'JOT'
    elif club_name in (u'Idun Idrettslag'):
       club_code=u'IDUN'
    elif club_name in (u'IF Eiker-Kvikk', u'If Eiker Kvikk'):
       club_code=u'EIKKV'
    elif club_name in (u'IF Kamp/Vestheim', u'Kamp/Vestheim IF'):
       club_code=u'KAVE'
    elif club_name in (u'If Klypetussen'):
       club_code=u'KLYP'
    elif club_name in (u'Ik Grane Arendal Friidrett'):
       club_code=u'GRANE'
    elif club_name in (u'IK Hind', u'IK Hind '):
       club_code=u'HIND'
    elif club_name in (u'Ikornnes Idrettslag'):
       club_code=u'IKORN'
    elif club_name in (u'IL Aasguten'):
       club_code=u'AASG'
    elif club_name in (u'IL Alvidra'):
       club_code=u'ALVI'
    elif club_name in (u'IL Bever`n'):
       club_code=u'ILBEV'
    elif club_name in (u'IL Brodd'):
       club_code=u'BRODD'
    elif club_name in (u'IL Flåværingen, 'u'Flåværingen IL '):
       club_code=u'FLV'
    elif club_name in (u'IL Gry'):
       club_code=u'GRY'
    elif club_name in (u'IL Norodd'):
       club_code=u'ILNOR'
    elif club_name in (u'IL Pioner Friidrett'):
       club_code=u'PIO'
    elif club_name in (u'IL Polarstjernen'):
       club_code=u'POL'
    elif club_name in (u'IL Samhald'):
       club_code=u'SAMH'
    elif club_name in (u'IL Santor'):
       club_code=u'SANT'
    elif club_name in (u'IL Stålkameratene'):
       club_code=u'STKAM'
    elif club_name in (u'IL Tambarskjelvar'):
       club_code=u'TAMBA'
    elif club_name in (u'IL Triumf'):
       club_code=u'TRIUM'
    elif club_name in (u'Vestby IL'):
       club_code=u'VESTB'
    elif club_name in (u'Il Vindbjart'):
       club_code=u'VIND'
    elif club_name in (u'IL Vinger'):
       club_code=u'VING'
    elif club_name in (u'Inderøy Idrettslag'):
       club_code=u'INDRY'
    elif club_name in (u'Innstranda IL'):
       club_code=u'INN'
    elif club_name in (u'International School of Stavanger'):
       club_code=u'INSTA'
    elif club_name in (u'Isfjorden Idrettslag'):
       club_code=u'ISFJO'
    elif club_name in (u'Jondalen Idrettslag'):
       club_code=u'JOND'
    elif club_name in (u'Jægervatnet Idrettslag'):
       club_code=u'JVTN'
    elif club_name in (u'Jøa Idrettslag'):
       club_code=u'JIL'
    elif club_name in (u'Jølster Idrettslag', u'Jølster IL'):
       club_code=u'JLSTE'
    elif club_name in (u'Kaupanger Idrettslag'):
       club_code=u'KAUP'
    elif club_name in (u'Kfum-kameratene Oslo'):
       club_code=u'KFUM'
    elif club_name in (u'Kjelsås Idrettslag', u'Kjelsås IL'):
       club_code=u'KJ'
    elif club_name in (u'Klepp Idrettslag'):
       club_code=u'KLPP'
    elif club_name in (u'Klæbu Løpeklubb'):
       club_code=u'KLK'
    elif club_name in (u'Kløfta Idrettslag'):
       club_code=u'KLIL'
    elif club_name in (u'Kolbukameratene I L'):
       club_code=u'KLBK'
    elif club_name in (u'Koll Idrettslaget', u'IL Koll', u'Koll, Idrettslaget'):
       club_code=u'KOLL'
    elif club_name in (u'Kolvereid Idrettslag'):
       club_code=u'KLVIL'
    elif club_name in (u'Kongsberg Idrettsforening', u'Kongsberg IF'):
       club_code=u'KNGSB'
    elif club_name in (u'Kongsvinger IL Friidrett'):
       club_code=u'KNGSV'
    elif club_name in (u'Konnerud IL Friidrett'):
       club_code=u'KONN'
    elif club_name in (u'Kopervik Idrettslag'):
       club_code=u'KOP'
    elif club_name in (u'Korgen Idrettslag'):
       club_code=u'KORG'
    elif club_name in (u'Kragerø IF Friidrett'):
       club_code=u'KRAG'
    elif club_name in (u'Kråkerøy Idrettslag'):
       club_code=u'KRAAK'
    elif club_name in (u'Kråkstad Idrettslag'):
       club_code=u'KRSTD'
    elif club_name in (u'Kristiansand Løpeklubb'):
       club_code=u'KRL'
    elif club_name in (u'Kristiansands Idrettsforening Friidrett', u'Kristiansands IF'):
       club_code=u'KIF'
    elif club_name in (u'Krødsherad Idrettslag'):
       club_code=u'KRHER'
    elif club_name in (u'Kvinesdal Idrettslag'):
       club_code=u'KVINES'
    elif club_name in (u'Kvæfjord Idrettslag'):
       club_code=u'KVFJ'
    elif club_name in (u'Kyrksæterøra Idrettslag Kil'):
       club_code=u'KYRK'
    elif club_name in (u'Laksevåg Turn og Idrettslag', u'Laksevåg TIL'):
       club_code=u'LAKS'
    elif club_name in (u'Lalm Idrettslag'):
       club_code=u'LALM'
    elif club_name in (u'Lambertseter IF', u'Lambertseter Idrettsforening'):
       club_code=u'LAM'
    elif club_name in (u'Langesund Sykle- og triathlonklubb'):
       club_code=u'LANGS'
    elif club_name in (u'Lånke Idrettslag'):
       club_code=u'LNKEIL'
    elif club_name in (u'Larvik Turn & Idrettsforening', u'Larvik Turn & IF',u'Larvik Turn og Idrettsforening'):
       club_code=u'LRVK'
    elif club_name in (u'Leinstrand Idrettslag'):
       club_code=u'LEINS'
    elif club_name in (u'Lena Idrettsforening'):
       club_code=u'LENA'
    elif club_name in (u'Lierne Idrettslag'):
       club_code=u'LIERN'
    elif club_name in (u'Lillehammer Idrettsforening', u'Lillehammer IF'):
       club_code=u'LIF'
    elif club_name in (u'Lillesand Idrettslag'):
       club_code=u'LILLS'
    elif club_name in (u'Lista Idrettslag'):
       club_code=u'LISTA'
    elif club_name in (u'Loddefjord IL'):
       club_code=u'LODD'
    elif club_name in (u'Lofoten Triatlonklubb'):
       club_code=u'LFTR'
    elif club_name in (u'Lom Idrettslag'):
       club_code=u'LOM'
    elif club_name in (u'Lundamo Idrettslag'):
       club_code=u'LUND'
    elif club_name in (u'Lundehøgda IL'):
       club_code=u'LUNDH'
    elif club_name in (u'Luster Idrettslag'):
       club_code=u'LUST'
    elif club_name in (u'Lye Idrettslag'):
       club_code=u'LYE'
    elif club_name in (u'Lyn Ski'):
       club_code=u'LYN'
    elif club_name in (u'Lyngdal Idrettslag', u'Lyngdal IL'):
       club_code=u'LNGD'
    elif club_name in (u'Lyngen/ Karnes Il'):
       club_code=u'LYKA'
    elif club_name in (u'Lyngstad og Omegn Idrettslag'):
       club_code=u'LYNGO'
    elif club_name in (u'Lørenskog Friidrettslag'):
       club_code=u'LRSKG'
    elif club_name in (u'Løten Friidrett'):
       club_code=u'LFK'
    elif club_name in (u'Løten Friidrett 2'):
       club_code=u'LTN'
    elif club_name in (u'Malm IL'):
       club_code=u'MALM'
    elif club_name in (u'Målselv Idrettslag'):
       club_code=u'MLSEL'
    elif club_name in (u'Malvik Idrettslag'):
       club_code=u'MALV'
    elif club_name in (u'Måløy Idrettslag Hovedstyre'):
       club_code=u'MAAL'
    elif club_name in (u'Mandal & Halse I.l.'):
       club_code=u'MAHA'
    elif club_name in (u'Måndalen Idrettslag'):
       club_code=u'MNDL'
    elif club_name in (u'Markabygda Idrettslag'):
       club_code=u'MABY'
    elif club_name in (u'Markane Idrettslag', u'Markane IL'):
       club_code=u'MARKA'
    elif club_name in (u'Marnardal Idrettslag'):
       club_code=u'MARNA'
    elif club_name in (u'Medkila Skilag'):
       club_code=u'MEDKI'
    elif club_name in (u'Meldal Idrettslag'):
       club_code=u'MELD'
    elif club_name in (u'Melhus Idrettslag'):
       club_code=u'MELHU'
    elif club_name in (u'Midsund Idrettslag'):
       club_code=u'MDSND'
    elif club_name in (u'Mjøsdalen IL'):
       club_code=u'MJSD'
    elif club_name in (u'Modum Friidrettsklubb'):
       club_code=u'MOD'
    elif club_name in (u'Moelven Idrettslag', u'Moelven IL'):
       club_code=u'MOELV'
    elif club_name in (u'Moi Idrettslag'):
       club_code=u'MOI'
    elif club_name in (u'Molde og Omegn Idrettsforening'):
       club_code=u'MOLDE'
    elif club_name in (u'Molde Olymp'):
       club_code=u'OLYMP'
    elif club_name in (u'Moltustranda Idrettslag'):
       club_code=u'MOITU'
    elif club_name in (u'Mosjøen Friidrettsklubb'):
       club_code=u'MOSJ'
    elif club_name in (u'Moss Idrettslag', u'Moss IL'):
       club_code=u'MOSS'
    elif club_name in (u'Mosvik Idrettslag', 'Mosvik IL - Friidrett'):
       club_code=u'MOSV'
    elif club_name in (u'MUIL - Mefjordvær Ungdoms- og Idrettslag'):
       club_code=u'MUIL'
    elif club_name in (u'Namdal løpeklubb'):
       club_code=u'NAML'
    elif club_name in (u'Namdalseid Idrettslag'):
       club_code=u'NAMDA'
    elif club_name in (u'Namsen Fif'):
       club_code=u'NAMSE'
    elif club_name in (u'Nannestad Idrettslag'):
       club_code=u'NANN'
    elif club_name in (u'Narvik Idrettslag'):
       club_code=u'NAR'
    elif club_name in (u'Nesbyen Idrettslag', u'Nesbyen IL Friidrett'):
       club_code=u'NESB'
    elif club_name in (u'Nesodden IF'):
       club_code=u'NESO'
    elif club_name in (u'Nesøya Idrettslag', u'Nesøya IL'):
       club_code=u'NES'
    elif club_name in (u'Nidelv Idrettslag'):
       club_code=u'NID'
    elif club_name in (u'Nissedal Idrettslag'):
       club_code=u'NISS'
    elif club_name in (u'Nittedal Idrettslag', u'Nittedal IL'):
       club_code=u'NITT'
    elif club_name in (u'Nordkjosbotn Idrettslag'):
       club_code=u'NRDKJ'
    elif club_name in (u'Nordre Eidsvoll Idrettslag'):
       club_code=u'NEIDS'
    elif club_name in (u'Nordre Fjell Friidrett'):
       club_code=u'NFJEL'
    elif club_name in (u'Nordre Land Idrettslag', u'Nordre Land IL'):
       club_code=u'NLAND'
    elif club_name in (u'Nordre Trysil IL'):
       club_code=u'NTRY'
    elif club_name in (u'Nordøy Idrettslag'):
       club_code=u'NORIL'
    elif club_name in (u'Norrøna IL'):
       club_code=u'NORR'
    elif club_name in (u'Northern Runners'):
       club_code=u'NRUN'
    elif club_name in (u'NTNUI - Norges Teknisk-Naturvitenskapelige Universitets Idrettsforening'):
       club_code=u'NTNUI'
    elif club_name in (u'Nydalens Skiklub'):
       club_code=u'NYSK'
    elif club_name in (u'Nykirke Idrettsforening'):
       club_code=u'NYKIR'
    elif club_name in (u'Nøtterøy Idrettsforening'):
       club_code=u'NTTRY'
    elif club_name in (u'Odda Idrettslag'):
       club_code=u'ODDA'
    elif club_name in (u'Ogndal Idrettslag Hovedlaget'):
       club_code=u'OGND'
    elif club_name in (u'Olden Idrettslag'):
       club_code=u'OLD'
    elif club_name in (u'Olderdalen Idrettsklubb'):
       club_code=u'OLDA'
    elif club_name in (u'Oppdal IL Hovedlaget'):
       club_code=u'OPPD'
    elif club_name in (u'Oppegård Idrettslag', u'Oppegård IL'):
       club_code=u'OPP'
    elif club_name in (u'Oppsal Idrettsforening', u'Oppsal IF'):
       club_code=u'OPSL'
    elif club_name in (u'Oppstad Idrettslag'):
       club_code=u'OPST'
    elif club_name in (u'Oppstad Idrettslag 2'):
       club_code=u'OPPST'
    elif club_name in (u'Oppstryn Idrettslag'):
       club_code=u'OPSTR'
    elif club_name in (u'Opptur Motbakkeklubb'):
       club_code=u'OPPT'
    elif club_name in (u'Orkanger Idrettsforening'):
       club_code=u'ORKA'
    elif club_name in (u'Orkdal Idrettslag'):
       club_code=u'ORKD'
    elif club_name in (u'Orre Idrettslag'):
       club_code=u'ORRE'
    elif club_name in (u'Os Idrettslag'):
       club_code=u'OS'
    elif club_name in (u'Os Turnforening'):
       club_code=u'OSTU'
    elif club_name in (u'OSI Friidrett'):
       club_code=u'FRII'
    elif club_name in (u'Oslo Politis Idrettslag', u'Oslo Politis IL'):
       club_code=u'POLIT'
    elif club_name in (u'Oslostudentenes Idrettsklubb', 'Oslostudentenes IK'):
       club_code=u'OSI'
    elif club_name in (u'Osterøy Idrottslag', u'Osterøy IL'):
       club_code=u'OST'
    elif club_name in (u'Otra IL'):
       club_code=u'OTRA'
    elif club_name in (u'Ottestad Idrettslag'):
       club_code=u'OTTE'
    elif club_name in (u'Ottestad Kast og Styrkeløft'):
       club_code=u'OTKS'
    elif club_name in (u'Overhalla Idrettslag', u'Overhalla IL'):
       club_code=u'OVRH'
    elif club_name in (u'Porsanger Idrettslag'):
       club_code=u'PORS'
    elif club_name in (u'Rana Friidrettsklubb'):
       club_code=u'RANA'
    elif club_name in (u'Ranheim Idrettslag', u'Ranheim IL'):
       club_code=u'RAN'
    elif club_name in (u'Raufoss IL Friidrett', 'Raufoss Friidrett'):
       club_code=u'RAU'
    elif club_name in (u'Raumnes & Årnes Idrettslag', u'Raumnes & Årnes IL'):
       club_code=u'RAUM'
    elif club_name in (u'Re Friidrettsklubb'):
       club_code=u'RE'
    elif club_name in (u'Ready Idrettsforeningen'):
       club_code=u'READY'
    elif club_name in (u'Rena Idrettslag'):
       club_code=u'RENA'
    elif club_name in (u'Rendalen Idrettslag'):
       club_code=u'RENDA'
    elif club_name in (u'Rennebu Idrettslag'):
       club_code=u'RENB'
    elif club_name in (u'Rindal Idrettslag', u'Rindal IL'):
       club_code=u'RIND'
    elif club_name in (u'Ringerike Friidrettsklubb'):
       club_code=u'RING'
    elif club_name in (u'Risør Idrettslag'):
       club_code=u'RIS'
    elif club_name in (u'Rjukan Idrettslag'):
       club_code=u'RJU'
    elif club_name in (u'Rogne Idrettslag'):
       club_code=u'ROGNE'
    elif club_name in (u'Romerike Friidrett'):
       club_code=u'ROMFR'
    elif club_name in (u'Romerike Ultraløperklubb'):
       club_code=u'ROMUL'
    elif club_name in (u'Romsdal Randoneklubb'):
       club_code=u'ROMRA'
    elif club_name in (u'Rosendal Turnlag', u'Rosendal TL'):
       club_code=u'ROSEN'
    elif club_name in (u'Royal Sport'):
       club_code=u'ROYAL'
    elif club_name in (u'Rustad Idrettslag', u'Rustad IL'):
       club_code=u'RUS'
    elif club_name in (u'Rygge Idrettslag', u'Rygge IL'):
       club_code=u'RYGGE'
    elif club_name in (u'Røa Allianseidrettslag'):
       club_code=u'RIL'
    elif club_name in (u'Røldal Idrettslag'):
       club_code=u'RDIL'
    elif club_name in (u'Røros Idrettslag'):
       club_code=u'ROSIL'
    elif club_name in (u'Røyken UIL'):
       club_code=u'RKEN'
    elif club_name in (u'Salangen IF Friidrett', u'Salangen IF - Friidrett', u'Salangen If - Friidrett'):
       club_code=u'SALA'
    elif club_name in (u'Samnanger Idrettslag'):
       club_code=u'SAMN'
    elif club_name in (u'Sandane Turn og Idrettslag'):
       club_code=u'SANTU'
    elif club_name in (u'Sandefjord Turn & Idrettsforening', u'SANDEFJORD TURN & IDRETTSFORENING'):
       club_code=u'STIF'
    elif club_name in (u'Sandnes Idrettslag', u'Sandnes IL'):
       club_code=u'SAND'
    elif club_name in (u'Sandnes Idrettslag 2'):
       club_code=u'SNDI'
    elif club_name in (u'Sandnessjøen Idrettslag', u'Sandnessjøen IL'):
       club_code=u'SNDSJ'
    elif club_name in (u'Sarpsborg Allianseidrettslag', u'Sarpsborg IL'):
       club_code=u'SARP'
    elif club_name in (u'Sauda Idrettslag'):
       club_code=u'SAUD'
    elif club_name in (u'Sauland Idrettslag'):
       club_code=u'SAUL'
    elif club_name in (u'Selbu IL'):
       club_code=u'SELB'
    elif club_name in (u'Selje Idrettslag'):
       club_code=u'SELJE'
    elif club_name in (u'Seljord Idrettslag'):
       club_code=u'SELJO'
    elif club_name in (u'Selsbakk Idrettsforening'):
       club_code=u'SELS'
    elif club_name in (u'Sem Idrettsforening', u'Sem IF'):
       club_code=u'SEM'
    elif club_name in (u'Sigdal Friidrettsklubb'):
       club_code=u'SIGFR'
    elif club_name in (u'Sigdals Skiklub'):
       club_code=u'SIGSK'
    elif club_name in (u'Siljan Idrettslag'):
       club_code=u'SILJ'
    elif club_name in (u'Sirma Il'):
       club_code=u'SIRMA'
    elif club_name in (u'Sjetne Idrettslag'):
       club_code=u'SJET'
    elif club_name in (u'Sk Vedavåg Karmøy'):
       club_code=u'VEDA'
    elif club_name in (u'SK Vidar'):
       club_code=u'VID'
    elif club_name in (u'Skagerrak Sportsklubb'):
       club_code=u'SKAGE'
    elif club_name in (u'Skåla Idrettslag'):
       club_code=u'SKLA'
    elif club_name in (u'Skarphedin IL', u'Idrettslaget Skarphedin'):
       club_code=u'SKRPH'
    elif club_name in (u'Skaubygda Il'):
       club_code=u'SKAU'
    elif club_name in (u'Skaun Idrettslag'):
       club_code=u'SKAUN'
    elif club_name in (u'Ski IL Friidrett'):
       club_code=u'SKI'
    elif club_name in (u'Skjåk IL'):
       club_code=u'SKJK'
    elif club_name in (u'Skjoldar Il'):
       club_code=u'SKJO'
    elif club_name in (u'Skogn Idrettslag'):
       club_code=u'SKOGN'
    elif club_name in (u'Skotterud Idrettslag'):
       club_code=u'SKO'
    elif club_name in (u'Skreia Idrettslag'):
       club_code=u'SKREIA'
    elif club_name in (u'Snåsa Idrettslag'):
       club_code=u'SNSA'
    elif club_name in (u'Snøgg Friidrett'):
       club_code=u'SNGG'
    elif club_name in (u'Sogndal Idrettslag'):
       club_code=u'SIL'
    elif club_name in (u'Sokndal Friidrettsklubb'):
       club_code=u'SOKND'
    elif club_name in (u'Sola Friidrett'):
       club_code=u'SOLA'
    elif club_name in (u'Solnut IL'):
       club_code=u'SOLN'
    elif club_name in (u'Sortland Friidrettsklubb'):
       club_code=u'SORTL'
    elif club_name in (u'Sotra Sportsklubb'):
       club_code=u'SOT'
    elif club_name in (u'Spillum Idrettslag'):
       club_code=u'SPILL'
    elif club_name in (u'Spiridon Langløperlag'):
       club_code=u'SPRD'
    elif club_name in (u'Spirit Friidrettsklubb'):
       club_code=u'SPIRT'
    elif club_name in (u'Spjelkavik og Omegn Friidrettsklubb'):
       club_code=u'SPJVK'
    elif club_name in (u'Sportsklubben Kraft'):
       club_code=u'KRAFT'
    elif club_name in (u'Sportsklubben Rye', u'Rye Sp.Kl.'):
       club_code=u'RYE'
    elif club_name in (u'Sportsklubben Vidar'):
       club_code=u'VIDAR'
    elif club_name in (u'Spydeberg IL'):
       club_code=u'SPYDE'
    elif club_name in (u'Staal Jørpeland IL'):
       club_code=u'STJIL'
    elif club_name in (u'Stadsbygd IL'):
       club_code=u'STAD'
    elif club_name in (u'Stårheim Idrettslag', u'Stårheim IL'):
       club_code=u'STRHE'
    elif club_name in (u'Stavanger Døve-Idrettsforening'):
       club_code=u'STDIF'
    elif club_name in (u'Stavanger Friidrettsklubb'):
       club_code=u'STAVA'
    elif club_name in (u'Stavanger Idrettsforening Allianseidrettslag - Friidrett'):
       club_code=u'STAVIF'
    elif club_name in (u'Stegaberg Idrettslag'):
       club_code=u'STEGA'
    elif club_name in (u'Stein Friidrettsklubb'):
       club_code=u'STEIN'
    elif club_name in (u'Steinkjer Friidrettsklubb'):
       club_code=u'STEKJ'
    elif club_name in (u'Stettevik Sportsklubb'):
       club_code=u'STSK'
    elif club_name in (u'Stjørdal Fridrettsklubb', u'Stjørdal Friidrettsklubb'):
       club_code=u'STJF'
    elif club_name in (u'Stjørdal Paraidrettslag'):
       club_code=u'STJP'
    elif club_name in (u'Stjørdals-Blink IL'):
       club_code=u'STJB'
    elif club_name in (u'Stokke Idrettslag'):
       club_code=u'STOKK'
    elif club_name in (u'Stokmarknes Idrettslag'):
       club_code=u'STOKM'
    elif club_name in (u'Stord Idrettslag', u'Stord IL (Allianseidrettslag)'):
       club_code=u'STO'
    elif club_name in (u'Storfjord idrettslag'):
       club_code=u'STOFJ'
    elif club_name in (u'Stranda Idrottslag'):
       club_code=u'STRIL'
    elif club_name in (u'Strandebarm Idrettslag'):
       club_code=u'STRAB'
    elif club_name in (u'Stranden Idrettslag'):
       club_code=u'STRA'
    elif club_name in (u'Straumsnes Idrettslag'):
       club_code=u'STRAU'
    elif club_name in (u'Strindheim Idrettslag', u'Strindheim il'):
       club_code=u'STRI'
    elif club_name in (u'Stryn Turn og Idrettslag'):
       club_code=u'STRY'
    elif club_name in (u'Støren Sportsklubb'):
       club_code=u'STREN'
    elif club_name in (u'Sunndal IL Friidrett'):
       club_code=u'SUNND'
    elif club_name in (u'Surnadal Idrettslag'):
       club_code=u'SURN'
    elif club_name in (u'Svalbard Turn Idrettslag'):
       club_code=u'SVTU'
    elif club_name in (u'Svarstad Idrettslag', u'Svarstad IL'):
       club_code=u'SVARS'
    elif club_name in (u'Sveio Idrettslag'):
       club_code=u'SVEIO'
    elif club_name in (u'Svelgen Turn og Idrettsforening'):
       club_code=u'SVEL'
    elif club_name in (u'Svint IL'):
       club_code=u'SVINT'
    elif club_name in (u'SVORKMO N.O.I.', u'Svorkmo N.O.I.'):
       club_code=u'SVORK'
    elif club_name in (u'Sykkylven Idrottslag'):
       club_code=u'SYKK'
    elif club_name in (u'Sylling Idrettsforening'):
       club_code=u'SYLL'
    elif club_name in (u'Sædalen Idrettslag'):
       club_code=u'SDAL'
    elif club_name in (u'Sætre Idrætsforening Graabein'):
       club_code=u'GRAA'
    elif club_name in (u'Søfteland Turn & Idrettslag'):
       club_code=u'STIL'
    elif club_name in (u'Søgne Idrettslag'):
       club_code=u'SGNE'
    elif club_name in (u'Sømna Idrettslag', u'Sømna IL'):
       club_code=u'SMNA'
    elif club_name in (u'Søndre Land IL Friidrett', u'Friidrett Søndre Land IL'):
       club_code=u'SNDLA'
    elif club_name in (u'Søre Ål Idrettslag'):
       club_code=u'SAAL'
    elif club_name in (u'Sørild Fridrettsklubb', u'Sørild FIK'):
       club_code=u'SRILD'
    elif club_name in (u'Sørkedalens Idrettsforening'):
       club_code=u'SRKDL'
    elif club_name in (u'Sørum Idrettslag'):
       club_code=u'SORUM'
    elif club_name in (u'T I L Hovding'):
       club_code=u'HOVD'
    elif club_name in (u'Tamil Sangam IL'):
       club_code=u'TAMSAN'
    elif club_name in (u'Tistedalen FL'):
       club_code=u'TIST'
    elif club_name in (u'Tingvoll Friidrettsklubb', u'Tingvoll Friidrettskl.'):
       club_code=u'TING'
    elif club_name in ( 'IK Tjalve', 'Idrettsklubben Tjalve', 'Tjalve, IK', 'Tjalve, Idrettsklubben', 'Tjalve Idrettsklubben' ):
       club_code=u'TJALV'
    elif club_name in (u'Tjølling Idrettsforening'):
       club_code=u'TJØLL'
    elif club_name in (u'Tjøme Idrettslag'):
       club_code=u'TJI'
    elif club_name in (u'Tjøme Løpeklubb'):
       club_code=u'TJL'
    elif club_name in (u'Tolga Idrettslag'):
       club_code=u'TOL'
    elif club_name in (u'Tomrefjord Idrettslag'):
       club_code=u'TOMR'
    elif club_name in (u'Torodd IF'):
       club_code=u'TORO'
    elif club_name in (u'Torvikbukt Idrettslag'):
       club_code=u'TORVI'
    elif club_name in (u'Treungen Idrettslag'):
       club_code=u'TREU'
    elif club_name in (u'Trio idrettslag'):
       club_code=u'TRIO'
    elif club_name in (u'Tromsø Friidrettsklubb'):
       club_code=u'TRF'
    elif club_name in (u'Tromsø Løpeklubb'):
       club_code=u'TRL'
    elif club_name in (u'Tromsø Svømmeklubb'):
       club_code=u'TRS'
    elif club_name in (u'Trondheim & Omegn Sportsklubb'):
       club_code=u'TROO'
    elif club_name in (u'Trondheim Friidrett', u'Trondheim Friidrett - Friidrett'):
       club_code=u'TROF'
    elif club_name in (u'Trøgstad Skiklubb'):
       club_code=u'TSK'
    elif club_name in (u'TUIL Tromsdalen Friidrett'):
       club_code=u'TUIL'
    elif club_name in (u'Tvedestrand Turn & Idrettsforening'):
       club_code=u'TVEDE'
    elif club_name in (u'Tyrving Idrettslag', u'Tyrving IL'):
       club_code=u'TYR'
    elif club_name in (u'Tønsberg Friidrettsklubb'):
       club_code=u'TNSBF'
    elif club_name in (u'Tørvikbygd Idrettslag'):
       club_code=u'TRBIL'
    elif club_name in (u'Tøyen Sportsklubb'):
       club_code=u'TYEN'
    elif club_name in (u'Ullensaker/Kisa IL Friidrett'):
       club_code=u'ULLK'
    elif club_name in (u'Ullensaker/Kisa IL Friidrett 2'):
       club_code=u'ULKI'
    elif club_name in (u'Undheim Idrettslag'):
       club_code=u'UND'
    elif club_name in (u'Urædd Friidrett'):
       club_code=u'URFRI'
    elif club_name in (u'Utleira Idrettslag'):
       club_code=u'UTL'
    elif club_name in (u'Vaaler Idrettsforening'):
       club_code=u'VAAL'
    elif club_name in (u'Vadsø Atletklubb'):
       club_code=u'VA'
    elif club_name in (u'Vadsø Turnforening (Vtf)'):
       club_code=u'VTF'
    elif club_name in (u'Vågå Idrettslag'):
       club_code=u'VGAA'
    elif club_name in (u'Vågstranda Idrettslag'):
       club_code=u'VIL'
    elif club_name in (u'Valkyrien Idrettslag'):
       club_code=u'VALK'
    elif club_name in (u'Valldal Idrettslag'):
       club_code=u'VALL'
    elif club_name in (u'Vallset IL'):
       club_code=u'VAL'
    elif club_name in (u'Varegg Fleridrett'):
       club_code=u'VAR'
    elif club_name in (u'Varhaug Idrettslag'):
       club_code=u'VARH'
    elif club_name in (u'Varteig Idrettslag'):
       club_code=u'VART'
    elif club_name in (u'Vegårshei Idrettslag'):
       club_code=u'VEG'
    elif club_name in (u'Veldre Friidrett'):
       club_code=u'VELD'
    elif club_name in (u'Velledalen Idrettslag'):
       club_code=u'VELL'
    elif club_name in (u'Verdal Friidrettsklubb'):
       club_code=u'VERD'
    elif club_name in (u'Vestby Idrettslag'):
       club_code=u'VESTB'
    elif club_name in (u'Vestfossen Idrettsforening', u'Vestfossen IF'):
       club_code=u'VESTF'
    elif club_name in (u'Vestre Spone IF'):
       club_code=u'VSPON'
    elif club_name in (u'Vik Idrettslag', u'Vik IL'):
       club_code=u'VIKIL'
    elif club_name in (u'Vikane IL'):
       club_code=u'VIKAN'
    elif club_name in (u'Viking Turn og Idrettsforening', u'TIF Viking'):
       club_code=u'VIK'
    elif club_name in (u'Viksdalen Idrettslag'):
       club_code=u'VIKSD'
    elif club_name in (u'Viljar IL'):
       club_code=u'VILJ'
    elif club_name in (u'Vind Idrettslag'):
       club_code=u'VNDIL'
    elif club_name in (u'Vindafjord Idrettslag'):
       club_code=u'VINDA'
    elif club_name in (u'Vinje Idrottslag'):
       club_code=u'VINJE'
    elif club_name in (u'Vollan Idrettsklubb', u'Vollan I.K.'):
       club_code=u'VOLL'
    elif club_name in (u'Voss Idrottslag'):
       club_code=u'VOSS'
    elif club_name in (u'Ytterøy Idrettslag'):
       club_code=u'YTTER'
    elif club_name in (u'Ørje Idrettslag'):
       club_code=u'ORJIL'
    elif club_name in (u'Ørsta Idrettslag', u'Ørsta IL'):
       club_code=u'ORSTA'
    elif club_name in (u'Østmarka Marsjklubb'):
       club_code=u'OMARSJ'
    elif club_name in (u'Øyer/Tretten Idrettsforening'):
       club_code=u'OTRET'
    elif club_name in (u'Øystre Slidre Idrettslag'):
       club_code=u'OSLID'
    else:
       club_code = club_name
 
    return club_code

def sort_event_list(events):
    def sort_fcn(e):
        #print(e)
        catsort = ['G6-7', 'G8', 'G9', 'G10', 'G11', 'G11-14', 'G12', 'G13', 'G14', 'G15', 'G16', 'G17', 'G18-19', 
                   'J6-7', 'J8', 'J9', 'J10', 'J11-14', 'J11', 'J12', 'J13', 'J14', 'J15', 'J16', 'J17', 'J18-19', 
                   'MU20', 'MU23', 'MS', 'KU20', 'KU23', 'KS', 
                   'MV35', 'MV40', 'MV45', 'MV50', 'MV55', 'MV60', 'MV65', 'MV70', 'MV75',
                   'KV35', 'KV40', 'KV45', 'KV50', 'KV55', 'KV60', 'KV65', 'KV70', 'KV75']

        evsort = ['60', '100', '200', '400', '600', '800', '1000', '1500', 'MILE', '3000', '5000', '10000', 
                '60H', '80H', '100H', '110H', '200H', '300H', '400H', '2000SC', '3000SC', 
                'HJ', 'PV', 'LJ', 'TJ', 'SP', 'DT', 'JT', 'HT', 'PEN', 'HEX', 'HEP', 'ENN', 'DEC']
        return 100*catsort.index(e[2]) + evsort.index(e[1])

    print(events)
    events.sort(key=sort_fcn)
    return events

def read_isonenxls(f):
    wb = load_workbook(filename=f)
    ws = wb.active

#   columns = ws[1]
#   print(list(columns))
#   sys.exit()
    events =  []
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
            cat = cat_code(value[columns.index('Klasse')])
            nat = cat_code(value[columns.index('Landskode')])
            athlete_key = (first_name, last_name, dob, g, club, nat)
            event = (ev, event_code(ev),  cat)
            print(athlete_key)
            print(event)

            if event[0] is None:
                continue
            if event not in events:
                events.append(event)
    
            if athlete_key not in events_by_athlete.keys():
                events_by_athlete[athlete_key] = []
            if event not in events_by_athlete[athlete_key]:
                events_by_athlete[athlete_key].append( event )

    events = sort_event_list(events)
    return events, events_by_athlete

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
    #event = event_code(event)
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
    events, events_by_athlete = read_isonenxls(f)

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
    ws["H1"] = 'Nationality'
    ws["I1"] = 'Event'
    ws["J1"] = 'Pb'
    ws["K1"] = 'Sb'
#   ws1["A1"] = 'Event selection'
    row_counter = 2

    jf = 0
    jt = 0
    jm = 0
    full_events = {}
    for e in events:
        event  = e[0]
        evcode = e[1]
        cat    = e[2]
        if isfield(event):
            jf +=1
            event_ref = "F%02d"%jf
        elif ismulti(event):
            jm +=1
            event_ref = "M%02d"%jm
        else:
            jt +=1
            event_ref = "T%02d"%jt

        #print(e)
        full_events[ ( cat , evcode ) ]  = event_ref + ' - ' + ' '.join(( cat, event_spec(event, cat) ))
        ws1["A%d"%row_counter] = event_ref + ' - '  + ' '.join([e[0], event_spec(e[1], cat)])
        ws1["B%d"%row_counter] = event_ref
        ws1["C%d"%row_counter] = evcode
        ws1["D%d"%row_counter] = age_group(cat)
        ws1["E%d"%row_counter] = get_gender(cat)
        ws1["F%d"%row_counter] = cat
#       ws1["G%d"%row_counter] = age_group(class_code(e[0]))

        ws1["H%d"%row_counter] = ' '.join(( cat, event_spec(event, cat) ))
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
        fn   = key[0]
        ln   = key[1]
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
            ws["G%d"%row_counter] = club_code(club)
            ws["H%d"%row_counter] = nat
            ws["I%d"%row_counter] = full_events[ (e[2], e[1]) ]

            #event = e[1]
            if not isfield(event):
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
