import sys
from interfaces import Interfaces


class Verification(object):

    @staticmethod
    def verification_date(edition, acces, clients, coefmachines, coefprests, comptes, livraisons, machines,
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
        return verif

    @staticmethod
    def verification_cohérence(generaux, edition, acces, clients, coefmachines, coefprests, comptes, livraisons,
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

        clients_actifs = Verification.obtenir_clients_actifs(acces, reservations, livraisons)

        if (edition.version != '0') and (len(clients_actifs) > 1):
            Interfaces.log_erreur("Si version différente de 0, un seul client autorisé")
            sys.exit("Trop de clients pour version > 0")

        verif += comptes.est_coherent(clients, clients_actifs)
        return verif

    @staticmethod
    def obtenir_clients_actifs(acces, reservations, livraisons):
        clients_actifs = []
        for code in livraisons.obtenir_codes():
            if code not in clients_actifs:
                clients_actifs.append(code)
        for code in reservations.obtenir_codes():
            if code not in clients_actifs:
                clients_actifs.append(code)
        for code in acces.obtenir_codes():
            if code not in clients_actifs:
                clients_actifs.append(code)
        return clients_actifs
