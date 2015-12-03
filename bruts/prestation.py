from . import Fichier
from interfaces import Interfaces


class Prestation(Fichier):
    """prestation du catalogue"""

    def __init__(self, nom_dossier, delimiteur, encodage):
        cles = ['annee', 'mois', 'id_prestation', 'designation', 'categorie', 'unite_prest', 'prix_unit',
                'val_moy_achat', 'cout_unit', 'prix_rev_unit']
        nom_fichier = "prestation.csv"
        libelle = "Prestations"
        Fichier.__init__(self, libelle, cles, nom_dossier + nom_fichier, delimiteur, encodage)

    def contient_id(self, id_prestation):
        for prestation in self.donnees:
            if prestation['id_prestation'] == id_prestation:
                return 1
        return 0

    def est_coherent(self, generaux):
        msg = ""
        ligne = 1
        ids = []
        donnees_dict = {}

        for donnee in self.donnees:
            if donnee['id_prestation'] == "":
                msg += "le prestation id de la ligne " + ligne + " ne peut être vide\n"
            elif donnee['id_prestation'] not in ids:
                ids.append(donnee['id_prestation'])
                del donnee['annee']
                del donnee['mois']
                donnees_dict[donnee['id_prestation']] = donnee
            else:
                msg += "l'id prestation '" + donnee['id_prestation'] + "' de la ligne " + ligne +\
                       " n'est pas unique\n"

            if donnee['categorie'] == "":
                msg += "la catégorie  de la ligne " + ligne + " ne peut être vide\n"
            elif donnee['categorie'] not in generaux.obtenir_d3():
                msg += "la catégorie '" + donnee['categorie'] + "' de la ligne " + ligne +\
                       " n'existe pas dans les paramètres D3\n"

            ligne += 1

        self.donnees = donnees_dict

        if msg != "":
            msg = self.libelle + "\n" + msg
            print("msg : " + msg)
            Interfaces.log_erreur(msg)
            return 1
        return 0
