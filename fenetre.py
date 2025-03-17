import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from tkinter import messagebox
from marche import Marche
from box import Box
from paiement import Paiement
from loyer import Loyer
from datetime import datetime
from location import Location

class Fenetre:
    def __init__(self, dim, title, connexion):
        self.root = tk.Tk()
        self.root.geometry(dim)
        self.root.title(title)
        self.connexion = connexion

        # Création du canvas pour dessiner les marchés et les boxes
        self.canvas = tk.Canvas(self.root, width=1000, height=650, bg="white")
        self.canvas.place(x=20, y=20)  # Décale de 20px à gauche et en bas

        self.frame = tk.Frame(self.root)
        self.frame.pack(pady=10)
        self.echelle = 10

        self.last_x = None  
        self.last_y = None  
        self.last_idMarche = None

        self.canvas.bind("<Button-1>", self.cliquer)

        self.afficher_formulaire_moisAnnee()
        self.afficher_marches()
        self.afficher_boxes()
        self.creer_boutons_ajout()

    def cliquer(self, event):
        self.last_x, self.last_y = event.x, event.y  
        print(f"Clique détecté : x={self.last_x}, y={self.last_y}")
        idMarche = Marche.isInMarche(self.connexion, self.last_x, self.last_y)
        if idMarche is not None:
            self.last_idMarche = idMarche
            self.ajoutBoxFormulaire()
            print(self.last_idMarche)
        else:
            self.ajoutMarcheFormulaire()
            print("ajout de marche")

    def afficher(self):
        self.root.mainloop()

    def afficher_formulaire_moisAnnee(self):
        self.frame = tk.Frame(self.root)
        self.frame.place(x=1100, y=400, width=700, height=100)
    
        tk.Label(self.frame, text="Mois").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.moisVerification = tk.Entry(self.frame)
        self.moisVerification.grid(row=0, column=1, padx=5, pady=5)
    
        tk.Label(self.frame, text="Annee").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.anneeVerification = tk.Entry(self.frame)
        self.anneeVerification.grid(row=1, column=1, padx=5, pady=5)
    
        self.btnVerifier = tk.Button(self.frame, text="Vérifier", command=self.update_box_colors)
        self.btnVerifier.grid(row=2, column=0, columnspan=2, pady=10)

    def payement(self):
        idBox = int(self.idBox.get())
        idPerson = int(self.id_personne.get())
        mois_srt = self.moisPayena.get().strip() 
        annee_srt = self.anneePayena.get().strip() 

        mois = None if not mois_srt else int(mois_srt)
        annee = None if not annee_srt else int(annee_srt)

        montant = int(self.montant.get())
        date = str(self.datePaiement.get())

        confirmation = messagebox.askyesno("Confirmation", "Voulez-vous vraiment valider ce paiement ?")
    
        if confirmation:
            Paiement.realInsertion(self.connexion, idBox, idPerson, mois, annee, montant, date)
            messagebox.showinfo("Succès", "Le paiement a été effectué avec succès.")
        else:
            messagebox.showinfo("Annulation", "Le paiement a été annulé.")
        
    def afficher_marches(self):
        marches = Marche.get_all(self.connexion)
        for marche in marches:
            self.canvas.create_rectangle(marche.x, marche.y,
                                         marche.x + marche.width * self.echelle, marche.y + marche.height * self.echelle,
                                         outline="black", fill="lightgray")
            self.canvas.create_text(marche.x + marche.width/2, marche.y + marche.height/2, 
                                    text=marche.nomMarche, fill="black")
            info_text = f"x:{marche.x}, y:{marche.y}\nw:{marche.width}, h:{marche.height}"
            self.canvas.create_text(
                marche.x + 10, marche.y - 30,
                text=info_text, fill="navy", anchor="nw", font=("Arial", 8)
            )

    def get_box_payer(self):
        try:
            mois = int(self.moisVerification.get())
            annee = int(self.anneeVerification.get())
            return Paiement.getBoxPaye(self.connexion, mois, annee)
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer des valeurs numériques valides pour le mois et l'année")
            return []
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur s'est produite: {str(e)}")
            return []

    def update_box_colors(self):
        self.canvas.delete("box")
        self.afficher_boxes()

    def afficher_boxes(self):
        marches = Marche.get_all(self.connexion)
        
        if self.moisVerification.get() and self.anneeVerification.get():
            boxAlreadyPayed = self.get_box_payer()
        else:
            boxAlreadyPayed = []

        for marche in marches:
            boxes = Marche.getAllBox(self.connexion, marche.idMarche)
            for box in boxes:
                width_scaled = box.width * self.echelle  
                
                if self.moisVerification.get() and self.anneeVerification.get():
                    pourcentage = Paiement.getPourcentageNaloa(self.connexion, box.idBox, self.moisVerification.get(), self.anneeVerification.get())
                    print(f" payee pourcent {pourcentage}")
                    paid_width = (pourcentage / 100) * width_scaled  # Partie payée en vert
                    
                    # Vérifier si le box est loué pour le mois et l'année spécifiés
                    if Location.misyOlonaVe(self.connexion, box.idBox, self.moisVerification.get(), self.anneeVerification.get()):
                        # Si le box est loué, afficher vert et rouge selon le paiement
                        self.canvas.create_rectangle(
                            box.x, box.y,
                            box.x + paid_width, box.y + box.height * self.echelle,
                            outline="black", fill="green"
                        )
                        self.canvas.create_rectangle(
                            box.x + paid_width, box.y,
                            box.x + width_scaled, box.y + box.height * self.echelle,
                            outline="black", fill="red"
                        )
                        print(f"pas gris {box.idBox} mois {self.moisVerification.get()} annee {self.anneeVerification.get()}")

                    else:
                        # Si le box n'est pas loué, le mettre en gris
                        self.canvas.create_rectangle(
                            box.x, box.y,
                            box.x + width_scaled, box.y + box.height * self.echelle,
                            outline="black", fill="gray"
                        )
                        print(f"gris {box.idBox} mois {self.moisVerification.get()} annee {self.anneeVerification.get()}")
                else:
                    # Si aucun mois ou année n'est spécifié, afficher en rouge par défaut
                    color = "red"
                    self.canvas.create_rectangle(
                        box.x, box.y,
                        box.x + width_scaled, box.y + box.height * self.echelle,
                        outline="black", fill=color
                    )

                info_text = f"id:{box.idBox}"
                self.canvas.create_text(
                    box.x + 10, box.y,
                    text=info_text,
                    fill="navy",
                    anchor="nw",
                    font=("Arial", 8)
                )

    def creer_formulaire(self):
        self.formPayement = tk.Toplevel(self.root)
        self.formPayement.title("Formulaire de Paiement du Box")
        self.formPayement.geometry("400x400")

        tk.Label(self.formPayement, text="Identifiant Personne:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.id_personne = tk.Entry(self.formPayement)
        self.id_personne.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.formPayement, text="Sélection du marché:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        marches = Marche.get_all(self.connexion)
        marche_noms = [marche.nomMarche for marche in marches]
        self.var_marche = tk.StringVar()
        self.idMarche = ttk.Combobox(self.formPayement, textvariable=self.var_marche, values=marche_noms)
        self.idMarche.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.formPayement, text="idBox:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.idBox = tk.Entry(self.formPayement)
        self.idBox.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(self.formPayement, text="Mois:").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.moisPayena = tk.Entry(self.formPayement)
        self.moisPayena.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(self.formPayement, text="Année:").grid(row=4, column=0, sticky="w", padx=5, pady=5)
        self.anneePayena = tk.Entry(self.formPayement)
        self.anneePayena.grid(row=4, column=1, padx=5, pady=5)

        tk.Label(self.formPayement, text="Montant:").grid(row=5, column=0, sticky="w", padx=5, pady=5)
        self.montant = tk.Entry(self.formPayement)
        self.montant.grid(row=5, column=1, padx=5, pady=5)

        tk.Label(self.formPayement, text="Date de paiement:").grid(row=6, column=0, sticky="w", padx=5, pady=5)
        self.datePaiement = DateEntry(self.formPayement, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        self.datePaiement.grid(row=6, column=1, padx=5, pady=5)

        self.btnVerifier = tk.Button(self.formPayement, text="Payer", command=self.payement)
        self.btnVerifier.grid(row=7, column=0, columnspan=2, pady=10)

    # Nouveau formulaire pour louer un box
    def louerBoxFormulaire(self):
        self.louerWindow = tk.Toplevel(self.root)
        self.louerWindow.title("Formulaire de Location de Box")
        self.louerWindow.geometry("400x300")

        tk.Label(self.louerWindow, text="idBox:").pack(pady=5)
        self.louerIdBoxEntry = tk.Entry(self.louerWindow)
        self.louerIdBoxEntry.pack(pady=5)

        tk.Label(self.louerWindow, text="Identifiant Personne:").pack(pady=5)
        self.louerIdPersonEntry = tk.Entry(self.louerWindow)
        self.louerIdPersonEntry.pack(pady=5)

        tk.Label(self.louerWindow, text="Date de début de location:").pack(pady=5)
        self.louerDateEntry = DateEntry(self.louerWindow, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        self.louerDateEntry.pack(pady=5)

        tk.Button(self.louerWindow, text="Louer", command=self.louerBoxAction).pack(pady=10)

    def louerBoxAction(self):
        try:
            idBox = int(self.louerIdBoxEntry.get())
            idPerson = int(self.louerIdPersonEntry.get())
            date_str = self.louerDateEntry.get()

            confirmation = messagebox.askyesno("Confirmation", "Voulez-vous vraiment louer ce box ?")
            if confirmation:
                Location.louerBox(self.connexion, idBox, idPerson, date_str)
                messagebox.showinfo("Succès", "Box loué avec succès!")
                # self.louerWindow.destroy()
                self.canvas.delete("all")
                self.afficher_marches()
                self.afficher_boxes()
            else:
                messagebox.showinfo("Annulation", "La location a été annulée.")
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer des valeurs numériques valides pour idBox et idPerson.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur s'est produite: {str(e)}")

    # Nouveau formulaire pour quitter un box
    def quitterBoxFormulaire(self):
        self.quitterWindow = tk.Toplevel(self.root)
        self.quitterWindow.title("Formulaire de Délocation de Box")
        self.quitterWindow.geometry("400x300")

        tk.Label(self.quitterWindow, text="idBox:").pack(pady=5)
        self.quitterIdBoxEntry = tk.Entry(self.quitterWindow)
        self.quitterIdBoxEntry.pack(pady=5)

        tk.Label(self.quitterWindow, text="Identifiant Personne:").pack(pady=5)
        self.quitterIdPersonEntry = tk.Entry(self.quitterWindow)
        self.quitterIdPersonEntry.pack(pady=5)

        tk.Label(self.quitterWindow, text="Date de fin de location:").pack(pady=5)
        self.quitterDateEntry = DateEntry(self.quitterWindow, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        self.quitterDateEntry.pack(pady=5)

        tk.Button(self.quitterWindow, text="Quitter", command=self.quitterBoxAction).pack(pady=10)

    def quitterBoxAction(self):
        try:
            idBox = int(self.quitterIdBoxEntry.get())
            idPerson = int(self.quitterIdPersonEntry.get())
            date_str = self.quitterDateEntry.get()

            confirmation = messagebox.askyesno("Confirmation", "Voulez-vous vraiment quitter ce box ?")
            if confirmation:
                Location.quitterBox(self.connexion, idBox, idPerson, date_str)
                messagebox.showinfo("Succès", "Box quitté avec succès!")
                # self.quitterWindow.destroy()
                self.canvas.delete("all")
                self.afficher_marches()
                self.afficher_boxes()
            else:
                messagebox.showinfo("Annulation", "La délocation a été annulée.")
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer des valeurs numériques valides pour idBox et idPerson.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur s'est produite: {str(e)}")

    def ajoutMarcheFormulaire(self):
        self.marcheWindow = tk.Toplevel(self.root)
        self.marcheWindow.title("Ajout de Marché")
        self.marcheWindow.geometry("400x400")

        tk.Label(self.marcheWindow, text="Nom du marché:").pack(pady=5)
        self.nomMarcheEntry = tk.Entry(self.marcheWindow)
        self.nomMarcheEntry.pack(pady=5)

        tk.Label(self.marcheWindow, text="Loyer:").pack(pady=5)
        self.loyerEntry = tk.Entry(self.marcheWindow)
        self.loyerEntry.pack(pady=5)

        tk.Label(self.marcheWindow, text="X:").pack(pady=5)
        self.xEntry = tk.Entry(self.marcheWindow)
        self.xEntry.pack(pady=5)
        if self.last_x is not None:
            self.xEntry.insert(0, str(self.last_x))

        tk.Label(self.marcheWindow, text="Y:").pack(pady=5)
        self.yEntry = tk.Entry(self.marcheWindow)
        self.yEntry.pack(pady=5)
        if self.last_y is not None:
            self.yEntry.insert(0, str(self.last_y))

        tk.Label(self.marcheWindow, text="width:").pack(pady=5)
        self.widthEntry = tk.Entry(self.marcheWindow)
        self.widthEntry.pack(pady=5)

        tk.Label(self.marcheWindow, text="height:").pack(pady=5)
        self.heightEntry = tk.Entry(self.marcheWindow)
        self.heightEntry.pack(pady=5)

        tk.Button(self.marcheWindow, text="Ajouter", command=self.ajouterMarche).pack(pady=10)

    def ajouterMarche(self):
        nom = self.nomMarcheEntry.get()
        x = int(self.xEntry.get())
        y = int(self.yEntry.get())
        width = int(self.widthEntry.get())
        height = int(self.heightEntry.get())
        montantLoyer = int(self.loyerEntry.get())

        idMarche = Marche.create(self.connexion, nom, x, y, width, height)
        Loyer.create(self.connexion, idMarche, montantLoyer)

        messagebox.showinfo("Succès", "Marché ajouté avec succès!")
        self.marcheWindow.destroy()
        self.canvas.delete("all")
        self.afficher_marches()
        self.afficher_boxes()

    def ajoutBoxFormulaire(self):
        self.boxWindow = tk.Toplevel(self.root)
        self.boxWindow.title("Ajout de Box")
        self.boxWindow.geometry("400x400")

        tk.Label(self.boxWindow, text="ID Marché:").pack(pady=5)
        self.idMarcheEntry = tk.Entry(self.boxWindow)
        self.idMarcheEntry.pack(pady=5)
        if self.last_idMarche is not None:
            self.idMarcheEntry.insert(0, str(self.last_idMarche))

        tk.Label(self.boxWindow, text="Id Person:").pack(pady=5)
        self.idPersonEntry = tk.Entry(self.boxWindow)
        self.idPersonEntry.pack(pady=5)

        tk.Label(self.boxWindow, text="X:").pack(pady=5)
        self.xBoxEntry = tk.Entry(self.boxWindow)
        self.xBoxEntry.pack(pady=5)
        if self.last_x is not None:
            self.xBoxEntry.insert(0, str(self.last_x))  

        tk.Label(self.boxWindow, text="Y:").pack(pady=5)
        self.yBoxEntry = tk.Entry(self.boxWindow)
        self.yBoxEntry.pack(pady=5)
        if self.last_y is not None:
            self.yBoxEntry.insert(0, str(self.last_y))  

        tk.Label(self.boxWindow, text="Largeur:").pack(pady=5)
        self.widthBoxEntry = tk.Entry(self.boxWindow)
        self.widthBoxEntry.pack(pady=5)

        tk.Label(self.boxWindow, text="Hauteur:").pack(pady=5)
        self.heightBoxEntry = tk.Entry(self.boxWindow)
        self.heightBoxEntry.pack(pady=5)

        tk.Button(self.boxWindow, text="Ajouter", command=self.ajouterBox).pack(pady=10)

    def ajouterBox(self):
        id_marche = int(self.idMarcheEntry.get())
        id_person_str = self.idPersonEntry.get().strip()
        idPerson = None if not id_person_str else int(id_person_str)

        x = int(self.xBoxEntry.get())
        y = int(self.yBoxEntry.get())
        width = int(self.widthBoxEntry.get())
        height = int(self.heightBoxEntry.get())

        Box.create(self.connexion, idPerson, id_marche, x, y, width, height)
        messagebox.showinfo("Succès", "Box ajouté avec succès!")
        self.boxWindow.destroy()
        self.canvas.delete("all")
        self.afficher_marches()
        self.afficher_boxes()

    def creer_boutons_ajout(self):
        frameAjout = tk.LabelFrame(self.root, text="Gestion", padx=10, pady=10, font=("Arial", 10, "bold"), fg="black")
        frameAjout.place(x=1100, y=100, width=210, height=300)  # Augmenter la hauteur pour accueillir plus de boutons

        btnAjouterMarche = tk.Button(frameAjout, text="Ajouter Marché", width=20, height=2, bg="#f0f0f0", font=("Arial", 10), command=self.ajoutMarcheFormulaire)
        btnAjouterMarche.grid(row=0, column=0, padx=10, pady=5)

        btnAjouterBox = tk.Button(frameAjout, text="Ajouter Box", width=20, height=2, bg="#f0f0f0", font=("Arial", 10), command=self.ajoutBoxFormulaire)
        btnAjouterBox.grid(row=1, column=0, padx=10, pady=5)

        btnPayement = tk.Button(frameAjout, text="Paiement", width=20, height=2, bg="#f0f0f0", font=("Arial", 10), command=self.creer_formulaire)
        btnPayement.grid(row=2, column=0, padx=10, pady=5)

        btnLouerBox = tk.Button(frameAjout, text="Louer Box", width=20, height=2, bg="#f0f0f0", font=("Arial", 10), command=self.louerBoxFormulaire)
        btnLouerBox.grid(row=3, column=0, padx=10, pady=5)

        btnQuitterBox = tk.Button(frameAjout, text="Quitter Box", width=20, height=2, bg="#f0f0f0", font=("Arial", 10), command=self.quitterBoxFormulaire)
        btnQuitterBox.grid(row=4, column=0, padx=10, pady=5)