# Projet-de-mise-en-pratique

Projet transversal des connaissances accumulées.

#Requirements :

Pour utiliser ce logiciel, il faut installer la librairie tkinter sur votre machine et avoir python3 installé.

Pour ce faire :
	-installer python3 : ```sudo apt-get install python3 ```
	-installer tkinter sur l'ordinateur : ```sudo apt install python3-tk```
	-installer tkinter dans python3 : ```pip3 install tk```

#Indications de fonctionnement :

Pour lancer le serveur : 
	-```python3 -m src.mains.mainServeur``` ou ```make launch_server```

Pour fermer le serveur :
	-```python3 -m src.fonctions.fermetureServeur``` ou ```make close_server```

Pour lancer l'interface utilisateur :
	-```python3 -m src.mains.mainDebut``` ou ```make launch_user_interface``` ou plus rapidement ```make```

Il est posssible de jouer hors ligne sans que le serveur soit lancé, pour le mode en ligne, veuillez lancer le serveur d'abord (dans un autre terminal).

#Règles du jeu :

Chaque joueur doit placer 5 bateaux sur son damier.

A tour de rôle, les joueurs choisissent une case où ils pensent que l'adversaire a caché un bateau. Quand un bateau a été touché sur toutes ses cellules, il est coulé. 
Le premier joueur à couler tous les bateaux adverses remporte la partie.
