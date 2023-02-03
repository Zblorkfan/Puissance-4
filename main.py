"""
JEU DU PUISSANCE 4 !
Créé par Eloi LEGER et Thomas TORTI.                                                                            
L'IA utilise l'algorithme Minimax.                                                                      
"""
#Utiliser facilement les tableaux
import numpy as np 
#Affichage graphique
import pygame
#Police pour pygame
import sys
#Facilite les opérations
import math
#Coup aléatoire
import random 
#Couleurs utilisées par pygame
BLEU = (0,0,255)
NOIR = (0,0,0)
ROUGE = (255,0,0)
JAUNE = (255,255,0)
#Définitions des jetons des deux joueurs
j1=1
j2=2
PROFONDEUR=4#Profondeur de l'algorithme MiniMax,de facile à dur.
#A partir de 7, l'ordinateur peut ramer car il a beaucoup de calculs à effectuer.
PR = PROFONDEUR+1#Prodondeur + 1, utile pour le comptage des scores dans l'algorithme.
#Définition des joueurs
Joueur1 = 0
Joueur2 = 1

# Création d'une grille vide avec numpy
def grille0():
    g= np.zeros((6,7))
    return g
#Placer une pièce dans la grille
def jouer(g,ligne,colonne,j):
    g[ligne][colonne] = j
#Vérifier si une colonne n'est pas remplie    
def coup_possible(g,colonne):
    return g[6-1][colonne]==0
#Vérification de la prochaine ligne libre dans une colonne donnée
def prochaine_ligne_libre(g,colonne):
    for l in range(6):
        if g[l][colonne]==0:
            return l

# Retourne un booléen pour savoir si un joueur gagne 
def victoire(g,j):
    # Fonction HORIZ
    for c in range(7-3):
        for l in range(6):
            if g[l][c] == j and g[l][c+1]== j and g[l][c+2]==j and g[l][c+3]==j:
                return True
    # Fonction VERTIC
    for c in range(7):
        for l in range(6-3):
            if g[l][c] == j and g[l+1][c] == j and g[l+2][c]== j and g[l+3][c]==j:
                return True
    # Fonction Diag : Première diagonale
    for c in range(7-3):
        for l in range(6-3):
            if g[l][c] == j and g[l+1][c+1] == j and g[l+2][c+2]== j and g[l+3][c+3]==j:
                return True
    # 2eme fonction diag : deuxième diagonale
    for c in range(7-3):
        for l in range(3,6):
            if g[l][c] == j and g[l-1][c+1] == j and g[l-2][c+2]== j and g[l-3][c+3]==j:
                return True


        
    
# Booléen qui retourne s'il y a fin du jeu, si victoire ou match nul.
def fin_du_jeu(g):
    return victoire(g,j1) or victoire(g,j2) or len(liste_positions_valides(g))==0

def compte_score(case,j): #Cette fonction qui compte le score sera utile à calcul_score puis à l'algorithme minimax
    score=0
    adversaire_j= j1
    if j== j1:
        adversaire_j=j2
    #nombre de js
    if case.count(j)==4:
        score+=100
    elif case.count(j)==3 and case.count(0)==1:
        score+=5
    elif case.count(j)==2 and case.count(0)==2:
        score+=2
    
    if case.count(adversaire_j)==3 and case.count(0)==1:
        score-=4
    if case.count(adversaire_j)==2 and case.count(0)==2:
        score-=1.5
    return score
    
