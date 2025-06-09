import streamlit as st
from sqlalchemy import create_engine,text

"""Raccoglie le principali funzioni condivise dalle varie pagine"""
def connect_db(dialect,username,password,host,dbname):
    engine=create_engine(f'{dialect}://{username}:{password}@{host}/{dbname}')
    conn=engine.connect()
    return conn

def check_connection():
    if "connection" not in st.session_state.keys():
        st.session_state["connection"] = False
    
    if st.sidebar.button("Connetti al DataBase"):
        myconnection = connect_db(dialect="mysql+pymysql",username="student",password="user_pwd",host="localhost",dbname="palestra")
        if myconnection is not False:
            st.session_state["connection"] = myconnection
        else:
            st.session_state["connection"] = False
            st.sidebar.error("errore nella connessione al DB")

    if st.session_state["connection"]:
        st.sidebar.success("Connesso al DB")
        return True
    
def execute_query(conn,query):
    return conn.execute(text(query))
