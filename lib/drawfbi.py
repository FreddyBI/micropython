# for pixels on screen
# generate point(s) data: (x,y),(x,y).... x and y as integer example (10,15),(56,70)
# and or line(s) (None,numbercorners)(x,y),(x,y)..... example (None,5)(0,0),(10,0),(10,10),(0,10),(0,0)

from math import sqrt,sin,cos,radians,pi
from fbi import roundint
from cfbi import ch,rotatexy
from framebuffbi import zoomtext as _zoomtext

def xyroundint (x,y): # return (roundint(x),roundint(y))
  return (roundint(x),roundint(y))
  
def xyzoom(x,y,cx,cy,z): # zoom xy to cx,cy
  return xyroundint((x-cx)*z+cx,(y-cy)*z+cy)  

def xypixels(genxy): # convert generator line(s) in data to (x,y) pixel data
  for x,y in genxy:
     if x is None: # generate lines pixels
       for i in range(y):
         if i:
           x0,y0=x1,y1
           x1,y1=next(genxy)
           if y0 == y1: # hline
             for x in range(min(x0,x1),max(x0,x1)+1,1):
               yield (x,y0)
           elif x0 == x1: # vline
             for y in range(min(y0,y1),max(y0,y1)+1,1):
               yield (x0,y)
           else: # diagonal line
             _x0, _y0 = x0, y0
             _x1, _y1 = x1, y1
             steep = abs(_y1 - _y0) > abs(_x1 - _x0)
             if steep:
               _x0, _y0 = _y0, _x0
               _x1, _y1 = _y1, _x1
             if _x0 > _x1:
               _x0, _x1 = _x1, _x0
               _y0, _y1 = _y1, _y0
             dx = _x1 - _x0
             dy = abs(_y1 - _y0)
             err = dx // 2
             ystep = 0
             if _y0 < _y1:
               ystep = 1
             else:
               ystep = -1
             while _x0 <= _x1:
               if steep:
                 yield (_y0, _x0)
               else:
                 yield (_x0, _y0)
               err -= dy
               if err < 0:
                  _y0 += ystep
                  err += dx
               _x0 += 1
         else: # i is 0
           x1,y1=next(genxy)
     else:
       yield (x,y)
  
def xyrotate (x,y,deg,midx,midy): # rotate x,y degrees and round to int 
  return (xyroundint(*rotatexy(x,y,deg,midx,midy))) # conter clock

def xyadd (x,y,addx,addy): # add x,y,addx,addy
  return (x+addx,y+addy) # landa function to add values on x,y

def xydo (genxy,f,fp): # return generator data transformed with function f and parameters fp
  for x,y in genxy:
     if x is None: # no action if x is non 
       yield (x,y)  
     else:
       yield f(x,y,*fp)

def xy(x,y): 
  yield (x,y)
  
def vline(x,y,l): 
  yield (None,2)
  yield (x,y)
  yield (x,y+l-1)
  
def hline(x,y,l): 
  yield (None,2)
  yield (x,y)
  yield (x+l-1,y)  

def line(xy0,xy1): 
  yield (None,2)
  yield xy0
  yield xy1    

def rect(x,y,lx,ly):
  lx-=1
  ly-=1
  yield (None,5)
  yield (x,y)
  yield (x+lx,y)
  yield (x+lx,y+ly)
  yield (x,y+ly)
  yield (x,y) 
    
def fillrect(x,y,lx,ly): 
  lx-=1
  yield (None,ly*2)
  for iy in range (ly):
    yield (x,y+iy)
    yield (x+lx,y+iy) 
    
def roundrect(x,y,l,h=0,r=0,pix=1): 
     if h is 0: h=l
     yield from fillrect (x+r,y,l-(2*r),pix)
     yield from fillrect (x+r,y+h-pix,l-(2*r),pix)
     yield from fillrect (x,y+r,pix,h-(2*r))
     yield from fillrect (x+l-pix,y+r,pix,h-(2*r))
     for i in range(pix):
       yield from arc(x+r,y+r,r-i,4)
       yield from arc(x+l-r,y+r,r-i,1)
       yield from arc(x+r,y+h-r,r-i,3)
       yield from arc(x+l-r,y+h-r,r-i,2)    
    
def lines(xys): # generate yield xy(s) from tuple example ((,),(,),...)
    yield (None,len(xys))
    for xy in xys:
      yield xy   
         
def triangle(xy0,xy1,xy2): 
  yield (None,4)
  yield xy0
  yield xy1
  yield xy2
  yield xy0

def circle(x,y,r): 
  if r > 0:
    r=r-1
    px=x
    py=y
    x=x
    y=0
    rsq=r*r
    while x>y:
      x=round(sqrt(rsq-y*y))
      yield (px+x,py+y)
      yield (px+x,py-y)
      yield (px-x,py+y)
      yield (px-x,py-y)
      yield (px+y,py+x)
      yield (px+y,py-x)
      yield (px-y,py+x)
      yield (px-y,py-x)
      y+=1

