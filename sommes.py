from interfaces import Interfaces


class Sommes(object):
    """ métodes de claculs des sommes"""


    @staticmethod
    def nouveau_somme_projet():
        cles_somme_projet = ['somme_p_pu', 'somme_p_pv', 'somme_p_pm', 'somme_p_qu', 'somme_p_qv', 'somme_p_qm',
                             'somme_p_om', 'somme_p_nm', 'somme_p_lm', 'somme_p_lr', 'lp', 'somme_p_cm', 'somme_p_cr',
                             'cp', 'somme_p_wm', 'somme_p_wr', 'wp', 'somme_p_xm', 'somme_p_xr', 'xp']
        somme_projet = {}
        for cle in cles_somme_projet:
            somme_projet[cle] = 0
        return somme_projet



    @staticmethod
    def sommes_par_projet(livraisons, reservations, acces, prestations):
        comptes = {}
        for acce in acces.donnees:
            id_compte = acce['id_compte']
            if id_compte not in comptes:
                comptes[id_compte] = {}
            num_projet = acce['num_projet']
            compte = comptes[id_compte]
            if num_projet not in compte:
                compte[num_projet] = Sommes.nouveau_somme_projet()
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
            if id_compte not in comptes:
                comptes[id_compte] = {}
            num_projet = reservation['num_projet']
            compte = comptes[id_compte]
            if num_projet not in compte:
                compte[num_projet] = Sommes.nouveau_somme_projet()
            projet = compte[num_projet]
            projet['somme_p_pv'] += reservation['pv']
            projet['somme_p_pm'] += reservation['pv']
            projet['somme_p_qv'] += reservation['qv']
            projet['somme_p_qm'] += reservation['qv']
            projet['somme_p_qm'] += reservation['qv']

        for livraison in livraisons.donnees:
            id_compte = livraison['id_compte']
            if id_compte not in comptes:
                comptes[id_compte] = {}
            num_projet = livraison['num_projet']
            compte = comptes[id_compte]
            if num_projet not in compte:
                compte[num_projet] = Sommes.nouveau_somme_projet()
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
                0
            else:
                Interfaces.log_erreur("Catégorie de prestation non-disponible")

        print("ouf...")
