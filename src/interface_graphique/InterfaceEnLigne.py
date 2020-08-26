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
from src.interface_graphique.InterfaceJeu import *

argFonfNoir = dict()
argFonfNoir["fg"] = "white"
argFonfNoir["background"] = "black"

class InterfaceConnexion(Frame):
    
	"""Notre fenêtre principale.
	Tous les widgets sont stockés comme attributs de cette fenêtre."""
	def __init__(self, fenetre,serveur, **kwargs):
		fenetre.geometry("700x224")
		self.fenetre = fenetre
		Frame.__init__(self, fenetre, width=760, height=570,background="black", **kwargs)
		self.serveur=serveur
		self.pack(fill=BOTH)
		self.bouton_retour = None
		self.messagenoConnect = Label(self, text="Mot de passe ou login erroné", fg = "red")
		self.reinitTot()
		# Création de nos widgets

	def connexion(self) :
		try :

			login = self.var_log.get()
			mdp = self.var_key.get()
			if(self.var_case.get()==1) :
				with open("localdata/identifiants","wb") as file :
					_temp = (login,mdp)
					pickle.dump(_temp,file)
			else :
				os.system("rm -f localdata/identifiants")
			tstActual = True
			try :
				file = open("localdata/dataJoueur","rb")
			except FileNotFoundError :
				tstActual = False
			else :
				joueurActuel = pickle.load(file)
				file.close()
				if(joueurActuel.pseudo != "__localhost__") :
					self.serveur.send(b"actualiser profil")
					time.sleep(0.1)
					self.serveur.send(login.encode())
					time.sleep(0.1)
					self.serveur.send(mdp.encode())
					time.sleep(0.1)
					joueurActuel=pickle.dumps(joueurActuel)
					self.serveur.send(joueurActuel)
					_osef = self.serveur.recv(1024)
					#print(_osef.decode())
			self.serveur.send(b"tentative connexion")
			time.sleep(0.1)
			self.serveur.send(login.encode())
			time.sleep(0.1)
			self.serveur.send(mdp.encode())
			retour = self.serveur.recv(1024)
			
			if(retour == b"False") :
				self.message.config(text="Mot de passe ou login errone",fg="red")
				self.ligne_log.config(background="red")
				self.ligne_key.config(background="red")
			elif(retour == b"deja connecte") :
				self.message.config(text="Ce compte est déjà connecté",fg="red")
				self.ligne_log.config(background="red")
				self.ligne_key.config(background="red")
			else :
				retour = pickle.loads(retour)
				with open("localdata/dataJoueur","wb") as file :
					pickle.dump(retour,file)
				lancerInterfaceUtilisateur(self,self.serveur,self.fenetre,retour)
		except BrokenPipeError :
			print("serveur hors-ligne")
			self.serveur.close()
			self.destroy()
			self.fenetre.destroy()
			os._exit(1)
		


	def reinitTot(self) :
		try :
			file = open("localdata/identifiants","rb")
			file.close()
		except FileNotFoundError :
			self.var_log = StringVar()
			self.ligne_log = Entry(self, textvariable=self.var_log,justify="center", width=30)
			#self.ligne_log.pack()

			self.var_key = StringVar()
			self.ligne_key = Entry(self, textvariable=self.var_key,justify="center", width=30,show="*")
			#self.ligne_key.pack()

			self.var_case = IntVar()
			self.case = Checkbutton(self, text="Se souvenir de moi", variable=self.var_case)
			#self.case.pack(side="top")
		else :
			log=""
			mdp=""
			with open("localdata/identifiants","rb") as file :
				log,mdp = pickle.load(file)
			self.var_log = StringVar()
			self.ligne_log = Entry(self, textvariable=self.var_log,justify="center", width=25)
			self.var_log.set(log)
			#self.ligne_log.pack()

			self.var_key = StringVar()
			self.ligne_key = Entry(self, textvariable=self.var_key,justify="center", width=25,show="*")
			self.var_key.set(mdp)
			#self.ligne_key.pack()

			self.var_case = IntVar()
			self.var_case.set(1)
			self.case = Checkbutton(self, text="Se souvenir de moi", variable=self.var_case)
			#self.case.pack(side="top")
		finally :
			"""self.cadreSup = Label(self,text="BattleShip",width=60,height=5)
			self.cadreSup.pack(side="top",fill=X,padx=0,pady=0,ipadx=0,ipady=0)"""
			self.message = Label(self, text="Connectez-vous ou créez un compte.",**argFonfNoir)
			self.message.pack()

			self.message2 = Label(self, text="Login",**argFonfNoir)
			self.message2.pack()


			self.ligne_log.pack()

			self.message3 = Label(self, text="Mot de passe",**argFonfNoir)
			self.message3.pack()

			self.ligne_key.pack()

			self.case.pack(side="top",pady=5)

			self.bouton_co = Button(self, text="Connectez vous", fg="red", command=self.connexion,background="black")
			self.bouton_co.pack(side="left")
			self.bouton_re = Button(self, text="Inscrivez vous", fg="red", command=self.inscription,background="black")
			self.bouton_re.pack(side="right")

			self.bouton_quitter = Button(self, text="Quitter", command=self.quit,background="red")
			self.bouton_quitter.pack(side="bottom",pady=5)
			self.bouton_retour = Button(self, text="Retour", command=self.retour,**argFonfNoir)
			self.bouton_retour.pack(side="bottom",pady=5)
			self.ligne_log.focus()

	def retour(self) :
		self.serveur.send(b"fin exit(0)")
		self.serveur.close()
		self.destroy()
		self.fenetre.destroy()
		os.system("python3.8 -m src.mains.mainDebut")


	def quit(self) :
		self.serveur.send(b"fin exit(0)")
		self.serveur.close()
		self.destroy()
		self.fenetre.destroy()

	def inscription(self) :
		lancerInterfaceInscription(self.fenetre,self,self.serveur)


