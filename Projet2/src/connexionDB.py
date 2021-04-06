import sqlite3
from traceback import print_exc
import numpy as np

# TODO creer des index

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

    PRIMARY KEY(mot1, mot2),
    FOREIGN KEY(mot1) REFERENCES word_dict(id),
    FOREIGN KEY(mot2) REFERENCES word_dict(id)
)
'''
DROP_MAT = 'DROP TABLE IF EXISTS cooc_mat'
INSERT_MAT = 'INSERT INTO cooc_mat VALUES(?, ?, ?)'

UPDATE_MAT = '''
        UPDATE cooc_mat
            SET
                frequence = ?
            WHERE
                mot1 = ? and
                mot2 = ?
'''

DELETE_MAT = 'DELETE FROM cooc_mat WHERE frequence = 0'

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
            print_exc()

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
        except:
            print("je suis ic")


    # def select(self, enonce):
    #     self.cur.execute(enonce)
    #     rangees = cur.fetchall()
    #     #print(rangees)
    #     for rangee in rangees:
    #         print(rangee)

    # reçoit une liste de tuples [(id, mot), (id, mot), (nid, nmot)]
    def insert_new_word(self, tuplesmot):
        self.cur.executemany(INSERT_WORD, tuplesmot)
        self.connexion.commit()

    # reçoit une liste de tuples [(id1,id2, frequence), (id1,id2, frequence), (nid1,nid2, nfrequence)]
    def insert_mat(self, matcooc):

        self.cur.executemany(INSERT_MAT, matcooc)
        self.connexion.commit()

    def update_mat(self, matcooc):
        print(matcooc[0])
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

    def get_cooc_dict(self):
        self.cur.execute('SELECT * FROM cooc_mat')
        matriceCo = {}
        rangees = self.cur.fetchall()
        for rangee in rangees:
            matriceCo[(rangee[0], rangee[1])] = rangee[2]
            matriceCo[(rangee[1], rangee[0])] = rangee[2]

        return matriceCo

    def get_cooc_mat(self, nbmotunique):
        self.cur.execute('SELECT * FROM cooc_mat')
        matriceCo = np.zeros((nbmotunique, nbmotunique))
        rangees = self.cur.fetchall()
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
            print_exc()
            return 0
