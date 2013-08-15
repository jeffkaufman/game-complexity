b,p=[[' ']*19 for x in range(19)],set()
def v(x,y):return 0<=x<19 and 0<=y<19
def j(x,y):return [(xv,yv) for xv,yv in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)] if v(xv,yv)]
def z():return tuple(map(tuple,b))
def r(x,y,t):
 C,V=b[x][y],set()
 def h(xh,yh):
  if (xh,yh) in V:return 0
  V.add((xh,yh))
  if b[xh][yh]==t:return 1
  if b[xh][yh]==C:
   for xv,yv in j(xh,yh):
    if h(xv,yv):return 1
  return 0
 return h(x,y)
def sf(x,y):
 if b[x][y]!=' ':return b[x][y]
 r_b=r(x,y,'b')
 r_w=r(x,y,'w')
 if r_b and r_w:return ' '
 if r_b:return 'b'
 if r_w:return 'w'
 return ' '
def c(x,y,C):
 if b[x][y]!=C:return
 b[x][y]=' '
 for xv,yv in j(x,y):c(x,y)
def cc(C):
 for x in range(19):
  for y in range(19):
   if b[x][y]==C:
    if not r(x,y,' '):c(x,y,C)
def t(C):
 while 1:
  n=raw_input(C+'>')
  if n=='p':return 0
  try:
   x,y=n.split()
   x,y=int(x),int(y)
  except ValueError:continue
  if not v(x,y):continue
  if b[x][y]!=' ':continue
  break
 p.add(z())
 b[x][y]=C
 cc('b' if C=='w' else 'w')
 cc(C)
 if z() in p:raise Exception('r')
 return 1
mb,mw=1,1
while mb or mw:
 mb=t('b')
 if mb or mw:mw=t('w')
ss={' ':0,'b':0,'w':0}
for x in range(19):
 for y in range(19):ss[sf(x,y)]+=1
if ss['b']==ss['w']:print 't'
elif ss['b']>ss['w']:print 'b'
else:print 'w'