class ChargeReception(Thread) :
	def __init__(self,serveur,barre) :
		Thread.__init__(self)
		self.serveur = serveur
		self.tst = True
		self.retour = ""
		self.barre = barre

	def run(self) :
		self.serveur.send(b"cherche adversaire")
		self.retour = self.serveur.recv(1024).decode()
		self.barre.step()
		self.barre.update()
		

class ChargeAffichage(Thread) :
	def __init__(self,barre,reception) :
		Thread.__init__(self)
		self.barre=barre
		self.tst = True

	def run(self) :
		pass


class InterfaceUtilisateur(Frame):
    
	"""Notre fenêtre principale.
	Tous les widgets sont stockés comme attributs de cette fenêtre."""
	def __init__(self, serveur,fenetre,joueur, **kwargs):
		fenetre.title("Battleship v1 "+joueur.pseudo)
		fenetre.geometry("700x284")
		self.fenetre = fenetre
		Frame.__init__(self, fenetre, width=(7680/2), height=(5760/2), **kwargs)
		self.serveur=serveur
		self.joueur = joueur
		self.tst = True
		self.pack(fill=BOTH)
		self.message = Label(self, text="Bienvenue "+self.joueur.pseudo)
		self.message2 = Label(self,text="Niveau "+str(self.joueur.niveau))
		self.el = Label(self,text="Ratio en ligne : "+str(self.joueur.getRatioEL()))
		self.nbPart = Label(self,text="Nombre de parties en ligne : "+str(self.joueur.nbPartiesEL))
		self.message.pack(side="top")
		self.message2.pack()
		self.el.pack()
		self.nbPart.pack()
		style = Style()
 
		style.theme_use('default')
 
		style.configure("green.Horizontal.TProgressbar", background='green')

		style.configure("blue.Horizontal.TProgressbar", background='blue')
		self.barre2 = Progressbar(self,length=100,style = "blue.Horizontal.TProgressbar",mode="determinate")
		self.barre2["value"]=0
		self.messageCharge = Label(self,text="")

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
		self.bouton_co = Button(self, text="Chercher un adversaire", fg="white",background="blue", command=self.lancerJeu)
		self.bouton_co.pack()
		self.bouton_quitter = Button(self, text="Quitter", command=self.quit,bg="red",fg="white")
		self.tstCherche = False
		self.bouton_quitter.pack(side="bottom")

	def lancerJeu(self) :
		retour = "pas encore"
		self.bouton_co.config(state = "disabled")
		self.bouton_quitter.config(state="disabled")
		self.messageC = Label(self,text="Recherche d'adversaire : ")
		self.messageC.pack()
		self.bouton_arret_recherche = Button(self, text="Arret recherche",fg="white",bg="red",command=self.arretAttente)
		

		style = Style()
 
		style.theme_use('default')
 
		style.configure("green.Horizontal.TProgressbar", background='green')

		style.configure("blue.Horizontal.TProgressbar", background='blue')
		self.barre2 = Progressbar(self,length=100,style = "blue.Horizontal.TProgressbar",mode="determinate")
		self.barre2["value"]=0
			
		self.barre2.pack()
		self.bouton_arret_recherche.pack()
		self.serveur.send(b"cherche")
		retour = self.serveur.recv(1024).decode()
		#print(retour)
		time.sleep(0.1)
		self.tstCherche = True
		while(self.tstCherche) :
			self.tstCherche = (retour!="trouve")
			self.serveur.send(b"attente")
			retour = self.serveur.recv(1024).decode()
			self.barre2.step()
			self.barre2.update()
			self.update()
		self.messageCharge.destroy()
		self.messageC.destroy()
		self.barre2.destroy()
		if(retour=="trouve") :
			self.messageCharge = Label(self,text="Joueur Trouvé !")
			self.messageCharge.pack(side="bottom")
			self.messageCharge.update()
			self.bouton_arret_recherche.destroy()
			self.update()
			time.sleep(2)
			self.tst=False
			self.destroy()
			self.fenetre.geometry("500x700")
			self.fenetre.enJeu = True
			interface = InterfaceJeuEL(self.fenetre,self.serveur,self.joueur)
			interface.mainloop()
			if(interface.tst) :
				if(interface.partieEnCours) :
					interface.joueur.partieELPerdue()
					if(not interface.tstDamier) :
						interface.serveur.send(b"abandon")
					interface.serveur.send(b"arret jeu")
					time.sleep(0.1)
				interface.serveur.send(b"joueur deconnecte")
				time.sleep(0.1)
				interface.serveur.send(pickle.dumps(self.joueur))
				time.sleep(0.1)
				interface.serveur.send(b"fin exit(0)")
		else :
			self.messageCharge = Label(self,text="Pas de joueur trouvé")
			self.messageCharge.pack(side="bottom")

	def arretAttente(self) :
		self.tstCherche = False
		self.tstCherche = False
		self.serveur.send(b"arret attente")
		self.bouton_co.config(state = "normal")
		self.bouton_quitter.config(state="normal")
		self.barre2.destroy()
		self.messageC.destroy()
		self.messageCharge.destroy()
		self.bouton_arret_recherche.destroy()


	def quit(self) :
		self.tst = False
		self.serveur.send(b"arret attente")
		time.sleep(0.1)
		self.serveur.send(b"joueur deconnecte")
		time.sleep(0.1)
		self.serveur.send(pickle.dumps(self.joueur))
		time.sleep(0.1)
		self.serveur.send(b"fin exit(0)")
		self.serveur.close()
		self.destroy()
		self.fenetre.destroy()




