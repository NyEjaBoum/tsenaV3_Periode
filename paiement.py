from box import Box
from marche import Marche
from datetime import datetime
from location import Location
from personne import Personne

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

    # @staticmethod
    # def getResteApayer(connexion,idBox,idPerson,mois,annee):
    #     sumLoyer = Paiement.sumLoyerMoisAnneeBoxPerson(connexion,idBox,idPerson,mois,annee)
    #     loyerApayer = Box.getLoyerBox(connexion,idBox,mois,annee)
    #     reste = 0
    #     if loyerApayer>sumLoyer:
    #         reste = loyerApayer-sumLoyer
    #     return reste

    # @staticmethod
    # def getResteApayer(connexion,idBox,idPerson,mois,annee):
    #     sumLoyer = Paiement.sumLoyerMoisAnneeBoxPerson(connexion,idBox,idPerson,mois,annee)
    #     # if Box.isHisBox(connexion,idBox,idPerson):
    #     loyerApayer = Box.getLoyerBox(connexion,idBox,mois,annee)
    #     reste = 0
    #     if loyerApayer>sumLoyer:
    #         reste = loyerApayer-sumLoyer
    #     # else:
    #     #     reste = 0
    #     return reste


    @staticmethod
    def getResteApayer(connexion, idBox, idPerson, mois, annee):
        # Vérifier d'abord si un contrat actif existe pour cette période
        contrat = Paiement.get_active_contract(connexion, idBox, idPerson, mois, annee)
        
        if contrat:  # Si un contrat actif existe
            sumLoyer = Paiement.sumLoyerMoisAnneeBoxPerson(connexion, idBox, idPerson, mois, annee)
            loyerApayer = Box.getLoyerBox(connexion, idBox, mois, annee)
            reste = 0
            if loyerApayer > sumLoyer:
                reste = loyerApayer - sumLoyer
            return reste
        return 0  # Pas de contrat actif, donc rien à payer

    @staticmethod
    def sumNaloanyPersonByDate(connexion,idPerson,mois,annee):
        query = f"SELECT SUM(MONTANT) FROM PAIEMENT WHERE IDPERSON = {idPerson} AND YEAR(DATEPAIEMENT) * 12 + MONTH(DATEPAIEMENT) <= {annee} *12 + {mois}"
        rows = connexion.execute_query(query)
        total = 0
        for row in rows:
            if row[0] is not None:
                total = row[0]
        return total


    @staticmethod
    def sommeTokonyNaloanyByDate(connexion, idPerson, mois, annee):
        allContrat = Location.getAllContratPerson(connexion, idPerson)
        maxDate = Location.getMaxDateFinContratPerson(connexion, idPerson)

        if maxDate:
            maxDate_mois = maxDate.month
            maxDate_annee = maxDate.year
        else:
            maxDate_mois = mois
            maxDate_annee = annee

        maxDateT = maxDate_annee * 12 + maxDate_mois
        moisT = annee * 12 + mois
        # print(f"max date mois {maxDate_mois} annee {maxDate_annee} total { maxDateT}")
        # print(f"date input date mois {mois} annee {annee} total {moisT}")
        # moisTRef = min(maxDateT, moisT)
        # print(f"ty no alainy {moisTRef} ")
        moisTRef = moisT
        total_dettes = 0.0

        for contrat in allContrat:
            moisDeb = contrat.date.month
            anneeDeb = contrat.date.year
            moisDebT = anneeDeb * 12 + moisDeb

            while moisDebT <= moisTRef:
                misyContrat = Paiement.get_active_contract(connexion,contrat.idBox,idPerson,moisDeb,anneeDeb)
                if misyContrat:
                    reste = Box.getLoyerBox(connexion, contrat.idBox,moisDeb, anneeDeb)
                else:
                    reste = 0
                # print(f"Reste pour idBox={contrat.idBox}, mois={moisDeb}, année={anneeDeb} : {reste}")
                total_dettes += reste

                moisDeb += 1
                if moisDeb > 12:
                    moisDeb = 1
                    anneeDeb += 1
                moisDebT = anneeDeb * 12 + moisDeb

        print(f"Tokony naloany pour idPerson={idPerson} jusqu'à {mois}/{annee} : {total_dettes}")
        return total_dettes

    @staticmethod
    def sommeDetteTokonyNaloany(connexion, idPerson, mois, annee):
        efaVoaloa = Paiement.sumNaloanyPersonByDate(connexion,idPerson,mois,annee)
        tokonyAloa = Paiement.sommeTokonyNaloanyByDate(connexion,idPerson,mois,annee)
        # print(f"ty efa voaloa {efaVoaloa}")
        # print(f"ty tokony aloa {tokonyAloa}")

        totalDette = tokonyAloa - efaVoaloa
        return totalDette


    @staticmethod
    def get_active_contract(connexion, idBox, idPerson, moisApayer, anneeApayer):
        """Récupère les informations d'un contrat actif pour une période donnée."""
        query_contrat = f"""
            SELECT MONTH(dateDebut), YEAR(dateDebut), MONTH(dateFin), YEAR(dateFin)
            FROM LOCATION 
            WHERE idBox = {idBox} AND idPerson = {idPerson}
            AND (YEAR(dateDebut) * 12 + MONTH(dateDebut)) <= ({anneeApayer} * 12 + {moisApayer})
            AND (dateFin IS NULL OR (YEAR(dateFin) * 12 + MONTH(dateFin)) >= ({anneeApayer} * 12 + {moisApayer}))
        """
        contrat = connexion.execute_query(query_contrat)
        if contrat:
            return contrat[0]  # Retourne mois_debut, annee_debut, mois_fin, annee_fin
        return None

    @staticmethod
    def getAllBoxApayerPerson(connexion,idPerson):
        allBoxPerson = Box.getAllBoxPerson(connexion,idPerson)
        boxApayer = []
        for box in allBoxPerson:
            mois,annee = Location.getDebutContrat(connexion,box.idBox,idPerson)
            reste = Paiement.getResteApayer(connexion,box.idBox,idPerson,mois,annee)
            if reste > 0:
                boxApayer.append(box.idBox)
        return boxApayer


    @staticmethod
    def checkFinContrat(connexion, idBox, idPerson, moisApayer, anneeApayer, mois_fin, annee_fin):
            """Vérifie si la période actuelle dépasse la fin du contrat."""
            mois_fin_total = (annee_fin * 12 + mois_fin) if mois_fin and annee_fin else None
            mois_courant_total = (anneeApayer * 12 + moisApayer)
            print(f"mois courant annee courant total {moisApayer} , {anneeApayer},{mois_courant_total}")
            print(f"mois fin annee fin total {mois_fin} , {annee_fin},{mois_fin_total}")
            if mois_fin_total and mois_courant_total > mois_fin_total:
                print(f"Fin de contrat atteinte à {mois_fin}/{annee_fin}, arrêt des paiements pour ce contrat")
                return True
            return False

    @staticmethod
    def getNextContrat(connexion,idPerson,mois_fin,annee_fin):
        """Recherche le prochain contrat après la fin du contrat actuel."""
        query_next_contract = f"""
            SELECT TOP 1 MONTH(dateDebut), YEAR(dateDebut)
            FROM LOCATION 
            WHERE idPerson = {idPerson} 
            AND dateDebut > #{annee_fin}-{mois_fin:02d}-01#
            ORDER BY dateDebut ASC
        """
        rows = connexion.execute_query(query_next_contract)
        if rows:
            moisApayer, anneeApayer = rows[0]
            print(f"Nouveau contrat détecté à partir de {moisApayer}/{anneeApayer}")
            return moisApayer, anneeApayer
        print("Aucun nouveau contrat trouvé, arrêt")
        return None, None

    @staticmethod
    def get_active_contract(connexion, idBox, idPerson, moisApayer, anneeApayer):
        """Récupère les informations d'un contrat actif pour une période donnée."""
        query_contrat = f"""
            SELECT MONTH(dateDebut), YEAR(dateDebut), MONTH(dateFin), YEAR(dateFin)
            FROM LOCATION 
            WHERE idBox = {idBox} AND idPerson = {idPerson}
            AND (YEAR(dateDebut) * 12 + MONTH(dateDebut)) <= ({anneeApayer} * 12 + {moisApayer})
            AND (dateFin IS NULL OR (YEAR(dateFin) * 12 + MONTH(dateFin)) >= ({anneeApayer} * 12 + {moisApayer}))
        """
        contrat = connexion.execute_query(query_contrat)
        if contrat:
            return contrat[0]  # Retourne mois_debut, annee_debut, mois_fin, annee_fin
        return None

    @staticmethod
    def realInsertion(connexion, idBox, idPerson, mois, annee, montant, date):
        try:
            datePaiement = date if isinstance(date, str) else date.strftime('%Y-%m-%d')
            montant_restant = montant
            current_idBox = idBox

            while(montant_restant > 0):
                dettePlusAncienne = Personne.getPlusAncienDette(connexion, idPerson)
                if not dettePlusAncienne:
                    print("Aucune dette à payer")
                    break
                idBoxAncien, montant_dette, moisApayer, anneeApayer = dettePlusAncienne
                print(f"Dette la plus ancienne : idBox={idBoxAncien}, mois={moisApayer}, année={anneeApayer}, montant_dette={montant_dette}")
                
                # Vérifier les autres dettes pour le même mois et année
                query_check_other_debts = f"""
                SELECT DETTE.idBox, DETTE.montant, BOX.numeroBox 
                FROM DETTE, BOX 
                WHERE DETTE.idBox = BOX.idBox 
                AND DETTE.idPerson = {idPerson}
                AND DETTE.mois = {moisApayer}
                AND DETTE.annee = {anneeApayer}
                AND DETTE.montant > 0 
                ORDER BY BOX.numeroBox ASC
                """
                other_debts = connexion.execute_query(query_check_other_debts)

                if other_debts and len(other_debts) > 0:
                    # S'il y a plusieurs dettes, prendre celle avec le numeroBox le plus bas qui a encore un reste à payer
                    for debt in other_debts:
                        idBox_temp = debt[0]
                        montant_temp = debt[1]
                        numero_box = debt[2]
                        reste_idBox = Paiement.getResteApayer(connexion, idBox_temp, idPerson, moisApayer, anneeApayer)
                        if reste_idBox is not None and reste_idBox > 0:
                            current_idBox = idBox_temp
                            print(f"Priorisation de idBox={current_idBox} (Box n°{numero_box}) pour mois={moisApayer}, année={anneeApayer}")
                            break
                    else:
                        # Si aucune dette n'a de reste à payer, prendre la box avec le plus petit numéro
                        current_idBox = other_debts[0][0]
                        print(f"Choix par défaut de idBox={current_idBox} pour mois={moisApayer}, année={anneeApayer}")
                else:
                    current_idBox = idBoxAncien or idBox
                    print(f"Une seule dette ou aucune autre dette, utilisation de idBox={current_idBox}")

                print(f"Box courante sélectionnée : idBox={current_idBox}")

                # Calculer le reste à payer
                reste = Paiement.getResteApayer(connexion, current_idBox, idPerson, moisApayer, anneeApayer) or 0
                print(f"Reste à payer pour idBox={current_idBox}, mois={moisApayer}, année={anneeApayer} : {reste}")

                # Vérifier l'existence d'un contrat actif avec la nouvelle fonction
                contrat = Paiement.get_active_contract(connexion, current_idBox, idPerson, moisApayer, anneeApayer)
                if not contrat:
                    print(f"Aucun contrat actif pour idBox={current_idBox}, mois={moisApayer}, année={anneeApayer}, dette ignorée")
                    query_delete_dette = f"DELETE FROM DETTE WHERE idPerson = {idPerson} AND idBox = {current_idBox} AND mois = {moisApayer} AND annee = {anneeApayer}"
                    connexion.execute_update(query_delete_dette)
                    continue

                mois_debut, annee_debut, mois_fin, annee_fin = contrat

                if(reste > 0):
                    #mijery fin contrat
                    if Paiement.checkFinContrat(connexion, current_idBox, idPerson, moisApayer, anneeApayer, mois_fin, annee_fin):
                        moisApayer, anneeApayer = Paiement.getNextContrat(connexion, idPerson, mois_fin, annee_fin)
                        if moisApayer is None or anneeApayer is None:
                            break
                        continue

                    #payement
                    paiement_actuel = min(montant_restant, reste)
                    print(f"Paiement actuel : {paiement_actuel}")
                    query_paiement = f"INSERT INTO PAIEMENT (idBox, idPerson, mois, annee, montant, datePaiement) VALUES ({current_idBox}, {idPerson}, {moisApayer}, {anneeApayer}, {paiement_actuel}, '{datePaiement}')"
                    connexion.execute_update(query_paiement)
                    print(f"Paiement de {paiement_actuel} inséré pour idBox={current_idBox}, mois={moisApayer}, année={anneeApayer}")

                    montant_restant -= paiement_actuel
                    print(f"Montant restant après paiement : {montant_restant}")

                    # Mettre à jour la dette
                    nouveau_reste = Paiement.getResteApayer(connexion, current_idBox, idPerson, moisApayer, anneeApayer) or 0
                    print(f"Nouveau reste après paiement : {nouveau_reste}")
                    Personne.updateDette(connexion, current_idBox, idPerson, moisApayer, anneeApayer, nouveau_reste)

                moisApayer += 1
                if moisApayer > 12:
                    moisApayer = 1
                    anneeApayer += 1

                #mijery raha midepasse fin contrat ny insertion 
                if Paiement.checkFinContrat(connexion, current_idBox, idPerson, moisApayer, anneeApayer, mois_fin, annee_fin):
                    moisApayer, anneeApayer = Paiement.getNextContrat(connexion, idPerson, mois_fin, annee_fin)
                    if moisApayer is None or anneeApayer is None:
                        continue
                    print(f"Nouveau contrat trouvé : mois={moisApayer}, année={anneeApayer}")
                print(f"Passage au mois suivant pour idBox={current_idBox} : {moisApayer}/{anneeApayer}")
                montant_dette_suivante = Paiement.getResteApayer(connexion, current_idBox, idPerson, moisApayer, anneeApayer) or 0
                print(f"Reste à payer pour le nouveau mois {moisApayer}/{anneeApayer} : {montant_dette_suivante}")

                if montant_dette_suivante >= 0:
                    query_nouvelle_dette = f"INSERT INTO DETTE (idBox, idPerson, mois, annee, montant) VALUES ({current_idBox}, {idPerson}, {moisApayer}, {anneeApayer}, {montant_dette_suivante})"
                    connexion.execute_update(query_nouvelle_dette)
                    print(f"Nouvelle dette de {montant_dette_suivante} insérée pour idBox={current_idBox}, mois={moisApayer}, année={anneeApayer}")
                else:
                    print(f"Aucune dette à insérer pour idBox={current_idBox}, mois={moisApayer}, année={anneeApayer}")

            print("Paiement réussi")
            return True

        except Exception as e:
            print(f"Erreur : {e}")
            return False

            
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
    def getPourcentageNaloa(connexion,idBox,moisV,anneeV):
        print("eto")
        mois = int(moisV)
        annee = int(anneeV)
        dejaPayer = Paiement.sumLoyerMoisAnneeBox(connexion,idBox,mois,annee)
        loyerApayer = Box.getLoyerBox(connexion,idBox,mois,annee)
        # resultat = (dejaPayer*100) / loyerApayer
        resultat = (dejaPayer*100) / loyerApayer
        return resultat


        

