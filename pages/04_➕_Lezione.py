import streamlit as st
from utils.utils import *
import pandas as pd
import datetime

def get_list_progr(attributo):
    query=f"SELECT DISTINCT {attributo} FROM Programma"
    result=execute_query(st.session_state["connection"],query)
    result_list=[]
    for row in result.mappings():
        result_list.append(row[attributo])
    return result_list
def get_list_istr(attributo):
    query=f"SELECT DISTINCT {attributo} FROM Istruttore"
    result=execute_query(st.session_state["connection"],query)
    result_list=[]
    for row in result.mappings():
        result_list.append(row[attributo])
    return result_list
def get_list_corsi(attributo):
    query=f"SELECT DISTINCT {attributo} FROM Corsi"
    result=execute_query(st.session_state["connection"],query)
    result_list=[]
    for row in result.mappings():
        result_list.append(row[attributo])
    return result_list

def check_info(less_dict):
    query = f"SELECT COUNT(*) AS count FROM Programma  WHERE CodC = '{less_dict["CodC"]}' AND Giorno = '{less_dict["Giorno"]}'"
    result = execute_query(st.session_state["connection"], query)
    count = list(result.mappings())[0]["count"]

    if count > 0:
        st.error("Esiste già una lezione per questo corso in questo giorno.")
        return False
    for value in less_dict.values():
        if value=='':
            return False
    return True

def insert(less_dict):
    print("insert")
    if check_info(less_dict):
        attributi=", ".join(less_dict.keys())
        valori=tuple(less_dict.values())
        query=f"INSERT INTO Programma ({attributi}) VALUES {valori};"
        try:
            execute_query(st.session_state["connection"],query)
            st.session_state["connection"].commit()
        except Exception as e:
            st.error(e)
            return False
        return True
    else:
        return False

def create_form():
    with st.form("Nuova Lezione"):
        st.header(":blue[Aggiungi Lezione:]")

        code=get_list_corsi("CodC")
        codfisc=get_list_istr("CodFisc")
        
        Giorno=st.selectbox("Giorno",["Lunedì","Martedì","Mercoledì","Giovedì","Venerdì"])
        oraInizio=st.time_input("Ora inizio",value=datetime.time(8,00))
        durata=st.slider("Durata",min_value=0,max_value=60,step=5)
        codCorso=st.selectbox("Codice Corso",code)
        codFiscale=st.selectbox("Codice Fiscale Insegnante",codfisc)
        sala_t=st.number_input("Numero Sala",min_value=1,max_value=10,step=1)
        sala=f"S{sala_t}"

        insert_dict= {"Giorno":Giorno,"CodFisc":codFiscale,"OraInizio":oraInizio.strftime("%H:%M:%S"),"Durata":durata,"Sala":sala,"CodC":codCorso}
        
        submitted =st.form_submit_button("Submit",type='primary')
    
    if submitted:
        if insert(insert_dict):
            st.success("Hai inserito questa lezione: ",icon='✅')
            st.write(insert_dict)
        else:
            st.error("Impossibile aggiungere lezione.",icon='⚠️')
 

if __name__ == "__main__":
    st.title("Nuova Lezione")
    st.markdown("Pagina per inserire una nuova lezione a calendario.\n\nSelezionare il corso dall'elenco. Inserire giorno e orario (controllando che non ci siano altre lezioni per questo corso in quel giorno), la durata (non superiore a 60 minuti) e la sala.")
    if check_connection():
        create_form()