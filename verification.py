import sys
from interfaces import Interfaces


class Verification(object):

    def __init__(self):
        self.a_verifier = 2

    def verification_date(self, edition, acces, clients, coefmachines, coefprests, comptes, livraisons, machines,
                          prestations, reservations):
        verif = 0
        verif += acces.verification_date(edition.annee, edition.mois)
        verif += clients.verification_date(edition.annee, edition.mois)
        verif += coefmachines.verification_date(edition.annee, edition.mois)
        verif += coefprests.verification_date(edition.annee, edition.mois)
        verif += comptes.verification_date(edition.annee, edition.mois)
        verif += livraisons.verification_date(edition.annee, edition.mois)
        verif += machines.verification_date(edition.annee, edition.mois)
        verif += prestations.verification_date(edition.annee, edition.mois)
        verif += reservations.verification_date(edition.annee, edition.mois)
        self.a_verifier = 1
        return verif

    def verification_cohérence(self, generaux, edition, acces, clients, coefmachines, coefprests, comptes, livraisons,
                               machines, prestations, reservations):
        verif = 0
        verif += acces.est_coherent(comptes, machines)
        verif += reservations.est_coherent(comptes, machines)
        verif += livraisons.est_coherent(comptes, prestations)
        verif += machines.est_coherent(coefmachines)
        verif += prestations.est_coherent(generaux)
        verif += coefmachines.est_coherent()
        verif += coefprests.est_coherent()
        verif += clients.est_coherent(coefmachines, coefprests, generaux)

        comptes_actifs, clients_actifs = Verification.obtenir_comptes_clients_actifs(acces, reservations, livraisons)

        if (edition.version != '0') and (len(clients_actifs) > 1):
            Interfaces.log_erreur("Si version différente de 0, un seul client autorisé")
            sys.exit("Trop de clients pour version > 0")

        verif += comptes.est_coherent(clients, comptes_actifs)
        self.a_verifier = 0
        return verif

    @staticmethod
    def obtenir_comptes_clients_actifs(acces, reservations, livraisons):
        comptes_actifs = []
        clients_actifs = []
        for client, comptes in livraisons.obtenir_comptes().items():
            if client not in clients_actifs:
                clients_actifs.append(client)
            for compte in comptes:
                if compte not in comptes_actifs:
                    comptes_actifs.append(compte)
        for client, comptes in reservations.obtenir_comptes().items():
            if client not in clients_actifs:
                clients_actifs.append(client)
            for compte in comptes:
                if compte not in comptes_actifs:
                    comptes_actifs.append(compte)
        for client, comptes in acces.obtenir_comptes().items():
            if client not in clients_actifs:
                clients_actifs.append(client)
            for compte in comptes:
                if compte not in comptes_actifs:
                    comptes_actifs.append(compte)

        return comptes_actifs, clients_actifs
