# -*- coding: utf-8 -*-
import json
import datetime
import re
from openpyxl import Workbook
from openpyxl.styles import colors as xlcolors
from openpyxl.styles import Font, Color

def get_category(birthdate, eventdate, gender):
    birthyear = birthdate.year
    eventyear = eventdate.year
    age = int(eventyear)-int(birthyear)

    g = {'F' : 'J', 'M' : 'G' }
    if age > 19:
        a = 'S'
        g = {'F' : 'K', 'M' : 'M' }
    elif age in (18,19):
        a = '18/19'
    else:
        a = '%d'%(age)

    cat = g[gender]+a
    return cat

def club_name(club_code):
    club_names = {
    u'AALEN':u'ÅLEN IDRETTSLAG',
    u'AASUN':u'Ålesund Friidrettsklubb',
    u'IKV':u'Allianseidrettslaget Ik Våg',
    u'ALM':u'Almenning Il',
    u'ALSV':u'Alsvåg Idrettslag',
    u'ALTA':u'Alta Idrettsforening',
    u'ANDAL':u'Åndalsnes Idrettsforening',
    u'ANDE':u'Andebu Idrettslag',
    u'ANDSK':u'Andørja Sportsklubb',
    u'ARE':u'Aremark Idrettsforening',
    u'ARNA':u'Arna Turn & Idrettslag',
    u'ASIL':u'Ås Idrettslag',
    u'AASEN':u'Åsen Idrettslag',
    u'AASER':u'Åseral idrettslag',
    u'ASK':u'Ask Friidrett',
    u'ASKFL':u'Asker Fleridrettslag',
    u'ASKSK':u'Asker Skiklubb',
    u'ASKIM':u'Askim Idrettsforening',
    u'ATNA':u'Atna Idrettslag',
    u'AURE':u'Aure Idrettslag',
    u'AURL':u'Aurland Idrettslag',
    u'AURS':u'Aurskog-Høland Friidrettslag',
    u'AUFJ':u'Austefjord Idrettslag',
    u'AUST':u'Austevoll Idrettsklubb',
    u'AUSTR':u'Austrheim Idrettslag',
    u'BAGN':u'Bagn Idrettslag',
    u'BAKKE':u'Bakke IF',
    u'BALE':u'Balestrand Idrettslag',
    u'BARD':u'Bardu Idrettslag',
    u'BTSFJ':u'Båtsfjord Sportsklubb',
    u'BGND':u'Begnadalen Idrettslag',
    u'BEIT':u'Beitstad Idrettslag',
    u'BCK':u'Bergen Cykleklubb',
    u'BTC':u'Bergen Triathlon Club',
    u'BTU':u'Bergens Turnforening',
    u'BERGE':u'Berger Idrettslag',
    u'BFGL':u'BFG Bergen Løpeklubb',
    u'BJERR':u'Bjerkreim Idrettslag',
    u'BJERV':u'Bjerkvik Idrettsforening',
    u'BLA':u'Blaker IL',
    u'BLEFJ':u'Blefjell Idrettslag',
    u'BODO':u'Bodø & Omegn IF Friidrett',
    u'BODL':u'Bodø Bauta Løpeklubb',
    u'BODF':u'Bodø Friidrettsklubb',
    u'BOKN':u'Bokn Idrettslag',
    u'BOS':u'Bossekop Ungdomslag',
    u'BOTNA':u'Botnan Idrettslag',
    u'BOT':u'Botne Skiklubb',
    u'BRNDB':u'Brandbu Idretsforening',
    u'BRATS':u'Bratsberg Idrettslag',
    u'BRATTV':u'Brattvåg Idrettslag',
    u'BREIM':u'Breimsbygda IL',
    u'BREKK':u'Brekke Idrettslag',
    u'BREMA':u'Bremanger Idrettslag',
    u'BREM':u'Bremnes Idrettslag',
    u'BRE':u'Brevik Idrettslag',
    u'BROMM':u'Bromma Idrettslag',
    u'BRYF':u'Bryne Friidrettsklubb',
    u'BRYT':u'BRYNE TRIATLONKLUBB',
    u'BUD':u'Bud Idrettslag',
    u'BYS':u'Byaasen Skiklub',
    u'BYI':u'Byåsen Idrettslag',
    u'BYN':u'Byneset IL Hovedlaget',
    u'BSK':u'Bækkelagets SK',
    u'BRVHA':u'Bærums Verk Hauger Idrettsforening',
    u'BVRFJ':u'Bæverfjord Idrettslag',
    u'BIF':u'Bøler Idrettsforening',
    u'BMLO':u'Bømlo Idrettslag',
    u'BRSA':u'Børsa Idrettslag',
    u'DALE':u'Dale Idrettslag',
    u'DLN':u'Dalen Idrettslag',
    u'DIM':u'Dimna IL',
    u'DMB':u'Dombås Idrettslag',
    u'DRIV':u'Driv Idrettslag',
    u'DRIVA':u'Driva IL',
    u'DRFR':u'Drøbak-Frogn Idrettslag',
    u'DPVG':u'Dypvåg Idrettsforening',
    u'EGRSU':u'Egersunds Idrettsklubb',
    u'EIDIL':u'Eid Idrettslag',
    u'EIDA':u'Eidanger Idrettslag',
    u'EIDF':u'Eidfjord Idrettslag',
    u'EIDSB':u'Eidsberg Idrettslag',
    u'EIDS':u'Eidsvåg Idrettslag',
    u'EIDTU':u'Eidsvold Turnforening Friidrett',
    u'EIK':u'Eikanger Idrettslag',
    u'ESK':u'Ekeberg Sports Klubb',
    u'ESPA':u'Espa Idrettslag',
    u'ETNE':u'Etne Idrettslag',
    u'FAGIL':u'Fagernes Idrettslag N',
    u'FAG':u'Fagernes Idrettslag O',
    u'FALK':u'Falkeid idrettslag',
    u'FANA':u'Fana Idrettslag',
    u'FEIR':u'Feiring Idrettslag',
    u'FET':u'Fet Friidrettsklubb',
    u'FA77':u'FIL AKS-77',
    u'FINNY':u'Finnøy Idrettslag',
    u'FISIF':u'Fiskå Idrettsforening',
    u'FISIL':u'Fiskå Idrettslag',
    u'FITJ':u'Fitjar Idrettslag',
    u'FJVE':u'Fjellhug/Vereide IL',
    u'FLATS':u'Flatås Idrettslag',
    u'FLOR':u'Florø Turn og Idrettsforening',
    u'FOLFO':u'Follafoss Idrettslag',
    u'FOL':u'Folldal Idrettsforening',
    u'FOLLO':u'Follo Løpeklubb',
    u'FORRA':u'Forra Idrettslag',
    u'FOSSU':u'Fossum Idrettsforening',
    u'FRED':u'Fredrikstad Idrettsforening',
    u'FREI':u'Freidig Sportsklubben',
    u'ORION':u'Friidretsklubben Orion',
    u'REN':u'Friidrettsklubben Ren-Eng',
    u'BAMSE':u'Friidrettslaget Bamse',
    u'BORG':u'Friidrettslaget Borg',
    u'FRISK':u'Friidrettslaget Frisk',
    u'FRO':u'Frognerparken Idrettslag',
    u'FROL':u'Frol Idrettslag',
    u'FROSTA':u'Frosta Idrettslag',
    u'FRLND':u'Frøyland Idrettslag',
    u'FUR':u'Furuset Allidrett IF',
    u'FYLL':u'Fyllingen Idrettslag',
    u'FRDE':u'Førde Idrettslag',
    u'GAU':u'Gausdal Friidrettsklubb',
    u'GEI':u'Geilo Idrettslag',
    u'GEIR':u'Geiranger Idrettslag',
    u'GJER':u'Gjerpen Idrettsforening',
    u'GJERS':u'Gjerstad Idrettslag',
    u'GJDAL':u'Gjesdal Idrettslag',
    u'GJFK':u'Gjøvik Friidrettsklubb',
    u'GJVIK':u'Gjøvik Friidrettsklubb 2',
    u'GLO':u'Gloppen Friidrettslag',
    u'GOL':u'Gol Idrettslag',
    u'GRON':u'Grong Idrettslag',
    u'GRO':u'Groruddalen Friidrettsklubb',
    u'GRUE':u'Grue Idrettslag',
    u'GTI':u'GTI Friidrettsklubb',
    u'GUI':u'Gui Sportsklubb - Friidrett',
    u'GUL':u'Gulset Idrettsforening',
    u'HAB':u'HAB IL',
    u'HADE':u'Hadeland Friidrettsklubb',
    u'HAGA':u'Haga Idrettsforening ',
    u'HAL':u'Halden Idrettslag',
    u'HALMO':u'Halmsås & Omegn Skilag',
    u'HALSA':u'Halsa Idrettslag',
    u'HIL':u'Hamar Idrettslag Hovedlaget',
    u'HANNEV':u'Hannevikas Idrettslag',
    u'HARDB':u'Hardbagg Idrettslag',
    u'HAREI':u'Hareid Idrettslag',
    u'HARE':u'Harestua Idrettslag',
    u'HATT':u'Hattfjelldal Idrettslag',
    u'HAUGN':u'Haugen Idrettslag',
    u'HAUGR':u'Haugerud Idrettsforening',
    u'HAUGF':u'Haugesund Idrettslag Friidrett',
    u'HAUGT':u'Haugesund Triathlon Klubb',
    u'HAV':u'Havørn Allianseidrettslag',
    u'HEGGF':u'Heggedal Friidrettsklubb',
    u'HEGGI':u'Heggedal Idrettslag',
    u'HELLU':u'Hell Ultraløperklubb',
    u'HEM':u'Heming Idrettslaget',
    u'HENN':u'Henning I L',
    u'HERA':u'Herand Idrettslag',
    u'HERK':u'Herkules Friidrett',
    u'HERY':u'Herøy Idrettslag',
    u'HIN':u'Hinna Friidrett',
    u'HITF':u'Hitra Friidrettsklubb',
    u'HITL':u'Hitra Løpeklubb',
    u'HOB':u'Hobøl Idrettslag',
    u'HOF':u'Hof Idrettslag',
    u'HOL':u'Hol Idrettslag',
    u'HOLMS':u'Holmemstranda Idrettslag',
    u'HOLUM':u'Holum Idrettslag',
    u'HMLV':u'Hommelvik Idrettslag',
    u'HOPE':u'Hope Idrettslag',
    u'HORNI':u'Hornindal Idrettslag',
    u'HORFR':u'Horten Friidrettsklubb',
    u'HUG':u'Huglo Idrettslag',
    u'HURD':u'Hurdal Idrettslag',
    u'HVAM':u'Hvam Idrettslag',
    u'HVFO':u'Hvittingfoss Idrettslag',
    u'HYEN':u'Hyen Idrettslag',
    u'HYLLS':u'Hyllestad Idrettslag',
    u'HSI':u'Høybråten og Stovner IL',
    u'HDMO':u'Høydalsmo Idrottslag',
    u'FJELLO':u'I.l Fjellørnen',
    u'FRAMS':u'I.L. Framsteg',
    u'NORSA':u'I.L. Norna Salhus',
    u'NYBR':u'I.L. Nybrott',
    u'IDD':u'Idd Sportsklubb',
    u'BIRK':u'Idrettsforeningen Birkebeineren',
    u'FRAM':u'Idrettsforeningen Fram',
    u'HELLA':u'Idrettsforeningen Hellas',
    u'NJAAL':u'Idrettsforeningen Njaal',
    u'STUR':u'Idrettsforeningen Sturla',
    u'IFORN':u'Idrettsforeningen Ørn',
    u'BJARG':u'Idrettslaget Bjarg',
    u'ILBJ':u'Idrettslaget Bjørn',
    u'DLBR':u'Idrettslaget Dalebrand',
    u'DYREV':u'Idrettslaget Dyre Vaa',
    u'EXPR':u'Idrettslaget Express',
    u'FORSK':u'Idrettslaget Forsøk',
    u'FRI':u'Idrettslaget Fri',
    u'GNE':u'Idrettslaget Gneist',
    u'HOLE':u'Idrettslaget Holeværingen',
    u'BULT':u'Idrettslaget I Bondeungdomslaget I Tromsø',
    u'ILAR':u'Idrettslaget Ilar',
    u'IVRIG':u'Idrettslaget Ivrig',
    u'JARD':u'Idrettslaget Jardar',
    u'JUT':u'Idrettslaget Jutul',
    u'ILROS':u'Idrettslaget Ros',
    u'RUNAR':u'Idrettslaget Runar',
    u'ILSAN':u'Idrettslaget Sand',
    u'SANDV':u'Idrettslaget Sandvin',
    u'SKADE':u'Idrettslaget Skade',
    u'SKJA':u'Idrettslaget Skjalg',
    u'SYR':u'Idrettslaget Syril',
    u'TRY':u'Idrettslaget Trysilgutten',
    u'GULA':u'Idrottslaget Gular Bygdeungdomen I Bergen',
    u'ILIBUL':u'IDROTTSLAGET I BUL',
    u'ILBUL':u'IDROTTSLAGET I BUL 2',
    u'JOT':u'Idrottslaget Jotun',
    u'IDUN':u'Idun Idrettslag',
    u'EIKKV':u'If Eiker Kvikk',
    u'KAVE':u'IF Kamp/Vestheim',
    u'KLYP':u'If Klypetussen',
    u'GRANE':u'Ik Grane Arendal Friidrett',
    u'HIND':u'IK Hind',
    u'IKORN':u'Ikornnes Idrettslag',
    u'AASG':u'IL Aasguten',
    u'ALVI':u'IL Alvidra',
    u'ILBEV':u'IL Bever`n',
    u'BRODD':u'IL Brodd',
    u'FLV':u'IL Flåværingen',
    u'GRY':u'IL Gry',
    u'ILNOR':u'IL Norodd',
    u'PIO':u'IL Pioner Friidrett',
    u'POL':u'IL Polarstjernen',
    u'SAMH':u'IL Samhald',
    u'SANT':u'IL Santor',
    u'STKAM':u'IL Stålkameratene',
    u'TRIUM':u'IL Triumf',
    u'VIND':u'Il Vindbjart',
    u'VING':u'IL Vinger',
    u'INDRY':u'Inderøy Idrettslag',
    u'INN':u'Innstranda IL',
    u'INSTA':u'International School of Stavanger',
    u'ISFJO':u'Isfjorden Idrettslag',
    u'JOND':u'Jondalen Idrettslag',
    u'JVTN':u'Jægervatnet Idrettslag',
    u'JIL':u'Jøa Idrettslag',
    u'JLSTE':u'Jølster Idrettslag',
    u'KAUP':u'Kaupanger Idrettslag',
    u'KFUM':u'Kfum-kameratene Oslo',
    u'KJ':u'Kjelsås Idrettslag',
    u'KLPP':u'Klepp Idrettslag',
    u'KLK':u'Klæbu Løpeklubb',
    u'KLIL':u'Kløfta Idrettslag',
    u'KLBK':u'Kolbukameratene I L',
    u'KOLL':u'IL Koll',
    u'KLVIL':u'Kolvereid Idrettslag',
    u'KNGSB':u'Kongsberg Idrettsforening',
    u'KNGSV':u'Kongsvinger IL Friidrett',
    u'KOP':u'Kopervik Idrettslag',
    u'KORG':u'Korgen Idrettslag',
    u'KRAG':u'Kragerø IF Friidrett',
    u'KRAAK':u'Kråkerøy Idrettslag',
    u'KRSTD':u'Kråkstad Idrettslag',
    u'KRL':u'Kristiansand Løpeklubb',
    u'KIF':u'Kristiansands Idrettsforening Friidrett',
    u'KRHER':u'Krødsherad Idrettslag',
    u'KVINES':u'Kvinesdal Idrettslag',
    u'KVFJ':u'Kvæfjord Idrettslag',
    u'KYRK':u'Kyrksæterøra Idrettslag Kil',
    u'LAKS':u'Laksevåg Turn og Idrettslag',
    u'LALM':u'Lalm Idrettslag',
    u'LAM':u'Lambertseter IF',
    u'LANGS':u'Langesund Sykle- og triathlonklubb',
    u'LNKEIL':u'Lånke Idrettslag',
    u'LRVK':u'Larvik Turn & Idrettsforening',
    u'LEINS':u'Leinstrand Idrettslag',
    u'LENA':u'Lena Idrettsforening',
    u'LIERN':u'Lierne Idrettslag',
    u'LIF':u'Lillehammer Idrettsforening',
    u'LILLS':u'Lillesand Idrettslag',
    u'LISTA':u'Lista Idrettslag',
    u'LODD':u'Loddefjord IL',
    u'LFTR':u'Lofoten Triatlonklubb',
    u'LOM':u'Lom Idrettslag',
    u'LUND':u'Lundamo Idrettslag',
    u'LUNDH':u'Lundehøgda IL',
    u'LUST':u'Luster Idrettslag',
    u'LYE':u'Lye Idrettslag',
    u'LYN':u'Lyn Ski',
    u'LNGD':u'Lyngdal Idrettslag',
    u'LYKA':u'Lyngen/ Karnes Il',
    u'LYNGO':u'Lyngstad og Omegn Idrettslag',
    u'LRSKG':u'Lørenskog Friidrettslag',
    u'LFK':u'Løten Friidrett',
    u'LTN':u'Løten Friidrett 2',
    u'MALM':u'Malm IL',
    u'MLSEL':u'Målselv Idrettslag',
    u'MALV':u'Malvik Idrettslag',
    u'MAAL':u'Måløy Idrettslag Hovedstyre',
    u'MAHA':u'Mandal & Halse I.l.',
    u'MNDL':u'Måndalen Idrettslag',
    u'MABY':u'Markabygda Idrettslag',
    u'MARKA':u'Markane Idrettslag',
    u'MARNA':u'Marnardal Idrettslag',
    u'MEDKI':u'Medkila Skilag',
    u'MELD':u'Meldal Idrettslag',
    u'MELHU':u'Melhus Idrettslag',
    u'MDSND':u'Midsund Idrettslag',
    u'MJSD':u'Mjøsdalen IL',
    u'MOD':u'Modum Friidrettsklubb',
    u'MOELV':u'Moelven Idrettslag',
    u'MOI':u'Moi Idrettslag',
    u'MOLDE':u'Molde og Omegn Idrettsforening',
    u'OLYMP':u'Molde Olymp',
    u'MOITU':u'Moltustranda Idrettslag',
    u'MOSJ':u'Mosjøen Friidrettsklubb',
    u'MOSS':u'Moss Idrettslag',
    u'MOSV':u'Mosvik Idrettslag',
    u'MUIL':u'MUIL - Mefjordvær Ungdoms- og Idrettslag',
    u'NAML':u'Namdal løpeklubb',
    u'NAMDA':u'Namdalseid Idrettslag',
    u'NAMSE':u'Namsen Fif',
    u'NANN':u'Nannestad Idrettslag',
    u'NAR':u'Narvik Idrettslag',
    u'NESB':u'Nesbyen Idrettslag',
    u'NESO':u'Nesodden IF',
    u'NES':u'Nesøya Idrettslag',
    u'NID':u'Nidelv Idrettslag',
    u'NISS':u'Nissedal Idrettslag',
    u'NITT':u'Nittedal Idrettslag',
    u'NRDKJ':u'Nordkjosbotn Idrettslag',
    u'NEIDS':u'Nordre Eidsvoll Idrettslag',
    u'NFJEL':u'Nordre Fjell Friidrett',
    u'NLAND':u'Nordre Land Idrettslag',
    u'NTRY':u'Nordre Trysil IL',
    u'NORIL':u'Nordøy Idrettslag',
    u'NORR':u'Norrøna IL',
    u'NRUN':u'Northern Runners',
    u'NTNUI':u'NTNUI - Norges Teknisk-Naturvitenskapelige Universitets Idrettsforening',
    u'NYSK':u'Nydalens Skiklub',
    u'NYKIR':u'Nykirke Idrettsforening',
    u'NTTRY':u'Nøtterøy Idrettsforening',
    u'ODDA':u'Odda Idrettslag',
    u'OGND':u'Ogndal Idrettslag Hovedlaget',
    u'OLD':u'Olden Idrettslag',
    u'OLDA':u'Olderdalen Idrettsklubb',
    u'OPPD':u'Oppdal IL Hovedlaget',
    u'OPP':u'Oppegård Idrettslag',
    u'OPSL':u'Oppsal Idrettsforening',
    u'OPST':u'Oppstad Idrettslag',
    u'OPPST':u'Oppstad Idrettslag 2',
    u'OPSTR':u'Oppstryn Idrettslag',
    u'OPPT':u'Opptur Motbakkeklubb',
    u'ORKA':u'Orkanger Idrettsforening',
    u'ORKD':u'Orkdal Idrettslag',
    u'ORRE':u'Orre Idrettslag',
    u'OS':u'Os Idrettslag',
    u'OSTU':u'Os Turnforening',
    u'FRII':u'OSI Friidrett',
    u'POLIT':u'Oslo Politis Idrettslag',
    u'OSI':u'Oslostudentenes Idrettsklubb',
    u'OST':u'Osterøy Idrottslag',
    u'OTRA':u'Otra IL',
    u'OTTE':u'Ottestad Idrettslag',
    u'OTKS':u'Ottestad Kast og Styrkeløft',
    u'OVRH':u'Overhalla Idrettslag',
    u'PORS':u'Porsanger Idrettslag',
    u'RANA':u'Rana Friidrettsklubb',
    u'RAN':u'Ranheim Idrettslag',
    u'RAU':u'Raufoss IL Friidrett',
    u'RAUM':u'Raumnes & Årnes Idrettslag',
    u'RE':u'Re Friidrettsklubb',
    u'READY':u'Ready Idrettsforeningen',
    u'RENA':u'Rena Idrettslag',
    u'RENDA':u'Rendalen Idrettslag',
    u'RENB':u'Rennebu Idrettslag',
    u'RIND':u'Rindal Idrettslag',
    u'RING':u'Ringerike Friidrettsklubb',
    u'RIS':u'Risør Idrettslag',
    u'RJU':u'Rjukan Idrettslag',
    u'ROGNE':u'Rogne Idrettslag',
    u'ROMFR':u'Romerike Friidrett',
    u'ROMUL':u'Romerike Ultraløperklubb',
    u'ROMRA':u'Romsdal Randoneklubb',
    u'ROSEN':u'Rosendal Turnlag',
    u'ROYAL':u'Royal Sport',
    u'RUS':u'Rustad Idrettslag',
    u'RYGGE':u'Rygge Idrettslag',
    u'RIL':u'Røa Allianseidrettslag',
    u'RDIL':u'Røldal Idrettslag',
    u'ROSIL':u'Røros Idrettslag',
    u'RKEN':u'Røyken UIL',
    u'SALA':u'Salangen IF Friidrett',
    u'SAMN':u'Samnanger Idrettslag',
    u'SANTU':u'Sandane Turn og Idrettslag',
    u'STIF':u'SANDEFJORD TURN & IDRETTSFORENING',
    u'SAND':u'Sandnes Idrettslag',
    u'SNDI':u'Sandnes Idrettslag 2',
    u'SNDSJ':u'Sandnessjøen Idrettslag',
    u'SARP':u'Sarpsborg Allianseidrettslag',
    u'SAUD':u'Sauda Idrettslag',
    u'SAUL':u'Sauland Idrettslag',
    u'SELB':u'Selbu IL',
    u'SELJE':u'Selje Idrettslag',
    u'SELJO':u'Seljord Idrettslag',
    u'SELS':u'Selsbakk Idrettsforening',
    u'SEM':u'Sem Idrettsforening',
    u'SIGFR':u'Sigdal Friidrettsklubb',
    u'SIGSK':u'Sigdals Skiklub',
    u'SILJ':u'Siljan Idrettslag',
    u'SIRMA':u'Sirma Il',
    u'SJET':u'Sjetne Idrettslag',
    u'VEDA':u'Sk Vedavåg Karmøy',
    u'VID':u'SK Vidar',
    u'SKAGE':u'Skagerrak Sportsklubb',
    u'SKLA':u'Skåla Idrettslag',
    u'SKRPH':u'Skarphedin IL',
    u'SKAU':u'Skaubygda Il',
    u'SKAUN':u'Skaun Idrettslag',
    u'SKI':u'Ski IL Friidrett',
    u'SKJK':u'Skjåk IL',
    u'SKJO':u'Skjoldar Il',
    u'SKOGN':u'Skogn Idrettslag',
    u'SKO':u'Skotterud Idrettslag',
    u'SKREIA':u'Skreia Idrettslag',
    u'SNSA':u'Snåsa Idrettslag',
    u'SNGG':u'Snøgg Friidrett',
    u'SIL':u'Sogndal Idrettslag',
    u'SOKND':u'Sokndal Friidrettsklubb',
    u'SOLA':u'Sola Friidrett',
    u'SOLN':u'Solnut IL',
    u'SORTL':u'Sortland Friidrettsklubb',
    u'SOT':u'Sotra Sportsklubb',
    u'SPILL':u'Spillum Idrettslag',
    u'SPRD':u'Spiridon Langløperlag',
    u'SPJVK':u'Spjelkavik og Omegn Friidrettsklubb',
    u'KRAFT':u'Sportsklubben Kraft',
    u'RYE':u'Sportsklubben Rye',
    u'VIDAR':u'Sportsklubben Vidar',
    u'SPYDE':u'Spydeberg IL',
    u'STJIL':u'Staal Jørpeland IL',
    u'STAD':u'Stadsbygd IL',
    u'STRHEI':u'Stårheim Idrettslag',
    u'STDIF':u'Stavanger Døve-Idrettsforening',
    u'STAVA':u'Stavanger Friidrettsklubb',
    u'STAVIF':u'Stavanger Idrettsforening Allianseidrettslag - Friidrett',
    u'STEGA':u'Stegaberg Idrettslag',
    u'STEIN':u'Stein Friidrettsklubb',
    u'STEKJ':u'Steinkjer Friidrettsklubb',
    u'STSK':u'Stettevik Sportsklubb',
    u'STJF':u'Stjørdal Fridrettsklubb',
    u'STJP':u'Stjørdal Paraidrettslag',
    u'STJB':u'Stjørdals-Blink IL',
    u'STOKK':u'Stokke Idrettslag',
    u'STOKM':u'Stokmarknes Idrettslag',
    u'STO':u'Stord Idrettslag',
    u'STOFJ':u'Storfjord idrettslag',
    u'STRIL':u'Stranda Idrottslag',
    u'STRAB':u'Strandebarm Idrettslag',
    u'STRA':u'Stranden Idrettslag',
    u'STRAU':u'Straumsnes Idrettslag',
    u'STRI':u'Strindheim Idrettslag',
    u'STRY':u'Stryn Turn og Idrettslag',
    u'STREN':u'Støren Sportsklubb',
    u'SUNND':u'Sunndal IL Friidrett',
    u'SURN':u'Surnadal Idrettslag',
    u'SVTU':u'Svalbard Turn Idrettslag',
    u'SVARS':u'Svarstad Idrettslag',
    u'SVEIO':u'Sveio Idrettslag',
    u'SVEL':u'Svelgen Turn og Idrettsforening',
    u'SVINT':u'Svint IL',
    u'SVORK':u'SVORKMO N.O.I.',
    u'SYKK':u'Sykkylven Idrottslag',
    u'SYLL':u'Sylling Idrettsforening',
    u'SDAL':u'Sædalen Idrettslag',
    u'GRAA':u'Sætre Idrætsforening Graabein',
    u'STIL':u'Søfteland Turn & Idrettslag',
    u'SGNE':u'Søgne Idrettslag',
    u'SMNA':u'Sømna Idrettslag',
    u'SNDLA':u'Søndre Land IL Friidrett',
    u'SAAL':u'Søre Ål Idrettslag',
    u'SRILD':u'Sørild Fridrettsklubb',
    u'SRKDL':u'Sørkedalens Idrettsforening',
    u'HOVD':u'T I L Hovding',
    u'TAMSAN':u'Tamil Sangam IL',
    u'TING':u'Tingvoll Friidrettsklubb',
    u'TJAL':u'IK Tjalve',
    u'TJØLL':u'Tjølling Idrettsforening',
    u'TJI':u'Tjøme Idrettslag',
    u'TJL':u'Tjøme Løpeklubb',
    u'TOL':u'Tolga Idrettslag',
    u'TOMR':u'Tomrefjord Idrettslag',
    u'TORO':u'Torodd IF',
    u'TORVI':u'Torvikbukt Idrettslag',
    u'TREU':u'Treungen Idrettslag',
    u'TRIO':u'Trio idrettslag',
    u'TRF':u'Tromsø Friidrettsklubb',
    u'TRL':u'Tromsø Løpeklubb',
    u'TRS':u'Tromsø Svømmeklubb',
    u'TROO':u'Trondheim & Omegn Sportsklubb',
    u'TROF':u'Trondheim Friidrett',
    u'TSK':u'Trøgstad Skiklubb',
    u'TUIL':u'TUIL Tromsdalen Friidrett',
    u'TVEDE':u'Tvedestrand Turn & Idrettsforening',
    u'TYR':u'Tyrving Idrettslag',
    u'TNSBF':u'Tønsberg Friidrettsklubb',
    u'TRBIL':u'Tørvikbygd Idrettslag',
    u'TYEN':u'Tøyen Sportsklubb',
    u'ULLK':u'Ullensaker/Kisa IL Friidrett',
    u'ULKI':u'Ullensaker/Kisa IL Friidrett 2',
    u'UND':u'Undheim Idrettslag',
    u'URFRI':u'Urædd Friidrett',
    u'UTL':u'Utleira Idrettslag',
    u'VAAL':u'Vaaler Idrettsforening',
    u'VA':u'Vadsø Atletklubb',
    u'VTF':u'Vadsø Turnforening (Vtf)',
    u'VGAA':u'Vågå Idrettslag',
    u'VIL':u'Vågstranda Idrettslag',
    u'VALK':u'Valkyrien Idrettslag',
    u'VALL':u'Valldal Idrettslag',
    u'VAL':u'Vallset IL',
    u'VAR':u'Varegg Fleridrett',
    u'VARH':u'Varhaug Idrettslag',
    u'VART':u'Varteig Idrettslag',
    u'VEG':u'Vegårshei Idrettslag',
    u'VELD':u'Veldre Friidrett',
    u'VELL':u'Velledalen Idrettslag',
    u'VERD':u'Verdal Friidrettsklubb',
    u'VESTB':u'Vestby Idrettslag',
    u'VESTF':u'Vestfossen Idrettsforening',
    u'VSPON':u'Vestre Spone IF',
    u'VIKIL':u'Vik Idrettslag',
    u'VIKAN':u'Vikane IL',
    u'VIK':u'Viking Turn og Idrettsforening',
    u'VIKSD':u'Viksdalen Idrettslag',
    u'VILJ':u'Viljar, IL',
    u'VNDIL':u'Vind Idrettslag',
    u'VINDA':u'Vindafjord Idrettslag',
    u'VINJE':u'Vinje Idrottslag',
    u'VOLL':u'Vollan Idrettsklubb',
    u'VOSS':u'Voss Idrottslag',
    u'YTTER':u'Ytterøy Idrettslag',
    u'ORJIL':u'Ørje Idrettslag',
    u'ORSTA':u'Ørsta Idrettslag',
    u'OMARSJ':u'Østmarka Marsjklubb',
    u'OTRET':u'Øyer/Tretten Idrettsforening',
    u'OSLID':u'Øystre Slidre Idrettslag'
    }

    return club_names[club_code]
   
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
            'HJ'     : 'Høyde'             , 
            'PV'     : 'Stav'              , 
            'LJ'     : 'Lengde'            , 
            'TJ'     : 'Tresteg'           , 
            'SP'     : 'Kule'              , 
            'DT'     : 'Diskos'            , 
            'HT'     : 'Slegge'            , 
            'JT'     : 'Spyd'              , 
            'DEC'    : 'Tikamp'            , 
            'HEP'    : 'Sjukamp'           
            }
    return event_names[code]

