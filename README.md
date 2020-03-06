<p align="center"><img width=45% src="https://raw.githubusercontent.com/Simplon-IA-Bdx-1/realestate-ange-de-la-ville/master/ange.png"></p>


# Realestate Ange de la ville 

Ce projet a pour objectif de prédire le prix de vente de bien immobilier. 
Dans un premier temps, nous nous sommes concentrées sur les maisons et les appartements à Bordeaux. 
Nous avons décidé de scrapper le site se loger.com, ce dernier ayant des protection anti-scrapping nous avons utilisé sélénium afin de pouvoir imiter le comportement d'un utilisateur humain afin de ne pas être repérer.
Nous avons ainsi rassemblé les caractéristiques de 847 maisons et 728 appartements sur Bordeaux.
Nous avons ensuite construit le modèle regressor de sklearn en utilisant un pipeline pour la préparation des données.

## Features

|   Features   |  type  | 
|     :---:    |      :---:      |
idannonce |  int  |
| typedebien |  object  |
| typedetransaction |  object  |
| codepostal |  int  |
| ville |  object  |
| etage |  int  |
| idtypechauffage |  object  |
| idtypecuisine |  object  |
| naturebien |  int  |
| si_balcon |  int  |
| nb_chambres |  int  |
| nb_pieces |  int  |
| si_sdbain |  int  |
| si_sdEau |  int |
| nb_photos |  int  |
| prix |  int  |
| surface |  int  |
| dpeL |  int  |
| dpeC|  int  |






## Organisation du projet

|   Notebook   |  Git  | Local |  Description  |
|     :---:    |      :---:      |     :---:      |     :---:      |
| Scrapping de SeLoger.com   | [Scrapping](https://github.com/Simplon-IA-Bdx-1/realestate-ange-de-la-ville/blob/master/scraperseloger.ipynb) |   [Scrapping](http://localhost:8888/notebooks/scraperseloger.ipynb)  | Scrapping et utilisation de Sélénium | 
| Création du modèle  | [Regressor sklearn](https://github.com/Simplon-IA-Bdx-1/realestate-ange-de-la-ville/blob/master/model.ipynb)|   [Regressor sklearn](http://localhost:8888/notebooks/model.ipynb)  | Modèle Regressor avec pipeline pour la préparation des données | 



## Installation

Pour cloner le repo sur votre machine, tapez dans ton terminal :

```bash
  $ git clone https://github.com/Simplon-IA-Bdx-1/realestate-ange-de-la-ville.git
```

Ensuite vous pourrez installer et utiliser Jupyter dans l'environnement *conda* avec la commande suivante :

```bash
  $ conda env create -f anges.yml && conda activate anges && jupyter notebook --no-browser
```

Conda installera les librairies nécessaires et sélectionnera le nouvel environnement, puis l'application jupyter notebook sera lancée.


