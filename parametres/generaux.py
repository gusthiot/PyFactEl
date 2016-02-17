import csv
import sys
from outils import Outils
from erreurs import ErreurConsistance
from collections import namedtuple

_champs_article = ["code_d", "code_sap", "quantite", "unite", "type_prix",
                   "type_rabais", "texte_sap"]
Article = namedtuple("Article", _champs_article)

class Generaux(object):
    """
    Classe pour l'importation des paramètres généraux
    """

    nom_fichier = "paramgen.csv"
    libelle = "Paramètres Généraux"
    cles_obligatoires = ['origine', 'code_int', 'code_ext', 'commerciale', 'canal', 'secteur', 'devise', 'financier', 'fonds',
            'entete', 'poste_emolument', 'lien', 'chemin', 'code_t', 'code_n', 'nature_client', 'code_d', 'code_sap', 'quantite',
            'unite', 'type_prix', 'type_rabais', 'texte_sap', 'modes']
    cles_autorisees = cles_obligatoires + ['code_sap_qas']

    def __init__(self, dossier_source, prod2qual=None):
        """
        initialisation et importation des données

        :param dossier_source: Une instance de la classe dossier.DossierSource
        :param prod2qual: Une instance de la classe Prod2Qual si on souhaite éditer
                          des factures et annexes avec les codes d'articles de
                          qualification
        """
        self.donnees = {}
        try:
            for ligne in dossier_source.reader(self.nom_fichier):
                cle = ligne.pop(0)
                if cle not in self.cles_autorisees:
                    Outils.fatal(ErreurConsistance(),
                                 "Clé inconnue dans %s: %s" % (self.nom_fichier, cle))
                while "" in ligne:
                    ligne.remove("")
                self.donnees[cle] = ligne
        except IOError as e:
            Outils.fatal(e, "impossible d'ouvrir le fichier : "+Generaux.nom_fichier)
        if prod2qual and 'code_sap_qas' in self.donnees:
            self.donnees['code_sap'] = self.donnees['code_sap_qas']

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

    def obtenir_modes_envoi(self):
        """
        retourne les modes d'envoi
        :return: modes d'envoi
        """
        return self.donnees['modes'][1:]

    @property
    def fonds(self):
        return self.donnees['fonds'][1]

    @property
    def articles(self):
        """renvoie la liste des articles de facturation.

        Le premier (émolument) s'appelle "D1"; les deux seconds (prix
        plafonnés / non plafonnés) s'appellent "D2"; les suivants (en nombre
        variable) s'appellent "D3".

        :return: une liste ordonnée d'objets Article
        """
        if not hasattr(self, "_articles"):
            self._articles = []
            for i in range(1, len(self.donnees['code_d'])):
                kw = dict((k, self.donnees[k][i]) for k in _champs_article)
                self._articles.append(Article(**kw))
        return self._articles

    @property
    def articles_d3(self):
        """
        retourne uniquement les articles D3

        :return: une liste ordonnée d'objets Article
        """
        return self.articles[3:]

    def obtenir_d3(self):
        return [a.code_d for a in self.articles_d3]

    @property
    def centre_financier(self):
        return self.donnees['financier'][1]

    @property
    def poste_emolument(self):
        return self.donnees['poste_emolument'][1]

    @property
    def code_t(self):
        return self.donnees['code_t'][1]
