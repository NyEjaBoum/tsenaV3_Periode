class Loyer:
    def __init__(self,idLoyer,idMarche,montant):
        self.idLoyer = idLoyer
        self.idMarche = idMarche
        self.montant = montant

    @staticmethod
    def create(connexion,idMarche,montant):
        query = f"INSERT INTO LOYER (idMarche,montant) VALUES ({idMarche},{montant})"
        try:
            connexion.execute_update(query)
            print("Insertion Loyer reussie")
        except Exception as e:
            print(f"Erreur d'insertion Loyer : {e}")