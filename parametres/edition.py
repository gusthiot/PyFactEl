import csv
import sys
from outils import Outils


class Edition(object):
    """
    Classe pour l'importation des paramètres d'édition
    """

    nom_fichier = "paramedit.csv"
    libelle = "Paramètres d'Edition"

    def __init__(self, nom_dossier, delimiteur, encodage):
        """
        initialisation de la structure des données et du nom et de la position du fichier importé
        :param nom_dossier: nom du dossier où se trouve le fichier à importer
        :param delimiteur: code délimiteur de champ dans le fichier csv
        :param encodage: encodage du texte
        """
        donnees_csv = []
        try:
            self.nom_fichier = nom_dossier + Edition.nom_fichier
            csv_fichier = open(self.nom_fichier, newline='', encoding=encodage)
            fichier_reader = csv.reader(csv_fichier, delimiter=delimiteur, quotechar='|')
            for ligne in fichier_reader:
                donnees_csv.append(ligne)
        except IOError:
            Outils.affiche_message("impossible d'ouvrir le fichier : "+Edition.nom_fichier)
            sys.exit("Erreur I/O")

        num = 3
        if len(donnees_csv) != num:
            info = Edition.libelle + ": nombre de lignes incorrect : " + str(len(donnees_csv)) \
                   + ", attendu : " + str(num)
            print(info)
            Outils.affiche_message(info)
            sys.exit("Erreur de consistance")
        try:
            self.annee = int(donnees_csv[0][1])
            self.mois = int(donnees_csv[1][1])
        except ValueError:
            info = Edition.libelle + "\nle mois et l'année doivent être des nombres"
            Outils.affiche_message(info)
            sys.exit("Erreur de consistance")

        self.version = donnees_csv[2][1]
