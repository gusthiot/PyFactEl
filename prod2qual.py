import csv
import os

class Prod2Qual(object):
    def __init__(self, dossier_csv, delimiteur):
        qas_codes_csv = os.path.join(dossier_csv, "QAS_vs_PRD.csv")
        self.actif = os.path.exists(qas_codes_csv)
        if not self.actif:
            return
        self._client_conv = dict((kv["PRD"], kv["QAS"]) for kv in list(csv.DictReader(open(qas_codes_csv), delimiter=delimiteur)))
                         
    def traduire_code_client(self, code_client_prod):
        assert self.actif

        if self.code_client_existe(code_client_prod):
            return self._client_conv[code_client_prod]
        else:
            return "XXX" + str(code_client_prod)

    def code_client_existe(self, code_client_prod):
        return code_client_prod in self._client_conv

