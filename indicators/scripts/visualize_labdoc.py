import sys,os
import spacy
import typer 
sys.path.append("/Users/anis/test_labnbook/math_ner/indicators/model/fr_LabnbookNer-0.0.0")

from components import *
typer.secho(sys.path,fg = typer.colors.RED)

nlp = spacy.load("/Users/anis/test_labnbook/math_ner/indicators/model/fr_LabnbookNer-0.0.0")

sys.path.append((os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
+ '/tmp'))


# import json
# import gzip
# from spacy import displacy
# import streamlit as st

# st.set_page_config(layout="wide")
# import streamlit.components.v1 as components
# import pandas as pd
# import warnings

# warnings.filterwarnings("ignore")
# from IPython.core.display import display, HTML
# import numpy as np
# import seaborn as sns
# import matplotlib.pyplot as plt





# def get_labdoc_text(id_mission: int, id_report: int, id_labdoc: int):
#     with gzip.open(
#         f"tmp/missions_texts/{id_mission}.json.gz", "rt", encoding="utf-8"
#     ) as zipfile:
#         mission = json.load(zipfile)
#     report = mission[str(id_report)]
#     labdoc = report[str(id_labdoc)]
#     return labdoc


# def get_labdoc_contribs(id_mission: int, id_report: int, id_labdoc: int):
#     with gzip.open(
#         f"tmp/missions_contribs/{id_mission}.json.gz", "rt", encoding="utf-8"
#     ) as zipfile:
#         mission = json.load(zipfile)
#     report = mission[str(id_report)]
#     labdoc = report[str(id_labdoc)]
#     return labdoc


# def get_labdoc_contribs_segment(id_mission: int, id_report: int, id_labdoc: int):
#     with gzip.open(f"tmp/collab.json.gz", "rt", encoding="utf-8") as zipfile:
#         data = json.load(zipfile)
#     mission = data[str(id_mission)]
#     report = mission[str(id_report)]
#     labdoc = report[str(id_labdoc)]
#     # pour chaque trace on sortie 'id_trace': [n_users, nb_tokens, indice_collab, coec_index, collab_matrix_segments]]
#     traces = list(labdoc.keys())
#     return labdoc, traces


# def visualize_labdoc(id_mission: int, id_report: int, id_labdoc: int):
#     nlp = spacy.load(
#         "/Users/anis/test_labnbook/math_ner/indicators/model/fr_LabnbookNer-0.0.0"
#     )

#     labdoc_texts = get_labdoc_text(id_mission, id_report, id_labdoc)

#     labdoc_contrib = get_labdoc_contribs(id_mission, id_report, id_labdoc)

#     labdoc_results, traces = get_labdoc_contribs_segment(
#         id_mission, id_report, id_labdoc
#     )

#     st.title(
#         f"id_labdoc : {id_labdoc}, id_report : {id_report}, id_mission : {id_mission}"
#     )

#     for i, trace in enumerate(traces):
#         if trace != 0:
#             doc = nlp(labdoc_texts[i][0])
#             users = labdoc_contrib[i][0]
#             n_users, eqc_index, coec_index = (
#                 labdoc_results[trace][0],
#                 labdoc_results[trace][2],
#                 labdoc_results[trace][3],
#             )

#             collab_matrix_segments = labdoc_results[trace][4]
#             segments, tokens, nb_tokens = (
#                 labdoc_results[trace][5]["SEGS"],
#                 labdoc_results[trace][5]["TOKS"],
#                 labdoc_results[trace][5]["NB_TOKS"],
#             )

#             # TODO : revoir le calcul de la matrice de contribution dans tmp/collab.json.gz
#             collab_matrix = labdoc_contrib[i][1]

