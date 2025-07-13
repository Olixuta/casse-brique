import random # Pour les tirages aleatoires
import sys # Pour quitter proprement
import pygame # Le module Pygame
import pygame.freetype # Pour afficher du texte
import math
import csv

speudo=input('Veuillez choisir un speudonyme:')
def fusion(L1,L2):
    l=[]
    while L1!=[] or L2!=[]:
        if L1==[]:
            l+=L2
            L2=[]
        elif L2==[]:
            l+=L1
            L1=[]
        elif int(L1[0][1])>int(L2[0][1]):
            l.append(L1[0])
            L1=L1[1:]
        else:
            l.append(L2[0])
            L2=L2[1:]
    return l              

def tri_fusion(L):# un tri fusion pour le leaderboard
    longueur=len(L)
    if longueur==1:
        return L
    else:
        l=longueur//2
        l1=tri_fusion(L[longueur//2:])
        l2=tri_fusion(L[:longueur//2])
        return fusion(l1,l2)
pygame.init() # initialisation de Pygame

# Pour le texte.
pygame.freetype.init()
myfont=pygame.freetype.SysFont(None, 20) # texte de taille 20

# Taille de la fenetre
width, height = 900, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Ping")


# Pour limiter le nombre d'images par seconde
clock=pygame.time.Clock()

BLANC = (255, 255, 255)
NOIR = (0, 0, 0)

RAYON_BALLE = 10
XMIN, YMIN = 0, 0
XMAX, YMAX = width, height

#texte, rect = myfont.render("Mon message", (155, 155, 155), size=20)
#rect.midleft = (50,550)
#screen.blit(texte, rect)



class Raquette:
    def __init__(self):
        self.x = (XMIN+XMAX)/2
        self.y = YMAX - RAYON_BALLE
        self.longueur = 10*RAYON_BALLE
    def afficher(self):
        pygame.draw.rect(screen, BLANC,(int(self.x-self.longueur/2), int(self.y-RAYON_BALLE),self.longueur, 2*RAYON_BALLE), 0)
    def deplacer(self, x):
        if x - self.longueur/2 < XMIN:
            self.x = XMIN + self.longueur/2
        elif x + self.longueur/2 > XMAX:
            self.x = XMAX - self.longueur/2
        else:
            self.x = x
    def collision_balle(self, balle):
        vertical = abs(self.y - balle.y) < 2*RAYON_BALLE
        horizontal = abs(self.x - balle.x) < self.longueur/2 + RAYON_BALLE
        return vertical and horizontal

class Balle:
    def vitesse_par_angle(self, angle):
        self.vx = self.vitesse * math.cos(math.radians(angle))
        self.vy = -self.vitesse * math.sin(math.radians(angle))
    def __init__(self):
        self.x, self.y = (400, 400)
        self.vitesse = 8 # vitesse initiale
        self.vitesse_par_angle(60) # vecteur vitesse
        self.sur_raquette=True
        self.vie=5
    def afficher(self):
        pygame.draw.rect(screen, BLANC,(int(self.x-RAYON_BALLE), int(self.y-RAYON_BALLE),2*RAYON_BALLE, 2*RAYON_BALLE), 0)

    def rebond_raquette(self,raquette):
        diff=raquette.x - self.x
        longueur_totale=raquette.longueur/2 + RAYON_BALLE
        angle=90+80*diff/longueur_totale
        self.vitesse_par_angle(angle)

    def deplacer(self,raquette):
        if self.sur_raquette:
            self.y=raquette.y-2*RAYON_BALLE
            self.x=raquette.x
        else:
            self.x += self.vx
            self.y += self.vy
            if raquette.collision_balle(self) and self.vy > 0:
                self.rebond_raquette(raquette)
            if self.x + RAYON_BALLE > XMAX:
                self.vx = -self.vx
            if self.x - RAYON_BALLE < XMIN:
                self.vx = -self.vx
            if self.y + RAYON_BALLE > YMAX:
                self.sur_raquette=True
                self.vie = self.vie -1
                jeu.combo=0 # le combo se reset si on perd une vie 
                if self.vie ==0: # si on a perdu 
                    texte, rect = myfont.render("Game over", (220, 22, 22), size=100)# on affiche "Game over"
                    rect.midleft = (200,height//2)
                    screen.blit(texte, rect)
                    pygame.display.flip()
                    pygame.time.delay(1000)
                    jeu.run=False # et on arrete le jeu 
            if self.y - RAYON_BALLE < YMIN:
                self.vy = -self.vy

class Jeu:
    def __init__(self):
        self.balle = Balle()
        self.raquette=Raquette()
        self.brique2=[]# Pour stocker les briques
        self.score=0 # score
        self.combo=0# combo
        self.run=True# pour arreter le jeu si on a perdu 
    def gestion_evenements(self):
    # Gestion des evenements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit() # Pour quitter
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button==1:
                    if self.balle.sur_raquette:
                        self.balle.sur_raquette=False
                        self.balle.vitesse_par_angle(60)
    def mise_a_jour(self):
        x,y=pygame.mouse.get_pos()
        self.balle.deplacer(self.raquette)
        for b in self.brique2: # je parcours l'ensemble des briques
            if b.en_vie():
                if b.collision_balle(self.balle):
                    self.score=self.score+self.combo+1
                    self.combo=self.combo+1
        self.raquette.deplacer(x)
    def affichage(self):
        screen.fill(NOIR) # on efface l'écran
        self.balle.afficher()
        self.raquette.afficher()
        for b in self.brique2:# je parcours l'ensemble des briques
            if b.en_vie():
                b.afficher()
        texte, rect = myfont.render("Vie = "+str(self.balle.vie), (155, 155, 155), size=20)# Pour afficher le nombre de vie 
        rect.midleft = (50,130)
        screen.blit(texte, rect)
        texte, rect = myfont.render("Score = "+str(self.score), (155, 155, 155), size=20)# Pour afficher le score
        rect.midleft = (50,50)
        screen.blit(texte, rect)
        texte, rect = myfont.render("Combo = "+str(self.combo), (155, 155, 155), size=20)# Pour afficher le combo
        rect.midleft = (50,90)
        screen.blit(texte, rect)
        texte, rect = myfont.render("Leaderboard: ", (155, 155, 155), size=20)# Pour afficher le leaderboard
        rect.midleft = (700,50)
        screen.blit(texte, rect)
        for i in range(n):# on afficher les meilleurs scores
            texte, rect = myfont.render(str(i+1) + ". "+leaderboard[i][0]+': '+str(leaderboard[i][1]), (155, 155, 155), size=20)
            rect.midleft = (700,50+(i+1)*30)
            screen.blit(texte, rect)



class Brique:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vie = 1
        self.longueur = 5 * RAYON_BALLE
        self.largeur = 3 * RAYON_BALLE
    def en_vie(self):
        return self.vie > 0
    def afficher(self):
        pygame.draw.rect(screen, (100,149,237), (int(self.x-self.longueur/2),
        int(self.y-self.largeur/2),
        self.longueur, self.largeur), 0)
    def collision_balle(self, balle):
        # on suppose que largeur<longueur
        marge = self.largeur/2 + RAYON_BALLE
        dy = balle.y - self.y
        touche = False
        if balle.x >= self.x: # on regarde a droite
            dx = balle.x - (self.x + self.longueur/2 - self.largeur/2)
            if abs(dy) <= marge and dx <= marge: # on touche
                touche = True
                if dx <= abs(dy):
                    balle.vy = -balle.vy
                else: # a droite
                    balle.vx = -balle.vx
        else: # on regarde a gauche
            dx = balle.x - (self.x - self.longueur/2 + self.largeur/2)
            if abs(dy) <= marge and -dx <= marge: # on touche
                touche = True
                if -dx <= abs(dy):
                    balle.vy = -balle.vy
                else: # a gauche
                    balle.vx = -balle.vx
        if touche:
            self.vie -= 1
        return touche

leaderboard=[]
with open("leaderboard-PADOVAN-DORIAN.txt","r") as ldb:# on récupere les anciens score stocké dans un fihicer csv 
    info=ldb.readline()
    n=len(info)
    while info!='':
        i=0
        score=''
        nom=''
        while info[i]!=':':
            nom=nom+info[i]
            i=i+1
        i=i+1
        #print(info[i])
        while i!=n:
            score=score+info[i]
            i=i+1
        leaderboard.append((nom,int(score)))
        info=ldb.readline()
        n=len(info)


leaderboard=tri_fusion(leaderboard)# on tri le leaderboard par ordre décroissant 
n=len(leaderboard)
if n>10:
    n=10

jeu = Jeu()
bool=True
while bool:
    jeu.gestion_evenements()
    jeu.mise_a_jour()
    jeu.affichage()
    pygame.display.flip() # envoi de l'image à la carte graphique
    clock.tick(60) # on attend pour ne pas dépasser 60 images/seconde
    jeu.balle.vitesse=8+(0.25)*math.log(jeu.score+0.1) # on augmente la vitesse 
    if not jeu.run:# Pour arreter le jeu si on a perdu 
        bool=False
    for e in jeu.brique2:# Pour chaque brique 
        if e.y>height: # on vérifie si la brique a touché le sol 
            e.vie=0
            texte, rect = myfont.render("Game over", (220, 22, 22), size=100)
            rect.midleft = (200,height//2)
            screen.blit(texte, rect)
            pygame.display.flip()
            pygame.time.delay(1000)
            bool=False

        if  not e.en_vie(): # on supprime les briques pour éviter du lag si le jeu tourne depuis trop longtemps
            jeu.brique2.remove(e)
        e.y=e.y+0.15 # la brique descend 
    for i in range(1,18):# on rajoute alétoirement des briques sur le haut de l'écran 
        if random.randint(1,2000)==1:
            jeu.brique2.append(Brique(50*i,15))

with open('leaderboard-PADOVAN-DORIAN.txt','a') as ldb: # on stock le score avec le speudo dans le fichier texte 
    ldb.write("\n"+speudo+':'+str(jeu.score))

def clear_leaderboard():
    with open('leaderboard-PADOVAN-DORIAN.txt','w') as lbd:
        pass

#clear_leaderboard() #pour reset le leaderboard 