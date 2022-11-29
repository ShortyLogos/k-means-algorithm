# matrice de centroïde : k * n, où k = nombre de centroïdes demandés et n = ensemble de tous les mots (nombre de dimensions)
# placer les centroïdes à des coordonnées identiques à des points sélectionnés au hasard à l'initialisation du clustering
# calcul de la distance d'un mot par rapport à un centroïde dans la boucle : utiliser least-squares
# trouver une façon pour que les points de données gardent en mémoire
# il faut penser à inclure les stopwords pour le tp3

from dao import Dao
from time import perf_counter
import numpy as np
import random

# méthode qui sera utilisée par le main/argparse
def partionnement(bd: Dao, taille: int, k: int, nb_resultats: int):
    donnees_uniques, liste_cooccurrences = bd.obtenir_donnees(taille)
    kmeans = KMeans(k, liste_cooccurrences, donnees_uniques, nb_resultats)
    kmeans.equilibrer()

class KMeans:
    def __init__(self, k: int, liste_cooccurrences: list, donnees_uniques: dict, nb_resultats: int):
        self.__temps_completion = perf_counter()
        self.__k = k
        self.__dimensions = len(donnees_uniques)
        self.__donnees_uniques = list(donnees_uniques.keys())
        self.__cooccurrences = self.__construire_matrice_cooccurrences(liste_cooccurrences)
        self.__centroides = self.__construire_matrice_centroides()
        self.__clusters_precedents = np.arange(self.__dimensions)
        self.__clusters_nouveaux = np.arange(self.__dimensions)
        self.__centroide_nb_mots = np.zeros(self.__k)
        self.__nb_changements = 0
        self.__nb_generations = 0
        self.__equilibre = False
        self.__nb_resultats = nb_resultats
        
    def __construire_matrice_cooccurrences(self, liste_cooccurrences) -> np.array:
        matrice = np.zeros((self.__dimensions, self.__dimensions))
        if len(liste_cooccurrences) > 0:
            for point1, point2, score in liste_cooccurrences:
                matrice[point1, point2] = score
        return matrice
    
    # on initialise les centroïdes à des coordoonées intelligentes -> on prend celles de points de données au hasard
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
    def __determiner_centroides(self) -> None:
        self.__centroide_nb_mots = np.zeros(self.__k)
        for i, point in enumerate(self.__cooccurrences):
            distances = []
            for centroide in self.__centroides:
                distances.append(self.__operation_moindre_carres(point, centroide))
                self.__clusters_nouveaux[i] = distances.index(min((distances)))
                self.__centroide_nb_mots[self.__clusters_nouveaux[i]] += 1
                
    # on vérifie si l'équilibre a été atteint, autrement on poursuit les itérations            
    def __verifier_equilibre(self) -> None:
        if self.__nb_generations != 0:
            changements = np.not_equal(self.__clusters_nouveaux, self.__clusters_precedents)
            self.__nb_changements = sum(changements.astype(int))
            self.__clusters_precedents = self.__clusters_nouveaux
            self.__clusters_nouveaux = np.arange(self.__dimensions)
            if self.__nb_changements == 0:
                self.__equilibre = True
    
    def __nouvelles_coordonnees(self) -> None:
        for index_centroide in range(self.__k):
            points = np.where(self.__clusters_nouveaux == index_centroide)[0]
            self.__centroides[index_centroide] = np.mean([self.__cooccurrences[index_point] for index_point in points], axis=0)
            self.__imprimer_nb_mots(index_centroide)
            
    def __imprimer_nb_mots(self, index_centroide) -> None:
        print(f"Il y a {self.__centroide_nb_mots[index_centroide]} mots appartenant au centroïde {index_centroide}.")
        
    def __imprimer_changements(self) -> None:
        if self.__nb_generations != 0:
            print(f"\nEffectuée en {str(perf_counter() - self.__temps_iteration)} secondes. ({self.__nb_changements} changements)\n")
        else:
            print(f"\nEffectuée en {str(perf_counter() - self.__temps_iteration)} secondes.\n")
        print("**********************************")
        
    def __imprimer_iteration(self) -> None:
        print(f'\nItération {self.__nb_generations}\n')
        
    def __imprimer_resultats_clusters(self) -> None:
        clusters = [[] for _ in range(self.__k)]
            
        for index_point, index_cluster in enumerate(self.__clusters_precedents):
            distance = self.__operation_moindre_carres(self.__cooccurrences[index_point], self.__centroides[index_cluster])
            clusters[index_cluster].append((self.__donnees_uniques[index_point], distance))
            
        for index, cluster in enumerate(clusters):
            print(f"Pour le cluster {index}:")
            cluster = sorted(cluster, key = lambda x:x[1], reverse = False)
            for donnee, distance in cluster[:self.__nb_resultats]:
                print(f"\t{donnee} --> {distance}")
            print('\n')
            
    def __imprimer_resultats(self) -> None:
        print("\nFIN DE L'ALGORITHME KMEANS\n")
        print(f"Clustering effectué en {self.__nb_generations} itérations.")
        print(f"Durée totale de l'exécution: {str(perf_counter() - self.__temps_completion)} secondes.\n")
        self.__imprimer_resultats_clusters()

    def equilibrer(self) -> None:
        while self.__equilibre is False:
            self.__temps_iteration = perf_counter()
            self.__imprimer_iteration()
            self.__determiner_centroides()
            self.__nouvelles_coordonnees()
            self.__verifier_equilibre()
            self.__imprimer_changements()
            if not self.__equilibre:
                self.__nb_generations += 1
        self.__imprimer_resultats()


def main():
    bd = Dao()
    bd.connecter()
    partionnement(bd, 7, 30, 12)
    bd.deconnecter()

    return 0

if __name__ == '__main__':
    quit(main())
    
