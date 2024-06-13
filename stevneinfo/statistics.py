import re
import requests
import json
from collections import defaultdict
import time

athlete_ids = {}

def event_id(event, cat):

    event_ids = {}

    if event == '40':
        eid = '1'
    elif event == '60':
        eid = '2'
    elif event == '80':
        eid =' 3'
    elif event == '100':
        eid = '4'
    elif event == '200':
        eid = '5'
    elif event == '300':
        eid = '6'
    elif event == '400':
        eid = '7'
    elif event == '600':
        eid = '8'
    elif event == '800':
        eid = '9'
    elif event == '1000':
        eid = '10'
    elif event == '1500':
        eid = '11'
    elif event == '2000':
        eid = '12'
    elif event == '3000':
        eid = '13'
    elif event == '5000':
        eid = '14'
    elif event == '10000':
        eid = '15'
    elif event ==  '60H':
        eid = { 'J10' : '19', 'J11' : '19', 'J12' : '19', 'J13' : '20', 'J14' : '20', 'J15' : '20', 'J16' : '20', 'J17' : '20', 'J18/19' : '21','KJ' : '21','KU20' : '21', 'KU23' : '21', 'KS' : '21', 'G10' : '19', 'G11' : '19', 'G12' : '20', 'G13' : '20', 'G14' : '21', 'G15' : '21', 'G16' : '22', 'G17' : '22', 'G18/19' : '23','MU20' : '23', 'MU23' : '24', 'MS' : '24', 'default':'' }.get(cat,'')
    elif event == '80H':
        eid = { 'J15' : '27', 'J16' : '27', 'G14' : '28' }.get(cat,'')
    elif event == '100H':
        eid = { 'J16' : '34', 'J17' : '34', 'J18/19' : '35','KJ' : '35','KU20' : '35', 'KU23' : '35', 'KS' : '35', 'G15' : '35', 'G16' : '36'}.get(cat,'')
    elif event == '110H':
        eid = { 'G17' : '40', 'G18/19' : '41','MJ' : '41', 'MU20' : '41', 'MU23' : '42', 'MS' : '42' }.get(cat,'')
    elif event == '200H':
        eid = { 'J10' : '44', 'J11' : '44', 'J12' : '44', 'J13' : '44', 'G10' : '44', 'G11' : '44', 'G12' : '44', 'G13' : '44', 'default' : '45' }.get(cat,'')
    elif event == '300H':
        eid = { 'J15' : '51', 'J16' : '51', 'J17' : '51', 'J18/19' : '51','KJ' : '51','KU20' : '51', 'KU23' : '51', 'KS' : '51', 'G15' : '51', 'G16' : '52', 'G17' : '52', 'G18/19' : '53','MJ' : '53', 'MU20' : '53', 'MU23' : '53', 'MS' : '53' }.get(cat,'')
    elif event == '400H':
        eid = { 'J15' : '57', 'J16' : '57', 'J17' : '57', 'J18/19' : '57','KJ' : '57','KU20' : '57', 'KU23' : '57', 'KS' : '57', 'G15' : '57', 'G16' : '58', 'G17' : '58', 'G18/19' : '59','MJ' : '59','MU20' : '59', 'MU23' : '59', 'MS' : '59' }.get(cat,'')
#   event_ids['1500SC'] = {}
#   event_ids['2000SC'] = {}
#   event_ids['3000SC'] = {}
# ... jumps
    elif event == 'HJ':
        eid = '68' 
    elif event == 'SHJ':
        eid = '69' 
    elif event == 'PV':
        eid = '70' 
    elif event == 'LJ':
        eid = {'G10': '72','G11': '72','G12': '72',  'G13': '72', 'J10': '72','J11': '72','J12': '72',  'J13': '72', 'default' : '71' }.get(cat,'71')
    elif event == 'SLJ':
        eid = '74' 
    elif event == 'TJ':
        eid = {'G10': '76','G11': '76','G12': '76',  'G13': '76', 'J10': '76','J11': '76','J12': '76',  'J13': '76', 'default' : '75' }.get(cat,'75')
    elif event == 'STJ':
        eid = '78' 
