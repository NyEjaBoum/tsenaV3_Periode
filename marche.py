
class Marche:
    def __init__(self, idMarche, nomMarche, x, y, width, height):
        self.idMarche = idMarche
        self.nomMarche = nomMarche
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    # @staticmethod
    # def create(connexion, nomMarche, x, y, width, height):
    #     query = f"INSERT INTO MARCHE (nomMarche, x, y, width, height) VALUES ('{nomMarche}', {x}, {y}, {width}, {height})"
    #     try:
    #         connexion.execute_update(query)
    #         print("Insertion réussie")
    #     except Exception as e:
    #         print(f"Erreur d'insertion : {e}")

    @staticmethod
    def isInMarche(connexion,eventX,eventY):
        marches = Marche.get_all(connexion)
        for marche in marches:
            if marche.x <= eventX <= marche.x + marche.width and marche.y <= eventY <=marche.y + marche.height:
                return marche.idMarche
        return None


    @staticmethod
    def create(connexion, nomMarche, x, y, width, height):
        query_insert = f"INSERT INTO MARCHE (nomMarche, x, y, width, height) VALUES ('{nomMarche}', {x}, {y}, {width}, {height})"
    
        try:
            connexion.execute_update(query_insert)  
            query_id = "SELECT MAX(idMarche) FROM MARCHE"
            rows = connexion.execute_query(query_id)
            for row in rows:
                idMarche = row[0]  
        
            print("Insertion réussie, ID:", idMarche)
            return idMarche
    
        except Exception as e:
            print(f"Erreur d'insertion : {e}")
            return None  

    
    @staticmethod
    def get_all(connexion):
        query = "SELECT * FROM MARCHE"
        rows = connexion.execute_query(query)

        marches = []
        for row in rows:
            idMarche = row[0]
            nomMarche = row[1]
            x = row[2]
            y = row[3]
            width = row[4]
            height = row[5]
            marche = Marche(idMarche,nomMarche,x,y,width,height)
            marches.append(marche)

        return marches

    @staticmethod
    def getTarifSpecial(connexion,idMarche,mois,annee):
        query = f"SELECT MONTANT FROM TARIF_SPECIAL WHERE IDMARCHE = {idMarche} AND MOIS = {mois} AND ANNEE = {annee}"
        rows = connexion.execute_query(query)
        for row in rows:
            tarifSpe = row[0]
        return tarifSpe

    @staticmethod
    def getAllBox(connexion, idMarche):
        from box import Box  # Import local pour éviter l'import circulaire
        query = f"SELECT idBox FROM BOX WHERE IDMARCHE = {idMarche}"
        rows = connexion.execute_query(query)
        boxs = []
        for row in rows:
            idBox = row[0]
            box = Box.getById(connexion, idBox)
            boxs.append(box)
        return boxs

    @staticmethod
    def getById(connexion,idMarche):
        query = f"SELECT * FROM marche WHERE idMarche = {idMarche}"
        rows = connexion.execute_query(query)
        for row in rows:
            idMarche = row[0]
            nomMarche = row[1]
            x = row[2]
            y = row[3]
            width = row[4]
            height = row[5]
            return Marche(idMarche, nomMarche, x, y, width, height)
        return None  

    @staticmethod
    def getLoyerMarche(connexion,idMarche):
        query = f"SELECT MONTANT FROM LOYER WHERE IDMARCHE = {idMarche}"
        rows = connexion.execute_query(query)
        for row in rows:
            loyer = row[0]
        return loyer

