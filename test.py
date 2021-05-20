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
           "Enter", "0", "act/desact"
           ]

lignesBroches = [32,36,38,40] #GPIO 12-16-20-21
colonnesBroches = [31,33,35] #GPIO 6-13-19


def boucle():
    clavier = c.Keypad(touches, lignesBroches, colonnesBroches, Constante.LIGNES, Constante.COLONNES)
    
    clavier.setDebounceTime(50)
    
    while True:
        
        touche = clavier.getKey() #obtenir l'état de la touche
        
        if (touche != clavier.NULL and touche != "Enter" and touche != "act/desact"):
            print ("Touche : " + touche)
        elif (touche == "Enter"):
            print("Enter")
        elif touche == "act/desact":
            print("Vous ne pouvez désactiver le système d'alarme sans le code")
        
def d():
    t = Thread(target = boucle)
    print("boucle start")
    t.start()


if __name__ == "__main__":
    print("Démarrage")
    
    try:
        
        d()
    except KeyboardInterrupt:
        GPIO.cleanup()
        print("CTRL+C")
