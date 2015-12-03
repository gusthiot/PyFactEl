from os import getcwd
from bruts import Client, Acces, CoefMachine, CoefPrest, Compte, Livraison, Machine, Prestation, Reservation
from interfaces import Interfaces
from generaux import Generaux
from edition import Edition
from sommes import Sommes
import sys


encodage = "ISO-8859-1"
delimiteur = ';'
dossier_travail = getcwd()
dossier_data = dossier_travail + "/test/"
edition = Edition(dossier_data,delimiteur,encodage)

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

if (edition.version != '0') and (len(clients.donnees) > 1):
    Interfaces.log_erreur("Si version différente de 0, un seul client autorisé")
    sys.exit("Trop de clients pour version > 0")

verif_dat = 0
verif_dat += acces.verification_date(edition.annee, edition.mois)
verif_dat += clients.verification_date(edition.annee, edition.mois)
verif_dat += coefmachines.verification_date(edition.annee, edition.mois)
verif_dat += coefprests.verification_date(edition.annee, edition.mois)
verif_dat += comptes.verification_date(edition.annee, edition.mois)
verif_dat += livraisons.verification_date(edition.annee, edition.mois)
verif_dat += machines.verification_date(edition.annee, edition.mois)
verif_dat += prestations.verification_date(edition.annee, edition.mois)
verif_dat += reservations.verification_date(edition.annee, edition.mois)

if verif_dat > 0:
    sys.exit("Erreur dans les dates")

acces.est_coherent(comptes, machines)
reservations.est_coherent(comptes, machines)
livraisons.est_coherent(comptes, prestations)
machines.est_coherent(coefmachines)
prestations.est_coherent(generaux)
coefmachines.est_coherent()
coefprests.est_coherent()
clients.est_coherent(coefmachines, coefprests, generaux)
comptes.est_coherent(clients, coefmachines, coefprests)

print(generaux.obtenir_d1())
print(generaux.obtenir_d2())
print(generaux.obtenir_d3())

livraisons.calcul_montants(prestations, coefprests, comptes, clients)
reservations.calcul_montants(machines, coefmachines, comptes, clients)
acces.calcul_montants(machines, coefmachines, comptes, clients)

Sommes.sommes_par_projet(livraisons, reservations, acces, prestations)

Interfaces.log_erreur("OK !!!")
