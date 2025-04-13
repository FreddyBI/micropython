from math import sin, radians
from fbi import roundint

def main():
  show=o.show
  fill=o.fill
  pixel=o.pixel
  vline=o.vline
  hline=o.hline
  HHEIGHT=(HEIGHT//2)-1
  stepx=360/WIDTH
  ly=bytearray(WIDTH)
  for x in range(WIDTH):
    ly[x]=roundint((sin(radians(x*stepx))*HHEIGHT)+HHEIGHT)+1
  i=0  
  while True:    
    show()
    fill(0)
    hline(0,HHEIGHT,WIDTH,1)
    for x in range(WIDTH):
      y=ly[(x+i)%WIDTH]  
      if y < HHEIGHT:  
        vline(x,y,HHEIGHT-y,1)
      else:
        vline(x,HHEIGHT,y-HHEIGHT,1)  
    i=(i-1)%WIDTH
main()
