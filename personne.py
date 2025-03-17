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

    @staticmethod
    def getPlusAncienDette(connexion, idPerson):
        query = f"""
            SELECT idBox, montant, mois, annee 
            FROM DETTE 
            WHERE montant IS NOT NULL AND montant <> 0 AND idPerson = {idPerson} 
            ORDER BY annee ASC, mois ASC;
        """
        rows = connexion.execute_query(query)
    
        if not rows:  # Si la requête ne retourne rien
            return None, None, None, None
    
        return rows[0]  # (idBox, montant, mois, annee)

    @staticmethod
    def updateDette(connexion,idBox,idPerson,mois,annee,montant):
        query = f"SELECT COUNT(*) FROM DETTE WHERE IDBOX = {idBox} AND IDPERSON = {idPerson} AND MOIS = {mois} AND ANNEE = {annee}"
        rows = connexion.execute_query(query)
        if rows: # rehefa misy dette anle box sy person
            print("update dette ty anhhhh")
            update = f"UPDATE Dette SET MONTANT = {montant} WHERE IDBOX = {idBox} AND IDPERSON = {idPerson} AND MOIS = {mois} AND ANNEE = {annee}"
            try:
                connexion.execute_update(update)
                print("update de dette reussie")
            except Exception as e:
                print(f"Erreur : {e}")
        else:
            print("insert new dette ty anhhhh")
            insert = f"INSERT INTO DETTE (IDPERSON,IDBOX,MONTANT,MOIS,ANNEE) VALUES ({idPerson},{idBox},{montant},{mois},{annee})"
            try:
                connexion.execute_update(insert)
            except Exception as e:
                print(f"Erreur : {e}")
        
    @staticmethod
    def getDetteMoisAnneePerson(connexion,idBox,idPerson,mois,annee):
        query = f"SELECT MONTANT FROM DETTE WHERE IDPERSON = {idPerson} AND IDBOX = {idBox} AND MOIS = {mois} AND ANNEE = {annee}"
        rows = connexion.execute_query(query)
        montant = 0        

        for row in rows:
            montant = row[0]

        return montant

