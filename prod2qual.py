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
        self.prod2qual = lambda code_client_prod: self._prod2qual(code_client_prod)
        self.prod2qual.has = lambda code_client_prod: self.has(code_client_prod)
                         
    def _prod2qual(self, code_client_prod):
        assert self.actif

        if self.has(code_client_prod):
            return self._conv[code_client_prod]
        else:
            return "XXX" + str(code_client_prod)

    def has(self, code_client_prod):
        return code_client_prod in self._conv
                
