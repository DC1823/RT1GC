from libmat import *
from math import tan, pi, atan2, acos, sqrt

class Shape(object):
    def __init__(self, pos, mat):
        self.pos = pos
        self.mat = mat
        
    def rintrsct(self, ori, dir):
        return None

class Intercept(object):
    def __init__(self, dist, punto, norm, obj, txtucrds):
        self.dist = dist
        self.punto = punto
        self.norm = norm
        self.obj = obj
        self.txtucrds = txtucrds

class Plane(Shape):
    def __init__(self, pos, norm, mat):
        self.norm = norm
        super().__init__(pos, mat)

    def rintrsct(self, ori, dir):
        deno = prodpunto(dir, self.norm)
        if abs(deno) <=0.0001:
            return None
        nm = prodpunto(sv(self.pos, ori), self.norm)
        t= nm / deno
        if t < 0 :
            return None
        P = av(ori, escxv(dir, t))
        return Intercept(dist=t,punto=P,norm=self.norm,txtucrds=None,obj=self)
    
class Disk(Plane):
    def __init__(self, pos, norm, mat, radi):
        self.radi = radi
        super().__init__(pos, norm, mat)

    def rintrsct(self, ori, dir):
        rintrsct = super().rintrsct(ori, dir)
        if rintrsct is None:
            return None
        dist = magnv(sv(rintrsct.punto, self.pos))
        return None if dist > self.radi else Intercept(dist=rintrsct.dist,punto=rintrsct.punto,norm=rintrsct.norm,txtucrds=None,obj=self)

class AABB(Shape):
    def __init__(self, pos, tama, mat):
        self.tama = tama
        super().__init__(pos, mat)
        self.planos = []
        self.tama = tama
        izqPlane = Plane(av(pos, (-tama[0] / 2, 0, 0)), (-1, 0, 0), mat)
        derPlane = Plane(av(pos, (tama[0] / 2, 0, 0)), (1, 0, 0), mat)
        topPlane = Plane(av(pos, (0, tama[1] / 2, 0)), (0, 1, 0), mat)
        botPlane = Plane(av(pos, (0, -tama[1] / 2, 0)), (0, -1, 0), mat)
        frontPlane = Plane(av(pos, (0, 0, tama[2]/ 2)), (0, 0, 1), mat)
        backPlane = Plane(av(pos, (0, 0, -tama[2]/ 2)), (0, 0, -1), mat)
        self.planos.append(izqPlane)
        self.planos.append(derPlane)
        self.planos.append(topPlane)
        self.planos.append(botPlane)
        self.planos.append(frontPlane)
        self.planos.append(backPlane)
        self.limiMin =[0,0,0]
        self.limiMax =[0,0,0]
        bs = 0.0001
        for i in range(3):
            self.limiMin[i] = self.pos[i] - (self.tama[i] / 2 + bs)
            self.limiMax[i] = self.pos[i] + self.tama[i] / 2 + bs

    def rintrsct(self, ori, dir):
        intersect = None
        t = float("inf")
        u=0
        v=0
        for plane in self.planos:
            planeIntersect = plane.rintrsct(ori, dir)
            if planeIntersect is not None:
                planePoint = planeIntersect.punto
                if self.limiMin[0] < planePoint[0] < self.limiMax[0]:
                    if self.limiMin[1] < planePoint[1] < self.limiMax[1]:
                        if self.limiMin[2] < planePoint[2] < self.limiMax[2]:
                            if planeIntersect.dist < t:
                                t = planeIntersect.dist
                                intersect = planeIntersect
                                if abs(plane.norm[0])>0:
                                    u= (planePoint[1]-self.limiMin[1]) / (self.tama[1] + 0.002)
                                    v= (planePoint[2]-self.limiMin[2]) / (self.tama[2] + 0.002)
                                elif abs(plane.norm[1])>0:
                                    u= (planePoint[0]-self.limiMin[0]) / (self.tama[0] + 0.002)
                                    v= (planePoint[2]-self.limiMin[2]) / (self.tama[2] + 0.002)
                                elif abs(plane.norm[2])>0:
                                    u= (planePoint[0]-self.limiMin[0]) / (self.tama[0] + 0.002)
                                    v= (planePoint[1]-self.limiMin[1]) / (self.tama[1] + 0.002)
        return None if intersect is None else Intercept(dist=t,punto=intersect.punto,norm=intersect.norm,txtucrds=(u,v),obj=self)

class Sphere(Shape):
    def __init__(self, pos, radi, mat):
        self.radi = radi
        super().__init__(pos,mat)

    def rintrsct(self, ori, dir):
        L = sv(self.pos, ori)
        lenL = magnv(L)
        ta = prodpunto(L, dir)
        d = (lenL ** 2 - ta ** 2) ** 0.5
        if 0>lenL ** 2 - ta ** 2 or d > self.radi:
            return None
        tc = (self.radi ** 2 - d ** 2) ** 0.5
        t = ta - tc
        t1 = ta + tc
        if t < 0:
            t = t1
        if t < 0:
            return None
        punto = av(ori, escxv(dir, t))
        norm = sv(punto, self.pos)
        norm = nrv(norm)
        u = (atan2(norm[2], norm[0]) / (2 * pi)) + 0.5
        v = acos(norm[1]) / pi
        return Intercept(dist=t, punto=punto, norm=norm, txtucrds=(u, v),obj=self)
