b=[list(R) for R in [' w w w w','w w w w ',' w w w w','. . . . ',' . . . .','b b b b ',' b b b b','b b b b ']]
def v(x,y):return x>=0 and x<8 and y>=0 and y<8
def c(x,y):return b[x][y].lower()
def j(x,y,d):
 dn=1 if c(x,y)=='w' else -1
 def h(f):return [(xv,yv) for (xv,yv) in [(x+(dn*f*d),y+d),(x+(dn*f*d),y-d)] if v(xv,yv)]
 return h(1)+(h(-1) if b[x][y] in ['W','B'] else [])
def e(C):
 for xs in range(8):
  for ys in range(8):
   if c(xs,ys)==C:
    for xe,ye in j(xs,ys,2):
     if c(xe,ye)=='.':
      if c((xs+xe)/2,(ys+ye)/2) not in [C,'.']:return 1
def m(C,xs,ys,xe,ye,xj,yj):
 def am():
  b[xe][ye]=b[xs][ys]
  b[xs][ys]='.'
  if C=='w' and xe==7:b[xe][ye]='W'
  if C=='b' and xe==0:b[xe][ye]='B'
 if ((not (v(xs,ys) and v(xe,ye) and c(xs,ys)==C and b[xe][ye]!=' ' and c(xe,ye)=='.')) or (xj!=-1 and (xs!=xj or ys!=yj))):return 0
 if (xe,ye) in j(xs,ys,1):
  if xj!=-1 or e(C):return 0
  am()
  return 1
 if (xe,ye) in j(xs,ys,2):
  jx,jy=(xs+xe)/2,(ys+ye)/2
  if c(jx,jy) in [C,'.']:return 0
  b[jx][jy]='.'
  am()
  return 2
 return 0
def t(C):
 xj,yj=-1,-1
 while 1:
  h=raw_input(C+'>')
  if xj!=-1 and h=='p' and not e(C):break
  if h=='r':raise Exception(C+' L')
  try:xs,ys,xe,ye=[int(i) for i in h.split()]
  except ValueError:continue
  R=m(C,xs,ys,xe,ye,xj,yj)
  if R==2:xj,yj=xe,ye
  if R==1:break
while 1:t('b'),t('w')

