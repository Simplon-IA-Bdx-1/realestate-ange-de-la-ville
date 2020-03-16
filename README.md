<p align="center"><img width=45% src="https://raw.githubusercontent.com/Simplon-IA-Bdx-1/realestate-ange-de-la-ville/master/ange.png"></p>


# Realestate Ange de la ville 

Ce projet a pour objectif de prédire le prix de vente de bien immobilier. 
Dans un premier temps, nous nous sommes concentré sur les maisons et les appartements à Bordeaux. 
Nous avons décidé de scrapper le site seloger.com, ce dernier ayant des protections anti-scrapping nous avons utilisé sélénium afin de pouvoir imiter le comportement d'un utilisateur humain afin de ne pas être repéré.
Nous avons ainsi rassemblé les caractéristiques de 847 maisons et 728 appartements sur Bordeaux.
Nous avons ensuite construit le modèle regressor de sklearn en utilisant un pipeline pour la préparation des données.
Le modèle a ensuite été exporté sous forme de pickle et déployé dans une application Flask.
L'application flask permet d'obtenir le prix estimé d'un bien immobilier sur Bordeaux. 
La prédiction peut être obtenu de deux manières :
* Via un formulaire web
* Au format json via une API (Les informations sur le bien doivent être fournies au format json) 

## Répartition des tâches 
Avant le premier mois en entreprise :
* Maud : README + modele
* Christophe : Scrapping
* Maxime & Corantin : BDD

Pour la suite :

* Maxime : optimisation du scrapping et enregistrement en BDD
* Maud : application Flask, cURL
* Corantin : Azure Function


## Features modèle et prédiction

|   Features   |  type  |   Valeurs suporté   |
|     :---:    |      :---:      |      :---:      |
idannonce |  int  |
| typedebien |  object  | "Appartement",  "Maison / Villa" |
| typedetransaction |  object  | "['vente de prestige']",  "['vente']" |
| codepostal |  int  |  33000, 33100, 33200, 33300, 33700, 33800 |
| ville |  object  |
| etage |  int  | 0 > ... < 30 |
| idtypechauffage |  object  | "individuel", "individuel électrique", "individuel électrique radiateur", "gaz","individuel électrique","mixte","électrique", "individuel gaz sol", "gaz radiateur", "électrique mixte" |  
| idtypecuisine |  object  | "aucune", "coin cuisine", "équipée", "séparée", "séparée équipée", "américaine", "américaine équipée" |
| naturebien |  int  | 0, 1 |
| si_balcon |  int  | 0, 1 |
| nb_chambres |  int  | 0 > ... < 10 |
| nb_pieces |  int  | 0 > ... < 10 |
| si_sdbain |  int  | 0, 1 |
| si_sdEau |  int | 0, 1 |
| nb_photos |  int  |
| prix |  int  |
| surface |  int  | 0 > ... < 900 |
| dpeL |  int  |
| dpeC|  int  |

## Librairie


|   LIB   |  Version  |
|     :---:    |      :---:      |
|     sqlite    |      3.31.1      |
|     Scikit-learn    |      0.21.3     |
|     Flask    |   1.1.1 |
|     beautifulsoup4    |      4.8.2      |
|     python    |      3.4.6      |
|     requests   |      2.22.0      |
|     selenium    |      3.141.0      |

## Organisation du projet

|   Notebook   |  Git  | Local |  Description  |
|     :---:    |      :---:      |     :---:      |     :---:      |
| Scrapping de SeLoger.com   | [Scrapping](https://github.com/Simplon-IA-Bdx-1/realestate-ange-de-la-ville/blob/master/scraperseloger.ipynb) |   [Scrapping](http://localhost:8888/notebooks/scraperseloger.ipynb)  | Scrapping et utilisation de Sélénium | 
| Création du modèle  | [Regressor sklearn](https://github.com/Simplon-IA-Bdx-1/realestate-ange-de-la-ville/blob/master/model.ipynb)|   [Regressor sklearn](http://localhost:8888/notebooks/model.ipynb)  | Modèle Regressor avec pipeline pour la préparation des données | 
|     Application Flask    |      [App](https://github.com/Simplon-IA-Bdx-1/realestate-ange-de-la-ville/tree/master/app)      |     :---:      |     Application web et API      |
|     Class Annonce    |      [Class Annonce](https://github.com/Simplon-IA-Bdx-1/realestate-ange-de-la-ville/blob/master/app/annonce.py)      |     :---:      |     Class annonce pour l'import en BDD     |
|     Class Bien   |      [Class Bien](https://github.com/Simplon-IA-Bdx-1/realestate-ange-de-la-ville/blob/master/app/bien.py)      |     :---:      |     Class protegée Bien pour la prédiction     |


## Organisation de l'application Flask

* Prédiction : [http://localhost:5000/predict](http://localhost:5000/predict)
* Création de la table SeLoger : [http://localhost:5000/create-table](http://localhost:5000/create-table)
* Import des données depuis csv : [http://localhost:5000/import](http://localhost:5000/import)
* Affichage en json des annonce présente dans la Base de Données  : [http://localhost:5000/get](http://localhost:5000/get)


## Exemple de requête cURL

Pour une prédiction les informations du bien doivent être fournies au format json.
Fichier exemple : [data.json](https://github.com/Simplon-IA-Bdx-1/realestate-ange-de-la-ville/blob/master/app/data.json)

```bash
 $ curl -d "@data.json" -X POST http://localhost:5000/predict -H "Content-Type: application/json"
```


## Installation

Pour cloner le repo sur votre machine, tapez dans votre terminal :

```bash
  $ git clone https://github.com/Simplon-IA-Bdx-1/realestate-ange-de-la-ville.git
```

Ensuite vous pourrez installer et utiliser Jupyter dans l'environnement *conda* avec la commande suivante :

```bash
  $ conda env create -f anges.yml && conda activate anges && jupyter notebook --no-browser
```

Conda installera les librairies nécessaires et sélectionnera le nouvel environnement, puis l'application jupyter notebook sera lancée.