def calcul_score(g,j):#Calcule le score à partir de compte_score() pour permettre à minimax d'identifier la meilleure case ou jouer
    score=0
    
    #Score colonne centrale
    tableau_centre=[int(i) for i in list(g[:,7//2])]
    nombre_centre= tableau_centre.count(j) 
    score+=nombre_centre*3
    
    
    #Score horizontal
    
    for l in range(6):
        tableau_ligne=[int(i) for i in list(g[l,:])]

        for c in range(7-PR):
            case= tableau_ligne[c:c+PROFONDEUR]
            score+=compte_score(case,j)
    #Score vertical
    for c in range(7):
        tableau_colonne=[int(i)for i in list(g[:,c])]
        for l in range(6-PR):
            case=tableau_colonne[l:l+PROFONDEUR]
            score+=compte_score(case,j)
    #Score diagonale positive
    for l in range(6-3):
        for c in range(7-PR):
            case=[g[l+i][c+i] for i in range(PROFONDEUR)]
            score+=compte_score(case,j)
    #Score diagonale negative
    for l in range(6-3):
        for c in range(7-PR):
            case=[g[l+3-i][c+i]for i in range(PROFONDEUR)]
            score+=compte_score(case,j)
    return score
#Algorithme Minimax         
def minimax(g, profondeur,alpha,beta,maximizingPlayer):
    coup_possible=liste_positions_valides(g)    #liste des coups possibles
    findujeu=fin_du_jeu(g) #Booléen retournant si il y a fin du jeu
    if profondeur==0 or findujeu: #Si la profondeur est nulle ou si il y a fin du jeu.
        if findujeu: #S'il y a fin du jeu
            if victoire(g,j2): #Si l'IA a gagné
                return (None,1000000) #On retourne une valeur nulle car on ne joue pas et une très bonne valeur
            elif victoire(g,j1): #Si le joueur a gagné
                return (None,-1000000)#On retourne une valeur nulle car on ne joue pas et une très mauvaise valeur
            else: #Si personne n'a gagné, donc en cas de match nul
                return (None, 0)#On retourne une valeur nulle car on ne joue pas et une valeur neutre, 0
        else: #Si la profondeur vaut 0 
            return (None,calcul_score(g, j2))#On retourne une valeur nulle car on ne joue pas et une valeur neutre, 0
    if maximizingPlayer:
        value= -math.inf #moins l'infini
        colonne= random.choice(coup_possible)#colonne au hasard dans celles ou on peut jouer
        for c in coup_possible:
            ligne= prochaine_ligne_libre(g,c)#ligne dispo pour la colonne c, qui prend les valeurs des colonnes possibles.
            tempog= g.copy()#copie temporaire de la grille g
            jouer(tempog,ligne,c,j2) #simulation de jeu sur la grille tempog
            new_score=minimax(tempog,profondeur-1,alpha,beta,False)[1]#valeur obtenue par le jeu dans une colonne donnée c
            if new_score>value: #Si la valeur est supérieure (le coup est meilleur), la colonne à retourner change et value devient new score
                value=new_score
                colonne= c
            alpha=max(alpha,value)#alpha prend la valeur de value si value est supérieur
            if alpha>=beta: #si alpha > beta, c a d si alpha > infini, on arrete la boucle.
                break
        return colonne,value #on retourne la colonne pour jouer et la valeur donnée par minimax pour le jeu dans cette colonne.
               
    else: #minimizing player 
        value= math.inf#l'infini
        colonne= random.choice(coup_possible)#colonne au hasard dans celles ou c'est possible de jouer
        for c in coup_possible:
            ligne= prochaine_ligne_libre(g,c)
            tempog= g.copy()#création d'une copie de la grille, puis simulation de jeu dans la colonne choisie.
            jouer(tempog,ligne,c,j1)
            new_score=minimax(tempog,profondeur-1,alpha,beta,True)[1]
            if new_score<value:
                value=new_score
                colonne=c
            beta= min(beta,value)#beta prend la valeur de value si elle est inférieure.
            if alpha>=beta: #si alpha > beta, on brise la boucle et on renvoie la colonne pour jouer et le score de cette colonne(pour l'algorithme)
                    break
        return colonne,value
        
                   
#Retourne l'ensemble des positions colonnes dans lesquelles on peut jouer               
def liste_positions_valides(g):
    positions_valides=[]
    for c in range(7):
        if coup_possible(g,c):
            positions_valides.append(c)
    return positions_valides

    
    
#Modélisation de la grille avec pygame    
def gui_grille(g):
    for c in range(7):
        for l in range(6):
            pygame.draw.rect(screen,BLEU,(c*TAILLECERCLE,l*TAILLECERCLE + TAILLECERCLE,TAILLECERCLE,TAILLECERCLE ))
            pygame.draw.circle(screen,NOIR,(int(c*TAILLECERCLE + TAILLECERCLE/2),int(l*TAILLECERCLE + TAILLECERCLE+ TAILLECERCLE/2)),RAYON)
    for c in range(7):
        for l in range(6):
            if g[l][c]==j1:
                pygame.draw.circle(screen,JAUNE,(int(c*TAILLECERCLE + TAILLECERCLE/2),longueur-int(l*TAILLECERCLE + TAILLECERCLE/2)),RAYON)
            elif g[l][c]==j2:
                pygame.draw.circle(screen,ROUGE,(int(c*TAILLECERCLE + TAILLECERCLE/2),longueur-int(l*TAILLECERCLE+ TAILLECERCLE/2)),RAYON)
    pygame.display.update()           
g= grille0()
game_over= False


pygame.init()
infoObject = pygame.display.Info()
largeur= infoObject.current_w #largeur exacte de l'écran
longueur= infoObject.current_h#longueur exacte de l'écran

TAILLECERCLE= longueur/7 #pour caler la grille en bas.


RAYON = int(TAILLECERCLE/2 -5) #rayon du cercle
screen = pygame.display.set_caption("Jeu du Puissance4")#Définition de l'écran pygame
screen= pygame.display.set_mode((0, 0), pygame.FULLSCREEN)



pygame.display.update() #Update de l'écran pygame
myfont = pygame.font.SysFont("Comic sans ms", 75) #Utilisation de sys pour utiliser la police comic sans ms dans pygame
myfont2 = pygame.font.SysFont("Comic sans ms", 30) #Utilisation de sys pour utiliser la police comic sans ms dans pygame
text3 = myfont.render('Choisissez votre mode de jeu', True, (255,255,255))
screen.blit(text3, (200,200))
smallfont = pygame.font.SysFont('Comic sans ms',35)
text = smallfont.render('Jeu à deux joueurs' , True , (0,0,0))
pygame.draw.rect(screen,ROUGE,[longueur/2,largeur/2,350,40])
screen.blit(text , (longueur/2+25,largeur/2- 7.5))
text2 = smallfont.render('Jeu contre une IA' , True , (0,0,0))
pygame.draw.rect(screen,JAUNE,[longueur/2 + 450,largeur/2,350,40])
screen.blit(text2 , (longueur/2+475,largeur/2-7.5))
pygame.display.update()



while True : 
    mouse = pygame.mouse.get_pos()
    for event in pygame.event.get(): 

        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:      
            if longueur/2 <= mouse[0] <= longueur/2+350 and largeur/2 <= mouse[1] <= largeur/2+40:
                screen.fill(NOIR)
                tour= random.randint(Joueur1, Joueur2)#le 1er tour de jeu est attribué aléatoirement
                while not game_over: #Tant que personne n'a gagné et qu'il n'y a pas de match nul
                    gui_grille(g)#Appel de la fonction qui dessine la grille
                    for event in pygame.event.get(): #Si l'utilisateur quitte en faisant échap, on quitte le programme
                        if event.type == pygame.QUIT:
                            sys.exit()
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE:
                                pygame.quit()
                                sys.exit()
                        if event.type == pygame.MOUSEMOTION and event.pos[0] <= TAILLECERCLE*7 : #Si l'utilisateur bouge la souris, on fait suivre le cercle du jeton (si c'est son tour)
                            pygame.draw.rect(screen, NOIR,(0,0,largeur,TAILLECERCLE))
                            coordonneesx= event.pos[0]
                            if tour==Joueur1:
                                pygame.draw.circle(screen,JAUNE,(coordonneesx,int(TAILLECERCLE/2)),RAYON)
                            if tour == Joueur2:
                                pygame.draw.circle(screen,ROUGE,(coordonneesx,int(TAILLECERCLE/2)),RAYON)

                            
                        pygame.display.update()#Update de l'écran
                      
                        if event.type == pygame.MOUSEBUTTONDOWN and event.pos[0] <= TAILLECERCLE*7:
                             #Si l'utilisateur clique pour poser son jeton
                            pygame.draw.rect(screen, NOIR, (0,0, largeur, TAILLECERCLE))
                            
                            

                                                       # Si c'est son tour
                            if tour==Joueur1:
                                coordonnees_x= event.pos[0]
                                colonne= int(math.floor(coordonnees_x/TAILLECERCLE)) #on calcule la colonne a partir des coordonnées de la souris
                                
                                
                                if coup_possible(g,colonne): #Si on peut jouer
                                    ligne=prochaine_ligne_libre(g,colonne) #On détermine la ligne posible pour jouer
                                    jouer(g,ligne,colonne,j1)#On joue
                                    
                                    if victoire(g,j1):#Si victoire du joueur
                                        victoire= myfont.render("Le joueur jaune a gagné",1,JAUNE)#On écrit la victoire sur l'écran
                                        screen.blit(victoire, (0,0))#On l'affiche
                                        game_over= True#On passe game_over à true car il y a eu victoire

                                    tour+=1 #On passe le tour à l'ia

                                    gui_grille(g)#On dessine la grille
                            elif tour==Joueur2:
                                coordonnees_x= event.pos[0]
                                colonne= int(math.floor(coordonnees_x/TAILLECERCLE)) #on calcule la colonne a partir des coordonnées de la souris
                                
                                
                                if coup_possible(g,colonne): #Si on peut jouer
                                    ligne=prochaine_ligne_libre(g,colonne) #On détermine la ligne posible pour jouer
                                    jouer(g,ligne,colonne,j2)#On joue
                                    
                                    if victoire(g,j2):#Si victoire du joueur
                                        victoire= myfont.render("Le joueur rouge a gagné",1,ROUGE)#On écrit la victoire sur l'écran
                                        screen.blit(victoire, (0,0))#On l'affiche
                                        game_over= True#On passe game_over à true car il y a eu victoire

                                    tour-=1 #On passe le tour à l'ia

                                    gui_grille(g)#On dessine la grille
                                    

                    if game_over: #Si il y a fin du jeu, on attend que l'utilisateur quitte avec echap
                        while game_over : 
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    sys.exit()
                                if event.type == pygame.KEYDOWN: 
                                    if event.key == pygame.K_ESCAPE: 
                                        pygame.quit()
                                        sys.exit()                        

            if longueur/2 + 475 <= mouse[0] <= longueur/2+825 and largeur/2 <= mouse[1] <= largeur/2+ 40: 
                screen.fill(BLEU)
                text3 = myfont.render('Choisissez la difficulté de l\'IA', True, (255,255,255))
                screen.blit(text3, (200,200))
                pygame.draw.rect(screen,NOIR,[75,705,110,40])
                text = smallfont.render('Faible', True, (255,255,255))
                screen.blit(text, ( 75,700))
                pygame.draw.rect(screen,(255,255,255),[225,705,110,40])
                text2 = smallfont.render('Moyen', True, (0,0,255))
                screen.blit(text2, (225,700))

                pygame.draw.rect(screen,JAUNE,[375,705,80,40])
                text1 = smallfont.render('Fort', True, (255,0,0))
                screen.blit(text1, (375,700))

                pygame.draw.rect(screen,ROUGE,[495,705,150,40])
                text1 = smallfont.render('Extrème', True,JAUNE)
                screen.blit(text1, (495,700))
                pygame.display.update()
                test3 = True
                while test3: 
                    mouse = pygame.mouse.get_pos()
                    for event in pygame.event.get(): 
                        if event.type == pygame.QUIT:
                            sys.exit()
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE:
                                pygame.quit()
                                sys.exit()
                        if event.type == pygame.MOUSEBUTTONDOWN:      
                            if 75 <= mouse[0] <= 185 and 705 <= mouse[1] <= 745: 
                                PROFONDEUR = 1
                                test3 = False
                                break
                            elif 225 <= mouse[0] <= 335 and 705 <= mouse[1] <= 745:
                                PROFONDEUR = 2
                                test3 = False
                                break
                            elif 375 <= mouse[0] <= 455 and 705 <= mouse[1] <= 745:
                                PROFONDEUR =3
                                test3 = False
                                break
                            elif 495 <= mouse[0] <= 645 and 705 <= mouse[1] <= 745:
                                PROFONDEUR = 4
                                test3 = False
                                break                            

                screen.fill(NOIR)
                tour= random.randint(Joueur1, Joueur2)#le 1er tour de jeu est attribué aléatoirement
                while not game_over: #Tant que personne n'a gagné et qu'il n'y a pas de match nul
                    gui_grille(g)#Appel de la fonction qui dessine la grille
                    for event in pygame.event.get(): #Si l'utilisateur quitte en faisant échap, on quitte le programme
                        if event.type == pygame.QUIT:
                            sys.exit()
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE:
                                pygame.quit()
                                sys.exit()
                        if event.type == pygame.MOUSEMOTION and event.pos[0] <= TAILLECERCLE*7: #Si l'utilisateur bouge la souris, on fait suivre le cercle du jeton (si c'est son tour)
                            pygame.draw.rect(screen, NOIR,(0,0,largeur,TAILLECERCLE))
                            coordonneesx= event.pos[0]
                            if tour==Joueur1:
                                pygame.draw.circle(screen,JAUNE,(coordonneesx,int(TAILLECERCLE/2)),RAYON)
                            
                        pygame.display.update()#Update de l'écran
                        
                        if event.type == pygame.MOUSEBUTTONDOWN and event.pos[0] <= TAILLECERCLE*7: #Si l'utilisateur clique pour poser son jeton
                            pygame.draw.rect(screen, NOIR, (0,0, largeur, TAILLECERCLE))
                            
                            
                           
                            # Si c'est son tour
                            if tour==Joueur1:
                                coordonnees_x= event.pos[0]
                                colonne= int(math.floor(coordonnees_x/TAILLECERCLE)) #on calcule la colonne a partir des coordonnées de la souris
                                
                                
                                if coup_possible(g,colonne): #Si on peut jouer
                                    ligne=prochaine_ligne_libre(g,colonne) #On détermine la ligne posible pour jouer
                                    jouer(g,ligne,colonne,j1)#On joue
                                    
                                    if victoire(g,j1):#Si victoire du joueur
                                        victoire= myfont.render("Vous avez gagné !",1,JAUNE)#On écrit la victoire sur l'écran
                                        screen.blit(victoire, (0,0))#On l'affiche
                                        game_over= True#On passe game_over à true car il y a eu victoire

                                    tour+=1 #On passe le tour à l'ia

                                    gui_grille(g)#On dessine la grille
                                    
                    # Tour de l'IA
                    if tour== Joueur2 and not game_over :#Si c'est son tour et que personne n'a gagné
                        colonne,minimax_score= minimax(g,PROFONDEUR,-math.inf,math.inf,True) #Détermination de la colonne avec minimax
                        position=(colonne)
                        
                        if coup_possible(g,colonne): #Si c'est possible
                            ligne=prochaine_ligne_libre(g,colonne)#La ligne est déterminée
                            jouer(g,ligne,colonne,j2)#On joue

                            
                            if victoire(g,j2): #Si victoire de l'IA
                                victoire= myfont.render("Victoire de l'IA",1,ROUGE)#Affichage du message de victoire
                                screen.blit(victoire, (0,0))

                                game_over=True #On met game_over à true
                        gui_grille(g)#On dessine la grille
                            
                        tour = tour -1 #On passe le tour au joueur
                    if game_over: #Si il y a fin du jeu, on attend que l'utilisateur quitte avec echap
                        while game_over : 
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    sys.exit()
                                if event.type == pygame.KEYDOWN: 
                                    if event.key == pygame.K_ESCAPE: 
                                        pygame.quit()
                                        sys.exit()                        