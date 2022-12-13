import random
#A = ["SP M", "SP M", "SP M", "HJ M", "HJ M", "HJ W", "SP W"]
#W = [7, 3, 1, 1]
#A = ["800 W", "400H W", "LJ W", "800 M", "DT M", "JT M"] 
#B = ["100 W", "400 W", "1500 W", "HJ W", "SP W", "100 M", "3000 M", "110H M", "400H M", "TJ M", "HT M"]
#     "100 W", "400 W", "800 W" "LJ W", "SP W"] 
A = ['SM', 'SW']
B=['U20M', 'U20W']
#A_events = random.choices(A, weights=W,k=3)
n=4
nA = random.randint(2,3)
nB = n-nA
#nA = 3
#nB= 2
print(nA,nB)

A_events = random.sample(A, k=nA)
A_places = [random.randint(1,5) for iter in range(nA)]
print ( A_events )
print ( A_places )
B_events = random.sample(B,k=nB)
B_places = [random.randint(1,3) for iter in range(nB)]
print ( B_events )
print ( B_places )
