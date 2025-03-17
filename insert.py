from box import Box
from location import Location
from marche import Marche
from paiement import Paiement
from personne import Personne
from connexion import Connexion

class Insert:
    def __init__(self):
        pass


    @staticmethod
    def insertDonnees(connexion):
        #marche
        # Marche.create(connexion,"Nosy Be",100,200,40,30)
        # Marche.create(connexion,"Andravoahangy",550,200,50,30)

        # #Box
        Box.create(connexion,1,100,220,2,5,1)
        Box.create(connexion,1,120,220,2,5,2)
        Box.create(connexion,1,140,220,2,5,3)
        Box.create(connexion,1,160,220,2,5,4)
        Box.create(connexion,1,180,220,2,5,5)
        Box.create(connexion,1,200,220,2,5,6)
        Box.create(connexion,1,220,220,2,5,7)
        Box.create(connexion,1,240,220,2,5,8)
        Box.create(connexion,1,260,220,2,5,9)
        Box.create(connexion,1,280,220,2,5,10)
        Box.create(connexion,1,300,220,2,5,11)
        Box.create(connexion,1,320,220,2,5,12)
        Box.create(connexion,1,340,220,2,5,13)
        Box.create(connexion,1,360,220,2,5,14)
        Box.create(connexion,1,380,220,2,5,15)
        Box.create(connexion,1,400,220,2,5,16)
        Box.create(connexion,1,420,220,2,5,17)
        Box.create(connexion,1,440,220,2,5,18)
        Box.create(connexion,1,460,220,2,5,19)
        Box.create(connexion,1,480,220,2,5,20)

        Box.create(connexion,2,550,220,3,5,1)
        Box.create(connexion,2,570,220,3,5,2)
        Box.create(connexion,2,590,220,3,5,3)
        Box.create(connexion,2,610,220,3,5,4)
        Box.create(connexion,2,630,220,3,5,5)
        Box.create(connexion,2,650,220,3,5,6)
        Box.create(connexion,2,670,220,3,5,7)
        Box.create(connexion,2,710,220,3,5,8)
        Box.create(connexion,2,730,220,3,5,9)
        Box.create(connexion,2,750,220,3,5,10)
        Box.create(connexion,2,770,220,3,5,11)
        Box.create(connexion,2,810,220,3,5,12)
        Box.create(connexion,2,830,220,3,5,13)
        Box.create(connexion,2,860,220,3,5,14)
        Box.create(connexion,2,880,220,3,5,15)


        #location nosy be
        Location.louerBox(connexion,1,1,"2022-01-01","2022-12-31")
        Location.louerBox(connexion,2,1,"2022-01-01","2022-12-31")
        Location.louerBox(connexion,3,1,"2022-01-01","2022-12-31")
        Location.louerBox(connexion,4,1,"2022-01-01","2022-12-31")
        Location.louerBox(connexion,5,1,"2022-01-01","2022-12-31")

        Location.louerBox(connexion,6,2,"2022-01-01",None)
        Location.louerBox(connexion,7,2,"2022-01-01",None)
        Location.louerBox(connexion,8,2,"2022-01-01",None)
        Location.louerBox(connexion,9,2,"2022-01-01",None)
        Location.louerBox(connexion,10,2,"2022-01-01",None)

        Location.louerBox(connexion,11,3,"2022-01-01",None)
        Location.louerBox(connexion,12,3,"2022-01-01",None)
        Location.louerBox(connexion,13,3,"2022-01-01",None)
        Location.louerBox(connexion,14,3,"2022-01-01",None)
        Location.louerBox(connexion,15,3,"2022-01-01",None)

        Location.louerBox(connexion,16,4,"2022-01-01",None)
        Location.louerBox(connexion,17,4,"2022-01-01",None)
        Location.louerBox(connexion,18,4,"2022-01-01",None)
        Location.louerBox(connexion,19,4,"2022-01-01",None)
        Location.louerBox(connexion,20,4,"2022-01-01",None)

        #location andravoanhgy
        Location.louerBox(connexion,21,4,"2022-01-01","2022-12-31")
        Location.louerBox(connexion,22,4,"2022-01-01","2022-12-31")
        Location.louerBox(connexion,23,4,"2022-01-01","2022-12-31")
        Location.louerBox(connexion,24,4,"2022-01-01","2022-12-31")
        Location.louerBox(connexion,25,4,"2022-01-01","2022-12-31")

        Location.louerBox(connexion,26,4,"2022-01-01",None)
        Location.louerBox(connexion,27,4,"2022-01-01",None)
        Location.louerBox(connexion,28,4,"2022-01-01",None)
        Location.louerBox(connexion,29,4,"2022-01-01",None)
        Location.louerBox(connexion,30,4,"2022-01-01",None)

        Location.louerBox(connexion,31,5,"2022-01-01","2022-12-31")
        Location.louerBox(connexion,32,5,"2022-01-01","2022-12-31")
        Location.louerBox(connexion,33,5,"2022-01-01","2022-12-31")
        Location.louerBox(connexion,34,5,"2022-01-01","2022-12-31")
        Location.louerBox(connexion,35,5,"2022-01-01","2022-12-31")

        #changement nosy be
        Location.louerBox(connexion,1,6,"2023-01-01",None)
        Location.louerBox(connexion,2,6,"2023-01-01",None)
        Location.louerBox(connexion,3,6,"2023-01-01",None)
        Location.louerBox(connexion,4,6,"2023-01-01",None)
        Location.louerBox(connexion,5,6,"2023-01-01",None)

        #changement andrav
        Location.louerBox(connexion,21,7,"2023-01-01",None)
        Location.louerBox(connexion,22,7,"2023-01-01",None)
        Location.louerBox(connexion,23,7,"2023-01-01",None)
        Location.louerBox(connexion,24,7,"2023-01-01",None)
        Location.louerBox(connexion,25,7,"2023-01-01",None)

        Location.louerBox(connexion,31,8,"2023-01-01",None)
        Location.louerBox(connexion,32,8,"2023-01-01",None)
        Location.louerBox(connexion,33,8,"2023-01-01",None)
        Location.louerBox(connexion,34,8,"2023-01-01",None)
        Location.louerBox(connexion,35,8,"2023-01-01",None)

        #Paiement 2022    
        Paiement.realInsertion(connexion,1,1,12,2022,4000000,"2022-12-12")
        Paiement.realInsertion(connexion,1,2,12,2022,6000000,"2022-12-12")
        Paiement.realInsertion(connexion,1,3,12,2022,6000000,"2022-12-12")
        Paiement.realInsertion(connexion,1,4,12,2022,23600000,"2022-12-12")
        Paiement.realInsertion(connexion,1,5,12,2022,11700000,"2022-12-12")

        Paiement.realInsertion(connexion,1,6,1,2023,400000,"2023-01-01")
        Paiement.realInsertion(connexion,1,2,1,2023,600000,"2023-01-01")
        Paiement.realInsertion(connexion,1,3,1,2023,600000,"2023-01-01")
        Paiement.realInsertion(connexion,1,4,1,2023,1050000,"2023-01-01")
        Paiement.realInsertion(connexion,1,7,1,2023,1050000,"2023-01-01")
        Paiement.realInsertion(connexion,1,8,1,2023,1050000,"2023-01-01")





        