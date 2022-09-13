import sys, os
import entrainement as ent
import prediction as pred

def main(params):
    prompt_utilisateur = ("\n Entrez un mot, le nombre de synonymes que vous voulez"
                                " et la méthode de calcul, i.e. produit scalaire: 0, least-squares: 1"
                                ", city-block: 2 \n\n Tapez q pour quitter.\n\n")
    verbose = False
    try:
        if len(params) > 4: # Argument facultatif pour imprimer les temps d'exécution
            verbose = bool(params[4])
        taille_fenetre, encodage, chemin = params[1:4] # Ignore le premier argument qui est le path du fichier actuel
    except:
        print("Veuillez spécifier la taille de la fenêtre, l'encodage et le chemin du fichier")
    
    if int(taille_fenetre) > 0 and encodage is not None and chemin is not None:
        entraineur = ent.Entrainement(chemin, encodage, int(taille_fenetre))
        entraineur.entrainer(verbose)
        
        predicteur = pred.Prediction(entraineur.cooccurrences, entraineur.mots_uniques, entraineur.encodage)
        predicteur.stopwords = os.path.join(sys.path[0], "stopwords.txt")
        
        entree_utilisateur = input(prompt_utilisateur)
        while entree_utilisateur != 'q':
            try:
                mot, nbr_reponses, methode_choisie = str.lower(entree_utilisateur).split()
                predicteur.predire(mot, nbr_reponses, methode_choisie, verbose)
            except ValueError:
                print('Vous devez entrer 3 arguments. Veuillez réessayer.')
            entree_utilisateur = input(prompt_utilisateur)
    
if __name__ == '__main__':
	quit(main(sys.argv))