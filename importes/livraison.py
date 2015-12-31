from importes import Fichier
from interfaces import Interfaces


class Livraison(Fichier):
    """
    Classe pour l'importation des données de Livraisons
    """

    def __init__(self, nom_dossier, delimiteur, encodage):
        """
        initialisation de la structure des données et du nom et de la position du fichier importé
        :param nom_dossier: nom du dossier où se trouve le fichier à importer
        :param delimiteur: code délimiteur de champ dans le fichier csv
        :param encodage: encodage du texte
        """
        cles = ['annee', 'mois', 'id_compte', 'intitule_compte', 'code_client', 'abrev_labo', 'id_user', 'nom_user',
                'prenom_user', 'num_projet', 'intitule_projet', 'id_prestation', 'designation', 'date_livraison',
                'quantite', 'unite', 'rabais', 'responsable', 'id_livraison', 'date_commande', 'date_prise', 'remarque']
        nom_fichier = "lvr.csv"
        libelle = "Livraison Prestations"
        Fichier.__init__(self, libelle, cles, nom_dossier + nom_fichier, delimiteur, encodage)
        self.codes = []

    def obtenir_codes(self, comptes, prestations):
        """
        retourne la liste de tous les codes clients
        :param comptes: comptes importés
        :param prestations: prestations importées
        :return: liste des codes clients présents dans les données livraisons importées
        """
        if len(self.codes) == 0:
            self.est_coherent(comptes, prestations)
        return self.codes

    def est_coherent(self, comptes, prestations):
        """
        vérifie que les données du fichier importé sont cohérentes (id compte parmi comptes,
        id prestation parmi prestations), et efface les colonnes mois et année
        :param comptes: comptes importés
        :param prestations: prestations importées
        :return: 1 s'il y a une erreur, 0 sinon
        """
        msg = ""
        ligne = 1
        donnees_list = []

        for donnee in self.donnees:
            if donnee['id_compte'] == "":
                msg += "le compte id de la ligne " + ligne + " ne peut être vide\n"
                continue
            if donnee['id_prestation'] == "":
                msg += "le prestation id de la ligne " + ligne + " ne peut être vide\n"
                continue

            if comptes.contient_id(donnee['id_compte']) == 0:
                msg += "le compte id '" + donnee['id_compte'] + "' de la ligne " + ligne + " n'est pas référencé\n"
            if prestations.contient_id(donnee['id_prestation']) == 0:
                msg += "le prestation id '" + donnee['id_prestation'] + "' de la ligne " + ligne +\
                       " n'est pas référencé\n"

            if donnee['code_client'] not in self.codes:
                self.codes.append(donnee['code_client'])

            donnee['quantite'], info = self.est_un_nombre(donnee['quantite'], "la quantité", ligne)
            msg += info
            donnee['rabais'], info = self.est_un_nombre(donnee['rabais'], "le rabais", ligne)
            msg += info

            del donnee['annee']
            del donnee['mois']
            donnees_list.append(donnee)

            ligne += 1

        self.donnees = donnees_list

        if msg != "":
            msg = self.libelle + "\n" + msg
            print("msg : " + msg)
            Interfaces.log_erreur(msg)
            return 1
        return 0

    def calcul_montants(self, prestations, coefprests, comptes, clients):
        """
        calcule le 'montant' et le 'rabais_r' et les ajoute aux données
        :param prestations: prestations importées
        :param coefprests: coefficients prestations importés
        :param comptes: comptes importés
        :param clients: clients importés
        """
        donnees_list = []
        for donnee in self.donnees:
            prestation = prestations.donnees[donnee['id_prestation']]
            compte = comptes.donnees[donnee['id_compte']]
            client = clients.donnees[compte['code_client']]
            coefprest = coefprests.donnees[client['id_classe_tarif'] + prestation['categorie']]
            donnee['montant'] = round(donnee['quantite'] * round(prestation['prix_unit'] *
                                                                 coefprest['coefficient'], 2), 2)
            donnee['rabais_r'] = round(donnee['rabais'], 2)
            donnees_list.append(donnee)
        self.donnees = donnees_list

    def livraisons_pour_projet_par_categorie(self, num_projet, id_compte, code_client, prestations):
        """
        retourne les livraisons pour un projet donné, pour une catégorie de prestations donnée
        :param num_projet: lenuméro de projet
        :param id_compte: l'id du compte
        :param code_client: le code du client
        :param prestations: prestations importées
        :return: les livraisons pour le projet donné, pour une catégorie de prestations donnée
        """
        donnees_dico = {}
        for donnee in self.donnees:
            if (donnee['id_compte'] == id_compte) and (donnee['code_client'] == code_client) \
                    and (donnee['num_projet'] == num_projet):
                categorie = prestations.donnees[donnee['id_prestation']]['categorie']
                if categorie not in donnees_dico:
                    donnees_dico[categorie] = []
                liste = donnees_dico[categorie]
                liste.append(donnee)
        return donnees_dico
