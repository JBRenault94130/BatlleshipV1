all : launch_user_interface

launch_user_interface : 
	python3 -m src.mains.mainDebut

close_server :
	python3 -m src.fonctions.fermetureServeur

launch_server :
	python3 -m src.mains.mainServeur