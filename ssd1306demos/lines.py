from random import randint
def testlines():
  o.fill(0)
  while True:
     x0=randint(0,WIDTH-1)
     x1=randint(0,WIDTH-1)
     y0=randint(0,HEIGHT-1)
     y1=randint(0,HEIGHT-1)
     o.line(x0,y0,x1,y1,1)
     o.show()
     o.line(x0,y0,x1,y1,0)
     
testlines()    
