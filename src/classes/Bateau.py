#!/usr/local/bin/python3.8
# -*-coding:Utf-8 -*
from src.classes.exceptions.ExceptionsBateau import *
from src.classes.Damier import *
import re



class Bateau :
	"""Classe mère modélisant les bateaux"""
	cpt = 0
	def __init__(self,taille,pv,carburant,nom) :
		"""La plupart des parametres sont renvoyées par les initialisations d'objets héritants de celui la """
		self.taille=taille
		self._pv = pv
		self.pv = pv
		self.carburant = carburant
		self._carburant = carburant
		self.nom = nom
		self.aFlot = True
		self.position = []
		self.id = Bateau.cpt
		Bateau.cpt+=1

	def __repr__(slef) :
		return("Le "+nom+" a "+str(pv)+" PV et il lui reste "+str(self.carburant)+" en carburant")

	def __str__(slef) :
		return("Le "+nom+" a "+str(pv)+" PV et il lui reste "+str(self.carburant)+" en carburant")

	"""def peut_bouger(self) :
		return(self.carburant!=0)"""

	"""def avance(self,direction) :
		if(self.peut_bouger()) :
			if(self.aFlot) :
				self.carburant-=1
				absisse, ordonnee = 
			else :
				raise EstMortError("Ce "+self.nom+" a coulé et ne peut donc plus avancer")
		else :
			raise NoMovementException("Plus de carburant")  #A définir !"""

	"""def ravitaille(self,nb) :
		if(self.aFlot) :
			if(self.carburant+nb>self._carburant) :
				self.carburant=self._carburant
			else :
				self.carburant+=nb
		else :
			raise EstMortError("Ce "+self.nom+" est déjà coulé : il ne peut être ravitaillé.")"""

	def getPosition(self) :
		"""Retourne la liste des positions du bateau"""
		return(self.position)

	def est_touche(self) :
		"""vérifie su le bateau est coulé, lui enlève 1 pv sinon"""
		self.pv-=1
		if(self.pv<=0) :
			self.pv = 0
			self.est_coule()
		else :
			raise ToucheException("Le "+self.nom+" est touché!")

	def est_coule(self) :
		"""Si le bateau est coulé, envoie une exception"""
		self.aFlot = False
		raise ToucheCouleException("Le "+self.nom+" est coulé!")

class PorteAvion(Bateau) :
	"""Classe porte-avions, elle posséde 2 chasseurs de reconnaissance et a une longueur de 5 cases"""
	def __init__(self) :
		Bateau.__init__(self,5,5,2,"porte-avion")
		self.chasseurs = 2
		self._chasseurs = 2

	"""def reconaissance(self) :
		if(self.pv!=0) :
			self.chasseurs -= 1
			if(self.chasseur == 0) :
				raise NoWeaponError("Plus de chasseurs")
		else :
			raise EstMortError("Ce "+self.nom+" a déjà coulé : il ne peut pas envoyer de chasseurs.")

	def ravitaille(self,nbChasseur) :
		Bateau.ravitaille(self)
		self.chasseurs = self._chasseurs

	def tire(self) :
		raise NoWeaponError("Un porte-avion n'a pas de missiles.")"""

class SousMarin(Bateau) :
	"""Classe sous-marin : 3 cases"""
	def __init__(self) :
		Bateau.__init__(self,3,3,10,"sous-marin")
		#self.missiles = 10
		#self._missiles = 10

	"""def tire(self) :
		self.missiles-=1"""

class Torpilleur(Bateau) :
	"""Classe torpilleur : 2 cases"""
	def __init__(self) :
		Bateau.__init__(self,2,2,15,"torpilleur")
		#self.missiles = 5
		#self._missiles = 5

class ContreTorpilleur(Bateau) :
	"""Classe contre-torpilleur : 3 cases"""
	def __init__(self) :
		Bateau.__init__(self,3,3,15,"contre-torpilleur")
		#self.missiles = 5
		#self._missiles = 5

class Croiseur(Bateau) :

	def __init__(self) :
		Bateau.__init__(self,4,4,15,"croiseur")
		#self.missiles = 5
		#self._missiles = 5