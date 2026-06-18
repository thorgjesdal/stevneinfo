import json
import pandas as pd
from collections import defaultdict

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


def build_matrix(athlete_events):
    # all events
    events = sorted({ev for evs in athlete_events.values() for ev in evs})

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

male_matrix = build_matrix(gender_map["M"])
female_matrix = build_matrix(gender_map["F"])

# Save results
male_matrix.to_csv("male_crosstable.csv")
female_matrix.to_csv("female_crosstable.csv")

print("Done! Files saved: male_crosstable.csv, female_crosstable.csv")
