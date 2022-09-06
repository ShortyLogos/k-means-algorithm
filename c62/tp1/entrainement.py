import numpy as np
import re
from time import perf_counter

class Entrainement:
    def __init__(self, chemin, encodage, taille_fenetre):
        self.chemin = chemin
        self.encodage = encodage
        self.taille_fenetre = taille_fenetre
        
    def entrainer(self):
        start_time_training = perf_counter()
        self.lire_texte()
        self.extraire_mots_uniques()
        self.analyser_texte()
        end_time_training = perf_counter()
        print("Training Execution time: "+str(end_time_training-start_time_training))
            
    def lire_texte(self):
        try:
            fichier = open(self.chemin, 'r', encoding = self.encodage)
            self.texte_complet = re.findall("\w+", fichier.read())         
            fichier.close()
        except:
            print("Une erreur est survenus durant la lecture du fichier.")
        
    def extraire_mots_uniques(self):
        self.mots_uniques = {}
        for mot in self.texte_complet:
            if mot not in self.mots_uniques:
                self.mots_uniques[mot] = len(self.mots_uniques)
        
    def analyser_texte(self):
        self.cooccurrences = np.zeros((len(self.mots_uniques), len(self.mots_uniques)))
        demie_fenetre = self.taille_fenetre // 2
        for i in range(len(self.texte_complet)):
            for index in range(1, demie_fenetre+1):
                idx_mot = self.mots_uniques[self.texte_complet[i]]
                if i-index >= 0:
                    idx_cooccurrent = self.mots_uniques[self.texte_complet[i-index]]
                    self.cooccurrences[idx_mot][idx_cooccurrent] += 1
                if i+index < len(self.texte_complet):
                    idx_cooccurrent = self.mots_uniques[self.texte_complet[i+index]]
                    self.cooccurrences[idx_mot][idx_cooccurrent] += 1

# création d'une matrice numpy en enlevant tous les doublons pour obtenir les index de tous les mots uniques