#!/usr/local/bin/python3.8
# -*-coding:Utf-8 -*
from src.classes.Bateau import *
from src.classes.Joueur import *
from src.classes.Damier import *
from src.classes.exceptions.ExceptionsBateau import *
from src.fonctions.fonctionsDamier import *
import random
import time

class Partie :

	def __init__(self,joueur1,damier1,joueur2,damier2) :
		self.timer = time.time()
		self.enCours = True
		self.joueur1=joueur1
		self.joueur2=joueur2
		self.tour = [random.choice([self.joueur2,self.joueur1])]
		self.grille1 = damier1
		self.grille2 = damier2
		self.posinit = "Z20"
		self.previousDirec = "a"
		self.tempDir = ""
		self.gagnant = None
		self.perdant = None

	def initTest(self):
		pass

	def trouveCaseIA(self,pos,posinit="",direc = "",direcTestees = []) :
		y, x = decoder(pos)
		#print(pos+" "+direc)
		if(direc=="") : #A l'initialisation, on teste si les cases alentour sont touchées (pos vaut forcement -2)

			tstMurD = False
			tstMurG = False
			tstMurB = False
			tstMurH = False
			try :
				if(self.grille1.getValue(x+1,y)==-2) :
					return(self.trouveCaseIA(encoder(x+1,y),posinit=pos,direc="d"))
			except ValueError :
				tstMurD = True
			try :
				if(self.grille1.getValue(x-1,y)==-2) :
					return(self.trouveCaseIA(encoder(x-1,y),posinit=pos,direc="g"))
			except ValueError :
				tstMurG = True
			try :
				if(self.grille1.getValue(x,y+1)==-2) :
					return(self.trouveCaseIA(encoder(x,y+1),posinit=pos,direc="b"))
			except ValueError :
				tstMurB = True
			try :
				if(self.grille1.getValue(x,y-1)==-2) :
					return(self.trouveCaseIA(encoder(x,y-1),posinit=pos,direc="h"))
			except ValueError :
				tstMurH = True

			if(not tstMurD) :
				if(self.grille1.getValue(x+1,y)>=0) :
					self.tempDir = "d"
					return(encoder(x+1,y))
			if(not tstMurG) :
				if(self.grille1.getValue(x-1,y)>=0) :
					self.tempDir = "g"
					return(encoder(x-1,y))
			if(not tstMurB) :
				if(self.grille1.getValue(x,y+1)>=0) :
					self.tempDir = "b"
					return(encoder(x,y+1))
			if(not tstMurH) :
				if(self.grille1.getValue(x,y-1)>=0) :
					self.tempDir = "h"
					return(encoder(x,y-1))
		elif(direc=="d") :
			if("d" not in direcTestees) :
				try :
					if(self.grille1.getValue(x+1,y)==-2) :
						return(self.trouveCaseIA(encoder(x+1,y),posinit=posinit,direc="d",direcTestees=direcTestees))
				except ValueError :
					direcTestees.append("d")
					return(self.trouveCaseIA(posinit,posinit=posinit,direc="g",direcTestees=direcTestees))
				else :
					if(self.grille1.getValue(x+1,y)>=0) :
						self.tempDir = "d"
						return(encoder(x+1,y))
					else :
						direcTestees.append("d")
						return(self.trouveCaseIA(posinit,posinit=posinit,direc="g",direcTestees=direcTestees))
			else :
				return(self.trouveCaseIA(posinit,posinit=posinit,direc="h",direcTestees=direcTestees))

		elif(direc=="g") :
			if("g" not in direcTestees) :
				try :
					if(self.grille1.getValue(x-1,y)==-2) :
						return(self.trouveCaseIA(encoder(x-1,y),posinit=posinit,direc="g",direcTestees=direcTestees))
				except ValueError :
					direcTestees.append("g")
					return(self.trouveCaseIA(posinit,posinit=posinit,direc="d",direcTestees=direcTestees))
				else :
					if(self.grille1.getValue(x-1,y)>=0) :
						self.tempDir = "g"
						return(encoder(x-1,y))
					else :
						direcTestees.append("g")
						return(self.trouveCaseIA(posinit,posinit=posinit,direc="d",direcTestees=direcTestees))
			else :
				return(self.trouveCaseIA(posinit,posinit=posinit,direc="b",direcTestees=direcTestees))
		elif(direc=="b") :
			if("b" not in direcTestees) :
				try :
					if(self.grille1.getValue(x,y+1)==-2) :
						return(self.trouveCaseIA(encoder(x,y+1),posinit=posinit,direc="b",direcTestees=direcTestees))
				except ValueError :
					direcTestees.append("b")
					return(self.trouveCaseIA(posinit,posinit=posinit,direc="h",direcTestees=direcTestees))
				else :
					if(self.grille1.getValue(x,y+1)>=0) :
						self.tempDir = "b"
						return(encoder(x,y+1))
					else :
						direcTestees.append("b")
						return(self.trouveCaseIA(posinit,posinit=posinit,direc="h",direcTestees=direcTestees))
			if("b" in direcTestees) :
				return(self.trouveCaseIA(posinit,posinit=posinit,direc="d",direcTestees=direcTestees))
		elif(direc=="h") :
			if("h" not in direcTestees) :
				try :
					if(self.grille1.getValue(x,y-1)==-2) :
						return(self.trouveCaseIA(encoder(x,y-1),posinit=posinit,direc="h",direcTestees=direcTestees))
				except ValueError :
					direcTestees.append("h")
					return(self.trouveCaseIA(posinit,posinit=posinit,direc="b",direcTestees=direcTestees))
				else :
					if(self.grille1.getValue(x,y-1)>=0) :
						self.tempDir = "h"
						return(encoder(x,y-1))
					else :
						direcTestees.append("h")
						return(self.trouveCaseIA(posinit,posinit=posinit,direc="b",direcTestees=direcTestees))
			else :
				return(self.trouveCaseIA(posinit,posinit=posinit,direc="g",direcTestees=direcTestees))				

	def tourIA(self) :
		coordTir = ""
		listeTouche = self.grille1.getCoordFromValue(-2)
		retour = ""
		if(len(listeTouche) == 0) :
			listeAbs = ["A","B","C","D","E","F","G","H","I","J"]
			listeOrd = ["1","2","3","4","5","6","7","8","9","10"]
			lettre = random.choice(listeAbs)
			numero = random.choice(listeOrd)
			coordTir = lettre+numero
			try :
				self.tirer(coordTir)
			except NoHarmException :
				pass
			except ToucheException :
				pass
			except ToucheCouleException :
				pass
			except PositionError :
				self.tourIA()
		else :
			if(self.previousDirec=="a") :
				coord = listeTouche[0]
				coordTir = self.trouveCaseIA(coord,direcTestees=[])
				try :
					self.tirer(coordTir)
				except NoHarmException :
					retour="aleau"
				except ToucheException :
					retour="touche"
					self.previousDirec = self.tempDir
				except ToucheCouleException :
					self.previousDirec = "a"
					retour="coule"
			else :
				coord = listeTouche[0]
				coordTir = self.trouveCaseIA(coord,direc = self.previousDirec,posinit=coord,direcTestees=[])
				try :
					self.tirer(coordTir)
				except NoHarmException :
					retour="aleau"
				except ToucheException :
					retour="touche"
					self.previousDirec = self.tempDir
				except ToucheCouleException :
					self.previousDirec = "a"
					retour="coule"

	def placerIA(self) :
		self.placerIAPorteAvion()
		self.placerIACroiseur()
		self.placerIASousMarin()
		self.placerIAContreTorpilleur()
		self.placerIATorpilleur()

	def placerIAPorteAvion(self) :
		listeAbs = ["A","B","C","D","E","F","G","H","I","J"]
		listeOrd = ["1","2","3","4","5","6","7","8","9","10"]
		listeDir = ["haut","bas","droite","gauche"]
		x = random.choice(listeAbs)
		y = random.choice(listeOrd)
		direction = random.choice(listeDir)
		pos = x+y
		pA = PorteAvion()
		try :
			self.grille2.placer(direction,pos,pA)
		except MauvaisPlacementError :
			self.placerIAPorteAvion()

	def placerIACroiseur(self) :
		listeAbs = ["A","B","C","D","E","F","G","H","I","J"]
		listeOrd = ["1","2","3","4","5","6","7","8","9","10"]
		listeDir = ["haut","bas","droite","gauche"]
		x = random.choice(listeAbs)
		y = random.choice(listeOrd)
		direction = random.choice(listeDir)
		pos = x+y
		c = Croiseur()
		try :
			self.grille2.placer(direction,pos,c)
		except MauvaisPlacementError :
			self.placerIACroiseur()

	def placerIASousMarin(self) :
		listeAbs = ["A","B","C","D","E","F","G","H","I","J"]
		listeOrd = ["1","2","3","4","5","6","7","8","9","10"]
		listeDir = ["haut","bas","droite","gauche"]
		x = random.choice(listeAbs)
		y = random.choice(listeOrd)
		direction = random.choice(listeDir)
		pos = x+y
		sM = SousMarin()
		try :
			self.grille2.placer(direction,pos,sM)
		except MauvaisPlacementError :
			self.placerIASousMarin()

	def placerIAContreTorpilleur(self) :
		listeAbs = ["A","B","C","D","E","F","G","H","I","J"]
		listeOrd = ["1","2","3","4","5","6","7","8","9","10"]
		listeDir = ["haut","bas","droite","gauche"]
		x = random.choice(listeAbs)
		y = random.choice(listeOrd)
		direction = random.choice(listeDir)
		pos = x+y
		cT = ContreTorpilleur()
		try :
			self.grille2.placer(direction,pos,cT)
		except MauvaisPlacementError :
			self.placerIAContreTorpilleur()

	def placerIATorpilleur(self) :
		listeAbs = ["A","B","C","D","E","F","G","H","I","J"]
		listeOrd = ["1","2","3","4","5","6","7","8","9","10"]
		listeDir = ["haut","bas","droite","gauche"]
		x = random.choice(listeAbs)
		y = random.choice(listeOrd)
		direction = random.choice(listeDir)
		pos = x+y
		t = Torpilleur()
		try :
			self.grille2.placer(direction,pos,t)
		except MauvaisPlacementError :
			self.placerIATorpilleur()


	def tirer(self,pos) :
		if(self.tour[0]==self.joueur1) :
			try :
				self.grille2.tirer(pos)
			except ToucheCouleException :
				self.tourTermine()
				ordonnee, absisse = decoder(pos)
				#self.grilleAdverse1.changer(absisse,ordonnee,-3)
				raise ToucheCouleException("")
			except ToucheException :
				self.tourTermine()
				ordonnee, absisse = decoder(pos)
				#self.grilleAdverse1.changer(absisse,ordonnee,-2)
				raise ToucheException("")
			else :
				self.tourTermine()
				#self.grilleAdverse1.tirer(pos)
				raise NoHarmException("Dans l'eau.")

		else :
			try :
				self.grille1.tirer(pos)
			except ToucheCouleException :
				self.tourTermine()
				ordonnee, absisse = decoder(pos)
				#self.grilleAdverse2.changer(absisse,ordonnee,-3)
				raise ToucheCouleException("")
			except ToucheException :
				self.tourTermine()
				ordonnee, absisse = decoder(pos)
				#self.grilleAdverse2.changer(absisse,ordonnee,-2)
				raise ToucheException("")
			else :
				self.tourTermine()
				#self.grilleAdverse2.tirer(pos)
				raise NoHarmException("Dans l'eau.")

	def tourTermine(self) :
		if(self.tour[0]==self.joueur1) :
			self.tour = [self.joueur2]
		else :
			self.tour = [self.joueur1]

	def testFin(self) :
		if(len(self.grille1.getCoordFromValue(1))==0) :
			self.enCours = False
			self.gagnant = self.joueur2
			self.perdant = self.joueur1
			return(not self.enCours)
		elif(len(self.grille2.getCoordFromValue(1))==0) :
			self.enCours = False
			self.gagnant = self.joueur1
			self.perdant = self.joueur2
			return(not self.enCours)

