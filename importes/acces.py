from importes import Fichier
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
        self.codes = []

    def obtenir_codes(self, comptes, machines):
        if len(self.codes) == 0:
            self.est_coherent(comptes, machines)
        return self.codes

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

            if donnee['code_client'] not in self.codes:
                self.codes.append(donnee['code_client'])

            donnee['duree_machine_hp'], info = self.est_un_nombre(donnee['duree_machine_hp'], "la durée machine hp",
                                                                  ligne)
            msg += info
            donnee['duree_machine_hc'], info = self.est_un_nombre(donnee['duree_machine_hc'], "la durée machine hc",
                                                                  ligne)
            msg += info
            donnee['duree_operateur_hp'], info = self.est_un_nombre(donnee['duree_operateur_hp'],
                                                                    "la durée opérateur hp", ligne)
            msg += info
            donnee['duree_operateur_hc'], info = self.est_un_nombre(donnee['duree_operateur_hc'],
                                                                    "la durée opérateur hc", ligne)
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

    def calcul_montants(self, machines, coefmachines, comptes, clients):
        donnees_list = []
        for donnee in self.donnees:
            compte = comptes.donnees[donnee['id_compte']]
            machine = machines.donnees[donnee['id_machine']]
            client = clients.donnees[compte['code_client']]
            coefmachine = coefmachines.donnees[client['id_classe_tarif'] + machine['categorie']]

            donnee['pu'] = round(donnee['duree_machine_hp'] / 60 * round(machine['t_h_machine_hp_p'] *
                                                                         coefmachine['coef_p'], 2) +
                                 donnee['duree_machine_hc'] / 60 * round(machine['t_h_machine_hc_p'] *
                                                                         coefmachine['coef_p']), 2)

            donnee['qu'] = round(donnee['duree_machine_hp'] / 60 * round(machine['t_h_machine_hp_np'] *
                                                                         coefmachine['coef_np'], 2) +
                                 donnee['duree_machine_hc'] / 60 * round(machine['t_h_machine_hc_np'] *
                                                                         coefmachine['coef_np']), 2)

            donnee['om'] = round(donnee['duree_operateur_hp'] / 60 *
                                 round(machine['t_h_operateur_hp_mo'] * coefmachine['coef_mo'], 2) +
                                 donnee['duree_operateur_hc'] / 60 *
                                 round(machine['t_h_operateur_hc_mo'] * coefmachine['coef_mo']), 2)

            donnees_list.append(donnee)
        self.donnees = donnees_list

    def acces_pour_projet(self, num_projet, id_compte, code_client):
        donnees_list = []
        for donnee in self.donnees:
            if (donnee['id_compte'] == id_compte) and (donnee['code_client'] == code_client) \
                    and (donnee['num_projet'] == num_projet):
                donnees_list.append(donnee)
        return donnees_list