from sqlite3.dbapi2 import Error
import gestionnaireBD as BD
from tkinter import *
import Constante

 
class Interface:
    def __init__(self, principal):
        
        self.fenetre = principal

        #--------------------------Affichage--------------------------

        
        fenetre.title("Évenement Système d'alarme")
        fenetre.geometry('530x150')
        fenetre.resizable(0, 0)



        #bouton de depart du système
        self.btn_active=Button(text="Afficher évenement", command=self.afficherEvenemnt_clicked)

        self.btn_active.grid(row=0, column=0)

        #Entrée code d'accès
        self.entry_code=Entry()
        self.entry_code.grid(row=0, column=1)

        self.txt_afficher = Text()
        self.txt_afficher.configure(height=5, width=65)
        self.txt_afficher.grid(row=1, column=0, columnspan= 2)
        
    def afficherEvenemnt_clicked(self):
        self.txt_afficher.delete("1.0","end")
        nombresEvenements = BD.nombresEvenements()
        
        
        try:
            
            if int(self.entry_code.get()) <= nombresEvenements and int(self.entry_code.get()) > 0:
                evenement = BD.selection(self.entry_code.get())
                
                self.txt_afficher.insert(INSERT, evenement)
                #ajouter dans le self.txt_afficher
            else:
                self.txt_afficher.insert(INSERT, Constante.messErreur + str(nombresEvenements+1))
                
        except ValueError or Error:
            if isinstance(nombresEvenements, int):
                self.txt_afficher.insert(INSERT, Constante.messErreur + str(nombresEvenements+1))
            else:
                self.txt_afficher.insert(INSERT,nombresEvenements) 
                self.btn_active["state"] = DISABLED
                self.entry_code["state"] = DISABLED

if __name__ == "__main__":
    #creation de la fenetre
        root = fenetre=Tk()    
        app = Interface(root)
        fenetre.mainloop()