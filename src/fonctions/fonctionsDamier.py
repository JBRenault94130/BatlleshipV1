#!/usr/local/bin/python3.8
# -*-coding:Utf-8 -*
from src.classes.exceptions.ExceptionsBateau import *
def encoder(x,y) :
	"""Renvoie un string correspondant à la case : encode(0,3) renvoie "A4" """
	_y=str(y+1)
	_x=""
	if(x==0) :
		_x="A"
	elif(x==1) :
		_x="B"
	elif(x==2) :
		_x="C"
	elif(x==3) :
		_x="D"
	elif(x==4) :
		_x="E"
	elif(x==5) :
		_x="F"
	elif(x==6) :
		_x="G"
	elif(x==7) :
		_x="H"
	elif(x==8) :
		_x="I"
	elif(x==9) :
		_x="J"
	else :
		raise PositionError("position impossible a")
	if(y+1>10) :
		raise PositionError("position impossible b")
	else :
		return(_x+_y)

def decoder(pos) :
	"""Renvoie un couple d'abscisse ordonnee correspondant à la case : decode("A4") renvoie 0,3 """
	_x=pos[0]
	x=-1
	_y = pos[1:]
	y=int(pos[1:])-1
	if(_x=="A") :
		x=0
	elif(_x=="B") :
		x=1
	elif(_x=="C") :
		x=2
	elif(_x=="D") :
		x=3
	elif(_x=="E") :
		x=4
	elif(_x=="F") :
		x=5
	elif(_x=="G") :
		x=6
	elif(_x=="H") :
		x=7
	elif(_x=="I") :
		x=8
	elif(_x=="J") :
		x=9
	else :
		raise PositionError(_x+_y+" n'existe pas")
	if(y>=10) :
		raise PositionError(_x+_y+" n'existe pas")
	else :
		return(y,x)