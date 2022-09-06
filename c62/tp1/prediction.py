import re
from time import perf_counter
from enum import Enum

class Methode(Enum):
    PRODUIT_SCALAIRE = 0
    LEAST_SQUARES = 1
    CITY_BLOCK = 2

class Prediction:
    def __init__(self, matrice_cooccurrences, mots_uniques):
        self.matrice_cooccurrences = matrice_cooccurrences
        self.mots_uniques = mots_uniques
        self.prompt_utilisateur = ("\n Entrez un mot, le nombre de synonymes que vous voulez"
                                      " et la méthode de calcul, i.e. produit scalaire: 0, least-squares: 1"
                                      ", city-block: 2 \n\n Tapez q pour quitter.\n\n")
        
    def predire(self):
        entree_utilisateur = input(self.prompt_utilisateur)
        while entree_utilisateur != 'q':
            try:
                mot, nbr_reponses, methode_choisie = str.lower(entree_utilisateur).split()
                if mot is not None and int(methode_choisie) < 3:
                    match methode_choisie:
                        case Methode.PRODUIT_SCALAIRE:
                            self.prediction_scalaire(mot, nbr_reponses)
                        case Methode.LEAST_SQUARES:
                            self.prediction_squares(mot, nbr_reponses)
                        case Methode.CITY_BLOCK:
                            self.prediction_block(mot, nbr_reponses)
            except:
                print(' Entrée invalide. Veuillez réessayer.')
            entree_utilisateur = input(self.prompt_utilisateur)
            
    def prediction_scalaire(self, mot, nbr_reponses):
        """
            Produit scalaire
            (a, b, c) ● (d, e, f) = ad + be + cf

            L’idée est que la multiplication des composantes et leur addition donnera une plus grande valeur si les composantes sont proches en valeur.
            On cherche à maximiser le score.

            Mot: (a, b)  --  Synonyme 1: (c, d)  --  Synonyme 2: (e, f)

            score(mot, synonyme1)vs score(mot synonyme2)

            (𝑎∗𝑐)+(𝑏∗𝑑)  𝑣𝑠 (𝑎∗𝑒)+(𝑏∗𝑓)
        """
        #exemple pour une colonne = self.matrice_cooccurrences[:,self.mots_uniques[mot]]
        #doit basically imprimer le top X (nbr_reponses) des synonymes du mot passé en params selon la méthode des Produit scalaire 
        pass
    
    def prediction_squares(self, mot, nbr_reponses):
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
        #exemple pour une colonne = self.matrice_cooccurrences[:,self.mots_uniques[mot]]
        #doit basically imprimer le top X (nbr_reponses) des synonymes du mot passé en params selon la méthode des Moindres-carrés
        pass
    
    def prediction_block(self, mot, nbr_reponses):
        """
            City-block (Manhattan distance)
            Considérons le mot pour lequel on cherche un synonyme comme une destination dans une ville disposée en grille (NYC).
            On veut trouver le vecteur qui est le moins distant du vecteur de notre mot (a, b) en voyageant un coin de rue à la fois.
            On cherche à minimiser le score.

            Mot: (a, b)  --  Synonyme 1: (c, d)  --  Synonyme 2: (e, f)

            score(mot, synonyme1)vs score(mot synonyme2)

            |𝑎−𝑐|+|𝑏−𝑑|  𝑣𝑠 |𝑎−𝑒|+|𝑏−𝑓|
        """
        #exemple pour une colonne = self.matrice_cooccurrences[:,self.mots_uniques[mot]]
        #doit basically imprimer le top X (nbr_reponses) des synonymes du mot passé en params selon la méthode City-block
        pass