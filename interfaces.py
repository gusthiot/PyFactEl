from tkinter.filedialog import *


class Interfaces(object):
    """
    Classe contenant quelques interfaces graphiques
    """

    @staticmethod
    def log_erreur(message):
        """
        affiche une petite boite de dialogue avec un message d'erreur et un bouton OK
        :param message: message à afficher
        """
        fenetre = Tk()
        fenetre.title("Erreur")
        label = Label(fenetre, text=message)
        label.pack()
        button = Button(fenetre, text='OK', command=fenetre.destroy)
        button.pack()
        mainloop()

    @staticmethod
    def choisir_dossier():
        """
        affiche une interface permettant de choisir un dossier
        :return: la position du dossier sélectionné
        """
        fenetre = Tk()
        fenetre.title("Choix du dossier")
        dossier = askdirectory(parent=fenetre, initialdir="/home/cgusthiot/Bureau",
                               title='Choisissez un dossier de travail')
        fenetre.destroy()
        if dossier == "":
            Interfaces.log_erreur("Aucun dossier choisi")
            sys.exit("Aucun dossier choisi")
        return dossier

    @staticmethod
    def choisir_edition():
        """
        affiche l'interface d'édition tant que la sélection n'est pas cohérente (non-utilisé actuellement)
        :return: tableau contenant 'année', 'mois' et 'version'
        """
        while 1:
            entree = Interfaces.interface_edition()
            if entree['annee'] == "" or entree['mois'] == "" or entree['version'] == "":
                Interfaces.log_erreur("Impossible de laisser un champ vide, veuillez réessayer")
                continue
            entree['annee'] = int(entree['annee'])
            entree['mois'] = int(entree['mois'])
            if entree['annee'] < 1900 or entree['annee'] > 2100:
                Interfaces.log_erreur("L'annéée paraît irréaliste, veuillez réessayer")
                continue
            if entree['mois'] < 1 or entree['mois'] > 12:
                Interfaces.log_erreur("L'année compte 12 mois (1-12), veuillez réessayer")
                continue
            return entree

    @staticmethod
    def interface_edition():
        """
        affiche une boite de dialogue permettant de choisir les paramètres d'édition (non utilisé actuellement)
        :return: tableau contenant 'année', 'mois' et 'version'
        """
        reponse = {}
        fenetre = Tk()

        def retourner():
            reponse['annee'] = var_annee.get()
            reponse['mois'] = var_mois.get()
            reponse['version'] = entree_version.get()
            fenetre.destroy()

        Label(fenetre, text='Année : ').pack(side=LEFT)
        var_annee = StringVar(fenetre)
        annees = [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020]
        var_annee.set(annees[5])
        select_annee = OptionMenu(fenetre, var_annee, *annees)
        select_annee.pack(side=LEFT)

        Label(fenetre, text='Mois : ').pack(side=LEFT)
        var_mois = StringVar(fenetre)
        mois = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        var_mois.set(mois[0])
        select_mois = OptionMenu(fenetre, var_mois, *mois)
        select_mois.pack(side=LEFT)

        Label(fenetre, text='Version : ').pack(side=LEFT)
        entree_version = Entry(fenetre, width=5)
        entree_version.insert(0, '0')
        entree_version.pack(side=LEFT)

        button = Button(fenetre, text='Ok', command=retourner)
        button.pack()
        mainloop()
        return reponse
