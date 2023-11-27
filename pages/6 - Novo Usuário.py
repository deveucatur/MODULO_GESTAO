import streamlit as st
from random import choices
import string
import random
import string
from PIL import Image
import streamlit_authenticator as stauth
import pandas as pd
import mysql.connector
from utilR import font_TITLE, menuProjeuHtml, menuProjeuCss


conexao = mysql.connector.connect(
    passwd='nineboxeucatur',
    port=3306,
    user='ninebox',
    host='nineboxeucatur.c7rugjkck183.sa-east-1.rds.amazonaws.com',
    database='projeu'
)
mycursor = conexao.cursor()

st.set_page_config(
    page_title="9box | New User",
    page_icon=Image.open('imagens/icone.png'),
    layout="wide",
    initial_sidebar_state='collapsed')

comandUSERS = 'SELECT * FROM projeu_users;'
mycursor.execute(comandUSERS)
dadosUser = mycursor.fetchall()

names = [x[2] for x in dadosUser]
usernames = [x[3] for x in dadosUser]
hashed_passwords = [x[7] for x in dadosUser]

def convert_to_dict(names, usernames, passwords):
    credentials = {"usernames": {}}
    for name, username, password in zip(names, usernames, passwords):
        user_credentials = {
            "email":username,
            "name": name,
            "password": password
        }
        credentials["usernames"][username] = user_credentials
    return credentials

credentials = convert_to_dict(names, usernames, hashed_passwords)
authenticator = stauth.Authenticate(credentials, "Teste", "abcde", 30)

col1, col2,col3 = st.columns([1,3,1])
with col2:
    name, authentication_status, username = authenticator.login('Acesse o sistema PROJEU', 'main')

if authentication_status == False:
    with col2:
        st.error('Email ou Senha Incorreto')
elif authentication_status == None:
    with col2:
        st.warning('Insira seu Email e Senha')
