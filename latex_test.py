from exportation import Exportation


content = r'''\documentclass[a4paper,landscape]{article}
\usepackage[utf8]{inputenc}

%opening
\title{%(title)s}
\author{%(author)s}

\begin{document}


Voilà

\begin{tabular}{lll}
   1.1 & 1.2 & 1.3 \\
   2.1 & 2.2 & 2.3 \\
\end{tabular}

\end{document}
'''

dictio = {'title': "Titre", 'author': "Moi-même"}

Exportation.creer_latex("test", content % dictio)
