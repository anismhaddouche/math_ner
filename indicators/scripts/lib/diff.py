#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  5 13:19:45 2020

Pour une meilleure compréhension, lire les commentaires des fonctions en commençant
par la dernière.
"""

import difflib
import spacy
import typer

def get_users(chain):
    # Retourne la la liste des utilisateurs d'une chaine
    users_contrib = chain[1]
    users_list = [
        str(users_contrib[i][j][0])
        for i in range(len(users_contrib))
        for j in range(len(users_contrib[i]))
    ]
    users = list(set(users_list))
    users.sort()
    return users


def get_words(chain):
    # Retourne la liste des mots d'une chaine
    return chain[2]


def get_matrix(chain):
    # Retourne la matrice A, telle que a_{i,j} est la contribution de l'utilisateurs
    # i sur le mot j
    users = get_users(chain)
    words = get_words(chain)
    intervals = chain[0]
    sparse_matrix = chain[1]
    matrix = [[0.0 for w in words] for u in users]
    for interval_idx, interval in enumerate(intervals):
        users_sparse_contrib = sparse_matrix[interval_idx]
        users_contrib = [0.0 for u in users]
        for user, contrib in users_sparse_contrib:
            users_contrib[users.index(user)] = contrib
        for word_idx in range(*interval):
            for user_idx in range(len(users)):
                matrix[user_idx][word_idx] = users_contrib[user_idx]
    return matrix


# def clean_and_tokenize(text):
#     # Nettoie un texte de tout ce qui pourrait entraver sa tokenization
#     # (rien pour l'instant) puis tokenize par mot
#     #
#     # Entrée : le texte à nettoyer/tokenizer
#     # Sortie : le texte nettoyé/tokenizé
#     #
#     # TODO : gérer les signes de ponctuation ? () ... ,

#     return text.split()

# def clean_and_tokenize(text):
#     # Nettoie un texte de tout ce qui pourrait entraver sa tokenization
#     # (rien pour l'instant) puis tokenize par mot
#     #
#     # Entrée : le texte à nettoyer/tokenizer
#     # Sortie : le texte nettoyé/tokenizé
#     #
#     # TODO : gérer les signes de ponctuation ? () ... ,
#     doc = nlp(text)
#     tokens = [tok for tok in doc ]
#     return tokens


def initialize(list_of_text_user, debug):
    # Initialise la chaîne de contribution.
    #
    # -> Voir la description de la fonction "contribution" pour une définition
    #    précise de la notion de "chaine de contribution"
    #
    # Renvoie un unique segment avec le score 1 pour le user qui lui est
    # associé.
    #
    # Entrée : list_of_text_user sous forme de liste de [text, id_user].
    #          debug : génère des affichages en cas de débugage.
    # Sortie : [segments, scores, text]
    #   *segments = [[0, longueur du texte]]
    #   *scores = [[[le user du premier texte, 1]]]
    #   *text = le premier texte

    # Affichages en cas de debug
    if debug:
        print("--- Start Fonction initialize")

    text = list_of_text_user[0][0]
    id_user = list_of_text_user[0][1]
    segments = [[0, len(text)]]
    scores = [[[id_user, 1.0]]]
    chain = [segments, scores, text]

    # Affichages en cas de debug
    if debug:
        print("OUT - Chaine : ", chain)
        print("--- End Fonction initialize")

    return chain


def select_segments_idx(segments, idx_init, i1, i2, debug):
    # Renvoie la liste des index des segments compris entre i1 et i2.
    # A ce stade, i1 et i2 sont nécessairement des bornes de segments.
    #
    # Exemple 1 :
    # Liste de segments :
    #   [[0, 2],[2, 4],[4, 8],[8, 15],[15, 16],[16, 16],[16, 20]]
    #   avec i1 = 2 et i2 = 15
    # renvoie [1, 2, 3]
    #
    # Exemple 2 :
    # Liste de segments :
    #   [[0, 2],[2, 4],[4, 8],[8, 15],[15, 16],[16, 16],[16, 20]]
    #   avec i1 = 16 et i2 = 20
    # renvoie [6]
    #
    # Entrées : une liste de segments, l'indice du segment de départ
    #           i1 et i2, des entiers parmi les bornes des segments.
    #          debug : génère des affichages en cas de débugage.
    # Sortie : la liste des segments sélectionnés.

    # Affichages en cas de debug
    if debug:
        print("--- Start Fonction selected_segments_idx")
        print("IN - Segments : ", segments)
        print("IN - Idx init : ", idx_init)
        print("IN - i1 : ", i1, " i2 : ", i2)

    seg_idx = idx_init

    # Recherche de la borne inférieure
    while segments[seg_idx][0] != i1:
        seg_idx += 1

    # Si i1 est différent de i2 et que le segment est vide (de forme [a, a]),
    # on prend le segment suivant comme premier segment à sélectionner.
    # La raison est que l'insertion crée des segments vides qui n'ont pas à
    # être sélectionnés en dehors d'une insertion (i1=i2).
    # Le 2ème exemple de la description illustre la situation.
    seg_idx_i1 = seg_idx
    seg_idx_i1 += i1 != i2 and segments[seg_idx][0] == segments[seg_idx][1]

    # Recherche de la borne supérieure
    while segments[seg_idx][1] != i2:
        seg_idx += 1

    # Rajout de 1 pour le slicing de Python
    seg_idx_i2 = seg_idx + 1

    selected_segments_idx = [k for k in range(seg_idx_i1, seg_idx_i2)]

    # Affichages en cas de debug
    if debug:
        print("OUT - selected_segments_idx : ", selected_segments_idx)
        print("--- End Fonction selected_segments_idx")

    return selected_segments_idx


def simple_split(segments, idx_init, scores, i, debug):
    # Découpe le segment de la liste contenant i en deux sous segments si i
    # n'est pas une borne de celui-ci. Les scores associés au segment sont
    # dupliqués.
    #
    # Exemple :
    # Séquence de la chaine :
    #   [0, 4]  [4, 15]  [15, 16] et i = 8
    #    u1:1    u1:0.5   u1:0.75
    #    u2:0    u2:0.5   u2:0.25
    # renvoie :
    #   [0, 4]  [4, 8]  [8, 15]  [15, 16]]
    #    u1:1   u1:0.5   u1:0.5   u1:0.75
    #    u2:0   u2:0.5   u2:0.5   u2:0.25
    #
    # Entrées : la liste des segments, l'indice du segment de départ
    #           et les scores associés.
    #           i, un entier qui correspond à l'endroit où couper.
    #          debug : génère des affichages en cas de débugage.
    # Sortie : la liste des segments découpés et les scores associés
    #           (dont les scores dupliqués).

    # Affichages en cas de debug
    if debug:
        print("--- Start Fonction simple_split")
        print("IN - Segments : ", segments)
        print("IN - idx init : ", idx_init)
        print("IN - Scores : ", scores)
        print("IN - i : ", i)

    # Récupération de la liste des bornes des segments de la chaine
    sep = [segments[idx_init][0]] + list(
        segments[k][1] for k in range(idx_init, len(segments))
    )

    if i not in sep:
        # i n'est pas une borne
        seg_idx = idx_init

        # Récupération de l'index du segment dans la liste de segments
        while not (segments[seg_idx][0] < i < segments[seg_idx][1]):
            seg_idx += 1

        # Segment [a, b]
        a = segments[seg_idx][0]
        b = segments[seg_idx][1]

        # Sauvegarde des scores associés à [a, b]
        scores_to_duplicate = scores[seg_idx]

        # Suppression puis découpe et insertion des scores
        del segments[seg_idx]
        segments = segments[:seg_idx] + [[a, i]] + [[i, b]] + segments[seg_idx:]
        scores.insert(seg_idx, scores_to_duplicate)

    # Affichages en cas de debug
    if debug:
        print("OUT - Segments : ", segments)
        print("OUT - Scores : ", scores)
        print("--- End Fonction simple_split")

    return [segments, scores]


def simple_insertion(segments, idx_init, scores, i, debug):
    # Insère un segment à l'endroit [i, i] où a lieu l'insertion de texte.
    # les scores associés sont vides.
    #
    # Exemple :
    # Séquence de la chaine :
    #   [0, 4]  [4, 15]  [15, 16] et i = 15
    #    u1:1    u1:0.5   u1:0.75
    #    u2:0    u2:0.5   u2:0.25
    # renvoie :
    #   [0, 4]  [4, 15]  [15, 15]  [15, 16]]
    #    u1:1   u1:0.5              u1:0.75
    #    u2:0   u2:0.5              u2:0.25
    #
    # Entrées : la liste des segments, l'indice du segment de départ
    #           et les scores associés.
    #           i, un entier qui correspond à l'endroit où couper.
    #          debug : génère des affichages en cas de débugage.
    # Sortie : la liste des segments découpés et les scores associés.

    # Affichages en cas de debug
    if debug:
        print("--- Start Fonction simple_insertion")
        print("IN - Segments : ", segments)
        print("IN - idx init : ", idx_init)
        print("IN - Scores : ", scores)
        print("IN - i : ", i)

    # Si l'insertion a lieu en toute fin de chaine
    if idx_init == len(segments):
        segments.append([i, i])
        scores.append([])
    else:
        first_word_idx = segments[idx_init][0]
        if i == first_word_idx:
            # Si l'insertion a lieu en tout début de chaine
            segments = (
                segments[:idx_init]
                + [[first_word_idx, first_word_idx]]
                + segments[idx_init:]
            )
            scores = scores[:idx_init] + [[]] + scores[idx_init:]
        else:
            # Recherche de l'index de la liste des segments où insérer [i, i]
            # On ne regarde pas avant idx_init car les index correspondent
            # à la nouvelle chaine
            seg_idx = idx_init
            while i != segments[seg_idx][1]:
                seg_idx += 1
            seg_idx += 1

            # Insertion
            segments = segments[:seg_idx] + [[i, i]] + segments[seg_idx:]
            scores = scores[:seg_idx] + [[]] + scores[seg_idx:]

    # Affichages en cas de debug
    if debug:
        print("OUT - Segments : ", segments)
        print("OUT - Scores : ", scores)
        print("--- End Fonction simple_insertion")

    return [segments, scores]


def equal(segments, sel_seg_idx, scores, j1, j2, user, debug):
    # Met à jour les scores et les segments pour une égalité.
    #   - Les nouveaux scores sont identiques aux anciens scores.
    #   - Les nouveaux segments sont décalés de sorte que le premier commence
    #     à j1 et le dernier termine à j2.
    # A ce stade, j1 et j2 sont des bornes des intervalles.
    #
    # Exemple :
    #               nouvelle chaine             ancienne chaine
    #               ________________ ________________________________________
    #   segments  | [0, 23] [23, 25] [4, 8] [8, 15] [15, 16] [16, 16] [16, 20]
    #   scores    |  u1:1   u1:0.9   u1:0.9  u1:1    u1:0              u1:0.5
    #             |  u2:0   u2:0.1   u2:0.1  u2:0    u2:1              u2:0.5
    #
    #                   sel_seg_idx = [2, 3]
    #                   j1 = 25 et j2 = 36 (nécessairement)
    #
    #    renvoie :            nouvelle chaine              ancienne chaine
    #               __________________________________ _________________________
    #   segments  | [0, 23] [23, 25] [25, 29] [29, 36] [15, 16] [16, 16] [16, 20]
    #   scores    |  u1:1    u1:0.9   u1:0.9    u1:1     u1:0             u1:0.5
    #             |  u2:0    u2:0.1   u2:0.1    u2:0     u2:1             u2:0.5
    #
    # Entrées : liste des segments, les index à modifier, les scores associés.
    #           j1 et j2 sont les index de mots correspondant à la nouvelle chaine.
    #           user est l'utilisateur à qui le tag est associé.
    #           debug : génère des affichages en cas de débugage.
    # Sorties : les segments et les scores actualisés (le score est identique ici).
    #           le nombre de segments effacés, 0 ici.

    # Affichages en cas de debug
    if debug:
        print("--- Start Fonction equal")
        print("IN - Segments : ", segments)
        print("IN - Scores : ", scores)
        print("IN - Selected segments idx : ", sel_seg_idx)

    # Décalage que l'on va utiliser pour chaque borne de chaque segment
    shift = j1 - segments[sel_seg_idx[0]][0]

    # Actualisation de chaque segment
    for seg_idx in sel_seg_idx:
        segments[seg_idx][0] += shift
        segments[seg_idx][1] += shift

    # Affichages en cas de debug
    if debug:
        print("OUT - Segments : ", segments)
        print("OUT - Scores : ", scores)
        print("--- End Fonction equal")

    return [segments, scores, 0]


def insert(segments, sel_seg_idx, scores, j1, j2, user, debug):
    # Met à jour les scores et les segments pour une insertion.
    #   - Les nouveaux scores sont [user, 1] pour l'unique segment concerné.
    #   - Le nouveau segment est [j1, j2].
    #
    # Exemple :
    #                            nouvelle chaine                ancienne chaine
    #               ___________________________________________ _________________
    #   segments  | [0, 23] [23, 25] [25, 29] [29, 36] [36, 37] [16, 16] [16, 20]
    #   scores    |  u1:1   u1:0.9    u1:0.9     u1:1    u1:0             u1:0.5
    #             |  u2:0   u2:0.1    u2:0.1     u2:0    u2:1             u2:0.5
    #
    #                   sel_seg_idx = [5], user = u2
    #
    #   renvoie :                     nouvelle chaine                 ancienne chaine
    #               ____________________________________________________ ________
    #   segments  | [0, 23] [23, 25] [25, 29] [29, 36] [36, 37] [37, 52] [16, 20]
    #   scores    |  u1:1   u1:0.9    u1:0.9     u1:1    u1:0     u1:0    u1:0.5
    #             |  u2:0   u2:0.1    u2:0.1     u2:0    u2:1     u2:1    u2:0.5
    #
    # Entrées : liste des segments, les index à modifier, les scores associés.
    #           j1 et j2 sont les index de mots correspondant à la nouvelle chaine.
    #           user est l'utilisateur à qui le tag est associé.
    #           debug : génère des affichages en cas de débugage.
    # Sorties : les segments et les scores actualisés.
    #           le nombre de segments effacés, 0 ici.

    # Affichages en cas de debug
    if debug:
        print("--- Start Fonction insert")
        print("IN - Segments : ", segments)
        print("IN - Scores : ", scores)
        print("IN - Selected segments idx : ", sel_seg_idx)

    seg_idx = sel_seg_idx[0]
    segments[seg_idx] = [j1, j2]
    scores[seg_idx] = [[user, 1.0]]

    # Affichages en cas de debug
    if debug:
        print("OUT - Segments : ", segments)
        print("OUT - Scores : ", scores)
        print("--- End Fonction insert")

    return [segments, scores, 0]


def delete(segments, sel_seg_idx, scores, j1, j2, user, debug):
    # Supprime certains segments et scores (peut concerner plusieurs segments contigus).
    #
    # Exemple :
    #               nouvelle chaine             ancienne chaine
    #               ________________ ________________________________________
    #   segments  | [0, 23] [23, 25] [4, 8] [8, 15] [15, 16] [16, 16] [16, 20]
    #   scores    |  u1:1   u1:0.9   u1:0.9  u1:1    u1:0              u1:0.5
    #             |  u2:0   u2:0.1   u2:0.1  u2:0    u2:1              u2:0.5
    #
    #                   sel_seg_idx = [2, 3]
    #
    #    renvoie :  nouvelle chaine       ancienne chaine
    #               ________________ _________________________
    #   segments  | [0, 23] [23, 25] [15, 16] [16, 16] [16, 20]
    #   scores    |  u1:1    u1:0.9    u1:0             u1:0.5
    #             |  u2:0    u2:0.1    u2:1             u2:0.5
    #
    # Entrées : liste des segments, les index à modifier, les scores associés.
    #           j1 et j2 sont les index de mots correspondant à la nouvelle chaine.
    #           user est l'utilisateur à qui le tag est associé.
    #           debug : génère des affichages en cas de débugage.
    # Sorties : les segments et les scores actualisés.
    #           shift, le nombre de segments effacés.

    # Affichages en cas de debug
    if debug:
        print("--- Start Fonction delete")
        print("IN - Segments : ", segments)
        print("IN - Scores : ", scores)
        print("IN - Selected segments idx : ", sel_seg_idx)

    # Actualisation de chaque segment
    # On inverse l'ordre des segments sélectionnés pour éviter les erreurs
    # d'index en cas de suppressions multiples
    shift = 0
    for seg_idx in reversed(sel_seg_idx):
        del segments[seg_idx]
        del scores[seg_idx]
        shift += 1

    # Affichages en cas de debug
    if debug:
        print("OUT - Segments : ", segments)
        print("OUT - Scores : ", scores)
        print("OUT - Shift : ", shift)
        print("--- End Fonction delete")

    return [segments, scores, shift]


def replace(segments, sel_seg_idx, scores, j1, j2, dist, user, debug):
    # Recalcule les scores selon la méthode suivante.
    #   1. On calcule la moyenne de contribution par mot de chaque utilisateur
    #       sur l'ensemble des segments sélectionnés.
    #       Dans l'exemple ci dessous, pour u1, (4*0.9+7*1)/11 = 0,964
    #                                  pour u2, (4*0.1+7*0)/11 = 0,036
    #   2. On calcule les noubeaux scores :
    #       - pour l'utilisateur user : s <- s + dist*(1-s) = s*(1-dist) + dist
    #       - pour les autres : s <- s*(1-dist)
    #       Dans l'exemple ci-dessous, pour u1, 0,964*0,25 = 0,241
    #                                  pour u2, 0,036*0,25+0,75 = 0,759
    #   3. On insère un nouveau segment avec es scores précédents.
    #
    # Exemple :
    #               nouvelle chaine             ancienne chaine
    #               ________________ ________________________________________
    #   segments  | [0, 23] [23, 25] [4, 8] [8, 15] [15, 16] [16, 16] [16, 20]
    #   scores    |  u1:1   u1:0.9   u1:0.9  u1:1    u1:0              u1:0.5
    #             |  u2:0   u2:0.1   u2:0.1  u2:0    u2:1              u2:0.5
    #
    #                   sel_seg_idx = [2, 3]
    #                   dist = 0.75
    #                   user = u2
    #
    #    renvoie :        nouvelle chaine            ancienne chaine
    #               _________________________   _________________________
    #   segments  | [0, 23] [23, 25] [25, 52]   [15, 16] [16, 16] [16, 20]
    #   scores    |  u1:1    u1:0.9   u1:0.241    u1:0             u1:0.5
    #             |  u2:0    u2:0.1   u2:0.759    u2:1             u2:0.5
    #
    # Entrées : liste des segments, les index à modifier, les scores associés.
    #           j1 et j2 sont les index de mots correspondant à la nouvelle chaine.
    #           dist est la mesure de la contribution de user.
    #           user est l'utilisateur à qui le tag est associé.
    #           debug : génère des affichages en cas de débugage.
    # Sorties : les segments et les scores actualisés.
    #           shift, le nombre de segments effacés.

    # Affichages en cas de debug
    if debug:
        print("--- Start Fonction replace")
        print("IN - Segments : ", segments)
        print("IN - Scores : ", scores)
        print("IN - Selected segments idx : ", sel_seg_idx)
        print("IN - dist:", dist)

    # Nombre de mots affectés par le replace
    idx_min = segments[sel_seg_idx[0]][0]
    idx_max = segments[sel_seg_idx[-1]][1]
    total_word_nbr = idx_max - idx_min

    # Liste des utilisateurs et des contributions (somme cumulée sur chaque mot
    # de chaque segment)
    users_list = []
    contrib_sum_list = []
    for seg_idx in sel_seg_idx:
        word_nbr = segments[seg_idx][1] - segments[seg_idx][0]
        for u, s in scores[seg_idx]:
            if u in users_list:
                user_idx = users_list.index(u)
                contrib_sum_list[user_idx] += word_nbr * s
            else:
                users_list.append(u)
                contrib_sum_list.append(word_nbr * s)
    # Normalisation
    contrib_list = [s / total_word_nbr for s in contrib_sum_list]

    # Ajout de l'utilisateur qui a réalisé le replace à la liste des users
    if user not in users_list:
        users_list.append(user)
        contrib_list.append(0)

    # Calcul des nouveaux scores s
    user_idx = users_list.index(user)
    contrib_list = [s * (1 - dist) for s in contrib_list]
    contrib_list[user_idx] += dist

    # Mise à jour des segments et des scores
    shift = 0
    # On parcourt la liste dans l'ordre inverse sans prendre le dernier élément
    for seg_idx in sel_seg_idx[-1:0:-1]:
        # print(f"effacement : {seg_idx}, {segments[seg_idx]}")
        del segments[seg_idx]
        del scores[seg_idx]
        shift += 1
    seg_idx = sel_seg_idx[0]
    segments[seg_idx] = [j1, j2]
    scores[seg_idx] = [[ui, si] for ui, si in zip(users_list, contrib_list)]

    # Affichages en cas de debug
    if debug:
        print("OUT - Segments : ", segments)
        print("OUT - Scores : ", scores)
        print("OUT - Shift : ", shift)
        print("--- End Fonction replace")

    return [segments, scores, shift]


def one_step_contribution(chain, text_user, debug=False):
    if debug:
        print("--- Start Fonction one_step_contribution")
        print("IN - Chaine : ", chain)

    segments, scores, first_text = chain

    second_text = text_user[0]

    user = text_user[1]
    # on ajoute l'utilisateur à la liste des contributeurs (avec un score nul sur
    # le 1er segment). Si sa contribution est vide (relecture ou effacements),
    # on garde ainsi une trace de son passage
    users_list = [
        str(scores[i][j][0]) for i in range(len(scores)) for j in range(len(scores[i]))
    ]
    users = list(set(users_list))
    if user not in users:
        scores[0].append([user, 0.0])

    s = difflib.SequenceMatcher(None, first_text, second_text)

    idx_init = 0
    # Pour chaque détection par difflib (tag unique)
    for tag, i1, i2, j1, j2 in s.get_opcodes():
        # Découpe ou insertion de segments
        if i1 != i2:
            # Appel à une fonction dédiée à la découpe
            segments, scores = simple_split(segments, idx_init, scores, i2, debug)
        else:
            # Appel à une fonction dédiée à l'insertion
            segments, scores = simple_insertion(segments, idx_init, scores, i2, debug)

        # Récupère les index des segments de la chaine découpée affectés par le tag
        sel_seg_idx = select_segments_idx(segments, idx_init, i1, i2, debug)

        # Effectue le calcul selon le tag
        if tag == "equal":
            segments, scores, shift = equal(
                segments, sel_seg_idx, scores, j1, j2, user, debug
            )
        if tag == "insert":
            segments, scores, shift = insert(
                segments, sel_seg_idx, scores, j1, j2, user, debug
            )
        if tag == "delete":
            segments, scores, shift = delete(
                segments, sel_seg_idx, scores, j1, j2, user, debug
            )
        if tag == "replace":
            # On calcule la distance entre les segments de départ et d'arrivée après
            # avoir recomposé les textes comme des listes de lettres et non de mots
            # print("first text", type(first_text),first_text,"\n second text",type(second_text),second_text)
            # print("i1",i1,"i2",i2,"j1",j1,"j2",j2)
            a = " ".join(second_text[i1:i2])
            b = " ".join(second_text[j1:j2])
            # a = first_text
            # b = second_text

            # typer.secho(f"replaces : {type(a)} : {a} , \n  {type(b)}: {b} , ", fg=typer.colors.RED)
            # On enlève les espaces pour calculer la similarité ?
            # -> cela permet d'éviter que "a a a" et "b b b" aient 40% de similarité
            # s2 = difflib.SequenceMatcher(lambda x: x in " \t", a, b)
            s2 = difflib.SequenceMatcher(None, a, b)
            # dist = mesure de la contribution de l'utilisateur aux segments modifiés
            # 0 : contribution nulle
            # 1 : contribution totale
            dist = 1 - s2.ratio()
            segments, scores, shift = replace(
                segments, sel_seg_idx, scores, j1, j2, dist, user, debug
            )

        idx_init = sel_seg_idx[-1] + 1 - shift

    chain = [segments, scores, second_text]

    # Affichages en cas de debug
    if debug:
        print("OUT - Chaine : ", chain)
        print("--- End Fonction one_step_contribution\n\n")

    return chain


# def contribution(list_of_text_user, debug):

#     list_of_text_user = [(clean_and_tokenize(text), user) for (text, user) in list_of_text_user]

#     # Initialisation
#     chain = initialize(list_of_text_user, debug)

#     # Calcul des diffs successifs
#     for text_user in list_of_text_user[1:]:
#         chain = one_step_contribution(chain, text_user, debug)

#     return chain

"""text_user = []
text_user.append(("la fonction sinus est 2pi-périodique", "user1"))
text_user.append(("la fonction sinus est impaire et 2pi-périodique", "user2"))
text_user.append(("la fonction sinus est impaire", "user2"))
text_user.append(("la fonction tangente est impaire et 2pi-périodique", "user1"))
text_user.append(("les fonctions sinus et tangente sont impaires et 2pi-périodiques", "user2"))

# Analyse de contribution
result = contribution(text_user, debug=True)"""
