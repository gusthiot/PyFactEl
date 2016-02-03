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
        fenetre.title("Message")
        texte = ScrolledText(fenetre)
        texte.insert(END, message)
        texte.pack()
        button = Button(fenetre, text='OK', command=fenetre.destroy)
        button.pack()
        mainloop()

    @staticmethod
    def affiche_message_conditionnel(message):
        """
        affiche une petite boite de dialogue avec un message et 2 boutons OUI/NON, le NON arrête le programme
        :param message: message à afficher
        """
        fenetre = Tk()
        fenetre.title("Message conditionnel")
        texte = ScrolledText(fenetre)
        texte.insert(END, message)
        texte.pack()
        button = Button(fenetre, text='OUI', command=fenetre.destroy)
        button.pack(side="left")
        button = Button(fenetre, text='NON', command=sys.exit)
        button.pack(side="right")
        mainloop()

    @staticmethod
    def choisir_dossier(plateforme):
        """
        affiche une interface permettant de choisir un dossier
        :param plateforme: OS utilisé
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
        return dossier + Outils.separateur_os(plateforme)

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
    def separateur_os(plateforme):
        """
        retourne le séparateur de chemin logique en fonction de l'OS (si windows ou pas)
        :param plateforme: OS utilisé
        :return: séparateur, string
        """
        if plateforme == "win32":
            return "\\"
        else:
            return "/"

    @staticmethod
    def separateur_lien(texte, generaux):
        """
        remplace le séparateur de chemin logique en fonction du lien donné dans les paramètres généraux
        :param texte: texte à traiter
        :param generaux: paramètres généraux
        :return: séparateur, string
        """
        if "\\" in generaux.donnees['lien'][1]:
            if "/" in generaux.donnees['lien'][1]:
                Outils.affiche_message("'/' et '\\' présents dans le lien des paramètres généraux !!! ")
            texte = texte.replace("/", "\\")
        else:
            texte = texte.replace("\\", "/")
        return texte.replace("//", "/").replace("\\" + "\\", "\\")

    @staticmethod
    def separateur_dossier(texte, generaux, plateforme):
        """
        remplace le séparateur de chemin logique en fonction du chemin donné dans les paramètres généraux
        :param texte: texte à traiter
        :param generaux: paramètres généraux
        :param plateforme: OS utilisé
        :return: séparateur, string
        """
        if "\\" in generaux.donnees['chemin'][1]:
            if "/" in generaux.donnees['chemin'][1]:
                Outils.affiche_message("'/' et '\\' présents dans le lien des paramètres généraux !!! ")
            texte = texte.replace("/", "\\")
            """
            if "\\" != Outils.separateur_os(plateforme):
                Outils.affiche_message_conditionnel("Le chemin d'enregistrement n'utilise pas le même séparateur que "
                                                    "l'os sur lequel tourne le logiciel. Voulez-vous tout de même "
                                                    "continuer ?")
            """
        else:
            texte = texte.replace("\\", "/")
            """
            if "/" != Outils.separateur_os(plateforme):
                Outils.affiche_message_conditionnel("Le chemin d'enregistrement n'utilise pas le même séparateur que "
                                                    "l'os sur lequel tourne le logiciel. Voulez-vous tout de même "
                                                    "continuer ?")
            """
        return texte.replace("//", "/").replace("\\" + "\\", "\\")

    @staticmethod
    def eliminer_double_separateur(texte):
        """
        élimine les doubles (back)slashs
        :param texte: texte à nettoyer
        :return: texte nettoyé
        """
        return texte.replace("//", "/").replace("\\" + "\\", "\\")

    @staticmethod
    def chemin_dossier(structure, plateforme, generaux):
        """
        construit le chemin pour enregistrer les données
        :param structure: éléments du chemin
        :param plateforme:OS utilisé
        :param generaux: paramètres généraux
        :return:chemin logique complet pour dossier
        """
        chemin = ""
        for element in structure:
            chemin += str(element) + Outils.separateur_os(plateforme)
        if not os.path.exists(chemin):
            os.makedirs(chemin)
        return Outils.eliminer_double_separateur(Outils.separateur_dossier(chemin, generaux, plateforme))

    @staticmethod
    def lien_dossier(structure, plateforme, generaux):
        """
        construit le chemin pour enregistrer les données sans vérifier son existence
        :param structure: éléments du chemin
        :param plateforme: OS utilisé
        :param generaux: paramètres généraux
        :return:chemin logique complet pour dossier
        """
        chemin = ""
        for element in structure:
            chemin += str(element) + Outils.separateur_os(plateforme)
        return Outils.eliminer_double_separateur(Outils.separateur_lien(chemin, generaux))

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
