b,S=[],{'w':0,'b':0}
for x in range(62):
 b.append([])
 for y in range(62):b[-1].append(" ")
def v(x,y):return 0<=x<30 and 0<=y<30
def m(C,xs,ys,xe,ye):
 if not v(xs,ys) or not v(xe,ye): return 0
 if xs>xe:xs,xe=xe,xs
 if ys>ye:ys,ye=ye,ys
 if xs==xe and ye==ys+1:bx,by,ch=2*xs,2*ys+1,'-'
 elif ys==ye and xe==xs+1:bx,by,ch=2*xs+1,2*ys,'|'
 else:return 0
 if b[bx][by]!=' ':return 0
 b[bx][by]=ch
 def cs(x,y):
  if s(x,y):
   S[C]+=1
   return 1
 if ((ch=='-' and (cs(bx+1,by) or cs(bx-1,by))) or (ch=='|' and (cs(bx,by+1) or cs(bx,by-1)))):return 2
 return 1
def s(x,y):
 for xs,ys in [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]:
  if xs<0 or ys<0 or xs>62 or ys>62 or b[xs][ys]==' ':return 0
 return 1
def t(C):
 while 1:
  if S['w']+S['b']==841:raise Exception("b" if S['b']>S['w'] else ("w" if S['w']>S['b'] else "t"))
  h=raw_input(C+">")
  try:xs,ys,xe,ye=[int(i) for i in h.split()]
  except ValueError:continue
  r=m(C,xs,ys,xe,ye)
  if r==2:continue
  if r==1:break
while 1:t("w"),t("b")