#---------------------------------------
with open('downloads.json', 'r') as f: 
    j = json.load(f)

#print(type(j))
#print(j.keys())
#print(j['date'])
d  = j['date']
d2 = j['finishDate']
isodateformat = "%Y-%M-%d"
date = datetime.datetime.strptime(d, isodateformat)
date2 = datetime.datetime.strptime(d2, isodateformat)
bdate = datetime.datetime.strptime('2005-06-24', isodateformat)
#print(get_category(bdate,date,'F'))


meetname = j['fullName']
slug = j['slug']
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
    if 'teamId' in c.keys():
        t    = c['teamId']

    if 'gender' in c.keys():
        g = c['gender']
    if fn=='':
        ignore_bibs.append(bib)
    else:
        competitors[bib] = (fn, ln, dob, g, t)
        #print(bib, competitors[bib])



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
for e in j["events"]:
    event_code = e["eventCode"]
    if event_code not in e.keys():
        results[event_code] = {}
#       for u in e["units"]:
        trials = {}
        series = {}
        for pool, u in zip(range(len(e["units"])),e["units"]):
            #results[event_code] ={}
            for r in u["results"]:
                if "bib" in r.keys():
                    bib = r["bib"]
                
                if bib not in ignore_bibs:
                     bdate = competitors[bib][2]
                     g = competitors[bib][3]
                     cat = get_category(bdate,date,g)
                     if results[event_code].get(cat) == None:
                         results[event_code][cat] = {}
                     if results[event_code][cat].get(pool) == None:
                         results[event_code][cat][pool] = []
