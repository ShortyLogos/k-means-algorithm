##########################################################################
#                               VOCABULAIRE                              #
##########################################################################

CREER_VOCABULAIRE = '''
CREATE TABLE IF NOT EXISTS vocabulaire
(
    index_mot INTEGER PRIMARY KEY,
    mot TEXT NOT NULL UNIQUE
)
'''
DROP_VOCABULAIRE = 'DROP TABLE IF EXISTS vocabulaire'
INSERT_VOCABULAIRE = 'INSERT OR IGNORE INTO vocabulaire(mot, index_mot) VALUES(?, ?)'
SELECT_VOCABULAIRE = 'SELECT mot, index_mot FROM vocabulaire'
SELECT_TEST_VOCABULAIRE = 'SELECT mot, index_mot FROM vocabulaire ORDER BY index_mot DESC LIMIT 10'

##########################################################################
#                               COOCCURRENCES                            #
##########################################################################

CREER_COOCCURRENCES = '''
CREATE TABLE IF NOT EXISTS cooccurrences
(
    taille INTEGER NOT NULL,
    index_mot INTEGER NOT NULL,
    index_mot2 INTEGER NOT NULL,
    score NUMBER NOT NULL,
    PRIMARY KEY (index_mot, index_mot2, taille)
)
'''
DROP_COOCCURRENCES = 'DROP TABLE IF EXISTS cooccurrences'
INSERT_COOCCURRENCES = '''
    INSERT OR REPLACE INTO cooccurrences (taille, index_mot, index_mot2, score) 
    VALUES (?, ?, ?, ?);
'''
SELECT_COOCCURRENCES = 'SELECT index_mot, index_mot2, score FROM cooccurrences WHERE taille = ?'
SELECT_TEST_COOCCURENCES = 'SELECT index_mot, index_mot2, score FROM cooccurrences ORDER BY score DESC LIMIT 10'