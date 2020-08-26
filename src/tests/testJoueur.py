import unittest
from src.classes.Joueur import *

class TestBateau(unittest.TestCase) :
	def setUp(self) :
		self.joueur = Joueur("R2d2")

	def testMatchHL(self) :
		with self.assertRaises(NewLevelException) :
			self.joueur.partieHLGagnee()
		self.assertEqual(self.joueur.niveau,2)
		self.assertEqual(self.joueur.xp,0)

		self.joueur.partieHLGagnee()
		self.joueur.partieHLPerdue()
		self.assertEqual(self.joueur.niveau,2)
		self.assertEqual(self.joueur.xp,500)
		self.assertEqual(self.joueur.nbPartiesHL,3)

	def testMatchEL(self) :
		with self.assertRaises(NewLevelException) :
			self.joueur.partieELGagnee()
		self.assertEqual(self.joueur.niveau,2)
		self.assertEqual(self.joueur.xp,0)

		self.joueur.partieELGagnee()
		self.joueur.partieELPerdue()
		self.assertEqual(self.joueur.niveau,2)
		self.assertEqual(self.joueur.xp,500)
		self.assertEqual(self.joueur.nbPartiesEL,3)