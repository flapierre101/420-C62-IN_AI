import sqlite3
from traceback import print_exc

CHEMINBD = 'maBD.db'
ACTIVER_FK = 'PRAGMA foreign_keys = 1'

CREER_D = '''
CREATE TABLE IF NOT EXISTS departement
(
    id  INT PRIMARY KEY NOT NULL,
    nom CHAR(15) NOT NULL
)
'''
DROP_D = 'DROP TABLE IF EXISTS departement'
INSERT_D = 'INSERT INTO departement VALUES(?, ?)'

CREER_E = '''
CREATE TABLE IF NOT EXISTS employe
(
    id  INT NOT NULL,
    id_dept INT NOT NULL,
    nom CHAR(15) NOT NULL,
    PRIMARY KEY(id),
    FOREIGN KEY(id_dept) REFERENCES departement(id)
)
'''
DROP_E = 'DROP TABLE IF EXISTS employe'
INSERT_E = 'INSERT INTO employe VALUES(?, ?, ?)'
DELETE_E = 'DELETE FROM employe WHERE nom = ?'

def connecter():
    connexion = sqlite3.connect(CHEMINBD)
    curseur = connexion.cursor()
    curseur.execute(ACTIVER_FK)
    
    return connexion, curseur
    
def deconnecter(connexion, curseur):
    curseur.close()
    connexion.close()
    
    
def creer_tables(cur):
    cur.execute(DROP_E)
    cur.execute(DROP_D)

    cur.execute(CREER_D)
    cur.execute(CREER_E)
    
    
def select(cur, enonce):
    cur.execute(enonce)
    rangees = cur.fetchall()
    #print(rangees)
    for rangee in rangees:
        print(rangee)
        
def test_insert(cur):
    cur.execute(INSERT_D, (1, 'informatique'))
    
    cur.execute(INSERT_E, (1000, 1, 'Marcel'))
    cur.execute(INSERT_E, (2000, 1, 'Michelle'))
    cur.execute(INSERT_E, (3000, 1, 'Jean-Marc'))
    cur.execute(INSERT_E, (4000, 1, 'Toto'))
    
    
def main():
    try:
        connexion, curseur = connecter()
        
        
        #select(curseur, 'SELECT "Hello world!"')
        creer_tables(curseur)
        #curseur.execute('INSERT INTO employe VALUES(1000, 1, "Tata")')
        
        test_insert(curseur)
        curseur.execute(DELETE_E, ('Toto',))
        
        
        liste_emp = [(5000, 1, 'Richard'), (6000, 1, 'Éric')]
        curseur.executemany(INSERT_E, liste_emp)
        
        connexion.commit()
        
        select(curseur, 'SELECT * FROM employe')
        
        deconnecter(connexion, curseur)
        
    except:
        print_exc()
        return 1
    return 0
    
    
if __name__ == '__main__':
    quit(main())