# ... throws
    elif event == 'SP':
        eid = { 'J10' : '81', 'J11' : '81', 'J12' : '81', 'J13' : '81', 'J14' : '82', 'J15' : '82', 'J16' : '82', 'J17' : '82', 'J18/19' : '83', 'KU20' : '83', 'KU23' : '83', 'KS' : '83', 'G10' : '81', 'G11' : '81', 'G12' : '82', 'G13' : '82', 'G14' : '83', 'G15' : '83', 'G16' : '84', 'G17' : '84', 'G18/19' : '85', 'MU20' : '85', 'MU23' : '86', 'MS' : '86', 'default' : ''}.get(cat,'')
    elif event == 'DT':
        eid = { 'J10' : '88', 'J11' : '88', 'J12' : '88', 'J13' : '88', 'J14' : '89', 'J15' : '89', 'J16' : '89', 'J17' : '89', 'J18/19' : '90', 'KU20' : '90', 'KU23' : '90', 'KS' : '90', 'G10' : '88', 'G11' : '88', 'G12' : '89', 'G13' : '89', 'G14' : '90', 'G15' : '90', 'G16' : '91', 'G17' : '91', 'G18/19' : '92', 'MU20' : '92', 'MU23' : '93', 'MS' : '93', 'default': ''}.get(cat,'')
    elif event == 'JT':
        eid = { 'J10' : '95', 'J11' : '95', 'J12' : '95', 'J13' : '95', 'J14' : '95', 'J15' : '139', 'J16' : '139', 'J17' : '139', 'J18/19' : '96', 'KU20' : '96', 'KU23' : '96', 'KS' : '96', 'G10' : '95', 'G11' : '95', 'G12' : '95', 'G13' : '95', 'G14' : '96', 'G15' : '96', 'G16' : '97', 'G17' : '97', 'G18/19' : '98', 'MU20' : '98', 'MU23' : '98', 'MS' : '98', 'default': ''}.get(cat,'')
    elif event == 'HT':
        eid = { 'J10' : '101', 'J11' : '101', 'J12' : '101', 'J13' : '101', 'J14' : '155', 'J15' : '155', 'J16' : '155', 'J17' : '155', 'J18/19' : '103', 'KU20' : '103', 'KU23' : '103', 'KS' : '103', 'G10' : '101', 'G11' : '101', 'G12' : '155', 'G13' : '155', 'G14' : '103', 'G15' : '103', 'G16' : '104', 'G17' : '104', 'G18/19' : '105', 'MU20' : '105', 'MU23' : '106', 'MS' : '106', 'default': ''}.get(cat,'')

    elif event == 'OT':
        eid = 109
    return eid

def format_result(res):
    MINSECPAT = r'(\d?\d)[:.,](\d\d[,.]\d?\d)'
    match1 = re.match(MINSECPAT,res)
    if match1:
        mins = match1.group(1)
        secs = match1.group(2).replace(',','.')
        res  = f'{mins}:{secs}'
    else:
        res= res.replace(',','.')

    return res

def get_athlete_id(fn, ln, dob):
    #
    if (fn, ln, dob) in athlete_ids.keys():
        aid = athlete_ids[(fn,ln,dob)]
    else:
        url = 'https://www.minfriidrettsstatistikk.info/php/sokutover.php'
        print(f'{fn}, {ln}, {dob}')
        r = requests.post(url, data=json.dumps({'FirstName' : fn.split()[0], 'LastName' : ln.split()[-1], 'DateOfBirth' : dob}))

        aid = ''
        ATHIDPAT = r'{"Athlete_Id":"(\d*)",.*}'

        for i in range(3):
            match = re.search(ATHIDPAT, r.text)
            if match:
                aid = match.group(1)
                continue
            time.sleep(1.0)
    return aid


