from random import randint
def testlines():
  o.fill(0)
  while True:
     x=randint(0,WIDTH-2)
     y=randint(0,HEIGHT-2)
     lx=randint(1,WIDTH-x)
     ly=randint(1,HEIGHT-y)
     o.rect(x,y,lx,ly,1)
     o.show()
     o.rect(x,y,lx,ly,0)
    
testlines()    
