#!/usr/local/bin/python3.8
# -*-coding:Utf-8 -*

from src.classes.Joueur import *
from tkinter import *
from src.interface_graphique.InterfaceHorsLigne import *

fenetre = Tk()
instance = InterfaceHorsLigne(fenetre)
instance.mainloop()