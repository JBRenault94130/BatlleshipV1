#!/usr/local/bin/python3.8
# -*-coding:Utf-8 -*
from tkinter import *
import pickle
from src.classes.Joueur import *
from src.classes.StructureJoueurs import *
from src.interface_graphique.InterfaceDebut import *
import socket
import os
import time

class InterfaceConnexion(Frame):
    
	"""Notre fenêtre principale.
	Tous les widgets sont stockés comme attributs de cette fenêtre."""
	def __init__(self, fenetre,serveur, **kwargs):
		self.fenetre = fenetre
		Frame.__init__(self, fenetre, width=(7680/2), height=(5760/2), **kwargs)
		self.serveur=serveur
		self.pack(fill=BOTH)
		self.bouton_retour = None
		self.messagenoConnect = Label(self, text="Mot de passe ou login erroné", fg = "red")
		self.reinitTot()
		# Création de nos widgets
		

	def reinit(self,log) :
		self.message["text"] = "Bienvenue "+log
		self.bouton_retour = Button(self, text="Se déconnecter",command=self.reinitTot())
		self.ligne_log.destroy()
		self.ligne_key.destroy()
		self.bouton_co.destroy()
		self.bouton_re.destroy()
		self.bouton_retour.pack()

#3A37666FACCADE7D47AC6C6F34

	def connexion(self) :
		try :
			login = self.var_log.get()
			mdp = self.var_key.get()
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
			else :
				retour = pickle.loads(retour)
				lancerInterfaceUtilisateur(self,self.serveur,self.fenetre,retour)
		except BrokenPipeError :
			print("serveur hors-ligne")
			self.serveur.close()
			self.destroy()
			self.fenetre.destroy()
			os._exit(1)
		


	def reinitTot(self) :
		self.message = Label(self, text="Connectez-vous ou créez un compte.")
		self.message.pack()

		self.message2 = Label(self, text="Login")
		self.message2.pack()


		self.var_log = StringVar()
		self.ligne_log = Entry(self, textvariable=self.var_log, width=30)
		self.ligne_log.pack()

		self.message3 = Label(self, text="Mot de passe")
		self.message3.pack()

		self.var_key = StringVar()
		self.ligne_key = Entry(self, textvariable=self.var_key, width=30)
		self.ligne_key.pack()

		self.bouton_co = Button(self, text="Connectez vous", fg="red", command=self.connexion)
		self.bouton_co.pack(side="left")
		self.bouton_re = Button(self, text="Inscrivez vous", fg="red", command=self.inscription)
		self.bouton_re.pack(side="right")

		self.bouton_quitter = Button(self, text="Quitter", command=self.quitter)
		self.bouton_quitter.pack(side="bottom")
        
		
		if(self.bouton_retour is not None) :
			self.bouton_retour.destroy()

	def quitter(self) :
		self.serveur.send(b"fin exit(0)")
		self.serveur.close()
		self.destroy()
		self.fenetre.destroy()

	def inscription(self) :
		lancerInterfaceInscription(self.fenetre,self,self.serveur)

class InterfaceUtilisateur(Frame):
    
	"""Notre fenêtre principale.
	Tous les widgets sont stockés comme attributs de cette fenêtre."""
	def __init__(self, serveur,fenetre,joueur, **kwargs):
		self.fenetre = fenetre
		Frame.__init__(self, fenetre, width=(7680/2), height=(5760/2), **kwargs)
		self.serveur=serveur
		self.joueur = joueur
		self.pack(fill=BOTH)
		self.bouton_retour = None
		self.message = Label(self, text="Bienvenue "+str(self.joueur.pseudo))
		self.message.pack()


		self.bouton_quitter = Button(self, text="Quitter", fg="red", command=self.quitter)
		self.bouton_quitter.pack()		# Création de nos widgets

	def quitter(self) :
		self.serveur.send(b"fin exit(0)")
		self.serveur.close()
		self.destroy()
		self.fenetre.destroy()

class InterfaceInscription(Frame):
    
	"""Notre fenêtre principale.
	Tous les widgets sont stockés comme attributs de cette fenêtre."""
	def __init__(self, fenetre,serveur, **kwargs):
		self.fenetre = fenetre
		Frame.__init__(self, fenetre, width=(7680/2), height=(5760/2), **kwargs)
		self.serveur=serveur
		self.pack(fill=BOTH)
		self.bouton_retour = None
		self.message = Label(self, text="Inscription.")
		self.message.pack()

		self.message2 = Label(self, text="Login")
		self.message2.pack()


		self.var_log = StringVar()
		self.ligne_log = Entry(self, textvariable=self.var_log, width=30)
		self.ligne_log.pack()

		self.message3 = Label(self, text="Mot de passe")
		self.message3.pack()

		self.var_key = StringVar()
		self.ligne_key = Entry(self, textvariable=self.var_key, width=30)
		self.ligne_key.pack()

		self.message4 = Label(self, text="Pseudo")
		self.message4.pack()

		self.var_pseudo = StringVar()
		self.ligne_pseudo = Entry(self, textvariable=self.var_pseudo, width=30)
		self.ligne_pseudo.pack()

		self.bouton_in = Button(self, text="Inscription", fg="green", command=self.envoi)
		self.bouton_in.pack()

		self.bouton_re = Button(self, text="Retour connexion", command=self.retour)
		self.bouton_re.pack()

		self.bouton_quitter = Button(self, text="Quitter", fg="red", command=self.quitter)
		self.bouton_quitter.pack()		# Création de nos widgets

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
		lancerInterfaceIntermediaire(frame,fenetre,serveur)
	else :
		raise CommunicationError("Message inattendu")

def essaiConnexion(fenetre,frame,login,mdp,serveur) :
	serveur.send(b"tentative connexion")
	time.sleep(0.1)
	serveur.send(login.encode())
	time.sleep(0.1)
	serveur.send(mdp.encode())
	retour = serveur.recv(1024).decode()
	if(retour == "False") :
		fenetre.message = Label(self, text="Mot de passe ou login erroné")
	else :
		lancerInterfaceUtilisateur(frame,serveur,fenetre,retour)

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
	#interface.destroy()

def lancerInterface(serveur) :
	fenetre = Tk()
	interface = InterfaceConnexion(fenetre,serveur)

	interface.mainloop()
	#fenetre.destroy()