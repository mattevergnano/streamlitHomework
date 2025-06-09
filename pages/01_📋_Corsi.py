import streamlit as st
from utils.utils import *
import pandas as pd

if __name__ == "__main__":
    st.title("📋 Corsi")
    st.markdown("Pagina per visualizzare informazioni dei corsi.\n\nSelezionare la tipologia e il livello. Nella sezione programma ci sono le lezioni programmate per i corsi inclusi nella selezione.")
    if check_connection():
        col_select1,col_select2 = st.columns(2)
        with col_select1:
            livello=st.slider("Seleziona il livello",1,4,(1,4))
        categoria=execute_query(st.session_state["connection"],f"SELECT DISTINCT Tipo FROM Corsi")
        with col_select2:
            corsi_categoria = col_select2.multiselect("Categoria:",categoria)
        if corsi_categoria:
            categoria_query = "(" + ",".join([f"'{c}'" for c in corsi_categoria]) + ")"
        else:
            categoria_query = "('')"
        corsi_info=execute_query(st.session_state["connection"],f"SELECT COUNT(DISTINCT CodC) AS TotCorsi,COUNT(DISTINCT Tipo) AS TotTipo FROM Corsi WHERE Livello>={livello[0]} AND Livello<={livello[1]} AND Tipo IN {categoria_query};")
        corsi_info_dict = [dict(zip(corsi_info.keys(), result)) for result in corsi_info]
        col1,col2 = st.columns(2)
        col1.metric('Numero Corsi',f"{corsi_info_dict[0]['TotCorsi']}")
        col2.metric('Numero Categorie',f"{corsi_info_dict[0]['TotTipo']}")
        with st.expander("Programma",False):
            programma = execute_query(st.session_state["connection"],f"SELECT Tipo,Giorno, OraInizio,Durata,Sala, CONCAT(Istruttore.Nome, ' ' ,Istruttore.Cognome) AS NomeCompleto ,Email FROM Programma,Corsi,Istruttore WHERE Programma.CodC=Corsi.CodC AND Programma.CodFisc=Istruttore.CodFisc AND Livello>={livello[0]} AND Livello<={livello[1]} AND Tipo IN {categoria_query} ORDER BY Giorno ASC;")
            df_programma=pd.DataFrame(programma)
            if not df_programma.empty:
                st.dataframe(df_programma,use_container_width=True)
            else:
                    st.error("Nessun risultato")