import streamlit as st
from utils.utils import *
import pandas as pd

def get_list(attributo):
    query=f"SELECT DISTINCT {attributo} FROM Corsi"
    result=execute_query(st.session_state["connection"],query)
    result_list=[]
    for row in result.mappings():
        result_list.append(row[attributo])
    return result_list
def check_info(corso_dict):
    Codici=get_list("CodC")
    for value in corso_dict.values():
        if value=='':
            return False
    if corso_dict["Livello"] < 1 or corso_dict["Livello"] > 4:
        st.error("Immetti un livello valido (1-4)")
        return False
    if not corso_dict["CodC"].startswith("CT"):
        st.error("Codice corso non valido")
        return False
    if corso_dict["CodC"] in Codici:
        st.error("Codice Corso già presente")
    return True
def insert(corso_dict):
    if check_info(corso_dict):
        attributi=", ".join(corso_dict.keys())
        valori=tuple(corso_dict.values())
        query=f"INSERT INTO Corsi ({attributi}) VALUES {valori};"
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
    with st.form("Nuovo Corso"):
        st.header(":blue[Aggiungi Corso:]")

        Tipi=get_list("Tipo")
        code=st.text_input("Codice corso",placeholder="CT***")
        nome=st.text_input("Nome corso",placeholder="Inserisci il nome del corso")
        tipo=st.selectbox("Tipologia",Tipi)
        livello=st.slider("Livello",1,4)

        insert_dict= {"CodC":code, "Nome":nome,"Tipo":tipo,"Livello":livello}
        
        submitted =st.form_submit_button("Submit",type='primary')
    
    if submitted:
        if insert(insert_dict):
            st.success("Hai inserito questo corso: ",icon='✅')
            st.write(insert_dict)
        else:
            st.error("Impossibile aggiungere il corso.",icon='⚠️')
 

if __name__ == "__main__":
    st.title("Nuovo Corso")
    st.markdown("Pagina per inserire un nuovo corso nel sistema. Scegliere un codice non ancora utilizzato.r")
    if check_connection():
        create_form()