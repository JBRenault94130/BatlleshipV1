
#!/usr/local/bin/python3.8
# -*-coding:Utf-8 -*
class NoMovementException(Exception) :
	def __init__(self,message) :
		#print(message)
		self.message=message

	def __str__(self) :
		return(self.message)

class NoWeaponError(Exception) :
	def __init__(self,message) :
		#print(message)
		self.message=message

	def __str__(self) :
		return(self.message)

class PositionError(Exception) :
	def __init__(self,message) :
		#print(message)
		self.message=message

	def __str__(self) :
		return(self.message)

class MauvaisPlacementError(Exception) :
	def __init__(self,message) :
		#print(message)
		self.message=message

	def __str__(self) :
		return(self.message)

class ToucheCouleException(Exception) :
	def __init__(self,message) :
		#print(message)
		self.message=message

	def __str__(self) :
		return(self.message)

class FinDuJeuException(Exception) :
	def __init__(self,message) :
		#print(message)
		self.message=message

	def __str__(self) :
		return(self.message)

class NoHarmException(Exception) :
	def __init__(self,message) :
		#print(message)
		self.message=message

	def __str__(self) :
		return(self.message)

class ToucheException(Exception) :
	def __init__(self,message) :
		#print(message)
		self.message=message

	def __str__(self) :
		return(self.message)