from marche import Marche
from tarif_special import tarif_special

class Box:
    def __init__(self, idBox, idMarche, idPerson, x, y, width, height):
        self.idBox = idBox
        self.idPerson = idPerson
        self.idMarche = idMarche
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    @staticmethod
    def getSuperficie(width, height):
        return width * height

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
    def create(connexion, idPerson, idMarche, x, y, width, height):
        idPersonValue = "NULL" if idPerson is None else idPerson
        query = f"INSERT INTO BOX (idMarche, idPerson, x, y, width, height) VALUES ({idMarche}, {idPersonValue}, {x}, {y}, {width}, {height})"
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
            idPerson = row[2]
            x = row[3]
            y = row[4]
            width = row[5]
            height = row[6]
            return Box(idBox, idMarche, idPerson, x, y, width, height)
        return None  # Retourne None si la Box n'est pas trouvée

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
            loyerApayer = Marche.getLoyerMarche(connexion, idMarche)
        else:
            loyerApayer = tarifSpe
            
        superficie = Box.getSuperficie(box.width, box.height)
        
        aloa = superficie * loyerApayer
        return aloa
