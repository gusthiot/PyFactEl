import subprocess
import shlex
import os

class Latex(object):

    @staticmethod
    def creer(nom_fichier, contenu):
        with open(nom_fichier + ".tex",'w') as f:
            f.write(contenu)

        proc=subprocess.Popen(shlex.split('pdflatex ' + nom_fichier + ".tex"))
        proc.communicate()

        os.unlink(nom_fichier + '.tex')
        os.unlink(nom_fichier + '.log')
        os.unlink(nom_fichier + '.aux')

    @staticmethod
    def example(titre, soustitre):
        content=r'''\documentclass{article}
        \begin{document}
        ...
        \textbf{\huge %(title)s \\}
        \vspace{1cm}
        \textbf{\Large %(subtitle)s \\}
        ...
        \end{document}
        '''

        dictio = {'title': titre, 'subtitle': soustitre}

        Latex.creer("test", content%dictio)
