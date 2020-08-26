#!/usr/local/bin/python3.8
# -*-coding:Utf-8 -*

import socket
import select
from src.classes.Joueur import *
from src.classes.StructureJoueurs import *
from src.classes.Partie import *

def initialiserServeur() :
	serveur = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	serveur.bind(('',12800))
	serveur.listen(10)
	return(serveur)

def lecture(serveur) :
	liste_connexions = []
	liste_attente = []
	liste_enJeu = []
	liste_joueurs_connectes = []
	liste_parties = []
	liste_abandon = []
	damiers_en_stock = []
	tst = True
	try :
		while(tst) :
			connexions, wlist, xlist = select.select([serveur],(),(),0.05)

			for con in connexions :
				clients, infos = con.accept()

				liste_connexions.append(clients)

			aLire = []
			try :
				aLire, wlist, xlist = select.select(liste_connexions,(),(),0.05)
			except select.error :
				pass
			else :
				for el in aLire :
					msg = el.recv(1024)
					msg = msg.decode()
					_temp = False
					if(msg.lower() == "renvoi joueur") :
						joueur = pickle.loads(el.recv(1024))
						structure = StructureJoueurs()
						structure.importStructure()
						cle=""
						for clef in structure.dicoJoueurs.keys() :
							if(structure.dicoJoueurs[clef].pseudo==joueur.pseudo) :
								cle=clef
						structure.dicoJoueurs[cle] = joueur
						structure.editStructure()
					if(msg.lower() == "fin partie") :
						joueur = pickle.loads(el.recv(1024))
						structure = StructureJoueurs()
						structure.importStructure()
						cle=""
						for clef in structure.dicoJoueurs.keys() :
							if(structure.dicoJoueurs[clef].pseudo==joueur.pseudo) :
								cle=clef
						structure.dicoJoueurs[cle] = joueur
						structure.editStructure()
						for el1,el2,partie in liste_parties :
							if(el is el1) :
								liste_parties.remove((el1,el2,partie))
							if(el is el2) :
								liste_parties.remove((el1,el2,partie))

						for el1,el2 in liste_enJeu :
							if((el is el1) or (el is el2)) :
								liste_enJeu.remove((el1,el2))
					if(msg.lower() == "a joue") :
						partie = pickle.loads(el.recv(9999))
						tstFini = partie.testFin()
						for el1, el2 in liste_enJeu :
							if(el is el1) :
								if(tstFini) :
									el2.send(b"perdu")
								else :
									el2.send(b"a toi")
									time.sleep(0.1)
									el2.send(pickle.dumps(partie))
							elif(el is el2) :
								if(tstFini) :
									el1.send(b"perdu")
								else :
									el1.send(b"a toi")
									time.sleep(0.1)
									el1.send(pickle.dumps(partie))
					if(msg.lower() == "envoi damier") :
						damier = pickle.loads(el.recv(1024))
						joueur = pickle.loads(el.recv(1024))
						el.send(b"OK")
						damiers_en_stock.append((el,damier,joueur))
					if(msg.lower() == "abandon") :
						for el1,el2 in liste_enJeu :
							if(el is el1) :
								liste_abandon.append(el2)
							elif(el is el2) :
								liste_abandon.append(el1)
					if(msg.lower() == "attente damier") :
						adversaire = None
						for el1,el2 in liste_enJeu :
							if(el is el1) :
								adversaire = el2
							elif(el is el2) :
								adversaire = el1
						tstDamier = False
						damier1 = None
						damier2 = None
						joueur1 = None
						joueur2 = None
						for el1 in liste_abandon :
							if(el is el1) :
								el.send(b"partie interrompue")
								liste_abandon.remove(el)
						for co,damier,joueur in damiers_en_stock :
							if(co is adversaire) :
								tstDamier = True
								damier2 = damier
								joueur2 = joueur
							elif(co is el) :
								damier1 = damier
								joueur1 = joueur
						if(tstDamier) :
							el.send(b"partie")
							time.sleep(0.1)
							damiers_en_stock.remove((el,damier1,joueur1))
							damiers_en_stock.remove((adversaire,damier2,joueur2))
							partie = Partie(joueur1,damier1,joueur2,damier2)
							el.send(pickle.dumps(partie))
							liste_parties.append((el,adversaire,partie))
						else :
							tstBoucle = False
							for co1,co2,part in liste_parties :
								if((el is co1) or (el is co2)) :
									el.send(b"partie")
									time.sleep(0.1)
									el.send(pickle.dumps(part))
									tstBoucle = True
							if(not tstBoucle) :
								el.send(b"attente")

					if(msg.lower() == "arret attente") :
						for elem in liste_attente :
							if(elem is el) :
								_temp =True
						if(_temp) :
							liste_attente.remove(el)
							cpt=0
						for el1,el2 in liste_enJeu :
							if(el is el1 or el is el2) :
								liste_enJeu.remove((el1,el2))
					else :
						pass
					if(msg.lower() == "cherche") :							
						liste_attente.append(el)
						el.send(b"pas encore")
					if(msg.lower() == "attente") :
						tst1=False
						for el1,el2 in liste_enJeu :
							if((el is el1) or (el is el2)) :
								el.send(b"trouve")
								tst1=True
						if(tst1) :
							pass
						else :
							if(len(liste_attente)>1) :
								if(el is liste_attente[0]) :
									liste_enJeu.append((el,liste_attente[1]))
									liste_attente.remove(liste_attente[1])
									liste_attente.remove(el)
								else :
									liste_enJeu.append((el,liste_attente[0]))
									liste_attente.remove(liste_attente[0])
									liste_attente.remove(el)
								el.send(b"trouve")
							else :
								el.send(b"pas encore")						

					if(msg.lower() == "actualiser profil") :
						structure = StructureJoueurs()
						try :
							structure.importStructure()
						except :
							structure = StructureJoueurs()
						login = el.recv(1024).decode()
						mdp = el.recv(1024).decode()
						joueurActuel = el.recv(1024)
						joueurActuel = pickle.loads(joueurActuel)
						try :
							structure.actualiserJoueur(joueurActuel,login,mdp)
						except NoPlayerFoundException :
							el.send(b"False")
						except NoActualException :
							el.send(b"False")
						else :
							el.send(b"Done")
					if(msg.lower() == "arret jeu") :
						_temp1 = None
						_temp2 = None
						_temp3 = None
						tstIn = False
						for el1,damier,adv in damiers_en_stock :
							if(el is el1) :
								_temp1 = el1
								_temp2 = damier
								_temp3 = adv
								tstDIn = True
						if(tstIn) :
							damiers_en_stock.remove((_temp1,_temp2,_temp3))
						tstIn = False
						for el1,el2,partie in liste_parties :
							if(el is el1) :
								_temp1 = el1
								_temp2 = el2
								_temp3 = partie
								try :
									el2.send(b"partie interrompue")
								except OSError :
									pass
								tstIn = True
							elif(el is el2) :
								_temp1 = el1
								_temp2 = el2
								_temp3 = partie
								try :
									el1.send(b"partie interrompue")
								except OSError :
									pass
								tstIn = True
						if(tstIn) :
							liste_parties.remove((_temp1,_temp2,_temp3))
						tstIn = False
						for el1,el2 in liste_enJeu :
							if(el is el1 or el is el2) :
								_temp1 = el1
								_temp2 = el2
								tstIn = True
						if(tstIn) :
							liste_enJeu.remove((_temp1,_temp2))
					if(msg.lower() == "tentative connexion") :
						structure = StructureJoueurs()
						try :
							structure.importStructure()
						except :
							structure = StructureJoueurs()
						login = el.recv(1024).decode()
						mdp = el.recv(1024).decode()
						joueur = None
						try :
							joueur = structure.getJoueur(login,mdp)
						except NoPlayerFoundException :
							el.send(b"False")
						else :
							if(joueur.pseudo in liste_joueurs_connectes) :
								el.send(b"deja connecte")
							else :
								liste_joueurs_connectes.append(joueur.pseudo)
								joueur = pickle.dumps(joueur)
								el.send(joueur)
					elif(msg.lower()=="tentative inscription") :
						structure = StructureJoueurs()
						structure.importStructure()
						login = el.recv(1024).decode()
						mdp = el.recv(1024).decode()
						pseudo = el.recv(1024).decode()
						try :
							structure.ajouterJoueur(Joueur(pseudo),login,mdp)
						except LoginExistantException :
							el.send(b"False login")
						except PseudoExistantException :
							el.send(b"False pseudo")
						except HashException :
							el.send(b"False encodage")
						else :
							structure.editStructure()
							el.send(b"Done")

					elif(msg.lower()=="joueur deconnecte") :
						joueur = pickle.loads(el.recv(1024))
						cle=""
						structure = StructureJoueurs()
						structure.importStructure()
						for clef in structure.dicoJoueurs.keys() :
							if(structure.dicoJoueurs[clef].pseudo==joueur.pseudo) :
								cle = clef
						structure.dicoJoueurs[cle]=joueur
						structure.editStructure()
						liste_joueurs_connectes.remove(joueur.pseudo)

					elif(msg.lower()=="fin exit(0)") :
						for elem in liste_abandon :
							if(elem is el) :
								liste_abandon.remove(el)
						el.close()
						liste_connexions.remove(el)
					elif(msg.lower()=="fermeture reseau principal") :
						for el in liste_connexions :
							try :
								el.send(b"coupure reseau")
							except BrokenPipeError :
								pass
							el.close()
							serveur.close()
							tst=False


	except KeyboardInterrupt :
		for el in liste_connexions :
			el.send(b"fin exit(0)")
			el.close()
		serveur.close()
		print("WTF?")
		raise KeyboardInterrupt
