from . import Fichier
from interfaces import Interfaces


class Acces(Fichier):
    """Contrôle Accès Equipement"""


    def __init__(self, nom_dossier, delimiteur, encodage):
        cles = ['annee', 'mois', 'id_compte', 'intitule_compte', 'code_client', 'abrev_labo', 'id_user', 'nom_user',
                'prenom_user', 'num_projet', 'intitule_projet', 'id_machine', 'nom_machine', 'date_login',
                'duree_machine_hp', 'duree_machine_hc', 'duree_operateur_hp', 'duree_operateur_hc', 'id_op', 'nom_op',
                'remarque_op', 'remarque_staff']
        nom_fichier = "cae.csv"
        libelle = "Contrôle Accès Equipement"
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
                msg += "le machine id '" + donnee['id_machine'] + "' de la ligne " + ligne + " n'est pas référencé\n"

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

            donnee['pu'] = round(float(donnee['duree_machine_hp']) / 60 * round(float(machine['t_h_machine_hp_p']) *
                                                                                float(coefmachine['coef_p']), 2) +
                                 float(donnee['duree_machine_hc']) / 60 * round(float(machine['t_h_machine_hc_p']) *
                                                                                float(coefmachine['coef_p'])), 2)

            donnee['qu'] = round(float(donnee['duree_machine_hp']) / 60 * round(float(machine['t_h_machine_hp_np']) *
                                                                                float(coefmachine['coef_np']), 2) +
                                 float(donnee['duree_machine_hc']) / 60 * round(float(machine['t_h_machine_hc_np']) *
                                                                                float(coefmachine['coef_np'])), 2)

            donnee['om'] = round(float(donnee['duree_operateur_hp']) / 60 *
                                 round(float(machine['t_h_operateur_hp_mo']) * float(coefmachine['coef_mo']), 2) +
                                 float(donnee['duree_operateur_hc']) / 60 *
                                 round(float(machine['t_h_operateur_hc_mo']) * float(coefmachine['coef_mo'])), 2)

            donnees_list.append(donnee)
        self.donnees = donnees_list
