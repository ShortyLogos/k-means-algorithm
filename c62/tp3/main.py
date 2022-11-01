import sys, os
from typing import Optional, Sequence
from entrainement import Entrainement
from prediction import Prediction
from options import gestion_arguments
from dao import Dao

prompt_utilisateur = ("\n Entrez un mot, le nombre de synonymes que vous voulez"
							" et la méthode de calcul, i.e. produit scalaire: 0, least-squares: 1"
							", city-block: 2 \n\n Tapez q pour quitter.\n\n")

def entrainement(bd: Dao, chemin: str, encodage: str, taille: int, verbose: bool, **kwargs: Optional[Sequence[str]]) -> None:
	entraineur = Entrainement(chemin, encodage, taille, verbose)
	entraineur.reconstruire(*bd.obtenir_donnees(taille))
	entraineur.entrainer()
	bd.inserer_vocabulaire(list(entraineur.mots_uniques.items()))
	bd.inserer_cooccurrences(entraineur.cooccurrences)

def recherche(bd: Dao, taille: int, stopwords: str, verbose: bool, **kwargs: Optional[Sequence[str]]) -> None:
	mots_uniques, cooccurrences = bd.obtenir_donnees(taille)
	predicteur = Prediction(cooccurrences, mots_uniques, verbose)
	predicteur.stopwords = os.path.join(sys.path[0], stopwords)
	entree_utilisateur = input(prompt_utilisateur)
	while entree_utilisateur.lower() != 'q':
		try:
			mot, nbr_reponses, methode_choisie = str.lower(entree_utilisateur).split()
			predicteur.predire(mot, int(nbr_reponses), int(methode_choisie))
		except ValueError:
			print('Vous devez entrer 3 arguments. Veuillez réessayer.')
		entree_utilisateur = input(prompt_utilisateur)

def reinitialise(bd: Dao, **kwargs: Optional[Sequence[str]]) -> None:
	if (os.path.exists(bd.chemin_bd)):
		bd.detruire_tables()
	bd.creer_tables()
	print("La base de données a été réinitialisée avec succès.")

def main(argv: Optional[Sequence[str]] = None) -> int:
	arguments = gestion_arguments(entrainement, recherche, reinitialise, argv)
	with Dao(arguments["verbose"]) as bd:
		arguments['function'](bd, **arguments)
	return 0

if __name__ == '__main__':
	quit(main())