class InterfaceInscription(Frame):
    
	"""Notre fenêtre principale.
	Tous les widgets sont stockés comme attributs de cette fenêtre."""
	def __init__(self, fenetre,serveur, **kwargs):
		fenetre.geometry("250x290")
		fenetre.config(bg="black")
		self.fenetre = fenetre
		Frame.__init__(self, fenetre, width=(7680/2), height=(5760/2),bg="black", **kwargs)
		self.serveur=serveur
		self.pack(fill=BOTH)
		self.bouton_retour = None
		self.message = Label(self, text="Inscription",fg="blue",bg="black",font=("Helvetica",18))
		self.message.pack()

		self.message2 = Label(self, text="Login",fg="white",bg="black")
		self.message2.pack()


		self.var_log = StringVar()
		self.ligne_log = Entry(self, textvariable=self.var_log, width=30,bg="white",fg="black")
		self.ligne_log.pack()

		self.message3 = Label(self, text="Mot de passe",fg="white",bg="black")
		self.message3.pack()

		self.var_key = StringVar()
		self.ligne_key = Entry(self, textvariable=self.var_key, width=30,show="*",bg="white",fg="black")
		self.ligne_key.pack()

		self.message4 = Label(self, text="Pseudo",fg="white",bg="black")
		self.message4.pack()

		self.var_pseudo = StringVar()
		self.ligne_pseudo = Entry(self, textvariable=self.var_pseudo, width=30,bg="white",fg="black")
		self.ligne_pseudo.pack()

		self.bouton_in = Button(self, text="Inscription", bg="green",fg="white", command=self.envoi)
		self.bouton_in.pack(pady=5)

		self.bouton_re = Button(self, text="Retour connexion",bg="blue",fg="white", command=self.retour)
		self.bouton_re.pack(pady=5)

		self.bouton_quitter = Button(self, text="Quitter", bg="red",fg="white", command=self.quitter)
		self.bouton_quitter.pack(pady=5)		# Création de nos widgets

	def quitter(self) :
		self.serveur.send(b"fin exit(0)")
		self.serveur.close()
		self.destroy()
		self.fenetre.destroy()


	def envoi(self) :
		try :
			essaiInscription(self,self.fenetre,self.var_log.get(),self.var_key.get(),self.var_pseudo.get(),self.serveur)
		except BrokenPipeError :
			print("serveur hors-ligne")
			self.serveur.close()
			self.destroy()
			self.fenetre.destroy()
			os._exit(1)

	def retour(self) :
		retourInterface(self,self.fenetre,self.serveur)

