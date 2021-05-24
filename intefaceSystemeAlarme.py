from threading import Thread
from tkinter import *
import datetime
from gpiozero import MotionSensor,LED
from signal import pause
import LCD1602
import Constante 
import Evenement as e
import gestionnaireBD as BD
import time
from tkinter import messagebox
import sqlite3
import RPi.GPIO as GPIO
import Keypad as c  
          
touches = ["1", "2", "3",
            "4", "5", "6",
            "7", "8", "9",
            "Enter", "0", "act/desact/backspace"
            ]

lignesBroches = [12,16,20,21] #broche 32,36,38,40
colonnesBroches = [6,13,19] #broche 31,33,35

code = str(2636)
sensor = MotionSensor(23)
ledVert = LED(22)
ledRouge = LED(27)
listeEvent = []
noEvent = 0
sysBloque = False
detecteurOn = True
alarme = False
sysActive = False
LCD1602.init(0x27,1)
LCD1602.clear()
tentativeCode = 0
#création de la BD
BD.creationBdTable()   

class Interface:
    
        
    
    def __init__(self, principal):

        self.fenetre = principal
        
        #--------------------------Affichage--------------------------

        #creation de la fenetre
        
        fenetre.title("Système d'alarme")
        fenetre.geometry('650x550')



        #bouton de depart du système
        self.btn_active=Button(text="Activation système")
        self.btn_active.grid(row=0, column=0)

        #bouton arrêt du système
        self.btn_desactive=Button(text="Désactivation système", state='disabled')
        self.btn_desactive.grid(row=0, column=1)


        self.txt_afficher = Text()
        self.txt_afficher.grid(row=1, column=0, columnspan= 2)

        #Entrée code d'accès
        self.entry_code=Entry()
        self.entry_code['state'] = 'disabled'
        self.entry_code.grid(row=2, column=0)
        
        #Label explication du keypad
        self.label_explication=Label()
        self.label_explication['text'] = "Le # est pour activer et désasctiver le système.\n Le * est pour entrer le code.\n Si on doit entrer le code d'accès # fait office de backspace. "
        self.label_explication.grid(row=3, column=0, columnspan= 2)
        
        #bouton de validation du code d'accès
        self.btn_code=Button(text="Valider code", command=self.validationCode_clicked)
        self.btn_code["state"] = 'disabled'
        self.btn_code.grid(row=2, column=1)

    #2ieme paramètre est l'évenement arrivé et le 3iem est l'objet evenement
    def setup(self,evenementArrive, evenement):
        global code

            
        #quand le sensor detecte un mouvement et que le système est enclenché
        if evenementArrive == Constante.motion:
            
            LCD1602.write(0, 0, 'Entrer le code')
            LCD1602.write(0, 1, code)
            time.sleep(1)
        
        #quand on desactive le systme on clear le LCD et on insère l'évenemnt dans la BD    
        elif evenementArrive == Constante.desactivation:
            
            connexion = BD.connexionBD()
            BD.insertionDonnees(evenement, connexion)
            BD.fermerBD(connexion)
            LCD1602.clear()
            LCD1602.write(0, 0, 'System disabled')
        
        #quand on desactive le systme on clear le LCD et on insère l'évenemnt dans la BD       
        elif evenementArrive == Constante.activation:
            connexion = BD.connexionBD()
            BD.insertionDonnees(evenement, connexion)
            BD.fermerBD(connexion)
            LCD1602.clear()
            LCD1602.write(0, 0, 'System enabled')
        
        elif evenementArrive == Constante.blocked:
            connexion = BD.connexionBD()
            BD.insertionDonnees(evenement,connexion)
            BD.fermerBD(connexion)
            LCD1602.clear()
            LCD1602.write(0, 0, 'Acces blocked')
        
        else:
            connexion = BD.connexionBD()
            BD.insertionDonnees(evenement, connexion)
            BD.fermerBD(connexion)
            

  

    def activation_alarme(self):
        global detecteurOn
        global sysActive
        global alarme
        
        
        if self.btn_desactive['state'] == 'disabled':
            detecteurOn = False
        else:
            alarme = True
            detecteurOn = True
            
        if tentativeCode < 3 and detecteurOn  :
            detecteurOn = True
            self.entry_code['state'] = 'normal'
            self.btn_code["state"] = 'normal'
            self.btn_desactive['state'] = 'disabled'
            ledVert.off()
            ledRouge.on()
            self.setup(Constante.motion, "")
        detecteurOn = False

        #verifie si un mouvement est detcter lorsque le detecteur est ON
    def moveDetected(self,detecteurOn):
        
        if detecteurOn:
            
            sensor.when_motion = self.activation_alarme
    

    def date(self):

        x = datetime.datetime.now()
        date = x.strftime("%a ")
        date += x.strftime("%b ")
        date += x.strftime("%d ")
        date += x.strftime("%H:")
        date += x.strftime("%M:")
        date += x.strftime("%S ")
        date += x.strftime("%Y ")
        
        
        return date

    
    def activationSystem_clicked(self):
        global noEvent
        global sysActive
        sysActive = True
        global detecteurOn
        noEvent += 1
        
        event = e.Evenement(noEvent, self.date(), Constante.activation)
        listeEvent.append(event)
        
        self.txt_afficher.insert(END, event.afficherEvenement())
        self.btn_active['state'] = 'disabled'
        self.btn_desactive['state'] = 'normal'
        self.setup(Constante.activation,event)
        ledVert.on()
        self.moveDetected(detecteurOn)
        
        

    def desactivationSystem_clicked(self):
        global noEvent
        global sysActive
        sysActive = False
        global detecteurOn
        
        noEvent += 1
        event = e.Evenement(noEvent, self.date(), Constante.desactivation)
        listeEvent.append(event)
        ledVert.off()
        ledRouge.off()
        self.txt_afficher.insert(END, event.afficherEvenement()) 
        self.btn_active['state'] = 'normal'
        self.btn_desactive['state'] = 'disabled'
        self.entry_code['state'] = 'disabled'
        self.btn_code["state"] = 'disabled'
        detecteurOn = True
        self.setup(Constante.desactivation,event)
        

    
        
    def validationCode_clicked(self):
        
        global tentativeCode
        global code
        global noEvent
        global alarme
        global sysActive
        if self.entry_code.get() == code:
            alarme = False
            sysActive = False
            noEvent += 1
            tentativeCode = 0
            event = e.Evenement(noEvent, self.date(), Constante.codeValide)
            listeEvent.append(event)
            # "" pcq on ne veux rien afficher dans le LCD
            self.setup("", event)
            self.txt_afficher.insert(END, event.afficherEvenement()) 
            self.desactivationSystem_clicked()
            
        else:
            if tentativeCode < 3:
                noEvent += 1
                tentativeCode += 1 
                event = e.Evenement(noEvent, self.date(), Constante.codeInvalide)
                listeEvent.append(event)
                # "" pcq on ne veux rien afficher dans le LCD
                self.setup("", event)
                self.txt_afficher.insert(END, event.afficherEvenement())
            if tentativeCode >= 3:
                global detecteurOn
                global sysBloque
                alarme = False
                sysActive = False
                detecteurOn = False
                sysBloque = True
                
                event = e.Evenement(noEvent, self.date(), Constante.blocked)
                
                self.setup(Constante.blocked, event)
                ledVert.off()
                ledRouge.blink(0.2)
                self.btn_code["state"] = DISABLED
                self.entry_code["state"] = 'disabled'
                self.btn_active["state"] = 'disabled'
                #affiche sur le lcd que c L'accès est bloqué et tu fait clignotée la led
    
    def boucle(self):
        
        global sysActive
        global alarme
        clavier = c.Keypad(touches, lignesBroches, colonnesBroches, Constante.LIGNES, Constante.COLONNES)
    
        clavier.setDebounceTime(50)
        
        while True:
            if not sysBloque:
                
                touche = clavier.getKey() #obtenir l'état de la touche
                #si le sytème est actif
                if sysActive:
                    #si l'alarme n'est pas enclenchée'
                    if not alarme:
                        #si on appuis sur le dièse on désactive le sytème
                        if touche == "act/desact/backspace":
                            self.desactivationSystem_clicked()
                    else:
                        
                        if (touche != clavier.NULL and touche != "Enter" and touche != "act/desact/backspace"):
                            self.entry_code['state'] = 'normal'
                            
                            self.entry_code.insert(END, touche)
                            
                            self.entry_code['state'] = 'disabled'
                        elif (touche == "Enter"):
                            self.validationCode_clicked()
                        elif touche == "act/desact/backspace":
                            longueurCode = len(self.entry_code.get())
                            
                            if longueurCode > 0:
                                self.entry_code['state'] = 'normal'
                                
                                self.entry_code.delete(longueurCode - 1,END)
                                
                                self.entry_code['state'] = 'disabled'
                            
                #si le système n'est pas actif
                else:
                    #si l'alarme n'est pas enclenchée'
                    if not alarme:  
                        #si on appuis sur le dièse on active le sytème
                        if touche == "act/desact/backspace":                    
                            self.activationSystem_clicked()

    def debutThread(self):
        
        t = Thread(target = self.boucle)
        
        t.start()
        
        

if __name__ == "__main__":
    #creation de la fenetre
    root = fenetre=Tk()    
    app = Interface(root)
    try:
        
        app.debutThread()
    
    except KeyboardInterrupt:
        GPIO.cleanup()
    
    fenetre.mainloop()