#!/usr/local/bin/python3.8
# -*-coding:Utf-8 -*
import re
from src.fonctions.fonctionsDamier import *
from src.classes.exceptions.ExceptionsBateau import *
from src.classes.Bateau import *
class Damier() :
    """Damier modélisant une moitié du jeu
            Barême : 0 : rien sur la case
                     1 : un bateau sur la case
                     -1 : une case vide sur laquelle on a tiré
                     -2 : une case ou un bateau a été touché
                     -3 : une case ou un bateau est coulé
        self.liste contient la matrice dans laquelle on place les bateaux

        self.listeBateau contient la liste des bateau placés



    """
    cmpt=0
    def __init__(self,*args) :
        """On initialise la matrice avec des 0 et la listeBateau à une liste vide si aucun parametre
        On copie le damier qui est mis en parametre


        """
        self.liste = []
        self.listeBateau = []
        if(not args) :
            for i in range(0,10) :
                liste1=[]
                for j in range(0,10) :
                    liste1.append(0)
                self.liste.append(list(liste1))
            self.id=int(Damier.cmpt)
            Damier.cmpt+=1
        else :
            for el in args :
                self.liste = list(el.liste)
                self.listeBateau = list(el.listeBateau)
                self.id=int(Damier.cmpt)
                Damier.cmpt+=1
                break

    def __repr__(self) :
        string = "[\n"
        for i in self.liste :
            string+=str(i)+"\n"
        string+= "\n]"
        return(string)

    def __str__(self) :
        string = "[\n"
        for i in self.liste :
            string+=str(i)+"\n"
        string+= "]"
        return(string)

    def tirer(self,pos) :
        """Lance un tir sur la cellule selectionnée"""
        ordonnee, absisse = decoder(pos)
        if(self.getValue(absisse,ordonnee)==0) :
            self.changer(absisse,ordonnee,-1)
        elif(self.getValue(absisse,ordonnee)==1) :
            self.changer(absisse,ordonnee,-2)
            for bat in self.listeBateau :
                for coord in bat.position :
                    if(coord == pos):
                        try :
                            bat.est_touche()
                        except ToucheCouleException :
                            for coordo in bat.position :
                                ordo , absi = decoder(coordo)
                                self.changer(absi,ordo,-3)
                            nom = str(bat.nom)
                            #self.listeBateau.remove(bat)
                            raise ToucheCouleException("Le "+nom+" est coulé.")
                        except ToucheException :
                            raise ToucheException("")

        else :
            raise PositionError("Vous ne pouvez pas tirer en "+pos)

    def estVide(self) :
        return(self.listeBateau==[])

    def changer(self,absisse,ordonnee,val) :
        """Change la valeur d'une case de la matrice"""

        if(absisse<0 or absisse>9 or ordonnee<0 or ordonnee>9) :
            raise ValueError
        else :
            self.liste[ordonnee][absisse] = val

    def getValue(self,absisse,ordonnee) :
        """renvoie la valeur d'une case de la matrice"""
        if(absisse<0 or absisse>9 or ordonnee<0 or ordonnee>9) :
            raise ValueError
            return(None)
        else :
            return(self.liste[ordonnee][absisse])

    def getCoordFromValue(self,val) :
        """Renvoie la liste des cases sur lesquelles la valeur est celle entrée en parametres. Exemple ["A10","E8"]"""
        liste = []
        cpt1 = 0
        cpt2 = 0
        for i in self.liste :
            cpt2 = 0
            for j in i :
                if(val==j) :
                    liste.append(encoder(cpt2,cpt1))
                cpt2+=1
            cpt1+=1
        return(liste)

    def placer(self,direction,pos,bateau) :
        """Place un bateau sur la matrice"""
        tst = True
        _damier = Damier(self)
        #print(pos+"fin")
        ordonnee, absisse = decoder(pos)            

        if(direction=="haut") :
            for i in range(0,bateau.taille) :
                if(ordonnee-i<0) :
                    tst = False
                elif(self.getValue(absisse,ordonnee-i)==1) :
                        raise MauvaisPlacementError("Un bateau se trouve déjà ici")
            if(tst) :
                for i in range(0,bateau.taille) :
                    bateau.position.append(encoder(absisse,ordonnee-i))
                    self.changer(absisse,ordonnee-i,1)
                self.listeBateau.append(bateau)
            else :
                self = Damier(_damier)
                raise MauvaisPlacementError("On ne peut pas placer ce bateau dans ce sens à cet endroit")
        elif(direction=="bas") :
            for i in range(0,bateau.taille) :
                if(ordonnee+i>=10) :
                    tst = False
                elif(self.getValue(absisse,ordonnee+i)==1) :
                        raise MauvaisPlacementError("Un bateau se trouve déjà ici")
            if(tst) :
                for i in range(0,bateau.taille) :
                    bateau.position.append(encoder(absisse,ordonnee+i))
                    self.changer(absisse,ordonnee+i,1)
                self.listeBateau.append(bateau)
            else :
                self = Damier(_damier)
                raise MauvaisPlacementError("On ne peut pas placer ce bateau dans ce sens à cet endroit")
        elif(direction=="droite") :
            for i in range(0,bateau.taille) :
                if(absisse+i>=10) :
                    #print(str(absisse+i)+" "+str(ordonnee))
                    tst = False
                elif(self.getValue(absisse+i,ordonnee)==1) :
                        raise MauvaisPlacementError("Un bateau se trouve déjà ici")
            if(tst) :
                for i in range(0,bateau.taille) :
                    bateau.position.append(encoder(absisse+i,ordonnee))
                    self.changer(absisse+i,ordonnee,1)
                self.listeBateau.append(bateau)
            else :
                self = Damier(_damier)
                raise MauvaisPlacementError("On ne peut pas placer ce bateau dans ce sens à cet endroit")           

        elif(direction=="gauche") :
            for i in range(0,bateau.taille) :
                if(absisse-i<0) :
                    tst = False
                elif(self.getValue(absisse-i,ordonnee)==1) :
                        raise MauvaisPlacementError("Un bateau se trouve déjà ici")
            if(tst) :
                for i in range(0,bateau.taille) :
                    bateau.position.append(encoder(absisse-i,ordonnee))
                    self.changer(absisse-i,ordonnee,1)
                self.listeBateau.append(bateau)
            else :
                self = Damier(_damier)
                raise MauvaisPlacementError("On ne peut pas placer ce bateau dans ce sens à cet endroit")
        else :
            raise NameError(direction+" n'est pas une direction.")