class InterfaceIntermediaire(Frame):
    
	"""Notre fenêtre principale.
	Tous les widgets sont stockés comme attributs de cette fenêtre."""
	def __init__(self, fenetre,serveur, **kwargs):
		self.fenetre = fenetre
		Frame.__init__(self, fenetre, width=(7680/2), height=(5760/2), **kwargs)
		self.serveur=serveur
		self.pack(fill=BOTH)
		self.bouton_retour = None
		self.message = Label(self, text="Bravo ! Vous êtes bien inscrits")
		self.message.pack()

		self.message2 = Label(self, text="Appuyez sur le bouton pour revenir à l'écran de connexion")
		self.message2.pack()

		self.bouton_re = Button(self, text="Retour connexion", command=self.retour)
		self.bouton_re.pack()

		self.bouton_quitter = Button(self, text="Quitter", fg="red", command=self.quitter)
		self.bouton_quitter.pack()		# Création de nos widgets

	def quitter(self) :
		self.serveur.send(b"fin exit(0)")
		self.serveur.close()
		self.destroy()
		self.fenetre.destroy()

	def retour(self) :
		retourInterface(self,self.fenetre,self.serveur)

def essaiInscription(frame,fenetre,login,mdp,pseudo,serveur) :
	serveur.send(b"tentative inscription")
	time.sleep(0.1)
	serveur.send(login.encode())
	time.sleep(0.1)
	serveur.send(mdp.encode())
	time.sleep(0.1)
	serveur.send(pseudo.encode())
	retour = serveur.recv(1024).decode()
	if(retour == "False login") :
		frame.ligne_log.config(background = "red")
		frame.ligne_pseudo.config(background = "white")
		frame.ligne_key.config(background = "white")
	elif(retour == "False pseudo") :
		frame.ligne_pseudo.config(background = "red")
		frame.ligne_log.config(background = "white")
		frame.ligne_key.config(background = "white")
	elif(retour == "False encodage") :
		frame.ligne_pseudo.config(background = "white")
		frame.ligne_log.config(background = "red")
		frame.ligne_key.config(background = "red")
	elif(retour == "Done") :
		joueur = Joueur(pseudo)
		with open("localdata/dataJoueur","wb") as file :
			pickle.dump(joueur,file)
		lancerInterfaceIntermediaire(frame,fenetre,serveur)
	else :
		raise CommunicationError("Message inattendu")

def lancerInterfaceIntermediaire(frame,fenetre,serveur) :
	frame.destroy()
	interface = InterfaceIntermediaire(fenetre,serveur)

	interface.mainloop()
	#interface.destroy()

def retourInterface(frame,fenetre,serveur) :
	frame.destroy()
	interface = InterfaceConnexion(fenetre,serveur)

	interface.mainloop()
	#interface.destroy()


def lancerInterfaceInscription(fenetre,frame,serveur) :
	frame.destroy()
	interface = InterfaceInscription(fenetre,serveur)

	interface.mainloop()
	#interface.destroy()

def lancerInterfaceUtilisateur(frame,serveur,fenetre,joueur) :
	frame.destroy()
	interface = InterfaceUtilisateur(serveur,fenetre,joueur)
	interface.mainloop()
	if(interface.tst) :
		try :
			serveur.send(b"arret attente")
			time.sleep(0.1)
			serveur.send(b"joueur deconnecte")
			time.sleep(0.1)
			serveur.send(pickle.dumps(joueur))
			time.sleep(0.1)
			serveur.send(b"fin exit(0)")
		except BrokenPipeError:
			print("serveur hors-ligne")
		finally :
			serveur.close()

def lancerInterface(serveur) :
	fenetre = Tk()
	interface = InterfaceConnexion(fenetre,serveur)

	interface.mainloop()
	#fenetre.destroy()