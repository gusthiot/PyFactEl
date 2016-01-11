from interfaces import Interfaces
from rabais import Rabais
import csv


class Sommes(object):
    """
    Classe contenant les méthodes pour le calcul des sommes par projet, compte, catégorie et client
    """

    cles_somme_projet = ['intitule', 'somme_p_pu', 'somme_p_pv', 'somme_p_pm', 'somme_p_qu', 'somme_p_qv', 'somme_p_qm',
                         'somme_p_om', 'somme_p_nm', 'somme_p_lm', 'somme_p_lr', 'lp', 'somme_p_cm', 'somme_p_cr',
                         'cp', 'somme_p_wm', 'somme_p_wr', 'wp', 'somme_p_xm', 'somme_p_xr', 'xp']

    cles_somme_compte = ['somme_j_pu', 'somme_j_pv', 'somme_j_pm', 'prj', 'pj', 'somme_j_qu', 'somme_j_qv',
                         'somme_j_qm', 'qrj', 'qj', 'somme_j_om', 'orj', 'oj', 'somme_j_nm', 'nrj', 'nj',
                         'somme_j_lm', 'somme_j_lr', 'lj', 'somme_j_cm', 'somme_j_cr', 'cj', 'somme_j_wm',
                         'somme_j_wr', 'wj', 'somme_j_xm', 'somme_j_xr', 'xj', 'si_facture']

    cles_somme_categorie = ['somme_k_pu', 'somme_k_pv', 'somme_k_pm', 'somme_k_prj', 'pk', 'somme_k_qu',
                            'somme_k_qv', 'somme_k_qm', 'somme_k_qrj', 'qk', 'somme_k_om', 'somme_k_orj', 'ok',
                            'somme_k_nm', 'somme_k_nrj', 'nk', 'somme_k_lm', 'somme_k_lr', 'lk', 'somme_k_cm',
                            'somme_k_cr', 'ck', 'somme_k_wm', 'somme_k_wr', 'wk', 'somme_k_xm', 'somme_k_xr', 'xk']

    cles_somme_client = ['somme_t_pu', 'somme_t_pv', 'somme_t_pm', 'somme_t_prj', 'pt', 'somme_t_qu',
                         'somme_t_qv', 'somme_t_qm', 'somme_t_qrj', 'qt', 'somme_t_om', 'somme_t_orj', 'ot',
                         'somme_t_nm', 'somme_t_nrj', 'nt', 'somme_t_lm', 'somme_t_lr', 'lt', 'somme_t_cm',
                         'somme_t_cr', 'ct', 'somme_t_wm', 'somme_t_wr', 'wt', 'somme_t_xm', 'somme_t_xr', 'xt',
                         'somme_eq', 'somme_sb', 'somme_t', 'em', 'er0', 'er', 'e']

    def __init__(self, verification):

        self.verification = verification
        self.sommes_projets = {}
        self.sp = 0
        self.sommes_comptes = {}
        self.sco = 0
        self.sommes_categories = {}
        self.sca = 0
        self.sommes_clients = {}
        self.calculees = 0

    def calculer_toutes(self, livraisons, reservations, acces, prestations, comptes, clients):
        self.sommes_par_projet(livraisons, reservations, acces, prestations, comptes)
        self.somme_par_compte(comptes)
        self.somme_par_categorie(comptes)
        self.somme_par_client(clients)

    @staticmethod
    def nouveau_somme(cles):
        """
        créé un nouveau dictionnaire avec les clés entrées
        :param cles: clés pour le dictionnaire
        :return: dictionnaire indexé par les clés données, avec valeurs à zéro
        """
        somme = {}
        for cle in cles:
            somme[cle] = 0
        return somme

    @staticmethod
    def ordonner_keys_str_par_int(keys):
        """
        ordonne une liste de clés-nombres enregistrées comme string par ordre croissant
        :param keys: clés à trier
        :return: clés triées
        """
        ordonne = []
        for key in keys:
            ordonne.append(int(key))
        ordonne = sorted(ordonne)
        for pos in range(0, len(ordonne)):
            ordonne[pos] = str(ordonne[pos])
        return ordonne

    def sommes_par_projet(self, livraisons, reservations, acces, prestations, comptes):
        """
        calcule les sommes par projets sous forme de dictionnaire : client->compte->projet->clés_sommes
        :param livraisons: livraisons importées et vérifiées
        :param reservations: réservations importées et vérifiées
        :param acces: accès machines importés et vérifiés
        :param prestations: prestations importées et vérifiées
        :param comptes: comptes importés et vérifiés
        """

        if self.verification.a_verifier != 0:
            info = "Sommes :  vous devez faire les vérifications avant de calculer les sommes"
            print(info)
            Interfaces.log_erreur(info)
            return

        spp = {}
        for acce in acces.donnees:
            id_compte = acce['id_compte']
            co = comptes.donnees[id_compte]
            code_client = co['code_client']
            if code_client not in spp:
                spp[code_client] = {}
            client = spp[code_client]
            if id_compte not in client:
                client[id_compte] = {}
            num_projet = acce['num_projet']
            compte = client[id_compte]
            if num_projet not in compte:
                compte[num_projet] = Sommes.nouveau_somme(Sommes.cles_somme_projet)
                projet = compte[num_projet]
                projet['intitule'] = acce['intitule_projet']
            else:
                projet = compte[num_projet]
            projet['somme_p_pu'] += acce['pu']
            projet['somme_p_pm'] += acce['pu']
            projet['somme_p_qu'] += acce['qu']
            projet['somme_p_qm'] += acce['qu']
            projet['somme_p_om'] += acce['om']
            projet['somme_p_nm'] += acce['om']
            projet['somme_p_nm'] += acce['qu']

        for reservation in reservations.donnees:
            id_compte = reservation['id_compte']
            co = comptes.donnees[id_compte]
            code_client = co['code_client']
            if code_client not in spp:
                spp[code_client] = {}
            client = spp[code_client]
            if id_compte not in client:
                client[id_compte] = {}
            num_projet = reservation['num_projet']
            compte = client[id_compte]
            if num_projet not in compte:
                compte[num_projet] = Sommes.nouveau_somme(Sommes.cles_somme_projet)
                projet = compte[num_projet]
                projet['intitule'] = reservation['intitule_projet']
            else:
                projet = compte[num_projet]
            projet['somme_p_pv'] += reservation['pv']
            projet['somme_p_pm'] += reservation['pv']
            projet['somme_p_qv'] += reservation['qv']
            projet['somme_p_qm'] += reservation['qv']
            projet['somme_p_nm'] += reservation['qv']

        for livraison in livraisons.donnees:
            id_compte = livraison['id_compte']
            co = comptes.donnees[id_compte]
            code_client = co['code_client']
            if code_client not in spp:
                spp[code_client] = {}
            client = spp[code_client]
            if id_compte not in client:
                client[id_compte] = {}
            num_projet = livraison['num_projet']
            compte = client[id_compte]
            if num_projet not in compte:
                compte[num_projet] = Sommes.nouveau_somme(Sommes.cles_somme_projet)
                projet = compte[num_projet]
                projet['intitule'] = livraison['intitule_projet']
            else:
                projet = compte[num_projet]

            id_prestation = livraison['id_prestation']
            prestation = prestations.donnees[id_prestation]
            categorie = prestation['categorie']

            if categorie == 'L':
                projet['somme_p_lm'] += livraison['montant']
                projet['somme_p_lr'] += livraison['rabais_r']
                projet['lp'] += livraison['montant'] - livraison['rabais_r']
            elif categorie == 'C':
                projet['somme_p_cm'] += livraison['montant']
                projet['somme_p_cr'] += livraison['rabais_r']
                projet['cp'] += livraison['montant'] - livraison['rabais_r']
            elif categorie == 'W':
                projet['somme_p_wm'] += livraison['montant']
                projet['somme_p_wr'] += livraison['rabais_r']
                projet['wp'] += livraison['montant'] - livraison['rabais_r']
            elif categorie == 'X':
                projet['somme_p_xm'] += livraison['montant']
                projet['somme_p_xr'] += livraison['rabais_r']
                projet['xp'] += livraison['montant'] - livraison['rabais_r']
            else:
                Interfaces.log_erreur("Catégorie de prestation non-disponible")

        self.sp = 1
        self.sommes_projets = spp

    @staticmethod
    def afficher_somme_projet(somme_projet, nom_dossier, encodage, delimiteur):
        csv_fichier = open(nom_dossier + "somme_projet.csv", 'w', newline='', encoding=encodage)
        fichier_writer = csv.writer(csv_fichier, delimiter=delimiteur, quotechar='|')

        keys0 = Sommes.ordonner_keys_str_par_int(somme_projet.keys())
        for code_client in keys0:
            print(code_client)
            client = somme_projet[code_client]
            keys = Sommes.ordonner_keys_str_par_int(client.keys())
            for id_compte in keys:
                print(id_compte)
                compte = client[id_compte]
                keys2 = Sommes.ordonner_keys_str_par_int(compte.keys())
                for num_projet in keys2:
                    print("  " + str(num_projet))
                    fichier_writer.writerow([code_client, id_compte, num_projet])
                    projet = compte[num_projet]
                    for cle in Sommes.cles_somme_projet:
                        print("   " + cle + " : %.2f" % projet[cle])
                        fichier_writer.writerow([cle, "%.2f" % projet[cle]])
                    fichier_writer.writerow([" "])

    def somme_par_compte(self, comptes):
        """
        calcule les sommes par comptes sous forme de dictionnaire : client->compte->clés_sommes
        :param comptes: comptes importés et vérifiés
        """

        if self.sp != 0:
            spc = {}
            for code_client, client in self.sommes_projets.items():
                if code_client not in spc:
                    spc[code_client] = {}
                cl = spc[code_client]
                for id_compte, compte in client.items():
                    cc = comptes.donnees[id_compte]
                    cl[id_compte] = Sommes.nouveau_somme(Sommes.cles_somme_compte)
                    somme = cl[id_compte]
                    for num_projet, projet in compte.items():
                        somme['somme_j_pu'] += projet['somme_p_pu']
                        somme['somme_j_pv'] += projet['somme_p_pv']
                        somme['somme_j_pm'] += projet['somme_p_pm']
                        somme['somme_j_qu'] += projet['somme_p_qu']
                        somme['somme_j_qv'] += projet['somme_p_qv']
                        somme['somme_j_qm'] += projet['somme_p_qm']
                        somme['somme_j_om'] += projet['somme_p_om']
                        somme['somme_j_nm'] += projet['somme_p_nm']
                        somme['somme_j_lm'] += projet['somme_p_lm']
                        somme['somme_j_lr'] += projet['somme_p_lr']
                        somme['lj'] += projet['lp']
                        somme['somme_j_cm'] += projet['somme_p_cm']
                        somme['somme_j_cr'] += projet['somme_p_cr']
                        somme['cj'] += projet['cp']
                        somme['somme_j_wm'] += projet['somme_p_wm']
                        somme['somme_j_wr'] += projet['somme_p_wr']
                        somme['wj'] += projet['wp']
                        somme['somme_j_xm'] += projet['somme_p_xm']
                        somme['somme_j_xr'] += projet['somme_p_xr']
                        somme['xj'] += projet['xp']

                    somme['prj'], somme['qrj'], somme['orj'] = Rabais.rabais_plafonnement(somme['somme_j_pm'], cc['seuil'],
                                                                                          cc['pourcent'])

                    somme['pj'] = somme['somme_j_pm'] - somme['prj']
                    somme['qj'] = somme['somme_j_qm'] - somme['qrj']
                    somme['oj'] = somme['somme_j_om'] - somme['orj']

                    somme['nrj'] = somme['qrj'] + somme['orj']
                    somme['nj'] = somme['somme_j_nm'] - somme['nrj']
                    tot = somme['somme_j_pm'] + somme['somme_j_qm'] + somme['somme_j_om'] + somme['somme_j_lm'] + \
                          somme['somme_j_cm'] + somme['somme_j_wm'] + somme['somme_j_xm']
                    if tot > 0:
                        somme['si_facture'] = 1

                    self.sco = 1
                    self.sommes_comptes = spc

        else:
            info = "Vous devez d'abord faire la somme par projet, avant la somme par compte"
            print(info)
            Interfaces.log_erreur(info)

    @staticmethod
    def afficher_somme_compte(somme_compte, nom_dossier, encodage, delimiteur):
        csv_fichier = open(nom_dossier + "somme_compte.csv", 'w', newline='', encoding=encodage)
        fichier_writer = csv.writer(csv_fichier, delimiter=delimiteur, quotechar='|')

        keys0 = Sommes.ordonner_keys_str_par_int(somme_compte.keys())
        for code_client in keys0:
            print(code_client)
            client = somme_compte[code_client]
            keys = Sommes.ordonner_keys_str_par_int(client.keys())
            for id_compte in keys:
                print(id_compte)
                fichier_writer.writerow([code_client, id_compte])
                compte = client[id_compte]
                for cle in Sommes.cles_somme_compte:
                    print("   " + cle + " : %.2f" % compte[cle])
                    fichier_writer.writerow([cle, "%.2f" % compte[cle]])
                fichier_writer.writerow([" "])

    def somme_par_categorie(self, comptes):
        """
        calcule les sommes par catégories sous forme de dictionnaire : client->catégorie->clés_sommes
        :param comptes: comptes importés et vérifiés
        """

        if self.verification.a_verifier != 0:
            info = "Sommes :  vous devez faire les vérifications avant de calculer les sommes"
            print(info)
            Interfaces.log_erreur(info)
            return

        if self.sco != 0:
            spc = {}
            for code_client, client in self.sommes_comptes.items():
                if code_client not in spc:
                    spc[code_client] = {}
                cl = spc[code_client]
                for id_compte, compte in client.items():
                    co = comptes.donnees[id_compte]
                    categorie = co['categorie']
                    if categorie not in cl:
                        cl[categorie] = Sommes.nouveau_somme(Sommes.cles_somme_categorie)
                    somme = cl[categorie]

                    somme['somme_k_pu'] += compte['somme_j_pu']
                    somme['somme_k_pv'] += compte['somme_j_pv']
                    somme['somme_k_pm'] += compte['somme_j_pm']
                    somme['somme_k_prj'] += compte['prj']
                    somme['pk'] += compte['pj']
                    somme['somme_k_qu'] += compte['somme_j_qu']
                    somme['somme_k_qv'] += compte['somme_j_qv']
                    somme['somme_k_qm'] += compte['somme_j_qm']
                    somme['somme_k_qrj'] += compte['qrj']
                    somme['qk'] += compte['qj']
                    somme['somme_k_om'] += compte['somme_j_om']
                    somme['somme_k_orj'] += compte['orj']
                    somme['ok'] += compte['oj']
                    somme['somme_k_nm'] += compte['somme_j_nm']
                    somme['somme_k_nrj'] += compte['nrj']
                    somme['nk'] += compte['nj']
                    somme['somme_k_lm'] += compte['somme_j_lm']
                    somme['somme_k_lr'] += compte['somme_j_lr']
                    somme['lk'] += compte['lj']
                    somme['somme_k_cm'] += compte['somme_j_cm']
                    somme['somme_k_cr'] += compte['somme_j_cr']
                    somme['ck'] += compte['cj']
                    somme['somme_k_wm'] += compte['somme_j_wm']
                    somme['somme_k_wr'] += compte['somme_j_wr']
                    somme['wk'] += compte['wj']
                    somme['somme_k_xm'] += compte['somme_j_xm']
                    somme['somme_k_xr'] += compte['somme_j_xr']
                    somme['xk'] += compte['xj']

                    self.sca = 1
                    self.sommes_categories = spc

        else:
            info = "Vous devez d'abord faire la somme par compte, avant la somme par catégorie"
            print(info)
            Interfaces.log_erreur(info)

    @staticmethod
    def afficher_somme_categorie(somme_categorie, nom_dossier, encodage, delimiteur):
        csv_fichier = open(nom_dossier + "somme_categorie.csv", 'w', newline='', encoding=encodage)
        fichier_writer = csv.writer(csv_fichier, delimiter=delimiteur, quotechar='|')
        keys = Sommes.ordonner_keys_str_par_int(somme_categorie.keys())
        for code_client in keys:
            print(code_client)
            client = somme_categorie[code_client]
            keys2 = Sommes.ordonner_keys_str_par_int(client.keys())
            for categorie in keys2:
                print("  " + str(categorie))
                fichier_writer.writerow([code_client, categorie])
                cat = client[categorie]
                for cle in Sommes.cles_somme_categorie:
                    print("   " + cle + " : %.2f" % cat[cle])
                    fichier_writer.writerow([cle, "%.2f" % cat[cle]])
                fichier_writer.writerow([" "])

    def somme_par_client(self, clients):
        """
        calcule les sommes par clients sous forme de dictionnaire : client->clés_sommes
        :param clients: clients importés et vérifiés
        """

        if self.verification.a_verifier != 0:
            info = "Sommes :  vous devez faire les vérifications avant de calculer les sommes"
            print(info)
            Interfaces.log_erreur(info)
            return

        if self.sca != 0:
            spc = {}
            for code_client, client in self.sommes_categories.items():
                spc[code_client] = Sommes.nouveau_somme(Sommes.cles_somme_client)
                somme = spc[code_client]
                for categorie, som_cat in client.items():
                    somme['somme_t_pu'] += som_cat['somme_k_pu']
                    somme['somme_t_pv'] += som_cat['somme_k_pv']
                    somme['somme_t_pm'] += som_cat['somme_k_pm']
                    somme['somme_t_prj'] += som_cat['somme_k_prj']
                    somme['pt'] += som_cat['pk']
                    somme['somme_t_qu'] += som_cat['somme_k_qu']
                    somme['somme_t_qv'] += som_cat['somme_k_qv']
                    somme['somme_t_qm'] += som_cat['somme_k_qm']
                    somme['somme_t_qrj'] += som_cat['somme_k_qrj']
                    somme['qt'] += som_cat['qk']
                    somme['somme_t_om'] += som_cat['somme_k_om']
                    somme['somme_t_orj'] += som_cat['somme_k_orj']
                    somme['ot'] += som_cat['ok']
                    somme['somme_t_nm'] += som_cat['somme_k_nm']
                    somme['somme_t_nrj'] += som_cat['somme_k_nrj']
                    somme['nt'] += som_cat['nk']
                    somme['somme_t_lm'] += som_cat['somme_k_lm']
                    somme['somme_t_lr'] += som_cat['somme_k_lr']
                    somme['lt'] += som_cat['lk']
                    somme['somme_t_cm'] += som_cat['somme_k_cm']
                    somme['somme_t_cr'] += som_cat['somme_k_cr']
                    somme['ct'] += som_cat['ck']
                    somme['somme_t_wm'] += som_cat['somme_k_wm']
                    somme['somme_t_wr'] += som_cat['somme_k_wr']
                    somme['wt'] += som_cat['wk']
                    somme['somme_t_xm'] += som_cat['somme_k_xm']
                    somme['somme_t_xr'] += som_cat['somme_k_xr']
                    somme['xt'] += som_cat['xk']

                cl = clients.donnees[code_client]
                somme['somme_eq'], somme['somme_sb'], somme['somme_t'], somme['em'], somme['er0'], somme['er'] = \
                    Rabais.rabais_emolument(somme['pt'], somme['qt'], somme['ot'], somme['lt'], somme['ct'], somme['wt'],
                                            somme['xt'], cl['emol_base_mens'], cl['emol_fixe'], cl['coef'],
                                            cl['emol_sans_activite'])

                self.calculees = 1
                self.sommes_clients = spc

        else:
            info = "Vous devez d'abord faire la somme par catégorie, avant la somme par client"
            print(info)
            Interfaces.log_erreur(info)

    @staticmethod
    def afficher_somme_client(somme_client, nom_dossier, encodage, delimiteur):
        csv_fichier = open(nom_dossier + "somme_client.csv", 'w', newline='', encoding=encodage)
        fichier_writer = csv.writer(csv_fichier, delimiter=delimiteur, quotechar='|')
        keys = Sommes.ordonner_keys_str_par_int(somme_client.keys())
        for code_client in keys:
            print(code_client)
            fichier_writer.writerow([code_client])
            client = somme_client[code_client]
            for cle in Sommes.cles_somme_client:
                print("   " + cle + " : %.2f" % client[cle])
                fichier_writer.writerow([cle, "%.2f" % client[cle]])
            fichier_writer.writerow([" "])
