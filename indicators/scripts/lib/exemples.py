#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@authors: Anne, Karim, Guillaume, Sébastien
"""

import diff
import difflib

# Affiche les résultats obtenus avec difflib pour un texte initial et un texte final
def get_opcodes_difflib(a, b):
    s = difflib.SequenceMatcher(None, a, b)
    for idx, (tag, i1, i2, j1, j2) in enumerate(s.get_opcodes()):
        if tag == 'replace':
            a2 = ' '.join(a[i1:i2])
            b2 = ' '.join(b[j1:j2])
            #s2 = difflib.SequenceMatcher(lambda x: x in " \t", a2, b2)
            s2 = difflib.SequenceMatcher(None, a2, b2)
            score = 1 - s2.ratio()
            print('{:7} ({:4}) a[{}:{}] --> b[{}:{}] {!r:>20} --> {!r}'.format(tag,
                                        round(score, 2), i1, i2, j1, j2, ' '.join(a[i1:i2]), ' '.join(b[j1:j2])))
        else:
            print('{:14} a[{}:{}] --> b[{}:{}] {!r:>20} --> {!r}'.format(tag,
                                        i1, i2, j1, j2, ' '.join(a[i1:i2]), ' '.join(b[j1:j2])))

print("Exemple 1\n")
text_user = []
text_user.append(["LabNbook est une plateforme gratuite, utilisée par plus de 2 800 élèves chaque année, à l'Université Grenoble-Alpes, Grenoble-INP, dans des collèges, lycées et des CPGE.", "etudiant1"])
text_user.append(["LabNbook est une plateforme open source et gratuite, utilisée par plus de 2 800 étudiants chaque année, à l'Université Grenoble-Alpes, Grenoble-INP, dans des lycées et des CPGE.", "etudiant2"])

# Librairie difflib
get_opcodes_difflib(text_user[0][0].split(), text_user[1][0].split())

# Calcul de diff
result = diff.contribution(text_user, debug=False)
print("\n", diff.get_users(result), "\n", diff.get_matrix(result), "\n", diff.get_words(result))


print("\nExemple 2\n")
text_user = []
text_user.append(["LabNbook est une plateforme utilisée à l'Université Grenoble-Alpes et dans des établissements secondaires ", "etudiant1"])
text_user.append(["LabNbook est une plateforme open source et gratuite, utilisée par près de 3000 élèves tout au long de l’année, à l'Université Grenoble-Alpes", "etudiant2"])
text_user.append(["LabNbook est une plateforme open source et gratuite, utilisée par plus de 2800 étudiants chaque année, à l'Université Grenoble-Alpes mais aussi dans des lycées et des CPGE", "etudiant1"])
# Librairie difflib
get_opcodes_difflib(text_user[0][0].split(), text_user[1][0].split())
print("\n")
get_opcodes_difflib(text_user[1][0].split(), text_user[2][0].split())

# Calcul de diff
result = diff.contribution(text_user, debug=False)
print("\n", diff.get_users(result), "\n", diff.get_matrix(result), "\n", diff.get_words(result))
