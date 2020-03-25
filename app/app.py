import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
import webbrowser
import pandas as pd 
import json
import csv
from annonce import Annonce
from bien import Bien
import codecs
import datetime
import os
app = Flask(__name__, instance_relative_config=True)


ADMIN_KEY = "5453213761213547681243576"
# Config options - Make sure you created a 'config.py' file.
app.config.from_pyfile('config.py')
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
model_path = 'model_maisons_apparts.pickle'
model = pickle.load(open('model_maisons_apparts.pickle', 'rb'))


@app.route('/', methods=['GET'])
def dropdown():


    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():

    
    if (request.url == 'http://127.0.0.1:5000/predict') & (request.headers['content-type'] == 'application/x-www-form-urlencoded'):
        form = request.form.to_dict()
        data = { "biens" : [form]}
        nb_bien = 1
    
    if request.headers['content-type'] == 'application/json':
        data = request.get_json(force=True)
        nb_bien = len(data['biens'])
    biens = []
    chambres = []

    for i in range(0,nb_bien):
        bien = Bien()
        bien.set_etage(data['biens'][i]['etage'])
        bien.set_si_balcon(data['biens'][i]['si_balcon'])
        bien.set_nb_chambres(data['biens'][i]['nb_chambres'])
        bien.set_nb_pieces(data['biens'][i]['nb_pieces'])
        bien.set_si_sdbain(data['biens'][i]['si_sdbain'])
        bien.set_si_sdeau(data['biens'][i]['si_sdEau'])
        bien.set_surface(data['biens'][i]['surface'])
        bien.set_typedebien(data['biens'][i]['typedebien'])
        bien.set_typedetransaction(data['biens'][i]['typedetransaction'])
        bien.set_idtypechauffage(data['biens'][i]['idtypechauffage'])
        bien.set_idtypecuisine(data['biens'][i]['idtypecuisine'])
        bien.set_codepostal(data['biens'][i]['codepostal'])
        biens.append(bien)


    # Get form answers of the user
    
  
    

    final_features = pd.DataFrame([b.__dict__ for b in biens ])


    f = final_features[['_typedebien', '_typedetransaction', '_codepostal', '_etage', '_idtypechauffage', '_idtypecuisine', '_si_balcon', '_nb_chambres', '_nb_pieces', '_si_sdbain', '_si_sdEau', '_surface']]
    df = f.rename(columns={'_typedebien': 'typedebien', '_typedetransaction' : 'typedetransaction', '_codepostal' : 'codepostal', '_etage': 'etage', '_idtypechauffage' : 'idtypechauffage', '_idtypecuisine' : 'idtypecuisine', '_si_balcon' : 'si_balcon', '_nb_chambres' : 'nb_chambres', '_nb_pieces' : 'nb_pieces', '_si_sdbain' : 'si_sdbain', '_si_sdEau' : 'si_sdEau', '_surface' : 'surface'})

    # # # Predict with loaded model
    prediction = model.predict(df)

    # # # Format of the output prediction
    
    headers = request.headers['content-type']
    outputs = []


    for i in range(0,nb_bien):
        outputs.append(prediction[i])

    date = datetime.datetime.now()
    conn = get_db()
    cur = conn.cursor()

    data = ('prediction', date, model_path, str(outputs))

    cursor = cur.execute("""insert into Prediction  (action,
                            date,
                            model,
                            predictions) values (?, ?, ?, ?)""", data)
                        
    cur.close()
    conn.commit()                    
    close_connection(cur) 




    if (request.url == 'http://127.0.0.1:5000/predict') & (request.headers['content-type'] == 'application/x-www-form-urlencoded'):
        return render_template('response.html', prediction_text='Le prix estimé du bien est', prediction_prix= f'{int(outputs[0])} euros')
    
    
    if request.headers['content-type'] == 'application/json':
        
        dictionnaire = {
        'type': 'Prédiction bien immobilier',
         'prix': data
        # 'prix': outputs
        }
        return jsonify(dictionnaire)


@app.route('/create-table',methods=['GET'])
def create_seloger_table():

    if 'key' in request.args:
        key = request.args.get('key')
        if ADMIN_KEY == key:

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

            cur.execute("""
                CREATE TABLE IF NOT EXISTS  `Prediction` (
                'id' INTEGER PRIMARY KEY,
                `action` VARCHAR(255) NOT NULL,
                `date` DATETIME NOT NULL,
                'model' VARCHAR(255) NOT NULL,
                `predictions` TEXT NOT NULL 
            );""")

            # cur.execute("""DROP TABLE Model""")
        
            cur.execute("""
                CREATE TABLE IF NOT EXISTS  `Model` (
                'id' INTEGER PRIMARY KEY,
                `r2` FLOAT NOT NULL,
                `mae` FLOAT NOT NULL,
                `rmse` FLOAT NOT NULL,
                `date` DATETIME NOT NULL,
                'model_name' VARCHAR(255) NOT NULL
            );""")
            cur.close()
            close_connection(cur)

            if "curl" in request.headers['User-agent']:
                return jsonify({'status': 'OK',
                                    'result': 'Les tables ont bien été crées'},
                                200)
                
            else:
                return render_template('response.html', texte='La table est prête à être utilisée', texte2= f'Have Fun')
        
        if "curl" in request.headers['User-agent']:
            return jsonify({'status': 'Accès interdit'},
                    403)
        else:
            return render_template('acces_interdit.html')

    else:
        if "curl" in request.headers['User-agent']:
            return jsonify({'status': 'Accès interdit'},
                        403)          
        else:
            return render_template('acces_interdit.html')      




