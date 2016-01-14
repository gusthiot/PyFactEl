import sys
from os import getcwd

from importes import Client, Acces, CoefMachine, CoefPrest, Compte, Livraison, Machine, Prestation, Reservation
from annexes import Annexes
from facture import Facture
from interfaces import Interfaces
from parametres import Edition, Generaux
from sommes import Sommes
from bilan_mensuel import BilanMensuel
from verification import Verification

"""
 fichier à lancer pour faire tourner le logiciel avec les csv de test
"""

plateforme = sys.platform
encodage = "ISO-8859-1"
delimiteur = ';'
dossier_travail = getcwd()
dossier_data = dossier_travail + "/test/"
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

verification = Verification()

if verification.verification_date(edition, acces, clients, coefmachines, coefprests, comptes, livraisons, machines,
                                  prestations, reservations) > 0:
    sys.exit("Erreur dans les dates")

if verification.verification_cohérence(generaux, edition, acces, clients, coefmachines, coefprests, comptes, livraisons,
                                       machines, prestations, reservations) > 0:
    sys.exit("Erreur dans la cohérence")

livraisons.calcul_montants(prestations, coefprests, comptes, clients, verification)
reservations.calcul_montants(machines, coefmachines, comptes, clients, verification)
acces.calcul_montants(machines, coefmachines, comptes, clients, verification)

sommes = Sommes(verification)
sommes.calculer_toutes(livraisons, reservations, acces, prestations, comptes, clients)

Facture.factures(sommes, dossier_data, encodage, delimiteur, edition, generaux, clients, comptes)

Annexes.annexes_techniques(sommes, clients, edition, livraisons, acces, machines, reservations,
                           prestations, comptes, dossier_data, plateforme)

BilanMensuel.bilan(dossier_data, encodage, delimiteur, edition, sommes, clients, generaux, acces, reservations,
                   livraisons, comptes)

Interfaces.log_erreur("OK !!!")
