# This Python file uses the following encoding: utf-8

"""
Fichier principal à lancer pour faire tourner le logiciel

Usage:
  main.py [options]

Options:

  -h   --help              Affiche le présent message
  --entrees <chemin>       Chemin des fichiers d'entrée
  --sansgraphiques         Pas d'interface graphique
"""

import sys
from docopt import docopt

from importes import Client, Acces, CoefMachine, CoefPrest, Compte, Livraison, Machine, Prestation, Reservation
from outils import Outils
from parametres import Edition, Generaux
from traitement import Annexes, BilanMensuel, Facture, Sommes, Verification
from prod2qual import Prod2Qual
from latex import Latex

arguments = docopt(__doc__)

plateforme = sys.platform
encodage = "cp1252"
delimiteur = ';'

if arguments["--sansgraphiques"]:
    Outils.interface_graphique(False)

if arguments["--entrees"] :
  dossier_data = arguments["--entrees"]
else:
  dossier_data = Outils.choisir_dossier(plateforme)
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

dossier_enregistrement = Outils.chemin_dossier([generaux.donnees['chemin'][1], edition.annee,
                                                Outils.mois_string(edition.mois)], plateforme, generaux)
dossier_lien = Outils.lien_dossier([generaux.donnees['lien'][1], edition.annee, Outils.mois_string(edition.mois)],
                                   plateforme, generaux)
livraisons.calcul_montants(prestations, coefprests, comptes, clients, verification)
reservations.calcul_montants(machines, coefmachines, comptes, clients, verification)
acces.calcul_montants(machines, coefmachines, comptes, clients, verification)

sommes = Sommes(verification, generaux)
sommes.calculer_toutes(livraisons, reservations, acces, prestations, comptes, clients)

if edition.version == '0':
    dossier_csv = Outils.chemin_dossier([dossier_enregistrement, "csv_0"], plateforme, generaux)
else:
    dossier_csv = Outils.chemin_dossier([dossier_enregistrement, "csv_" + edition.version + "_" +
                                         edition.client_unique], plateforme, generaux)

annexes = "annexes"
dossier_annexes = Outils.chemin_dossier([dossier_enregistrement, annexes], plateforme, generaux)
lien_annexes = Outils.lien_dossier([dossier_lien, annexes], plateforme, generaux)
annexes_techniques = "annexes_techniques"
dossier_annexes_techniques = Outils.chemin_dossier([dossier_enregistrement, annexes_techniques], plateforme, generaux)
lien_annexes_techniques = Outils.lien_dossier([dossier_lien, annexes_techniques], plateforme, generaux)

Facture.factures(sommes, dossier_csv, encodage, delimiteur, edition, generaux, clients, comptes, lien_annexes,
                 lien_annexes_techniques, annexes, annexes_techniques)

prod2qual = Prod2Qual(dossier_data, delimiteur)
if prod2qual.actif:
    Facture.factures(sommes, dossier_csv, encodage, delimiteur, edition, generaux, clients, comptes, lien_annexes,
                     lien_annexes_techniques, annexes, annexes_techniques, prod2qual.prod2qual)

if Latex.possibles():
    Annexes.annexes_techniques(sommes, clients, edition, livraisons, acces, machines, reservations, prestations,
                               comptes, dossier_annexes_techniques, plateforme, coefprests, generaux)
    Annexes.annexes(sommes, clients, edition, livraisons, acces, machines, reservations, prestations, comptes,
                    dossier_enregistrement, plateforme, coefprests, generaux)

BilanMensuel.bilan(dossier_csv, encodage, delimiteur, edition, sommes, clients, generaux, acces,
                   reservations, livraisons, comptes)

liste_archiver = [acces.nom_fichier, clients.nom_fichier, coefmachines.nom_fichier, coefprests.nom_fichier,
                  comptes.nom_fichier, livraisons.nom_fichier, machines.nom_fichier, prestations.nom_fichier,
                  reservations.nom_fichier, generaux.nom_fichier, edition.nom_fichier]
Outils.archiver_liste(liste_archiver, dossier_csv)

Outils.affiche_message("OK !!!")
