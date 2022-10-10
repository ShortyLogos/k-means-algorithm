import sqlite3
from tkinter import INSERT

CHEMINBD = 'emp_dep.db'
FOREIGN_KEYS = 'PRAGMA foreign_keys = 1'

CREER_DEPARTEMENT = '''
CREATE TABLE IF NOT EXISTS departement
(
    id INT PRIMARY KEY NOT NULL,
    nom CHAR(15) UNIQUE NOT NULL
)
'''
DROP_DEPARTEMENT = 'DROP TABLE IF EXISTS departement'
INSERT_DEPARTEMENT = 'INSERT INTO departement(id, nom) VALUES(?, ?)'
SELECT_DEPARTEMENT = 'SELECT * FROM departement'
DELETE_DEPARTEMENT = 'DELETE FROM departement WHERE nom = ?'

CREER_EMPLOYE = '''
CREATE TABLE IF NOT EXISTS employe
(
    id INT NOT NULL,
    id_departement INT NOT NULL,
    nom CHAR(15) NOT NULL,
    PRIMARY KEY(id),
    FOREIGN KEY(id_departement) REFERENCES departement(id)
)
'''
DROP_EMPLOYE = 'DROP TABLE IF EXISTS employe'
INSERT_EMPLOYE = 'INSERT INTO employe(id, nom, id_departement) VALUES(?, ?, ?)'
SELECT_EMPLOYE = 'SELECT * FROM employe'
DELETE_EMPLOYE = 'DELETE FROM employe WHERE nom = ?'

# connexion = sqlite3.connect(CHEMINBD)
# curseur = connexion.cursor()
# curseur.execute('SELECT "Hello world!"')
# rangees = curseur.fetchall()
# print(rangees)
# for rangee in rangees:
#     print(rangee)

def connecter(chemin_bd):
    connexion = sqlite3.connect(chemin_bd)
    curseur = connexion.cursor()
    curseur.execute(FOREIGN_KEYS)

    return connexion, curseur

def deconnecter(connexion, curseur):
    curseur.close()
    connexion.close()

def creer_tables(curseur):
    curseur.execute(DROP_EMPLOYE)
    curseur.execute(DROP_DEPARTEMENT)
    curseur.execute(CREER_DEPARTEMENT)
    curseur.execute(CREER_EMPLOYE)

def inserer(curseur):
    curseur.execute(INSERT_DEPARTEMENT, (1, 'Informatique'))
    curseur.execute(INSERT_EMPLOYE, (1000, 'Marcel', 1))
    curseur.execute(INSERT_EMPLOYE, (2000, 'Michelle', 1))
    curseur.execute(INSERT_EMPLOYE, (3000, 'Richard', 1))
    curseur.execute(INSERT_EMPLOYE, (4000, 'Toto', 1))

def afficher(curseur):
    print('************** DEPARTEMENT ******************')
    curseur.execute(SELECT_DEPARTEMENT)
    for rangee in curseur.fetchall():
        print(rangee)

    print('************** EMPLOYE ******************')
    curseur.execute(SELECT_EMPLOYE)
    for rangee in curseur.fetchall():
        print(rangee)

        

def main():
    conn, cur = connecter(CHEMINBD)

    #creer_tables(cur)
    #inserer(cur)
    #conn.commit()
    afficher(cur)
    #cur.execute(DELETE_EMPLOYE, ('Toto',))
    #conn.commit()
    #cur.execute(DELETE_DEPARTEMENT, ('Informatique',))
    employes = [(5000, 'JMD', 1), (6000, 'JCD', 1)]
    cur.executemany(INSERT_EMPLOYE, employes)
    afficher(cur)

    deconnecter(conn, cur)

    return 0

if __name__ == '__main__':
    quit(main())
