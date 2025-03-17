from box import Box
from datetime import datetime
# from paiement import Paiement

class Location:
    def __init__(self,idLocation,idBox,idPerson,date,dateFin):
        self.idLocation = idLocation
        self.idBox = idBox
        self.idPerson = idPerson
        self.date = date
        self.dateFin = dateFin
    
    @staticmethod
    def create(connexion, idBox, idPerson, dateDebut,dateFin):
        dateDebutContrat = dateDebut if isinstance(dateDebut, str) else dateDebut.strftime('%Y-%m-%d')
        # dateFinContrat = dateFin if isinstance(dateFin, str) else dateFin.strftime('%Y-%m-%d')
        if dateFin is None:
            query = f"INSERT INTO LOCATION (IDBOX,IDPERSON,dateDebut,dateFin) VALUES ({idBox},{idPerson},'{dateDebutContrat}',NULL)"
        else :
            dateFinContrat = dateFin if isinstance(dateFin, str) else dateFin.strftime('%Y-%m-%d')
            query = f"INSERT INTO LOCATION (IDBOX,IDPERSON,dateDebut,dateFin) VALUES ({idBox},{idPerson},'{dateDebutContrat}','{dateFinContrat}')"
        print("eto lesy eh ")
        try:
            connexion.execute_update(query)
            print("Insertion Location réussie")
        except Exception as e:
            print(f"Erreur : {e}")


    # @staticmethod
    # def create(connexion, idBox, idPerson, dateDebut, dateFin):
    #     # Gestion de dateDebut
    #     dateDebutContrat = dateDebut if isinstance(dateDebut, str) else dateDebut.strftime('%Y-%m-%d')
        
    #     # Gestion de dateFin : si None, on utilise NULL, sinon on formate
    #     dateFinContrat = 'NULL' if dateFin is None else (dateFin if isinstance(dateFin, str) else dateFin.strftime('%Y-%m-%d'))
    #     print(dateFinContrat)
    #     print("eto lesy eh ")
    #     query = f"INSERT INTO LOCATION (IDBOX, IDPERSON, dateDebut, dateFin) VALUES ({idBox}, {idPerson}, '{dateDebutContrat}', '{dateFinContrat}')"
    #     try:
    #         connexion.execute_update(query)
    #         print("Insertion Location réussie")
    #     except Exception as e:
    #         print(f"Erreur : {e}")

    # @staticmethod
    # def getDebutContrat(connexion,idBox,idPerson):
    #     query = f"SELECT MONTH(DATEDEBUT),YEAR(DATEDEBUT) FROM LOCATION WHERE IDBOX = {idBox} AND IDPERSON = {idPerson}"
    #     rows = connexion.execute_query(query)
    #     for row in rows:
    #         mois,annee = row[0],row[1]
    #     return mois,annee

    # @staticmethod
    # def getFinContrat(connexion,idBox,idPerson):
    #     query = f"SELECT " DEC 2022 JANV 2023 

    # @staticmethod
    # def getTokonyAloaContrat(connexion,idPerson,mois,annee):

    @staticmethod
    def getDebutContrat(connexion, idBox, idPerson):
        query = f"SELECT TOP 1 MONTH(DATEDEBUT), YEAR(DATEDEBUT) FROM LOCATION WHERE IDBOX = {idBox} AND IDPERSON = {idPerson} ORDER BY DATEDEBUT DESC"
        rows = connexion.execute_query(query)
        for row in rows:  # TOP 1 garantit une seule ligne
            mois, annee = row[0], row[1]
            return mois, annee
        return None, None  # Si aucun contrat trouvé

    @staticmethod
    def getFinContrat(connexion, idBox, idPerson):
        query = f"SELECT TOP 1 MONTH(DATEFIN), YEAR(DATEFIN) FROM LOCATION WHERE IDBOX = {idBox} AND IDPERSON = {idPerson} ORDER BY DATEDEBUT DESC"
        rows = connexion.execute_query(query)
        for row in rows:
            mois, annee = row[0], row[1]
            return mois, annee
        return None, None  # Si aucun contrat trouvé

    @staticmethod
    def louerBox(connexion, idBox, idPerson, date_str,date_str2):
        date = datetime.strptime(date_str, '%Y-%m-%d') if isinstance(date_str, str) else date_str
        dateFin = datetime.strptime(date_str2, '%Y-%m-%d') if isinstance(date_str2, str) else date_str2

        Location.create(connexion, idBox, idPerson, date,dateFin)
        
        moisDebut = date.month
        anneeDebut = date.year

        loyerApayer = Box.getLoyerBox(connexion, idBox, moisDebut, anneeDebut)
        # Box.updatePerson(connexion,idBox,idPerson)
        Box.insertDette(connexion, idPerson, idBox, loyerApayer, moisDebut, anneeDebut)

    @staticmethod
    def quitterBox(connexion, idBox, idPerson, date_str):
        date = datetime.strptime(date_str, '%Y-%m-%d') if isinstance(date_str, str) else date_str
        date_access = f"#{date.strftime('%Y-%m-%d')}#"
        
        query = f"""
            UPDATE LOCATION 
            SET DATEFIN = {date_access}
            WHERE IDBOX = {idBox}
            AND IDPERSON = {idPerson}
            AND DATEFIN IS NULL
        """
        connexion.execute_update(query)
        Box.manalaPerson(connexion, idBox)

    @staticmethod
    def getAllContratPerson(connexion,idPerson):
        query = f"SELECT * FROM LOCATION WHERE IDPERSON = {idPerson}"
        rows = connexion.execute_query(query)
        liste = []
        for row in rows:
            idLocation = row[0]
            idBox = row[1]
            idPerson = row[2]
            dateDebut = row[3]
            dateFin = row[4]
            lo = Location(connexion,idBox,idPerson,dateDebut,dateFin)
            liste.append(lo)
        return liste

    @staticmethod
    def getContratValideMoisAnneePerson(connexion,idPerson,mois,annee):
        query = f"SELECT * FROM LOCATION WHERE IDPERSON = 4"
        rows = connexion.execute_query(query)
        liste = []
        for row in rows:
            idLocation = row[0]
            idBox = row[1]
            idPerson = row[2]
            dateDebut = row[3]
            dateFin = row[4]
            lo = Location(connexion,idBox,idPerson,dateDebut,dateFin)
            liste.append(lo)
        return liste

    # @staticmethod
    # def getDureeContratPersonParBox(connexion,idBox,idPerson):
    #     query = f"""SELECT DateDiff("m",dateDebut,dateFin) + 1 AS dureeMois FROM LOCATION WHERE IDPERSON = {idPerson} AND IDBOX = {idBox}"""
    #     rows = connexion.execute_query(query)
    #     for row in rows:
    #         return row[0]
    
    @staticmethod
    def getMaxDateFinContratPerson(connexion, idPerson):
        query = f"SELECT MAX(dateFin) FROM LOCATION WHERE IDPERSON = {idPerson}"
        result = connexion.execute_query(query)
        if result and result[0][0]:
            return result[0][0]
        return None




    
    
    # @staticmethod
    # def misyOlonaVe(connexion,idBox,mois,annee):
    #     mois = int(mois)
    #     annee = int(annee)
    #     mois_total = (annee * 12 + mois)
    #     print(f" mois total{mois_total}")
    #     query = f"""SELECT idPerson,type FROM LOCATION WHERE IDBOX = {idBox} AND ((YEAR(DATELOCATION) *12 +MONTH(DATELOCATION)) <= {mois_total})
    #             ORDER BY (YEAR(DATELOCATION) * 12 + MONTH(DATELOCATION)) DESC
    #             """
    #     rows = connexion.execute_query(query)
    #     idPerson = None
    #     Type = None

    #     for row in rows:
    #         idPerson = row[0]
    #         Type = row[1]
    #         break
    #     print(f"id Box {idBox} type {Type} mois {mois} annee {annee}")
    #     if Type == 1:
    #         return True
    #     return False


    @staticmethod
    def misyOlonaVe(connexion, idBox, mois, annee):
        mois = int(mois)
        annee = int(annee)
        mois_total = (annee * 12 + mois)
        print(f"mois total {mois_total}")

        query = f"""
            SELECT idPerson 
            FROM LOCATION 
            WHERE idBox = {idBox} 
            AND (
                dateFin IS NULL 
                OR (YEAR(dateFin) * 12 + MONTH(dateFin)) >= {mois_total}
            )
            AND (YEAR(dateDebut) * 12 + MONTH(dateDebut)) <= {mois_total}
            ORDER BY (YEAR(dateDebut) * 12 + MONTH(dateDebut)) DESC
        """
        rows = connexion.execute_query(query)
        
        for row in rows:
            idPerson = row[0]
            print(f"id Box {idBox} mois {mois} annee {annee} idPerson {idPerson}")
            return True
            break
        
        return False

    @staticmethod
    def isHisBoxMoisAnnee(connexion, idBox, idPerson, mois, annee):
        mois = int(mois)
        annee = int(annee)
        mois_total = (annee * 12 + mois)
        print(f"mois total {mois_total}")
        
        query = f"""SELECT idPerson, type 
                    FROM LOCATION 
                    WHERE IDBOX = {idBox} 
                    AND idPerson = {idPerson} 
                    AND ((YEAR(DATELOCATION) * 12 + MONTH(DATELOCATION)) <= {mois_total})
                    ORDER BY (YEAR(DATELOCATION) * 12 + MONTH(DATELOCATION)) DESC"""
        rows = connexion.execute_query(query)
        
        found_idPerson = None
        Type = None
        for row in rows:
            found_idPerson = row[0]
            Type = row[1]
            break
        
        print(f"id Box {idBox} idPerson {found_idPerson} type {Type} mois {mois} annee {annee}")
        
        # Vérifie si la personne correspond et si la location est active (type = 1)
        if found_idPerson == idPerson and Type == 1:
            return True
        return False


    @staticmethod
    def isDetteInContrat(connexion, idBox, idPerson, mois_dette, annee_dette):
        mois_dette_total = annee_dette * 12 + mois_dette
        query = f"""
            SELECT MONTH(dateDebut), YEAR(dateDebut), MONTH(dateFin), YEAR(dateFin)
            FROM LOCATION 
            WHERE idBox = {idBox} AND idPerson = {idPerson}
            AND (YEAR(dateDebut) * 12 + MONTH(dateDebut)) <= {mois_dette_total}
            AND (dateFin IS NULL OR (YEAR(dateFin) * 12 + MONTH(dateFin)) >= {mois_dette_total})
        """
        rows = connexion.execute_query(query)
        if rows:
            return rows[0]  # Retourne (mois_debut, annee_debut, mois_fin, annee_fin)
        return None

    @staticmethod
    def checkAndAdvanceToNextMonth(mois_courant, annee_courant, mois_fin, annee_fin):
        mois_courant_total = annee_courant * 12 + mois_courant
        mois_fin_total = (annee_fin * 12 + mois_fin) if mois_fin and annee_fin else None
        
        if mois_fin_total and mois_courant_total > mois_fin_total:
            return True, None, None  # Fin atteinte, mois et année non mis à jour ici
        else:
            # Avancer au mois suivant
            mois_suivant = mois_courant + 1
            annee_suivante = annee_courant
            if mois_suivant > 12:
                mois_suivant = 1
                annee_suivante += 1
            return False, mois_suivant, annee_suivante


    @staticmethod
    def getProchainContrat(connexion, idBox, idPerson, mois_fin, annee_fin):
        query = f"""
            SELECT TOP 1 MONTH(dateDebut), YEAR(dateDebut)
            FROM LOCATION 
            WHERE idBox = {idBox} AND idPerson = {idPerson} 
            AND dateDebut > #{annee_fin}-{mois_fin:02d}-01#
            ORDER BY dateDebut ASC
        """
        rows = connexion.execute_query(query)
        if rows:
            return rows[0]  # Retourne (mois_debut, annee_debut)
        return None



