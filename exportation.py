import csv
from sommes import Sommes
import os
import subprocess


class Exportation(object):

    @staticmethod
    def factures(somme_client, somme_compte, nom_dossier, encodage, delimiteur, edition, generaux, clients, comptes):
        mois = edition.mois
        if mois < 10:
            mois = "0" + str(mois)
        else:
            mois = str(mois)
        nom = nom_dossier + "facture_" + str(edition.annee) + "_" + mois + "_" + str(edition.version) + ".csv"
        csv_fichier = open(nom, 'w', newline='', encoding=encodage)
        fichier_writer = csv.writer(csv_fichier, delimiter=delimiteur, quotechar='|')
        fichier_writer.writerow(["Poste", "Système d'origine", "Type de document de vente", "Organisation commerciale",
                                 "Canal de distribution", "Secteur d'activité", "Agence commerciale",
                                 "Groupe de vendeurs", "Donneur d'ordre", "Client facturé", "Payeur", "Client livré",
                                 "Numéro de la commande d'achat du client", "Date de livraison E/Tsouhaitée",
                                 "Nom émetteur", "Textes", "Lien réseau 01", "Doc interne", "Lien réseau 02",
                                 "Doc interne", "Lien réseau 03", "Doc interne", "Lien réseau 04", "Doc interne",
                                 "Lien réseau 05", "Doc interne", "Article",
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

        keys = Sommes.ordonner_keys_str_par_int(somme_client.keys())

        for code_client in keys:
            poste = 0
            client = somme_client[code_client]
            cl = clients.donnees[code_client]
            if cl['type_labo'] == "I":
                genre = generaux.donnees['code_int'][1]
            else:
                genre = generaux.donnees['code_ext'][1]
            nature = generaux.donnees['nature_client'][generaux.donnees['code_n'].index(cl['type_labo'])]
            reference = nature + str(edition.annee)[2:] + mois + "." + code_client
            if edition.version != "0":
                reference += "-" + edition.version
            fichier_writer.writerow([poste, generaux.donnees['origine'][1], genre, generaux.donnees['commerciale'][1],
                                     generaux.donnees['canal'][1], generaux.donnees['secteur'][1], "", "", code_client,
                                     code_client, code_client, code_client, reference, "", "",
                                     generaux.donnees['entete'][1], "->", "", "->", ""])

            op_centre = cl['type_labo'] + str(edition.annee)[2:] + mois
            if int(cl['emol_base_mens']) > 0:
                poste = generaux.donnees['poste_emolument'][1]
                fichier_writer.writerow(Exportation.ligne_facture(generaux, 1, poste, client['em'], client['er'],
                                                                  op_centre, ""))

            inc = 1
            client_comptes = somme_compte[code_client]
            keys2 = Sommes.ordonner_keys_str_par_int(client_comptes.keys())
            for id_compte in keys2:
                compte = client_comptes[id_compte]
                co = comptes.donnees[id_compte]
                if compte['si_facture'] > 0:
                    poste = inc*10
                    if compte['somme_j_pm'] > 0:
                        fichier_writer.writerow(Exportation.ligne_facture(generaux, 2, poste, compte['somme_j_pm'],
                                                                          compte['prj'], op_centre, co['intitule']))
                        poste += 1

                    if compte['somme_j_nm'] > 0:
                        fichier_writer.writerow(Exportation.ligne_facture(generaux, 3, poste, compte['somme_j_nm'],
                                                                          compte['nrj'], op_centre, co['intitule']))
                        poste += 1

                    if compte['somme_j_lm'] > 0:
                        fichier_writer.writerow(Exportation.ligne_facture(generaux, 4, poste, compte['somme_j_lm'],
                                                                          compte['somme_j_lr'], op_centre,
                                                                          co['intitule']))
                        poste += 1

                    if compte['somme_j_cm'] > 0:
                        fichier_writer.writerow(Exportation.ligne_facture(generaux, 5, poste, compte['somme_j_cm'],
                                                                          compte['somme_j_cr'], op_centre,
                                                                          co['intitule']))
                        poste += 1

                    if compte['somme_j_wm'] > 0:
                        fichier_writer.writerow(Exportation.ligne_facture(generaux, 6, poste, compte['somme_j_wm'],
                                                                          compte['somme_j_wr'], op_centre,
                                                                          co['intitule']))
                        poste += 1

                    if compte['somme_j_xm'] > 0:
                        fichier_writer.writerow(Exportation.ligne_facture(generaux, 7, poste, compte['somme_j_xm'],
                                                                          compte['somme_j_xr'], op_centre,
                                                                          co['intitule']))
                        poste += 1
                    inc += 1

    @staticmethod
    def ligne_facture(generaux, index, poste, net, rabais, op_centre, consommateur):
        if rabais == 0:
            rabais = ""
        code_op = generaux.donnees['code_t'][1] + op_centre + generaux.donnees['code_d'][index]
        return [poste, "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "",
                "", generaux.donnees['code_sap'][index], "", generaux.donnees['quantite'][index],
                generaux.donnees['unite'][index], generaux.donnees['type_prix'][index], net,
                generaux.donnees['type_rabais'][index], rabais, "", generaux.donnees['financier'][1], "",
                generaux.donnees['fond'][1], "", "", code_op, "", "", "", generaux.donnees['texte_sap'][index],
                consommateur]

    @staticmethod
    def annexes_techniques(somme_client, somme_compte, somme_categorie, somme_projet, clients, edition, livraisons,
                           acces, machines, reservations, prestations, comptes, nom_dossier):

        dossier_annexe = nom_dossier + "annexes_techniques/"
        if not os.path.exists(dossier_annexe):
            os.makedirs(dossier_annexe)

        keys = Sommes.ordonner_keys_str_par_int(somme_client.keys())

        debut = r'''\documentclass[a4paper]{article}
            \usepackage[utf8]{inputenc}
            \usepackage[margin=20mm]{geometry}
            \begin{document}
            '''
        fin = r'''\end{document}
            '''

        for code_client in keys:
            scl = somme_client[code_client]
            client = clients.donnees[code_client]
            sca = somme_categorie[code_client]

            contenu = debut

            dic_entete = {'code': code_client, 'nom': client['nom_labo'], 'annee': edition.annee, 'mois': edition.mois}
            entete = r'''%(code)s
                \newline
                %(nom)s
                \newline
                %(annee)s/%(mois)s
                \newline
                \newline
                ''' % dic_entete

            contenu += entete

            dic_emo = {'emb': client['emol_base_mens'], 'ef': client['emol_fixe'], 'pente': client['coef'],
                       'tot_eq_p': str(scl['pt']), 'tot_eq_np': str(scl['qt']), 'tot_eq': str(scl['somme_eq']),
                       'rabais': str(scl['er'])}

            structure_emolument = r'''{|l|l|l|l|l|l|l|}'''
            legende_emolument = r'''Emolument pour client ''' + code_client
            contenu_emolument = r'''
                Emolument de base & Emolument fixe & Pente & Total EQ P & Total EQ NP & Total EQ & Rabais émolument \\
                \hline
                %(emb)s & %(ef)s & %(pente)s & %(tot_eq_p)s & %(tot_eq_np)s & %(tot_eq)s & %(rabais)s \\
                \hline
                ''' % dic_emo

            contenu += Exportation.tableau(contenu_emolument, structure_emolument, legende_emolument)

            tab = 2

            structure_recap_compte = r'''{|l|l|l|l|l|l|l|l|l|}'''
            legende_recap_compte = r'''Récapitulaitf des comptes pour client ''' + code_client
            contenu_recap_compte = r'''
                Intitulé & Type & Plafonné & Nn Plaf. & Loc. SB & Conso. & Trav. Spé. & Frais Exp. & Total cpte \\
                \hline
                '''

            client_comptes = somme_compte[code_client]
            keys2 = Sommes.ordonner_keys_str_par_int(client_comptes.keys())
            for id_compte in keys2:

                client_compte_projet = somme_projet[code_client][id_compte]
                keys3 = Sommes.ordonner_keys_str_par_int(client_compte_projet.keys())

                structure_recap_projet = r'''{|l|l|l|l|l|l|l|l|}'''
                legende_recap_projet = r'''Récapitulatif compte ''' + id_compte
                contenu_recap_projet = r'''
                    Numéro & Plafonné & Non Plaf. & Loc. SB & Conso. & Trav. Spé. & Frais Exp. & Total projet \\
                    \hline
                    '''

                for num_projet in keys3:

                    sp = somme_projet[code_client][id_compte][num_projet]
                    total = sp['somme_p_pm'] + sp['somme_p_nm'] + sp['lp'] + sp['cp'] + sp['wp'] + sp['xp']
                    dico_recap_projet = {'num': num_projet, 'plafond': "%.2f" % sp['somme_p_pm'],
                                         'non_plafond': "%.2f" % sp['somme_p_nm'], 'loc_sb': "%.2f" % sp['lp'],
                                         'conso': "%.2f" % sp['cp'], 'travail': "%.2f" % sp['wp'],
                                         'frais': "%.2f" % sp['xp'], 'total': "%.2f" % total}
                    contenu_recap_projet += r'''%(num)s & %(plafond)s & %(non_plafond)s & %(loc_sb)s &
                        %(conso)s & %(travail)s & %(frais)s & %(total)s \\
                        \hline
                        ''' % dico_recap_projet

                    cae_proj = acces.acces_pour_projet(num_projet, id_compte, code_client)
                    for cae in cae_proj:
                        tableau = Exportation.tableau_cae(cae, machines.donnees[cae['id_machine']])
                        contenu += tableau
                        tab += 1
                        if tab == 4:
                            contenu += r'''\clearpage'''
                            tab = 0

                    res_proj = reservations.reservation_pour_projet(num_projet, id_compte, code_client)
                    for res in res_proj:
                        tableau = Exportation.tableau_res(res, machines.donnees[res['id_machine']])
                        contenu += tableau
                        tab += 1
                        if tab == 4:
                            contenu += r'''\clearpage'''
                            tab = 0

                    liv_proj_cat = livraisons.livraisons_pour_projet_par_categorie(num_projet, id_compte, code_client,
                                                                                   prestations)

                    for categorie in ['L', 'C', 'W', 'X']:
                        if categorie in liv_proj_cat:
                            livs = liv_proj_cat[categorie]
                            for liv in livs:
                                tableau = Exportation.tableau_livraison(liv, prestations.donnees[liv['id_prestation']])
                                contenu += tableau
                                tab += 1
                                if tab == 4:
                                    contenu += r'''\clearpage'''
                                    tab = 0

                sco = somme_compte[code_client][id_compte]

                sj = sco['pj'] + sco['nj'] + sco['lj'] + sco['cj'] + sco['wj'] + sco['xj']
                dico_recap_compte = {'plafond': "%.2f" % sco['somme_j_pm'], 'non_plafond': "%.2f" % sco['somme_j_nm'],
                                     'loc_sb': "%.2f" % sco['lj'], 'conso': "%.2f" % sco['cj'],
                                     'travail': "%.2f" % sco['wj'], 'frais': "%.2f" % sco['xj'],
                                     'prj': "%.2f" % sco['prj'], 'nrj': "%.2f" % sco['nrj'], 'pj': "%.2f" % sco['pj'],
                                     'nj': "%.2f" % sco['nj'], 'lj': "%.2f" % sco['lj'], 'cj': "%.2f" % sco['cj'],
                                     'wj': "%.2f" % sco['wj'], 'xj': "%.2f" % sco['xj'], 'sj': "%.2f" % sj}
                contenu_recap_projet += r'''\hline
                    Montant article & %(plafond)s & %(non_plafond)s & %(loc_sb)s &
                    %(conso)s & %(travail)s & %(frais)s \\
                    \hline
                    Plafonnement & %(prj)s & %(nrj)s  \\
                    \hline
                    Total article & %(pj)s & %(nj)s & %(lj)s &
                    %(cj)s & %(wj)s & %(xj)s & %(sj)s\\
                    \hline
                    ''' % dico_recap_compte

                contenu += Exportation.tableau(contenu_recap_projet, structure_recap_projet, legende_recap_projet)

                tab += 1
                if tab == 4:
                    contenu += r'''\clearpage'''
                    tab = 0

                co = comptes.donnees[id_compte]

                dico_recap_compte = {'compte': id_compte, 'type': co['categorie'], 'plafond': "%.2f" % sco['pj'],
                                     'non_plafond': "%.2f" % sco['nj'], 'loc_sb': "%.2f" % sco['lj'],
                                     'conso': "%.2f" % sco['cj'], 'travail': "%.2f" % sco['wj'],
                                     'frais': "%.2f" % sco['xj'], 'total': "%.2f" % sj}

                contenu_recap_compte += r'''Compte %(compte)s & %(type)s & %(plafond)s & %(non_plafond)s & %(loc_sb)s &
                        %(conso)s & %(travail)s & %(frais)s & %(total)s \\
                        \hline
                        ''' % dico_recap_compte

                structure_recap_poste = r'''{|l|l|l|l|}'''
                legende_recap_poste = r'''Récapitulatif postes pour compte ''' + id_compte

                dico_recap_poste = {'spu': "%.2f" % sco['somme_j_pu'], 'prj': "%.2f" % sco['prj'],
                                    'pj': "%.2f" % sco['pj'], 'spv': "%.2f" % sco['somme_j_pv'],
                                    'squ': "%.2f" % sco['somme_j_qu'], 'nrj': "%.2f" % sco['nrj'],
                                    'nj': "%.2f" % sco['nj'], 'sqv': "%.2f" % sco['somme_j_qv'],
                                    'som': "%.2f" % sco['somme_j_om'], 'slm': "%.2f" % sco['somme_j_lm'],
                                    'slr': "%.2f" % sco['somme_j_lr'], 'lj': "%.2f" % sco['lj'],
                                    'scm': "%.2f" % sco['somme_j_cm'], 'scr': "%.2f" % sco['somme_j_cr'],
                                    'cj': "%.2f" % sco['cj'], 'swm': "%.2f" % sco['somme_j_wm'],
                                    'swr': "%.2f" % sco['somme_j_wr'], 'wj': "%.2f" % sco['wj'],
                                    'sxm': "%.2f" % sco['somme_j_xm'], 'sxr': "%.2f" % sco['somme_j_xr'],
                                    'xj': "%.2f" % sco['xj']}

                contenu_recap_poste = r'''Compte  ''' + id_compte + r''' & Montant & Rabais & Total \\
                    \hline
                    Montant utilisation Machine P & %(spu)s & %(prj)s & %(pj)s \\
                    \hline
                    Montant réservation Machine P & %(spv)s & %(prj)s & %(pj)s \\
                    \hline
                    Montant utilisation Machine NP & %(squ)s & %(nrj)s & %(nj)s \\
                    \hline
                    Montant réservation Machine NP & %(sqv)s & %(nrj)s & %(nj)s \\
                    \hline
                    Montant Main d'oeuvre & %(som)s & %(nrj)s & %(nj)s \\
                    \hline
                    Location salle blanche & %(slm)s & %(slr)s & %(lj)s \\
                    \hline
                    Consommables & %(scm)s & %(scr)s & %(cj)s \\
                    \hline
                    Travaux spécifiques & %(swm)s & %(swr)s & %(wj)s \\
                    \hline
                    Frais d'expédition & %(sxm)s & %(sxr)s & %(xj)s \\
                    \hline
                    ''' % dico_recap_poste

                contenu += Exportation.tableau(contenu_recap_poste, structure_recap_poste, legende_recap_poste)

                tab += 1
                if tab == 4:
                    contenu += r'''\clearpage'''
                    tab = 0

            dico_recap_compte = {'plafond': "%.2f" % scl['pt'], 'non_plafond': "%.2f" % scl['nt'],
                                 'loc_sb': "%.2f" % scl['lt'], 'conso': "%.2f" % scl['ct'],
                                 'travail': "%.2f" % scl['wt'], 'frais': "%.2f" % scl['xt'],
                                 'total': "%.2f" % scl['somme_t']}

            contenu_recap_compte += r'''Total article & & %(plafond)s & %(non_plafond)s & %(loc_sb)s &
                    %(conso)s & %(travail)s & %(frais)s & %(total)s \\
                    \hline
                    ''' % dico_recap_compte

            contenu += Exportation.tableau(contenu_recap_compte, structure_recap_compte, legende_recap_compte)

            tab += 1
            if tab == 4:
                contenu += r'''\clearpage'''

            structure_recap_poste_cl = r'''{|l|l|l|l|}'''
            legende_recap_poste_cl = r'''Récapitulatif postes pour client ''' + code_client

            dico_recap_poste_cl = {'kpm1': 0, 'kprj1': 0, 'pk1': 0, 'kpm2': 0, 'kprj2': 0, 'pk2': 0, 'kpm3': 0,
                                   'kprj3': 0, 'pk3': 0, 'kpm4': 0, 'kprj4': 0, 'pk4': 0,
                                   'tpm': "%.2f" % scl['somme_t_pm'], 'tprj': "%.2f" % scl['somme_t_prj'],
                                   'pt': "%.2f" % scl['pt'], 'tqm': "%.2f" % scl['somme_t_qm'],
                                   'nt': "%.2f" % scl['nt'], 'tnrj': "%.2f" % scl['somme_t_nrj'],
                                   'tom': "%.2f" % scl['somme_t_om'], 'tlm': "%.2f" % scl['somme_t_lm'],
                                   'tlr': "%.2f" % scl['somme_t_lr'], 'lt': "%.2f" % scl['lt'],
                                   'tcm': "%.2f" % scl['somme_t_cm'], 'tcr': "%.2f" % scl['somme_t_cr'],
                                   'ct': "%.2f" % scl['ct'], 'twm': "%.2f" % scl['somme_t_wm'],
                                   'twr': "%.2f" % scl['somme_t_wr'], 'wt': "%.2f" % scl['wt'],
                                   'txm': "%.2f" % scl['somme_t_xm'], 'txr': "%.2f" % scl['somme_t_xr'],
                                   'xt': "%.2f" % scl['xt']}

            if '1' in sca:
                dico_recap_poste_cl['kpm1'] = "%.2f" % sca['1']['somme_k_pm']
                dico_recap_poste_cl['kprj1'] = "%.2f" % sca['1']['somme_k_prj']
                dico_recap_poste_cl['pk1'] = "%.2f" % sca['1']['pk']
            if '2' in sca:
                dico_recap_poste_cl['kpm2'] = "%.2f" % sca['2']['somme_k_pm']
                dico_recap_poste_cl['kprj2'] = "%.2f" % sca['2']['somme_k_prj']
                dico_recap_poste_cl['pk2'] = "%.2f" % sca['2']['pk']
            if '3' in sca:
                dico_recap_poste_cl['kpm3'] = "%.2f" % sca['3']['somme_k_pm']
                dico_recap_poste_cl['kprj3'] = "%.2f" % sca['3']['somme_k_prj']
                dico_recap_poste_cl['pk3'] = "%.2f" % sca['3']['pk']
            if '4' in sca:
                dico_recap_poste_cl['kpm4'] = "%.2f" % sca['4']['somme_k_pm']
                dico_recap_poste_cl['kprj4'] = "%.2f" % sca['4']['somme_k_prj']
                dico_recap_poste_cl['pk4'] = "%.2f" % sca['4']['pk']

            contenu_recap_poste_cl = r''' & Montant & Rabais & Total \\
                \hline
                Machine P (catégorie Utilisateur) & %(kpm1)s & %(kprj1)s & %(pk1)s \\
                \hline
                Machine P (catégorie Etudiant en projet Master) & %(kpm2)s & %(kprj2)s & %(pk2)s \\
                \hline
                Machine P (catégorie Etudiant en projet Semestre) & %(kpm3)s & %(kprj3)s & %(pk3)s \\
                \hline
                Machine P (catégorie Client) & %(kpm4)s & %(kprj4)s & %(pk4)s \\
                \hline
                Machine P & %(tpm)s & %(tprj)s & %(pt)s \\
                \hline
                Machine NP & %(tqm)s & %(tnrj)s & %(nt)s \\
                \hline
                Main d'oeuvre & %(tom)s & %(tnrj)s & %(nt)s \\
                \hline
                Location salle blanche & %(tlm)s & %(tlr)s & %(lt)s \\
                \hline
                Consommables & %(tcm)s & %(tcr)s & %(ct)s \\
                \hline
                Travaux spécifiques & %(twm)s & %(twr)s & %(wt)s \\
                \hline
                Frais d'expédition & %(txm)s & %(txr)s & %(xt)s \\
                \hline
                ''' % dico_recap_poste_cl

            contenu += Exportation.tableau(contenu_recap_poste_cl, structure_recap_poste_cl, legende_recap_poste_cl)

            contenu += fin

            mois = edition.mois
            if mois < 10:
                mois = "0" + str(mois)
            else:
                mois = str(mois)
            nom = "annexeT_" + str(edition.annee) + "_" + mois + "_" + str(edition.version) + "_" + code_client

            Exportation.creer_latex(nom, contenu, dossier_annexe)

    @staticmethod
    def tableau(contenu, structure, legende):
        return r'''\vspace{1cm}
            \begin{table}[!ht]
            \begin{tabular}''' + structure + contenu + r'''
            \end{tabular}
            \caption{''' + legende + r'''}
            \end{table}
            \vspace{1cm}
            '''

    @staticmethod
    def tableau_cae(cae, machine):
        p1 = float(machine['t_h_machine_hp_p']) * float(cae['duree_machine_hp'])
        p2 = float(machine['t_h_machine_hp_np']) * float(cae['duree_machine_hp'])
        p3 = float(machine['t_h_operateur_hp_mo']) * float(cae['duree_operateur_hp'])
        p4 = float(machine['t_h_machine_hc_p']) * float(cae['duree_machine_hc'])
        p5 = float(machine['t_h_machine_hc_np']) * float(cae['duree_machine_hc'])
        p6 = float(machine['t_h_operateur_hc_mo']) * float(cae['duree_operateur_hc'])

        dico = {'login': cae['date_login'], 'machine': cae['nom_machine'].encode('utf-8'),
                'projet': cae['intitule_projet'], 'operateur': cae['nom_op'], 'rem_op': cae['remarque_op'],
                'rem_staff': cae['remarque_staff'], 'deq_hp': cae['duree_machine_hp'],
                'dmo_hp': cae['duree_operateur_hp'], 'deq_hc': cae['duree_machine_hc'],
                'dmo_hc': cae['duree_operateur_hc'], 't1': machine['t_h_machine_hp_p'],
                't2': machine['t_h_machine_hp_np'], 't3': machine['t_h_operateur_hp_mo'],
                't4': machine['t_h_machine_hc_p'], 't5': machine['t_h_machine_hc_np'],
                't6': machine['t_h_operateur_hc_mo'], 'p1': p1, 'p2': p2, 'p3': p3, 'p4': p4, 'p5': p5, 'p6': p6}

        structure = r'''{|l|l|l|l|l|l|l|}'''
        legende = r'''Utilisation CAE pour ''' + cae['id_compte'] + r''' / ''' + cae['num_projet']
        contenu = r''' &  &  & Durée & & [CHF/h] & [CHF] \\
            \hline
            Login & \verb+%(login)s+ & HP & %(deq_hp)s & P & %(t1)s & %(p1)s \\
            \hline
            Machine & \verb+%(machine)s+ & HP & %(deq_hp)s & NP & %(t2)s & %(p2)s \\
            \hline
            Projet & \verb+%(projet)s+ & HP & %(dmo_hp)s & MO & %(t3)s & %(p3)s \\
            \hline
            Opérateur & \verb+%(operateur)s+ & HC & %(deq_hc)s & P & %(t4)s & %(p4)s \\
            \hline
            Rem OP & \verb+%(rem_op)s+ & HC & %(deq_hc)s & NP & %(t5)s & %(p5)s \\
            \hline
            Rem Staff & \verb+%(rem_staff)s+ & HC & %(dmo_hc)s & MO & %(t6)s & %(p6)s \\
            \hline
            ''' % dico

        return Exportation.tableau(contenu, structure, legende)

    @staticmethod
    def tableau_res(res, machine):
        p7 = float(machine['t_h_machine_hp_p']) * float(res['duree_fact_hp'])
        p8 = float(machine['t_h_machine_hp_np']) * float(res['duree_fact_hp'])
        p9 = float(machine['t_h_machine_hc_p']) * float(res['duree_fact_hc'])
        p10 = float(machine['t_h_machine_hc_np']) * float(res['duree_fact_hc'])

        dico = {'slot': res['date_debut'], 'machine': res['nom_machine'].encode('utf-8'),
                'projet': res['intitule_projet'], 'reserve': res['date_reservation'],
                'supprime': res['date_suppression'], 'shp': res['duree_hp'], 'shc': res['duree_hc'],
                'fhp': res['duree_fact_hp'], 'fhc': res['duree_fact_hc'], 't7': machine['t_h_machine_hp_p'],
                't8': machine['t_h_machine_hp_np'], 't9': machine['t_h_machine_hc_p'],
                't10': machine['t_h_machine_hc_np'], 'p7': p7, 'p8': p8, 'p9': p9, 'p10': p10}

        structure = r'''{|l|l|l|l|l|l|l|l|}'''
        legende = r'''Réservation pour ''' + res['id_compte'] + r''' / ''' + res['num_projet']
        contenu = r''' &  &  & Durée Slot & Durée Facturée & & [CHF/h] & [CHF] \\
            \hline
            Slot & \verb+%(slot)s+ & HP & %(shp)s & %(fhp)s & P & %(t7)s & %(p7)s\\
            \hline
            Machine & \verb+%(machine)s+ & HP & %(shp)s & %(fhp)s & NP & %(t8)s & %(p8)s\\
            \hline
            Réservé le & \verb+%(reserve)s+ & HC & %(shc)s & %(fhc)s & P & %(t9)s & %(p9)s\\
            \hline
            Supprimé le & \verb+%(supprime)s+ & HC & %(shc)s & %(fhc)s & NP & %(t10)s & %(p10)s\\
            \hline
            Projet & \verb+%(projet)s+ \\
            \hline
            ''' % dico

        return Exportation.tableau(contenu, structure, legende)

    @staticmethod
    def tableau_livraison(livraison, prestation):
        montant = float(livraison['quantite']) * float(prestation['prix_unit'])
        total = montant - float(livraison['rabais'])
        dico = {'date': livraison['date_livraison'], 'prestation': prestation['designation'].replace('µ', 'mu'),
                'categorie': prestation['categorie'], 'quantite': livraison['quantite'], 'unite': livraison['unite'],
                'rapport': prestation['prix_unit'], 'montant': str(montant), 'rabais': livraison['rabais'],
                'total': str(total), 'projet': livraison['intitule_projet'], 'id': livraison['id_livraison'],
                'responsable': livraison['responsable'], 'commande': livraison['date_commande'],
                'remarque': livraison['remarque']}
        structure = r'''{|l|l|l|l|l|l|l|l|l|}'''
        legende = r'''Livraisons pour ''' + livraison['id_compte'] + r''' / ''' + livraison['num_projet']
        contenu = r'''Date livraison & Intitulé & Catégorie & Quantité & Unité & [CHF/u] & Montant [CHF] &
            Rabais [CHF] & Total [CHF] \\
            \hline
            \verb+%(date)s+ & \verb+%(prestation)s+ & \verb+%(categorie)s+ & \verb+%(quantite)s+ & \verb+%(unite)s+ &
            \verb+%(rapport)s+ & \verb+%(montant)s+ & \verb+%(rabais)s+ & \verb+%(total)s+ \\
            \hline
            Projet & \verb+%(projet)s+ \\
            \hline
            Num livraison & \verb+%(id)s+ \\
            \hline
            Livré par & \verb+%(responsable)s+ \\
            \hline
            Commande & \verb+%(commande)s+ \\
            \hline
            Remarque & \verb+%(remarque)s+ \\
            \hline
            ''' % dico

        return Exportation.tableau(contenu, structure, legende)

    @staticmethod
    def annexes():
        print("annexes")


    @staticmethod
    def creer_latex(nom_fichier, contenu, nom_dossier=""):
        with open(nom_fichier + ".tex",'w') as f:
            f.write(contenu)

        proc=subprocess.Popen(['pdflatex', nom_fichier + ".tex"])
        proc.communicate()

        os.unlink(nom_fichier + '.tex')
        os.unlink(nom_fichier + '.log')
        os.unlink(nom_fichier + '.aux')

        if nom_dossier != "":
            proc=subprocess.Popen(['mv', nom_fichier + ".pdf", nom_dossier])
            proc.communicate()
