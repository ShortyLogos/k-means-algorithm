import sqlite3
import script
from time import perf_counter
import traceback

class Dao:
    def __init__(self, verbose: bool = False) -> None:
        self.chemin_bd = './mainBD.db'
        self.__verbose = verbose
        self.__start_time_training = perf_counter()

    def __enter__(self):
        self.connecter()
        return self
    
    def __exit__(self, exc_type, exc_value, exc_tb):
        self.deconnecter()
        if isinstance(exc_value, Exception):
            trace = traceback.format_exception(exc_type, exc_value, exc_tb)
            print(''.join(trace))
            return False
        return True

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
        if self.__verbose: print("Insertion Vocabulaire Execution time: " + str(perf_counter()-self.__start_time_training))

    def inserer_cooccurrences(self, cooccurrences: list) -> None:
        self.curseur.executemany(script.INSERT_COOCCURRENCES, cooccurrences)
        self.connexion.commit()
        if self.__verbose: print("Insertion Cooccurrences Execution time: " + str(perf_counter()-self.__start_time_training))

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
