"""
TODO:
      * sort per category
      * finish conflics list
      *
"""
import json
import pandas as pd
from collections import defaultdict
import pprint

# Load your JSON file
with open("nordicmasters.json") as f:
    data = json.load(f)

# Adapt this depending on structure:
# Expect list of entries with athlete_id, gender, event_name
entries = data["competitors"]  # adjust key if needed

# Build: gender -> athlete -> events
gender_map = {
    "M": defaultdict(set),
    "F": defaultdict(set)
}


for e in entries:
    athlete = e["competitorId"]
    gender = e["gender"]
    for v in e["eventsEntered"]:
        event = v["eventCode"]

        if gender in gender_map:
            gender_map[gender][athlete].add(event)

athletes = {}
for e in entries:
    athlete = e["competitorId"]
    name = e['fullName']
    athletes[athlete] = name
#print(athletes)


def sort_events(e):
    sort_order=('100', '150', '200', '300', '400', '600', '800', '1000', '1500', 'MILE', '2000', '3000', '5000', '10000',
                '60H', '80H', '100H', '110H', '200H', '300H', '400H', '1500SC', '2000SC', '3000SC', '3000W', '5000W',
                'HJ', 'PV', 'LJ', 'TJ', 'SP', 'DT', 'JT', 'HT','WT')
    return sort_order.index(e)

def build_matrix(athlete_events):
    # all events
    events = sorted({ev for evs in athlete_events.values() for ev in evs}, key=sort_events)


    #events.sort(key=sort_events)
    #print(events)

    # empty matrix
    df = pd.DataFrame(0, index=events, columns=events)

    # fill
    for ev1 in events:
        for ev2 in events:
            count = sum(
                1 for evs in athlete_events.values()
                if ev1 in evs and ev2 in evs
            )
            df.loc[ev1, ev2] = count

    return df

def build_and_save_conflicts_table(athlete_events):
    events = sorted({ev for evs in athlete_events.values() for ev in evs}, key=sort_events)
    #print ( athlete_events )

    conflicts = {}
    for ev1 in events:
        for ev2 in events:
            if ev1==ev2:
                continue
            if ev1 not in conflicts:
                conflicts[ev1] = {}
            for bib in athlete_events.keys():
                evs = athlete_events[bib]
                if ev1 in evs and ev2 in evs:
                    if ev2 not in conflicts[ev1]:
                        conflicts[ev1][ev2]=[]
                    conflicts[ev1][ev2].append(athletes[bib])

    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(conflicts)
     


    """
    # empty matrix
    df = pd.DataFrame( None, index=events, columns=events, dtype=object )

    print( 'test', df.loc['100','100']  )

    # fill
    for ev1 in events:
        for ev2 in events:
            count = sum(
                1 for evs in athlete_events.values()
                if ev1 in evs and ev2 in evs
            )
            df.loc[ev1, ev2] = count
"""

test = build_and_save_conflicts_table(gender_map["F"])

male_matrix = build_matrix(gender_map["M"])
female_matrix = build_matrix(gender_map["F"])

# Save results
male_matrix.to_csv("male_crosstable.csv")
female_matrix.to_csv("female_crosstable.csv")

print("Done! Files saved: male_crosstable.csv, female_crosstable.csv")
