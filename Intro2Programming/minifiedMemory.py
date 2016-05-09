import simplegui as s,random
def n():global s,t,c,u;s=t=0;c=2*range(8);random.shuffle(c);u=16*[1]   
def m(p):
 global s,a,b,t;i=p[0]/50	
 if u[i]:
  u[i]=0
  if s>1:
   u[a]=u[b]=c[a]!=c[b];s=1;a=i
  elif s:s=2;b=i;t+=1
  else:s=1;a=i
def d(v):
 l.set_text("Turns: %d"%t)
 for i in range(16):
  j=50*i+25
  if u[i]:v.draw_line((j,0),(j,98),48,"tan") 
  else:v.draw_text(str(c[i]),(j-9,60),34,"red")
f=s.create_frame("",800,99)
f.add_button("Reset",n)
l=f.add_label("")
f.set_mouseclick_handler(m)
f.set_draw_handler(d)
n()
f.start()