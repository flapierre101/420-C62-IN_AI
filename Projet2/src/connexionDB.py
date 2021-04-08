import sqlite3
import numpy as np

#==========================CONSTANTE REQUEST SQL================================
CHEMINBD = 'synonyms_dict.db'
ACTIVER_FK = 'PRAGMA foreign_keys = 1'

CREER_WORD = '''
    CREATE TABLE IF NOT EXISTS word_dict
    (
        id  INT PRIMARY KEY NOT NULL,
        mot CHAR(24) NOT NULL
    )
'''
DROP_WORD = 'DROP TABLE IF EXISTS word_dict'
INSERT_WORD = 'INSERT INTO word_dict VALUES(?, ?)'

CREER_MAT = '''
    CREATE TABLE IF NOT EXISTS cooc_mat
    (
        mot1 INT NOT NULL,
        mot2 INT NOT NULL,
        frequence int NOT NULL,
        fenetre int NOT NULL,

        PRIMARY KEY(mot1, mot2, fenetre),
        FOREIGN KEY(mot1) REFERENCES word_dict(id),
        FOREIGN KEY(mot2) REFERENCES word_dict(id)
    )
'''
DROP_MAT = 'DROP TABLE IF EXISTS cooc_mat'
INSERT_MAT = 'INSERT INTO cooc_mat VALUES(?, ?, ?, ?)'

UPDATE_MAT = '''
    UPDATE cooc_mat
        SET
            frequence = ?
        WHERE
            mot1 = ? and
            mot2 = ? and
            fenetre = ?
'''

DELETE_MAT = 'DELETE FROM cooc_mat WHERE frequence = 0'

GET_MAT = 'SELECT * FROM cooc_mat WHERE fenetre = ?'

VACUUM = 'VACUUM'

CREATE_FILES_DB = '''
       CREATE TABLE IF NOT EXISTS files_DB
        (
            file_name   TEXT    NOT NULL,
            fenetre     INT     NOT NULL,

            PRIMARY KEY(file_name, fenetre)
        )
'''
DROP_FILES_DB = 'DROP TABLE IF EXISTS files_DB'
INSERT_FILE_DB = 'INSERT INTO files_DB VALUES(?, ?)'


class ConnexionDB():
    def __init__(self):
        try:
            self.connexion = sqlite3.connect(CHEMINBD)
            self.cur = self.connexion.cursor()
            self.cur.execute(ACTIVER_FK)
        except:
            print("ERREUR LORS DE LA CONNECTION À LA BD!")

    def deconnecter(self):
        self.cur.close()
        self.connexion.close()

    def creer_tables(self):
        self.cur.execute(CREER_WORD)
        self.cur.execute(CREER_MAT)
        self.cur.execute(CREATE_FILES_DB)

    def drop_tables(self):
        try:
            self.cur.execute(DROP_MAT)
            self.cur.execute(DROP_WORD)
            self.cur.execute(DROP_FILES_DB)
            self.cur.execute(VACUUM)
        except:
            print("Erreur lors de la supression de la base de données!")

    # reçoit une liste de tuples [(id, mot), (id, mot), (nid, nmot)]

    def insert_new_word(self, tuplesmot):
        self.cur.executemany(INSERT_WORD, tuplesmot)
        self.connexion.commit()

    # reçoit une liste de tuples [(id1,id2, frequence), (id1,id2, frequence),
	#                               (nid1,nid2, nfrequence)]
    def insert_mat(self, matcooc):

        self.cur.executemany(INSERT_MAT, matcooc)
        self.connexion.commit()

    def update_mat(self, matcooc):
        self.cur.executemany(UPDATE_MAT, matcooc)
        self.connexion.commit()

    # retourne liste de tuple
    def get_words(self):
        motUnique = {}
        self.cur.execute('SELECT * FROM word_dict')
        rangees = self.cur.fetchall()
        for rangee in rangees:
            motUnique[rangee[1]] = rangee[0]

        return motUnique

    def get_cooc_dict(self, fenetre):
        self.cur.execute('SELECT * FROM cooc_mat WHERE fenetre = ?', (fenetre, ))
        dictCooc = {}
        rangees = self.cur.fetchall()
        for rangee in rangees:
            dictCooc[(rangee[0], rangee[1])] = rangee[2]
            dictCooc[(rangee[1], rangee[0])] = rangee[2]

        return dictCooc

    def get_cooc_mat(self, nbmotunique, fenetre):
        self.cur.execute(GET_MAT, (fenetre,))
        matriceCo = np.zeros((nbmotunique, nbmotunique))
        rangees = self.cur.fetchall()
        if len(rangees) == 0:
            matriceCo = "Invalide"
        else:
            for rangee in rangees:
                matriceCo[rangee[0]][rangee[1]] = rangee[2]
                matriceCo[rangee[1]][rangee[0]] = rangee[2]

        return matriceCo

    def insert_new_file(self, filename, fenetre):
        insert = (filename, fenetre)
        self.cur.execute(INSERT_FILE_DB, insert)
        self.connexion.commit()

    def get_file_db(self):
        try:
            self.cur.execute('SELECT * FROM files_DB')
            file_dict = {}
            results = self.cur.fetchall()
            for result in results:
                file_dict[result[1]] = result[0]
            return file_dict
        except:
            return 0
