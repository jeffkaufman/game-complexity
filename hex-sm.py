b,m=[],[0]
for x in range(10):
 b.append([])
 for y in range(10):b[-1].append(' ')
def v(x,y):return 0<=x<10 and 0<=y<10
def w(x,y,C):
 R,V=[0,0],set()
 def h(xs,ys):
  if b[xs][ys]!=C or (xs,ys) in V:return
  V.add((xs,ys))
  c=xs if C=='b' else ys
  if c==9:R[0]=1
  if c==0:R[1]=1
  for (xc,yc) in [(x+1,y),(x-1,y),(x-1,y+1),(x+1,y-1)]:
   if v(xc,yc):h(xc, yc)
  h(x,y)
  return r[0] and r[1]
def t(C):
 while 1:
  h=raw_input(C+">")
  try:
   x,y=h.split()
   x,y=int(x),int(y)
  except ValueError:continue
  if not v(x,y) or b[x][y] != ' ':continue
  b[x][y]=C
  m[0]+=1
  if w(x,y,C):raise Exception(C)
  if m[0]==100:raise Exception("draw")
  break
while 1:t('b'),t('w')

