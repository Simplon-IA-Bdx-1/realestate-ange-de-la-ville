class Annonce:

    def __init__(self,idannonce, typedebien, typedetransaction, codepostal, ville, etage, idtypechauffage, idtypecuisine, naturebien, si_balcon, nb_chambres, nb_pieces, si_sdbain, si_sdEau,nb_photos,prix, surface):
        self.idannonce = idannonce
        self.typedebien	 = typedebien
        self.typedetransaction	= typedetransaction
        self.codepostal = codepostal
        self.ville = ville
        self.etage = etage
        self.idtypechauffage = idtypechauffage
        self.idtypecuisine = idtypecuisine
        self.naturebien	= naturebien
        self.si_balcon	= si_balcon
        self.nb_chambres = nb_chambres 
        self.nb_pieces = nb_pieces
        self.si_sdbain = si_sdbain
        self.si_sdEau = si_sdEau
        self.nb_photos = nb_photos
        self.prix = prix
        self.surface = surface
