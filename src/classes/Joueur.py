#!/usr/local/bin/python3.8
# -*-coding:Utf-8 -*
import time
from src.classes.exceptions.ExceptionsJoueur import *
class Joueur :
	compt = 0

	def __init__(self,pseudo) :
		self.pseudo = pseudo
		self.niveau = 1
		self.xp = 0
		self.nbVictoiresEL = 0
		self.nbDefaitesEL = 0
		self.nbPartiesEL = 0
		self.nbVictoiresHL = 0
		self.nbDefaitesHL = 0
		self.nbPartiesHL = 0
		self.tempsDeJeuTotal = 0.0
		self.tempsDebutJeu = 0.0
		self.creation = time.time()
		self.enAttente = False

	def debutPartie(self) :
		self.tempsDebutJeu = time.time()

	def finPartie(self) :
		self.tempsDeJeuTotal += time.time() - self.tempsDebutJeu
		self.tempsDebutJeu = 0.0

	def addXp(self,xp) :
		self.xp+=xp
		self.verifieLvl()

	def partieHLGagnee(self) :
		self.nbVictoiresHL+=1
		self.nbPartiesHL+=1
		self.addXp(500)

	def partieELGagnee(self) :
		self.nbVictoiresEL+=1
		self.nbPartiesEL+=1
		self.addXp(500)

	def lancerChrono(self) :
		self.tempsDebutJeu = time.time()

	def finChrono(self) :
		tempsFin = time.time()
		self.tempsDeJeuTotal+= tempsFin - self.tempsDebutJeu
		self.tempsDebutJeu = 0.0

	def getRatioEL(self) :
		if(self.nbPartiesEL==0) :
			return(0)
		else :
			return(self.nbVictoiresEL/self.nbPartiesEL)

	def getRatioHL(self) :
		if(self.nbPartiesHL==0) :
			return(0)
		else :
			return(self.nbVictoiresHL/self.nbPartiesHL)

	def getDateCreation(self) :
		date = time.localtime(self.creation)
		jourSem = date.tm_wday
		if(jourSem==0) :
			jourSem="Lundi"
		elif(jourSem==1) :
			jourSem="Mardi"
		elif(jourSem==2) :
			jourSem="Mercredi"
		elif(jourSem==3) :
			jourSem="Jeudi"
		elif(jourSem==4) :
			jourSem="Vendredi"
		elif(jourSem==5) :
			jourSem="Samedi"
		elif(jourSem==6) :
			jourSem="Dimanche"
		else :
			jourSem="Unknown"

		mois = date.tm_mon
		if(mois==0) :
			mois="Janvier"
		elif(mois==1) :
			mois="Février"
		elif(mois==2) :
			mois="Mars"
		elif(mois==3) :
			mois="Avril"
		elif(mois==4) :
			mois="Mai"
		elif(mois==5) :
			mois="Juin"
		elif(mois==6) :
			mois="Juillet"
		elif(mois==7) :
			mois="Août"
		elif(mois==8) :
			mois="Septembre"
		elif(mois==9) :
			mois="Octobre"
		elif(mois==10) :
			mois="Novembre"
		elif(mois==11) :
			mois="Décembre"
		else :
			mois = "Unknown"

		minutes = date.tm_min
		if(minutes<10) :
			minutes = "0"+str(date.tm_min)
		else :
			minutes = str(date.tm_min)

		rendu = "Votre compte a été créé le "+jourSem+" "+str(date.tm_mday)+" "+mois+" "+str(date.tm_year)+" à "+str(date.tm_hour)+"h"+minutes+" et "+str(date.tm_sec)+" secondes"

		return(rendu)

	def getTempsDeJeu(self) :
		_tmp = int(self.tempsDeJeuTotal)
		heures = _tmp//3600
		_tmp = _tmp%3600
		minutes = _tmp//60
		_tmp = _tmp%60
		secondes = _tmp
		return(str(heures)+" heure(s) "+str(minutes)+" minute(s) "+str(secondes)+" seconde(s)")

	def partieHLPerdue(self) :
		self.nbDefaitesHL+=1
		self.nbPartiesHL+=1
		self.addXp(0)

	def partieELPerdue(self) :
		self.nbDefaitesEL+=1
		self.nbPartiesEL+=1
		self.addXp(0)

	def matchNulEL(self) :
		self.nbPartiesEL+=1
		self.addXp(0)

	def matchNulHL(self) :
		self.nbPartiesHL+=1
		self.addXp(0)

	def verifieLvl(self) :
		if(self.niveau==1) :
			if(self.xp>=500):
				self.niveau+=1
				self.xp-=500
				#raise NewLevelException("Vous passez niveau 2")
			else :
				pass
		elif(self.niveau==2) :
			if(self.xp>=1500) :
				self.niveau+=1
				self.xp-=1500
				#raise NewLevelException("Vous passez niveau 3")
			else :
				pass
		elif(self.niveau==3) :
			if(self.xp>=5000) :
				self.niveau+=1
				self.xp-=5000
				#raise NewLevelException("Vous passez niveau 4")
			else :
				pass
		elif(self.niveau==4) :
			if(self.xp>=15000) :
				self.niveau+=1
				self.xp-=15000
				#raise NewLevelException("Vous passez niveau 5")
			else :
				pass
		elif(self.niveau==5) :
			if(self.xp>=20000) :
				self.niveau+=1
				self.xp-=20000
				#raise NewLevelException("Vous passez niveau 6")
			else :
				pass
		else :
			pass


		