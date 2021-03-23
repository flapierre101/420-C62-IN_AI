import sqlite3
from traceback import print_exc

# TODO creer des index

CHEMINBD = 'maBD.db'
ACTIVER_FK = 'PRAGMA foreign_keys = 1'

CREER_D = '''
CREATE TABLE IF NOT EXISTS word_dict
(
    id  INT PRIMARY KEY NOT NULL,
    mot CHAR(24) NOT NULL
)
'''
DROP_D = 'DROP TABLE IF EXISTS word_dict'
INSERT_D = 'INSERT INTO word_dict VALUES(?, ?)'

CREER_E = '''
CREATE TABLE IF NOT EXISTS cooc_mat
(
    mot1 INT NOT NULL,
    mot2 INT NOT NULL,
    frequence int NOT NULL,

    PRIMARY KEY(mot1, mot2),
    FOREIGN KEY(mot1) REFERENCES word_dict(id)
    FOREIGN KEY(mot2) REFERENCES word_dict(id)
)
'''
DROP_E = 'DROP TABLE IF EXISTS cooc_mat'
INSERT_E = 'INSERT INTO cooc_mat VALUES(?, ?, ?)'
DELETE_E = 'DELETE FROM cooc_mat WHERE nom = ?'

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