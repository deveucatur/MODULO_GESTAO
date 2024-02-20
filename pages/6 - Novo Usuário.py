import streamlit as st
from PIL import Image
import streamlit_authenticator as stauth
from utilR import font_TITLE, menuProjeuHtml, menuProjeuCss, validarEmail, enviar_email
import string
import random
from conexao import conexaoBD

conexao = conexaoBD()
mycursor = conexao.cursor()

st.set_page_config(
page_title="9box | New User",
page_icon=Image.open('imagens/icone.png'),
layout="wide",
initial_sidebar_state='collapsed')

menuHtml = menuProjeuHtml(" ")
menuCss = menuProjeuCss()
st.write(f'<div>{menuHtml}</div>', unsafe_allow_html=True)
st.write(f'<style>{menuCss}</style>', unsafe_allow_html=True)

comando1 = 'SELECT * FROM projeu_users;'
mycursor.execute(comando1)
usersBD = mycursor.fetchall()

tab1, tab2 = st.tabs(['Novos Usuários', 'Usuários Criados'])

with tab1:
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
    

    def func_users(username):
        dic_users = {'Padrão': 'P',
                     'Administrador': 'A',
                     'Governança': 'GV',
                     'Liderança': 'L'}

        return dic_users[str(username).strip()]
    
    def gerar_sequencia_aleatoria():
        tamanho = 5

        trava = True
        while trava:
            caracteres = string.ascii_letters + string.digits
            carac_random =''.join(random.choices(caracteres, k=tamanho))
            if carac_random not in [x[14] for x in usersBD]:
                trava = False    

        return carac_random


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
                    if str(empresa).strip() == 'PJ' and len(str(cpf).strip()) < 1:
                        st.toast('Primeiramente, preencha todos os campos corretamente.', icon='❌')                    
                    elif 0 not in [len(str(x).strip()) for x in [str(nome).strip(), str(email).strip(),email2, senha, senhaaux]]:
                        if str(email).strip().lower() not in [str(x[3]).strip().lower() for x in usersBD]:
                            codigo = gerar_sequencia_aleatoria()

                            columnsBD = '''Nome, cpf_cnpj, email, senha, unidade_fgkey, empresa_fgkey, macroprocesso_fgkey, condicao_pagamento_fgkey, especialidade, senha_hash, perfil_proj, codigo_user, email_pj'''
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
                                        '{str(codigo).strip()}', 
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
                            st.toast('Cadastro Concluído!', icon='✅')

                            validarEmail(str(codigo).strip())
                            enviar_email(str(email).strip(), str(codigo).strip())
                            st.info("Verifique o código de validação enviado no e-mail cadastrado")
                        else:
                            st.toast('Email já utilizado.', icon='❌')
                    else:
                        st.toast('Primeiramente, preencha todos os campos corretamente.', icon='❌')
                        
    CadastroDeUsuarios()

with tab2:
    cmdUnidade = 'SELECT * FROM projeu_unidades;'
    mycursor.execute(cmdUnidade)
    unidadeBD = mycursor.fetchall()
    
    mapearUnidades = {unidade[0]: unidade[1] for unidade in unidadeBD}
    
    unidadesAssociadas = [mapearUnidades.get(user[5], "") for user in usersBD]

    st.dataframe({"Matrícula" : [x[1] for x in usersBD],
                  "Nome" : [x[2] for x in usersBD],
                  "E-mail" : [x[3] for x in usersBD],
                  "Unidade" : [x for x in unidadesAssociadas],
                  "Perfil" : [x[8] for x in usersBD],
                  "Status" : [x[15] for x in usersBD]},
                  use_container_width=True)

    selectColab = st.selectbox("Colaborador", [x[2] for x in usersBD])
    index = [x[2] for x in usersBD].index(selectColab)

    if usersBD[index][5] is not None:
        indiceUnidade = [x[0] for x in unidadeBD].index(usersBD[index][5])
    else:
        indiceUnidade = None

    if usersBD[index][6] is not None:
        indiceMacro = macroprocBD.index(macroprocBD[usersBD[index][6] - 1])
    else:
        indiceMacro = None

    col1, col2, col3 = st.columns(3)

    with col1:
        matricula = st.text_input("Matricula", usersBD[index][1])
        senha = st.text_input("Nova Senha", type='password')
        especialidade = st.text_area("Especialidade", usersBD[index][12])
    with col2:
        nome = st.text_input("Nome", usersBD[index][2])
        unidade = st.selectbox("Unidade", [x[1] for x in unidadeBD], indiceUnidade)
        status = st.text_input("Status", usersBD[index][15])
    with col3:
        email = st.text_input("E-mail", usersBD[index][3])
        macro = st.selectbox("Macroprocesso", macroprocBD, indiceMacro)
        cpf = st.text_input("CPF / CNPJ", usersBD[index][13])

    salvar = st.button("Salvar")

    if salvar:
        colunasBD = ['Matricula', 'especialidade', 'Nome', 'unidade_fgkey', 'status_user', 'email', 'macroprocesso_fgkey', 'cpf_cnpj']
        valoresBD = [f'{str(matricula).strip()}',
            f"""'{str(especialidade).strip()}'""",
            f"""'{str(nome).strip()}'""",
            f'{list(set(x[3] for x in dadosPagingBD if x[0] == unidade))[0]}',
            f"""'{str(status).strip()}'""",
            f"""'{str(email).strip()}'""",
            f'{list(set(x[4] for x in dadosPagingBD if x[1] == macro))[0]}',
            f"""{str(cpf).strip() if cpf != None else 'NULL'}"""]

        if senha:
            colunasBD += ['senha', 'senha_hash']
            valoresBD += [f"""'{senha}'""",
                f"""'{stauth.Hasher([senha]).generate()[0]}'"""]

        mycursor = conexao.cursor()
        cmdUpdate = "UPDATE projeu_users SET "
        for i in range(len(colunasBD)):
            cmdUpdate += f"""{colunasBD[i]} = {valoresBD[i]}"""
            if i != len(colunasBD) - 1:
                cmdUpdate += ", "
        cmdUpdate += f" WHERE id_user = {usersBD[index][0]}"

        mycursor.execute(cmdUpdate)
        conexao.commit()

        st.toast('Usuário atualizado com sucesso!', icon='✅')
