from importes import Fichier
from interfaces import Interfaces


class CoefMachine(Fichier):
    """coefficient de machine"""

    def __init__(self, nom_dossier, delimiteur, encodage):
        cles = ['annee', 'mois', 'id_classe_tarif', 'intitule', 'categorie', 'coef_p', 'coef_np', 'coef_mo']
        nom_fichier = "coeffmachine.csv"
        libelle = "Coefficients Machines"
        Fichier.__init__(self, libelle, cles, nom_dossier + nom_fichier, delimiteur, encodage)
        self.classes = []

    def obtenir_classes(self):
        if len(self.classes) == 0:
            self.est_coherent()
        return self.classes

    def contient_categorie(self, categorie):
        for coefmachine in self.donnees:
            if coefmachine['categorie'] == categorie:
                return 1
        return 0

    def est_coherent(self):
        msg = ""
        ligne = 1
        categories = []
        couples = []
        donnees_dict = {}

        for donnee in self.donnees:
            if donnee['categorie'] == "":
                msg += "la catégorie de la ligne " + ligne + " ne peut être vide\n"
            elif donnee['categorie'] not in categories:
                categories.append(donnee['categorie'])

            if donnee['id_classe_tarif'] == "":
                msg += "la classe de tarif de la ligne ne peut être vide\n"
            elif donnee['id_classe_tarif'] not in self.classes:
                self.classes.append(donnee['id_classe_tarif'])

            if (donnee['categorie'] != "") and (donnee['id_classe_tarif'] != ""):
                couple = [donnee['categorie'], donnee['id_classe_tarif']]
                if couple not in couples:
                    couples.append(couple)
                    del donnee['annee']
                    del donnee['mois']
                    donnees_dict[donnee['id_classe_tarif']+donnee['categorie']] = donnee
                else:
                    msg += "Couple categorie '" + donnee['categorie'] + "' et classe de tarif '" + \
                           donnee['id_classe_tarif'] + "' de la ligne " + ligne + " pas unique\n"

            donnee['coef_p'], info = self.est_un_nombre(donnee['coef_p'], "le coefficient P", ligne)
            msg += info
            donnee['coef_np'], info = self.est_un_nombre(donnee['coef_np'], "le coefficient NP", ligne)
            msg += info
            donnee['coef_mo'], info = self.est_un_nombre(donnee['coef_mo'], "le coefficient MO", ligne)
            msg += info

            ligne += 1

        self.donnees = donnees_dict

        for categorie in categories:
            for classe in self.classes:
                couple = [categorie, classe]
                if couple not in couples:
                    msg += "Couple categorie '" + categorie + "' et classe de tarif '" + \
                           classe + "' n'existe pas\n"

        if msg != "":
            msg = self.libelle + "\n" + msg
            print("msg : " + msg)
            Interfaces.log_erreur(msg)
            return 1
        return 0