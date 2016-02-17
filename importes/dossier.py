import csv
import sys
import os
from contextlib import contextmanager

class _DossierBase(object):
    def __init__(self, chemin_dossier, encodage="cp1252", delimiteur=";"):
        """
        initialisation de l'objet

        :param chemin_dossier: Chemin du dossier
        :param delimiteur: code délimiteur des champs dans les fichier csv
        :param encodage: encodage des fichiers texte (CSV ou HTML)
        """
        self.chemin = chemin_dossier
        self.delimiteur = delimiteur
        self.quotechar = "|"
        self.encodage = encodage

    def _open(self, chemin_relatif, flags):
        return open(self._chemin(chemin_relatif), flags, newline='',
                    encoding=self.encodage)

    def _chemin(self, chemin_relatif):
        return os.path.join(self.chemin, chemin_relatif)

    def existe(self, chemin_relatif):
        return os.path.exists(self._chemin(chemin_relatif))


class DossierSource(_DossierBase):
    """
    Source de données.

    Une instance représente un répertoire de données source avec tous les réglages
    idoines du parseur (délimiteur, format de caractères). La méthode reader()
    permet d'ouvrir un CSV par nom relatif.
    """
    def reader(self, chemin_relatif):
        return csv.reader(self._open(chemin_relatif, "r"), delimiter=self.delimiteur,
                          quotechar=self.quotechar)

    def DictReader(self, chemin_relatif):
        return csv.DictReader(self._open(chemin_relatif, "r"), delimiter=self.delimiteur,
                          quotechar=self.quotechar)

class DossierDestination(_DossierBase):
    """Destination de données.

    Une instance représente un répertoire de données de destination
    avec tous les réglages idoines (délimiteur CSV, format de
    caractères). La méthode open() permet de créer un fichier par nom
    relatif. La méthode csv_writer() fait de même, mais avec un objet
    csv.writer plutôt qu'un descripteur de fichier.
    """

    @contextmanager
    def open(self, chemin_relatif):
        with self._open(chemin_relatif, "w") as fichier:
            yield fichier

    @contextmanager
    def writer(self, chemin_relatif):
        with self._open(chemin_relatif, "w") as csv_fichier:
            yield csv.writer(csv_fichier, delimiter=self.delimiteur,
                             quotechar=self.quotechar)

