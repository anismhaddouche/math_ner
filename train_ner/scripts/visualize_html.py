

import streamlit as st
import streamlit.components.v1 as components
import typer 
import os
from utility import execute_query


# def visualize_html(id_labdoc):
def visualize_html(id_labdoc):
    """
    Visualize the html file in a streamlit app
    # """
    user = "root"
    password = 11950022
    host = "localhost"
    database = "Labnbook"
    query = f"SELECT  labdoc_data from labdoc where id_labdoc = {id_labdoc}; "
    html = execute_query(user, host, database, password, query)[0][0]
    st.title(f"id_labdoc : {id_labdoc}")
    components.html(html,width=800, height=1000)
    #components.html("<html><body><h1>Hello, World</h1></body></html>", width=200, height=200)



if __name__ == "__main__":
    try:
        typer.run(visualize_html)
    except SystemExit as se:
        if se.code != 0:
            raise

