#!/usr/local/bin/python3.8
# -*-coding:Utf-8 -*
from tkinter import *
import socket

def initialiserClient() :
	serveur = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	serveur.connect(('localhost',12800))
	return(serveur)

