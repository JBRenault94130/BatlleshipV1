#!/usr/local/bin/python3.8
# -*-coding:Utf-8 -*
from threading import Thread
from threading import RLock
from tkinter import *
from tkinter.ttk import *
import pickle
from src.classes.Joueur import *
from src.classes.StructureJoueurs import *
from src.interface_graphique.InterfaceHorsLigne import *
import socket
import os
import time
from src.classes.Partie import *
from src.fonctions.fonctionsInterface import *

class InterfaceJeuEL(Frame) :
	def __init__(self,fenetre,serveur,joueur,**kwargs) :
		fenetre.title("BattleShip v1 (hors-ligne) "+joueur.pseudo)
		Frame.__init__(self, fenetre, width=500, height=700, **kwargs)
		self.serveur = serveur
		self.pack(fill=BOTH)
		self.tst = True
		self.tstDamier = False
		self.partieEnCours = True
		self.fenetre = fenetre
		self.joueur = joueur
		self.aPlace = False
		self.timer = time.time()
		self.joueur.debutPartie()
		self.IA = Joueur("Ordinateur")
		self.d1 = Damier()
		self.d2 = Damier()
		self.message = Label(self,text="Etape 1 : Placez vos bateaux")
		style = Style()
 
		style.theme_use('default')
 
		style.configure("blue.Horizontal.TProgressbar", background='blue')
		self.barreCherche = Progressbar(self,length=100,style="blue.Horizontal.TProgressbar")
		self.message.pack(fill=X)
		self.partie = Partie(self.joueur,self.d1,self.IA,self.d2)
		#self.partie.placerIA()
		self.partie.tour[0] = self.joueur
		self.d2 = self.partie.grille2
		self.grillePerso = GrillePlacement(self,self.partie)
		self.grilleTir = GrilleTirEL(self,self.grillePerso,self.partie,self.joueur,self.serveur)
		self.message.pack()
		self.grillePerso.pack()
		self.grilleTir.pack(padx=60)
		self.valider = Button(self,text="Valider",fg="white",bg="green",command=self.valider)
		self.valider.pack()
		self.quitter = Button(self,text="Quitter",command=self.quit,fg="black",bg="red")
		self.quitter.pack()

	def quit(self) :
		self.tst = False
		if(self.partieEnCours) :
			self.joueur.partieELPerdue()
		if(not self.tstDamier) :
			self.serveur.send("abandon")
		self.serveur.send(b"arret jeu")
		time.sleep(0.1)
		self.serveur.send(b"joueur deconnecte")
		time.sleep(0.1)
		self.serveur.send(pickle.dumps(self.joueur))
		time.sleep(0.1)
		self.serveur.send(b"fin exit(0)")
		time.sleep(0.1)
		self.destroy()
		self.fenetre.destroy()

	def valider(self) :
		if(self.grillePerso.remplie()) :
			self.grillePerso.disableGrille()
			#print(self.partie.grille1)
			#print(self.partie.grille2)
			self.message.config(text="Etape 2 : Attente du joueur adverse")
			self.valider.destroy()
			self.grillePerso.valider.destroy()
			self.grillePerso.choix.pA.destroy()
			self.grillePerso.choix.cT.destroy()
			self.grillePerso.choix.c.destroy()
			self.grillePerso.choix.t.destroy()
			self.grillePerso.choix.sM.destroy()
			self.tstDamier = True
			self.serveur.send(b"envoi damier")
			time.sleep(0.1)
			self.serveur.send(pickle.dumps(self.grillePerso.damier))
			time.sleep(0.1)
			self.serveur.send(pickle.dumps(self.joueur))
			_osef = self.serveur.recv(9999).decode()
			retour = "attente"
			#print(retour)
			self.tstCherche = True
			self.barreCherche.pack()
			while(self.tstCherche) :
				self.tstCherche = (retour=="attente")
				time.sleep(0.1)
				self.serveur.send(b"attente damier")
				retour = self.serveur.recv(9999).decode()
				if(retour!="attente") :
					break
				self.barreCherche.step()
				try :
					self.barreCherche.update()
					self.update()
				except :
					pass
			self.barreCherche.destroy()
			if(retour=="partie") :
				self.partie = pickle.loads(self.serveur.recv(9999))
				self.message.config(text="Etape 3 : Jouer")
				self.message.update()
				self.update()
				if(self.partie.tour[0].pseudo == self.joueur.pseudo) :
					self.grilleTir.actualiserPartie()
					self.grilleTir.enableGrille()
				else :
					#self.serveur.send(b"attente joueur")
					retour2 = self.serveur.recv(9999).decode()
					self.partie = pickle.loads(self.serveur.recv(9999))
					self.grillePerso.partie = self.partie
					for bouton, val in self.grillePerso.grille.listeCases :
						y, x = decoder(bouton.getCoord())
						if(self.partie.joueur1.pseudo == self.joueur.pseudo) :
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
						else :
							if(self.partie.grille2.getValue(x,y)==-1) :
								bouton.config(bg = "grey")
							elif(self.partie.grille2.getValue(x,y)==-2) :
								bouton.config(bg = "red")
							elif(self.partie.grille2.getValue(x,y)==-3) :
								bouton.config(bg = "black")
							elif(self.partie.grille2.getValue(x,y)==1) :
								bouton.config(bg = "green")
							else :
								bouton.config(bg = "white")
					self.grilleTir.actualiserPartie()
					self.grilleTir.enableGrille()
					
			else :
				self.partieEnCours = False
				self.message.config(text="Le joueur adverse a abandonné...")
				self.joueur.partieELGagnee()


