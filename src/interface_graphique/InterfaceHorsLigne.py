#!/usr/local/bin/python3.8
# -*-coding:Utf-8 -*
from tkinter import *
from tkinter.ttk import *
import pickle
from src.classes.Partie import *
#from fonctions.fonctionsDamier import *
import socket
import os
import time
from src.fonctions.fonctionsInterface import *

class InterfaceJeuHL(Frame) :
	def __init__(self, fenetre,joueur, **kwargs):
		#fenetre.geometry("800x800")
		fenetre.title("BattleShip v1 (hors-ligne)")
		Frame.__init__(self, fenetre, width=500, height=700, **kwargs)
		self.pack(fill=BOTH)
		self.fenetre = fenetre
		self.joueur = joueur
		self.aPlace = False
		self.joueur.debutPartie()
		self.IA = Joueur("Ordinateur")
		self.d1 = Damier()
		self.d2 = Damier()
		self.message = Label(self,text="Etape 1 : Placez vos bateaux")
		self.message.pack(fill=X)
		self.partie = Partie(self.joueur,self.d1,self.IA,self.d2)
		self.partie.placerIA()
		self.partie.tour[0] = self.joueur
		self.d2 = self.partie.grille2
		self.grillePerso = GrillePlacement(self,self.partie)
		self.grilleTir = GrilleTir(self,self.grillePerso,self.partie)
		self.message.pack()
		self.grillePerso.pack()
		self.grilleTir.pack(padx=60)
		self.valider = Button(self,text="Valider",fg="white",bg="green",command=self.valider)
		self.valider.pack()
		self.quitter = Button(self,text="Quitter",command=self.quitter,fg="black",bg="red")
		self.quitter.pack()
		
	def quitter(self) :
		self.destroy()
		self.fenetre.destroy()

	def valider(self) :
		if(self.grillePerso.remplie()) :
			self.grillePerso.disableGrille()
			self.grilleTir.enableGrille()
			print(self.partie.grille1)
			print(self.partie.grille2)
			self.message.config(text="Etape 2 : Jouez")
			self.valider.destroy()
			self.grillePerso.valider.destroy()
			self.grillePerso.choix.pA.destroy()
			self.grillePerso.choix.cT.destroy()
			self.grillePerso.choix.c.destroy()
			self.grillePerso.choix.t.destroy()
			self.grillePerso.choix.sM.destroy()

class FramePlacementGrille(Frame) :
	def __init__(self,interface,partie,**kwargs) :
		self.interface = interface
		Frame.__init__(self,interface,width = 300, height = 300, **kwargs)
		self.partie = partie
		self.listeCases = []
		listeAbs = ["A","B","C","D","E","F","G","H","I","J"]
		listeOrd = ["1","2","3","4","5","6","7","8","9","10"]
		for i in range(10):
			Label(self,text=listeAbs[i],bg="white").grid(row=1,column=i+1+5)
			Label(self,text=listeOrd[i],bg="white").grid(row=i+2,column=0+5)
			for j in range(10):
				valeur = IntVar()
				jb = JBCheckbutton(self, variable=valeur,bg="white",command=self.checkCase)
				jb.grid(row=j+2, column=i+1+5)
				jb.coordonnee = encoder(i,j)
				jb.deselect()
				self.listeCases.append((jb,valeur))

	def checkCase(self) :
		for bouton,val in self.listeCases :
			if(val.get()==1) :
				if(bouton.cget("bg")=="white") :
					bouton.config(bg="grey")
				else :
					bouton.config(bg="white")

	def actualiser(self) :
		for bouton, val in self.listeCases :
			y, x = decoder(bouton.getCoord())
			if(self.partie.grille1.getValue(x,y)==-1) :
				bouton.config(bg = "grey")
			elif(self.partie.grille1.getValue(x,y)==-2) :
				bouton.config(bg = "red")
			elif(self.partie.grille1.getValue(x,y)==-3) :
				bouton.config(bg = "black")
			elif(self.partie.grille1.getValue(x,y)==1) :
				bouton.config(bg = "green")
			else :
				bouton.config(bg = "white")

	def reinit(self) :
		for jb,val in self.listeCases :
			if(jb.cget("state")!="disabled") :
				val.set(0)

