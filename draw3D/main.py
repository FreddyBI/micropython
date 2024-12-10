from random import randint
from util import roundint,loopshuffle
from point3D import Point3D as P
from math import cos,sin,pi
from machine import Pin,I2C,SoftI2C
from ssd1306 import SSD1306_I2C
  
i2c=SoftI2C(scl=Pin(22), sda=Pin(21))

# Screen constant
WIDTH = const(128)
HEIGHT = const(64)

# create the display
o=SSD1306_I2C(WIDTH,HEIGHT,i2c)

def to_int(*args):
    for v in args:
      yield roundint(v) 

class demo:
    def __init__(self, width=128, height=64, fov=64, distance=4, rotateX=5, rotateY=5, rotateZ=5):
        
        # Data to draw
        self.points=[]
        self.edges=[]
        self.sides=0
        # Dimensions
        self.projection = [width, height, fov, distance]
        # Rotational speeds
        self.rotateX = rotateX
        self.rotateY = rotateY
        self.rotateZ = rotateZ
        
    def appendpoints(self,*args): # append points to list self.points  
        for v in args:
          self.points.append(v)
        
    def appendedges(self,*args): # append  edges to list self.edges  
        for v in args:
          self.edges.append(v)
        
    def appendpointandedge(self,p): # append  point and edge to list self.points and self.edges
        ip=len(self.points)
        self.points.append(p)
        ifrom=ip-1
        ito=ip
        if ip%self.sides is 0:
          ifrom+=self.sides
        self.edges.append((ifrom,ito))
        
    def poly2dxy(self,p): # create 2d xy polygon data
        deg=360/self.sides
        degrees=0
        for _ in range(self.sides):
          self.appendpointandedge(p.rotateZ(degrees))
          degrees+=deg
        
    def shape2dxy(self,*args): # create 2d shape data
        for v in args:
          self.appendpointandedge(v)
        
    def rect2dxy(self,x=1,y=1,z=0): # create 2d xy rectan data
        x2=x/2
        y2=y/2
        self.shape2dxy(P(-x2,y2,z),P(x2,y2,z),P(x2,-y2,z),P(-x2,-y2,z))
      
    def addedgespolygons(self): # add edges to all polygon points
        for step in range(0,len(self.points)-self.sides,self.sides):
          for i in range(self.sides):
            self.appendedges((i+step,i+step+self.sides))
  
    def poly2dxy2(self,x=1,y=0,z=0): # create 2d xy polygon data
        step=x/4*2
        for i in range(1,4):
           x=i*step 
           self.poly2dxy(P(x,y,z)) 

    def poly3d(self,x=1,y=0,z=1): # create 3d xyz polygon data
        for z in [z,-z]:
          self.poly2dxy(P(x,y,z))
        self.addedgespolygons()
        
    def cone3d(self,x=1,y=1,z=3): # create 3d xyz cone data
        z=z/2
        self.poly2dxy(P(0,0,z))
        self.poly2dxy(P(1,0,-z))
        self.addedgespolygons()
         
    def ball3d(self,x=1,y=1,degreelist=[90]): # create 3d xyz ball data
        self.sides=[4,20][randint(0,1)]
        self.poly2dxy(P(x,y,0))
        for degrees in degreelist:
          for i in range(self.sides):
            self.appendpointandedge(self.points[i].rotateX(degrees)) 
        
    def draw4(self,x=1,y=2,z=0,degreestep=45): # create 3d xyz star data
        self.sides=3
        for p in (P(x,0,z),P(0,y,z),P(-x,0,z)):
           self.appendpointandedge(p)
        degrees=degreestep
        while degrees <360.0001:
          for i in range(self.sides):
            self.appendpointandedge(self.points[i].rotateX(degrees)) 
          degrees+=degreestep
          
    def aeroplane(self):
        size=2
        l=size/3
        l2=size/6

        self.appendpoints(
            P( -size, 0, l2),
            P(-2*l, 0, l2),
            P(-2*l, 0, size-l2), 
            P(-l, 0, size-l2),
            P(-l, 0, l2), 
            P(2*l, 0, l2), 
            P(2*l, 0, l+l2),
            P(size, 0, l+l2), 
            P(size, 0, -l+-l2),
            P(2*l, 0, -l+-l2), 
            P(2*l, 0, -l2), 
            P(-l, 0, -l2), 
            P(-l, 0, -size-l2+l2), 
            P(-2*l, 0, -size+l2), 
            P(-2*l, 0, -l2), 
            P(-size, 0, -l2), 
            P(size, l, 0), 
            P(2*l, l, 0), 
            P(size, 0, 0), 
            P(2*l, 0, 0), 
            P(-size+-l, 0, 0)
        )
        self.appendedges(
            (0, 1), (1, 2), (2, 3), (3, 4),
            (4, 5), (5, 6), (6, 7), (7, 8),
            (8, 9), (9, 10), (10, 11), (11, 12),
            (12, 13), (13, 14), (14, 15), (0, 20), (15, 20),
            (19, 17), (17, 16), (16, 18), (18, 19)
        )
    def lantern(self,size=1.5): # create 3d xyz polygon data
        x=size/10
        for xz in [[x*4,size],[size,0],[x,0],[x,-size-x],[x*3,-size-x],[x*3,-size]]:
          x,z=xz  
          self.poly2dxy(P(x,0,z))
        self.addedgespolygons()
        
    def bol(self,size=3.5):
        z=size/2
        p=P(1,0,z)
        stepdeg=180/(self.sides-1)
        deg=0
        while deg < 180.001:
          rad = deg * pi / 180
          z1 = cos(rad)*z
          x1 = sin(rad)*z
          self.poly2dxy(P(x1,0,z1))
          deg+=stepdeg
        self.addedgespolygons()
        
        
    def tube(self,r=1,sides=10,l=10): # create 3d tube data
        self.sides=sides
        z=-r
        stepz=r/l*2
        for i in range(l):
          self.poly2dxy(P(r,0,z))
          z+=stepz
        stepdeg=180/l
        deg=0
        for i in range(len(self.points)):
          self.points[i]+=P(r,0,0)
          if i%self.sides is 0:
            deg+=stepdeg
          self.points[i]=self.points[i].rotateZ(deg)
        self.addedgespolygons()
        
    def rocket(self,x=1,y=1,z=3): # create 3d xyz cone data
        z=z/2
        for p in (P(0,0,2),P(0.5,0,1),P(0.5,0,-2)):
          self.poly2dxy(p)
        self.addedgespolygons()
        deg=0
        stepdeg=360/self.sides
        for s in range (self.sides):
          i=len(self.points)
          self.appendpoints(P(0.5,0,-1).rotateZ(deg),P(1,0,-1.5).rotateZ(deg),P(1,0,-2.5).rotateZ(deg),P(0.5,0,-2).rotateZ(deg))
          self.appendedges((i,i+1),(i+1,i+2),(i+2,i+3))
          deg+=stepdeg
          
    def sword(self): # create 3d xyz polygon data
        y1=0.3
        y2=y1/2
        x1=y1
        x2=y2
        self.rect2dxy(x1,y1,-2)
        self.rect2dxy(x1,y1,-1.8)
        
        self.rect2dxy(x2,y2,-1.6)
        self.rect2dxy(x2,y2,-1)
        
        self.rect2dxy(1.6,y1,-0.8)
        self.rect2dxy(1.6,y1,-0.6)
        
        self.shape2dxy(P(0,y2,-0.6),P(0.5,0,-0.6),P(0,-y2,-0.6),P(-0.5,0,-0.6))
        l=2
        self.shape2dxy(P(0,y2,-0.6+l),P(0.5,0,-0.6+l),P(0,-y2,-0.6+l),P(-0.5,0,-0.6+l))
        l+=2
        self.shape2dxy(P(0,0,-0.6+l),P(0,0,-0.6+l),P(0,0,-0.6+l),P(0,0,-0.6+l))
        
        self.addedgespolygons()
        
    def run(self):
        randsides=loopshuffle(5)
        typedraw=loopshuffle(11)
        while True:
          self.points.clear()
          self.edges.clear()
          self.sides=next(randsides)+3
          tdraw=next(typedraw)
          
          if tdraw is 0:
            self.poly2dxy2()
          elif tdraw is 1:
            self.poly3d(z=randint(1,4)*0.5)
          elif tdraw is 2:
            self.ball3d(degreelist=[[90],[45,90,135]][randint(0,1)])
          elif tdraw is 3:
            self.cone3d()
          elif tdraw is 4:
            self.draw4(degreestep=[120,90,45][randint(0,2)])
          elif tdraw is 5:
            self.aeroplane()
          elif tdraw is 6:
            self.lantern()             
          elif tdraw is 7:
            self.bol(size=3.5)
          elif tdraw is 8:
            self.tube()
          elif tdraw is 9:
            self.rocket()
          elif tdraw is 10:
            self.sides=4  
            self.sword()              
          line=o.line
          fill=o.fill
          show=o.show
          angleX, angleY, angleZ = 0, 0, 0
          t=[None]*len(self.points)
          
          for _ in range(360//self.rotateX):
            for i,v in enumerate(self.points):
                r = v.rotateX(angleX).rotateY(angleY).rotateZ(angleZ)
                p = r.project(*self.projection)
                t[i]=p
            fill(0)

            for e in self.edges:
              line(*to_int(t[e[0]].x, t[e[0]].y, t[e[1]].x, t[e[1]].y, 1))
            show()
 
            angleX += self.rotateX
            angleY += self.rotateY
            angleZ += self.rotateZ
            
          
s=Demo()
s.run()
