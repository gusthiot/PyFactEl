from . import Fichier
from interfaces import Interfaces


class Reservation(Fichier):
    """Réservation"""

    def __init__(self, nom_dossier, delimiteur, encodage):
        cles = ['annee', 'mois', 'id_compte', 'intitule_compte', 'code_client', 'abrev_labo', 'id_user', 'nom_user',
                'prenom_user', 'num_projet', 'intitule_projet', 'id_machine', 'nom_machine', 'date_debut', 'duree_hp',
                'duree_hc', 'si_supprime', 'duree_ouvree', 'date_reservation', 'date_suppression']
        nom_fichier = "res.csv"
        libelle = "Réservation Equipement"
        Fichier.__init__(self, libelle, cles, nom_dossier + nom_fichier, delimiteur, encodage)

    def est_coherent(self, comptes, machines):
        msg = ""
        ligne = 1
        donnees_list = []

        for donnee in self.donnees:
            if donnee['id_compte'] == "":
                msg += "le compte id de la ligne " + ligne + " ne peut être vide\n"
            elif comptes.contient_id(donnee['id_compte']) == 0:
                msg += "le compte id '" + donnee['id_compte'] + "' de la ligne " + ligne + " n'est pas référencé\n"

            if donnee['id_machine'] == "":
                msg += "le machine id de la ligne " + ligne + " ne peut être vide\n"
            elif machines.contient_id(donnee['id_machine']) == 0:
                msg += "le machine id '" + donnee['id_machine'] + "' de la ligne " + ligne \
                       + " n'est pas référencé\n"

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

    def calcul_montants(self, machines, coefmachines, comptes, clients):
        donnees_list = []
        for donnee in self.donnees:
            compte = comptes.donnees[donnee['id_compte']]
            machine = machines.donnees[donnee['id_machine']]
            client = clients.donnees[compte['code_client']]
            coefmachine = coefmachines.donnees[client['id_classe_tarif'] + machine['categorie']]
            duree_fact_hp = round(max(0, min(1, (1-float(donnee['duree_ouvree']) /
                                                 float(machine['delai_sans_frais'])))) * float(donnee['duree_hp']), 0)
            duree_fact_hc = round(max(0, min(1, (1-float(donnee['duree_ouvree']) /
                                                 float(machine['delai_sans_frais'])))) * float(donnee['duree_hc']), 0)

            donnee['pv'] = round(duree_fact_hp / 60 * round(float(machine['t_h_reservation_hp_p']) *
                                                            float(coefmachine['coef_p']), 2) + duree_fact_hc / 60 *
                                 round(float(machine['t_h_reservation_hc_p']) * float(coefmachine['coef_p'])), 2)

            donnee['qv'] = round(duree_fact_hp / 60 * round(float(machine['t_h_reservation_hp_np']) *
                                                            float(coefmachine['coef_np']), 2) + duree_fact_hc / 60 *
                                 round(float(machine['t_h_reservation_hc_np']) * float(coefmachine['coef_np'])), 2)

            donnees_list.append(donnee)
        self.donnees = donnees_list
