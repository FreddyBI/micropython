from math import cos,sin,pi

class Point3D:
    
    def __init__(self, x = 0, y = 0, z = 0):
        self.x, self.y, self.z = x, y, z
        
    def xyz(self):
        return self.x, self.y, self.z
        
    def __str__(self):
        return (f'Point3D({self.x},{self.y},{self.z})')
        
    __repr__ = __str__    
        
    def __add__ (self,P):
        R=Point3D(self.x,self.y,self.z)
        R.x=self.x+P.x
        R.y=self.y+P.y
        R.z=self.z+P.z        
        return R
        
    __radd__=__add__ 
    
    def __sub__(self, P):
        R = Point3D(self.x, self.y, self.z)
        R.x = self.x - P.x
        R.y = self.y - P.y
        R.z = self.z - P.z
        return R

    __rsub__ = __sub__

    def __mul__(self, num):
        R = Point3D(self.x, self.y, self.z)
        R.x = num * self.x
        R.y = num * self.y
        R.z = num * self.z
        return R

    __rmul__ = __mul__

    def __pow__(self, n):
        P = Point3D(self.x, self.y, self.z)
        P.x = self.x ** n
        P.y = self.y ** n
        P.z = self.z ** n
        return P

    def __neg__(self):
        O = Point3D(self.x, self.y, self.z)
        O.x = - self.x
        O.y = - self.y
        O.z = - self.z
        return O

    def rotateX(self, deg):
        """ Rotates this point around the X axis the given number of degrees. """
        rad = deg * pi / 180
        cosa = cos(rad)
        sina = sin(rad)
        y = self.y * cosa - self.z * sina
        z = self.y * sina + self.z * cosa
        return Point3D(self.x, y, z)

    def rotateY(self, deg):
        """ Rotates this point around the Y axis the given number of degrees. """
        rad = deg * pi / 180
        cosa = cos(rad)
        sina = sin(rad)
        z = self.z * cosa - self.x * sina
        x = self.z * sina + self.x * cosa
        return Point3D(x, self.y, z)

    def rotateZ(self, deg):
        """ Rotates this point around the Z axis the given number of degrees. """
        rad = deg * pi / 180
        cosa = cos(rad)
        sina = sin(rad)
        x = self.x * cosa - self.y * sina
        y = self.x * sina + self.y * cosa
        return Point3D(x, y, self.z)

    def project(self, win_width, win_height, fov, viewer_distance):
        """ Transforms this 3D point to 2D using a perspective projection. """
        factor = fov / (viewer_distance + self.z)
        x = self.x * factor + win_width / 2
        y = -self.y * factor + win_height / 2
        return Point3D(x, y, self.z)
 
