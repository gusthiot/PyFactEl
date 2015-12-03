from . import Fichier
from interfaces import Interfaces


class Client(Fichier):
    """client du CMi"""


    def __init__(self, nom_dossier, delimiteur, encodage):
        cles = ['annee', 'mois', 'code', 'abrev_labo', 'nom_labo', 'ref', 'dest', 'type_labo', 'emol_base',
                'emol_base_mens', 'emol_fixe', 'coef', 'id_classe_tarif', 'classe_tarif']
        nom_fichier = "client.csv"
        libelle = "Clients"
        Fichier.__init__(self, libelle, cles, nom_dossier + nom_fichier, delimiteur, encodage)
        self.codes = []


    def obtenir_codes(self, coefmachines, coefprests):
        if len(self.codes) == 0:
            self.est_coherent(coefmachines, coefprests)
        return self.codes

    def est_coherent(self, coefmachines, coefprests, generaux):
        msg = ""
        ligne = 1
        classes = []
        donnees_dict = {}

        for donnee in self.donnees:
            if donnee['id_classe_tarif'] == "":
                msg += "la classe de tarif de la ligne " + ligne + " ne peut être vide\n"
            elif donnee['id_classe_tarif'] not in classes:
                classes.append(donnee['id_classe_tarif'])

            if donnee['code'] == "":
                msg += "le code client de la ligne " + str(ligne) + " ne peut être vide\n"
            elif donnee['code'] not in self.codes:
                self.codes.append(donnee['code'])
                del donnee['annee']
                del donnee['mois']
                donnees_dict[donnee['code']] = donnee
            else:
                msg += "le code client '" + donnee['code'] + "' de la ligne " + str(ligne) +\
                       " n'est pas unique\n"

            if donnee['type_labo'] == "":
                msg += "le type de labo de la ligne " + ligne + " ne peut être vide\n"
            elif donnee['type_labo'] not in generaux.obtenir_donnees_cle('code_n'):
                msg + "le type de labo '" + donnee['type_labo'] + "' de la ligne " + str(ligne) +\
                    " n'existe pas dans les types N\n"

            ligne += 1

        self.donnees = donnees_dict

        for classe in classes :
            if classe not in coefmachines.obtenir_classes():
                msg += "la classe de tarif '" + classe + "' n'est pas présente dans les coefficients machines\n"
            if classe not in coefprests.obtenir_classes():
                msg += "la classe de tarif '" + classe + "' n'est pas présente dans les coefficients prestations\n"

        if msg != "":
            msg = self.libelle + "\n" + msg
            print("msg : " + msg)
            Interfaces.log_erreur(msg)
            return 1
        return 0
