from random import randint
from fbi import roundint,loopshuffle
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

class Demo: # Demo rotate 3d data and project as 2d on screen
      
    def __init__(self, width=128, height=64, fov=64, distance=4, rotateX=5, rotateY=5, rotateZ=5):
        
        # Data to draw
        self.points=[]
        self.edges=[]
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

    def poly2dxy(self,x=1,y=0,z=0,sides=1): # create 2d xy polygon data
        p=P(x,y,z)
        deg=360/sides
        degrees=0
        lenedges=len(self.edges)
        for _ in range(sides):
          self.points.append(p.rotateZ(degrees))
          degrees+=deg
        for i in range(sides-1):
          self.edges.append((lenedges+i,lenedges+i+1))
        self.edges.append((lenedges+i+1,lenedges))
        
    def addedgespolygons(self,sides): # add edges to all polygon points
        for step in range(0,len(self.points)-sides,sides):
          for i in range(sides):
            self.appendedges((i+step,i+step+sides))
        
    def poly2dxy2(self,x=1,y=0,z=0,sides=1): # create 2d xy polygon data
        step=x/4*2
        for i in range(1,4):
           x=i*step 
           self.poly2dxy(x,y,z,sides) 

    def poly3d(self,x=1,y=0,z=1,sides=1): # create 3d xyz polygon data
        for z in [z,-z]:
          self.poly2dxy(x,y,z,sides)
        self.addedgespolygons(sides)
        
    def cone3d(self,x=1,y=1,z=3,sides=1): # create 3d xyz cone data
        z=z/2
        self.poly2dxy(0,0,z,sides)
        self.poly2dxy(1,0,-z,sides)
        self.addedgespolygons(sides)
         
    def ball3d(self,x=1,y=1,sides=20,degreelist=[90]): # create 3d xyz ball data
        self.poly2dxy(x,y,0,sides)
        edgestep=sides
        for degrees in degreelist:
          for i in range(sides):
            self.points.append(self.points[i].rotateX(degrees)) 
            n0,n1=self.edges[i]
            self.edges.append((n0+edgestep,n1+edgestep))
          edgestep+=sides
        
    def draw4(self,x=1,y=2,z=0,degreestep=45): # create 3d xyz star data
        sides=3
        self.appendpoints(P(x,0,z),P(0,y,z),P(-x,0,z))
        self.appendedges((0,1),(1,2),(2,0))
        degrees=degreestep
        edgestep=sides
        while degrees <360.0001:
          for i in range(sides):
            self.points.append(self.points[i].rotateX(degrees)) 
            n0,n1=self.edges[i]
            self.edges.append((n0+edgestep,n1+edgestep))
          edgestep+=sides
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
    def lantern(self,size=1.5,sides=12): # create 3d xyz polygon data
        x=size/10
        for xz in [[x*4,size],[size,0],[x,0],[x,-size-x],[x*3,-size-x],[x*3,-size]]:
          x,z=xz  
          self.poly2dxy(x,0,z,sides)
        self.addedgespolygons(sides)
        
    def bol(self,size=3.5,sides=10):
        z=size/2
        p=P(1,0,z)
        stepdeg=180/(sides-1)
        deg=0
        while deg < 180.001:
          rad = deg * pi / 180
          z1 = cos(rad)*z
          x1 = sin(rad)*z
          self.poly2dxy(x1,0,z1,sides)
          deg+=stepdeg
        self.addedgespolygons(sides)
 
    def run(self):
        randsides=loopshuffle(5)
        typedraw=loopshuffle(8)
        while True:
          self.points.clear()
          self.edges.clear()
          sides=next(randsides)+3
          tdraw=next(typedraw)
          if tdraw is 0:
            self.poly2dxy2(sides=sides)
          elif tdraw is 1:
            self.poly3d(z=randint(1,4)*0.5,sides=sides)
          elif tdraw is 2:
            self.ball3d(sides=[4,20][randint(0,1)],degreelist=[[90],[45,90,135]][randint(0,1)])
          elif tdraw is 3:
            self.cone3d(sides=sides)
          elif tdraw is 4:
            self.draw4(degreestep=[120,90,45][randint(0,2)])
          elif tdraw is 5:
            self.aeroplane()
          elif tdraw is 6:
            self.lantern(sides=sides)             
          elif tdraw is 7:
            self.bol(size=3.5,sides=sides)
            
          line=o.line
          fill=o.fill
          show=o.show
          angleX, angleY, angleZ = 0, 0, 0
          t=[None]*len(self.points)
          
          for _ in range(180):
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