#             st.subheader(
#                 f"-------------------------------------- Trace : {trace} --------------------------------------"
#             )
#             # st.subheader('Text:')
#             # components.html(display(tab2),width=1000, height=300)
#             # if trace != 0:
#             components.html(
#                 displacy.render(doc, style="ent"),
#                 width=1800,
#                 height=200,
#                 scrolling=True,
#             )
#             # st.markdown(displacy.render(doc,style="ent"))
#             st.subheader("Segments and ents:")
#             components.html(
#                 displacy.render(list(doc.sents), style="ent"),
#                 width=1000,
#                 height=800,
#                 scrolling=True,
#             )

#             st.subheader("Contribution matrix :")
#             index = list(users)
#             index.insert(0, "tokens")
#             collab_matrix.insert(0, tokens)
#             tab1 = pd.DataFrame(collab_matrix, index=index).astype(str)
#             st.table(tab1)

#             st.subheader("Contribution matrix/segments :")

#             tab2 = pd.DataFrame(
#                 collab_matrix_segments,
#                 columns=["sent:" + str(seg) for seg in segments],
#                 index=list(users),
#             ).astype(str)

#             st.table(tab2)
#             # st.text(labdoc_results[trace][4])
#             # index = list(users)
#             st.text(
#                 f"n_users: {n_users} | nb_tokens: {nb_tokens} | eqc_index: {eqc_index} | coec_index: {coec_index} | nb_sentences: {len(segments)} "
#             )
#     matrix = np.array(collab_matrix_segments)
#     if st.button("Get a summary", key="summary"):
#         if np.shape(matrix)[0] > 1:
#             st.text("Contribution matrix for sentences:")
#             # st.text(f"id_labdoc : {id_labdoc}, id_report : {id_report}, id_mission : {id_mission}, id_trace : {trace} :{collab_matrix_segments}")
#             fig = plt.figure(figsize=(10, 4))
#             sns.heatmap(
#                 matrix,
#                 cmap="RdYlGn",
#                 annot=True,
#                 fmt=".2f",
#                 cbar_kws={"orientation": "horizontal"},
#             )
#             # change the size of st.write
#             st.pyplot(fig)
#             st.text(
#                 f"n_users: {n_users} | nb_tokens: {nb_tokens} | eqc_index: {eqc_index} | coec_index: {coec_index} | nb_sentences: {len(segments)} "
#             )

#             fuzzified = pd.read_csv("tmp/summary_fuzzy.csv", index_col=0)
#             fuzzified_mission = fuzzified[fuzzified["id_mission"] == id_mission]

#             fig = plt.figure(figsize=(10, 4))
#             sns.scatterplot(
#                 data=fuzzified_mission,
#                 x="eqc",
#                 y="eqc_degree",
#                 hue="eqc_membership",
#                 marker=".",
#             )
#             # change the size of st.write
#             st.pyplot(fig)

#         fig = plt.figure(figsize=(10, 4))
#         # fig.set_size_inches(30, 10)
#         sns.scatterplot(
#             data=fuzzified_mission,
#             x="coec",
#             y="coec_degree",
#             hue="coec_membership",
#             marker=".",
#         )
#         # change the size of st.write
#         st.pyplot(fig)
#         st.text(
#             f" \
#                 eqc membership: {fuzzified_mission[fuzzified_mission['id_labdoc'] == id_labdoc]['eqc_membership']} \n \
#                 eqc degree : {fuzzified_mission[fuzzified_mission['id_labdoc'] == id_labdoc]['eqc_degree']} \n \
#                 coec membership : {fuzzified_mission[fuzzified_mission['id_labdoc'] == id_labdoc]['coec_membership']} \n \
#                 coec degree : {fuzzified_mission[fuzzified_mission['id_labdoc'] == id_labdoc]['coec_degree']}"
#         )


# try:
#     # visualize_labdoc(1038, 24870, 247575 )
#     visualize_labdoc(1694,	47242,	471651)
#     # visualize_labdoc(429, 43158, 435623)
#     # visualize_labdoc(1544, 43471, 424607)
# except SystemExit as se:
#     if se.code != 0:
#         raise
