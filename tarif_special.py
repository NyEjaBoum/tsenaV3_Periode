class tarif_special:
    def __init__(self,idTarifSpecial,idMarche,mois,annee,montant):
        self.idTarifSpecial = idTarifSpecial
        self.idMarche = idMarche
        self.mois = mois
        self.annee = annee
        self.montant = montant

    @staticmethod
    def getAllTarifSpecial(connexion):
        query = "SELECT * FROM TARIF_SPECIAL"
        rows = connexion.execute_query(query)
        T = []
        for row in rows:
            idTarif  = row[0]
            idMarche = row[1]
            mois = row[2]
            annee = row[3]
            montant = row[4]
            t = tarif_special(idTarif,idMarche,mois,annee,montant)
            T.append(t)

        return T

    @staticmethod 
    def getTarifSpecialMoisAnnee(connexion,mois,annee):
        query = f"SELECT montant FROM TARIF_SPECIAL WHERE MOIS = {mois} AND ANNEE = {annee}"
        rows = connexion.execute_query(query)
        tarif = 0
        for row in rows:
            tarif = row[0]
        return tarif