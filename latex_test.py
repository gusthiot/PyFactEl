from annexes import Annexes

content = r'''\documentclass[a4paper,landscape]{article}
\usepackage[utf8]{inputenc}

%opening
\title{Titre}
\author{Auteur}

\begin{document}


Voilà


\begin{tabular}{lll}
   1.1 & 1.2 & 1.3 \\
   2.1 & 2.2 & 2.3  \\
\end{tabular}

\end{document}
'''


Annexes.creer_latex("test", content)
