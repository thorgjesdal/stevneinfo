import json

fname = 'tt.json'

with open(fname, 'r') as f:
    j = json.load(f)

print ( j.keys() )

events = []
for t in j['timetable']:
    event = t['eventName'] 
    day   = t['day']
    etime = t['scheduledStartTime']
    runde = t['round']
    heat  = t['heat']
    
    events.append( (day, etime, event, runde, heat ) )

events = sorted(events, key = lambda k: ( k[0], k[1] ) )
print(events)
days = ['Fredag', 'Lørdag', 'Søndag']
d = 0
for e in events:
    if e[0] > d:
        d = e[0]
        print( days[d-1] )
        continue
    if e[4] > 1:
        continue
    #print(e)
    line = f'{e[1]}\t{e[2]}'
    if e[3]>1:
        line +=' Finale'
    #line += '\n'
    print(line)



