import csv
import sys
from interfaces import Interfaces


class Fichier(object):
    """base du fichier extracté"""

    def __init__(self, libelle, cles, nom_fichier, delimiteur, encodage):
        self.libelle = libelle
        self.cles = cles
        try:
            csv_fichier = open(nom_fichier, newline='', encoding=encodage)
            fichier_reader = csv.reader(csv_fichier, delimiter=delimiteur, quotechar='|')
            donnees_csv = []
            for ligne in fichier_reader:
                donnees_ligne = self.extraction_ligne(ligne)
                if donnees_ligne == -1:
                    continue
                donnees_csv.append(donnees_ligne)
            self.donnees = donnees_csv
        except IOError:
            Interfaces.log_erreur("impossible d'ouvrir le fichier : "+nom_fichier)
            sys.exit("Erreur I/O")

    def extraction_ligne(self, ligne):
        num = len(self.cles)
        if len(ligne) != num:
            info = self.libelle + ": nombre de colonnes incorrect : " + str(len(ligne)) + ", attendu : " + str(num)
            print(info)
            Interfaces.log_erreur(info)
            sys.exit("Erreur de consistance")
        donnees_ligne = {}
        for xx in range(0, num):
            donnees_ligne[self.cles[xx]] = ligne[xx]
        return donnees_ligne

    def verification_date(self, annee, mois):
        msg = ""
        position = 1
        for donnee in self.donnees:
            try:
                if (int(donnee['mois']) != mois) or (int(donnee['annee']) != annee):
                    msg += "date incorrect ligne " + str(position) + "\n"
            except ValueError:
                msg += "année ou mois n'est pas valable" + str(position) + "\n"
            position += 1

        del self.donnees[0]

        if msg != "":
            msg = self.libelle + "\n" + msg
            print("msg : " + msg)
            Interfaces.log_erreur(msg)
            return 1
        return 0
