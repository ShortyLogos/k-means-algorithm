import sys, os
import entrainement as ent
import prediction as pred
import argparse
from typing import Optional
from typing import Sequence


def entrainement(args: argparse.Namespace) -> None:
    entraineur = ent.Entrainement(args.chemin, args.encodage, args.taille)
    entraineur.entrainer(args.verbose)
    #Ajouter les résultats à la base de données


def recherche(args: argparse.Namespace) -> None:
    encodage = args.encodage or 'utf-8' #Pas sur si devrais être spécifié en argument et oublié dans énoncé ou loader de la db...
    cooccurrences, mots_uniques = None #or load from database 
    prompt_utilisateur = ("\n Entrez un mot, le nombre de synonymes que vous voulez"
                                " et la méthode de calcul, i.e. produit scalaire: 0, least-squares: 1"
                                ", city-block: 2 \n\n Tapez q pour quitter.\n\n")
    
    predicteur = pred.Prediction(cooccurrences, mots_uniques, encodage)
    predicteur.stopwords = os.path.join(sys.path[0], "stopwords.txt")
        
    entree_utilisateur = input(prompt_utilisateur)
    while entree_utilisateur != 'q':
        try:
            mot, nbr_reponses, methode_choisie = str.lower(entree_utilisateur).split()
            predicteur.predire(mot, nbr_reponses, methode_choisie, args.verbose)
        except ValueError:
            print('Vous devez entrer 3 arguments. Veuillez réessayer.')
        entree_utilisateur = input(prompt_utilisateur)


def reinitialise(args: argparse.Namespace) -> None:
    print('Reinitialisé')


def arg_positif(s: str) -> int:
    try:
        value = int(s)
    except ValueError:
        raise argparse.ArgumentTypeError(f'Vous devez entrer un nombre, vous avez entrez un {type(s).__name__!r}.')
    if value <= 0:
        raise argparse.ArgumentTypeError(f'Vous devez entrer un nombre positif et supérieur à 0 vous avez entrez {s!r}')
    else:
        return value


def gestion_arguments(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
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
    
    return arguments


def main(argv: Optional[Sequence[str]] = None) -> int:
    arguments = gestion_arguments(argv)
    arguments.function(arguments)
    
if __name__ == '__main__':
	quit(main())