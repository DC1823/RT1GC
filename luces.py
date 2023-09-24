from libmat import *
from math import acos, asin

def reflectVector(norm, dir):
    reflex = 2 * prodpunto(norm, dir)
    reflex = escxv(reflex, norm)
    reflex = sv(reflex, dir)
    reflex = nrv(reflex)

    return reflex

class Light(object):
    def __init__(self, intens = 1, col = (1,1,1), tipo = "LIGHT"):
        self.intens = intens
        self.col = col
        self.tipo = tipo

    def gtlcol(self):
        return [self.col[0] * self.intens, self.col[1] * self.intens, self.col[2] * self.intens]
    
    def gtdcol(self, inter):
        return None
    
    def gtscol(self, inter, vpos):
        return None
    
class AmbientLight(Light):
    def __init__(self, intens = 1, col = (1,1,1)):
        super().__init__(intens, col, "AMBIENT")

def reflex(norm, dir):
    return nrv(sv(escxv(norm,2 * prodpunto(norm, dir)), dir))

def refra(norm,inci,n,n2):
    c = prodpunto(norm, inci)
    if c < 0:
        c = -c
    else:
        norm = negativev(norm)
        n, n2 = n2, n
    n = n / n2
    return nrv(sv(escxv(av(inci, escxv(norm, c)), n) , escxv(norm, (1 - n **2 * (1-c**2)) ** 0.5 )))

def fresnel(norm, inci,n, n2):
    c = prodpunto(norm, inci)
    if c < 0:
        c = -c
    else:
        n, n2 = n2, n
    s2 = (n * (1 - c ** 2) ** 0.5) / n2
    c2 = (1 - s2 ** 2) ** 0.5
    fc = ((n2 * c - n * c2) / (n2 * c + n * c2)) ** 2
    fc2 = ((n * c2 - n2 * c) / (n * c2 + n2 * c)) ** 2
    kr = (fc + fc2) / 2
    kt = 1 - kr
    return kr, kt

def totinterreflex(inci, norm , n, n2):
    c = prodpunto(norm, inci)
    if c < 0:
        c = -c
    else:
        norm = negativev(norm)
        n, n2 = n2, n 
    if n < n2:
        return False
    return acos(c) >= asin(n2/n)

class DirectionalLight(Light):
    def __init__(self, dir = (0,-1,0), intens = 1, col = (1,1,1)):
        self.dir = nrv(dir)
        super().__init__(intens, col, "DIRECTIONAL")
    
    def gtdcol(self, inter):
        dir = [i * -1 for i in self.dir]
        intens = max(0,min(1,prodpunto(inter.norm, dir) * self.intens))
        intens *= 1 - inter.obj.mat.ks
        return [i * intens for i in self.col] 
       
    def gtscol(self, inter, vpos):
        dir = [i * -1 for i in self.dir]
        refdir = reflex(inter.norm, dir)
        vdir = sv(vpos, inter.punto)
        vdir = nrv(vdir)
        intens = max(0, min(1, prodpunto(refdir, vdir))) ** inter.obj.mat.spec
        intens *= self.intens
        intens *= inter.obj.mat.ks
        return [i * intens for i in self.col]
    
class PointLight(Light):
    def __init__(self, puntop=(0,0,0), intens=1, col=(1,1,1)):
        self.puntop = puntop
        super().__init__(intens, col, "POINT")

    def gtdcol(self,inter):
        dir = sv(self.puntop, inter.punto)
        radi = magnv(dir)
        dir = escxv(dir, 1/radi)
        intens = prodpunto(inter.norm, dir) * self.intens
        intens *= 1 - inter.obj.mat.ks
        if radi is not 0:
            intens /= radi ** 2
        intens = max(0, min(1, intens))
        return [i * intens for i in self.col]
    
    def gtscol(self, inter, vpos):
        dir = sv(self.puntop, inter.punto)
        radi = magnv(dir)
        dir = escxv(dir, 1/radi)
        refdir = reflex(inter.norm, dir)
        vdir = sv(vpos, inter.punto)
        vdir = nrv(vdir)
        intens = max(0, min(1, prodpunto(refdir, vdir))) ** inter.obj.mat.spec
        intens *= self.intens
        intens *= inter.obj.mat.ks
        if radi is not 0:
            intens /= radi ** 2
        intens = max(0, min(1, intens))
        return [i * intens for i in self.col]