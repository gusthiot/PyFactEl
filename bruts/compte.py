from . import Fichier
from interfaces import Interfaces


class Compte(Fichier):
    """compte client du CMi"""

    def __init__(self, nom_dossier, delimiteur, encodage):
        cles = ['annee', 'mois', 'id_compte', 'intitule', 'categorie', 'code_client', 'abrev_labo', 'seuil', 'pourcent']
        nom_fichier = "compte.csv"
        libelle = "Comptes"
        Fichier.__init__(self, libelle, cles, nom_dossier + nom_fichier, delimiteur, encodage)

    def contient_id(self, id_compte):
        for compte in self.donnees:
            if compte['id_compte'] == id_compte:
                return 1
        return 0

    def est_coherent(self, client, coefmachines, coefprests, generaux, clients_actifs):
        msg = ""
        ligne = 1
        codes = []
        ids = []
        donnees_dict = {}

        for donnee in self.donnees:
            if donnee['code_client'] == "":
                print("code client du compte vide")
                # msg += "le code client de la ligne " + str(ligne) + " ne peut être vide\n"
            elif donnee['code_client'] not in codes:
                codes.append(donnee['code_client'])

            if donnee['id_compte'] == "":
                msg += "le compte id de la ligne " + ligne + " ne peut être vide\n"
            elif donnee['id_compte'] not in ids:
                ids.append(donnee['id_compte'])
                del donnee['annee']
                del donnee['mois']
                donnees_dict[donnee['id_compte']] = donnee
            else:
                msg += "l'id compte '" + donnee['id_compte'] + "' de la ligne " + ligne +\
                       " n'est pas unique\n"

            ligne += 1

        self.donnees = donnees_dict

        for code in codes:
            if code not in client.obtenir_codes(coefmachines, coefprests, generaux):
                if code in clients_actifs:
                    msg += "la code client '" + code + "' n'est pas présente dans les clients\n"

        if msg != "":
            msg = self.libelle + "\n" + msg
            print("msg : " + msg)
            Interfaces.log_erreur(msg)
            return 1
        return 0