class GrilleTirEL(Frame) :
	def __init__(self,interface,grille,partie,joueur,serveur,**kwargs) :
		Frame.__init__(self,interface,width = 330,height = 390, **kwargs)
		self.joueur = joueur
		self.serveur = serveur
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

	def actualiserPartie(self) :
		self.partie = self.interface.partie
		if(self.partie.joueur1.pseudo==self.joueur.pseudo) :
			self.listeBateau = self.partie.grille2.listeBateau
		else :
			self.listeBateau = self.partie.grille1.listeBateau

	def tirer(self) :
		try :
			self.partie.tirer(self.valeur.get())
		except ToucheException :
			for rb in self.listeRadio :
				if(rb.cget("value")==self.valeur.get()) :
					rb.config(bg="red",state="disabled")
				rb.config(state="disabled")
				rb.update()
				self.update()
				self.interface.update()
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
					rb.update()
					self.update()
					self.interface.update()
		except NoHarmException :
			for rb in self.listeRadio :
				if(rb.cget("value")==self.valeur.get()) :
					rb.config(bg="grey",state="disabled")
				rb.config(state="disabled")
				rb.update()
				self.update()
				self.interface.update()

		self.bouton_tirer.config(state="disabled")
		self.etat = "disabled"
		self.serveur.send(b"a joue")
		time.sleep(0.1)
		self.serveur.send(pickle.dumps(self.partie))
		time.sleep(0.1)
		if(self.partie.testFin()) :
			self.partieEnCours = False
			self.serveur.send(b"fin partie")
			time.sleep(0.1)
			self.joueur.finPartie()
			self.serveur.send(pickle.dumps(self.joueur))
			"""file = open("../localdata/dataJoueur","wb")
			pickle.dump(self.joueur,file)
			file.close()"""
			if(self.partie.gagnant.pseudo==self.joueur.pseudo) :
				self.interface.message.config(text="Vous avez gagné",fg="green")
				
				self.interface.joueur.partieELGagnee()
				self.interface.message.update()
				self.interface.update()
				if(self.interface.joueur.pseudo!="__localhost__") :
					"""with open("../localdata/dataJoueur","wb") as file :
						pickle.dump(self.joueur,file)
						file.close()"""
					pass
			else :
				self.interface.message.config(text="Vous avez perdu",fg="red")
				try :
					self.interface.joueur.partieELPerdue()
				except :
					pass
				if(self.interface.joueur.pseudo!="__localhost__") :
					"""with open("../localdata/dataJoueur","wb") as file :
						pickle.dump(self.interface.joueur,file)
						file.close()"""
					pass
		else :
			try :
				self.partie = self.attenteJeu()
			except PartieTermineeException :
				self.joueur.partieELGagnee()
				self.joueur.finPartie()
				self.interface.message.config(text="Le joueur adverse a abandonné")
				self.interface.partieEnCours = False
			except PartiePerdueException :
				self.interface.partieEnCours = False
				self.joueur.finPartie()
				self.interface.message.config(text="Vous avez perdu",fg="red")
				self.joueur.partieELPerdue()
				self.serveur.send(b"renvoi joueur")
				time.sleep(0.1)
				self.serveur.send(pickle.dumps(self.joueur))
				time.sleep(0.1)
			else :
				self.grillePerso.partie = self.partie
				for bouton, val in self.grillePerso.grille.listeCases :
					y, x = decoder(bouton.getCoord())
					if(self.partie.joueur1.pseudo == self.joueur.pseudo) :
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
					else :
						if(self.partie.grille2.getValue(x,y)==-1) :
							bouton.config(bg = "grey")
						elif(self.partie.grille2.getValue(x,y)==-2) :
							bouton.config(bg = "red")
						elif(self.partie.grille2.getValue(x,y)==-3) :
							bouton.config(bg = "black")
						elif(self.partie.grille2.getValue(x,y)==1) :
							bouton.config(bg = "green")
						else :
							bouton.config(bg = "white")
				self.grillePerso.update()
				self.enableGrille()

	def attenteJeu(self) :
		retour = self.serveur.recv(1024).decode()
		if(retour=="partie interrompue") :
			raise PartieTermineeException("Le joueur adverse a abandonné")
		elif(retour == "perdu") :
			raise PartiePerdueException("Vous avez perdu")
		else :
			retour = pickle.loads(self.serveur.recv(9999))
			return(retour)