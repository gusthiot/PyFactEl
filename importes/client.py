from importes import Fichier
from outils import Outils


class Client(Fichier):
    """
    Classe pour l'importation des données de Clients Cmi
    """

    def __init__(self, nom_dossier, delimiteur, encodage):
        """
        initialisation de la structure des données et du nom et de la position du fichier importé
        :param nom_dossier: nom du dossier où se trouve le fichier à importer
        :param delimiteur: code délimiteur de champ dans le fichier csv
        :param encodage: encodage du texte
        """
        cles = ['annee', 'mois', 'code', 'abrev_labo', 'nom_labo', 'ref', 'dest', 'type_labo', 'emol_sans_activite',
                'emol_base_mens', 'emol_fixe', 'coef', 'id_classe_tarif', 'classe_tarif']
        nom_fichier = "client.csv"
        libelle = "Clients"
        Fichier.__init__(self, libelle, cles, nom_dossier + nom_fichier, delimiteur, encodage)
        self.codes = []

    def obtenir_codes(self):
        """
        retourne les codes de tous les clients
        :return: codes de tous les clients
        """
        if self.verifie_coherence == 0:
            info = self.libelle + ". vous devez vérifier la cohérence avant de pouvoir obtenir les codes"
            print(info)
            Outils.affiche_message(info)
            return []
        return self.codes

    def est_coherent(self, coefmachines, coefprests, generaux):
        """
        vérifie que les données du fichier importé sont cohérentes (code client unique,
        classe tarif présente dans coefficients, type de labo dans paramètres), et efface les colonnes mois et année
        :param coefmachines: coefficients machines importés
        :param coefprests: coefficients prestations importés
        :param generaux: paramètres généraux
        :return: 1 s'il y a une erreur, 0 sinon
        """
        if self.verifie_date == 0:
            info = self.libelle + ". vous devez vérifier la date avant de vérifier la cohérence"
            print(info)
            Outils.affiche_message(info)
            return 1

        if self.verifie_coherence == 1:
            print(self.libelle + ": cohérence déjà vérifiée")
            return 0

        msg = ""
        ligne = 1
        classes = []
        donnees_dict = {}

        for donnee in self.donnees:
            if donnee['id_classe_tarif'] == "":
                msg += "la classe de tarif de la ligne " + str(ligne) + " ne peut être vide\n"
            elif donnee['id_classe_tarif'] not in classes:
                classes.append(donnee['id_classe_tarif'])

            if donnee['code'] == "":
                msg += "le code client de la ligne " + str(ligne) + " ne peut être vide\n"
            elif donnee['code'] not in self.codes:
                self.codes.append(donnee['code'])
                del donnee['annee']
                del donnee['mois']
                donnees_dict[donnee['code']] = donnee
            else:
                msg += "le code client '" + donnee['code'] + "' de la ligne " + str(ligne) +\
                       " n'est pas unique\n"

            if donnee['type_labo'] == "":
                msg += "le type de labo de la ligne " + str(ligne) + " ne peut être vide\n"
            elif donnee['type_labo'] not in generaux.obtenir_code_n():
                msg += "le type de labo '" + donnee['type_labo'] + "' de la ligne " + str(ligne) +\
                    " n'existe pas dans les types N\n"

            if not((donnee['emol_sans_activite'] == "NON") or (donnee['emol_sans_activite'] == "ZERO") or
                    (donnee['emol_sans_activite'] == "OUI")):
                msg += "l'émolument à payer même sans activité de la ligne " + ligne + " doit valoir ZERO, NON ou OUI\n"

            donnee['emol_base_mens'], info = Outils.est_un_nombre(donnee['emol_base_mens'], "l'émolument de base",
                                                                  ligne)
            msg += info
            donnee['emol_fixe'], info = Outils.est_un_nombre(donnee['emol_fixe'], "l'émolument fixe", ligne)
            msg += info
            donnee['coef'], info = Outils.est_un_nombre(donnee['coef'], "le coefficient a", ligne)
            msg += info

            ligne += 1

        self.donnees = donnees_dict
        self.verifie_coherence = 1

        for classe in classes:
            if classe not in coefmachines.obtenir_classes():
                msg += "la classe de tarif '" + classe + "' n'est pas présente dans les coefficients machines\n"
            if classe not in coefprests.obtenir_classes():
                msg += "la classe de tarif '" + classe + "' n'est pas présente dans les coefficients prestations\n"

        if msg != "":
            msg = self.libelle + "\n" + msg
            print("msg : " + msg)
            Outils.affiche_message(msg)
            return 1
        return 0
