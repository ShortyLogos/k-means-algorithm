import sqlite3
from script import *

# connexion = sqlite3.connect(CHEMINBD)
# curseur = connexion.cursor()
# curseur.execute('SELECT "Hello world!"')
# rangees = curseur.fetchall()
# print(rangees)
# for rangee in rangees:
#     print(rangee)

class Dao:
    def __init__(self):
        self.chemin_bd = CHEMINBD

    def connecter(self):
        self.connexion = sqlite3.connect(self.chemin_bd)
        self.curseur = self.connexion.cursor()
        self.curseur.execute(FOREIGN_KEYS)

    def deconnecter(self):
        self.curseur.close()
        self.connexion.close()

    def creer_tables(self):
        self.curseur.execute(DROP_EMPLOYE)
        self.curseur.execute(DROP_DEPARTEMENT)
        self.curseur.execute(CREER_DEPARTEMENT)
        self.curseur.execute(CREER_EMPLOYE)

    def inserer_departement(self, id, nom):
        self.curseur.execute(INSERT_DEPARTEMENT, (id, nom))
        self.connexion.commit()

    def inserer_employe(self, id, nom, id_departement):
        self.curseur.execute(INSERT_EMPLOYE, (id, nom, id_departement))
        self.connexion.commit()
        

    def afficher(self):
        print('************** DEPARTEMENT ******************')
        self.curseur.execute(SELECT_DEPARTEMENT)
        for rangee in self.curseur.fetchall():
            print(rangee)

        print('************** EMPLOYE ******************')
        self.curseur.execute(SELECT_EMPLOYE)
        for rangee in self.curseur.fetchall():
            print(rangee)

def main():
    dao = Dao()
    dao.connecter()
    dao.creer_tables()
    dao.deconnecter()
    return 0

if __name__ == '__main__':
    quit(main())