class FrameChoixBateau(Frame) :
	def __init__(self,interface,**kwargs) :
		Frame.__init__(self,interface,**kwargs)
		self.val_bateau = StringVar()
		self.pA = Radiobutton(self,variable=self.val_bateau,text="Porte-Avion(5)     ",value="pA")
		self.c = Radiobutton(self,variable=self.val_bateau,text="Croiseur(4)",value="c")
		self.cT = Radiobutton(self,variable=self.val_bateau,text="Contre-Torpilleur(3)",value="cT")
		self.sM = Radiobutton(self,variable=self.val_bateau,text="Sous-Marin(3)",value="sM")
		self.t = Radiobutton(self,variable=self.val_bateau,text="Torpilleur(2)",value="t")

		self.dejaPlace = []

		self.pA.grid(row=0,column=0,padx=1,columnspan=2)
		self.c.grid(row=0,column=2,padx=1,columnspan=2)

		self.cT.grid(row=0,column=4,padx=1)
		self.sM.grid(row=1,column=1,padx=1,columnspan=3)
		self.t.grid(row=1,column=3,padx=1,columnspan=2)
		self.t.deselect()

	def remplie(self) :
		tst = True
		if(self.pA.cget("state")=="normal") :
			tst=False
		elif(self.c.cget("state")=="normal") :
			tst=False
		elif(self.cT.cget("state")=="normal") :
			tst=False
		elif(self.sM.cget("state")=="normal") :
			tst=False
		elif(self.t.cget("state")=="normal") :
			tst=False
		return(tst)

