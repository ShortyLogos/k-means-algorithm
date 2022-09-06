import numpy as np
import re
from time import perf_counter

class Entrainement:
    def __init__(self, chemin, encodage, taille_fenetre):
        self.__chemin = chemin
        self.__encodage = encodage
        self.__taille_fenetre = taille_fenetre
        self.__cooccurrences = None
        self.__mots_uniques = {}
        
    @property
    def cooccurrences(self):
        return self.__cooccurrences

    @property
    def mots_uniques(self):
        return self.__mots_uniques

    def entrainer(self):
        start_time_training = perf_counter()
        self.__lire_texte()
        self.__extraire_mots_uniques()
        self.__analyser_texte()
        print("Training Execution time: "+str(perf_counter()-start_time_training))
            
    def __lire_texte(self):
        try:
            fichier = open(self.__chemin, 'r', encoding = self.__encodage)
            self.__texte_complet = re.findall("\w+", fichier.read().lower()) # On met en minuscule le texte pour éviter les doublons dû à des majuscules
            fichier.close()
        except:
            print("Une erreur est survenus durant la lecture du fichier.")
        
    def __extraire_mots_uniques(self):
        for mot in self.__texte_complet:
            if mot not in self.__mots_uniques:
                self.__mots_uniques[mot] = len(self.__mots_uniques) #Avec le length, on obtiens le bon indexe sans l'utilisation d'un itérateur
        
    def __analyser_texte(self):
        self.__cooccurrences = np.zeros((len(self.__mots_uniques), len(self.__mots_uniques)))
        demie_fenetre = self.__taille_fenetre // 2
        for i in range(len(self.__texte_complet)):
            for index in range(1, demie_fenetre+1):
                idx_mot = self.__mots_uniques[self.__texte_complet[i]]
                if i-index >= 0:
                    idx_cooccurrent = self.__mots_uniques[self.__texte_complet[i-index]]
                    self.__cooccurrences[idx_mot][idx_cooccurrent] += 1
                if i+index < len(self.__texte_complet):
                    idx_cooccurrent = self.__mots_uniques[self.__texte_complet[i+index]]
                    self.__cooccurrences[idx_mot][idx_cooccurrent] += 1