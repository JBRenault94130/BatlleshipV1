#!/usr/local/bin/python3.8
# -*-coding:Utf-8 -*
import unittest
from src.classes.StructureJoueurs import *
from src.classes.Joueur import *
from src.classes.exceptions.ExceptionsStock import *

class TestStructureJoueurs(unittest.TestCase) :
	def setUp(self) :
		self.j1 = Joueur("GingerBeard")
		self.j2 = Joueur("GingerBeard")
		self.j3 = Joueur("Code pandorum")
		self.j4 = Joueur("S-Cual")
		self.structure = StructureJoueurs()
		self.structure_remplie = StructureJoueurs()
		self.structure_remplie.ajouterJoueur(self.j1,"Ginger","motdepasse")
		self.structure_remplie.ajouterJoueur(self.j3,"gingea","modepa")
		self.structure_remplie.ajouterJoueur(self.j4,"login","mdp")

	def testAjouterJoueur(self) :
		self.structure.ajouterJoueur(self.j1,"GingerBeardlololol","gingerbeard96")
		
		self.assertTrue(self.j1 in self.structure.dicoJoueurs.values())
		self.assertFalse(self.j3 in self.structure.dicoJoueurs.values())

		self.structure.ajouterJoueur(self.j3,"Ginger","karakaba")

		self.assertTrue(self.j3 in self.structure.dicoJoueurs.values())

		with self.assertRaises(PseudoExistantException) :
			self.structure.ajouterJoueur(self.j2,"lalala","lololo")

		with self.assertRaises(LoginExistantException) :
			self.structure.ajouterJoueur(self.j4,"GingerBeardlololol","lololo")

	def testGetJoueur(self) :
		self.assertEqual(self.j1,self.structure_remplie.getJoueur("Ginger","motdepasse"))
		self.assertEqual(self.j3,self.structure_remplie.getJoueur("gingea","modepa"))
		self.assertEqual(self.j4,self.structure_remplie.getJoueur("login","mdp"))

		with self.assertRaises(NoPlayerFoundException) :
			self.structure_remplie.getJoueur("Cavapasmarcher","dutout")