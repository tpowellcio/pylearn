import simplegui as S,math as M,random as R
_="_blue"
y="http://commondatastorage.googleapis.com/codeskulptor-assets/"
j=y+"sounddogs/"
q=y+"lathrop/"
z=m=t=s=0
W=800
H=600
C=[W/2,H/2]
l=3
Z=[0,1]
L=lambda s:S.load_image(s+".png")
O=lambda s:S.load_sound(s)
r=lambda a,b:R.random()*(b-a)+a
A=lambda a:[M.cos(a),M.sin(a)]
h=O(j+"thrust.mp3")
def D(a,b,c,d,e,f,g=0):a.draw_image(b,c,d,e,f,g)
class I:
 def __init__(s,c,z,r=0,l=0,a=0):s.c=c;s.z=z;s.r=r;s.a=a;s.l=l if l else float('inf')
class X:
 def __init__(s,p,v,a,g,i,n,d=0):
  s.p=p;s.v=v;s.a=a;s.g=g;s.i=i;s.c=n.c;s.z=n.z;s.r=n.r
  if d:d.rewind();d.play()
 def d(s,c,a=0):D(c,s.i,[s.c[0]+a,s.c[1]],s.z,s.p,s.z,s.a)
 def w(s):s.a+=s.g;s.p[1]+=s.v[1];s.p[0]+=s.v[0];s.p[0]%=W;s.p[1]%=H
class T(X):
 def __init__(s,p,v,a,i,n):X.__init__(s,p,v,0,0,i,n);s.t=0
 def e(s):s.t=1-s.t;[h.rewind,h.play][s.t]()
 def f(a):
  global z;k=A(a.a);p=a.p[:];v=a.v[:]
  for i in Z:p[i]+=40*k[i];v[i]+=8*k[i]
  z=X(p,v,0,0,L(q+"shot2"),I([5,5],[10,10],3,50),O(j+"missile.mp3"))
 def d(s,c):X.d(s,c,s.z[0] if s.t else 0)
 def w(s):
  X.w(s)
  for i in Z:s.v[i]+=s.t*A(s.a)[i]/6;s.v[i]*=.98
def d(c):global t;t+=3;D(c,L(q+"nebula"+_),C,[W,H],C,[W,H]);B(c,-1);B(c,1);m.w();m.d(c);k.w();k.d(c);z.w();z.d(c);c.draw_text('Lives:'+str(l)+70*' '+'Score:'+str(s),[40,40],30,'tan')
def B(c,s):D(c,L(q+"debris2"+_),[320,240],C,((t/4)%W+s*W/2,H/2),(W,H))
def Y():global k;k=X([r(0,W),r(0,H)],[r(-2,2),r(-2,2)],0,r(-.2,.2),L(q+"asteroid"+_),I([45,45],[90,90],40))
def a(k,v=1):
 if k==39:m.g+=v*.1
 if k==37:m.g-=v*.1
 if k==38:m.e()
 if k*v==32:m.f()
f=S.create_frame("",W,H)
m=T([W/2,H/2],[0,0],0,L(q+"double_ship"),I([45,45],[90,90],35))
m.f()
Y()
f.set_draw_handler(d)
f.set_keydown_handler(a)
f.set_keyup_handler(lambda k:a(k,-1))
S.create_timer(W+H,Y).start()
f.start()