@app.route('/import',methods=['GET'])
def import_csv():
    
    if 'key' in request.args:
        key = request.args.get('key')
        if ADMIN_KEY == key:

            result = {}
            #create_seloger_table()
            conn = get_db()
            cur = conn.cursor()
            with open('biens_features.csv', 'r', encoding='utf-8', newline='\n') as csvfile:
                            reader = csv.DictReader(csvfile, delimiter=',')
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
                                
            
            if "curl" in request.headers['User-agent']:
                return jsonify({'status': 'OK',
                            'result': result},
                        200)
            else:
                return render_template('response.html', texte='Les données ont bien été ajoutées', texte2='Have Fun')
         
        else:
                
            if "curl" in request.headers['User-agent']:
                return jsonify({'status': 'Accès interdit'},
                        403)
            else:
                return render_template('acces_interdit.html')
            
    else:
        if "curl" in request.headers['User-agent']:
            return jsonify({'status': 'Accès interdit'},
                        403)          
        else:
            return render_template('acces_interdit.html')      




@app.route('/get-biens',methods=['GET'])
def get_biens():

    if 'key' in request.args:
        key = request.args.get('key')
        if ADMIN_KEY == key:

            cur = get_db().cursor()
            cur.execute("""SELECT * FROM SeLoger""")
            biens = cur.fetchall()


            cur.close()
                                
            close_connection(cur)

            return jsonify({'status': 'OK',
                            'result': biens},
                        200)
        return jsonify({'status': 'Accès interdit'},
                    403)

    return jsonify({'status': 'Accès interdit'},
                    403)

@app.route('/get-logs',methods=['GET'])
def get_log():


    if 'key' in request.args:
        key = request.args.get('key')
        if ADMIN_KEY == key:
            
            cur = get_db().cursor()
            cur.execute("""SELECT * FROM Prediction""")
            logs = cur.fetchall()


            cur.close()
                                
            close_connection(cur)

            return jsonify({'status': 'OK',
                        'result': logs},
                    200)   
    
        return jsonify({'status': 'Accès interdit'},
                    403)

    return jsonify({'status': 'Accès interdit'},
                    403)


@app.route('/get-models',methods=['GET'])
def get_model():
    

    if 'key' in request.args:
        key = request.args.get('key')
        if ADMIN_KEY == key:
            
            cur = get_db().cursor()
            cur.execute("""SELECT * FROM Model ORDER BY mae""")
            models = cur.fetchall()


            cur.close()
                                
            close_connection(cur)

            return jsonify({'status': 'OK',
                        'result': models},
                    200)   
    
        return jsonify({'status': 'Accès interdit'},
                    403)

    return jsonify({'status': 'Accès interdit'},
                    403)

@app.route('/list',methods=['GET'])
def list():
    if 'key' in request.args:
        key = request.args.get('key')
        if ADMIN_KEY == key:
            cur = get_db().cursor()
            cur.execute("""SELECT * FROM SeLoger""")
            rows = cur.fetchall()
            cur.close()
            close_connection(cur)
            
            return render_template("list.html",rows = rows)
            
        else:
            return render_template('acces_interdit.html')  

    else:
        return render_template('acces_interdit.html') 

@app.route('/list-models',methods=['GET'])
def list_models():

    if 'key' in request.args:
        key = request.args.get('key')
        if ADMIN_KEY == key:
            cur = get_db().cursor()
            cur.execute("""SELECT * FROM Model""")
            rows = cur.fetchall()
            cur.close()
            close_connection(cur)
        
            return render_template("list_models.html",rows = rows)
        else:
            return render_template('acces_interdit.html')  

    else:
        return render_template('acces_interdit.html')  



@app.route('/list-logs',methods=['GET'])
def list_logs():

    if 'key' in request.args:
        key = request.args.get('key')
        if ADMIN_KEY == key:
            cur = get_db().cursor()
            cur.execute("""SELECT * FROM Prediction""")
            rows = cur.fetchall()
            cur.close()
            close_connection(cur)
   
            return render_template("list_logs.html",rows = rows)
        
        else:
            return render_template('acces_interdit.html')  

    else:
        return render_template('acces_interdit.html')  


