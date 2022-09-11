import re
from time import perf_counter
from enum import IntEnum
import numpy as np
import sys, os

class Methode(IntEnum):
    PRODUIT_SCALAIRE = 0
    LEAST_SQUARES = 1
    CITY_BLOCK = 2

class Prediction:
    def __init__(self, matrice_cooccurrences, mots_uniques, encodage):
        self.__matrice_cooccurrences = matrice_cooccurrences
        self.__mots_uniques = mots_uniques
        self.__liste_cles = list(mots_uniques)
        self.__encodage_stopwords = encodage
        self.__prompt_utilisateur = ("\n Entrez un mot, le nombre de synonymes que vous voulez"
                                      " et la méthode de calcul, i.e. produit scalaire: 0, least-squares: 1"
                                      ", city-block: 2 \n\n Tapez q pour quitter.\n\n")
    
    def generer_stopwords(self, chemin = os.path.join(sys.path[0], "stopwords.txt")):
        try:
            fichier_stopwords = open(chemin, 'r', encoding = self.__encodage_stopwords)
            self.__stopwords = re.findall("\w+", fichier_stopwords.read().lower())
            fichier_stopwords.close()
        except:
            print("Le fichier stopwords.txt n'a pas été trouvé. Les résultats risquent d'être pollués.")

    def predire(self):
        entree_utilisateur = input(self.__prompt_utilisateur)
        while entree_utilisateur != 'q':
            try:
                mot, nbr_reponses, methode_choisie = str.lower(entree_utilisateur).split()
                if mot is not None and int(nbr_reponses) > 0:
                    print()
                    self.__mot = mot
                    self.__vecteur_mot = self.__matrice_cooccurrences[self.__mots_uniques[self.__mot]]
                    self.__nbr_reponses = int(nbr_reponses)
                    start_time_training = perf_counter()
                    match int(methode_choisie):
                        case Methode.PRODUIT_SCALAIRE.value:
                            self._prediction_scalaire()
                        case Methode.LEAST_SQUARES.value:
                            self._prediction_squares()
                        case Methode.CITY_BLOCK.value:
                            self._prediction_block()
                        case default:
                            raise ValueError('Méthode de calcul invalide.')
                    print("Training Execution time: " + str(perf_counter()-start_time_training))
            except KeyError as exception:
                print(f"{exception} n'existe pas dans le texte.")
            except ValueError as exception:
                print(f'{exception}. Veuillez réessayer.')
            entree_utilisateur = input(self.__prompt_utilisateur)

    def operation_scalaire(self, vecteur_compare, index):
        score = np.dot(self.__vecteur_mot, vecteur_compare)
        return score, index

        # ref : https://fr.acervolima.com/comment-calculer-le-produit-scalaire-de-deux-vecteurs-en-python/ (la méthode np.dot())

    def _prediction_scalaire(self):
        resultats_brutes = np.array([self.operation_scalaire(v, i) for i, v in enumerate(self.__matrice_cooccurrences)]) # on effectue le produit scalaire sur chacun des vecteurs
        resultats_tries = sorted(resultats_brutes, key = lambda x:x[0], reverse = True) # cette méthode effectue un tri mais détruit la nature numpy de la matrice

        nb_resultats = 0
        resultats_ignores = 0
        while nb_resultats < self.__nbr_reponses:
            resultat = nb_resultats + resultats_ignores
            try:
                mot = self.__liste_cles[int(resultats_tries[resultat][1])] # pour utiliser l'index, on doit le convertir en int car un float depuis numpy
                if mot not in self.__stopwords and mot != self.__mot: # on exclut les stopwords et le mot principal des résultats
                    print(f"{mot} --> {resultats_tries[resultat][0]}")
                    nb_resultats += 1
                else:
                    resultats_ignores += 1
            except IndexError as exception:
                print('\nMoins de résultats disponibles que demandés.')
                break

        # ref : https://stackoverflow.com/questions/42541303/numpy-apply-along-axis-and-get-row-index
        # ref https://www.adamsmith.haus/python/answers/how-to-access-a-dictionary-key-by-index-in-python

    def _prediction_squares(self):
        """ 
            Moindres-carrés (least-squares)
            Considérons le mot pour lequel on cherche un synonyme comme une moyenne.
            On veut choisir ceux qui sont le plus proche de la moyenne en calculant la somme de leurs différences avec cette moyenne, au carré.
            Un peu à la même manière que le calcul pour l’écart-type.
            On cherche donc à minimiser le score.

            Mot: (a, b)  --  Synonyme 1: (c, d)  --  Synonyme 2: (e, f)

            score(mot, synonyme1)vs score(mot synonyme2)

            (𝑎−𝑐)^2+〖(𝑏−𝑑)〗^2  𝑣𝑠 (𝑎−𝑒)^2+〖(𝑏 −𝑓)〗^2
        """
        pass
    
    def _prediction_block(self):
        """
            City-block (Manhattan distance)
            Considérons le mot pour lequel on cherche un synonyme comme une destination dans une ville disposée en grille (NYC).
            On veut trouver le vecteur qui est le moins distant du vecteur de notre mot (a, b) en voyageant un coin de rue à la fois.
            On cherche à minimiser le score.

            Mot: (a, b)  --  Synonyme 1: (c, d)  --  Synonyme 2: (e, f)

            score(mot, synonyme1)vs score(mot synonyme2)

            |𝑎−𝑐|+|𝑏−𝑑|  𝑣𝑠 |𝑎−𝑒|+|𝑏−𝑓|
        """
        pass