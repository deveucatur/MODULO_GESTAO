import streamlit as st
from PIL import Image
import streamlit_authenticator as stauth
import mysql.connector
from utilR import font_TITLE


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
layout="centered")

tab1, tab2, tab3 = st.tabs(['Novos Usuários', 'Usuários Criados', 'Check Usuário'])

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
        
        with st.form('Forms New User', clear_on_submit=False):
            font_TITLE('CADASTRO DE NOVOS USUÁRIOS', fonte_Projeto,"'Bebas Neue', sans-serif", 49, 'center')
            

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
            submitted_new_user = st.form_submit_button("Cadastrar")

            if submitted_new_user:
                if senha != senhaaux:
                    st.toast('Senhas diferentes', icon='❌')
                else:
                    #st.info([len(str(x).strip()) for x in [str(nome).strip(), str(cpf).strip(), str(email).strip(),email2, senha, senhaaux, cpf]])           
                    if 0 not in [len(str(x).strip()) for x in [str(nome).strip(), str(cpf).strip(), str(email).strip(),email2, senha, senhaaux, cpf]]:
                        if str(email).strip().lower() not in [str(x[3]).strip().lower() for x in usersBD]:
                            columnsBD = '''Nome, cpf_cnpj, email, senha, unidade_fgkey, empresa_fgkey, macroprocesso_fgkey, condicao_pagamento_fgkey, especialidade, senha_hash, perfil_proj, email_pj'''
                            values = f""" 
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
                                        '{func_users(str(type_user).strip())}', 
                                        '{email2}' """


                            if str(empresa).strip().upper() != 'PJ':
                                columnsBD += ', Matricula'
                                values += f', {matricula}'

                            senha = str(senha).strip()
                            mycursor = conexao.cursor()
                            cmdINSERT = f"""INSERT INTO projeu_users ({columnsBD})
                                                VALUES ({values});"""
                            
                            mycursor.execute(cmdINSERT)
                            conexao.commit()
                            mycursor.close()
                            st.toast('Cadastro Concluído!', icon='✅') 
                        else:
                            st.toast('Email já utilizado.', icon='❌')
                    else:
                        st.toast('Primeiramente, preencha todos os campos corretamente.', icon='❌')
 

    CadastroDeUsuarios()
