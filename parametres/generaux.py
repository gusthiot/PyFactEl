import csv
import sys
from outils import Outils
from erreurs import ErreurConsistance


class Generaux(object):
    """
    Classe pour l'importation des paramètres généraux
    """

    nom_fichier = "paramgen.csv"
    libelle = "Paramètres Généraux"
    cles_obligatoires = ['origine', 'code_int', 'code_ext', 'commerciale', 'canal', 'secteur', 'devise', 'financier', 'fonds',
            'entete', 'poste_emolument', 'lien', 'chemin', 'code_t', 'code_n', 'nature_client', 'code_d', 'code_sap', 'quantite',
            'unite', 'type_prix', 'type_rabais', 'texte_sap', 'modes']

    def __init__(self, dossier_source):
        """
        initialisation et importation des données

        :param dossier_source: Une instance de la classe dossier.DossierSource
        """
        self.donnees = {}
        try:
            for ligne in dossier_source.reader(self.nom_fichier):
                cle = ligne.pop(0)
                if cle not in self.cles_obligatoires:
                    Outils.fatal(ErreurConsistance(),
                                 "Clé inconnue dans %s: %s" % (self.nom_fichier, cle))
                while "" in ligne:
                    ligne.remove("")
                self.donnees[cle] = ligne
        except IOError as e:
            Outils.fatal(e, "impossible d'ouvrir le fichier : "+Generaux.nom_fichier)

        erreurs = ""
        for cle in self.cles_obligatoires:
            if cle not in self.donnees:
                erreurs += "\nClé manquante dans %s: %s" % (self.nom_fichier, cle)

        try:
            for quantite in self.donnees['quantite'][1:]:
                int(quantite)
        except ValueError:
            erreurs += "les quantités doivent être des nombres entiers\n"
        codes_n = []
        for nn in self.donnees['code_n'][1:]:
            if nn not in codes_n:
                codes_n.append(nn)
            else:
                erreurs += "le code N '" + nn + "' n'est pas unique\n"
        codes_d = []
        for dd in self.donnees['code_d'][1:]:
            if dd not in codes_d:
                codes_d.append(dd)
            else:
                erreurs += "le code D '" + dd + "' n'est pas unique\n"

        if len(self.donnees['code_n']) != len(self.donnees['nature_client']):
            erreurs += "le nombre de colonees doit être le même pour le code N et pour la nature du client\n"

        if (len(self.donnees['code_d']) != len(self.donnees['code_sap'])) or (len(self.donnees['code_d']) !=
                len(self.donnees['quantite'])) or (len(self.donnees['code_d']) !=
                len(self.donnees['unite'])) or (len(self.donnees['code_d']) !=
                len(self.donnees['type_prix'])) or (len(self.donnees['code_d']) !=
                len(self.donnees['type_rabais'])) or (len(self.donnees['code_d']) != len(self.donnees['texte_sap'])):
            erreurs += "le nombre de colonees doit être le même pour le code D, le code SAP, la quantité, l'unité, " \
                   "le type de prix, le type de rabais et le texte SAP\n"

        if erreurs != "":
            Outils.fatal(ErreurConsistance(), self.libelle + "\n" + erreurs)

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

    def obtenir_modes_envoi(self):
        """
        retourne les modes d'envoi
        :return: modes d'envoi
        """
        return self.donnees['modes'][1:]