class GrillePlacement(Frame) :
	def __init__(self,interface,partie,**kwargs) :
		Frame.__init__(self,interface,width = 330, height = 390, **kwargs)
		self.etat = "enabled"
		self.valider = Button(self,text="Valider",fg="white",bg="red",command=self.valider)
		self.interface = interface
		self.partie=partie
		self.damier = partie.grille1
		self.grille = FramePlacementGrille(self,self.partie)
		self.grille.pack()
		self.choix = FrameChoixBateau(self)
		self.choix.pack()
		self.valider.pack()

	def actualiser(self) :
		self.grille.actualiser()

	def remplie(self) :
		return(self.choix.remplie())

	def valider(self) :
		if(self.choix.val_bateau.get()=="pA" and "pA" not in self.choix.dejaPlace) :
			tst = False
			xmin=-1
			ymin=-1
			direc = ""
			pos = []
			but = []
			for bouton,val in self.grille.listeCases :
				if(val.get()==1) :
					val.set(0)
					bouton.config(bg="white")
					pos.append(bouton.getCoord())
					but.append(bouton)
			if(len(pos)==5) :
				y1, x1 = decoder(pos[0])
				y2, x2 = decoder(pos[1])
				y3, x3 = decoder(pos[2])
				y4, x4 = decoder(pos[3])
				y5, x5 = decoder(pos[4])
				if(x1==x2==x3==x4==x5) :
					if(abs(y1-y2)<5 and abs(y2-y3)<5 and abs(y1-y3)<5 and abs(y1-y4)<5 and abs(y2-y4)<5 and abs(y3-y4)<5 and abs(y1-y5)<5 and abs(y2-y5)<5 and abs(y3-y5)<5 and abs(y4-y5)<5) :
						tst = True
						ymin = min(y1,y2,y3,y4,y5)
						xmin = x1
						direc = "bas"
				elif(y1==y2==y3==y4==y4) :
					if(abs(x1-x2)<5 and abs(x2-x3)<5 and abs(x1-x3)<5 and abs(x1-x4)<5 and abs(x2-x4)<5 and abs(x3-x4)<5 and abs(x1-x5)<5 and abs(x2-x5)<5 and abs(x3-x5)<5 and abs(x4-x5)<5) :
						tst = True
						xmin = min(x1,x2,x3,x4,x5)
						ymin = y1
						direc = "droite"
			if(tst) :
				self.partie.grille1.placer(direc,encoder(xmin,ymin),PorteAvion())
				self.choix.dejaPlace.append("pA")
				for b in but :
					b.config(state="disabled",bg="green")
					self.choix.pA.deselect()
					self.choix.pA.config(state="disabled")
					
			else :
				self.grille.reinit()
		elif(self.choix.val_bateau.get()=="c" and "c" not in self.choix.dejaPlace) :
			tst = False
			xmin=-1
			ymin=-1
			direc = ""
			pos = []
			but = []
			for bouton,val in self.grille.listeCases :
				if(val.get()==1) :
					val.set(0)
					bouton.config(bg="white")
					pos.append(bouton.getCoord())
					but.append(bouton)
			if(len(pos)==4) :
				y1, x1 = decoder(pos[0])
				y2, x2 = decoder(pos[1])
				y3, x3 = decoder(pos[2])
				y4, x4 = decoder(pos[3])
				if(x1==x2==x3==x4) :
					if(abs(y1-y2)<4 and abs(y2-y3)<4 and abs(y1-y3)<4 and abs(y1-y4)<4 and abs(y2-y4)<4 and abs(y3-y4)<4) :
						tst = True
						ymin = min(y1,y2,y3,y4)
						xmin = x1
						direc = "bas"
				elif(y1==y2==y3==y4) :
					if(abs(x1-x2)<4 and abs(x2-x3)<4 and abs(x1-x3)<4 and abs(x1-x4)<4 and abs(x2-x4)<4 and abs(x3-x4)<4) :
						tst = True
						xmin = min(x1,x2,x3,x4)
						ymin = y1
						direc = "droite"
			if(tst) :
				self.partie.grille1.placer(direc,encoder(xmin,ymin),Croiseur())
				self.choix.dejaPlace.append("c")
				for b in but :
					b.config(state="disabled",bg="green")
					self.choix.c.deselect()
					self.choix.c.config(state="disabled")
					
			else :
				self.grille.reinit()
		elif(self.choix.val_bateau.get()=="cT" and "cT" not in self.choix.dejaPlace) :
			tst = False
			xmin=-1
			ymin=-1
			direc = ""
			pos = []
			but = []
			for bouton,val in self.grille.listeCases :
				if(val.get()==1) :
					val.set(0)
					bouton.config(bg="white")
					pos.append(bouton.getCoord())
					but.append(bouton)
			if(len(pos)==3) :
				y1, x1 = decoder(pos[0])
				y2, x2 = decoder(pos[1])
				y3, x3 = decoder(pos[2])
				if(x1==x2==x3) :
					if(abs(y1-y2)<3 and abs(y2-y3)<3 and abs(y1-y3)<3) :
						tst = True
						ymin = min(y1,y2,y3)
						xmin = x1
						direc = "bas"
				elif(y1==y2==y3) :
					if(abs(x1-x2)<3 and abs(x2-x3)<3 and abs(x1-x3)<3) :
						tst = True
						xmin = min(x1,x2,x3)
						ymin = y1
						direc = "droite"
			if(tst) :
				self.partie.grille1.placer(direc,encoder(xmin,ymin),ContreTorpilleur())
				self.choix.dejaPlace.append("cT")
				for b in but :
					b.config(state="disabled",bg="green")
					self.choix.cT.deselect()
					self.choix.cT.config(state="disabled")
					
			else :
				self.grille.reinit()
		elif(self.choix.val_bateau.get()=="sM" and "sM" not in self.choix.dejaPlace) :
			tst = False
			xmin=-1
			ymin=-1
			direc = ""
			pos = []
			but = []
			for bouton,val in self.grille.listeCases :
				if(val.get()==1) :
					val.set(0)
					bouton.config(bg="white")
					pos.append(bouton.getCoord())
					but.append(bouton)
			if(len(pos)==3) :
				y1, x1 = decoder(pos[0])
				y2, x2 = decoder(pos[1])
				y3, x3 = decoder(pos[2])
				if(x1==x2==x3) :
					if(abs(y1-y2)<3 and abs(y2-y3)<3 and abs(y1-y3)<3) :
						tst = True
						ymin = min(y1,y2,y3)
						xmin = x1
						direc = "bas"
				elif(y1==y2==y3) :
					if(abs(x1-x2)<3 and abs(x2-x3)<3 and abs(x1-x3)<3) :
						tst = True
						xmin = min(x1,x2,x3)
						ymin = y1
						direc = "droite"
			if(tst) :
				self.choix.dejaPlace.append("sM")
				self.partie.grille1.placer(direc,encoder(xmin,ymin),SousMarin())
				for b in but :
					b.config(state="disabled",bg="green")
					self.choix.sM.deselect()
					self.choix.sM.config(state="disabled")
					
			else :
				self.grille.reinit()
		elif(self.choix.val_bateau.get()=="t" and "t" not in self.choix.dejaPlace) :
			tst = False
			xmin=-1
			ymin=-1
			direc = ""
			pos = []
			but = []
			for bouton,val in self.grille.listeCases :
				if(val.get()==1) :
					val.set(0)
					bouton.config(bg="white")
					pos.append(bouton.getCoord())
					but.append(bouton)
			if(len(pos)==2) :
				y1, x1 = decoder(pos[0])
				y2, x2 = decoder(pos[1])
				if(x1==x2 and (y1==y2-1 or y1==y2+1)) :
					tst=True
					ymin = min(y1,y2)
					xmin=x1
					direc = "bas"
				elif(y1==y2 and (x1==x2+1 or x1==x2-1)) :
					tst=True
					xmin=min(x1,x2)
					ymin=y1
					direc = "droite"
			if(tst) :
				self.choix.dejaPlace.append("t")
				self.partie.grille1.placer(direc,encoder(xmin,ymin),Torpilleur())
				for b in but :
					b.config(state="disabled",bg="green")
					self.choix.t.deselect()
					self.choix.t.config(state="disabled")
					
			else :
				self.grille.reinit()

	def disableGrille(self) :
		for bouton,val in self.grille.listeCases :
			bouton.config(state="disabled")
			val.set(0)
		


