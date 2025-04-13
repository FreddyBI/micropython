from asyncfbi import *
from drawfbi import *
from random import randint

def main():
  sleep(0.5)  
  o.fill(0)
  a.add(do())
  a.run() 

def do():
   maxnr=2 
   while True:
    if a.nr < maxnr:
      a.add(p())
    yield    
   
def p():
   a.nr+=1
   zx=randint(3,5)
   x=randint(0,128-(zx*8))
   y=randint(0,64-(zx*8))
   char=chr(randint(65,90)) # from character A to Z
   deg=randint(0,359)
   midx=x+(zx*4)
   midy=y+(zx*4)
   do=randint(0,1)
   g=zoomtext(x,y,char,zx=zx,zy=zx,type=1)
   if do:    
     g=xydo(g,xyrotate,(deg,midx,midy))
   o.draw(g)
   o.show()
   yield from sleepms(randint(1,5)*100)
   g=zoomtext(x,y,char,zx=zx,zy=zx,type=1)
   if do:
     g=xydo(g,xyrotate,(deg,midx,midy))
   o.draw(g,0)   
   o.show()
   yield from sleepms(randint(1,5)*100)
   a.nr-=1
   
a=Async()
a.nr=0

main()
