import streamlit as st
import mysql.connector
from utilR import font_TITLE, menuProjeuHtml, menuProjeuCss
from time import sleep

st.set_page_config(page_title="Validar Email", 
                   layout="wide",
                   initial_sidebar_state="collapsed")

conexao = mysql.connector.connect(
    passwd='nineboxeucatur',
    port=3306,
    user='ninebox',
    host='nineboxeucatur.c7rugjkck183.sa-east-1.rds.amazonaws.com',
    database='projeu'
)
mycursor = conexao.cursor()

user = 'SELECT * FROM projeu_users;'
mycursor.execute(user)
usersBD = mycursor.fetchall()

st.markdown(
    """
        <style>
            [data-testid="collapsedControl"]{
                display: none
            }
        </style>
    """,
        unsafe_allow_html=True,
)

menuHtml = menuProjeuHtml("")
menuCss = menuProjeuCss()
st.write(f'<div>{menuHtml}</div>', unsafe_allow_html=True)
st.write(f'<style>{menuCss}</style>', unsafe_allow_html=True)

fonte_Projeto = '''@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Bungee+Inline&family=Koulen&family=Major+Mono+Display&family=Passion+One&family=Sansita+Swashed:wght@500&display=swap');'''
font_TITLE('VALIDAR E-MAIL', fonte_Projeto,"'Bebas Neue', sans-serif", 49, 'center')

col1, col2, col3 = st.columns(3)
with col2:
    codValidacao = st.text_input("Código de Validação", max_chars=5)
    validar = st.button("VALIDAR")

if validar:
        if codValidacao:
            usuario = [x for x in usersBD if x[14] == f'{codValidacao}']
            if len(usuario) != 0:
                update = f"UPDATE projeu_users SET status_user = 'A', codigo_user = NULL WHERE codigo_user = '{codValidacao}'"
                mycursor.execute(update)
                conexao.commit()
                st.toast("Usuário validado com sucesso!", icon='✅')
                # sleep(2)
                # st.switch_page("Home.py")
            else:
                st.info("Esse código não é válido")
        else:
            st.info("Insira o código de validação do seu e-mail")

mycursor.close()
