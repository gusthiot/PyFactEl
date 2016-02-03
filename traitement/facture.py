import csv

from outils import Outils


class Facture(object):
    """
    Classe contenant les méthodes nécessaires à la génération des factures
    """

    @staticmethod
    def factures(sommes, nom_dossier, encodage, delimiteur, edition, generaux, clients, comptes, lien_annexes,
                 lien_annexes_techniques, prod2qual = None):
        """
        génère la facture sous forme de csv
        :param sommes: sommes calculées
        :param nom_dossier: nom du dossier dans lequel enregistrer le csv
        :param delimiteur: code délimiteur de champ dans le fichier csv
        :param encodage: encodage du texte
        :param edition: paramètres d'édition
        :param generaux: paramètres généraux
        :param clients: clients importés
        :param comptes: comptes importés
        :param lien_annexes: lien au dossier contenant les annexes
        :param lien_annexes_techniques: lien au dossier contenant les annexes techniques
        :param prod2qual: Une fonction qui traduit les identifiants clients de PRD en QAS
        """

        if sommes.calculees == 0:
            info = "Vous devez d'abord faire toutes les sommes avant de pouvoir créer la facture"
            print(info)
            Outils.affiche_message(info)
            return

        if prod2qual:
            suffixe = "_qualite.csv"
        else:
            suffixe = ".csv"
        nom = nom_dossier + "facture_" + str(edition.annee) + "_" + Outils.mois_string(edition.mois) + "_" + \
              str(edition.version) + suffixe
        csv_fichier = open(nom, 'w', newline='', encoding=encodage)
        fichier_writer = csv.writer(csv_fichier, delimiter=delimiteur, quotechar='|')
        fichier_writer.writerow(["Poste", "Système d'origine", "Type de document de vente", "Organisation commerciale",
                                 "Canal de distribution", "Secteur d'activité", "Agence commerciale",
                                 "Groupe de vendeurs", "Donneur d'ordre", "Nom 2 du donneur d'ordre",
                                 "Nom 3 du donneur d'ordre", "Client facturé", "Payeur", "Client livré", "Devise",
                                 "Mode d'envoi", "Numéro de la commande d'achat du client",
                                 "Date de livraison E/Tsouhaitée", "Nom émetteur", "Textes", "Lien réseau 01",
                                 "Doc interne", "Lien réseau 02", "Doc interne", "Lien réseau 03", "Doc interne",
                                 "Lien réseau 04", "Doc interne", "Lien réseau 05", "Doc interne", "Article",
                                 "Désignation du poste d'une commande client", "Quantité cible en unité de vente",
                                 "Unité de quantité cible", "Type de prix net", "Prix net du poste",
                                 "Type de rabais poste", "Valeur rabais poste", "Date de livraison poste souhaitée",
                                 "Centre financier émetteur", "Compte budgétaire émetteur", "Fond émetteur",
                                 "OTP émetteur", "Numéro d'ordre interne émetteur", "Code OP émetteur",
                                 "Affaire émetteur", "Demande de voyage émetteur", "Matricule émetteur", "Textes",
                                 "Nom consommateur interne de la prestation", "Fond récepteur 01",
                                 "Proportion fond récepteur 01", "OTP récepteur fond 01",
                                 "Numéro d'ordre interne récepteur fond 01", "Code OP récepteur fond 01",
                                 "Affaire récepteur 01", "Demande de voyage récepteur fond 01",
                                 "Matricule récepteur fond 01", "Fond récepteur 02", "Proportion fond récepteur 02",
                                 "OTP récepteur fond 02", "Numéro d'ordre interne récepteur fond 02",
                                 "Code OP récepteur fond 02", "Affaire récepteur 02",
                                 "Demande de voyage récepteur fond 02", "Matricule récepteur fond 02",
                                 "Fond récepteur 03", "Proportion fond récepteur 03", "OTP récepteur fond 03",
                                 "Numéro d'ordre interne récepteur fond 03", "Code OP récepteur fond 03",
                                 "Affaire récepteur 03", "Demande de voyage récepteur fond 03",
                                 "Matricule récepteur fond 03", "Fond récepteur 04", "Proportion fond récepteur 04",
                                 "OTP récepteur fond 04", "Numéro d'ordre interne récepteur fond 04",
                                 "Code OP récepteur fond 04", "Affaire récepteur 04",
                                 "Demande de voyage récepteur fond 04", "Matricule récepteur fond 04",
                                 "Fond récepteur 05", "Proportion fond récepteur 05", "OTP récepteur fond 05",
                                 "Numéro d'ordre interne récepteur fond 05", "Code OP récepteur fond 05",
                                 "Affaire récepteur 05", "Demande de voyage récepteur fond 05",
                                 "Matricule récepteur fond 05"])

        for code_client in sorted(sommes.sommes_clients.keys()):
            poste = 0
            client = sommes.sommes_clients[code_client]
            cl = clients.donnees[code_client]
            if cl['type_labo'] == "I":
                genre = generaux.donnees['code_int'][1]
            else:
                genre = generaux.donnees['code_ext'][1]
            nature = generaux.donnees['nature_client'][generaux.donnees['code_n'].index(cl['type_labo'])]
            reference = nature + str(edition.annee)[2:] + Outils.mois_string(edition.mois) + "." + code_client
            if edition.version != "0":
                reference += "-" + edition.version

            lien_annexe = lien_annexes + "annexe_" + str(edition.annee) + "_" + Outils.mois_string(edition.mois) + \
                          "_" + str(edition.version) + "_" + code_client + ".pdf"

            lien_annexe_technique = lien_annexes_techniques + "annexeT_" + str(edition.annee) + "_" + \
                                    Outils.mois_string(edition.mois) + "_" + str(edition.version) + "_" + \
                                    code_client + ".pdf"
            if prod2qual:
                code_client_traduit = prod2qual(code_client)
            else:
                code_client_traduit = code_client
            fichier_writer.writerow([poste, generaux.donnees['origine'][1], genre, generaux.donnees['commerciale'][1],
                                     generaux.donnees['canal'][1], generaux.donnees['secteur'][1], "", "", code_client_traduit,
                                     cl['dest'], cl['ref'], code_client_traduit, code_client_traduit, code_client_traduit,
                                     generaux.donnees['devise'][1], "", reference, "", "",
                                     generaux.donnees['entete'][1], lien_annexe, "", lien_annexe_technique, "X"])

            op_centre = cl['type_labo'] + str(edition.annee)[2:] + Outils.mois_string(edition.mois)
            if int(cl['emol_base_mens']) > 0:
                poste = generaux.donnees['poste_emolument'][1]
                fichier_writer.writerow(Facture.ligne_facture(generaux, 1, poste, client['em'], client['er'],
                                                              op_centre, "", edition))

            inc = 1
            client_comptes = sommes.sommes_comptes[code_client]
            for id_compte in client_comptes.keys():
                compte = client_comptes[id_compte]
                co = comptes.donnees[id_compte]
                if compte['si_facture'] > 0:
                    poste = inc*10
                    if compte['somme_j_pm'] > 0:
                        fichier_writer.writerow(Facture.ligne_facture(generaux, 2, poste, compte['somme_j_pm'],
                                                                    compte['prj'], op_centre, co['intitule'], edition))
                        poste += 1

                    if compte['somme_j_nm'] > 0:
                        fichier_writer.writerow(Facture.ligne_facture(generaux, 3, poste, compte['somme_j_nm'],
                                                                    compte['nrj'], op_centre, co['intitule'], edition))
                        poste += 1

                    index = 4
                    for categorie in generaux.obtenir_d3():
                        if compte['sommes_cat_m'][categorie] > 0:
                            fichier_writer.writerow(Facture.ligne_facture(generaux, index, poste,
                                compte['sommes_cat_m'][categorie], compte['sommes_cat_r'][categorie], op_centre,
                                                                          co['intitule'], edition))
                            poste += 1
                        index += 1
                    inc += 1

    @staticmethod
    def ligne_facture(generaux, index, poste, net, rabais, op_centre, consommateur, edition):
        """
        retourne une ligne de facturation  formatée
        :param generaux: paramètres généraux
        :param index: index de colonne des paramètres généraux
        :param poste: indice de poste
        :param net: montant net
        :param rabais: rabais sur le montant
        :param op_centre: centre d'opération
        :param consommateur: consommateur
        :param edition: paramètres d'édition
        :return: ligne de facturation formatée
        """
        if rabais == 0:
            rabais = ""
        code_op = generaux.donnees['code_t'][1] + op_centre + generaux.donnees['code_d'][index]
        return [poste, "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "",
                "", "", "", "", "", generaux.donnees['code_sap'][index], "", generaux.donnees['quantite'][index],
                generaux.donnees['unite'][index], generaux.donnees['type_prix'][index], net,
                generaux.donnees['type_rabais'][index], rabais, edition.date_livraison, generaux.donnees['financier'][1], "",
                generaux.donnees['fond'][1], "", "", code_op, "", "", "", generaux.donnees['texte_sap'][index],
                consommateur]