elif authentication_status:
    with st.sidebar:
        authenticator.logout('Logout', 'main')

    user = [x[2] for x in dadosUser if x[3] == username][0]

    primeiroNome = user.split()[0]

    menuHtml = menuProjeuHtml(primeiroNome)
    menuCss = menuProjeuCss()
    st.write(f'<div>{menuHtml}</div>', unsafe_allow_html=True)
    st.write(f'<style>{menuCss}</style>', unsafe_allow_html=True)

    tab1, tab2 = st.tabs(['Novos Usuários', 'Usuários Criados'])

    with tab1:    
        comando1 = 'SELECT * FROM projeu_users;'
        mycursor.execute(comando1)
        usersBD = mycursor.fetchall()

        comando2 = """SELECT DISTINCT PU.unidade, PM.macroprocesso, PC.condicao, PU.id, PM.id, PC.id
            FROM projeu_macropr AS PM
            INNER JOIN projeu_unidades AS PU
            INNER JOIN projeu_condicao_pagamento AS PC
            GROUP BY PU.unidade, PM.macroprocesso, PC.condicao, PU.id, PM.id, PC.id;"""
        mycursor.execute(comando2)
        dadosPagingBD = mycursor.fetchall()

        comando3 = "SELECT * FROM projeu_empresas;"
        mycursor.execute(comando3)
        empresasBD = mycursor.fetchall()

        unidadesBD = list(set([x[0] for x in dadosPagingBD]))
        macroprocBD = list(set([x[1] for x in dadosPagingBD]))
        condPagamentoBD = list(set([x[2] for x in dadosPagingBD]))
        mycursor.close()

        def func_users(username):
            dic_users = {'Padrão': 'P',
                        'Administrador': 'A',
                        'Governança': 'GV',
                        'Liderança': 'L'}

            return dic_users[str(username).strip()]


        fonte_Projeto = '''@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Bungee+Inline&family=Koulen&family=Major+Mono+Display&family=Passion+One&family=Sansita+Swashed:wght@500&display=swap');'''
        def CadastroDeUsuarios():
            font_TITLE('CADASTRO DE NOVOS USUÁRIOS', fonte_Projeto,"'Bebas Neue', sans-serif", 49, 'center')
            
            # colU, colU1 = st.columns([2,1.3])
            # with colU: 
            #     unidade = st.selectbox("Unidade de Negócio",  unidadesBD)
            # with colU1:
            #     empresa = st.selectbox('Empresa', list(set([x[1] for x in empresasBD if x[0] != 0])))

            colu1, colu2 = st.columns([2, 1.6])
            col1, col2, col3 = st.columns(3)
            co1, co2, co3 = st.columns([3, 3, 2])

            with colu1:
                nome = st.text_input("Nome")
            with colu2:
                cpf = st.text_input("CPF / CNPJ")

            with col1:
                unidade = st.selectbox("Unidade de Negócio",  unidadesBD)
            with col2:
                empresa = st.selectbox('Empresa', list(set([x[1] for x in empresasBD if x[0] != 0])))
            with col3:
                macroproc = st.selectbox('Macroprocesso', macroprocBD)

            with co1:
                matricula = st.text_input('Matricula')
            with co2:
                condPagamento = st.selectbox("Condição de Pagamento", condPagamentoBD)
            with co3:
                codCartao = st.text_input("Código cartão da empresa")

            if str(empresa).strip().upper() == 'PJ':
                email2 = st.text_input('Email para receber notificações')

            st.text(' ')
            especialidade = st.text_area('Especialidades')
            st.divider()
            email = st.text_input("Insira seu e-mail/Login")
            col1, col2 = st.columns(2)
            with col1:
                senhaaux =st.text_input("Insira uma senha", type = "password")
            with col2:
                senha = st.text_input("Confirme a senha", type = "password")
            
            type_user = st.selectbox('Tipo Usuário', ['Padrão', 'Administrador', 'Governança', 'Liderança'])
            
            st.text(' ')
            submitted = st.button("Cadastrar")

            if submitted:
                if senha != senhaaux:
                    st.toast('Senhas diferentes', icon='❌')
                else:
                    if str(email).strip().lower() not in [str(x[3]).strip().lower() for x in usersBD] and (senha).strip().lower() not in [str(x[4]).strip().lower() for x in usersBD]:
                        columnsBD = '''Matricula, Nome, cpf_cnpj, email, senha, unidade_fgkey, empresa_fgkey, macroprocesso_fgkey, condicao_pagamento_fgkey, especialidade, senha_hash, perfil_proj'''
                        values = f"""{matricula}, 
                                    '{str(nome).strip()}', 
                                    '{str(cpf).strip()}',
                                    '{str(email).strip()}', 
                                    '{senha}',
                                    '{list(set(x[3] for x in dadosPagingBD if x[0] == unidade))[0]}',
                                    '{empresasBD[list(x[1] for x in empresasBD).index(empresa)][0]}',
                                    '{list(set(x[4] for x in dadosPagingBD if x[1] == macroproc))[0]}',
                                    '{list(set(x[5] for x in dadosPagingBD if x[2] == condPagamento))[0]}',
                                    '{str(especialidade).strip()}',
                                    '{stauth.Hasher([senha]).generate()[0]}',
                                    '{func_users(str(type_user).strip())}' """

                        if str(empresa).strip().upper() == 'PJ':
                            columnsBD += ', email_pj'
                            values += f", '{email2}'"

                        senha = str(senha).strip()
                        mycursor = conexao.cursor()
                        cmdINSERT = f"""INSERT INTO projeu_users ({columnsBD})
                                            VALUES ({values});"""
                        
                        mycursor.execute(cmdINSERT)
                        conexao.commit()
                        mycursor.close()
                        st.toast('Cadastro Concluído!', icon='✅') 
                    else:
                        st.toast('Muito comum email ou senha utilizada.', icon='❌')

        CadastroDeUsuarios()
