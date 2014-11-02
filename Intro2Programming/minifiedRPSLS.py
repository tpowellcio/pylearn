import random
w="player"
x="computer"
y="chooses"
z="wins"
u=["rock","Spock","paper","lizard","scissors"]
def n(i):return u.index(i)
def r(i):
 print"\n",w,y,i
 c=random.randint(0,4)
 print x,y,u[c]
 g=(c-n(i))%5
 if g==0:print w,"and",x,"tie"
 elif g<3:print x,z
 else:print w,z
for i in range(5):r(u[i])