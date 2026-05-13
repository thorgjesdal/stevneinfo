import json

fname = 'tt.json'

with open(fname, 'r') as f:
    j = json.load(f)

#print ( j.keys() )

events = []
for t in j['timetable']:
    event = t['eventName'] 
    day   = t['day']
    etime = t['scheduledStartTime']
    runde = t['round']
    heat  = t['heat']
    
    events.append( (day, etime, event, runde, heat ) )

events = sorted(events, key = lambda k: ( k[0], k[1] ) )
#print(events)
rounds = {}
for e in events:
    if e[2] not in rounds.keys():
        rounds[e[2]] = [e[3]]
    else:
        rounds[e[2]].append(e[3])
    rounds[e[2]] = list( set( rounds[e[2]]) ) 
#print('r', rounds)



days = ['Fredag', 'Lørdag', 'Søndag']
d = 0
for e in events:
    #print(e)
    if e[0] > d:
        d = e[0]
        print( days[d-1] )
        #continue
    if e[4] > 1:
        continue
    #print(e)
    line = f'{e[1]}\t{e[2]}'
    i = e[3]
    if i==1:
        if len(rounds[e[2]])>1:
            line +=' Forsøk'
    elif i>1:
        if i==2 and len(rounds[e[2]])> 2:
            line +=' Semifinale'
        else:
            line +=' Finale'
    print(line)



