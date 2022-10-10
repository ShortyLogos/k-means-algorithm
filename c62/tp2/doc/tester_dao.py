from dao import Dao

print(f'Dans tester_dao __name__: {__name__}') 

def main():
    bd = Dao()
    bd.connecter()

    bd.creer_tables()

    bd.inserer_departement(1, 'Architecture')
    bd.inserer_employe(1000, 'toto', 1)

    bd.afficher()

    bd.deconnecter()

    return 0

if __name__ == '__main__':
    quit(main())