gender = {'M':'M', 'K':'F', 'G':'M', 'J':'F'}
 
def cat_code(name):
    cat_codes = {
            u'6 år Fellesklasse' : u'F6' ,
            u'7 år Fellesklasse' : u'F7' ,
            u'Gutter Rekrutt'    : u'G6-7'          , 
            u'Gutter 6 - 7'      : u'G6-7'          , 
            u'Gutter 8'     : u'G8'          , 
            u'Gutter 9'     : u'G9'          , 
            u'Gutter  9-10' : u'G9-10'          , 
            u'Gutter 10'    : u'G10'          , 
            u'Gutter 11'    : u'G11'          , 
            u'Gutter 11-12' : u'G11-12'       , 
            u'Gutter 11-14' : u'G11-14'       , 
            u'Gutter 12'    : u'G12'          , 
            u'Gutter 13'    : u'G13'          , 
            u'Gutter 14'    : u'G14'          , 
            u'Gutter 15'    : u'G15'          , 
            u'Gutter 15-17' : u'G15-17'          , 
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
            u'Menn Senior Para'  : u'MSPARA'           , 
            u'Menn Senior NM'  : u'MS'           , 
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
            u'Jenter  9-10'     : u'J9-10'          , 
            u'Jenter 10'    : u'J10'          , 
            u'Jenter 11'    : u'J11'          , 
            u'Jenter 11-12' : u'J11-12'          , 
            u'Jenter 11-14' : u'J11-14'          , 
            u'Jenter 12'    : u'J12'          , 
            u'Jenter 13'    : u'J13'          , 
            u'Jenter 14'    : u'J14'          , 
            u'Jenter 15'    : u'J15'          , 
            u'Jenter 15-17' : u'J15-17'    , 
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
            u'Kvinner Senior NM'  : u'KS'           , 
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

