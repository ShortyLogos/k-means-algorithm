import re
from time import perf_counter
from enum import IntEnum
import numpy as np

class Methode(IntEnum):
    PRODUIT_SCALAIRE = 0
    LEAST_SQUARES = 1
    CITY_BLOCK = 2

class Prediction:
    def __init__(self, matrice_cooccurrences, mots_uniques):
        self.__matrice_cooccurrences = matrice_cooccurrences
        self.__mots_uniques = mots_uniques
        self.__prompt_utilisateur = ("\n Entrez un mot, le nombre de synonymes que vous voulez"
                                      " et la méthode de calcul, i.e. produit scalaire: 0, least-squares: 1"
                                      ", city-block: 2 \n\n Tapez q pour quitter.\n\n")
        
    def predire(self):
        entree_utilisateur = input(self.__prompt_utilisateur)
        while entree_utilisateur != 'q':
            try:
                mot, nbr_reponses, methode_choisie = str.lower(entree_utilisateur).split()
                if mot is not None and int(nbr_reponses) > 0:
                    self.__mot = mot
                    self.__nbr_reponses = int(nbr_reponses)
                    match int(methode_choisie):
                        case Methode.PRODUIT_SCALAIRE.value:
                            self._prediction_scalaire()
                        case Methode.LEAST_SQUARES.value:
                            self._prediction_block()
                        case Methode.CITY_BLOCK.value:
                            self._prediction_block()
                        case default:
                            raise ValueError('Méthode de calcul invalide')
            except ValueError as e:
                print(f'{e}. Veuillez réessayer.')
            entree_utilisateur = input(self.__prompt_utilisateur)
            
    def _prediction_scalaire(self):
        #doit basically imprimer le top X (nbr_reponses) des synonymes du mot passé en params selon la méthode des Produit scalaire
        """
            Produit scalaire
            (a, b, c) ● (d, e, f) = ad + be + cf

            L’idée est que la multiplication des composantes et leur addition donnera une plus grande valeur si les composantes sont proches en valeur.
            On cherche à maximiser le score.

            Mot: (a, b)  --  Synonyme 1: (c, d)  --  Synonyme 2: (e, f)

            score(mot, synonyme1)vs score(mot synonyme2)

            (𝑎∗𝑐)+(𝑏∗𝑑)  𝑣𝑠 (𝑎∗𝑒)+(𝑏∗𝑓)
        """
        #La ligne suivante sert à appliquer une fonction à chaque ligne
        matrice = np.apply_along_axis(self.test_scalaire, axis=1, arr=self.__matrice_cooccurrences)
        #Les deux lignes suivantes prennent la matrice et la met en ordre croissant si on veut faire ça...
        sorted_index_array = np.argsort(matrice)
        sorted_array = matrice[sorted_index_array]
        # Cette ligne garde les X plus haut nombres mais il nous manque à connaitre ces résultats correspondent à quel mots..
        rslt = sorted_array[-self.__nbr_reponses : ]

    def test_scalaire(self, x):
        #retourne pour une ligne x passé en parametre, le scalaire entre la ligne x et notre mot choisie avec la fonction dot de numpy
        return self.__matrice_cooccurrences[self.__mots_uniques[self.__mot], :].dot(x)       

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