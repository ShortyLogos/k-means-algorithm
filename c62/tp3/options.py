import argparse
from typing import Optional, Sequence, Callable

def arg_positif(value: str) -> int:
	try:
		value = int(value)
	except ValueError:
		raise argparse.ArgumentTypeError(f'Vous devez entrer un nombre, vous avez entrez un {type(value).__name__!r}.')
	if value <= 0:
		raise argparse.ArgumentTypeError(f'Vous devez entrer un nombre positif et supérieur à 0 vous avez entré {value!r}')
	else:
		return value

def gestion_arguments(entrainement: Callable, recherche: Callable, reinitialise: Callable, partionnement: Callable, argv: Optional[Sequence[str]] = None) -> dict:
	parser = argparse.ArgumentParser(prog='Synonyms Finder', description='Application qui offre des synonymes pour un mot donné.')
	actionChoice = parser.add_mutually_exclusive_group(required=True)
	actionChoice.add_argument('-e', dest='function', metavar='Action', help="Entrainer l'IA avec un nouveau texte", action='store_const', const=entrainement)
	actionChoice.add_argument('-r', dest='function', metavar='Action', help='Rechercher des synonymes', action='store_const', const=recherche)
	actionChoice.add_argument('-b', dest='function', metavar='Action', help='Régénérer la base de données', action='store_const', const=reinitialise)
	actionChoice.add_argument('-c', dest='function', metavar='Action', help='Clustering à partir de mégadonnées', action='store_const', const=partionnement)
	parser.add_argument('-t', dest='taille', help="Déterminer la grandeur de la fenêtre d'analyse.", type=arg_positif)
	parser.add_argument('-s', dest='stopwords', help='Spécifier le chemin vers le fichier stopwords. (défaut: %(default)s)', default="stopwords.txt", type=str)
	parser.add_argument('--enc', dest='encodage', help="Déterminer le type d'encodage désiré.", type=str)
	parser.add_argument('--chemin', dest='chemin', help='Spécifier le chemin complet vers le texte.', type=str)
	parser.add_argument('-k', dest='k', help='Déterminer le nombre de partitions.', type=arg_positif)
	parser.add_argument('-n', dest='nb_resultats', help='Déterminer le nombre de résultats à afficher par partition.', type=arg_positif)
	parser.add_argument('--bd', dest='bd_name', help='Spécifier le nom de la base de donnée à utiliser. (défaut: %(default)s)', type=str, default= 'mainBD')
	parser.add_argument('-v', dest='verbose', action='store_true', help='Démarrer le logiciel en mode verbose.  (défaut: %(default)s)', default=False)

	arguments = parser.parse_args(argv)
	
	if (arguments.function == entrainement or arguments.function == recherche or arguments.function == partionnement) and not arguments.taille:
		parser.error(f'Vous devez spécifier une taille de fenêtre pour l\'action choisie.')
	elif arguments.function == entrainement and not arguments.encodage:
		parser.error(f'Vous devez spécifier un type d\'encodage pour effectuer un entrainement.')
	elif arguments.function == entrainement and not arguments.chemin:
		parser.error(f'Vous devez spécifier un chemin vers le texte d\'entrainement.')
	elif arguments.function == partionnement and not arguments.k:
		parser.error(f'Vous devez spécifier un nombre de partitions désiré.')
	elif arguments.function == partionnement and not arguments.nb_resultats:
		parser.error(f'Vous devez spécifier un nombre de résultats à afficher par partition.')
	
	return vars(arguments)