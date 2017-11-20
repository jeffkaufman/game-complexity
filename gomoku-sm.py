w,b=[],[]
def o((x,y),s,(v,u)):
 if (x,y) in s:return o((x+v,y+u),s,(v,u))
 if v:return x
 return y
d=((0,1),(1,0),(1,1),(-1,1))
def W(m,s):
 for (x,y) in d:
  if o(m,s,(x,y))-o(m,s,(-x,-y))>5:return 1
 return 0
def t(c,p):
 while 1:
  C=raw_input(c+'>')
  try:
   x,y=C.split()
   m=(int(x),int(y))
  except ValueError:continue
  if m in b+w:continue
  p.append(m)
  if W(m,p):raise Exception(c)
  break
while 1:t("b",b),t("w",w)
