import sys

def main(params):
    try:
        size_arg, encoding_arg, path_arg = params[1:] # on ignore le premier paramètre qui correspond au nom du fichier
        try:
            f = open(path_arg, 'r', encoding = f'{encoding_arg}')
            for line in f:
                print(line)
            f.close()
        except:
            print("Chemin d'accès invalide")
    except:
        print("Veuillez spécifier la taille de la fenêtre, l'encodage et le chemin du fichier")
    
if __name__ == '__main__':
	quit(main(sys.argv))