#                    x
                     if "performance" in r.keys():
                         res = r["performance"]

                     if "place" in r.keys():
                         pl = r["place"]
                    
#               print (bib, res, pl, poolnr)
                     results[event_code][cat][pool].append((bib, res, pl))
                     #print (bib, res, pl, pool)
#           poolnr = poolnr + 1
#           print (type(u['trials']))
#           print (u['trials'])
            for t in u['trials']:
                bib = t['bib']
                if trials.get(bib)==None:
                    trials[bib] = {}
                print(event_code, t)
                height = t['height']
                if trials[bib].get(height)==None:
                    trials[bib][height] = []
                trials[bib][height].append(t['result'])
            #print(trials)
            for bib in trials.keys():
                s = ''
                for height in sorted(trials[bib].keys() ):
                    #print(trials[bib][height])
                    s += height + '(' + ''.join(trials[bib][height]) + ') ' 
                s = s.replace('.',',')
                i = s.index('x')
                j = s.index('o')
                ij = min(i,j)
                #print(s.index('x'), s.index('o') )
                print(s[ij-5:])
                series[bib] = s[ij-5:]
            #print(trials)
        #print('T', trials)
#... write template for Results to xlsx workbook
wb = Workbook()
ws = wb.active
    
greenfont = Font(name='Calibri', color=xlcolors.GREEN)
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
for event in sorted(results.keys()):
    print(event)
    for cat in sorted(results[event].keys() ):
        ws["A%(row_counter)d"%vars()] = cat; arc = ws["A%(row_counter)d"%vars()]; arc.font=boldfont
        ws["B%(row_counter)d"%vars()] = event_name(event) ; brc = ws["B%(row_counter)d"%vars()]; brc.font=boldfont
        row_counter +=1
        #print(cat)
        heats = sorted(results[event][cat].keys() )
        for h, heat in zip(range(len(heats)), heats):
            print('Heat: %d'%(h+1))
            ws["A%(row_counter)d"%vars()] = "Heat:";  ws["B%(row_counter)d"%vars()] = h+1;  
            row_counter +=1
            sorted_result = sorted(results[event][cat][heat], key=lambda tup: tup[2])
            for i,r in zip(range(len(sorted_result)),sorted_result):
                bib = r[0]
                perf = r[1].replace('.',',')

                fn  = competitors[bib][0]
                ln  = competitors[bib][1]
                dob = competitors[bib][2]
                club = competitors[bib][4]
                print(i+1, fn+' '+ln, club, perf)
                ws["A%(row_counter)d"%vars()] = i+1
                #ws["B%(row_counter)d"%vars()] = bib
                ws["C%(row_counter)d"%vars()] = ' '.join((fn,ln))
                ws["D%(row_counter)d"%vars()] = dob.strftime('%Y')
                ws["E%(row_counter)d"%vars()] = club_name(club)
                ws["F%(row_counter)d"%vars()] = perf
                row_counter +=1
                ws["A%(row_counter)d"%vars()] = series[bib]
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
