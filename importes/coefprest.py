from importes import Fichier
from interfaces import Interfaces


class CoefPrest(Fichier):
    """
    Classe pour l'importation des données de Coefficients Prestations
    """

    def __init__(self, nom_dossier, delimiteur, encodage):
        """
        initialisation de la structure des données et du nom et de la position du fichier importé
        :param nom_dossier: nom du dossier où se trouve le fichier à importer
        :param delimiteur: code délimiteur de champ dans le fichier csv
        :param encodage: encodage du texte
        """
        cles = ['annee', 'mois', 'id_classe_tarif', 'intitule', 'categorie', 'nom_categorie', 'coefficient']
        nom_fichier = "coeffprestation.csv"
        libelle = "Coefficients Prestations"
        Fichier.__init__(self, libelle, cles, nom_dossier + nom_fichier, delimiteur, encodage)
        self.classes = []

    def obtenir_classes(self):
        """
        retourne toutes les classes de tarif présentes
        :return: toutes les classes de tarif présentes
        """
        if len(self.classes) == 0:
            self.est_coherent()
        return self.classes

    def est_coherent(self):
        """
        vérifie que les données du fichier importé sont cohérentes (si couple catégorie - classe de tarif est unique),
        et efface les colonnes mois et année
        :return: 1 s'il y a une erreur, 0 sinon
        """
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
                           donnee['id_classe_tarif'] + "' de la ligne " + str(ligne) + " pas unique\n"

            donnee['coefficient'], info = self.est_un_nombre(donnee['coefficient'], "le coefficient", ligne)
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
