# -*- coding: utf-8 -*-
"""
Created on Sun Dec 29 10:12:54 2019
version : python 2.7

@author: Gauthier de Monteynard, Gabriel de Montcheuil -
Programme SpaceInvader qui permet de jouer au jeu spaceinvader, en respectant au mieux les consignes.
On doit donc detruire des vaisseaux ennemis sans se faire nous meme toucher.
Par souci d 'originalité , nous ne créns pas des blocs de vaisseaux mais plusieurs vaisseaux indépendants aux vitesses et autres caractéristiques variables pour chaque niveau.
Petit bémol : les vaisseaux peuvent venir à se chevaucher , ce qui n'est pas tres RP. De meme , nous avons décidé que les tirs enneis et alliés peuvent se chevaucher sans se détruire.
Nous nous sommes également écartés des consignes en faisant tirer les vaisseaux ennemis non pas à une vitesse égale à celle du vaisseau allié , mais chaque ennemi a sa propre vitesse de tir.
Suprise au niveau 7 !
"""# -*- coding: utf-8 -*-

from tkinter import *
from random import *
import copy
import time

def launch():#lance le programme complet
    class Commandes():#classe qui permet de choisir différentes options en début de partie
        def __init__(self, FenetreMenu):
            self.x='<Right>'
            
            self.y='<Left>'
            self.image=['fond_coeur.gif', 'fond_etoile.gif', 'fond_foudre.gif']
            self.fondecran='fond_etoile.gif'
        
        def Lettres(self):#fonction d'affichage qui permet à l'utilisateur d'entrer de nouvelles commandes.
            self.FenetreCommande=Tk()
            V=StringVar(self.FenetreCommande, value=self.x)
            W=StringVar(self.FenetreCommande, value=self.y)
            
            r = Entry(self.FenetreCommande, textvariable=V ) #champ de saisie pour la commande "droite"
            l = Entry(self.FenetreCommande, textvariable=W) #champ de saisie pour la commande "gauche"
            rr= Label(self.FenetreCommande, text="Commande Right")
            ll= Label(self.FenetreCommande, text="Commande Left")
            rr.pack()
            r.pack()
            ll.pack()
            l.pack()
            
            buttonValider = Button(self.FenetreCommande, text='valider', command= lambda : Truc.Valider(r,l))
            buttonValider.pack()
            self.FenetreCommande.mainloop()
        
        def Valider(self,r,l): #fonction qui valide les valeurs entrées pour modifier les commandes
            if r.get()!=l.get() and r.get()!='' and l.get()!='':
                self.x=r.get()
                self.y=l.get()
                self.FenetreCommande.destroy()
                    
                
                
        def FondEcran(self):#choisir son fond d'écran
            self.FenetreFond = Tk()
            buttonFondCoeur = Button(self.FenetreFond, text='Coeurs',width=8 , command= lambda :Truc.ValiderF(0))
            buttonFondTenebres = Button(self.FenetreFond, text='Ténèbres',width=8 , command= lambda : Truc.ValiderF(2))
            buttonFondEtoile = Button(self.FenetreFond, text='Etoile',width=8 , command= lambda :Truc.ValiderF(1))
            buttonFondCoeur.pack(padx=5, pady=5)
            buttonFondTenebres.pack(padx=5, pady=5)
            buttonFondEtoile.pack(padx=5, pady=5)
            self.FenetreFond.mainloop()
            
        def ValiderF(self,x):
            self.fondecran = self.image[x]
            print(self.fondecran)
            self.FenetreFond.destroy()
                
    
    
    class Jeu():#la classe qui gère le déplacement des différents vaisseaux
        def __init__(self, FenetrePrincipale):
            
            self.niveau =1
            self.Mechant1={'Vies' : 1, 'Vitesse':1, 'Points' : 10, 'Nom' : 'ennemi', 'CadenceTir' : 5000}#on crée ici les différents ennemis/bonus qu on pourra utiliser avec leurs caractéristiques
            self.Mechant2={'Vies' : 2, 'Vitesse':2, 'Points' : 20, 'Nom' : 'ennemi2', 'CadenceTir' : 4000}
            self.Mechant3={'Vies' : 2, 'Vitesse':3, 'Points' : 30, 'Nom' : 'ennemi3', 'CadenceTir' : 3000}
            self.EnnemiBonus={'Vies': 10, 'Vitesse': 5, 'Points' : 100, 'Nom': 'LM', 'CadenceTir' : 750}
            self.Bonus1={'Nom' : 'bonusheal', 'Vitesse': 30}
            self.score=0
            self.nbMissile=0 #compter le nombre de missiles permet de le réguler pour eviter le 'spam'
            self.Mechants=[]#tous les méchants créés atterissent dans cette liste
            self.Vies =3
            self.Tirs=[]#les tirs aterrisent dans cette liste
            self.FenetrePrincipale=FenetrePrincipale
        
        def univers (self):#on crée les éléments qui n apparaitront qu une fois comme les protections, on a aussi choisi de définir les scores ici, pour plus de lisibilité de __init__
             self.Paliers()#on appelle la fonction qui apelle un noveau niveau
             self.AffichScore = Label(FenetrePrincipale, text='Score:'+str(self.score))
             self.AffichScore.pack(padx=3,  pady= 3, anchor=E)
             self.AffichVies = Label(FenetrePrincipale, text='Vie(s):'+str(self.Vies))
             self.AffichVies.pack(padx=3,  pady= 3, anchor=W) 
             self.AffichNiveau = Label(FenetrePrincipale, text='Niveau '+str(self.niveau))
             self.AffichNiveau.pack(padx=3,  pady= 3, anchor=N)
             k=0
             self.Block=[]#création des protections, qu on a décidé de mettre en bas a gauche
             for j in [10,30,50]: 
                 for i in [10,30,50,70,90]:
                        self.Block.append(CanvasJeu.create_rectangle( i, 300+j,i+20, 320+j, fill= 'gray'))
                     
             
                 
             
             
             
        
        
        
        def Paliers(self): # lance les différents ennemis des qu'un nouveau niveau est atteind
            
            if self.niveau==1:#on appelle un par un les ennemis/bonus qui constitueront le niveau
                CanvasJeu.after(10,self.CreaMechant,CanvasJeu,self.Mechant1)
            elif self.niveau==2:#niveau 2
                    CanvasJeu.after(10,self.CreaMechant,CanvasJeu,self.Mechant1)
                    CanvasJeu.after(1200,self.CreaMechant,CanvasJeu,self.Mechant1)
                    
                    
            elif self.niveau==3:
                    CanvasJeu.after(10,self.CreaMechant,CanvasJeu,self.Mechant1)
                    CanvasJeu.after(10,self.CreaMechant,CanvasJeu,self.Mechant2)
                    CanvasJeu.after(1200,self.CreaMechant,CanvasJeu,self.Mechant2)
                    CanvasJeu.after(30,self.CreaBonus,CanvasJeu,self.Bonus1)
            elif self.niveau==4:
                    CanvasJeu.after(10,self.CreaMechant,CanvasJeu,self.Mechant1)
                    CanvasJeu.after(10,self.CreaMechant,CanvasJeu,self.Mechant2)
                    CanvasJeu.after(1200,self.CreaMechant,CanvasJeu,self.Mechant2)
                    CanvasJeu.after(70,self.CreaMechant,CanvasJeu,self.Mechant3)
                    
            elif self.niveau==5:   
                    CanvasJeu.after(10,self.CreaMechant,CanvasJeu,self.Mechant2)
                    CanvasJeu.after(1200,self.CreaMechant,CanvasJeu,self.Mechant2)
                    CanvasJeu.after(2200,self.CreaMechant,CanvasJeu,self.Mechant2)
                    CanvasJeu.after(40,self.CreaMechant,CanvasJeu,self.Mechant3)
                    CanvasJeu.after(1200,self.CreaMechant,CanvasJeu,self.Mechant3)
            elif self.niveau==6:    
                    CanvasJeu.after(10,self.CreaMechant,CanvasJeu,self.Mechant3)
                    CanvasJeu.after(1200,self.CreaMechant,CanvasJeu,self.Mechant3)
                    CanvasJeu.after(2200,self.CreaMechant,CanvasJeu,self.Mechant3)
                    CanvasJeu.after(3200,self.CreaMechant,CanvasJeu,self.Mechant3)                
                    CanvasJeu.after(4200,self.CreaMechant,CanvasJeu,self.Mechant3)
                    CanvasJeu.after(5200,self.CreaBonus,CanvasJeu,self.Bonus1)
            elif self.niveau==7:    
                    CanvasJeu.after(10,self.CreaMechant,CanvasJeu,self.EnnemiBonus)
    #========================================================================================================
        
            
        def CreaBonus(self, canvasJeu, CaractBonus):#on crée ici les bonus
            
            PhotoBonus1 =self.icone_bouton(CaractBonus['Nom'])
            Bonus1=CanvasJeu.create_image(250,40, anchor=CENTER ,image=PhotoBonus1) 
            
            CanvasJeu.after(1000,self.down,CanvasJeu,Bonus1, CaractBonus )#lance la descente progressive du bonus
            self.updateBonus(CanvasJeu,Bonus1, CaractBonus)
        
        def updateBonus (self, CanvasJeu, Bonus1 , CaractBonus):#on gere les déplacements et l effet du bonus si il a été activé (percuté)par le joueur
            try:
                touche=CanvasJeu.find_overlapping(CanvasJeu.coords(Bonus1)[0]-14,CanvasJeu.coords(Bonus1)[1]-12,CanvasJeu.coords(Bonus1)[0]+14,CanvasJeu.coords(Bonus1)[1]+12)
                for i in touche:
                    if i ==2:
                        if CaractBonus['Nom']=='bonusheal':
                            self.Vies+=1
                            self.AffichVies.config(text='Vie(s):'+str(self.Vies))
                            CanvasJeu.delete(Bonus1)
                CanvasJeu.after(5 , self.updateBonus, CanvasJeu, Bonus1, CaractBonus)
            except:
                Bonus1==None
                            
            
        def CreaMechant(self,CanvasJeu,Mechant): #création de l ennemi en fonction de ses caractéristiques
            
            PhotoMechant1 =self.icone_bouton(Mechant['Nom'])
            Mechant['largeur']=PhotoMechant1.width() #on récupere la hauteur/largeur de l image pour gérer la zone de contact (superposition avec un autre objet)
            Mechant['hauteur']=PhotoMechant1.height()
            Mechant1=CanvasJeu.create_image(250,40, anchor=CENTER ,image=PhotoMechant1) 
            self.Mechants.append(Mechant1)#on l ajoute a la liste des mechants
            CaractMechant=copy.deepcopy(Mechant)#on copie les caractéristiques pour ne modifier par la suite que celles de l ennemi en question et pas tous les ennemis du meme type
            CanvasJeu.after(1000,self.down,CanvasJeu, Mechant1,CaractMechant)#lance la descente progressive de l ennemi
            self.update(CanvasJeu,Mechant1,0,CaractMechant)#lance le déplacement horizontal de l'ennemi, ses interactions avec les autres objets
            CanvasJeu.after(100,self.CreaMissileEnnemi,CanvasJeu, Mechant1,CaractMechant)#lance les tirs de l ennemi
            
        def icone_bouton(self, pNom):#permet juste de garder une image avent que python la detruise, si il refresh avant que tkinter l ai sauvegardé (crédit : Virgile Craust)
            Photo=PhotoImage(file=pNom+".gif")
            label=Label(image=Photo)
            
            label.image=Photo
            return Photo
        
        
    
    
    #===============================================================================================    
        
        
        
        
        
        def down(self,CanvasJeu,Mechant,CaractMechant):#gere la descente des ennemis
           try:
               if CanvasJeu.coords(Mechant)[1]>500:
                   CanvasJeu.delete(Mechant)
                   
               CanvasJeu.move(Mechant,0,CaractMechant["Vitesse"])
               CanvasJeu.after(500,self.down,CanvasJeu, Mechant,CaractMechant )
           except:
                Mechant==None
            
        
        def CreaMissileEnnemi(self, CanvasJeu,Mechant,CaractMechant):#crée l objet missile ennemi
            try:
                CadenceAleatoire = randrange(CaractMechant['CadenceTir']-300, CaractMechant['CadenceTir']+300)
                MissileEnnemi =CanvasJeu.create_rectangle(CanvasJeu.coords(Mechant)[0]+2,CanvasJeu.coords(Mechant)[1],CanvasJeu.coords(Mechant)[0]-2,CanvasJeu.coords(Mechant)[1]+15, fill= 'blue')            
                self.updateMissileEnnemi(CanvasJeu,MissileEnnemi,CaractMechant)
                CanvasJeu.after(CadenceAleatoire,self.CreaMissileEnnemi,CanvasJeu, Mechant,CaractMechant)#fréquence de tir
            except:
                Mechant==None
            
        def updateMissileEnnemi(self, CanvasJeu,MissileEnnemi,CaractMechant) :#déplacement du tir ennemi et interactions avec les autres objets
                CanvasJeu.move(MissileEnnemi,0,CaractMechant["Vitesse"])
                    
                try:        
                    touche=CanvasJeu.find_overlapping(CanvasJeu.coords(MissileEnnemi)[0],CanvasJeu.coords(MissileEnnemi)[1],CanvasJeu.coords(MissileEnnemi)[2],CanvasJeu.coords(MissileEnnemi)[3])#test les chevauchements avec d autres objets 
                    for i in touche:
                        if i in self.Block :
                            CanvasJeu.delete(i)
                            CanvasJeu.delete(MissileEnnemi)
                        if i == 2 : #l élément 2 sera toujours le vaisseau, code moyenneemt propre mais pratique , meme si nous en convenons , mettre le vaisseau dans une liste comme pourles autres objets serait plus propre
                            self.Vies -= 1
                            self.AffichVies.config(text='Vie(s):'+str(self.Vies))
                            if self.Vies==0 :
                                FenetrePrincipale.destroy()#plus de vie : game over
                            Touchee = self.icone_bouton('touché')
                            self.ImgTouchee=CanvasJeu.create_image(CanvasJeu.coords(Vaisseau)[0],CanvasJeu.coords(Vaisseau)[1], anchor=CENTER ,image=Touchee)        
                            CanvasJeu.delete(MissileEnnemi)
                            CanvasJeu.after(500, self.deleteTouche, CanvasJeu)
                            
                             
                            
                    
                    
                except:
                    MissileEnnemi==None
                     
                try:   
                    if CanvasJeu.coords(MissileEnnemi)[1]>510:#destruction si sortie de l'écran
                         CanvasJeu.delete(MissileEnnemi)
                    
                    
                    else:
                         CanvasJeu.after(5, self.updateMissileEnnemi, CanvasJeu , MissileEnnemi,CaractMechant) 
                            
                except:
                        MissileEnnemi==None
            
        def deleteTouche(self,CanvasJeu):#gestion de l image indiquant qu on a été percuté par un missile ennemi
            CanvasJeu.delete(self.ImgTouchee)
    
        def update(self, CanvasJeu,Mechant,n,CaractMechant): #gere les déplacement verticaux et les test de collision des ennemis, l update des scores ...
                
                CanvasJeu.bind_all('<f>',lambda event : self.cheatcode())#cheatcode1 : gagner de la vie
                
                CanvasJeu.bind_all('<space>',lambda event : self.Tir(CanvasJeu,Mechant))   #test si l utilisateur lance un tir
                
                try :
                    
                    touche=CanvasJeu.find_overlapping(CanvasJeu.coords(Mechant)[0]-CaractMechant['largeur']/2,CanvasJeu.coords(Mechant)[1]-CaractMechant['hauteur']/2,CanvasJeu.coords(Mechant)[0]+CaractMechant['largeur']/2,CanvasJeu.coords(Mechant)[1]+CaractMechant['hauteur']/2)#test le chevauchement avec un autre objet
                    for i in touche:
                        if i in self.Block :
                            CanvasJeu.delete(i)
                        if i in self.Tirs: #si collision avec un tir du vaisseau
                            CanvasJeu.delete(i)
                            self.Tirs.remove(i)
                            
                            CaractMechant['Vies']=CaractMechant['Vies']-1
                            if CaractMechant['Vies']==0:
                                CanvasJeu.delete(Mechant)
                                self.Mechants.remove(Mechant)
                                self.score+=CaractMechant["Points"]
                                self.AffichScore.config(text='Score:'+str(self.score))
                        if i==2: #l élément 2 sera toujours le vaisseau, code moyenneemt propre mais pratique , meme si nous en convenons , mettre le vaisseau dans une liste comme pourles autres objets serait plus propre
                            self.Vies -= 1
                            self.AffichVies.config(text='Vie(s):'+str(self.Vies))
                            if self.Vies==0 :
                                CanvasJeu.delete(Vaisseau)
                            
                            
                            Touchee = self.icone_bouton('touché')
                            self.ImgTouchee=CanvasJeu.create_image(CanvasJeu.coords(Vaisseau)[0],CanvasJeu.coords(Vaisseau)[1], anchor=CENTER ,image=Touchee)                       
                            CanvasJeu.delete(Mechant)
                            self.Mechants.remove(Mechant)
                            self.score+=CaractMechant["Points"]
                            self.AffichScore.config(text='Score:'+str(self.score))
                            CanvasJeu.after(500, self.deleteTouche, CanvasJeu)
                                                            
                except :
                                Mechant = None
                                
                try :
                    
                    if (CanvasJeu.coords(Mechant)[1]) >=510:
                        CanvasJeu.delete(Mechant)
                        self.Mechants.remove(Mechant)
                    
                    if (CanvasJeu.coords(Mechant)[0] <=14) or (CanvasJeu.coords(Mechant)[0] >=486)  : #si aucune collision, déplacement du vaisseau
                        n+=1
                    
                    CanvasJeu.move(Mechant,CaractMechant["Vitesse"]*(-1)**n,0)
                    CanvasJeu.after(18, self.update, CanvasJeu,Mechant,n,CaractMechant)
                    
                except :
                    Mechant= None
                if self.Mechants==[]:#on passe au niveau suivant lorsqu il n y a plus d ennemis 
                    self.niveau+=1
                    self.AffichNiveau.config(text='Niveau '+str(self.niveau))
                    self.Paliers()
                    
                
        def cheatcode(self):#RAJOUTE UNE VIE quand on active le cheatcode
            self.Vies+=1
            self.AffichVies.config(text='Vie(s):'+str(self.Vies))
                
            
            
            #les déplacemnts du vaisseau
        def Droite(self, event):
            try:
                if CanvasJeu.coords(Vaisseau)[0] < 500 :
                    CanvasJeu.move(Vaisseau, 7,0)
            except:
                CanvasJeu.Vaisseau=None
            
        def Gauche(self, event):
           
            try:
                if CanvasJeu.coords(Vaisseau)[0] > 15:
                    CanvasJeu.move(Vaisseau,-7,0)
            except:
                CanvasJeu.Vaisseau=None
            
                    
    
    
    #========================================================================================            
                
        def Tir(self,CanvasJeu,Mechant):#création du missile allié
              if self.nbMissile ==0  :        
                Missile = CanvasJeu.create_rectangle(CanvasJeu.coords(Vaisseau)[0]-2,CanvasJeu.coords(Vaisseau)[1]-40,CanvasJeu.coords(Vaisseau)[0]+2,CanvasJeu.coords(Vaisseau)[1]- 20, fill= 'red')  
                self.nbMissile=1 #on ne tire qu'un missile a la fois, avec une latence 
                self.Tirs.append(Missile)
                self.updateMissile(CanvasJeu,Mechant,Missile)
                CanvasJeu.after(600, self.Latence)
        def Latence(self):
            self.nbMissile=0
                
            
            
        def updateMissile (self, CanvasJeu,Mechant,Missile):#déplacemnt du missile allié
            
        
                    
                    
            try:        
                touche=CanvasJeu.find_overlapping(CanvasJeu.coords(Missile)[0],CanvasJeu.coords(Missile)[1],CanvasJeu.coords(Missile)[2],CanvasJeu.coords(Missile)[3])#on test la collision avec les blocs de protection , car les autres collisions sont deja gérées par les autres objets
                for i in touche:
                    if i in self.Block:
                        CanvasJeu.delete(i)
                        CanvasJeu.delete(Missile)
                        
                   
                        
                    
            except:
                Missile==None        
     
            try:   
                CanvasJeu.move(Missile,0,-5)
                if CanvasJeu.coords(Missile)[1]<0:       
                    CanvasJeu.delete(Missile)
                else:
                    CanvasJeu.after(5, self.updateMissile, CanvasJeu,Mechant,Missile) 
    
            except:
                 Missile=None
                 
            
    
    
    class Classement():#classe qui gere la fin de partie
        
        def __init__(self):
            self.score=Jeu1.score #récupère le score final
            self.classement=[]
                
        def Rejouer(self):
            fenetreClassement.destroy()
            launch()
        
        def ScorePerso(self): #Permet d'ajouter un score et le pseudo à la base de données
            x=self.pseudo+';'+str(self.score)+'\n'
            fichierClassement.write(x)
            fichierClassement.close()
            self.TriFichier()
            
        def SortirDonnees(self): #Fonction qui ouvre le fichier et crée une liste avec les données.
            fc = open('classement.txt','r')
            l=fc.readlines()
            fc.close()
            
            for i,val in enumerate(l):
                y=val.split(";")
                y[1]=y[1].rstrip()
                l[i]=y
            print("l=",l)
            self.classement=l
    
            
        def TriFichier(self): #Fonction qui sort les fichiers du doc texte et le trie.
            
            self.SortirDonnees()
            self.classement=tri_bulle(self.classement)
            self.classement.reverse()
            print(self.classement)
            

        def PseudoetScore(self):#Ouvre une nouvelle fenetre et demande à l'utilisateur 
                                #de rentrer un pseudo afin de pouvoir enregister son score
            z=Label(fenetrePseudo, text='Enregistrez votre score',font=('arial',18)) #Titre : entrez votre score
            z.grid(row=0, column=0, columnspan=3)
            
            self.r = Entry(fenetrePseudo) #zone pour entrer son pseudo
            self.r.grid(row=1, column=1, padx=5, pady=50)
            
            y=Label(fenetrePseudo, text='Pseudo:',font=('arial',12)) #zone de texte pseudo
            y.grid(row=1, column=0, columnspan=1)
            
            x=Label(fenetrePseudo, text='Score:',font=('arial',12))  #zone de texte score
            x.grid(row=2, column=0, columnspan=1)
            
            score = Label(fenetrePseudo, text=self.score, font=('arial',12)) #affichage du score
            score.grid(row=2, column=1)
            
            self.buttonValider = Button(fenetrePseudo, text='Valider',font=('arial',12), #boutton de validation qui fait appel à la fonction suivante ValiderP())
                                        command= lambda : TOP.ValiderP(self.r), width=15)
            self.buttonValider.grid(row=1, column=2, padx=50)
            
            
        def ValiderP(self,r): #Fonction qui vérifie qu'un pseudo a été entré et ouvre la fenêtre Classement.
            #Entree: pseudo entré par l'utilisateur en entry de PseudoetScore()
            #Sortie : appel de nouveau PseudoetScore() si aucun pseudo entré, ouvre la fenetre de Classement sinon.
            self.pseudo=r.get()
            if self.pseudo == '':
                self.PseudoetScore()
            else:
                self.ScorePerso()
                self.SortirDonnees()
                self.TriFichier()
                fenetrePseudo.destroy()
                
              #  """IL FAUT FERMER LA FENETRE ACTUELLE ET OUVRIR LA FENETRE "FENETRECLASSEMENT""""
               
        def AffClassement(self): #Fonction d'affichage du classement, on trie le fichier juste avant d'afficher afin de prendre en compte le nouveau score.
            self.TriFichier()
            z=Label(fenetreClassement, text='Classement:',font=('arial',22)) 
            z.grid(row=0, column=1, columnspan=2)
            
            texte_pseudo=Label(fenetreClassement, text='Pseudo',font=('arial',12)) #texte pseudo et score
            texte_pseudo.grid(row=1, column=1)
            texte_score=Label(fenetreClassement, text='Score:' ,font=('arial',12)) 
            texte_score.grid(row=1, column=2)
            
            premier=Label(fenetreClassement, text=self.classement[0][0],font=('arial',12)) #pseudo du 1er 
            premier.grid(row=2, column=1)
            premier_score=Label(fenetreClassement, text=self.classement[0][1],font=('arial',12)) #score du 1er
            premier_score.grid(row=2, column=2)
            
            deuxieme=Label(fenetreClassement, text=self.classement[1][0],font=('arial',12)) #pseudo du 2e 
            deuxieme.grid(row=3, column=1)
            deuxieme_score=Label(fenetreClassement, text=self.classement[1][1],font=('arial',12)) #score du 2e
            deuxieme_score.grid(row=3, column=2)
            
            troisieme=Label(fenetreClassement, text=self.classement[2][0],font=('arial',12)) #pseudo du 3e 
            troisieme.grid(row=4, column=1)
            troisieme_score=Label(fenetreClassement, text=self.classement[2][1],font=('arial',12)) #score du 3e
            troisieme_score.grid(row=4, column=2)
    
            quatrieme=Label(fenetreClassement, text=self.classement[3][0],font=('arial',12)) #pseudo du 4e
            quatrieme.grid(row=5, column=1)
            quatrieme_score=Label(fenetreClassement, text=self.classement[3][1],font=('arial',12)) #score du 4e
            quatrieme_score.grid(row=5, column=2)
            
            cinquieme=Label(fenetreClassement, text=self.classement[4][0],font=('arial',12)) #pseudo du 5e
            cinquieme.grid(row=6, column=1)
            cinquieme_score=Label(fenetreClassement, text=self.classement[4][1],font=('arial',12)) #score du 5e
            cinquieme_score.grid(row=6, column=2)
            
            Quitter =  Button(fenetreClassement, text='Quitter',font=('arial',12), command=fenetreClassement.destroy)
            Quitter.grid(row=7, column=2, pady=20)
            Rejouer = Button(fenetreClassement, text='Rejouer',font=('arial',12), command=self.Rejouer)
            Rejouer.grid(row=7, column=1, pady=20)
            
    def tri_bulle(tab): #permet d'effectuer un tri bulle
        n = len(tab)
        # Traverser tous les éléments du tableau
        for i in range(n):
            for j in range(0, n-i-1):
                # échanger si l'élément trouvé est plus grand que le suivant
                if int(tab[j][1]) > int(tab[j+1][1]) :
                    tab[j], tab[j+1] = tab[j+1], tab[j]
        return tab
    
