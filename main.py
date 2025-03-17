from connexion import Connexion
from marche import Marche
from personne import Personne
from fenetre import Fenetre
from box import Box
from paiement import Paiement
from location import Location
from insert import Insert 

def lire_config():
    with open("config.txt", "r") as file:
        return file.readline().strip()

def main():
    db_file = lire_config()
    print(f"Chemin de la base : {db_file} (Type: {type(db_file)})")

    connexion = Connexion(db_file)
    connexion.connect()

    fenetre = Fenetre("1300x700", "Tsena",connexion)
    # print(Paiement.getResteApayerByDate(connexion,1,1,1,2022))
    # print(Paiement.sommeTokonyNaloanyByDate(connexion,4,1,2023))
    # test = Location.getContratValideMoisAnneePerson(connexion,4,1,2023)
    # for row in test:
    #     print(row.idBox)
    # print(Location.getDureeContratPersonParBox(connexion,1,1))
    # Insert.insertDonnees(connexion)
    fenetre.afficher()
    # liste = Location.getAllContratPerson(connexion,1)
    # for row in liste:
    #     print(row.idBox)

    allP = Personne.get_all(connexion)
    for r in allP:
        print(f"dette de {r.idPerson} est {Paiement.sommeDetteTokonyNaloany(connexion,r.idPerson,5,2026)}")
    
    connexion.close()

# Exécuter le programme
if __name__ == "__main__":
    main()