def fillcircle(x0,y0,r): 
  r-=1
  yield from vline(x0,y0-r,2*r+1)
  f = 1 - r
  ddF_x = 1
  ddF_y = -2 * r
  x = 0
  y = r
  while x < y:
    if f >= 0:
      y -= 1
      ddF_y += 2
      f += ddF_y
    x += 1
    ddF_x += 2
    f += ddF_x
    yield from vline(x0+x,y0-y,2*y+1)
    yield from vline(x0+y,y0-x,2*x+1)
    yield from vline(x0-x,y0-y,2*y+1)
    yield from vline(x0-y,y0-x,2*x+1)
    
def arc(x,y,r,nr=0): # yield xy(s)
  if r > 0:
    r=r-1
    px=x
    py=y
    x=x
    y=0
    rsq=r*r
    while x>y:
      x=round(sqrt(rsq-y*y))
      if nr is 1: #1 
        yield (px+y,py-x)
        yield (px+x,py-y)
      elif nr is 2: #2 
        yield (px+y,py+x)
        yield (px+x,py+y)
      elif nr is 3: #3 
        yield (px-x,py+y)        
        yield (px-y,py+x)
      elif nr is 4: #4 
        yield (px-y,py-x)
        yield (px-x,py-y)
        
      y+=1    

def polygon(x,y,sides,r,rotatedegrees=0,coord=True): # generate xy(s) or corne xy(s)
  # x and y = coordinate center polygon 
  # size polygon = x,y +-r  
  #  PI (3.14..) radians are equal to 180 degrees  
  if r > 0:
    r=r-1  
    xy=[]
    rad=radians(rotatedegrees) # covert to radians   
    for s in range(sides):
      t=2*pi*s/sides+rad  
      if t == pi:
        xy.append(((x-r),y))
      else:
        #xy.append((int(x+r*cos(t)),int(y+r*sin(t))))
        xy.append((roundint(x+r*cos(t)),roundint(y+r*sin(t))))
    if coord:
      x1,y1=xy[0]
      x2,y2=xy[-1]
      yield from lines(xy)
      yield from line((x1,y1),(x2,y2))
    else:
      for corne in xy:  
        yield corne

def _char(ch,x0,y0,glyph,char_height,char_width):
  import framebuf  
  buf = bytearray(glyph)  
  fb = framebuf.FrameBuffer(buf, char_width, char_height,framebuf.MONO_HLSB)
  for y in range(char_height):
    for x in range(char_width):
      if fb.pixel(x,y):
          yield (x0+x,y0+y)
          
def text(x0,y0,s,font=None):
  if font:     
    for c in s:
      glyph, char_height, char_width = font.get_ch(c)   
      yield from _char(c,x0,y0,glyph,char_height,char_width)
      x0+=char_width
  else: # from micropython internal character font
    yield from zoomtext(x0,y0,s,zx=1,zy=1)  
    
def zoomchar(tox,toy,och,zx=3,zy=3):
  pix=och.pixel # b.pixel() have no problem with out of range
  # put pixel index in dic

  for y in range(8):
    lup=0
    bup=0
    ldown=0
    bdown=0
    for x in range(8): # horizontal lines
      p=pix(x,y) 
      if p and not pix(x,y-1): # pixel exist no up pixel exist
        if lup is 0:
          bup=x  
        lup+=zx
      elif lup > 0 :
        yield from hline(tox+(bup*zx),toy+(y*zy),lup)
        lup = 0        
      if p and not pix(x,y+1): # pixel exist no down pixel exist
        if ldown is 0:
          bdown=x  
        ldown+=zx  
      elif ldown > 0 :
        yield from hline(tox+(bdown*zx),toy+((y+1)*zy)-1,ldown)
        ldown = 0  
    if lup > 0:
      yield from hline(tox+(bup*zx),toy+(y*zy),lup)
    if ldown > 0:
      yield from hline(tox+(bdown*zx),toy+((y+1)*zy)-1,ldown)
      
  for x in range(8):
    lleft=0
    bleft=0
    lright=0
    bright=0
    for y in range(8): # vertical lines
      p=pix(x,y)
      if p and not pix(x-1,y): # pixel exist and no left pixel exist
        if lleft is 0:
          bleft=y  
        lleft+=zy
      elif lleft > 0 :
        yield from vline(tox+(x*zx),toy+(bleft*zy),lleft)
        lleft = 0          
      if p and not pix(x+1,y): # pixel exist and no right pixel exist
        if lright is 0:
          bright=y  
        lright+=zy  
      elif lright > 0 :
        yield from vline(tox+((x+1)*zx)-1,toy+(bright*zy),lright)
        lright = 0  
    if lleft > 0:
      yield from vline(tox+(x*zx),toy+(bleft*zy),lleft)
    if lright > 0:
      yield from vline(tox+((x+1)*zx)-1,toy+(bright*zy),lright)
      
def zoomtext(tox,toy,s,zx=3,zy=3,type=2):
  if type is 2:
    for parameters in _zoomtext(tox,toy,s,zx,zy):
      yield from fillrect(*parameters)
  elif type is 1:
    step=zx<<3 # step = zx * 8  
    for c in s:
      yield from zoomchar(tox,toy,ch(c),zx,zy)
      tox+=step      

