
import mysql.connector as mariadb
import json
import gzip
# from pathlib import Path
import typer
# import tqdm


def extract_text_init(user: str, password: str, host: str, database: str):
    typer.secho(
        "-- Get text labdocs and possible initial texts (teacher)",
        fg=typer.colors.GREEN,
    )
    query = """
    SELECT t1.id_labdoc, t1.id_report, t1.id_ld_origin, t1.type_labdoc, t2.name, t2.labdoc_data
    FROM labdoc t1
    LEFT JOIN labdoc t2 ON t2.id_labdoc = t1.id_ld_origin
    WHERE t1.type_labdoc = 'text' AND t1.id_report IS NOT NULL
    ORDER BY t1.id_labdoc  ASC
    """
    # AND t2.labdoc_data IS NOT NULL AND t2.labdoc_data != '' AND t2.labdoc_data != '<p>.</p>
    try:
        conn = mariadb.connect(
            user=user, password=password, host=host, database=database
        )
    except mariadb.Error as e:
        typer.secho(f"Error connecting to MariaDB Platform: {e}", fg=typer.colors.RED)
    cur = conn.cursor()
    cur.execute(query)
    data = {}
    for row in cur:
        data[row[0]] = row[5]
    cur.close()
    conn.close()
    with gzip.open("tmp/labdocs_texts_init.json.gz", "wt", encoding="utf-8") as zipfile:
        json.dump(data, zipfile, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    typer.run(extract_text_init)
