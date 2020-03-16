import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
import webbrowser
import pandas as pd 
import json
import csv
from annonce import Annonce
from bien import Bien


# Config options - Make sure you created a 'config.py' file.
#app.config.from_object('config')
# To get one variable, tape app.config['MY_VARIABLE']



# function pour la base de données

import sqlite3
from flask import g

DATABASE = 'app.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

#@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv





# function pour la base de données

app = Flask(__name__)
model = pickle.load(open('model_maisons_apparts.pickle', 'rb'))


@app.route('/', methods=['GET'])
def dropdown():


    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():

    
    if (request.url == 'http://127.0.0.1:5000/predict') & (request.headers['content-type'] == 'application/x-www-form-urlencoded'):
        data = request.form.to_dict()
    
    if request.headers['content-type'] == 'application/json':
        data = request.get_json(force=True)

    # Get form answers of the user
    
    bien_features = {}
    
    bien = Bien() 

    bien_features['etage'] = bien.set_etage(data['etage'])
    bien_features['si_balcon']  = bien.set_etage(data['si_balcon'])
    bien_features['nb_chambres'] = bien.set_si_balcon(data['nb_chambres'])
    bien_features['nb_pieces'] = bien.set_nb_pieces(data['nb_pieces'])
    bien_features['si_sdbain'] = bien.set_si_sdbain(data['si_sdbain'])
    bien_features['si_sdEau'] = bien.set_si_sdeau(data['si_sdEau'])
    bien_features['surface'] = bien.set_surface(data['surface'])
    bien_features['typedebien'] = bien.set_typedebien(data['typedebien'])
    bien_features['typedetransaction'] = bien.set_typedetransaction(data['typedetransaction'])
    bien_features['idtypechauffage'] = bien.set_idtypechauffage(data['idtypechauffage'])
    bien_features['idtypecuisine'] = bien.set_idtypecuisine(data['idtypecuisine'])
    bien_features['codepostal'] = bien.set_codepostal(data['codepostal'])
    


    final_features = pd.DataFrame([bien_features])
    f = final_features[['typedebien', 'typedetransaction', 'codepostal', 'etage', 'idtypechauffage', 'idtypecuisine', 'si_balcon', 'nb_chambres', 'nb_pieces', 'si_sdbain', 'si_sdEau', 'surface']]


    # Predict with loaded model
    prediction = model.predict(f)

    # Format of the output prediction
    output = int(prediction[0])
    headers = request.headers['content-type']

    if (request.url == 'http://127.0.0.1:5000/predict') & (request.headers['content-type'] == 'application/x-www-form-urlencoded'):
        return render_template('index.html', prediction_text='Le prix estimé du bien est', prediction_prix= f'{output} euros')
    
    
    if request.headers['content-type'] == 'application/json':
        
        dictionnaire = {
        'type': 'Prédiction bien immobilier',
    
        'prix': output
        }
        return jsonify(dictionnaire)


@app.route('/create-table',methods=['GET'])
def create_seloger_table():
    
    cur = get_db().cursor()
    
    cur.execute("""
    CREATE TABLE IF NOT EXISTS  `SeLoger` (
        `idannonce` INT NOT NULL,
        `typedebien` VARCHAR(255) NOT NULL,
        `typedetransaction` VARCHAR(255) NOT NULL,
        `codepostal` INT NOT NULL,
        `ville` VARCHAR(255) NOT NULL,
        `etage` INT NOT NULL,
        `idtypechauffage` VARCHAR(255) NOT NULL,
        `idtypedecuisine` VARCHAR(255) NOT NULL,
        `naturebien` INT NOT NULL,
        `si_balcon` INT NOT NULL,
        `nb_chambres` INT NOT NULL,
        `nb_pieces` INT NOT NULL,
        `si_sdbain` INT NOT NULL,
        `si_sdEau` INT NOT NULL,
        `nb_photos` INT NOT NULL,
        `prix` INT NOT NULL,
        `surface` INT NOT NULL
    );""")
    cur.close()
    close_connection(cur)


    return render_template('index.html', prediction_text='La table est prête à être utilisée', prediction_prix= f'Have Fun')





@app.route('/import',methods=['GET'])
def import_csv():
    
    # data = request.get_data()

    # r = {}
    # b = []
    # i=1

    # b.append(str(data))
    # return jsonify(b)


    result = {}
    #create_seloger_table()
    conn = get_db()
    cur = conn.cursor()
    with open('biens_features.csv', 'r', encoding='utf-8', newline='\n') as csvfile:
                     reader = csv.DictReader(csvfile, delimiter=';')
                     for row in reader:
                        annonce = Annonce(
                                idannonce = row['idannonce'],
                                typedebien = row['typedebien'],
                                typedetransaction = row['typedetransaction'],
                                codepostal = row['codepostal'],
                                ville = row['ville'],
                                etage = row['etage'],
                                idtypechauffage = row['idtypechauffage'],
                                idtypecuisine = row['idtypecuisine'],
                                naturebien = row['naturebien'],
                                si_balcon = row['si_balcon'],
                                nb_chambres = row['nb_chambres'],
                                nb_pieces = row['nb_pieces'],
                                si_sdbain = row['si_sdbain'],
                                si_sdEau = row['si_sdEau'],
                                nb_photos =row['nb_photos'],
                                prix = row['prix'],
                                surface = row['surface']

                         )

                         
                        
                        data = (annonce.idannonce, annonce.typedebien, annonce.typedetransaction, annonce.codepostal, annonce.ville, annonce.etage, annonce.idtypechauffage, annonce.idtypecuisine, annonce.naturebien, annonce.si_balcon, annonce.nb_chambres, annonce.nb_pieces, annonce.si_sdbain, annonce.si_sdEau, annonce.nb_photos, annonce.prix, annonce.surface)

                        cursor = cur.execute("""insert into SeLoger (idannonce, 
                                                            typedebien, 
                                                            typedetransaction, 
                                                            codepostal, 
                                                            ville, 
                                                            etage, 
                                                            idtypechauffage, 
                                                            idtypedecuisine, 
                                                            naturebien, 
                                                            si_balcon, 
                                                            nb_chambres, 
                                                            nb_pieces, 
                                                            si_sdbain, 
                                                            si_sdEau, 
                                                            nb_photos, 
                                                            prix, 
                                                            surface) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", data)
                        
                        result[cur.lastrowid] = [annonce.idannonce, annonce.typedebien, annonce.typedetransaction, annonce.codepostal, annonce.ville, annonce.etage, annonce.idtypechauffage, annonce.idtypecuisine, annonce.naturebien, annonce.si_balcon, annonce.nb_chambres, annonce.nb_pieces, annonce.si_sdbain, annonce.si_sdEau, annonce.nb_photos, annonce.prix, annonce.surface]
    cur.close()
    conn.commit()                    
    close_connection(cur)                    
    
    
    return jsonify(result)




@app.route('/get',methods=['GET'])
def get_biens():
    cur = get_db().cursor()
    cur.execute("""SELECT * FROM SeLoger""")
    bien = cur.fetchall()
    cur.close()
                        
    close_connection(cur)

    return jsonify(bien)
if __name__ == '__main__':
    url = 'http://127.0.0.1:5000' 
    webbrowser.open_new(url)
    app.run(debug=True)