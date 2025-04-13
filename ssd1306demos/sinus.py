from math import sin, radians
from fbi import roundint

def main():
  sleep(0.5)  
  show=o.show
  fill=o.fill
  pixel=o.pixel
  HHEIGHT=(HEIGHT//2)-1
  stepx=360/WIDTH
  ly=bytearray(WIDTH)
  for x in range(WIDTH):
    ly[x]=roundint((sin(radians(x*stepx))*HHEIGHT)+HHEIGHT)+1
  i=0  
  while True:    
    show()
    fill(0)
    for x in range(WIDTH):
      pixel(x,ly[(x+i)%WIDTH],1)
      pixel(x,HHEIGHT,1)
    i=(i-1)%WIDTH

main()
