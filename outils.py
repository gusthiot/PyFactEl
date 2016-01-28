from tkinter.filedialog import *
from tkinter.scrolledtext import *

import shutil


class Outils(object):
    """
    Classe contenant diverses méthodes utiles
    """

    @staticmethod
    def affiche_message(message):
        """
        affiche une petite boite de dialogue avec un message et un bouton OK
        :param message: message à afficher
        """
        fenetre = Tk()
        """
        ascenseur = Scrollbar(fenetre)
        ascenseur.pack(side=RIGHT, fill=Y)
        fenetre.title("Erreur")
        texte = Text(fenetre, yscrollcommand=ascenseur.set)
        texte.insert(END, message)
        texte.pack()
        """
        fenetre.title("Erreur")
        texte = ScrolledText(fenetre)
        texte.insert(END, message)
        texte.pack()
        button = Button(fenetre, text='OK', command=fenetre.destroy)
        button.pack()
        mainloop()

    @staticmethod
    def choisir_dossier(plateforme):
        """
        affiche une interface permettant de choisir un dossier
        :return: la position du dossier sélectionné
        """
        fenetre = Tk()
        fenetre.title("Choix du dossier")
        dossier = askdirectory(parent=fenetre, initialdir="/",
                               title='Choisissez un dossier de travail')
        fenetre.destroy()
        if dossier == "":
            Outils.affiche_message("Aucun dossier choisi")
            sys.exit("Aucun dossier choisi")
        return dossier + Outils.separateur(plateforme)

    @staticmethod
    def format_heure(nombre):
        """
        transforme une heure d'un format float à un format hh:mm
        :param nombre: heure en float
        :return: heure en hh:mm
        """
        if nombre == 0:
            return ""
        heures = "%d" % (nombre // 60)
        if (nombre // 60) < 10:
            heures = '0' + heures
        minutes = "%d" % (nombre % 60)
        if (nombre % 60) < 10:
            minutes = '0' + minutes
        return heures + ':' + minutes

    @staticmethod
    def format_si_nul(nombre):
        """
        formate un nombre flottant à 2 chiffres après la virgule, retourn '-' si nul
        :param nombre: nombre flottant à formatter
        :return: nombre formaté
        """
        if nombre > 0:
            return "%.2f" % nombre
        else:
            return '-'

    @staticmethod
    def mois_string(mois):
        """
        prend un mois comme nombre, et le retourne comme string, avec un '0' devant si plus petit que 10
        :param mois: mois formaté en nombre
        :return: mois formaté en string
        """
        if mois < 10:
            return "0" + str(mois)
        else:
            return str(mois)

    @staticmethod
    def separateur(plateforme):
        """
        retourne le séprateur de chemin logique en fonction de l'OS (si windows ou pas)
        :param plateforme: OS utilisé
        :return: séparateur, string
        """
        if plateforme == "win32":
            return "\\"
        else:
            return "/"

    @staticmethod
    def eliminer_double_separateur(texte, plateforme):
        """
        élimine les doubles (back)slashs
        :return: texte nettoyé
        """
        return texte.replace(Outils.separateur(plateforme) + Outils.separateur(plateforme),
                             Outils.separateur(plateforme))

    @staticmethod
    def chemin_dossier(structure, plateforme):
        """
        construit le chemin pour enregistrer les données
        :param structure: éléments du chemin
        :param plateforme:OS utilisé
        :return:chemin logique complet pour dossier
        """
        chemin = ""
        for element in structure:
            chemin += str(element) + Outils.separateur(plateforme)
        if not os.path.exists(chemin):
            os.makedirs(chemin)
        return Outils.eliminer_double_separateur(chemin, plateforme)

    @staticmethod
    def archiver_liste(liste, dossier_archive):
        """
        archive une liste de documents
        :param liste: liste de documents
        :param dossier_archive: dossier dans lequel archiver les documents
        """
        for element in liste:
            shutil.copy(element, dossier_archive)

    @staticmethod
    def ordonner_keys_str_par_int(keys):
        """
        ordonne une liste de clés-nombres enregistrées comme string par ordre croissant
        :param keys: clés à trier
        :return: clés triées
        """
        ordonne = []
        for key in keys:
            ordonne.append(int(key))
        ordonne = sorted(ordonne)
        for pos in range(0, len(ordonne)):
            ordonne[pos] = str(ordonne[pos])
        return ordonne

    @staticmethod
    def est_un_nombre(donnee, colonne, ligne):
        """
        vérifie que la donnée est bien un nombre
        :param donnee: donnée à vérifier
        :param colonne: colonne contenant la donnée
        :param ligne: ligne contenant la donnée
        :return: la donnée formatée en nombre et un string vide si ok, 0 et un message d'erreur sinon
        """
        try:
            fl_d = float(donnee)
            return fl_d, ""
        except ValueError:
            return 0, colonne + " de la ligne " + str(ligne) + " doit être un nombre\n"
