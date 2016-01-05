import sys

from importes import Client, Acces, CoefMachine, CoefPrest, Compte, Livraison, Machine, Prestation, Reservation
from annexes import Annexes
from interfaces import Interfaces
from parametres import Edition, Generaux
from sommes import Sommes
from facture import Facture
from bilan_mensuel import BilanMensuel
from verification import Verification

"""
 fichier principal à lancer pour faire tourner le logiciel
"""

encodage = "ISO-8859-1"
delimiteur = ';'
dossier_data = Interfaces.choisir_dossier() + "/"
edition = Edition(dossier_data, delimiteur, encodage)

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

if Verification.verification_date(edition, acces, clients, coefmachines, coefprests, comptes, livraisons, machines,
                                  prestations, reservations) > 0:
    sys.exit("Erreur dans les dates")

if Verification.verification_cohérence(generaux, edition, acces, clients, coefmachines, coefprests, comptes, livraisons,
                                       machines, prestations, reservations) > 0:
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

BilanMensuel.bilan(dossier_data, encodage, delimiteur, edition, spca, spcl, clients, generaux, acces, reservations,
                   livraisons, comptes)

Interfaces.log_erreur("OK !!!")
