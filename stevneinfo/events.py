from collections import defaultdict

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



def sort_event_list(events):
    def sort_fcn(e):
        #print(e)
        catsort = ['G6-7', 'G8', 'G9', 'G9-10', 'G10', 'G11', 'G11-12', 'G11-14', 'G12', 'G13', 'G14', 'G15', 'G15-17', 'G16', 'G17', 'G18-19', 
                   'J6-7', 'J8', 'J9', 'J9-10', 'J10', 'J11', 'J11-12', 'J11-14', 'J12', 'J13', 'J14', 'J15', 'J15-17', 'J16', 'J17', 'J18-19', 
                   'MU20', 'MU23', 'MS', 'KU20', 'KU23', 'KS', 
                   'MSPARA',
                   'MV', 'MV35', 'MV40', 'MV45', 'MV50', 'MV55', 'MV60', 'MV65', 'MV70', 'MV75',
                   'KV', 'KV35', 'KV40', 'KV45', 'KV50', 'KV55', 'KV60', 'KV65', 'KV70', 'KV75']

        evsort = ['60', '100', '200', '400', '600', '800', '1000', '1500', 'MILE', '3000', '5000', '10000', 
                '60H', '80H', '100H', '110H', '200H', '300H', '400H', '2000SC', '3000SC', 
                'HJ', 'PV', 'LJ', 'TJ', 'SP', 'DT', 'JT', 'HT', 'OT', 'PEN', 'HEX', 'HEP', 'ENN', 'DEC']
        return 100*catsort.index(e[2]) + evsort.index(e[1])

    print(events)
    events.sort(key=sort_fcn)
    return events

