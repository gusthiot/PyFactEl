from importes import Fichier
from interfaces import Interfaces


class Prestation(Fichier):
    """
    Classe pour l'importation des données de Prestations du catalogue
    """

    def __init__(self, nom_dossier, delimiteur, encodage):
        """
        initialisation de la structure des données et du nom et de la position du fichier importé
        :param nom_dossier: nom du dossier où se trouve le fichier à importer
        :param delimiteur: code délimiteur de champ dans le fichier csv
        :param encodage: encodage du texte
        """
        cles = ['annee', 'mois', 'id_prestation', 'designation', 'categorie', 'unite_prest', 'prix_unit',
                'val_moy_achat', 'cout_unit', 'prix_rev_unit']
        nom_fichier = "prestation.csv"
        libelle = "Prestations"
        Fichier.__init__(self, libelle, cles, nom_dossier + nom_fichier, delimiteur, encodage)

    def contient_id(self, id_prestation):
        """
        vérifie si une prestation contient l'id donné
        :param id_prestation: id à vérifier
        :return: 1 si id contenu, 0 sinon
        """
        if self.verifie_coherence == 1:
            for cle, prestation in self.donnees.items():
                if prestation['id_prestation'] == id_prestation:
                    return 1
        else:
            for prestation in self.donnees:
                if prestation['id_prestation'] == id_prestation:
                    return 1
        return 0

    def est_coherent(self, generaux):
        """
        vérifie que les données du fichier importé sont cohérentes (id prestation unique,
        catégorie prestation présente dans les paramètres D3), et efface les colonnes mois et année
        :param generaux: paramètres généraux
        :return: 1 s'il y a une erreur, 0 sinon
        """
        if self.verifie_date == 0:
            info = self.libelle + ". vous devez vérifier la date avant de vérifier la cohérence"
            print(info)
            Interfaces.log_erreur(info)
            return 1

        if self.verifie_coherence == 1:
            print(self.libelle + ": cohérence déjà vérifiée")
            return 0

        msg = ""
        ligne = 1
        ids = []
        donnees_dict = {}

        for donnee in self.donnees:
            if donnee['id_prestation'] == "":
                msg += "le prestation id de la ligne " + ligne + " ne peut être vide\n"
            elif donnee['id_prestation'] not in ids:
                ids.append(donnee['id_prestation'])
                del donnee['annee']
                del donnee['mois']
                donnees_dict[donnee['id_prestation']] = donnee
            else:
                msg += "l'id prestation '" + donnee['id_prestation'] + "' de la ligne " + ligne +\
                       " n'est pas unique\n"

            if donnee['categorie'] == "":
                msg += "la catégorie  de la ligne " + ligne + " ne peut être vide\n"
            elif donnee['categorie'] not in generaux.obtenir_d3():
                msg += "la catégorie '" + donnee['categorie'] + "' de la ligne " + ligne +\
                       " n'existe pas dans les paramètres D3\n"

            donnee['prix_unit'], info = self.est_un_nombre(donnee['prix_unit'], "le prix unitaire", ligne)
            msg += info
            donnee['val_moy_achat'], info = self.est_un_nombre(donnee['val_moy_achat'], "la valeur moyenne d'achat",
                                                               ligne)
            msg += info
            donnee['cout_unit'], info = self.est_un_nombre(donnee['cout_unit'], "le coût unitaire", ligne)
            msg += info
            donnee['prix_rev_unit'], info = self.est_un_nombre(donnee['prix_rev_unit'], "le prix de revient unitaire",
                                                               ligne)
            msg += info

            ligne += 1

        self.donnees = donnees_dict
        self.verifie_coherence = 1

        if msg != "":
            msg = self.libelle + "\n" + msg
            print("msg : " + msg)
            Interfaces.log_erreur(msg)
            return 1
        return 0
