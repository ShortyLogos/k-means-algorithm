import sqlite3
import script

class Dao:
    def __init__(self) -> None:
        self.chemin_bd = './mainBD.db'

    def connecter(self) -> None:
        self.connexion = sqlite3.connect(self.chemin_bd)
        self.curseur = self.connexion.cursor()
        self.activer_foreign_keys()

    def deconnecter(self) -> None:
        if self.connexion:
            self.curseur.close()
            self.connexion.close()
            self.connexion = None

    def creer_tables(self) -> None:
        self.curseur.execute(script.CREER_VOCABULAIRE)
        self.curseur.execute(script.CREER_COOCCURRENCES)

    def detruire_tables(self) -> None:
        self.curseur.execute(script.DROP_COOCCURRENCES)
        self.curseur.execute(script.DROP_VOCABULAIRE)

    def inserer_vocabulaire(self, vocabulaire: list) -> None:
        self.curseur.executemany(script.INSERT_VOCABULAIRE, vocabulaire)
        self.connexion.commit()

    def inserer_cooccurrences(self, cooccurrences: list) -> None:
        self.curseur.executemany(script.INSERT_COOCCURRENCES, cooccurrences)
        self.connexion.commit()

    def obtenir_donnees(self, taille: int) -> tuple[dict, list]:
        vocabulaire = {}
        vocabulaire_liste = self.curseur.execute(script.SELECT_VOCABULAIRE).fetchall()
        for pair in vocabulaire_liste:
            mot = pair[0]
            index = pair[1]
            vocabulaire[mot] = index
        cooccurrences = self.curseur.execute(script.SELECT_COOCCURRENCES, str(taille)).fetchall()
        return [vocabulaire, cooccurrences]

    def activer_foreign_keys(self):
        self.curseur.execute('PRAGMA foreign_keys = 1')

    def desactiver_foreign_keys(self):
        self.curseur.execute('PRAGMA foreign_keys = 0')

    def verifier_foreign_keys(self):
        print('Erreur: ')
        print(self.curseur.execute('PRAGMA foreign_key_check(cooccurrences);').fetchall()[0])

    def afficher(self) -> None:
        print('************** VOCABULAIRE ******************')
        self.curseur.execute(script.SELECT_TEST_VOCABULAIRE)
        for rangee in self.curseur.fetchall():
            print(rangee)

        print('************** COOCCURRENCES ****************')
        self.curseur.execute(script.SELECT_TEST_COOCCURENCES)
        for rangee in self.curseur.fetchall():
            print(rangee)

def main():
    dao = Dao()
    dao.connecter()
    dao.creer_tables()
    dao.afficher()
    dao.detruire_tables()
    dao.deconnecter()
    return 0

if __name__ == '__main__':
    quit(main())
