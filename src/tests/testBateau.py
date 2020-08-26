#!/usr/local/bin/python3.8
# -*-coding:Utf-8 -*
import unittest
from src.classes.Damier import *
from src.classes.Bateau import *
from src.fonctions.fonctionsDamier import *
from src.classes.exceptions.ExceptionsBateau import *

class TestBateau(unittest.TestCase) :
	def setUp(self) :
		self.dNew = Damier()
		self.b = Bateau(5,5,2,"PorteAvion")
		self.p = PorteAvion()

		"""self.dCharge = Damier()
		self.dCharge.change(0,0,1)
		self.dCharge.change(19,19,1)
		self.dCharge.change(10,10,-1)"""

		#print(self.b.position)
	def testGetPosition(self) :
		self.dNew.placer("bas","A1",self.p)
		liste = ["A1","A2","A3","A4","A5"]
		self.assertEqual(liste,self.p.getPosition())
		self.setUp()
		self.dNew.placer("haut","H10",self.p)
		liste = ["H10","H9","H8","H7","H6"]
		self.assertEqual(liste,self.p.getPosition())
		self.setUp()
		self.dNew.placer("droite","F1",self.p)
		liste = ["F1","G1","H1","I1","J1"]
		self.assertEqual(liste,self.p.getPosition())
		self.setUp()
		self.dNew.placer("gauche","G10",self.p)
		liste = ["G10","F10","E10","D10","C10"]
		self.assertEqual(liste,self.p.getPosition())

	def testEstTouche(self) :
		with self.assertRaises(ToucheException):
			self.p.est_touche()
		self.assertEqual(self.p.pv,4)
		with self.assertRaises(ToucheException):
			self.p.est_touche()
		self.assertEqual(self.p.pv,3)
		with self.assertRaises(ToucheException):
			self.p.est_touche()
		self.assertEqual(self.p.pv,2)
		with self.assertRaises(ToucheException):
			self.p.est_touche()
		self.assertEqual(self.p.pv,1)

		with self.assertRaises(ToucheCouleException) :
			self.p.est_touche()
		self.assertEqual(self.p.pv,0)


	"""def testChange(self) :
		self.dNew.change(0,0,1)
		self.dNew.change(19,19,1)
		self.dNew.change(10,10,-1)
		self.assertEqual(self.dNew.liste[5][5],0)
		self.assertEqual(self.dNew.liste[0][0],1)
		self.assertEqual(self.dNew.liste[19][19],1)
		self.assertEqual(self.dNew.liste[10][10],-1)
		with self.assertRaises(ValueError):
			self.dNew.change(20,1,2)
		with self.assertRaises(ValueError):
			self.dNew.change(-1,1,2)
		with self.assertRaises(ValueError):
			self.dNew.change(1,20,2)
		with self.assertRaises(ValueError):
			self.dNew.change(0,-1,2)

	def testGetValue(self) :
		self.assertEqual(self.dCharge.getValue(0,0),1)
		self.assertEqual(self.dCharge.getValue(10,10),-1)
		self.assertEqual(self.dCharge.getValue(19,19),1)
		self.assertEqual(self.dCharge.getValue(1,1),0)

	def testGetCoordFromValue(self) :
		liste1 = self.dCharge.getCoordFromValue(1)
		self.assertTrue("T20" in liste1)
		self.assertTrue("A1" in liste1)
		self.assertFalse("K11" in liste1)

		liste2 = self.dCharge.getCoordFromValue(-1)
		self.assertTrue("K11" in liste2)
		self.assertFalse("A11" in liste2)

		liste0 = self.dCharge.getCoordFromValue(0)
		self.assertEqual(len(liste0),397)

		self.assertTrue(self.dCharge.getCoordFromValue(5)==[])"""