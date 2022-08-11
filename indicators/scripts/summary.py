from pathlib import Path
import json
# import csv
import pandas as pd
import skfuzzy as fuzz
import numpy as np
# from skfuzzy import control as ctrl
import gzip
import warnings
import typer

warnings.filterwarnings("ignore")


def fuzzy_classify(DataFrame, colnames: list):
    """Classify a dataframe with fuzzy rules"""
    for colname in colnames:
        nb_report, _ = np.shape(DataFrame)
        if nb_report > 1:
            data = DataFrame[colname]
            min = np.round(data.min(), 2)
            max = np.round(data.max(), 2)
            mid = np.median(np.arange(min, max, 0.1))
            universe = np.arange(np.floor(min), np.ceil(max) + 0.2, 0.1)

            trimf_low = np.round(fuzz.trimf(universe, [min, min, mid]), 2)
            trimf_mid = np.round(fuzz.trimf(universe, [min, mid, max + 0.1]), 2)
            trimf_hi = np.round(fuzz.trimf(universe, [mid, max + 0.1, max + 0.1]), 2)
            DataFrame[colname + "_low"] = np.round(
                fuzz.interp_membership(universe, trimf_low, data), 2
            )
            DataFrame[colname + "_mid"] = np.round(
                fuzz.interp_membership(universe, trimf_mid, data), 2
            )
            DataFrame[colname + "_high"] = np.round(
                fuzz.interp_membership(universe, trimf_hi, data), 2
            )

            DataFrame[colname + "_membership"] = DataFrame.loc[
                :, [colname + "_low", colname + "_mid", colname + "_high"]
            ].idxmax(axis=1)
            DataFrame[colname + "_degree"] = DataFrame.loc[
                :, [colname + "_low", colname + "_mid", colname + "_high"]
            ].max(axis=1)
    return DataFrame


def summary(file: Path):
    # Unzip de file using gzip
    # result = {'id_mission':str, 'id_report':str, 'id_labdoc':str, 'id_trace':str, 'n_users':int, 'eqc_index':int, 'coec_index':int,'nb_tokens':int,'nb_segments':int}
    with gzip.open(file) as f:
        data = json.loads(f.read())

    results = []

    id_missions = data.keys()
    # for each mission
    for id_mission in id_missions:
        id_reports = data[id_mission].keys()
        # for each report
        for id_report in id_reports:
            id_labdocs = data[id_mission][id_report].keys()
            # for each labdoc
            for id_labdoc in id_labdocs:
                # for each trace
                id_traces = list(data[id_mission][id_report][id_labdoc].keys())
                row = data[id_mission][id_report][id_labdoc][id_traces[-1]]
                # check if n_user >1
                if row[0] > 1:
                    # check if the labdc is not empty (when indicators == -1)
                    if row[2] > -1 or row[3] > -1:
                        result = [
                            id_mission,
                            id_report,
                            id_labdoc,
                            id_traces[-1],
                            row[0],
                            row[1],
                            row[5]["NB_TOKS"],
                            row[5]["NB_SEGS"],
                            row[2],
                            row[3],
                        ]
                        results.append(result)

    results = pd.DataFrame(
        results,
        columns=[
            "id_mission",
            "id_report",
            "id_labdoc",
            "id_trace",
            "n_users",
            "teacher",
            "n_tokens",
            "n_segments",
            "eqc",
            "coec",
        ],
    )
    results.to_csv("tmp/summary.csv")

    results_fuzzified = pd.DataFrame()
    for id_mission in results["id_mission"].unique():
        # Get lines of the mission
        DataFrame = results.loc[
            (results["id_mission"] == id_mission) & (results["teacher"] == 0), :
        ]
        try:
            fuzzified = fuzzy_classify(DataFrame, ["eqc", "coec"])
            results_fuzzified = pd.concat([results_fuzzified, fuzzified], axis=0)
        except:
            typer.secho(
                f"the mission {id_mission} has can't be fuzzified", fg=typer.colors.RED
            )
            pass
    results_fuzzified.to_csv("tmp/summary_fuzzy.csv")


if __name__ == "__main__":
    typer.run(summary)


# summary('/Users/anis/test_labnbook/math_ner/indicators/tmp/collab.json.gz')