@app.route('/train-model',methods=['GET'])
def train_model():
    
    if 'key' in request.args:
        key = request.args.get('key')
        if ADMIN_KEY == key:


            import pandas as pd
            from pandas import DataFrame, read_csv
            from sklearn.pipeline import Pipeline
            from sklearn.impute import SimpleImputer
            from sklearn.preprocessing import (StandardScaler, LabelEncoder,
                                            OneHotEncoder, OrdinalEncoder, FunctionTransformer,
                                            PowerTransformer)
            from sklearn.compose import ColumnTransformer
            from sklearn.linear_model import Ridge
            from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
            import numpy as np
            from sklearn.model_selection import train_test_split
            import pickle


            #load data
            df_full = read_csv('biens_features.csv', sep=",", index_col = 0)

            #data cleaning
            chauffageNArows = df_full['idtypechauffage'] == "0"
            df_full.loc[chauffageNArows,['idtypechauffage']] = np.nan

            cuisineNArows = df_full['idtypecuisine'] == "0"
            df_full.loc[cuisineNArows,'idtypecuisine'] = np.nan
            
            #df_full['surface'] = str(df_full['surface'])
            df_full['surface']= df_full['surface'].astype(str)
            df_full['surface'] = df_full['surface'].replace(',', '.')
            df_full['surface']= df_full['surface'].astype(float)

            #Suppression des biens de prix 0€
            len(df_full.loc[df_full['prix']==0])
            (df_full.loc[df_full['prix']==0]).index
            df_full = df_full.drop((df_full.loc[df_full['prix']==0]).index, axis=0)

            #Suppression des outliers
            (df_full.loc[df_full['prix']> 2500000]).index
            df_full = df_full.drop((df_full.loc[df_full['prix']> 2500000]).index, axis=0)
            df_full.drop(['idannonce', 'ville', 'nb_photos', 'naturebien'], inplace=True, axis=1)

            #pipeline
            categoricals = ['typedebien', 'typedetransaction','idtypechauffage', 'idtypecuisine', 'codepostal']
            binaries = ['si_balcon','si_sdbain','si_sdEau']
            numericals = ['nb_chambres', 'nb_pieces', 'etage', 'surface']

            #Categorical features
            #for col in categoricals:
                #print(df_full[col].unique())

            categorical_pipe = Pipeline([
                ('imputer', SimpleImputer(strategy='most_frequent')),
                ('onehot', OneHotEncoder(handle_unknown="ignore"))
            ])

            #binary features
            #for col in binaries:
                #print(df_full[col].unique())

            binary_pipe = Pipeline([
                ('imputer', SimpleImputer(strategy='most_frequent'))
            ])


            #Numerical features
            numerical_pipe = Pipeline([
                ('imputer', SimpleImputer(strategy='most_frequent')),
                ('scaler', StandardScaler())
            ])

            #preprocessing pipe
            preprocess_pipe = ColumnTransformer([
                ('cat', categorical_pipe, categoricals),
                ('num', numerical_pipe, numericals),
                ('ord', binary_pipe, binaries)
            ])

            #regression model
            regressor = Ridge()

            model = Pipeline([
                ('pre', preprocess_pipe),
                ('reg', regressor)
            ])

            #training and evaluation

            target_column = "prix"

            X_fulltrain = df_full.drop(target_column, axis=1)
            y_fulltrain = df_full[target_column]

            X_train, X_valid, y_train, y_valid = train_test_split(X_fulltrain, y_fulltrain, test_size=0.1, random_state=42)

            model.fit(X_train,y_train)

            y_valid_pred = model.predict(X_valid)
            r2 = r2_score(y_valid, y_valid_pred)
            rmse = np.sqrt(mean_squared_error(y_valid, y_valid_pred))
            mae = mean_absolute_error(y_valid, y_valid_pred)
        

            date = datetime.datetime.now()
            model_name = 'model_'+str(date.day)+'_'+str(date.month)+'_'+str(date.year)+'_'+ str(date.hour) +'h'+ str(date.minute)
            
            conn = get_db()
            cur = conn.cursor()
            cur.execute("""SELECT * FROM Model ORDER BY mae LIMIT 1""")
            old_models = cur.fetchall()

            

            
            data = (r2, mae, rmse, date, model_name)

            cursor = cur.execute("""insert into Model  (r2,
                                    mae,
                                    rmse,
                                    date,
                                    model_name) values (?, ?, ?, ?, ?)""", data)
                                
            cur.close()
            conn.commit()                    
            close_connection(cur) 

            if old_models[0][2] > mae:
                filename = 'model_test.pickle'
                pickle.dump(model, open(filename, 'wb'))

            
            pickle.dump(model, open(model_name, 'wb'))

            if "curl" in request.headers['User-agent']:
                return jsonify({'status': 'OK',
                                    'result': 'Le modèle à bien été mis à jour'},
                                200)
                
            else:
                return render_template('response.html', texte='modèle mis à jour', texte2='Have Fun')

        else:
            if "curl" in request.headers['User-agent']:
                return jsonify({'status': 'Accès interdit'},
                            403)          
            else:
                return render_template('acces_interdit.html')
    
    else:
        if "curl" in request.headers['User-agent']:
            return jsonify({'status': 'Accès interdit'},
                        403)          
        else:
            return render_template('acces_interdit.html')


if __name__ == '__main__':
    url = 'http://127.0.0.1:5000' 
    webbrowser.open_new(url)
    app.run(debug=True)