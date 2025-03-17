from marche import Marche
from tarif_special import tarif_special

class Box:
    def __init__(self, idBox, idMarche, x, y, width, height,numeroBox):
        self.idBox = idBox
        self.idMarche = idMarche
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.numeroBox = numeroBox

    @staticmethod
    def getSuperficie(width, height):
        return width * height

    @staticmethod
    def insertDette(connexion,idPerson,idBox,montant,mois,annee):
        query = f"INSERT INTO DETTE (IDPERSON,IDBOX,MONTANT,MOIS,ANNEE) VALUES ({idPerson},{idBox},{montant},{mois},{annee})"
        try:
            connexion.execute_update(query)
            print("insert dette reussie")
        except Exception as e:
            print(f"Erreur : {e}")

    # @staticmethod
    # def getPlusAncienDette(connexion, idPerson):
    #     query = f"""
    #         SELECT idBox, montant, mois, annee 
    #         FROM DETTE 
    #         WHERE montant IS NOT NULL AND montant <> 0 AND idPerson = {idPerson} 
    #         ORDER BY annee DESC, mois DESC;
    #     """
    #     rows = connexion.execute_query(query)
    #     for row in rows:
    #         idBox = row[0]
    #         montant = row[1]
    #         mois = row[2]
    #         annee = row[3]
    #     return idBox, montant, mois, annee


    @staticmethod
    def get_all(connexion):
        query = "SELECT * FROM box"
        rows = connexion.execute_query(query)

        boxs = []
        for row in rows:
            idBox = row[0]
            idMarche = row[1]
            idPerson = row[2]
            x = row[3]
            y = row[4]
            width = row[5]
            height = row[6]
            box = Box(idBox, idMarche, idPerson, x, y, width, height)
            boxs.append(box)

        return boxs


    @staticmethod
    def updatePerson(connexion,idBox,idPerson):
        query = f"UPDATE Box SET idPerson = {idPerson} WHERE idBox = {idBox}"
        try:
            connexion.execute_update(query)
            print("update reussie")
        except Exception as e:
            print(f"Erreur : {e}")
    
    @staticmethod
    def manalaPerson(connexion,idBox):
        query = f"UPDATE Box SET idPerson = NULL WHERE idBox = {idBox}"
        try:
            connexion.execute_update(query)
            print("update reussie")
        except Exception as e:
            print(f"Erreur : {e}")

    @staticmethod
    def create(connexion, idMarche, x, y, width, height,numeroBox):
        # idPersonValue = "NULL" if idPerson is None else idPerson
        query = f"INSERT INTO BOX (idMarche, x, y, width, height,numeroBox) VALUES ({idMarche}, {x}, {y}, {width}, {height},{numeroBox})"
        try:
            connexion.execute_update(query)
            print("Insertion Box réussie")
        except Exception as e:
            print(f"Erreur : {e}")

    @staticmethod
    def getIdMarche(connexion, idBox):
        query = f"SELECT idMarche FROM box WHERE idBox = {idBox}"
        rows = connexion.execute_query(query)
        for row in rows:
            idMarche = row[0]
        return idMarche

    @staticmethod
    def getById(connexion, idBox):
        query = f"SELECT * FROM box WHERE idBox = {idBox}"
        rows = connexion.execute_query(query)
        for row in rows:
            idBox = row[0]
            idMarche = row[1]
            x = row[2]
            y = row[3]
            width = row[4]
            height = row[5]
            numeroBox = row[6]
            return Box(idBox, idMarche, x, y, width, height,numeroBox)
        return None  # Retourne None si la Box n'est pas trouvée

    @staticmethod
    def getAllBoxPerson(connexion,idPerson):
        query = f"SELECT * FROM BOX WHERE IDPERSON = {idPerson}"
        rows = connexion.execute_query(query)
        boxes = []
        for row in rows:
            idBox = row[0]
            idMarche = row[1]
            idPerson = row[2]
            x = row[3]
            y = row[4]
            width = row[5]
            height = row[6]
            numeroBox = row[7]
            box = Box(idBox, idMarche, idPerson, x, y, width, height,numeroBox)
            boxes.append(box)
        return boxes

    @staticmethod
    def getLoyerBoxNormal(connexion, idBox):
        box = Box.getById(connexion, idBox)
        if box is None:
            print(f"Aucune Box trouvée pour idBox = {idBox}")
            return None
        
        idMarche = box.idMarche
        loyerApayer = Marche.getLoyerMarche(connexion, idMarche)
        superficie = Box.getSuperficie(box.width, box.height)
        
        aloa = superficie * loyerApayer
        return aloa

    # @staticmethod
    # def getLoyerBox(connexion, idBox,mois,annee):
    #     box = Box.getById(connexion, idBox)
    #     if box is None:
    #         print(f"Aucune Box trouvée pour idBox = {idBox}")
    #         return None
        
    #     idMarche = box.idMarche
    #     loyerApayer = 0
    #     tarifSpe = tarif_special.getTarifSpecialMoisAnnee(connexion,mois,annee)

    #     if tarifSpe == 0:
    #         loyerApayer = Marche.getLoyerMarche(connexion, idMarche)
    #     else:
    #         loyerApayer = tarifSpe
            
    #     superficie = Box.getSuperficie(box.width, box.height)
        
    #     aloa = superficie * loyerApayer
    #     return aloa

    @staticmethod
    def getLoyerBox(connexion, idBox,mois,annee):
        box = Box.getById(connexion, idBox)
        if box is None:
            print(f"Aucune Box trouvée pour idBox = {idBox}")
            return None
        
        idMarche = box.idMarche
        loyerApayer = 0
        tarifSpe = tarif_special.getTarifSpecialMoisAnnee(connexion,mois,annee)

        if tarifSpe == 0:
            loyerApayer = Marche.getLoyerMarche(connexion, idMarche,mois,annee)
        else:
            loyerApayer = tarifSpe
            
        superficie = Box.getSuperficie(box.width, box.height)
        
        aloa = superficie * loyerApayer
        return aloa

    @staticmethod
    def isHisBox(connexion,idBox,idPerson):
        box = Box.getById(connexion,idBox)
        if box.idPerson == idPerson:
            return True
        else:
            return False

    @staticmethod
    def misyOlona(connexion,idBox,mois,annee):
        box = Box.getById(connexion,idBox)
        if box.idPerson is not None:
            return True
        else:
            return False