#PROGRAMME PRINCIPAL
    FenetreMenu = Tk()
    FenetreMenu.title('Space Invader')
    Truc=Commandes(FenetreMenu)
    
    #bouton pour lancer le jeu avec les paramètres changés ou par défaut
    buttonJouer = Button(FenetreMenu, text='Jouer',width=20, command=FenetreMenu.destroy)
    buttonJouer.pack(padx=5, pady=5)
    
    # bouton pour choisir son fond d'écran
    buttonFond = Button(FenetreMenu, text='Choisissez votre fond',width=20, command=Truc.FondEcran)
    buttonFond.pack(padx=5,pady=5)
    
    #bouton pour paramétrer les commandes de déplacement avec le clavier.
    buttonChangeCommand1 = Button(FenetreMenu, text='changer les touches',width=20, command= Truc.Lettres)
    buttonChangeCommand1.pack(padx=5,pady=5)

    FenetreMenu.mainloop()
    
    
    FenetrePrincipale = Tk()    
    Jeu1=Jeu(FenetrePrincipale)
    FenetrePrincipale.title('SpaceInvader')
        
    BoutonJouer=  Button (FenetrePrincipale, text='Démarrer' ,command= Jeu1.univers)
    BoutonJouer.pack (padx=3,  pady= 3)
    
    BoutonQuitter = Button (FenetrePrincipale, text='Quitter', command= FenetrePrincipale.destroy)
    BoutonQuitter.pack (padx=3,  pady= 3)
    
    CanvasJeu = Canvas(FenetrePrincipale, height = 500, width = 500 , bg='black')
    CanvasJeu.pack (padx=3,  pady= 3)
    Background = PhotoImage(file=Truc.fondecran)
    CanvasJeu.create_image(250,250, anchor=CENTER ,image=Background)
    Ship = PhotoImage(file='ship.gif')
    Ship = Ship.subsample(10,10)
    Vaisseau = CanvasJeu.create_image(250, 450 , anchor=CENTER ,image=Ship)
    
    CanvasJeu.bind_all(Truc.x, Jeu1.Droite)
    CanvasJeu.bind_all(Truc.y, Jeu1.Gauche)
        
    FenetrePrincipale.mainloop()
    
    #============================================================================================
    
    #3 eme partie ; le score à la fin de la partie
   
    fichierClassement = open("classement.txt", "a")   #la liste des joueurs ayant participés
    
    #==============================================================================    
    TOP = Classement()
    #==============================================================================
    
    #INITIALISATION:
    TOP.SortirDonnees()
    TOP.TriFichier()
    
    #OUVERTURE PREMIERE FENETRE
    fenetrePseudo = Tk()
    TOP.SortirDonnees()
    fenetrePseudo.title('Enregistrement score')
    fenetrePseudo.geometry("450x200+400+200")
    TOP.PseudoetScore()
    TOP.SortirDonnees()
    TOP.TriFichier()
    
    fenetrePseudo.mainloop()
    #===============================================================================
    #OUVERTURE DEUXIEME FENETRE
    fenetreClassement= Tk()

    fenetreClassement.title('Classement')
    fenetreClassement.geometry("300x250+400+200")
    TOP.SortirDonnees()

    TOP.TriFichier()
    TOP.AffClassement()
    fenetreClassement.mainloop()

launch()


