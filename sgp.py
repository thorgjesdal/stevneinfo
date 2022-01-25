import random
A = ["1500 M", "LJ M", "DT M", "1500 W", "HJ W", "PV W"]
B = ["100 M", "400 M", "800 M" "400H M", "TJ M", 
     "100 W", "400 W", "800 W" "LJ W", "SP W"] 
A_events = random.sample(A,k=3)
A_places = [random.randint(1,3) for iter in range(3)]
print ( A_events )
print ( A_places )
B_events = random.sample(B,k=2)
B_places = [random.randint(1,2) for iter in range(2)]
print ( B_events )
print ( B_places )
