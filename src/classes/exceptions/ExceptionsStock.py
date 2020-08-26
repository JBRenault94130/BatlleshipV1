#!/usr/local/bin/python3.8
# -*-coding:Utf-8 -*
class LoginExistantException(Exception) :
	def __init__(self,message) :
		self.message=message

	def __str__(self) :
		return(self.message)

class PseudoExistantException(Exception) :
	def __init__(self,message) :
		self.message=message

	def __str__(self) :
		return(self.message)

class NoPlayerFoundException(Exception) :
	def __init__(self,message) :
		self.message=message

	def __str__(self) :
		return(self.message)

class HashException(Exception) :
	def __init__(self,message) :
		self.message=message

	def __str__(self) :
		return(self.message)

class NoActualException(Exception) :
	def __init__(self,message) :
		self.message=message

	def __str__(self) :
		return(self.message)