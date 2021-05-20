import sqlite3
from sqlite3.dbapi2 import Connection

#Création et/ou connection de la BD
def connexionBD():
    
    try:
        connexion = sqlite3.connect("evenements.db")
        print("Ouverture correctement de la base de données\n")
        return connexion
    
    except sqlite3.Error as error:
            print("Erreur de connexion à la base de données\n", error)

#Création de la table evenement
def creationBdTable():
    
    try:
        connexion = connexionBD()
        
        tableEvenement = """CREATE TABLE IF NOT EXISTS `evenement` ( `noEvenement` INTEGER PRIMARY KEY AUTOINCREMENT, `dateHeure` TEXT, `typeEvenement` TEXT );"""
        
        connexion.execute(tableEvenement)
        print("Table évenement créé\n")
        
        connexion.close()
        return connexion
    
    except sqlite3.Error as error:
        print("Erreur de connexion à la base de données\n", error)

#Insertion de l'évenement arrivé
def insertionDonnees(evenement, connexion):
    try:
        
        
        cur = connexion.cursor()
  
        param = (str(evenement.dateHeure), str(evenement.__repr__()))
        sql = """INSERT INTO evenement (dateHeure,typeEvenement) VALUES (?,?)"""         
        cur.execute(sql,param)
        
        connexion.commit()
        print("Enregistrement ajoutés")
        
        cur.close()
    
    except sqlite3.Error as error:
        print("Erreur d'insertion dans la base de données", error)
        
# à partir du numeréro entré par l'utilisateur(noEvenement dans la BD) on va séléctionner l'évenement correspondant
def selection(param):
    connexion = connexionBD()
    
    cur = connexion.cursor()
  
    
    sql = """SELECT * from evenement WHERE noEvenement = ? """  
    #(param,) pcq sinon ProgramingError explication @ 
    # https://stackoverflow.com/questions/16856647/sqlite3-programmingerror-incorrect-number-of-bindings-supplied-the-current-sta       
    cur.execute(sql, (param,))
    
    for ligne in cur:
        affichage = "Date: " + ligne[1] + "\nÉvenement: " + ligne[2] 
    
    cur.close()
    return affichage

#retourne le nombre d'évenements ou un message d'erreur si la BD n'existe pas 
def nombresEvenements():
    try:
        connexion = connexionBD()
        
        cur = connexion.cursor()
    
        
        sql = """select count(*) from evenement """         
        cur.execute(sql)
        
        for ligne in cur:
            nombresEvenement = ligne[0]
        
        cur.close()
        return nombresEvenement 
    except sqlite3.OperationalError:
        
        return "Aucune table existante pour allez chercher ce numéro d'évenement"
        

def fermerBD(connexion) :

    if connexion:
        connexion.close()
        print("Fermeture de la base de données\n")