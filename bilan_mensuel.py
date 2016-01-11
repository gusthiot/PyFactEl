import csv
from sommes import Sommes
from interfaces import Interfaces


class BilanMensuel(object):

    @staticmethod
    def bilan(nom_dossier, encodage, delimiteur, edition, sommes, clients, generaux, acces, reservations, livraisons,
              comptes):

        if sommes.calculees == 0:
            info = "Vous devez d'abord faire toutes les sommes avant de pouvoir créer le bilan mensuel"
            print(info)
            Interfaces.log_erreur(info)
            return

        mois = edition.mois
        if mois < 10:
            mois = "0" + str(mois)
        else:
            mois = str(mois)
        nom = nom_dossier + "bilan_" + str(edition.annee) + "_" + mois + "_" + str(edition.version) + ".csv"
        csv_fichier = open(nom, 'w', newline='', encoding=encodage)
        fichier_writer = csv.writer(csv_fichier, delimiter=delimiteur, quotechar='|')

        fichier_writer.writerow(["année", "mois", "référence", "code client", "abrév. labo", "nom labo", "type client",
                                 "nature client", "nb utilisateurs", "nb tot comptes", "nb comptes cat 1",
                                 "nb comptes cat 2", "nb comptes cat 3", "nb comptes cat 4", "somme T", "Em base",
                                 "somme EQ", "Rabais Em", "Prj 1", "Prj 2", "Prj 3", "Prj 4", "pt", "qt", "ot", "nt",
                                 "lt", "ct", "wt", "xt"])

        keys = Sommes.ordonner_keys_str_par_int(sommes.sommes_clients.keys())

        for code_client in keys:
            scl = sommes.sommes_clients[code_client]
            sca = sommes.sommes_categories[code_client]
            cl = clients.donnees[code_client]
            nature = generaux.donnees['nature_client'][generaux.donnees['code_n'].index(cl['type_labo'])]
            reference = nature + str(edition.annee)[2:] + mois + "." + code_client
            nb_u = len(BilanMensuel.utilisateurs(acces, livraisons, reservations, code_client))
            cptes = BilanMensuel.comptes(acces, livraisons, reservations, code_client)
            cat = {'1': 0, '2': 0, '3': 0, '4': 0}
            nb_c = 0
            for cpte in cptes:
                nb_c += 1
                cat[comptes.donnees[cpte]['categorie']] += 1

            if '1' in sca:
                kprj1 = sca['1']['somme_k_prj']
            else:
                kprj1 = 0
            if '2' in sca:
                kprj2 = sca['2']['somme_k_prj']
            else:
                kprj2 = 0
            if '3' in sca:
                kprj3 = sca['3']['somme_k_prj']
            else:
                kprj3 = 0
            if '4' in sca:
                kprj4 = sca['4']['somme_k_prj']
            else:
                kprj4 = 0

            fichier_writer.writerow([edition.annee, edition.mois, reference, code_client, cl['abrev_labo'],
                                     cl['nom_labo'], 'U', cl['type_labo'], nb_u, nb_c, cat['1'], cat['2'], cat['3'],
                                     cat['4'], scl['somme_t'], scl['em'], scl['somme_eq'], scl['er'], kprj1, kprj2,
                                     kprj3, kprj4, scl['pt'], scl['qt'], scl['ot'], scl['nt'], scl['lt'], scl['ct'],
                                     scl['wt'], scl['xt']])

    @staticmethod
    def utilisateurs(acces, livraisons, reservations, code_client):
        utilisateurs = []
        for cae in acces.donnees:
            if cae['code_client'] == code_client:
                if cae['id_user'] not in utilisateurs:
                    utilisateurs.append(cae['id_user'])
        for lvr in livraisons.donnees:
            if lvr['code_client'] == code_client:
                if lvr['id_user'] not in utilisateurs:
                    utilisateurs.append(lvr['id_user'])
        for res in reservations.donnees:
            if res['code_client'] == code_client:
                if res['id_user'] not in utilisateurs:
                    utilisateurs.append(res['id_user'])
        return utilisateurs

    @staticmethod
    def comptes(acces, livraisons, reservations, code_client):
        comptes = []
        for cae in acces.donnees:
            if cae['code_client'] == code_client:
                if cae['id_compte'] not in comptes:
                    comptes.append(cae['id_compte'])
        for lvr in livraisons.donnees:
            if lvr['code_client'] == code_client:
                if lvr['id_compte'] not in comptes:
                    comptes.append(lvr['id_compte'])
        for res in reservations.donnees:
            if res['code_client'] == code_client:
                if res['id_compte'] not in comptes:
                    comptes.append(res['id_compte'])
        return comptes
