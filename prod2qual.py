import csv
import os

class Prod2Qual(object):
    def __init__(self, dossier_csv, delimiteur):
        qas_codes_csv = os.path.join(dossier_csv, "QAS_vs_PRD.csv")
        if not os.path.exists(qas_codes_csv):
            self.actif = False
            return
        self.actif = True
        self._conv = dict((kv["PRD"], kv["QAS"]) for kv in list(csv.DictReader(open(qas_codes_csv), delimiter=delimiteur)))
                         
    def prod2qual(self, code_client_prod):
        assert self.actif
            
        if code_client_prod in self._conv:
            return self._conv[code_client_prod]
        else:
            return "XXX" + str(code_client_prod)
