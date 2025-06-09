import streamlit as st
import numpy as np
from sqlalchemy import create_engine,text
from utils.utils import *
import pandas as pd
import altair as alt

# def create_tab_area_chart(tab_area_chart):
#     lesson_info=execute_query(st.session_state["connection"],"SELECT * FROM Programma GROUP BY OraInizio,Giorno;") #numero lezioni per slot di tempo
#     lesson_info_dict = [dict(zip(lesson_info.keys(), result)) for result in lesson_info]
#     st.dataframe(lesson_info)
#     st.markdown("funziona")

if __name__ == "__main__":
    
    st.set_page_config(
        page_title="La mia App",
        layout="wide",
        initial_sidebar_state="collapsed",
        menu_items={
            'Get Help': 'https://dbdmg.polito.it/',
            'Report a bug': "https://dbdmg.polito.it/",
            'About': "# Homework di *Basi di Dati*"
        }
    )
    if "connection" not in st.session_state.keys(): #prende le chiavi del session state, controllo se la chiave connection esiste
        st.session_state["connection"] = False 
        colheader1,colheader2=st.columns([9,1])
        with colheader1:
            st.title("💾 :red[Homework 4]: Applicazione Web con Streamlit")
        with colheader2:
            st.image("images/polito_white.png")
    if check_connection():
        col1,col2=st.columns(2)
        with col1:
            st.title(":green[Panoramica]")
            st.markdown("Questo è il quarto quaderno del corso di Basi di Dati dell'anno accademico 2024-25")
            st.markdown("")

        with col2:
            st.title(":orange[Io: Matteo Vergnano]")
            st.markdown("Ho 22 anni, studio Matematica per l'Ingegneria.")
            st.markdown("Ho passioni molto variegate, che vanno dall'organizzazione di eventi allo sport.")

        # lesson_info=execute_query(st.session_state["connection"],"SELECT COUNT(*) AS TotLezioni,OraInizio FROM Programma GROUP BY OraInizio;") #numero lezioni per slot di tempo
        # lesson_info_dict = [dict(zip(lesson_info.keys(), result)) for result in lesson_info]
        col1_stat,col2_stat=st.columns(2)

        with col1_stat:
            lesson_info_hour=execute_query(st.session_state["connection"],"SELECT COUNT(*) AS TotLezioni,OraInizio FROM Programma GROUP BY OraInizio;") #numero lezioni per slot di tempo
            lesson_info_hour_dict = [dict(zip(lesson_info_hour.keys(), result)) for result in lesson_info_hour]
            st.area_chart(lesson_info_hour_dict,x="OraInizio",y="TotLezioni",color="#6C3BAA")
        with col2_stat:
            lesson_info_day=execute_query(st.session_state["connection"],"SELECT COUNT(*) AS TotLezioni,Giorno FROM Programma GROUP BY Giorno;") #numero lezioni per slot di tempo
            lesson_info_day_dict = [dict(zip(lesson_info_day.keys(), result)) for result in lesson_info_day]
            giorni_ordine = ["Lunedì", "Martedì", "Mercoledì", "Giovedì", "Venerdì"]
            df_giorni = pd.DataFrame(lesson_info_day_dict)
            df_giorni["Giorno"] = pd.Categorical(df_giorni["Giorno"], categories=giorni_ordine, ordered=True)
            bar_chart = alt.Chart(df_giorni).mark_bar().encode(
                x=alt.X("Giorno:N", sort=giorni_ordine),
                y=alt.Y("TotLezioni:Q"),
                color=alt.value("#82C8E5")
            ).properties(width="container")
            st.altair_chart(bar_chart, use_container_width=True)

