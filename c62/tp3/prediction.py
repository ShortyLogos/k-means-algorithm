import re
from time import perf_counter
from enum import IntEnum
from typing import Callable
import numpy as np

Score = int

class Methode(IntEnum):
    PRODUIT_SCALAIRE = 0
    LEAST_SQUARES = 1
    CITY_BLOCK = 2

class Prediction:
    def __init__(self, liste_cooccurrences: list, mots_uniques: dict, verbose: bool = False) -> None:
        self.__mots_uniques = mots_uniques
        self.__matrice_cooccurrences = self.__construire_matrice(liste_cooccurrences)
        self.__resultats_tries = None
        self.__stopwords = None
        self.__verbose = verbose
    
    @property
    def stopwords(self) -> list:
        return self.__stopwords
    
    @stopwords.setter
    def stopwords(self, chemin: str) -> None:
        try:
            fichier_stopwords = open(chemin, 'r', encoding = 'utf-8')
            self.__stopwords = re.findall("\w+", fichier_stopwords.read().lower())
        except:
            print("Le fichier stopwords.txt n'a pas été trouvé. Les résultats risquent d'être pollués.")
        finally:
            fichier_stopwords.close()

    @property
    def resultats_tries(self) -> list:
        return self.__resultats_tries  

    def predire(self, mot: str, nbr_reponses: int, methode_choisie: int) -> None:
        try:
            if mot is not None and nbr_reponses > 0:
                self.__mot = mot
                self.__vecteur_mot = self.__matrice_cooccurrences[self.__mots_uniques[self.__mot]]
                self.__nbr_reponses = nbr_reponses
                start_time_training = perf_counter()
                self._prediction_algorithme(methode_choisie)
                if self.__verbose: print("Training Execution time: " + str(perf_counter()-start_time_training) + ('\n'*2))
        except KeyError as exception:
            print(f"{exception} n'existe pas dans nos données.")
        except ValueError as exception:
            print(exception)
        except Exception as exception:
            if self.__verbose:
                print(exception)
            print('Erreur imprévue. Veuillez réessayer.')

    def __construire_matrice(self, liste_cooccurrences: list) -> np.array:
        matrice = np.zeros((len(self.__mots_uniques), len(self.__mots_uniques)))
        if len(liste_cooccurrences) > 0:
            for mot1, mot2, score in liste_cooccurrences:
                matrice[mot1][mot2] = score
        return matrice
        
    def _prediction_algorithme(self, methode_choisie: int) -> None:
        match methode_choisie:
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
        
    def __operation_scalaire(self, vecteur_compare: np.array) -> Score:
        return np.dot(self.__vecteur_mot, vecteur_compare)
    
    def __operation_moindre_carres(self, vecteur_compare: np.array) -> Score:
        return np.sum((self.__vecteur_mot - vecteur_compare)**2)
        
    def __operation_city_block(self, vecteur_compare: np.array) -> Score:
        return np.sum(np.abs(self.__vecteur_mot - vecteur_compare))
    
    def __prediction(self, fonction: Callable, maximiser: bool) -> list:
        liste_resultats = []
        for mot, index in self.__mots_uniques.items():
            if mot not in self.__stopwords and mot != self.__mot:
                score = fonction(self.__matrice_cooccurrences[index])
                liste_resultats.append((mot, score))
        return sorted(liste_resultats, key = lambda x:x[1], reverse = maximiser)
            
    def __imprimer_resultats(self) -> None:
        try:
            print('\n')
            for mot, score in self.__resultats_tries[:self.__nbr_reponses]:
                print(f"{mot} --> {score}")
            print('\n')
        except IndexError:
            print('\nMoins de résultats disponibles que demandés.')