#!/usr/local/bin/python3.8
# -*-coding:Utf-8 -*
class CommunicationError(Exception) :
	def __init__(self,message) :
		#print(message)
		self.message=message

	def __str__(self) :
		return(self.message)