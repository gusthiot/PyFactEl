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

from importes import Client, Acces, CoefMachine, CoefPrest, Compte, Livraison, Machine, Prestation, Reservation, DossierSource, DossierDestination
from outils import Outils
from parametres import Edition, Generaux
from traitement import Annexes, BilanMensuel, Facture, Sommes, Verification
from prod2qual import Prod2Qual
from latex import Latex

arguments = docopt(__doc__)

plateforme = sys.platform

if arguments["--sansgraphiques"]:
    Outils.interface_graphique(False)

if arguments["--entrees"] :
  dossier_data = arguments["--entrees"]
else:
  dossier_data = Outils.choisir_dossier(plateforme)
dossier_source = DossierSource(dossier_data)

edition = Edition(dossier_source)

acces = Acces(dossier_source)
clients = Client(dossier_source)
coefmachines = CoefMachine(dossier_source)
coefprests = CoefPrest(dossier_source)
comptes = Compte(dossier_source)
livraisons = Livraison(dossier_source)
machines = Machine(dossier_source)
prestations = Prestation(dossier_source)
reservations = Reservation(dossier_source)

generaux = Generaux(dossier_source)

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
destination = DossierDestination(dossier_csv)

annexes = "annexes"
dossier_annexes = Outils.chemin_dossier([dossier_enregistrement, annexes], plateforme, generaux)
lien_annexes = Outils.lien_dossier([dossier_lien, annexes], plateforme, generaux)
annexes_techniques = "annexes_techniques"
dossier_annexes_techniques = Outils.chemin_dossier([dossier_enregistrement, annexes_techniques], plateforme, generaux)
lien_annexes_techniques = Outils.lien_dossier([dossier_lien, annexes_techniques], plateforme, generaux)

facture_prod = Facture()
facture_prod.factures(sommes, destination, edition, generaux, clients, comptes,
                      lien_annexes, lien_annexes_techniques, annexes, annexes_techniques)

prod2qual = Prod2Qual(dossier_source)
if prod2qual.actif:
    facture_qual = Facture(prod2qual)
    generaux_qual = Generaux(dossier_source, prod2qual)
    facture_qual.factures(sommes, destination, edition, generaux_qual, clients, comptes,
                          lien_annexes, lien_annexes_techniques, annexes, annexes_techniques)

if Latex.possibles():
    Annexes.annexes_techniques(sommes, clients, edition, livraisons, acces, machines, reservations, prestations,
                               comptes, dossier_annexes_techniques, plateforme, coefprests, coefmachines, generaux)
    Annexes.annexes(sommes, clients, edition, livraisons, acces, machines, reservations, prestations, comptes,
                    dossier_enregistrement, plateforme, coefprests, coefmachines, generaux)

BilanMensuel.bilan(destination, edition, sommes, clients, generaux, acces,
                   reservations, livraisons, comptes)

Outils.affiche_message("OK !!!")
