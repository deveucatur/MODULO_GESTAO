import streamlit as st
from random import choices
import string
import random
import string
from PIL import Image
import streamlit_authenticator as stauth
import pandas as pd
import mysql.connector


conexao = mysql.connector.connect(
    passwd='nineboxeucatur',
    port=3306,
    user='ninebox',
    host='nineboxeucatur.c7rugjkck183.sa-east-1.rds.amazonaws.com',
    database='projeu'
)
mycursor = conexao.cursor()


comando2 = 'SELECT * FROM projeu_users;'
mycursor.execute(comando2)
listCod = mycursor.fetchall()

st.set_page_config(
page_title="9box | New User",
page_icon=Image.open('imagens/icone.png'),
layout="centered")

comando2 = 'SELECT * FROM projeu_users;'
mycursor.execute(comando2)
dadosUser = mycursor.fetchall()


def transform_to_string(lista):
    # Junta os elementos da lista em uma única string separada por vírgulas
    string_com_virgulas = ', '.join(map(str, lista))
    return string_com_virgulas


#perfilUser = 'BP'

tab1, tab2 = st.tabs(['Novos Usuários', 'Usuários Criados'])

with tab1:
    def gerar_sequencia_aleatoria():
        tamanho = 30

        trava = True
        while trava:
            caracteres = string.ascii_letters + string.digits
            carac_random =''.join(random.choices(caracteres, k=tamanho))
            if carac_random not in [x[1] for x in listCod]:
                trava = False    

        return carac_random


    def linkify(word, url):
        return f'<a href="{url}">{word}</a>'

    st.text(' ')
    st.subheader("Inclusão de Novos Usuários")
    st.text(' ')

    perfil_new_user = st.selectbox('Perfil', ['A', 'B'])

    if perfil_new_user == 'Administrador':
        perfil = 'A'
    elif perfil_new_user == 'Gestor':
        perfil = 'B'
    elif perfil_new_user == 'Business Partners':
        perfil = 'BP'
    else:
        perfil = 'C'
    
    #if perfil_new_user == 'Business Partners':
        #unidadeBP = st.multiselect('Unidades da BP', unidadesBD)

    funcao = st.selectbox('Função', ["Executor de Processos", "Líder de Processos", "Dono de processo", "Gestor de Processos",
                                    ])
    st.text(' ')
    st.text(' ')
    button = st.button('Gerar')

    codigo = gerar_sequencia_aleatoria()
    if button:
        if perfil != 'BP':
            comando = f'INSERT INTO Usuarios(cod_acesso, Perfil, Cargo) VALUES ("{codigo}", "{perfil}", "{funcao}")'
        else:
            comando = f'INSERT INTO Usuarios(cod_acesso, Perfil, Unidades_BP, Cargo) VALUES ("{codigo}", "{perfil}", "{transform_to_string(unidadeBP)}", "{funcao}")'

        mycursor.execute(comando)
        conexao.commit()
        with st.container():
            st.info(f"""
                        Cadastro | 9box
                        ----------------------------------------------------------------

                        ----------------------------------------------------------------

                        Insira o código de acesso 

                        ----------------------------------------------------------------
                        **{codigo}** 
                        ----------------------------------------------------------------                  
                        ----------------------------------------------------------------
                        No seguinte link:
                        
                        ----------------------------------------------------------------

                        https://9box-cadastro.eucatur.com.br/

                        ----------------------------------------------------------------

                        
                        """)

    st.text(' ')

    #with tab2:
    #    st.text(' ')
    #    st.subheader("Usuários Criados")
    #    st.text(' ')
    #    
    #    perfil = ''
    #    Unidade = st.multiselect("Unidade de negócio", list(set([x[2] for x in dadosUser if x[2] != '' and x[2] != None and x[2] != 'Zero'])), [])
    #                                                
    #    if len(Unidade) < 1:
    #        st.write("Não há uma unidade selecionada.")
    #    else:
    #        FuncList = set([x[6] for x in dadosUser if x[2] in Unidade])
    #        funcao = st.multiselect('Função', FuncList, FuncList)
    #        if len(funcao) < 1:
    #            st.info("Não há uma função selecionada")
    #        else:
    #            PerfList = list(set([x[9] for x in dadosUser if x[2] in Unidade and x[6] in funcao]))
    #            perfil = st.multiselect('Perfil', PerfList, PerfList)
#
    #    if len(perfil) > 0:
    #        dadosUser = [x for x in dadosUser if x[2] in Unidade and x[6] in funcao and x[9] in perfil]
#
    #        tipos_perfil = ['Administrador' if x[9] == 'A' else 'Gestor' if x[9] == 'B' else 'Business Partners' if x[9] == 'BP' else 'Avaliador' for x in dadosUser]
    #        
    #        list_dadosUser = [[dadosUser[x][4], dadosUser[x][5], dadosUser[x][2], tipos_perfil[x], dadosUser[x][1]] for x in range(len(dadosUser)) if dadosUser[x][5] != '' and dadosUser[x][5] != None and 'TESTE' not in str(dadosUser[x][5]).upper()]
    #        
    #        dados_user_to_df = pd.DataFrame({'Código Cadastro':[x[4] for x in list_dadosUser],
    #                                            'Matricula': [x[0] for x in list_dadosUser],
    #                                            'Colaborador': [x[1] for x in list_dadosUser],
    #                                            'Unidade': [x[2] for x in list_dadosUser],
    #                                            'Perfil': [x[3] for x in list_dadosUser]})
    #        
    #        st.table(dados_user_to_df)
