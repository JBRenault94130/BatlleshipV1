#!/usr/local/bin/python3.8
# -*-coding:Utf-8 -*
import unittest
from src.classes.Damier import *
from src.classes.Bateau import *
from src.fonctions.fonctionsDamier import *
from src.classes.exceptions.ExceptionsBateau import *

class TestDamier(unittest.TestCase) :
	def setUp(self) :
		self.dNew = Damier()
		self.dCharge = Damier()
		self.dCharge.changer(0,0,1)
		self.dCharge.changer(9,9,1)
		self.dCharge.changer(1,1,-1)
		self.b = Bateau(5,5,2,"PorteAvion")
		self.p = PorteAvion()

	def testInitDamier(self) :
		d = Damier(self.dCharge)
		self.assertEqual(d.liste[0][0],1)
		self.assertEqual(d.liste[9][9],1)
		self.assertEqual(d.liste[1][1],-1)

	def testPlacer(self) :
		self.dNew.placer("bas","A2",self.b)
		for i in range(0,5) :
			self.assertEqual(self.dNew.getValue(0,1+i),1)
		

		self.dNew.placer("droite","D4",self.p)
		for i in range(0,5) :
			self.assertEqual(self.dNew.getValue(i+3,3),1)

		self.dNew.placer("gauche","I8",self.p)
		for i in range(0,5) :
			self.assertEqual(self.dNew.getValue(8-i,7),1)

		self.dNew.placer("haut","J10",self.p)
		for i in range(0,5) :
			self.assertEqual(self.dNew.getValue(9,9-i),1)
		#print(self.dNew)


		with self.assertRaises(NameError) :
			self.dNew.placer("lol","D4",self.p)

		with self.assertRaises(MauvaisPlacementError) :
			self.dNew.placer("droite","G1",self.p)

		with self.assertRaises(MauvaisPlacementError) :
			self.dNew.placer("gauche","D1",self.p)

		with self.assertRaises(MauvaisPlacementError) :
			self.dNew.placer("bas","D7",self.p)

		with self.assertRaises(MauvaisPlacementError) :
			self.dNew.placer("haut","D4",self.p)

		with self.assertRaises(PositionError) :
			self.dNew.placer("droite","J11",self.p)

		with self.assertRaises(PositionError) :
			self.dNew.placer("droite","K10",self.p)

		with self.assertRaises(MauvaisPlacementError) :
			self.dNew.placer("droite","F10",self.p)

	def testTirer(self) :
		self.dNew.placer("bas","A1",self.p)
		with self.assertRaises(ToucheException):
			self.dNew.tirer("A3")
		self.assertEqual(self.dNew.getValue(0,2),-2)
		self.dNew.tirer("B3")
		self.assertEqual(self.dNew.getValue(1,2),-1)
		with self.assertRaises(ToucheCouleException) :
			try :
				self.dNew.tirer("A1")
			except(ToucheException) :
				pass
			try :
				self.dNew.tirer("A2")
			except(ToucheException) :
				pass
			try :
				self.dNew.tirer("A4")
			except(ToucheException) :
				pass
			try :
				self.dNew.tirer("A5")
			except(ToucheException) :
				pass

		with self.assertRaises(PositionError) :
			self.dNew.tirer("A1")

		with self.assertRaises(PositionError) :
			self.dNew.tirer("B3")



	def testChange(self) :
		self.dNew.changer(0,0,1)
		self.dNew.changer(9,9,1)
		self.dNew.changer(1,1,-1)
		self.assertEqual(self.dNew.liste[5][5],0)
		self.assertEqual(self.dNew.liste[0][0],1)
		self.assertEqual(self.dNew.liste[9][9],1)
		self.assertEqual(self.dNew.liste[1][1],-1)
		with self.assertRaises(ValueError):
			self.dNew.changer(10,1,2)
		with self.assertRaises(ValueError):
			self.dNew.changer(-1,1,2)
		with self.assertRaises(ValueError):
			self.dNew.changer(1,10,2)
		with self.assertRaises(ValueError):
			self.dNew.changer(0,-1,2)

	def testGetValue(self) :
		self.assertEqual(self.dCharge.getValue(0,0),1)
		self.assertEqual(self.dCharge.getValue(1,1),-1)
		self.assertEqual(self.dCharge.getValue(9,9),1)
		self.assertEqual(self.dCharge.getValue(2,2),0)

	def testGetCoordFromValue(self) :
		liste1 = self.dCharge.getCoordFromValue(1)
		self.assertTrue("J10" in liste1)
		self.assertTrue("A1" in liste1)

		liste2 = self.dCharge.getCoordFromValue(-1)
		self.assertTrue("B2" in liste2)
		self.assertFalse("A11" in liste2)

		liste0 = self.dCharge.getCoordFromValue(0)
		self.assertEqual(len(liste0),97)

		self.assertTrue(self.dCharge.getCoordFromValue(-3)==[])

#unittest.main()