import json
import codecs,os
import Constante 
class Evenement:
    'stocke les évènements'
    
    def __init__(self,noEvenement,dateHeure,typeEvenement):
        self.noEvenement = noEvenement
        self.dateHeure = dateHeure
        
        if typeEvenement == Constante.activation:
            self.typeEvenement = "Activation du système d'alarme"    
        elif typeEvenement == Constante.desactivation:
            self.typeEvenement = "Désactivation du système d'alarme"
        elif typeEvenement == Constante.codeValide:
            self.typeEvenement = "Accès valide du système d'alarme"
        elif typeEvenement == Constante.codeInvalide:
            self.typeEvenement = "Accès invalide du système d'alarme"
        else:
            self.typeEvenement = "Accès bloqué trop de tentatives"
            
        
    def __repr__(self):
        return self.typeEvenement
            
    def afficherEvenement(self):
        affichage = "\n" + str(self.dateHeure) + str(self.typeEvenement)

        return affichage