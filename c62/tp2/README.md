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
python main.py -e -t [taille fenetre, comme 7] --enc [encodage, tel que utf-8] --chemin \texte\[nom de fichier texte].txt
```

3. Effectuer une recherche de synonymes
```
python main.py -r -t [taille fenetre, comme 7]
```