# personne.py
from connexion import Connexion

class Personne:
    def __init__(self, idPerson, nom):
        self.idPerson = idPerson
        self.nom = nom

    @staticmethod
    def get_all(connexion):

        query = "SELECT * FROM person"
        rows = connexion.execute_query(query)
        
        personnes = []
        for row in rows:
            idPerson = row[0]  # ID dans la première colonne
            nom = row[1]       # Nom dans la deuxième colonne
            personne = Personne(idPerson, nom)
            personnes.append(personne)
        
        return personnes

    @staticmethod
    def create(connexion, nom):

        query = f"INSERT INTO person (nomPerson) VALUES ('{nom}')"
        try:
            connexion.execute_update(query)  # Utilisez execute_update ici pour l'insertion
            print(f"Personne '{nom}' ajoutée avec succès.")
        except Exception as e:
            print(f"Erreur lors de l'ajout de la personne : {e}")
        