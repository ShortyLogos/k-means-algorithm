import numpy as np

def mots_uniques(texte_original):
    return np.unique(texte_original)

def cooccurrences(mots_uniques_arg):
    return np.zeros((mots_uniques_arg.shape[0], mots_uniques_arg.shape[0]))

# création d'une matrice numpy en enlevant tous les doublons pour obtenir les index de tous les mots uniques