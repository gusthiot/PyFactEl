from importes import Fichier
from interfaces import Interfaces


class Compte(Fichier):
    """
    Classe pour l'importation des données de Comptes Cmi
    """

    def __init__(self, nom_dossier, delimiteur, encodage):
        """
        initialisation de la structure des données et du nom et de la position du fichier importé
        :param nom_dossier: nom du dossier où se trouve le fichier à importer
        :param delimiteur: code délimiteur de champ dans le fichier csv
        :param encodage: encodage du texte
        """
        cles = ['annee', 'mois', 'id_compte', 'intitule', 'categorie', 'code_client', 'abrev_labo', 'seuil', 'pourcent']
        nom_fichier = "compte.csv"
        libelle = "Comptes"
        Fichier.__init__(self, libelle, cles, nom_dossier + nom_fichier, delimiteur, encodage)

    def contient_id(self, id_compte):
        """
        vérifie si un compte contient l'id donné
        :param id_compte: id à vérifier
        :return: 1 si id contenu, 0 sinon
        """
        if self.verifie_coherence == 1:
            for cle, compte in self.donnees.items():
                if compte['id_compte'] == id_compte:
                    return 1
        else:
            for compte in self.donnees:
                if compte['id_compte'] == id_compte:
                    return 1
        return 0

    def est_coherent(self, clients, clients_actifs):
        """
        vérifie que les données du fichier importé sont cohérentes (code client dans clients,
        ou alors absent des clients actifs, id compte unique), et efface les colonnes mois et année
        :param clients: clients importés
        :param clients_actifs: codes des clients présents dans accès, réservations et livraisons
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
        codes = []
        ids = []
        donnees_dict = {}

        for donnee in self.donnees:
            if donnee['code_client'] == "":
                print("code client du compte vide")
                msg += "le code client de la ligne " + str(ligne) + " ne peut être vide\n"
            elif donnee['code_client'] not in codes:
                codes.append(donnee['code_client'])

            if donnee['id_compte'] == "":
                msg += "le compte id de la ligne " + ligne + " ne peut être vide\n"
            elif donnee['id_compte'] not in ids:
                ids.append(donnee['id_compte'])
                del donnee['annee']
                del donnee['mois']
                donnees_dict[donnee['id_compte']] = donnee
            else:
                msg += "l'id compte '" + donnee['id_compte'] + "' de la ligne " + ligne +\
                       " n'est pas unique\n"

            donnee['seuil'], info = self.est_un_nombre(donnee['seuil'], "le seuil", ligne)
            if info != "":
                print(info)
            msg += info + "\n"
            donnee['pourcent'], info = self.est_un_nombre(donnee['pourcent'], "le pourcent après seuil", ligne)
            if info != "":
                print(info)
            msg += info + "\n"

            ligne += 1

        self.donnees = donnees_dict
        self.verifie_coherence = 1

        for code in codes:
            if code not in clients.obtenir_codes():
                if code in clients_actifs:
                    msg += "la code client '" + code + "' n'est pas présente dans les clients\n"

        if msg != "":
            msg = self.libelle + "\n" + msg
            print("msg : " + msg)
            Interfaces.log_erreur(msg)
            return 1
        return 0
