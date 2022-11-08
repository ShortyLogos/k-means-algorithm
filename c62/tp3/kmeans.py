# matrice de centroïde : k * n, où k = nombre de centroïdes demandés et n = ensemble de tous les mots (nombre de dimensions)
# placer les centroïdes à des coordonnées identiques à des points sélectionnés au hasard à l'initialisation du clustering
# calcul de la distance d'un mot par rapport à un centroïde dans la boucle : utiliser least-squares
# trouver une façon pour que les points de données gardent en mémoire
# il faut penser à inclure les stopwords pour le tp3

from dao import Dao
import numpy as np
import random

# méthode qui sera utilisée par le main/argparse
def partionnement(bd: Dao, taille: int, k : int):
    donnees_uniques, liste_cooccurrences = bd.obtenir_donnees(taille)
    kmeans = KMeans(taille, k, liste_cooccurrences, donnees_uniques)
    kmeans.equilibrer()

class KMeans:
    def __init__(self, taille_fenetre : int, k : int, liste_cooccurrences: list, donnees_uniques: dict):
        self.__k = k
        self.__taille_fenetre = taille_fenetre
        self.__dimensions = len(donnees_uniques)
        self.__cooccurrences = self.__construire_matrice_cooccurrences(liste_cooccurrences)
        self.__centroides = self.__construire_matrice_centroides()
        self.__clusters = {} # [index_mot][index_centroide], va servir à vérifier à chaque itération si des mots on changé de cluster
        
    def __construire_matrice_cooccurrences(self, liste_cooccurrences) -> np.array:
        matrice = np.zeros((self.__dimensions, self.__dimensions))
        if len(liste_cooccurrences) > 0:
            for point1, point2, score in liste_cooccurrences:
                matrice[point1, point2] = score
        return matrice
    
    # on initialise les centroïdes à des coordoonées intelligentes 
    # on prend celles de points de données au hasard
    def __construire_matrice_centroides(self) -> np.array:
        matrice = np.zeros((self.__k, self.__dimensions))
        points_choisis = []
        
        for centroide in range(self.__k):
            while True:
                point = random.randrange(self.__dimensions)
                if point not in points_choisis:
                    points_choisis.append(point)
                    break
                
            matrice[centroide] = self.__cooccurrences[point]
        return matrice
    
    # méthode utiliser pour déterminer la distance d'un point de donnée par rapport à un centroide quelconque
    def __operation_moindre_carres(self, vecteur_point, vecteur_centroide: np.array) -> float:
        return np.sum((vecteur_point - vecteur_centroide)**2)
    
    # méthode qui s'occupera de trouver de manière itérative le point d'équilibre pour tous les centroïdes
    # lorsqu'aucun point de donnée n'a changé de cluster (le centroide), 
    # on considère que l'équilibre a été trouvé et on cesse l'exécution de l'algo
    def equilibrer(self) -> None:
        print(self.__centroides)
        for centroide in self.__centroides:
            print(np.sum(centroide))

def main():
    bd = Dao()
    bd.connecter()
    bd.afficher()
    partionnement(bd, 5, 10)
    bd.deconnecter()
    
    return 0

if __name__ == '__main__':
    quit(main())
    