import numpy as np
import re

class Entrainement:
    def __init__(self, chemin: str, encodage: str, taille_fenetre: int) -> None:
        self.__chemin = chemin
        self.__encodage = encodage
        self.__taille_fenetre = taille_fenetre
        self.__cooccurrences = None
        self.__mots_uniques = {}
        self.__liste_cooccurrences = None

    @property
    def mots_uniques(self) -> dict:
        return self.__mots_uniques

    @property
    def cooccurrences(self) -> list:
        liste = []
        valeurs_positives = np.argwhere(self.__cooccurrences > 0)
        for element in valeurs_positives:
            index_mot = int(element[0])
            index_mot2 = int(element[1])
            valeur = int(self.__cooccurrences[index_mot][index_mot2])
            liste.append((self.__taille_fenetre, index_mot, index_mot2, valeur))
        return liste

    def reconstruire(self, vocabulaire: dict, liste_cooccurrences: list) -> None:
        self.__mots_uniques = vocabulaire
        self.__liste_cooccurrences = liste_cooccurrences

    def entrainer(self) -> None:
        self.__lire_texte()
        self.__extraire_mots_uniques()
        self.__analyser_texte()
            
    def __lire_texte(self) -> None:
        try:
            fichier = open(self.__chemin, 'r', encoding = self.__encodage)
            self.__texte_complet = re.findall("\w+", fichier.read().lower()) # on met en minuscule le texte pour éviter les doublons dûs à des majuscules
            fichier.close()
        except:
            raise OSError("Une erreur est survenue durant la lecture du fichier.")
        
    def __extraire_mots_uniques(self) -> None:
        for mot in self.__texte_complet:
            if mot not in self.__mots_uniques:
                self.__mots_uniques[mot] = len(self.__mots_uniques) # avec le length, on obtient le bon index sans l'utilisation d'un itérateur
        
    def __analyser_texte(self) -> None:
        self.__cooccurrences = np.zeros((len(self.__mots_uniques), len(self.__mots_uniques)))
        if self.__liste_cooccurrences:
            for mot1, mot2, score in self.__liste_cooccurrences:
                self.__cooccurrences[mot1][mot2] = score
        demie_fenetre = self.__taille_fenetre // 2
        for i in range(len(self.__texte_complet)):
            for index in range(1, demie_fenetre + 1):
                idx_mot = self.__mots_uniques[self.__texte_complet[i]]
                if i - index >= 0:
                    idx_cooccurrent = self.__mots_uniques[self.__texte_complet[i-index]]
                    self.__cooccurrences[idx_mot][idx_cooccurrent] += 1
                if i + index < len(self.__texte_complet): # On itère dans les deux sens en même temps
                    idx_cooccurrent = self.__mots_uniques[self.__texte_complet[i+index]]
                    self.__cooccurrences[idx_mot][idx_cooccurrent] += 1