class JBCheckbutton(Checkbutton) :
	def __init__(self,fenetre,**kwargs) :
		Checkbutton.__init__(self,master=fenetre,**kwargs)
		self.coordonnee = "Z11"

	def getCoord(self) :
		return(self.coordonnee)

class GrilleTir(Frame) :
	def __init__(self,interface,grille,partie,**kwargs) :
		Frame.__init__(self,interface,width = 330,height = 390, **kwargs)
		self.etat = "disabled"
		self.partie=partie
		self.grillePerso = grille
		self.listeBateau = partie.grille2.listeBateau
		self.interface=interface
		self.damier = partie.grille2
		listeAbs = ["A","B","C","D","E","F","G","H","I","J"]
		listeOrd = ["1","2","3","4","5","6","7","8","9","10"]
		self.listeRadio = []
		Label(self).grid(row = 0,column=0)

		for i in range(10):
			Label(self,text=listeAbs[i],bg="white").grid(column=i+1+15,row=0)
			Label(self,text=listeOrd[i],bg="white").grid(column=0+15,row=i+1)
		self.valeur=StringVar()
		for i in range(10):
			for j in range(10):
				rb = Radiobutton(self, variable=self.valeur, value=encoder(i,j),cursor="target")
				if(self.damier.getValue(i,j)==-1) :
					rb.config(bg="grey",fg="red",state="disabled")
				elif(self.damier.getValue(i,j)==-2) :
					rb.config(bg="red",fg="white",state="disabled")
				elif(self.damier.getValue(i,j)==-3) :
					rb.config(bg="green",fg="red",state="disabled")
				else :
					rb.config(bg="white",fg="black",state="disabled")
				rb.grid(row=j+1, column=15+i+1)
				rb.deselect()
				self.listeRadio.append(rb)

		self.bouton_tirer = Button(self,text="Tirer",bg="red",fg="white",command=self.tirer,state="disabled",cursor="target")
		self.bouton_tirer.grid(column=3+15,row=17,columnspan=5)
		#self.bouton_secours = Button(self,text="DEBLOQUE!",bg="red",fg="white",command=self.enableGrille)
		#self.bouton_secours.grid(column=3,row=13,columnspan=5)
		self.texte = Label(self,text="")

	def enableGrille(self) :
		self.etat="enabled"
		for rb in self.listeRadio :
			if(rb.cget("bg")=="white") :
				rb.config(state="normal")
				rb.select()
		self.bouton_tirer.config(state="normal")

	def tirer(self) :
		try :
			self.partie.tirer(self.valeur.get())
		except ToucheException :
			for rb in self.listeRadio :
				if(rb.cget("value")==self.valeur.get()) :
					rb.config(bg="red",state="disabled")
				rb.config(state="disabled")
		except ToucheCouleException :
			position = []
			for bat in self.listeBateau :
				#print(bat.getPosition)
				if(self.valeur.get() in bat.getPosition()) :
					position = bat.getPosition()
			for coord in position :
				for rb in self.listeRadio :
					if(rb.cget("value")==coord) :
						rb.config(bg="green",state="disabled")
					rb.config(state="disabled")
		except NoHarmException :
			for rb in self.listeRadio :
				if(rb.cget("value")==self.valeur.get()) :
					rb.config(bg="grey",state="disabled")
				rb.config(state="disabled")

		self.bouton_tirer.config(state="disabled")
		self.etat = "disabled"
		if(self.partie.testFin()) :
			self.partie.joueur1.finPartie()
			if(len(self.damier.getCoordFromValue(1))==0) :
				self.interface.message.config(text="Vous avez gagné",fg="green")
				
				self.interface.joueur.partieHLGagnee()
				if(self.interface.joueur.pseudo!="__localhost__") :
					with open("localdata/dataJoueur","wb") as file :
						pickle.dump(self.interface.joueur,file)
						file.close()
			else :
				self.interface.message.config(text="Vous avez perdu",fg="red")
				try :
					self.interface.joueur.partieHLPerdue()
				except :
					pass
				if(self.interface.joueur.pseudo!="__localhost__") :
					with open("localdata/dataJoueur","wb") as file :
						pickle.dump(self.interface.joueur,file)
						file.close()
		else :
			self.partie.tourIA()
			self.grillePerso.actualiser()
			self.enableGrille()

			
			
