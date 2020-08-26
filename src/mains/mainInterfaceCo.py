#!/usr/local/bin/python3.8
# -*-coding:Utf-8 -*

from src.classes.Joueur import *
from src.classes.StructureJoueurs import *
from src.fonctions.fonctionsInterface import *
from src.interface_graphique.InterfaceDebut import *
import os
try :
	serveur = initialiserClient()
except ConnectionRefusedError :
	print("serveur hors-ligne")
else :
	lancerInterface(serveur)