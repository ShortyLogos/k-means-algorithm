import sys
import entrainement as ent
import prediction as pred
import numpy as np
from time import perf_counter

def main(params):
    start_time_total = perf_counter()
    
    try:
        taille_fenetre, encodage, chemin = params[1:] # on ignore le premier paramètre qui correspond au nom du fichier actuel
    except:
        print("Veuillez spécifier la taille de la fenêtre, l'encodage et le chemin du fichier")
    
    if taille_fenetre>0 and encodage is not None and chemin is not None:
        entraineur = ent.Entrainement(chemin, encodage, int(taille_fenetre))
        entraineur.entrainer()
        predicteur = pred.Prediction(entraineur.cooccurrences)
    
    end_time_total = perf_counter()
    print("Total Execution time: "+str(end_time_total-start_time_total))

    
if __name__ == '__main__':
	quit(main(sys.argv))
 
 # Sexual Lobster, the girl on TV