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
        self.__clusters_precedents = np.zeros(self.__dimensions)
        self.__clusters_nouveaux = np.zeros(self.__dimensions)
        self.__nb_changements = 0
        self.__nb_generations = 0
        self.__equilibre = False
        
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
    
    # les nouvelles coordonnées d'un centroide sont déterminées en faisant la moyenne des points appartenant à son cluster
    def __determiner_centroides(self):
        for i, point in enumerate(self.__cooccurrences):
            distances = []
            for centroide in self.__centroides:
                distances.append(self.__operation_moindre_carres(point, centroide))
                self.__clusters_nouveaux[i] = distances.index(min((distances)))
                
    def __verifier_equilibre(self):
        if self.__nb_generations != 0:
            changements = np.not_equal(self.__clusters_nouveaux, self.__clusters_precedents)
            self.__nb_changements = sum(changements.astype(int))
            print("nombre de changements:", self.__nb_changements)
            self.__clusters_precedents = np.copy(self.__clusters_nouveaux)
            if self.__nb_changements == 0:
                self.__equilibre = True
    
    # les nouvelles coordonnées d'un centroide sont déterminées en faisant la moyenne des points appartenant à son cluster
    def __nouvelles_coordonnees(self):
        for index_centroide, _ in enumerate(self.__centroides):
            points = np.where(self.__clusters_nouveaux == index_centroide)[0]
            self.__centroides[index_centroide] = np.mean([self.__cooccurrences[index_point] for index_point in points], axis=0)
            print("coord. du centroide ", index_centroide, " : ", self.__centroides[index_centroide])
    
    # méthode qui s'occupera de trouver de manière itérative le point d'équilibre pour tous les centroïdes
    # lorsqu'aucun point de donnée n'a changé de cluster (le centroide), 
    # on considère que l'équilibre a été trouvé et on cesse l'exécution de l'algo
    def equilibrer(self) -> None:
        while self.__equilibre is False:
            self.__determiner_centroides()
            self.__nouvelles_coordonnees()
            self.__verifier_equilibre()
            if not self.__equilibre:
                self.__nb_generations += 1
        print("\nFIN DE L'ALGORITHME KMEANS")

def main():
    bd = Dao()
    bd.connecter()
    bd.afficher()
    partionnement(bd, 5, 5)
    bd.deconnecter()

    return 0

if __name__ == '__main__':
    quit(main())
    