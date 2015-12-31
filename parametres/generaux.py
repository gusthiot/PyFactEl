import csv
import sys
from interfaces import Interfaces


class Generaux(object):
    """
    Classe pour l'importation des paramètres généraux
    """

    cles = ['origine', 'code_int', 'code_ext', 'commerciale', 'canal', 'secteur', 'financier', 'fond', 'entete',
            'poste_emolument', 'code_t', 'code_n', 'nature_client', 'code_d', 'code_sap', 'quantite', 'unite',
            'type_prix', 'type_rabais', 'texte_sap']
    nom_fichier = "paramgen.csv"
    libelle = "Paramètres Généraux"

    def __init__(self, nom_dossier, delimiteur, encodage):
        """
        initialisation de la structure des données et du nom et de la position du fichier importé
        :param nom_dossier: nom du dossier où se trouve le fichier à importer
        :param delimiteur: code délimiteur de champ dans le fichier csv
        :param encodage: encodage du texte
        """
        donnees_csv = []
        try:
            csv_fichier = open(nom_dossier + Generaux.nom_fichier, newline='', encoding=encodage)
            fichier_reader = csv.reader(csv_fichier, delimiter=delimiteur, quotechar='|')
            for ligne in fichier_reader:
                donnees_csv.append(ligne)
        except IOError:
            Interfaces.log_erreur("impossible d'ouvrir le fichier : "+Generaux.nom_fichier)
            sys.exit("Erreur I/O")

        num = len(Generaux.cles)
        if len(donnees_csv) != num:
            info = Generaux.libelle + ": nombre de lignes incorrect : " + str(len(donnees_csv)) + ", attendu : " + \
                   str(num)
            print(info)
            Interfaces.log_erreur(info)
            sys.exit("Erreur de consistance")

        self.donnees = {}
        for xx in range(0, num):
            donnee = donnees_csv[xx]
            while "" in donnee:
                donnee.remove("")
            del(donnee[0])
            self.donnees[Generaux.cles[xx]] = donnee

    def obtenir_code_n(self):
        """
        retourne les codes N
        :return: codes N
        """
        return self.donnees['code_n'][1:]

    def obtenir_d3(self):
        """
        retourne les codes D3
        :return: codes D3
        """
        return self.donnees['code_d'][4:]
