from connexion import Connexion
from marche import Marche
from personne import Personne
from fenetre import Fenetre
from box import Box
from paiement import Paiement

def lire_config():
    with open("config.txt", "r") as file:
        return file.readline().strip()

def main():
    db_file = lire_config()
    print(f"Chemin de la base : {db_file} (Type: {type(db_file)})")

    connexion = Connexion(db_file)
    connexion.connect()

    fenetre = Fenetre("1300x700", "Tsena",connexion)
    # print(Paiement.getPourcentageNaloa(connexion,2,1,2024))
    fenetre.afficher()
    # print(Box.getLoyerBox(connexion,4,1,2024))
    # print(Paiement.getNombreMoisPaye(connexion,2,1,1,2024))
    connexion.close()

# Exécuter le programme
if __name__ == "__main__":
    main()
