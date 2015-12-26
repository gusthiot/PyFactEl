from sommes import Sommes
import os
import subprocess
import re


class Annexes(object):

    @staticmethod
    def annexes_techniques(somme_client, somme_compte, somme_categorie, somme_projet, clients, edition, livraisons,
                           acces, machines, reservations, prestations, comptes, nom_dossier):

        dossier_annexe = nom_dossier + "annexes_techniques/"
        if not os.path.exists(dossier_annexe):
            os.makedirs(dossier_annexe)

        keys = Sommes.ordonner_keys_str_par_int(somme_client.keys())

        debut = r'''\documentclass[a4paper,9pt]{extarticle}
            \usepackage[utf8]{inputenc}
            \usepackage{microtype}
            \usepackage[margin=10mm, includefoot]{geometry}
            \usepackage{multirow}
            \usepackage{longtable}
            \begin{document}
            \renewcommand{\arraystretch}{1.2}

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

            dic_emo = {'emb':  "%.2f" % client['emol_base_mens'], 'ef':  "%.2f" % client['emol_fixe'],
                       'pente': client['coef'], 'tot_eq_p': "%.2f" % scl['pt'], 'tot_eq_np': "%.2f" % scl['qt'],
                       'tot_eq': "%.2f" % scl['somme_eq'], 'rabais': "%.2f" % scl['er']}

            structure_emolument = r'''{|p{2cm}|p{2cm}|p{1.5cm}|p{2cm}|p{2cm}|p{2cm}|p{2cm}|}'''
            legende_emolument = r'''Emolument pour client ''' + code_client
            contenu_emolument = r'''
                Emolument de base & Emolument fixe & Pente & Total EQ P & Total EQ NP & Total EQ & Rabais émolument \\
                \hline
                %(emb)s & %(ef)s & %(pente)s & %(tot_eq_p)s & %(tot_eq_np)s & %(tot_eq)s & %(rabais)s \\
                \hline
                ''' % dic_emo

            contenu += Annexes.tableau(contenu_emolument, structure_emolument, legende_emolument)

            structure_recap_compte = r'''{|p{2cm}|p{1cm}|p{1.5cm}|p{1.5cm}|p{1.5cm}|p{1.5cm}|p{1.5cm}|p{1.5cm}|
                p{1.5cm}|}'''
            legende_recap_compte = r'''Récapitulatif des comptes pour client ''' + code_client
            contenu_recap_compte = r'''
                Intitulé & Type & Plafonné & Non Plaf. & Loc. SB & Conso. & Trav. Spé. & Frais Exp. & Total cpte \\
                \hline
                '''

            client_comptes = somme_compte[code_client]
            keys2 = Sommes.ordonner_keys_str_par_int(client_comptes.keys())
            for id_compte in keys2:
                client_compte_projet = somme_projet[code_client][id_compte]
                keys3 = Sommes.ordonner_keys_str_par_int(client_compte_projet.keys())
                structure_recap_projet = r'''{|p{2.2cm}|p{1.5cm}|p{1.4cm}|p{1.4cm}|p{1.4cm}|p{1.5cm}|p{1.5cm}|
                    p{1.8cm}|}'''
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

                    structure_cae = r'''{|p{1.5cm}|p{1.2cm}|p{4cm}|p{0.5cm}|p{0.9cm}|p{0.9cm}||p{0.5cm}|p{0.5cm}|
                        p{0.5cm}||p{1.2cm}|p{1.2cm}|p{1.2cm}|}'''
                    dico_cae = {'compte': id_compte, 'projet': num_projet}
                    contenu_cae = r'''\multicolumn{3}{|l|}{%(compte)s/%(projet)s} & & \multicolumn{2}{l||}{hh:mm} &
                        \multicolumn{3}{l||}{CHF/h} & \multicolumn{3}{l|}{CHF} \\
                        \hline
                        Date & Heure & Equipement & & mach. & oper. & P & NP & OP & P & NP & OP\\
                        \hline''' % dico_cae
                    nombre_cae = 0
                    legende_cae = r'''Récapitulatif CAE compte : ''' + id_compte + r''' / projet : ''' + num_projet

                    cae_proj = acces.acces_pour_projet(num_projet, id_compte, code_client)
                    for cae in cae_proj:
                        nombre_cae += 1
                        contenu_cae += Annexes.ligne_cae(cae, machines.donnees[cae['id_machine']])

                    if nombre_cae > 0:
                        contenu += Annexes.tableau(contenu_cae, structure_cae, legende_cae)

                    structure_res = r'''{|p{1.5cm}|p{1.2cm}|p{5cm}|p{0.5cm}|p{0.9cm}|p{0.9cm}||p{0.5cm}|p{0.5cm}||
                        p{1.2cm}|p{1.2cm}|}'''
                    dico_res = {'compte': id_compte, 'projet': num_projet}
                    contenu_res = r'''\multicolumn{3}{|l|}{%(compte)s/%(projet)s} & & \multicolumn{2}{l||}{hh:mm} &
                        \multicolumn{2}{l||}{CHF/h} & \multicolumn{2}{l|}{CHF} \\
                        \hline
                        Date & Heure & Equipement & & slot & fact. & P & NP & P & NP\\
                        \hline''' % dico_res
                    nombre_res = 0
                    legende_res = r'''Récapitulatif Réservation compte : ''' + id_compte + r''' / projet :
                        ''' + num_projet

                    res_proj = reservations.reservation_pour_projet(num_projet, id_compte, code_client)
                    for res in res_proj:
                        nombre_res += 1
                        contenu_res += Annexes.ligne_res(res, machines.donnees[res['id_machine']])

                    if nombre_res > 0:
                        contenu += Annexes.tableau(contenu_res, structure_res, legende_res)

                    liv_proj_cat = livraisons.livraisons_pour_projet_par_categorie(num_projet, id_compte, code_client,
                                                                                   prestations)

                    for categorie in ['L', 'C', 'W', 'X']:
                        if categorie in liv_proj_cat:
                            livs = liv_proj_cat[categorie]
                            for liv in livs:
                                tableau = Annexes.tableau_livraison(liv, prestations.donnees[liv['id_prestation']])
                                contenu += tableau

                sco = somme_compte[code_client][id_compte]

                sj = sco['pj'] + sco['nj'] + sco['lj'] + sco['cj'] + sco['wj'] + sco['xj']
                dico_recap_projet = {'plafond': "%.2f" % sco['somme_j_pm'], 'non_plafond': "%.2f" % sco['somme_j_nm'],
                                     'loc_sb': "%.2f" % sco['lj'], 'conso': "%.2f" % sco['cj'],
                                     'travail': "%.2f" % sco['wj'], 'frais': "%.2f" % sco['xj'],
                                     'prj': "%.2f" % sco['prj'], 'nrj': "%.2f" % sco['nrj'], 'pj': "%.2f" % sco['pj'],
                                     'nj': "%.2f" % sco['nj'], 'lj': "%.2f" % sco['lj'], 'cj': "%.2f" % sco['cj'],
                                     'wj': "%.2f" % sco['wj'], 'xj': "%.2f" % sco['xj'], 'sj': "%.2f" % sj}
                contenu_recap_projet += r'''\hline
                    Montant article & %(plafond)s & %(non_plafond)s & %(loc_sb)s &
                    %(conso)s & %(travail)s & %(frais)s & \\
                    \hline
                    Plafonnement & %(prj)s & %(nrj)s & & & & &  \\
                    \hline
                    Total article & %(pj)s & %(nj)s & %(lj)s &
                    %(cj)s & %(wj)s & %(xj)s & %(sj)s\\
                    \hline
                    ''' % dico_recap_projet

                contenu += Annexes.tableau(contenu_recap_projet, structure_recap_projet, legende_recap_projet)

                co = comptes.donnees[id_compte]

                dico_recap_compte = {'compte': id_compte, 'type': co['categorie'], 'plafond': "%.2f" % sco['pj'],
                                     'non_plafond': "%.2f" % sco['nj'], 'loc_sb': "%.2f" % sco['lj'],
                                     'conso': "%.2f" % sco['cj'], 'travail': "%.2f" % sco['wj'],
                                     'frais': "%.2f" % sco['xj'], 'total': "%.2f" % sj}

                contenu_recap_compte += r'''Compte %(compte)s & %(type)s & %(plafond)s & %(non_plafond)s & %(loc_sb)s &
                        %(conso)s & %(travail)s & %(frais)s & %(total)s \\
                        \hline
                        ''' % dico_recap_compte

                structure_recap_poste = r'''{|p{5cm}|p{2cm}|p{2cm}|p{2cm}|}'''
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

                contenu += Annexes.tableau(contenu_recap_poste, structure_recap_poste, legende_recap_poste)

                contenu += r'''\clearpage'''

            dico_recap_compte = {'plafond': "%.2f" % scl['pt'], 'non_plafond': "%.2f" % scl['nt'],
                                 'loc_sb': "%.2f" % scl['lt'], 'conso': "%.2f" % scl['ct'],
                                 'travail': "%.2f" % scl['wt'], 'frais': "%.2f" % scl['xt'],
                                 'total': "%.2f" % scl['somme_t']}

            contenu_recap_compte += r'''Total article & & %(plafond)s & %(non_plafond)s & %(loc_sb)s &
                    %(conso)s & %(travail)s & %(frais)s & %(total)s \\
                    \hline
                    ''' % dico_recap_compte

            contenu += Annexes.tableau(contenu_recap_compte, structure_recap_compte, legende_recap_compte)

            structure_recap_poste_cl = r'''{|p{6cm}|p{2cm}|p{2cm}|p{2cm}|}'''
            legende_recap_poste_cl = r'''Récapitulatif postes pour client ''' + code_client

            dico_recap_poste_cl = {'kpm1': '0.00', 'kprj1': '0.00', 'pk1': '0.00', 'kpm2': '0.00', 'kprj2': '0.00',
                                   'pk2': '0.00', 'kpm3': '0.00', 'kprj3': '0.00', 'pk3': '0.00', 'kpm4': '0.00',
                                   'kprj4': '0.00', 'pk4': '0.00',
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

            contenu += Annexes.tableau(contenu_recap_poste_cl, structure_recap_poste_cl, legende_recap_poste_cl)

            contenu += fin

            mois = edition.mois
            if mois < 10:
                mois = "0" + str(mois)
            else:
                mois = str(mois)
            nom = "annexeT_" + str(edition.annee) + "_" + mois + "_" + str(edition.version) + "_" + code_client

            Annexes.creer_latex(nom, contenu, dossier_annexe)

    @staticmethod
    def tableau(contenu, structure, legende):
        return r'''
            \begin{longtable}[c]
            ''' + structure + contenu + r'''
            \caption{''' + legende + r'''}
            \end{longtable}
            '''

    @staticmethod
    def ligne_cae(cae, machine):
        p1 = Annexes.format_si_nul(machine['t_h_machine_hp_p'] * cae['duree_machine_hp'])
        p2 = Annexes.format_si_nul(machine['t_h_machine_hp_np'] * cae['duree_machine_hp'])
        p3 = Annexes.format_si_nul(machine['t_h_operateur_hp_mo'] * cae['duree_operateur_hp'])
        p4 = Annexes.format_si_nul(machine['t_h_machine_hc_p'] * cae['duree_machine_hc'])
        p5 = Annexes.format_si_nul(machine['t_h_machine_hc_np'] * cae['duree_machine_hc'])
        p6 = Annexes.format_si_nul(machine['t_h_operateur_hc_mo'] * cae['duree_operateur_hc'])
        login = Annexes.echappe_caracteres(cae['date_login']).split()
        temps = login[0].split('-')
        date = temps[2] + '.' + temps[1] + '.' + temps[0]

        dico = {'date': date, 'heure': login[1],
                'machine': Annexes.echappe_caracteres(cae['nom_machine']),
                'projet': Annexes.echappe_caracteres(cae['intitule_projet']),
                'operateur': Annexes.echappe_caracteres(cae['nom_op']),
                'rem_op': Annexes.echappe_caracteres(cae['remarque_op']),
                'rem_staff': Annexes.echappe_caracteres(cae['remarque_staff']),
                'deq_hp': Annexes.format_heure(cae['duree_machine_hp']),
                'dmo_hp': Annexes.format_heure(cae['duree_operateur_hp']),
                'deq_hc': Annexes.format_heure(cae['duree_machine_hc']),
                'dmo_hc': Annexes.format_heure(cae['duree_operateur_hc']),
                't1': "%d" % machine['t_h_machine_hp_p'], 't2': "%d" % machine['t_h_machine_hp_np'],
                't3': "%d" % machine['t_h_operateur_hp_mo'], 't4': "%d" % machine['t_h_machine_hc_p'],
                't5': "%d" % machine['t_h_machine_hc_np'], 't6': "%d" % machine['t_h_operateur_hc_mo'],
                'p1': p1, 'p2': p2, 'p3': p3, 'p4': p4, 'p5': p5, 'p6': p6}

        ligne = ""
        if (cae['duree_machine_hp'] > 0) or (cae['duree_operateur_hp'] > 0):
            ligne += r'''%(date)s & %(heure)s & %(machine)s & HP & %(deq_hp)s & %(dmo_hp)s & %(t1)s & %(t2)s & %(t3)s &
                %(p1)s & %(p2)s & %(p3)s \\
                \hline''' % dico

        if (cae['duree_machine_hc'] > 0) or (cae['duree_operateur_hc'] > 0):
            ligne += r'''%(date)s & %(heure)s & %(machine)s & HC & %(deq_hc)s & %(dmo_hc)s & %(t4)s & %(t5)s & %(t6)s &
                %(p4)s & %(p5)s & %(p6)s \\
                \hline''' % dico

        if (cae['remarque_staff'] != "") or (cae['remarque_op'] != ""):
            ligne += r'''%(date)s & %(heure)s & \multicolumn{10}{l|}{%(operateur)s ; %(rem_op)s ; %(rem_staff)s}\\
                \hline''' % dico

        return ligne

    @staticmethod
    def ligne_res(res, machine):
        p7 = Annexes.format_si_nul(machine['t_h_machine_hp_p'] * res['duree_fact_hp'])
        p8 = Annexes.format_si_nul(machine['t_h_machine_hp_np'] * res['duree_fact_hp'])
        p9 = Annexes.format_si_nul(machine['t_h_machine_hc_p'] * res['duree_fact_hc'])
        p10 = Annexes.format_si_nul(machine['t_h_machine_hc_np'] * res['duree_fact_hc'])
        login = Annexes.echappe_caracteres(res['date_debut']).split()
        temps = login[0].split('-')
        date = temps[2] + '.' + temps[1] + '.' + temps[0]

        dico = {'date': date, 'heure': login[1],
                'machine': Annexes.echappe_caracteres(res['nom_machine']),
                'projet': Annexes.echappe_caracteres(res['intitule_projet']),
                'reserve': Annexes.echappe_caracteres(res['date_reservation']),
                'supprime': Annexes.echappe_caracteres(res['date_suppression']),
                'shp': Annexes.format_heure(res['duree_hp']), 'shc': Annexes.format_heure(res['duree_hc']),
                'fhp': Annexes.format_heure(res['duree_fact_hp']), 'fhc': Annexes.format_heure(res['duree_fact_hc']),
                't7': "%d" % machine['t_h_machine_hp_p'], 't8': "%d" % machine['t_h_machine_hp_np'],
                't9': "%d" % machine['t_h_machine_hc_p'], 't10': "%d" % machine['t_h_machine_hc_np'], 'p7': p7,
                'p8': p8, 'p9': p9, 'p10': p10}

        ligne = ""
        if res['duree_fact_hp'] > 0:
            ligne += r'''%(date)s & %(heure)s & %(machine)s & HP & %(shp)s & %(fhp)s & %(t7)s & %(t8)s & %(p7)s &
                %(p8)s \\
                \hline''' % dico

        if res['duree_fact_hc'] > 0:
            ligne += r'''%(date)s & %(heure)s & %(machine)s & HC & %(shc)s & %(fhc)s & %(t9)s & %(t10)s & %(p9)s &
                %(p10)s \\
                \hline''' % dico

        if res['date_suppression'] != "":
            ligne += r'''%(date)s & %(heure)s & \multicolumn{8}{l|}{Supprimé le : %(supprime)s} \\
                \hline''' % dico

        return ligne

    @staticmethod
    def tableau_livraison(livraison, prestation):
        montant = livraison['quantite'] * prestation['prix_unit']
        total = montant - livraison['rabais']
        dico = {'date': Annexes.echappe_caracteres(livraison['date_livraison']),
                'prestation': Annexes.echappe_caracteres(livraison['designation']),
                'categorie': prestation['categorie'], 'quantite': livraison['quantite'],
                'unite': Annexes.echappe_caracteres(livraison['unite']),
                'rapport': prestation['prix_unit'], 'montant': "%.2f" % montant, 'rabais': "%.2f" % livraison['rabais'],
                'total': "%.2f" % total, 'projet': Annexes.echappe_caracteres(livraison['intitule_projet']),
                'id': livraison['id_livraison'], 'responsable': Annexes.echappe_caracteres(livraison['responsable']),
                'commande': Annexes.echappe_caracteres(livraison['date_commande']),
                'remarque': Annexes.echappe_caracteres(livraison['remarque'])}
        structure = r'''{|p{1.8cm}|p{4cm}|p{0.7cm}|p{0.8cm}|p{1.5cm}|p{1.4cm}|p{1.4cm}|p{1.1cm}|p{1.0cm}|}'''
        legende = r'''Livraisons pour ''' + livraison['id_compte'] + r''' / ''' + livraison['num_projet']
        contenu = r'''Date livraison & Intitulé & Cat. & Qu. & Unité & [CHF/u] & Montant [CHF] &
            Rabais [CHF] & Total [CHF] \\
            \hline
            %(date)s & %(prestation)s & %(categorie)s & %(quantite)s & %(unite)s &
            %(rapport)s & %(montant)s & %(rabais)s & %(total)s \\
            \hline
            Projet & %(projet)s & & & & & & & \\
            \hline
            Num livraison & %(id)s & & & & & & & \\
            \hline
            Livré par & %(responsable)s & & & & & & & \\
            \hline
            Commande & %(commande)s & & & & & & & \\
            \hline
            Remarque & %(remarque)s & & & & & & & \\
            \hline
            ''' % dico

        return Annexes.tableau(contenu, structure, legende)

    @staticmethod
    def annexes():
        print("annexes")

    @staticmethod
    def creer_latex(nom_fichier, contenu, nom_dossier=""):
        with open(nom_fichier + ".tex", 'w') as f:
            f.write(contenu)

        proc = subprocess.Popen(['pdflatex', nom_fichier + ".tex"])
        proc.communicate()

        os.unlink(nom_fichier + '.tex')
        os.unlink(nom_fichier + '.log')
        os.unlink(nom_fichier + '.aux')

        if nom_dossier != "":
            proc = subprocess.Popen(['mv', nom_fichier + ".pdf", nom_dossier])
            proc.communicate()

    @staticmethod
    def echappe_caracteres(texte):
        p = re.compile("[^ a-zA-Z0-9_'èéêàô.:,;\-%&$/|]")
        texte = p.sub('', texte)
        caracteres = ['%', '$', '_', '&']
        latex_c = ['\%', '\$', '\_', '\&']
        for pos in range(0, len(caracteres)):
            texte = texte.replace(caracteres[pos], latex_c[pos])
        return texte

    @staticmethod
    def format_heure(nombre):
        heures = "%d" % (nombre // 60)
        if (nombre // 60) < 10:
            heures = '0' + heures
        minutes = "%d" % (nombre % 60)
        if (nombre % 60) < 10:
            minutes = '0' + minutes
        return heures + ':' + minutes

    @staticmethod
    def format_si_nul(nombre):
        if nombre > 0:
            return "%.2f" % nombre
        else:
            return '-'