class InterfaceHorsLigne(Frame) :
    
	"""Notre fenêtre principale.
	Tous les widgets sont stockés comme attributs de cette fenêtre."""
	def __init__(self, fenetre, **kwargs):
		self.fenetre = fenetre
		Frame.__init__(self, fenetre, width=(7680/2), height=(5760/2), **kwargs)
		self.joueur = Joueur("__localhost__")
		try :
			file1=open("localdata/dataJoueur","rb")
		except FileNotFoundError :
			self.joueur = Joueur("__localhost__")
			with open("localdata/dataJoueur","wb") as file :
				pickle.dump(self.joueur,file)
				file.close()
		else :
			self.joueur = pickle.load(file1)
		finally :
			self.pack(fill=BOTH)
			self.reinitTot()

		
		# Création de nos widgets
		

#3A37666FACCADE7D47AC6C6F34

	def jouer(self) :
		self.destroy()
		instance = InterfaceJeuHL(self.fenetre,self.joueur)
		


	def reinitTot(self) :
		
		self.message = Label(self, text="Bienvenue "+self.joueur.pseudo)
		self.message2 = Label(self,text="Niveau "+str(self.joueur.niveau))
		self.hl = Label(self,text="Ratio hors-ligne : "+str(self.joueur.getRatioHL()))
		self.el = Label(self,text="Ratio en ligne : "+str(self.joueur.getRatioEL()))
		self.nbPart = Label(self,text="Nombre total de parties : "+str(self.joueur.nbPartiesEL+self.joueur.nbPartiesHL))
		self.message.pack(side="top")
		self.message2.pack()
		self.hl.pack()
		self.el.pack()
		self.nbPart.pack()
		style = Style()
 
		style.theme_use('default')
 
		style.configure("green.Horizontal.TProgressbar", background='green')

		self.barre = Progressbar(self,length=100,style = "green.Horizontal.TProgressbar")
		self.tempsDeJeu = Label(self,text="Temps de jeu : "+str(int(self.joueur.tempsDeJeuTotal//3600))+" heure(s) "+str((int(self.joueur.tempsDeJeuTotal%3600)//60))+" minute(s) et "+str(int(self.joueur.tempsDeJeuTotal%60))+" seconde(s).")
		if(self.joueur.niveau==1) :
			self.barre["value"] = self.joueur.xp/5
		elif(self.joueur.niveau==2) :
			self.barre["value"] = self.joueur.xp/15
		elif(self.joueur.niveau==3) :
			self.barre["value"] = self.joueur.xp/50
		elif(self.joueur.niveau==4) :
			self.barre["value"] = self.joueur.xp/150
		elif(self.joueur.niveau==5) :
			self.barre["value"] = self.joueur.xp/200
		else :
			self.barre["value"] = 100
		self.tempsDeJeu.pack()
		self.barre.pack()
		self.bouton_co = Button(self, text="Lancez une partie !", fg="white",background="blue", command=self.lancerJeu)
		self.bouton_co.pack()
		self.bouton_quitter = Button(self, text="Quitter", command=self.quitter,bg="red",fg="white")
		self.bouton_quitter.pack(side="bottom")

	def quitter(self) :
		"""with open("../localdata/dataJoueur","wb") as file :
				pickle.dump(self.joueur)"""
		self.destroy()
		self.fenetre.destroy()

	def lancerJeu(self) :
		if(self.joueur.pseudo=="__localhost__") :
			self.destroy()
			interface = InterfaceQuestion(self.fenetre)
			interface.mainloop()
		else :
			self.destroy()
			self.fenetre.destroy()
			fenetre = Tk()
			fenetre.geometry("500x700")
			instance = InterfaceJeuHL(fenetre,self.joueur)
			instance.mainloop()


class InterfaceQuestion(Frame) :
    
	"""Notre fenêtre principale.
	Tous les widgets sont stockés comme attributs de cette fenêtre."""
	def __init__(self, fenetre, **kwargs):
		self.fenetre = fenetre
		Frame.__init__(self, fenetre, width=(7680/2), height=(5760/2), **kwargs)
		self.pack(fill=BOTH)
		self.reinitTot()
		# Création de nos widgets

	def reinitTot(self) :
		self.message = Label(self, text="Pour sauvegarder votre progression hors-ligne, il faut vous inscrire.")
		self.message.pack(side="top")

		self.bouton_co = Button(self, text="Inscrivez-vous !",fg="green", command=self.lancerInscription)
		self.bouton_co.pack(side="left")
		self.bouton_re = Button(self, text="Jouer sans sauvegarde", fg="red", command=self.lancerJeuHL)
		self.bouton_re.pack(side="right")
		self.bouton_quitter = Button(self, text="Quitter", command=self.quitter)
		self.bouton_quitter.pack(side="bottom")

	def quitter(self) :
		"""with open("../localdata/dataJoueur","wb") as file :
				pickle.dump(self.joueur)"""
		self.destroy()
		self.fenetre.destroy()

	def lancerInscription(self) :
		self.destroy()
		try :
			serveur = initialiserClient()
		except ConnectionRefusedError :
			self.destroy()
			self.fenetre.destroy()
			os.system("python3.8 -m src.mains.mainDebut")
			print("serveur hors-ligne")
			os._exit(1)
		else :
			instance = InterfaceInscription(self.fenetre,serveur)
			instance.mainloop()

		"""os.system("python3.8 -m mains.mainInterfaceInscr")
		os._exit(0)"""

	def lancerJeuHL(self) :
		self.destroy()
		self.fenetre.destroy()
		fenetre = Tk()
		fenetre.geometry("600x600")
		instance = InterfaceJeuHL(fenetre,Joueur("__localhost__"))
		instance.mainloop()