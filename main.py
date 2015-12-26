import sys

from importes import Client, Acces, CoefMachine, CoefPrest, Compte, Livraison, Machine, Prestation, Reservation
from annexes import Annexes
from interfaces import Interfaces
from parametres import Edition, Generaux
from sommes import Sommes
from facture import Facture

encodage = "ISO-8859-1"
delimiteur = ';'
dossier_data = Interfaces.choisir_dossier() + "/"
edition = Edition(dossier_data, delimiteur, encodage)  # Interfaces.choisir_edition()

acces = Acces(dossier_data, delimiteur, encodage)
clients = Client(dossier_data, delimiteur, encodage)
coefmachines = CoefMachine(dossier_data, delimiteur, encodage)
coefprests = CoefPrest(dossier_data, delimiteur, encodage)
comptes = Compte(dossier_data, delimiteur, encodage)
livraisons = Livraison(dossier_data, delimiteur, encodage)
machines = Machine(dossier_data, delimiteur, encodage)
prestations = Prestation(dossier_data, delimiteur, encodage)
reservations = Reservation(dossier_data, delimiteur, encodage)

generaux = Generaux(dossier_data, delimiteur, encodage)

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

if verif > 0:
    sys.exit("Erreur dans les dates")

verif += acces.est_coherent(comptes, machines)
verif += reservations.est_coherent(comptes, machines)
verif += livraisons.est_coherent(comptes, prestations)
verif += machines.est_coherent(coefmachines)
verif += prestations.est_coherent(generaux)
verif += coefmachines.est_coherent()
verif += coefprests.est_coherent()
verif += clients.est_coherent(coefmachines, coefprests, generaux)


clients_actifs = []
for code in livraisons.obtenir_codes(comptes, prestations):
    if code not in clients_actifs:
        clients_actifs.append(code)
for code in reservations.obtenir_codes(comptes, machines):
    if code not in clients_actifs:
        clients_actifs.append(code)
for code in acces.obtenir_codes(comptes, machines):
    if code not in clients_actifs:
        clients_actifs.append(code)

if (edition.version != '0') and (len(clients_actifs) > 1):
    Interfaces.log_erreur("Si version différente de 0, un seul client autorisé")
    sys.exit("Trop de clients pour version > 0")

verif += comptes.est_coherent(clients, coefmachines, coefprests, generaux, clients_actifs)

if verif > 0:
    sys.exit("Erreur dans la cohérence")

livraisons.calcul_montants(prestations, coefprests, comptes, clients)
reservations.calcul_montants(machines, coefmachines, comptes, clients)
acces.calcul_montants(machines, coefmachines, comptes, clients)
spp = Sommes.sommes_par_projet(livraisons, reservations, acces, prestations, comptes)
# Sommes.afficher_somme_projet(spp, dossier_data, encodage, delimiteur)
spco = Sommes.somme_par_compte(spp, comptes)
# Sommes.afficher_somme_compte(spco, dossier_data, encodage, delimiteur)
spca = Sommes.somme_par_categorie(spco, comptes)
# Sommes.afficher_somme_categorie(spca, dossier_data, encodage, delimiteur)
spcl = Sommes.somme_par_client(spca, clients)
# Sommes.afficher_somme_client(spcl, dossier_data, encodage, delimiteur)

Facture.factures(spcl, spco, dossier_data, encodage, delimiteur, edition, generaux, clients, comptes)

Annexes.annexes_techniques(spcl, spco, spca, spp, clients, edition, livraisons, acces, machines, reservations,
                               prestations, comptes, dossier_data)

Interfaces.log_erreur("OK !!!")
