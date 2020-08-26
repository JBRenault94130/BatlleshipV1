#!/usr/local/bin/python3.8
# -*-coding:Utf-8 -*
class NewLevelException(Exception) :
	def __init__(self,message) :
		self.message=message

	def __str__(self) :
		return(self.message)

class PartieTermineeException(Exception) :
	def __init__(self,message) :
		self.message=message

	def __str__(self) :
		return(self.message)

class PartiePerdueException(Exception) :
	def __init__(self,message) :
		self.message=message

	def __str__(self) :
		return(self.message)