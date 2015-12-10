import csv
from sommes import Sommes

class Exportation(object):

    @staticmethod
    def factures(somme_client, somme_compte, nom_dossier, encodage, delimiteur):
        csv_fichier = open(nom_dossier + "factures.csv", 'w', newline='', encoding=encodage)
        fichier_writer = csv.writer(csv_fichier, delimiter=delimiteur, quotechar='|')

        keys = Sommes.ordonner_keys_str_par_int(somme_client.keys())

        for code_client in keys:
            client = somme_client[code_client]
            ligne = [code_client, " ", "Emolument mensuel", "%.2f" % client['em'], "%.2f" % client['er'],
                     "%.2f" % client['e']]
            print(ligne)
            fichier_writer.writerow(ligne)

            client_comptes = somme_compte[code_client]
            keys2 = Sommes.ordonner_keys_str_par_int(client_comptes.keys())
            for id_compte in keys2:
                compte = client_comptes[id_compte]
                if compte['si_facture'] > 0:
                    ligne = [code_client, id_compte, "Machine P", "%.2f" % compte['somme_j_pm'], "%.2f" % compte['prj'],
                             "%.2f" % compte['pj']]
                    print(ligne)
                    fichier_writer.writerow(ligne)

                    ligne = [code_client, id_compte, "Machine NP + MO", "%.2f" % compte['somme_j_nm'],
                             "%.2f" % compte['nrj'], "%.2f" % compte['nj']]
                    print(ligne)
                    fichier_writer.writerow(ligne)

                    ligne = [code_client, id_compte, "Location salle blanche", "%.2f" % compte['somme_j_lm'],
                             "%.2f" % compte['somme_j_lr'], "%.2f" % compte['lj']]
                    print(ligne)
                    fichier_writer.writerow(ligne)

                    ligne = [code_client, id_compte, "Consommables", "%.2f" % compte['somme_j_cm'],
                             "%.2f" % compte['somme_j_cr'], "%.2f" % compte['cj']]
                    print(ligne)
                    fichier_writer.writerow(ligne)

                    ligne = [code_client, id_compte, "Travaux spécifiques", "%.2f" % compte['somme_j_wm'],
                             "%.2f" % compte['somme_j_wr'], "%.2f" % compte['wj']]
                    print(ligne)
                    fichier_writer.writerow(ligne)

                    ligne = [code_client, id_compte, "Frais d'expédition", "%.2f" % compte['somme_j_xm'],
                             "%.2f" % compte['somme_j_xr'], "%.2f" % compte['xj']]
                    print(ligne)
                    fichier_writer.writerow(ligne)
