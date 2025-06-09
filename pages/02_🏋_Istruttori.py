import streamlit as st
from utils.utils import *
import pandas as pd
import datetime

if __name__ == "__main__":
    st.title("Istruttori")
    st.markdown("Pagina per visualizzare gli istruttori, selezionando il cognome e il range di date in cui devono essere nati.r")
    if check_connection():
        col_select1,col_select2 = st.columns(2)
        with col_select1:
            cognomi=execute_query(st.session_state["connection"],"SELECT DISTINCT Cognome FROM Istruttore")
            cognome = col_select1.multiselect("Inserisci il cognome dell'istruttore: ",cognomi)
        with col_select2:
            data=st.date_input("Inserisci l'intervallo di date di nascita: ",(datetime.date(1970, 1, 1),datetime.date.today()),
                               datetime.date(1900,1,1),datetime.date.today(),format="YYYY-MM-DD")
        data0=data[0]
        data1=data[1]
        date = execute_query(st.session_state["connection"],"SELECT DISTINCT DataNascita FROM Istruttore")
        date_dict = [dict(zip(date.keys(), result)) for result in date]
        df_date=pd.DataFrame(date_dict)
        lista_date = df_date["DataNascita"].tolist()
        print(lista_date[1]<data[1])
        for el in lista_date:
            el.strftime('%Y-%m-%d')
        if cognome:
            cognome_sql = ", ".join(f"'{c}'" for c in cognome)
            query = f"SELECT * FROM Istruttore WHERE Cognome IN ({cognome_sql}) AND DataNascita>'{data[0].strftime('%Y-%m-%d')}' AND DataNascita<'{data[1].strftime('%Y-%m-%d')}'"
        else:
            query = f"SELECT * FROM Istruttore WHERE DataNascita>'{data[0].strftime('%Y-%m-%d')}' AND DataNascita<'{data[1].strftime('%Y-%m-%d')}'"
        istruttori_info = execute_query(st.session_state["connection"], query)
        istruttori_info_dict = [dict(zip(istruttori_info.keys(), result)) for result in istruttori_info]
        df_istruttori=pd.DataFrame(istruttori_info_dict)
        if df_istruttori.size > 0:
            for index, row in df_istruttori.iterrows():
                with st.expander(f"{row['Nome']} {row['Cognome']}",icon=":material/person:"):
                    st.write(f"**Nome**: {row['Nome']}")
                    st.write(f"**Cognome**: {row['Cognome']}")
                    st.write(f"**Data di Nascita**: {row['DataNascita']}")
                    st.write(f"**Mail**: {row['Email']}")
                    st.write(f"**Telefono**: {row['Telefono']}")
                    st.write(f"**CF**: {row['CodFisc']}")
        else:
            st.error("Nessun risultato")