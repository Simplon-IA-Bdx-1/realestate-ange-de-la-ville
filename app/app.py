import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
import webbrowser
import pandas as pd 
import json

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
    error = []
    num_features = {'etage' : 30, 'si_balcon': 1, 'nb_chambres': 10,'nb_pieces': 10, 'si_sdbain': 1, 'si_sdEau': 1, 'surface': 900}
    features = list(num_features.keys())
    for feature in features :
        value = int(data[feature])
        if (value >= 0) | (value <= num_features[feature]) :
                    
            bien_features[feature] = [value]
        else:
            error.append(feature)
            bien_features[0]
            
    if (data['typedebien'] == "Appartement") | (data['typedebien'] == "Maison / Villa") :
        bien_features['typedebien'] = [data['typedebien']]
    else:
        error.append('typedebien')
        bien_features['typedebien'] = "Appartement"


    if (data['typedetransaction'] == "['vente de prestige']") | (data['typedetransaction'] == "['vente']") :
        bien_features['typedetransaction'] = [data['typedetransaction']]
    else:
        error.append('typedetransaction')
        bien_features['typedetransaction'] = "['vente']"

    if (data['idtypechauffage'] == "individuel") | (data['idtypechauffage'] == "individuel électrique") | (data['idtypechauffage'] == "individuel électrique radiateur") | (data['idtypechauffage'] == "gaz") | (data['idtypechauffage'] == "individuel électrique") | (data['idtypechauffage'] == "mixte") | (data['idtypechauffage'] == "électrique") | (data['idtypechauffage'] == "individuel gaz sol") | (data['idtypechauffage'] == "gaz radiateur") | (data['idtypechauffage'] == "électrique mixte") :    
        bien_features['idtypechauffage'] = [data['idtypechauffage']]
    else:
        error.append('idtypechauffage')
        bien_features['idtypechauffage'] = "individuel"
        
        

    if (data['idtypecuisine'] == "aucune") | (data['idtypecuisine'] == "coin cuisine") | (data['idtypecuisine'] == "équipée") | (data['idtypecuisine'] == "séparée") | (data['idtypecuisine'] == "	séparée équipée") | (data['idtypecuisine'] == "américaine") | (data['idtypecuisine'] == "américaine équipée") :
        bien_features['idtypecuisine'] = [data['idtypecuisine']]
        


    else:
        error.append('idtypecuisine')
        bien_features['idtypecuisine'] = "aucune"
    # return jsonify(data)
    # exit()    
   
    if (data['codepostal'] == 33000) | (data['codepostal'] == 33100) | (data['codepostal'] == 33200) | (data['codepostal'] == 33300) | (data['codepostal'] == 33700) | (data['codepostal'] == 33800) :
        bien_features['codepostal'] = [int(data['codepostal'])]  
        
    else:
        error.append('codepostal')
        bien_features['codepostal'] = 33000

        
    final_features = pd.DataFrame.from_dict(bien_features)
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
    
        'prix prédit': output
        }
        return jsonify(dictionnaire)
    
if __name__ == '__main__':
    url = 'http://127.0.0.1:5000' 
    webbrowser.open_new(url)
    app.run(debug=True)