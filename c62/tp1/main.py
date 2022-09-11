import sys
import entrainement as ent
import prediction as pred
import numpy as np

def main(params):  
    try:
        taille_fenetre, encodage, chemin = params[1:] # on ignore le premier paramètre qui correspond au nom du fichier actuel
    except:
        print("Veuillez spécifier la taille de la fenêtre, l'encodage et le chemin du fichier")
    
    if int(taille_fenetre) > 0 and encodage is not None and chemin is not None:
        entraineur = ent.Entrainement(chemin, encodage, int(taille_fenetre))
        entraineur.entrainer()
        predicteur = pred.Prediction(entraineur.cooccurrences, entraineur.mots_uniques, entraineur.encodage)
        predicteur.generer_stopwords()
        predicteur.predire()
    
if __name__ == '__main__':
	quit(main(sys.argv))