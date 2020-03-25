class Bien:

    def __init__(self):
        self._idannonce = None
        self._typedebien = None
        self._typedetransaction	= None
        self._codepostal = None
        self._ville = None
        self._etage = None
        self._idtypechauffage = None
        self._idtypecuisine = None
        self._naturebien	= None
        self._si_balcon	= None
        self._nb_chambres = None 
        self._nb_pieces = None
        self._nb_pieces = None
        self._si_sdEau = None
        self._bain = None
        self._nb_photos = None
        self._prix = None
        self._surface = None

    def set_idannonce(self, value):
        "Renvoie une variable contenant la valeur de idannonce pour le bien "
        
        self._idannonce = int(value)

        return(self._idannonce)


    def set_typedebien(self, value):
        "Renvoie une variable contenant la valeur de typedebien pour le bien "
        if (value == "Appartement") | (value == "Maison / Villa") :
            self._typedebien = value

        else:
            self._typedebien = "Appartement"
        return(self._typedebien)


    def set_typedetransaction(self, value):
        "Renvoie une variable contenant la valeur de typedetransaction pour le bien "
        if (value == "['vente de prestige']") | (value == "['vente']") :
            self._typedetransaction = value
        else:
            self._typedetransaction = "['vente']"
        return(self._typedetransaction)


    def set_codepostal(self, value):
        "Renvoie une variable contenant la valeur de codepostal pour le bien "
        if (value == 33000) | (value == 33100) | (value == 33200) | (value == 33300) | (value == 33700) | (value == 33800) :
            self._codepostal = int(value)
        else:
            self._codepostal = 33000
        return(self._codepostal)


    def set_etage(self, value):
        "Renvoie une variable contenant la valeur de etage pour le bien"
        if (int(value) >= 0) | (int(value) <= 30 ):
            self._etage = int(value)
        else:
            self._etage = 0
        return(self._etage)


    def set_idtypechauffage(self, value):
        "Renvoie une variable contenant la valeur de idtypechauffage pour le bien "
        if (value == "individuel") | (value == "individuel électrique") | (value == "individuel électrique radiateur") | (value == "gaz") | (value == "individuel électrique") | (value == "mixte") | (value == "électrique") | (value == "individuel gaz sol") | (value == "gaz radiateur") | (value == "électrique mixte") :
            self._idtypechauffage = value
        else:
            self._idtypechauffage = "individuel"
        return(self._idtypechauffage)


    def set_idtypecuisine(self, value):
        "Renvoie une variable contenant la valeur de idtypecuisine pour le bien "
        if (value == "aucune") | (value == "coin cuisine") | (value == "équipée") | (value == "séparée") | (value == "	séparée équipée") | (value == "américaine") | (value == "américaine équipée") :
            self._idtypecuisine = value
        else:
            self._idtypecuisine = "aucune"
        return(self._idtypecuisine)


    def set_si_balcon(self, value):
        "Renvoie une variable contenant la valeur de si_balcon pour le bien "
        
        if (int(value) == 0) | (int(value) == 1 ):
            self._si_balcon = int(value)
        else:
            self._si_balcon = 0
        return(self._si_balcon)

    def set_nb_chambres(self, value):
        "Renvoie une variable contenant la valeur de nb_chambres pour le bien "
        if (int(value) >= 0) | (int(value) <= 10 ):
            self._nb_chambres = int(value)
        else:
            self._nb_chambres = 0
        return(self._nb_chambres)

    def set_nb_pieces(self, value):
        "Renvoie une variable contenant la valeur de nb_pieces pour le bien "
        if (int(value) >= 0) | (int(value) <= 10 ):
            self._nb_pieces = int(value)
        else:
            self._nb_pieces = 0
        return(self._nb_pieces)


    def set_si_sdeau(self, value):
        "Renvoie une variable contenant la valeur de si_sdEau pour le bien "
        if (int(value) == 0) | (int(value) == 1 ):
            self._si_sdEau = int(value)
        else:
            self._si_sdEau = 0
        return(self._si_sdEau)


    def set_si_sdbain(self, value):
        "Renvoie une variable contenant la valeur de si_sdEau pour le bien "
        if (int(value) == 0) | (int(value) == 1 ):
            self._si_sdbain = int(value)
        else:
            self._si_sdbain = 0
        return(self._si_sdbain)

    def set_prix(self, value):
        "Renvoie une variable contenant la valeur de prix pour le bien "
        self._prix = int(value)
        
        return(self._prix)

    def set_surface(self, value):
        "Renvoie une variable contenant la valeur de surface pour le bien "
        if (int(value) >= 0) | (int(value) <= 900 ):
            self._surface = int(value)
        else:
            self._surface = 0
        return(self._surface)
    