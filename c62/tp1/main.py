import sys
import entrainement
import numpy as np

def lecture_texte(fichier):
    return np.array(fichier.read().split())

def main(params):
    texte_complet = None
    taille_fenetre = None
    
    try:
        taille_fenetre, encodage, chemin = params[1:] # on ignore le premier paramètre qui correspond au nom du fichier
        try:
            fichier = open(chemin, 'r', encoding = f'{encodage}')
            texte_complet = lecture_texte(fichier)           
            fichier.close()
        except:
            print("Chemin d'accès invalide")
    except:
        print("Veuillez spécifier la taille de la fenêtre, l'encodage et le chemin du fichier")
        
    ent = entrainement.Entrainement(texte_complet, int(taille_fenetre))

    
if __name__ == '__main__':
	quit(main(sys.argv))