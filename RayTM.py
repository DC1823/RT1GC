import pygame
from pygame.locals import *
from figu import *
from luces import *
from RayTracer import RayTracer
from mats import *
import random

Width = 350
Height = 350
pygame.init()
pantalla = pygame.display.set_mode((Width, Height), pygame.DOUBLEBUF | pygame.HWACCEL | pygame.HWSURFACE)
pantalla.set_alpha(None)
rayTracer = RayTracer(pantalla)

rayTracer.escena.append(Sphere(pos=(0, -1, -4), radi=1, mat=snow()))
rayTracer.escena.append(Sphere(pos=(0, 0, -4), radi=0.8, mat=snow()))
rayTracer.escena.append(Sphere(pos=(0, 1, -4), radi=0.5, mat=snow()))
rayTracer.escena.append(Sphere(pos=(0, -0.3, -3.), radi=0.1, mat=dark()))
rayTracer.escena.append(Sphere(pos=(0, -1, -3), radi=0.15, mat=dark()))
rayTracer.escena.append(Sphere(pos=(0, 0.3, -3), radi=0.1, mat=dark()))
rayTracer.escena.append(Sphere(pos=(-0.1, 0.85, -3), radi=0.06, mat=dark()))
rayTracer.escena.append(Sphere(pos=(0.1, 0.85, -3), radi=0.06, mat=dark()))
rayTracer.escena.append(Sphere(pos=(0.065, 0.55, -3), radi=0.03, mat=dark()))
rayTracer.escena.append(Sphere(pos=(-0.065, 0.55, -3), radi=0.03, mat=dark()))
rayTracer.escena.append(Sphere(pos=(0.16, 0.6, -3), radi=0.03, mat=dark()))
rayTracer.escena.append(Sphere(pos=(-0.16, 0.6, -3), radi=0.03, mat=dark()))
rayTracer.escena.append(Sphere(pos=(0, 0.7, -3), radi=0.05, mat=zana()))
rayTracer.luces.append(AmbientLight(intens=1))
rayTracer.luces.append(DirectionalLight(dir=(0,0,1),intens=0.5,col=(1,1,1)))
rayTracer.luces.append(PointLight(puntop=(0,0,0),intens=0.5,col=(1,1,1)))
corriendo = True
rayTracer.rayclear()
rayTracer.raytRend()

while corriendo:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            corriendo = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                corriendo = False
    pygame.display.flip()
pan = pygame.Rect(0, 0, Width, Height)
sb = pantalla.subsurface(pan)
pygame.image.save(sb, "output.png")
pygame.quit()