import sys, os
import argparse
from typing import Optional, Sequence
from entrainement import Entrainement
from prediction import Prediction
from dao import Dao
from time import perf_counter


def entrainement(bd: Dao, chemin: str, encodage: str, taille: int, verbose: bool, **kwargs: Optional[Sequence[str]]) -> None:
	start_time_training = perf_counter()
	bd.creer_tables()
	entraineur = Entrainement(chemin, encodage, taille)
	entraineur.reconstruire(*bd.obtenir_donnees(taille))
	if verbose: print("Reconstruction Execution time: " + str(perf_counter()-start_time_training))
	entraineur.entrainer()
	if verbose: print("Training Execution time: " + str(perf_counter()-start_time_training))
	bd.inserer_vocabulaire(list(entraineur.mots_uniques.items()))
	if verbose: print("Insertion Vocabulaire Execution time: " + str(perf_counter()-start_time_training))
	bd.inserer_cooccurrences(entraineur.cooccurrences)
	if verbose: print("Insertion Cooccurrences Execution time: " + str(perf_counter()-start_time_training))

def recherche(bd: Dao, taille: int, verbose: bool, **kwargs: Optional[Sequence[str]]) -> None:
	mots_uniques, cooccurrences = bd.obtenir_donnees(taille)
	prompt_utilisateur = ("\n Entrez un mot, le nombre de synonymes que vous voulez"
								" et la méthode de calcul, i.e. produit scalaire: 0, least-squares: 1"
								", city-block: 2 \n\n Tapez q pour quitter.\n\n")
	predicteur = Prediction(cooccurrences, mots_uniques)
	predicteur.stopwords = os.path.join(sys.path[0], "stopwords.txt")
		
	entree_utilisateur = input(prompt_utilisateur)
	while entree_utilisateur != 'q':
		try:
			mot, nbr_reponses, methode_choisie = str.lower(entree_utilisateur).split()
			predicteur.predire(mot, int(nbr_reponses), int(methode_choisie), bool(verbose))
		except ValueError:
			print('Vous devez entrer 3 arguments. Veuillez réessayer.')
		entree_utilisateur = input(prompt_utilisateur)

def reinitialise(bd: Dao, **kwargs: Optional[Sequence[str]]) -> None:
	if (os.path.exists(bd.chemin_bd)):
		bd.detruire_tables()
		bd.deconnecter()
		try:
			os.remove(bd.chemin_bd)
			print("La base de données a été réinitialisé avec succès.")
		except:
			print("Erreur durant la suppression d'un fichier.")


def arg_positif(s: str) -> int:
	try:
		value = int(s)
	except ValueError:
		raise argparse.ArgumentTypeError(f'Vous devez entrer un nombre, vous avez entrez un {type(s).__name__!r}.')
	if value <= 0:
		raise argparse.ArgumentTypeError(f'Vous devez entrer un nombre positif et supérieur à 0 vous avez entrez {s!r}')
	else:
		return value


def gestion_arguments(argv: Optional[Sequence[str]] = None) -> dict:
	parser = argparse.ArgumentParser(prog='Synonyms Finder', description='Application pour offrir des synonymes à un mot donné.')
	actionChoice = parser.add_mutually_exclusive_group(required=True)
	actionChoice.add_argument('-e', dest='function', metavar='Action', help="Entrainer l'IA avec un nouveau texte", action='store_const', const=entrainement)
	actionChoice.add_argument('-r', dest='function', metavar='Action', help='Rechercher des synonymes', action='store_const', const=recherche)
	actionChoice.add_argument('-b', dest='function', metavar='Action', help='Régénérer la base de données', action='store_const', const=reinitialise)
	parser.add_argument('-v', dest='verbose', action='store_true', help='Démarrez le logiciel en mode verbose.  (défaut: %(default)s)', default=False)
	parser.add_argument('-t', dest='taille', help="Déterminez la grandeur de la fenêtre d'analyse.", type=arg_positif)
	parser.add_argument('--enc', dest='encodage', help="Déterminez le type d'encodage désiré.", type=str)
	parser.add_argument('--chemin', dest='chemin', help='Spécifiez le chemin complet vers le texte.', type=str)

	arguments = parser.parse_args(argv)
	
	if (arguments.function == entrainement or arguments.function == recherche) and not arguments.taille:
		parser.error(f'Vous devez spécifier une taille de fenêtre pour l\'action choisie.')
	elif arguments.function == entrainement and not arguments.encodage:
		parser.error(f'Vous devez spécifier un type d\'encodage pour effectuer un entrainement.')
	elif arguments.function == entrainement and not arguments.chemin:
		parser.error(f'Vous devez spécifier un chemin vers le fichier à apprendre.')
	
	return vars(arguments)


def main(argv: Optional[Sequence[str]] = None) -> int:
	arguments = gestion_arguments(argv)
	bd = Dao()
	bd.connecter()
	arguments['function'](bd, **arguments) 
	bd.deconnecter()
	return 0

if __name__ == '__main__':
	quit(main())