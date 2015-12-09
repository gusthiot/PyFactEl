

class Rabais(object):

    @staticmethod
    def rabais_reservation(drsf, supp, shp, shc):
        if drsf == 0:
            return 0, 0
        else :
            k = max(0, min(1, (1-supp / drsf)))
            fhp = round(k * shp, 0)
            fhc = round(k * shc, 0)
            return fhp, fhc

    @staticmethod
    def rabais_emolument(pt, qt, ot, lt, ct, wt, xt, emb, fix, coef_a, regle):
            somme_eq = pt + qt
            somme_sb = pt + qt + ot
            somme_t = pt + qt + ot + lt + ct + wt + xt
            em = emb
            er0 = -round((min(emb, max(0, emb - fix - (coef_a - 1) * somme_eq))/10)*10, 0)
            if ((regle == "ZERO") and (somme_t == 0)) or ((regle == "NON") and (somme_sb == 0)):
                er = em
            else:
                er = er0
            return somme_eq, somme_sb, somme_t, em, er0, er

    @staticmethod
    def rabais_plafonnement(somme_j_pm, s, k):
        prj = -min(0, min(somme_j_pm, s) + k * max(0, somme_j_pm - s) - somme_j_pm)
        qrj = 0
        orj = 0
        return prj, qrj, orj