def get_athlete_bests(athlete_id, event_code, category):
    #
    Event_Id = event_id(event_code, category)

    pb = ''
    sb = ''
    if not athlete_id == '':
        #
        url = 'https://www.minfriidrettsstatistikk.info/php/hentresultater.php'
        r   = requests.post(url, data=json.dumps({'Athlete_Id' : athlete_id, 'Event_Id' : Event_Id}))

        PBSBPAT = r'{"Athlete_Id":.*"PB":{"Result":"(.*?)","Date":"\d{2}.\d{2}.\d{4}"},"SB":{"Result":"(.*?)","Date":"\d{2}.\d{2}.\d{4}"}}'
        PBPAT   = r'{"Athlete_Id":.*"PB":{"Result":"(.*?)","Date":"\d{2}.\d{2}.\d{4}"}}'
        for i in range(3):
            match1 = re.search(PBSBPAT,r.text)
            match2 = re.search(PBPAT  ,r.text)

            if match1:
                pb = match1.group(1)
                sb = match1.group(2)
            elif match2:
                pb = match2.group(1)
            if not pb=='' or not sb=='':
                continue
            else:
                time.sleep(1.0)

        pb = format_result(pb)
        sb = format_result(sb)
    

    return (pb, sb)
    

"""
Id   ShortName
1       40m 
2       60m 
3       80m 
4       100m 
5       200m 
6       300m 
7       400m 
8       600m 
9       800m 
10      1000m 
11      1500m 
12      2000m 
13      3000m 
14      5000m 
15      10000m 
19      60mhekk68,0cm 
20      60mhekk76,2cm 
21      60mhekk84,0cm 
22      60mhekk91,4cm 
23      60mhekk100cm 
24      60mhekk106,7cm 
26      80mhekk68,0cm 
27      80mhekk76,2cm 
28      80mhekk84,0cm 
29      80mhekk91,4cm 
30      80mhekk100cm 
31      80mhekk106,7cm 
34      100mhekk76,2cm 
35      100mhekk84,0cm 
36      100mhekk91,4cm 
40      110mhekk91,4cm 
41      110mhekk100cm 
42      110mhekk106,7cm 
44      200mhekk68,0cm
45      200mhekk76,2cm
51      300mhekk76,2cm
52      300mhekk84,0cm 
53      300mhekk91,4cm 
57      400mhekk76,2cm 
58      400mhekk84,0cm 
59      400mhekk91,4cm 
62      1500mhinder76,2cm 
63      1500mhinder91,4cm 
65      2000mhinder76,2cm 
66      2000mhinder91,4cm 
68      Høyde 
69      Høydeu/t 
70      Stav 
71      Lengde 
72      LengdeSone0,5m 
74      Lengdeu/t 
75      Tresteg 
76      TrestegSone0,5m 
78      Trestegu/t 
81      Kule2,0Kg 
82      Kule3,0Kg 
83      Kule4,0Kg 
84      Kule5,0Kg 
85      Kule6,0Kg 
86      Kule7,26Kg 
88      Diskos600gr 
89      Diskos750gr 
90      Diskos1,0Kg 
91      Diskos1,5Kg 
92      Diskos1,75Kg 
93      Diskos2,0Kg 
95      Spyd400gr 
96      Spyd600gr 
97      Spyd700gr 
98      Spyd800gr 
101         Slegge2,0Kg 
103         Slegge4,0Kg 
104      Slegge5,0Kg 
105         Slegge6,0Kg 
106         Slegge7,26Kg 
109         LitenBall150gr 
111         Slengball1,0Kg 
113      Vektkast5,45Kg 
114         Vektkast7,26Kg 
115         Vektkast9,08Kg 
116      Vektkast11,34Kg 
117         Vektkast15,88Kg 
118         Kappgang1000m 
120         3000mhinder76,2cm 
121         3000mhinder91,4cm 
122         Kappgang3000m 
123         1mile 
124     Kappgang5000m 
139         Spyd500gr 
143         Kappgang600m 
146         Kappgang400m 
147         Vektkast4,0kg 
148      Kappgang2000m 
151         Kappgang1500m 
155         Slegge3,0Kg/119,5cm 
156         Kappgang10000m 
236         Kappgang800m 
275         2000mhinder84,0cm 
"""
