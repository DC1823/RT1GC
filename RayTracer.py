from math import pi, sin, cos, tan, radians, acos, atan2, asin
from libmat import *
from luces import *
from mats import *

MXRECU = 4

class RayTracer(object):
    def __init__(self, pantalla):
        self.pantalla = pantalla
        _,_, self.WI, self.He = pantalla.get_rect()
        self.escena = []
        self.luces = []
        self.cpos = [0,0,0]
        self.rayvp(0,0,self.WI, self.He)
        self.rayproy()
        self.rtColor = (1,1,1)
        self.rayccol(0,0,0)
        self.rayclear()
        self.emap = None

    def rayccol(self, r,g,b):
        self.ccol = (r,g,b)
        
    def rayclear(self):
        self.pantalla.fill((self.ccol[0] * 255,self.ccol[1] * 255,self.ccol[2] * 255))
    
    def rayvp(self, posX, posY, Width, Height):
        self.vpX = posX
        self.vpY = posY
        self.vpW = Width
        self.vpH = Height
        
    def rayproy(self, fov = 60, n = 0.1):
        self.nearPlane = n
        aradi = self.vpW / self.vpH
        self.topEdge = tan((fov * pi / 360)) * n
        self.derEdge = self.topEdge * aradi
        
    def raytpixel(self, x, y, color=None):
        y = self.He - y-1
        if (0 <= x < self.WI) and (0 <= y < self.He):
            color = self.ccol if color is None else (color[0] * 255, color[1] * 255, color[2] * 255)
            self.pantalla.set_at((x, y), color)

    def raytcast(self, ori, dir, escena=None, recur=0):
        if recur >= MXRECU:
            return None
        dp = float("inf")
        inter = None
        ht = None
        for obj in self.escena:
            if obj is not escena:
                inter = obj.rintrsct(ori, dir)
                if inter is not None:
                    if inter.dist < dp:
                        dp = inter.dist
                        ht = inter
        return ht

    
    def raytcast(self, ori, dir, escena=None, recur=0):
        if recur >= MXRECU:
            return None
        dp = float("inf")
        inter = None
        ht = None
        for obj in self.escena:
            if obj is not escena:
                inter = obj.rintrsct(ori, dir)
                if inter is not None:
                    if inter.dist < dp:
                        dp = inter.dist
                        ht = inter
        return ht

    def raytrcol(self, inter, raytdir, recur=0):
        if inter is None:
            if self.emap:
                x = (atan2(raytdir[2], raytdir[0]) / (2 * pi)+0.5)*self.emap.get_width()
                y = acos(raytdir[1]) / pi * self.emap.get_height()
                ecol = self.emap.get_at((int(x), int(y)))
                return [ecol[i]/255 for i in range(3)]          
            else:
                color = self.ccol
                return [i/255 for i in self.ccol]
        mat = inter.obj.mat
        sfcol = mat.diff
        if mat.txtu and inter.txtucrds:
            tx = int(inter.txtucrds[0] * mat.txtu.get_width()-1)
            ty = int(inter.txtucrds[1] * mat.txtu.get_height()-1)
            if tx >= mat.txtu.get_width() or ty >= mat.txtu.get_height() or tx < 0 or ty < 0:
                tcol = [0,0,0]
            else:
                try:
                    tcol = mat.txtu.get_at((tx, ty))
                except:
                    print(tx,ty)
            tcol = [i / 255 for i in tcol]
            sfcol = [sfcol[i] * tcol[i] for i in range(3)]
        refxcol = [0, 0, 0]
        refcol = [0, 0, 0]
        acol = [0, 0, 0]
        diffcol = [0, 0, 0]
        speccol = [0, 0, 0]
        fcol = [0, 0, 0]
        if mat.mattipo == OPAQUE:
            for luz in self.luces:
                if luz.tipo == "AMBIENT":
                    color = luz.gtlcol()
                    acol = [acol[i] + color[i] for i in range(3)]
                else:
                    somdir = None
                    if luz.tipo == "DIRECTIONAL":
                        somdir = [i * -1 for i in luz.dir]
                    if luz.tipo == "POINT":
                        luzdir = sv(luz.puntop, inter.punto)
                        somdir = nrv(luzdir)
                    sominters = self.raytcast(inter.punto, somdir, inter.obj)
                    if sominters is None:
                        diffColor = luz.gtdcol(inter)
                        diffcol = [diffcol[i] + diffColor[i] for i in range(3)]
                        specColor = luz.gtscol(inter, self.cpos)
                        speccol = [speccol[i] + specColor[i] for i in range(3)]
        elif mat.mattipo == REFLECTIVE:
            refx = reflex(inter.norm, negativev(raytdir))
            refin = self.raytcast(inter.punto, refx, inter.obj, recur + 1)
            refxcol = self.raytrcol(refin, refx, recur + 1)
            for luz in self.luces:
                if luz.tipo != "AMBIENT":
                    luzdir = None
                    if luz.tipo == "DIRECTIONAL":
                        luzdir = [i * -1 for i in luz.dir]
                    if luz.tipo == "POINT":
                        luzdir = nrv(sv(luz.puntop, inter.punto))
                    sominters = self.raytcast(inter.punto, luzdir, inter.obj)
                    if sominters is None:
                        specColor = luz.gtscol(inter, self.cpos)
                        speccol = [speccol[i] + specColor[i] for i in range(3)]
        elif mat.mattipo == TRANSPARENT:
            af = prodpunto(raytdir, inter.norm) < 0
            bs = escxv(inter.norm, 0.001)
            refx = reflex(inter.norm, negativev(raytdir))
            refori = av(inter.punto, bs) if af else sv(inter.punto, bs)
            refin = self.raytcast(refori, refx, None, recur + 1)
            refxcol = self.raytrcol(refin, refx, recur + 1)
            for luz in self.luces:
                if luz.tipo != "AMBIENT":
                    somdir = None
                    if luz.tipo == "DIRECTIONAL":
                        somdir = [i * -1 for i in luz.dir]
                    if luz.tipo == "POINT":
                        luzdir = sv(luz.puntop, inter.punto)
                        somdir = nrv(luzdir)
                    sominters = self.raytcast(inter.punto, somdir, inter.obj)
                    if sominters is None:
                        specColor = luz.gtscol(inter, self.cpos)
                        speccol = [speccol[i] + specColor[i] for i in range(3)]
            if not totinterreflex(inter.norm, raytdir, 1.0, mat.ior):
                refract = refra(inter.norm, raytdir, 1.0, mat.ior)
                refracori = sv(inter.punto, bs) if af else av(inter.punto, bs)
                refrainterc = self.raytcast(refracori, refract, None, recur + 1)
                refcol = self.raytrcol(refrainterc, refract, recur + 1)
                kr, kt = fresnel(inter.norm, raytdir, 1.0, inter.obj.mat.ior)
                refxcol = escxv(refxcol, kr)
                refcol = escxv(refcol,kr)
        luzcol = [acol[i] + diffcol[i] + speccol[i] + refxcol[i] + refcol[i] for i in range(3)]
        fcol = [sfcol[i] * luzcol[i] for i in range(3)]
        return [min(1, i) for i in fcol]
    
    def raytRend(self):
        for x in range(self.vpX, self.vpX + self.vpW + 1):
            for y in range(self.vpY, self.vpY + self.vpH + 1):
                if 0 < x < self.WI and 0 < y < self.He:
                    pX = 2 * ((x + 0.5 - self.vpX) / self.vpW) - 1
                    pY = 2 * ((y + 0.5 - self.vpY) / self.vpH) - 1
                    pX *= self.derEdge
                    pY *= self.topEdge
                    dir = (pX, pY, -self.nearPlane)
                    dir = nrv(dir)
                    inter = self.raytcast(self.cpos, dir)
                    rayColor = self.raytrcol(inter, dir)
                    self.raytpixel(x, y, rayColor)
                    pygame.display.flip()