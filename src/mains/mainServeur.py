#!/usr/local/bin/python3.8
# -*-coding:Utf-8 -*

from src.classes.Joueur import *
from src.fonctions.coteServeur import *
import socket
import select

serveur = initialiserServeur()
lecture(serveur)