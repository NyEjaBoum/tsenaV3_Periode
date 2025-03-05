from box import Box
from marche import Marche
from datetime import datetime


class Paiement:
    def __init__(self,idPayement,idBox,idPerson,mois,annee,montant,date):
        self.idPayement = idPayement
        self.idBox = idBox
        self.idPerson = idPerson
        self.mois = mois
        self.annee = annee
        self.montant = montant
        self.date = date
    
    @staticmethod
    def getLoyerDejaPaye(connexion, idBox, idPerson):
        query = f"SELECT SUM(MONTANT) AS TOTAL_PAYE FROM PAIEMENT WHERE idBox = {idBox} AND idPerson = {idPerson}"
        rows = connexion.execute_query(query)
        total_paye = 0
        for row in rows:
            if row[0] is not None:
                total_paye = row[0]
        return total_paye


    @staticmethod
    def getNombreMoisPaye(connexion,idBox,idPerson,mois,annee):
        loyerApayer = Box.getLoyerBox(connexion,idBox,mois,annee)
        loyerDejaPayer = Paiement.sumLoyerMoisAnneeBox(connexion,idBox,mois,annee)
        nombreMoisPayer = loyerDejaPayer/loyerApayer
        return nombreMoisPayer
    
    @staticmethod
    def getProchainMoisAPayer(connexion, idBox, idPerson,mois,annee):
        nombreMoisPayer = Paiement.getNombreMoisPaye(connexion, idBox, idPerson,mois,annee)
        moisDepart, anneeDepart = 1, 2024

        moisDepart += int(nombreMoisPayer)
        while moisDepart > 12:
            moisDepart -= 12
            anneeDepart += 1

        return moisDepart, anneeDepart

    @staticmethod
    def getResteApayer(connexion,idBox,idPerson,mois,annee):
        sumLoyer = Paiement.sumLoyerMoisAnneeBoxPerson(connexion,idBox,idPerson,mois,annee)
        loyerApayer = Box.getLoyerBox(connexion,idBox,mois,annee)
        reste = 0
        if loyerApayer>sumLoyer:
            reste = loyerApayer-sumLoyer
        return reste


    # @staticmethod
    # def realInsertion(connexion, idBox, idPerson, mois, annee, montant, date):
    #     moisApayer, anneeApayer = Paiement.getProchainMoisAPayer(connexion, idBox, idPerson)
    #     datePaiement = date if isinstance(date, str) else date.strftime('%Y-%m-%d')
    #     #loyerApayer = Paiement.getResteApayer(connexion, idBox,mois,annee)
    #     loyerApayer = Box.getLoyerBox(connexion, idBox)

    #     try:
    #         if montant >= loyerApayer :
    #             while montant >= loyerApayer:
    #                 reste = Paiement.getResteApayer(connexion, idBox,moisApayer,anneeApayer)
    #                 query = f"INSERT INTO PAIEMENT (idBox, idPerson, mois, annee, montant, datePaiement) VALUES ({idBox}, {idPerson}, {moisApayer}, {anneeApayer}, {reste}, '{datePaiement}')"
    #                 connexion.execute_update(query)
    #                 montant -= reste

    #                 moisApayer, anneeApayer = Paiement.getProchainMoisAPayer(connexion, idBox, idPerson)
    #                 if montant > 0:
    #                     query = f"INSERT INTO PAIEMENT (idBox, idPerson, mois, annee, montant, datePaiement) VALUES ({idBox}, {idPerson}, {moisApayer}, {anneeApayer}, {montant}, '{datePaiement}')"
    #                     connexion.execute_update(query)
    #                 print("Paiement partiel réussi pour le mois suivant")

    #             print("Paiement réussi")
    #         else:
    #             query = f"INSERT INTO PAIEMENT (idBox, idPerson, mois, annee, montant, datePaiement) VALUES ({idBox}, {idPerson}, {moisApayer}, {anneeApayer}, {montant}, '{datePaiement}')"
    #             connexion.execute_update(query)
    #             moisApayer, anneeApayer = Paiement.getProchainMoisAPayer(connexion, idBox, idPerson)
    #             print("Paiement réussi")

    #     except Exception as e:
    #         print(f"Erreur : {e}")

        # @staticmethod
        # def realInsertion(connexion, idBox, idPerson, mois, annee, montant, date):
        #     moisApayer, anneeApayer = Paiement.getProchainMoisAPayer(connexion, idBox, idPerson,mois,annee)
        #     datePaiement = date if isinstance(date, str) else date.strftime('%Y-%m-%d')
        
        #     try:
        #         while montant > 0:
        #             reste = Paiement.getResteApayer(connexion, idBox, moisApayer, anneeApayer)
                
        #             if reste > 0:
        #                 paiement_actuel = min(montant, reste)  
        #                 query = f"INSERT INTO PAIEMENT (idBox, idPerson, mois, annee, montant, datePaiement) VALUES ({idBox}, {idPerson}, {moisApayer}, {anneeApayer}, {paiement_actuel}, '{datePaiement}')"
        #                 connexion.execute_update(query)
                    
        #                 montant -= paiement_actuel  

        #             if montant > 0:
        #                 moisApayer, anneeApayer = Paiement.getProchainMoisAPayer(connexion, idBox, idPerson,mois,annee)

        #         print("Paiement réussi")

        #     except Exception as e:
        #         print(f"Erreur : {e}")

    @staticmethod
    def realInsertion(connexion, idBox, idPerson, mois, annee, montant, date):
        # moisApayer, anneeApayer = mois, annee
        moisApayer, anneeApayer = 1,2024
        datePaiement = date if isinstance(date, str) else date.strftime('%Y-%m-%d')

        try:
            while montant > 0:
                reste = Paiement.getResteApayer(connexion, idBox,idPerson, moisApayer, anneeApayer)

                if reste > 0:
                    paiement_actuel = min(montant, reste)
                    query = f"INSERT INTO PAIEMENT (idBox, idPerson, mois, annee, montant, datePaiement) VALUES ({idBox}, {idPerson}, {moisApayer}, {anneeApayer}, {paiement_actuel}, '{datePaiement}')"
                    connexion.execute_update(query)

                    montant -= paiement_actuel

                if montant > 0:
                    moisApayer += 1
                    if moisApayer > 12:
                        moisApayer = 1
                        anneeApayer += 1

            print("Paiement réussi")

        except Exception as e:
            print(f"Erreur : {e}")



    @staticmethod
    def insertPayement(connexion,idBox,idPerson,mois,annee,montant,date):
        moisApayer,anneeApayer = Paiement.getProchainMoisAPayer(connexion,idBox,idPerson,mois,annee)
        datePaiement = date if isinstance(date, str) else date.strftime('%Y-%m-%d')
        query = f"INSERT INTO PAIEMENT (idBox,idPerson,mois,annee,montant,datePaiement) VALUES ({idBox},{idPerson},{moisApayer},{anneeApayer},{montant},#{datePaiement}#)"
        try:
            connexion.execute_update(query)
            print("paiement reussi")
        except Exception as e:
            print(f"Erreur : {e}")

    @staticmethod
    def sumLoyerMoisAnneeBox(connexion,idBox,mois,annee):
        query = f"SELECT SUM(MONTANT) FROM PAIEMENT WHERE MOIS = {mois} AND ANNEE = {annee} AND IDBOX = {idBox}"
        rows = connexion.execute_query(query)
        total = 0
        for row in rows:
            if row[0] is not None:
                total = row[0]
        return total

    @staticmethod
    def sumLoyerMoisAnneeBoxPerson(connexion,idBox,idPerson,mois,annee):
        query = f"SELECT SUM(MONTANT) FROM PAIEMENT WHERE MOIS = {mois} AND ANNEE = {annee} AND IDBOX = {idBox} AND IDPERSON = {idPerson}"
        rows = connexion.execute_query(query)
        total = 0
        for row in rows:
            if row[0] is not None:
                total = row[0]
        return total

    @staticmethod
    def getBoxPaye(connexion,mois,annee):
        query = f"SELECT IDBOX FROM PAIEMENT WHERE MOIS = {mois} AND ANNEE = {annee}"
        rows = connexion.execute_query(query)
        idBox = []
        for row in rows:
            if row[0] is not None:
                if(Paiement.sumLoyerMoisAnneeBox(connexion,row[0],mois,annee) >= Box.getLoyerBox(connexion,row[0],mois,annee)):
                    idBox.append(row[0])

        return idBox

    @staticmethod
    def getPourcentageNaloa(connexion,idBox,mois,annee):
        print("eto")
        dejaPayer = Paiement.sumLoyerMoisAnneeBox(connexion,idBox,mois,annee)
        loyerApayer = Box.getLoyerBox(connexion,idBox,mois,annee)
        # resultat = (dejaPayer*100) / loyerApayer
        resultat = (dejaPayer*100) / loyerApayer
        return resultat

