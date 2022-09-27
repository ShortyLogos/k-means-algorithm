import re
from time import perf_counter
from enum import IntEnum
import numpy as np

class Methode(IntEnum):
    PRODUIT_SCALAIRE = 0
    LEAST_SQUARES = 1
    CITY_BLOCK = 2

class Prediction:
    def __init__(self, matrice_cooccurrences, mots_uniques, encodage):
        self.__matrice_cooccurrences = matrice_cooccurrences
        self.__mots_uniques = mots_uniques
        self.__encodage_stopwords = encodage
        self.__resultats_tries = None
        self.__stopwords = None
    
    @property
    def stopwords(self):
        return self.__stopwords
    
    @stopwords.setter
    def stopwords(self, chemin):
        try:
            fichier_stopwords = open(chemin, 'r', encoding = self.__encodage_stopwords)
            self.__stopwords = re.findall("\w+", fichier_stopwords.read().lower())
            fichier_stopwords.close()
        except:
            print("Le fichier stopwords.txt n'a pas été trouvé. Les résultats risquent d'être pollués.")

    @property
    def resultats_tries(self):
        return self.__resultats_tries  

    def predire(self, mot, nbr_reponses, methode_choisie, verbose):
        try:
            if mot is not None and int(nbr_reponses) > 0:
                print()
                self.__mot = mot
                self.__vecteur_mot = self.__matrice_cooccurrences[self.__mots_uniques[self.__mot]]
                self.__nbr_reponses = int(nbr_reponses)
                start_time_training = perf_counter()
                self._prediction_algorithme(methode_choisie)
                if verbose: print("Training Execution time: " + str(perf_counter()-start_time_training))
        except KeyError as exception:
            print(f"{exception} n'existe pas dans le texte.")
        except ValueError as exception:
            print(exception)
        except Exception as exception:
            print('Erreur imprévue. Veuillez réessayer.')

    def _prediction_algorithme(self, methode_choisie):
        match int(methode_choisie):
            case Methode.PRODUIT_SCALAIRE.value:
                fonction = self.__operation_scalaire
                maximiser = True
            case Methode.LEAST_SQUARES.value:
                fonction = self.__operation_moindre_carres
                maximiser = False
            case Methode.CITY_BLOCK.value:
                fonction = self.__operation_city_block
                maximiser = False
            case default:
                raise ValueError('Méthode de calcul invalide. Veuillez réessayer.')
        self.__resultats_tries = self.__prediction(fonction, maximiser)
        self.__imprimer_resultats()
        
    def __operation_scalaire(self, vecteur_compare):
        return np.dot(self.__vecteur_mot, vecteur_compare)
    
    def __operation_moindre_carres(self, vecteur_compare):
        return np.sum((self.__vecteur_mot-vecteur_compare)**2)
        
    def __operation_city_block(self, vecteur_compare):
        return np.sum(np.abs(self.__vecteur_mot-vecteur_compare))
    
    def __prediction(self, fonction, maximiser):
        liste_resultats = []
        for mot, index in self.__mots_uniques.items():
            if mot not in self.__stopwords and mot != self.__mot:
                score = fonction(self.__matrice_cooccurrences[index])
                liste_resultats.append((mot, score))
        return sorted(liste_resultats, key = lambda x:x[1], reverse = maximiser)
            
    def __imprimer_resultats(self):
        try:
            for mot, score in self.__resultats_tries[:self.__nbr_reponses]:
                print(f"{mot} --> {score}")
        except IndexError:
            print('\nMoins de résultats disponibles que demandés.')