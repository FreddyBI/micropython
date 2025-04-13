# extention from framebuf micropython
import framebuf
from cfbi import ch

MONO_VLSB = framebuf.MONO_VLSB
MONO_HLSB = framebuf.MONO_HLSB
MONO_HMSB = framebuf.MONO_HMSB
RGB565 = framebuf.RGB565
GS2_HMSB = framebuf.GS2_HMSB
GS4_HMSB = framebuf.GS4_HMSB
GS8 = framebuf.GS8

def zoomchar(tox,toy,och,zx=2,zy=2):
    
  pix=och.pixel # b.pixel() have no problem with out of range
  
  # put pixel index in dic

  for y in range(8):
    pixon=False
    b=0
    l=0
    for x in range(8): # horizontal lines
      p=pix(x,y)
      if p : # pixel exist no up pixel exist
        if pixon is False:
          pixon=True
          b=x
          l=1
        else:
          l+=1  
      else:
        if l > 0:  
          yield (tox+(b*zx),toy+(y*zy),zx*l,zy)
        l=0
        pixon=False
    if l > 0 : 
      yield (tox+(b*zx),toy+(y*zy),zx*l,zy) 
      
def zoomtext(tox,toy,s,zx=2,zy=2):
      for i in range(len(s)):
        yield from zoomchar(tox,toy,ch(s[i]),zx,zy)
        tox+=zx*8
        
def swapcolor(c):
#
# swap 8 bits in 16 bit RGB565 color
# example RED -> '0b1111100000000000'
# swapcolor(RED) -> '0b11111000'
# use this funtion in FrameBuffer RGB565 for use in funtion blit_buffer from st7789 driver
# example:  
# o = tft_config.config(0)
# o.init()
# o.fill(BLUE)
#
# HEIGHT = o.height()
# WIDTH = o.width()
#
# b=bytearray(2*100*100)
# f=FrameBuffer(b,100,100,RGB565)
#
# f.fill(swapcolor(GREEN))
# o.blit_buffer(b,0,0,100,100)
#
  return (c<<8 & 0xFF00)|(c>>8 & 0x00FF)

class Framebuffbi(framebuf.FrameBuffer):

    def draw(self,genxy,c=1): # draw all data from generator drawfbi as pixel or line
    
       pix=self.pixel
       line=self.line
  
       def inrange(x,y):
          if x < 0 or x >= self.width:
             return False 
          if y < 0 or y >= self.height:
             return False
          return True
  
       for x,y in genxy:
         if x is None:
           for l in range(y):
             x,y = next(genxy)
             if l > 0:
               if prevx == x and prevy == y:
                 if inrange(x,y):  
                   pix(x,y,c) # o.pixel allready check in range
               else:
                 line(prevx,prevy,x,y,c) # o.line allready check in range
             prevx=x
             prevy=y
         else:
           if inrange(x,y):  
             pix(x,y,c) # o.pixel allready check in range

    def zoomtext(self,tox,toy,s,zx=2,zy=2,c=1,cbg=0,clean=True):
      if clean:
        self.fill_rect (tox,toy,len(s)*8*zx,8*zy,cbg)
      for parameters in zoomtext(tox,toy,s,zx,zy):
        self.fill_rect (*parameters,c)
    
