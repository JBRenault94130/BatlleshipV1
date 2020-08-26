#!/usr/local/bin/python3.8
# -*-coding:Utf-8 -*

"""Fichier d'installation de notre script salut.py."""

from cx_Freeze import setup, Executable

# On appelle la fonction setup
setup(
    name = "Serveur BattleShip",
    version = "1.0",
    description = "Serveur de la bataille navale",
    executables = [Executable("mainServeur.py")],
)