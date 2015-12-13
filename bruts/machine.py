from . import Fichier
from interfaces import Interfaces


class Machine(Fichier):
    """machine du CMi"""

    def __init__(self, nom_dossier, delimiteur, encodage):
        cles = ['annee', 'mois', 'id_machine', 'nom', 'categorie', 't_h_machine_hp_p', 't_h_machine_hp_np',
                't_h_operateur_hp_mo', 't_h_reservation_hp_p', 't_h_reservation_hp_np', 't_h_machine_hc_p',
                't_h_machine_hc_np', 't_h_operateur_hc_mo', 't_h_reservation_hc_p', 't_h_reservation_hc_np',
                'delai_sans_frais']
        nom_fichier = "machine.csv"
        libelle = "Machines"
        Fichier.__init__(self, libelle, cles, nom_dossier + nom_fichier, delimiteur, encodage)

    def contient_id(self, id_machine):
        ligne = 1
        for machine in self.donnees:
            if machine['id_machine'] == id_machine:
                return ligne
            ligne += 1
        return 0

    def est_coherent(self, coefmachines):
        msg = ""
        ligne = 1
        ids = []
        donnees_dict = {}

        for donnee in self.donnees:
            if donnee['id_machine'] == "":
                msg += "le machine id de la ligne " + ligne + " ne peut être vide\n"
            elif donnee['id_machine'] not in ids:
                ids.append(donnee['id_machine'])
                del donnee['annee']
                del donnee['mois']
                donnees_dict[donnee['id_machine']] = donnee
            else:
                msg += "l'id machine '" + donnee['id_machine'] + "' de la ligne " + ligne +\
                       " n'est pas unique\n"

            if donnee['categorie'] == "":
                msg += "la catégorie machine de la ligne " + ligne + " ne peut être vide\n"
            elif coefmachines.contient_categorie(donnee['categorie']) == 0:
                msg += "la catégorie machine '" + donnee['categorie'] + "' de la ligne " + ligne +\
                       " n'est pas référencé\n"

            ligne += 1

        self.donnees = donnees_dict

        if msg != "":
            msg = self.libelle + "\n" + msg
            print("msg : " + msg)
            Interfaces.log_erreur(msg)
            return 1
        return 0
