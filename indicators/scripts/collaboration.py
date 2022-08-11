#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@authors: Anne, Karim, Guillaume, Sébastien
"""

import json
import gzip
import os
import csv
import typer 
import numpy as np
import tqdm as tqdm 



def compute_coec_index(collab_matrix_segments,segments,users):
    # Check if the contribution matrix per segments is not  empty
    if not any(collab_matrix_segments) :
        return -1
    if len(collab_matrix_segments) == 1 : 
        return 0

    nb_users = len(users)
    if nb_users == 1 :
        return 0

    else : 
        if 'ens' in users : 
            collab_teacher_segments = collab_matrix_segments[-1] # last line is the teacher's contribution
            ratio = 1 - np.mean(collab_teacher_segments)
            nb_users -= 1
            if nb_users == 1:
                return  0         
        else :
            ratio = 1
            if nb_users == 1:
                return  0 

        eqc_segments = []
        weights = []
        for i,seg in enumerate(segments):
                #TODO : continuer
            weights.append(segments[i][1] - segments[i][0]+1)
            eqc_segments.append((np.round(1 - np.sqrt(((nb_users / (nb_users- 1)) * sum((np.array(collab_matrix_segments)[:,i]- (1/nb_users))**2))),2)))
        coec_index = ratio*(np.round(np.average(np.array(eqc_segments), weights=np.array(weights)),2))

        return coec_index


# ----------------------------------------------------------------------------------------------------------------------

def compute_eqc_index(collab_matrix,users,segments = None): 
    # Check if the contribution matrix is empty 
    if not any(collab_matrix) :
        return -1

    nb_users = len(users)
    if nb_users == 1 :
        return 0
    else : 
        if 'ens' in users : 
            collab_teacher = collab_matrix[-1] # last line is the teacher's contribution
            # collab_matrix = collab_matrix[:-1] # remove the teacher's contribution
            ratio = 1 - np.mean(collab_teacher)
            nb_users -= 1
            if nb_users == 1:
                return  0       
        else :
            ratio = 1
            if nb_users == 1:
                return  0
     
        collab_users = np.round(np.mean(collab_matrix,axis = 1),2)
        eqc_index = ratio *(np.round(1 - np.sqrt(((nb_users / (nb_users- 1)) * sum((collab_users - (1/nb_users))**2))),2))

    return eqc_index

# ----------------------------------------------------------------------------------------------------------------------

def compute_collab_matrix_segments(collab_matrix,segments):
    """
    Compute the contribution matrix of each segment for each user (including the teacher)
    """
    collab_matrix_segments=[]
    for i, user_contrib in enumerate(collab_matrix): # on boucle sur les lignes
        user_contrib_seg = []
        nb_tokens_seg = [seg[1] - seg[0] + 1 for seg in segments]
        for j, seg in enumerate(segments):
            #__________________________
            if nb_tokens_seg[j] == 0:
                user_contrib_seg.append(1)
            else:
                score = np.round(sum(user_contrib[seg[0]:seg[1]+1]) / nb_tokens_seg[j],2)
                user_contrib_seg.append(score)
            #__________________________

            # score = np.round(sum(user_contrib[seg[0]:seg[1]+1]) / nb_tokens_seg[j],2)
            # user_contrib_seg.append(score)
        collab_matrix_segments.append(user_contrib_seg)
    return collab_matrix_segments

# ----------------------------------------------------------------------------------------------------------------------

def compute_indicators(collab_matrix,users,meta,id_mission,id_report,id_labdoc,id_trace,debug=False) :
    segments = meta['SEGS']
    nb_segments = meta['NB_SEGS']
    nb_tokens = meta['NB_TOKS']
    collab_matrix_segments = compute_collab_matrix_segments(collab_matrix,segments)
    if debug == True :   
        if np.mean(np.sum(collab_matrix_segments,axis = 0)) != 1:
            typer.secho(f"The lines sum of contribution matrix of : (id_mission,id_report,id_labdoc,id_trace) = ({id_mission} {id_report} {id_labdoc} {id_trace}) differ from 1",fg = typer.colors.RED)
            print(f"contribution matrix: {collab_matrix_segments} users : {users}" )
            if len(users) in (1,2) :
                typer.secho(f"Only the teacher or only 1 user except the teacher is in the text sequence, considered as not collaboration.",fg = typer.colors.RED)
    
    teacher = 0
    if 'ens' in users :
        teacher = 1

    nb_users = len(users)
    eqc_index = compute_eqc_index(collab_matrix,users)
    coec_index = compute_coec_index(collab_matrix_segments,segments,users)
    return nb_users,teacher, eqc_index, coec_index, collab_matrix_segments

# ----------------------------------------------------------------------------------------------------------------------

def json2csv():
    with open('tmp/collab.csv', 'w', newline='') as outcsv:
        writer = csv.writer(outcsv)
        writer.writerow(["id_mission", "id_report", "id_labdoc", "id_trace", "n_users","teacher" ,"eqc_index","coec_index","collab_matrix_segments","meta"])

        with gzip.open('tmp/collab.json.gz', 'rt', encoding='utf-8') as zipfile:
            if zipfile:
                data = json.load(zipfile)
                for id_mission in data:
                    for id_report in data[id_mission]:
                        for id_labdoc in data[id_mission][id_report]:
                            for id_trace in data[id_mission][id_report][id_labdoc]:
                                n_users, teacher ,eqc_index, coec_index, collab_matrix_segments, meta = data[id_mission][id_report][id_labdoc][id_trace]
                                writer.writerow([id_mission, id_report, id_labdoc, id_trace, n_users, teacher ,eqc_index, coec_index, collab_matrix_segments,meta])

# ----------------------------------------------------------------------------------------------------------------------
#TODO ; rajouter un variable bool qui dit si l'ens est présente ou pas dans users
def collaboration(debug = False) :
    typer.secho(f"-- Execution of the collaboration indicator calculation algorithm",fg = typer.colors.GREEN)
    id_missions = [rep[:-8] for rep in os.listdir('tmp/missions_contribs/') if not rep.startswith('.')]
    data_out = {}
    #Loop on missions
    # pbar = tqdm.tqdm(total=len(id_missions), ascii=' >=',colour='green',desc='Missions')
    for id_mission in  id_missions:
    # for id_mission in id_missions:
        path = 'tmp/missions_contribs/' + id_mission + ".json.gz"
        with gzip.open(path, 'rt', encoding='utf-8') as zipfile:
            if zipfile:
                data_in = json.load(zipfile)
                data_out[id_mission] = {}
                #Loop on reports
                pbar = tqdm.tqdm(total=len(data_in),ascii=' >=',colour='green',desc=f"Mission {id_mission}")

                for id_report in data_in:
                    data_out[id_mission][id_report] = {}
                    #Loop on labdocs
                    for id_labdoc in data_in[id_report]:
                        data_out[id_mission][id_report][id_labdoc] = {}
                        # print(f"{id_mission} {id_report} {id_labdoc}")
                        #data_out[id_report][id_labdoc].append([users, matrix, id_trace, meta])

                        for elt in data_in[id_report][id_labdoc]:
                            # users, matrix, segments, id_trace, _ , meta = elt
                            users, collab_matrix, id_trace, meta = elt
                            #typer.secho(f"--- Calcul de collaboration : traitement du labdoc {id_labdoc} ---", fg=typer.colors.RED)
                            n_users,teacher,eqc_index, coec_index, collab_matrix_segments  = compute_indicators(collab_matrix, users, meta,id_mission,id_report,id_labdoc,id_trace,debug)
                            # n_users, eqc_index, coec_index, segments ,collab_matrix_segments  = compute_collab_index(matrix, users, segments,id_mission,id_report,id_labdoc,id_trace,debug)
                            # La contribution d'un enseignant seul n'est pas stocké
                            if (n_users, eqc_index )!= (0, 0):
                                data_out[id_mission][id_report][id_labdoc][id_trace] = [n_users,teacher ,eqc_index, coec_index ,collab_matrix_segments,meta]
                        # Les contributions vides sont omises

                        if not data_out[id_mission][id_report][id_labdoc]:
                            del data_out[id_mission][id_report][id_labdoc]
                    pbar.update(1)

                    if not data_out[id_mission][id_report]:
                        del data_out[id_mission][id_report]
                if not data_out[id_mission]:
                    del data_out[id_mission]

    with gzip.open(f"tmp/collab.json.gz", 'wt', encoding='utf-8') as zipfile:
        json.dump(data_out, zipfile, ensure_ascii=False,indent=1)

    #json2csv()

# ----------------------------------------------------------------------------------------------------------------------







if __name__ == "__main__":
    typer.run(collaboration)

