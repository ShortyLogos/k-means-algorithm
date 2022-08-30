import sys
import entrainement
import numpy as np

def lecture_texte(fichier):
    return np.array(fichier.read().split())
    

def main(params):
    try:
        fenetre, encodage, chemin = params[1:] # on ignore le premier paramètre qui correspond au nom du fichier
        try:
            fichier = open(chemin, 'r', encoding = f'{encodage}')
            texte_complet = lecture_texte(fichier)
            mots_uniques = entrainement.mots_uniques(texte_complet)
            print(mots_uniques)
            for mot in enumerate(mots_uniques):
                print(mot[0])
            print(entrainement.cooccurrences(mots_uniques))
            
            # for ligne in f:
            #     print(ligne)
            fichier.close()
        except:
            print("Chemin d'accès invalide")
    except:
        print("Veuillez spécifier la taille de la fenêtre, l'encodage et le chemin du fichier")
    
if __name__ == '__main__':
	quit(main(sys.argv))