# Répertoire du cours d'IA-ii, sous-répertoire TP2

## ÉQUIPE
+ Déric Marchand
+ Karl Marchand

## Commandes pour exécuter le logiciel:
1. Générer la base de données (et la réinitialiser)
```
python main.py -b
```

2. Effectuer un entraînement et stocker les résultats
```
python main.py -e -t TAILLE_FENETRE --enc ENCODAGE --chemin \texte\NOM_FICHIER.txt
```
*Note* : pour utiliser le mode verbeux (analyse des performances), ajouter l'argument -v.

3. Effectuer une recherche de synonymes
```
python main.py -r -t TAILLE_FENETRE
```
*Notes* : 
+ Pour utiliser le mode verbeux (analyse des performances), ajouter l'argument -v. Valide pour la phase d'entraînement.
+ Pour spécifier le chemin vers un autre fichier de *stopwords* que celui intégré par défaut, ajouter l'argument -s CHEMIN_DU_FICHIER
