#!/usr/local/bin/python3.8
# -*-coding:Utf-8 -*

from tkinter import *
from src.classes.Joueur import *
from src.fonctions.fonctionsInterface import *
from src.interface_graphique.InterfaceEnLigne import *
import os
import socket

class InterfaceDebut(Frame):
    
	"""Notre fenêtre principale.
	Tous les widgets sont stockés comme attributs de cette fenêtre."""
	def __init__(self, fenetre, **kwargs):
		"""turtle.setpos(10,10)
		turtle.pd()
		turtle.fd(5)
		turtle.right(90)
		turtle.fd(5)
		turtle.right(90)
		turtle.fd(5)
		turtle.right(90)
		turtle.fd(5)
		turtle.right(90)
		turtle.pu()"""

		self.fenetre = fenetre
		#back = PhotoImage(file = "../images_interface/background_depart.png",master=fenetre)
		Frame.__init__(self, fenetre,background="blue", width=500, height=200, **kwargs)
		
		self.pack(fill=BOTH,expand=1)
		self.bouton_retour = None
		self.message = Label(self, text="BattleShip",font = ("Helvetica",24,"bold italic"),fg="white",bg="black")
		self.message.pack(side="top",fill=X)
		self.message_charge = Label(self,text="Chargement")


		self.bouton_hl = Button(self, text="Partie hors-ligne", bg="green",fg="white", command=self.horsLigne)
		self.bouton_hl.pack(side="left",padx=10)

		self.bouton_re = Button(self, text="Partie en ligne", bg="green" ,fg="white",command=self.enLigne)
		self.bouton_re.pack(side="right",padx=10)

		self.bouton_quitter = Button(self, text="Quitter", bg="red",fg="white", command=self.quitter)
		self.bouton_quitter.place(x=200,y=165,width=100,height=30)		# Création de nos widgets

	def quitter(self) :
		self.quit()

	def enLigne(self) :
		self.destroy()
		try :
			serveur = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
			serveur.connect(('localhost',12800))
		except ConnectionError :
			print("serveur hors-ligne")
			os._exit(1)
		else :
			instance = InterfaceConnexion(self.fenetre,serveur)

	def horsLigne(self) :
		self.destroy()
		instance = InterfaceHorsLigne(self.fenetre)
		instance.mainloop()
		os._exit(0)

def lancerInterfaceDebut() :
	fenetre = Tk()
	fenetre.title("BattleShip v1")
	fenetre.geometry("500x200")
	interface = InterfaceDebut(fenetre)

	interface.mainloop()


