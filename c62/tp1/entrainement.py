import numpy as np

class Entrainement:
    def __init__(self, texte_complet, taille_fenetre):
        self.texte_complet = texte_complet
        self.taille_texte = len(self.texte_complet) - 1
        array_uniques = np.unique(self.texte_complet)
        self.mots_uniques = {}
        for index, mot in enumerate(array_uniques):
            self.mots_uniques[mot] = index
        self.cooccurrences = np.zeros((array_uniques.shape[0], array_uniques.shape[0]))
        self.taille_fenetre = taille_fenetre
        self.demie_fenetre = (taille_fenetre - 1) / 2
        self.index_fenetre = 0
        self.ajout_cooccurrence()
        
    def ajout_cooccurrence(self):
        for index in range(self.taille_fenetre):
            if not index == self.demie_fenetre:
                if (self.index_fenetre - index) > 0 and (self.index_fenetre + index) < self.taille_texte:
                    idx_mot = self.mots_uniques[self.texte_complet[self.index_fenetre]]
                    idx_relatif = (self.demie_fenetre + 1) - self.taille_fenetre + index
                    print(idx_relatif)
                    #print(idx_mot)
                    #temp = self.texte_complet[self.index_fenetre + idx_relatif]
                    #idx_cooccurrent = self.mots_uniques[temp]
                    #self.cooccurrences[idx_mot][idx_cooccurrent] += 1
        self.deplacer_fenetre()
                    
    def deplacer_fenetre(self):
        if not self.index_fenetre == self.taille_texte:
            self.index_fenetre += 1
            self.ajout_cooccurrence()
        else:
            print(self.cooccurrences)

# création d'une matrice numpy en enlevant tous les doublons pour obtenir les index de tous les mots uniques