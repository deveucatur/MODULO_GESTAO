import streamlit as st
from PIL import Image
from util import font_TITLE
import mysql.connector
from time import sleep
from datetime import date
import streamlit_authenticator as stauth
from utilR import menuProjeuHtml, menuProjeuCss

icone = Image.open('imagens/LogoProjeu.png')
st.set_page_config(
    page_title="Cadastro de Projetos",
    page_icon=icone,
    layout="wide",
    initial_sidebar_state='collapsed')

########CONECTANDO AO BANCO DE DADOS########
conexao = mysql.connector.connect(
    passwd='nineboxeucatur',
    port=3306,
    user='ninebox',
    host='nineboxeucatur.c7rugjkck183.sa-east-1.rds.amazonaws.com',
    database='projeu'
    )

def formatar_numero_string(numero_str):

    #FUNÇÃO QUE INVERTE STRINGS
    def inverteString(string):
        StringInvert = ''
        for i in range(len(string) - 1, -1, -1):
            StringInvert += string[i]

        return StringInvert

    partes = numero_str.split(",")
    
    #INVERTENDO OS NUMEROS PARA CONTABILIZAR E ADCIONAR PONTOS ENTRE OS DIGITOS
    textInvertAUX = inverteString(partes[0])

    contDigits = 0
    stringAUX = ''
    for a in textInvertAUX:
        contDigits += 1
        stringAUX += a
        if contDigits == 3:
            stringAUX += '.'
            contDigits = 0

    #INVERTENDO NOVAMENTE E TRAZENDO OS DIGITOS PARA FORMATO ORIGINAL, PORÉM, AGORA COM OS PONTOS ENTRE ELES
    stringOFI = inverteString(stringAUX)
    
    if len(partes) > 1:
        return f"{stringOFI},{partes[1]}0"
    else:
        return stringOFI


#CONSUMINDO OS DADOS DO BANCO DE ADOS
mycursor = conexao.cursor()
mycursor.execute("""SELECT 
  p.nome_prog, 
  m.macroprocesso
FROM projeu_programas p
JOIN projeu_macropr m ON p.macroprocesso_fgkey = m.id;"""
)

dados_page = mycursor.fetchall()

mycursor.execute("SELECT DISTINCT(name_proj) FROM projeu_projetos;")
dd_proj = [x[0] for x in mycursor.fetchall()]
prog_macro = [list(x) for x in dados_page]


mycursor.execute("""SELECT Matricula, 
                 Nome FROM projeu_users;"""
)
users = mycursor.fetchall()

mycursor.execute('SELECT * FROM projeu_users WHERE perfil_proj in ("A", "L", "GV");')
usersBD = mycursor.fetchall()
mycursor.close()


########################## APRESENTAÇÃO DO FRONT ##########################
names = [x[2] for x in usersBD]
usernames = [x[3] for x in usersBD]
hashed_passwords = [x[8] for x in usersBD]

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
    matriUser = [x[1] for x in usersBD if x[3] == username][0]
    dados_user = [x for x in usersBD if str(x[1]).strip() == str(matriUser).strip()]
    user = [x[2] for x in usersBD if x[3] == username][0]

    primeiroNome = user.split()[0]

    menuHtml = menuProjeuHtml(primeiroNome)
    menuCss = menuProjeuCss()
    st.write(f'<div>{menuHtml}</div>', unsafe_allow_html=True)
    st.write(f'<style>{menuCss}</style>', unsafe_allow_html=True)

    #$if str(dados_user[0][8]).strip().upper() == 'A':
    fonte_Projeto = '''@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Bungee+Inline&family=Koulen&family=Major+Mono+Display&family=Passion+One&family=Sansita+Swashed:wght@500&display=swap');
    '''
    font_TITLE('CADASTRO DE PROJETOS', fonte_Projeto,"'Bebas Neue', sans-serif", 49, 'center')
    complix = ['SEGURO', 'ACESSÍVEL', 'ABSTRATO I', 'ABSTRATO II', 'ABSTRATO III', 'SINGULAR I', 'SINGULAR II',
            'SINGULAR III']

    nomeProjeto = st.text_input('Nome do Projeto')
    col1, col2 = st.columns(2)
    with col1:
        colaux1, colaux2 = st.columns([1.3, 2])    
        with colaux1:
            typ_proj = st.selectbox('Tipo Projeto', ['Estratégico', 'OKR', 'Implantação', 'Rápido'])
        with colaux2:
            MacroProjeto = st.selectbox('Macroprocesso', list(set([x[1] for x in prog_macro])))    

        colG1, colG2 = st.columns([1,3]) 
        with colG2:
            gestorProjeto = st.selectbox('Gestor do Projeto', list(set([x[1] for x in users])), 0)
        with colG1:
            matric_gestor = st.text_input('Matricula Gestor', [x[0] for x in users if x[1] == gestorProjeto][0], disabled=True)
        
        if typ_proj not in ("Rápido", "Implantação"):
            mvp_name = st.text_input('MVP')

        pdt_entrFinal = st.text_area('Produto Projeto', key='ProdutoEntrega')

    with col2:
        nomePrograma = st.selectbox('Programa', [x[0] for x in prog_macro if x[1] == MacroProjeto])

        colD1, colD2 = st.columns([2,1]) 
        with colD1:
            dat_inic = st.date_input('Início Projeto')
        with colD2:
            ivsProget = st.text_input('Investimento', placeholder='R$ 0,00')

        if typ_proj not in ("Rápido", "Implantação"):
            mvp_produt = st.text_input('Produto MVP')    

        result_esperd = st.text_area('Resultado Esperado')

    if typ_proj in ('Implantação'):
        #PARÂMETROS ESPECÍFICOS DOS PROJETOS DE IMPLANTAÇÃO
        font_TITLE('PARÂMETROS DE IMPLANTAÇÃO', fonte_Projeto,"'Bebas Neue', sans-serif", 33, 'left')
        
        impl_stake = st.text_input('Stakeholders')
        impl_premi = st.text_input('Premissas')
        impl_risco = st.text_input('Riscos')
        impl_justific = st.text_area('Justificativa')
        col1, col2, col3 = st.columns(3)
        with col1:
            impl_obj = st.text_area('Objetivo Smart')
        with col2:
            impl_requis = st.text_area('Requisitos do Projeto')
        with col3:
            impl_restric = st.text_area('Restrições')
        

        ##### ADCIONANDO MARCOS NA LINHA DO TEMPO #####
        st.write('---')
        col1, col2 = st.columns([3,1])
        with col1:
            font_TITLE('LINHA DO TEMPO', fonte_Projeto,"'Bebas Neue', sans-serif", 33, 'left')
        with col2:
            qntd_entr = st.number_input('Quantidade', min_value=1, step=1, key='Cadastrar linha do tempo')

        listMarcosTime = []
        st.caption('Principais etapas e marcos do projeto')
        for a_entr in range(qntd_entr):
            listMarcosTime.append(st.text_input('', label_visibility="collapsed", key=f'Cadastrar linha do tempo{a_entr}'))

    else:
        ##### ADCIONANDO MÉTRICAS #####
        st.write('---')
        col1, col2 = st.columns([3,1])
        with col1:
            font_TITLE('MÉTRICAS', fonte_Projeto,"'Bebas Neue', sans-serif", 33, 'left')
        with col2:
            qntd_metric = st.number_input('Quantidade', min_value=1, step=1, key=f'Cadastrar Metricas')

        listMetric = []
        st.caption('Métricas')
        for a_metrc in range(qntd_metric):
            listMetric.append(st.text_input('', label_visibility="collapsed", key=f'Cadastrar Metricas{a_metrc}'))
            

    ##### ADCIONANDO AS PRÍNCIPAIS ENTREGAS #####
    st.write('---')
    col1, col2 = st.columns([3,1])
    with col1:
        font_TITLE('PRINCIPAIS ENTREGAS', fonte_Projeto,"'Bebas Neue', sans-serif", 33, 'left')
    with col2:
        qntd_entr = st.number_input('Quantidade', min_value=1, step=1, key='Cadastrar Entregas')

    listEntregas = []
    st.caption('Entregas')
    for a_entr in range(qntd_entr):
        listEntregas.append(st.text_input('', label_visibility="collapsed", key=f'Cadastrar Entreg{a_entr}'))

        
    ##### ADCIONANDO A EQUIPE #####
    st.write('---')
    col1, col2 = st.columns([3,1])
    with col1:
        font_TITLE('CADASTRO EQUIPE', fonte_Projeto,"'Bebas Neue', sans-serif", 33, 'left')
    with col2:
        qntd_clb = st.number_input('Quantidade', min_value=1, step=1)

    col_equip1, col_equip2, col_equip3 = st.columns([0.3, 2, 1])
    with col_equip1:
        st.caption('Matricula')
    with col_equip2:
        st.caption('Colaboradores')
    with col_equip3:
        st.caption('Função')

    #A IDEIA É QUE OS USUÁRIOS SELECIONADOS DURANTE O PREENCHIMENTO DO FORMULÁRIO SEJAM PEGOS AS INFORMAÇÕES DO BANCO DE DADOS DE USUÁRIO
    list_colbs = [[matric_gestor, 'Gestor']]
    for colb_a in range(qntd_clb):
        with col_equip2:
            colb_name = st.selectbox('Colaboradores', [x[1] for x in users], label_visibility="collapsed", key=f'Cadastrar Nome Colab{colb_a}')        
        with col_equip1:
            colab_matric = st.text_input('Matricula', list(set([x[0] for x in users if x[1] == colb_name]))[0], label_visibility="collapsed", disabled=True, key=f'Cadastrar MatriculaColabs{colb_a}')
        with col_equip3:
            colb_funç = st.selectbox('Função', ['Especialista', 'Executor'],None, label_visibility="collapsed", key=f'Cadastrar funcaoColab{colb_a}')
        list_colbs.append([colab_matric, colb_funç])

    st.text(' ')
    st.text(' ')
    colb1,colb2,colb3 = st.columns([3,3,1])
    with colb3:
        st.text(' ')
        btt_criar_prj = st.button('Criar Projeto')

    if btt_criar_prj:
        if len([x for x in list_colbs if x[1] == None]) < 1:
            if nomeProjeto not in dd_proj:
                if typ_proj == "Estratégico":
                    parametros = [len(str(x).strip()) if type(x) in (date, str) else len(x) for x in [typ_proj, MacroProjeto, gestorProjeto, mvp_name, pdt_entrFinal, nomePrograma, dat_inic, mvp_produt, result_esperd, listEntregas, list_colbs]]
                elif typ_proj == 'Rápido':
                    parametros = [len(str(x).strip()) if type(x) in (date, str) else len(x) for x in [typ_proj, MacroProjeto, gestorProjeto, pdt_entrFinal, nomePrograma, dat_inic, result_esperd, listEntregas, list_colbs]]
                elif typ_proj == 'Implantação':
                    parametros = [len(str(x).strip()) if type(x) in (date, str) else len(x) for x in [typ_proj, MacroProjeto, gestorProjeto, pdt_entrFinal, nomePrograma, dat_inic, listEntregas, list_colbs, impl_stake, impl_premi, impl_risco, impl_obj, impl_requis, impl_restric, impl_justific]]

                if 0 not in parametros:

                    mycursor = conexao.cursor()
                    try:
                        ############# INSERINDO O PROJETO #############
                        if typ_proj == "Estratégico":
                            cmd_criar_project = f"""INSERT INTO projeu_projetos(
                                type_proj_fgkey, macroproc_fgkey, progrm_fgkey, name_proj, 
                                result_esperad, gestor_id_fgkey, nome_mvp,
                                produto_mvp, produto_entrega_final,  
                                ano, date_posse_gestor,  status_proj, investim_proj
                                ) VALUES (
                                (SELECT id_type FROM projeu_type_proj WHERE type_proj LIKE '%{str(typ_proj).strip()}%'), (SELECT id FROM projeu_macropr WHERE macroprocesso LIKE '%{str(MacroProjeto).strip()}%'), 
                                (SELECT id_prog FROM projeu_programas WHERE nome_prog LIKE '%{nomePrograma}%'), 
                                '{str(nomeProjeto).strip()}', '{str(result_esperd).strip()}', 
                                (SELECT id_user FROM projeu_users WHERE Matricula = {matric_gestor}), '{str(mvp_name).strip()}', '{str(mvp_produt).strip()}', 
                                '{str(pdt_entrFinal).strip()}', {int(dat_inic.year)}, '{dat_inic}', 'Aguardando Início' , '{str(ivsProget).strip()}');"""
                        elif typ_proj == 'Rápido':
                            cmd_criar_project = f"""INSERT INTO projeu_projetos(
                                type_proj_fgkey, macroproc_fgkey, progrm_fgkey, name_proj, 
                                result_esperad, gestor_id_fgkey, produto_entrega_final,  
                                ano, date_posse_gestor,  status_proj, investim_proj
                                ) VALUES (
                                (SELECT id_type FROM projeu_type_proj WHERE type_proj LIKE '%{str(typ_proj).strip()}%'), (SELECT id FROM projeu_macropr WHERE macroprocesso LIKE '%{str(MacroProjeto).strip()}%'), 
                                (SELECT id_prog FROM projeu_programas WHERE nome_prog LIKE '%{nomePrograma}%'), 
                                '{str(nomeProjeto).strip()}', '{str(result_esperd).strip()}', 
                                (SELECT id_user FROM projeu_users WHERE Matricula = {matric_gestor}), '{str(pdt_entrFinal).strip()}', {int(dat_inic.year)}, '{dat_inic}', 'Aguardando Início' , '{str(ivsProget).strip()}');"""
                        elif typ_proj == 'Implantação':
                            cmd_criar_project = f"""
                                INSERT INTO 
                                    projeu_projetos( 
                                        type_proj_fgkey, 
                                        macroproc_fgkey, 
                                        progrm_fgkey, 
                                        name_proj, 
                                        result_esperad, 
                                        gestor_id_fgkey, 
                                        produto_entrega_final,
                                        ano, 
                                        date_posse_gestor, 
                                        status_proj, 
                                        investim_proj,
                                        justific_impl_proj,
                                        stakeholders_impl_proj,
                                        premissas_impl_proj,
                                        riscos_impl_proj,
                                        restric_impl_proj,
                                        objSmart_impl_proj,
                                        requisitos_impl_proj 
                                ) VALUES (
                                (SELECT id_type FROM projeu_type_proj WHERE type_proj LIKE '%{str(typ_proj).strip()}%'), (SELECT id FROM projeu_macropr WHERE macroprocesso LIKE '%{str(MacroProjeto).strip()}%'), 
                                (SELECT id_prog FROM projeu_programas WHERE nome_prog LIKE '%{nomePrograma}%'), 
                                '{str(nomeProjeto).strip()}', '{str(result_esperd).strip()}', 
                                (SELECT id_user FROM projeu_users WHERE Matricula = {matric_gestor}), '{str(pdt_entrFinal).strip()}', {int(dat_inic.year)}, '{dat_inic}', 'Aguardando Início' , '{str(ivsProget).strip()}', '{impl_justific}', '{impl_stake}', '{impl_premi}', '{impl_risco}', '{impl_restric}', '{impl_obj}', '{impl_requis}');"""


                        mycursor.execute(cmd_criar_project)
                        conexao.commit()
                        print('PROJETO CRIADO!')
                        print('---'*30)
                        print('VINCULANDO COLABORADORES AO PROJETO')
                        sleep(0.1)

                        if typ_proj not in ('Implantação'):
                            ############# INSERINDO MÉTRICAS DO PROJETO #############
                            dd_metric = ''
                            for metric_name in listMetric:
                                dd_metric += f"((SELECT id_proj FROM projeu_projetos WHERE name_proj LIKE '%{str(nomeProjeto).strip()}%' LIMIT 1), '{metric_name}'),"
                            dd_metric = dd_metric[:len(dd_metric)-1]

                            cmd_metric = f"""INSERT INTO projeu_metricas(id_prj_fgkey, name_metric) 
                                                VALUES {dd_metric};"""
                            
                            mycursor.execute(cmd_metric)
                            conexao.commit()
                            sleep(0.1)

                        #else:
                        #    ############# INSERINDO MARCOS DO PROJETO #############
                        #    values_line = ''
                        #    for marco_time in listMarcosTime:
                        #        
                        #        if len(str(marco_time).strip()) > 0: 
                        #            cmd_line_tempo = f"""('{marco_time}', (SELECT * FROM projeu_projetos WHERE name_proj LIKE '%{str(nomeProjeto).strip()}%')),"""
                        #            values_line += cmd_line_tempo
                        #    
                        #    values_line = values_line[:-1]
                        #
                        #    if len(str(values_line).strip()) > 0:
                        #        cmd_insert_marcos = f"""
                        #        INSERT INTO projeu_impl_linhaTempo (marco_line_tempo, id_proj_fgkey)
                        #            VALUES {values_line};"""
                        #


                        ############# INSERINDO COMPLEXIDADE #############
                        if typ_proj != "Rápido":
                            cmd_insert_complx = f'''INSERT INTO projeu_complexidade (proj_fgkey, date_edic) 
                            VALUES (
                            (SELECT id_proj FROM projeu_projetos WHERE name_proj LIKE '%{str(nomeProjeto).strip()}%' LIMIT 1),
                            '{date.today()}'
                            );'''
                        else:
                            cmd_insert_complx = f'''INSERT INTO projeu_complexidade (proj_fgkey, date_edic, complxdd, check_lider, check_govern, check_avaliado) 
                            VALUES (
                            (SELECT id_proj FROM projeu_projetos WHERE name_proj LIKE '%{str(nomeProjeto).strip()}%' LIMIT 1),
                            '{date.today()}', 'Rápido', 1, 1, 1
                            );'''

                        mycursor.execute(cmd_insert_complx)
                        conexao.commit()
                        print('LINHA DE COMPLEXIDADE VINCULADO AO BANCO DE DADOS!')
                        sleep(0.1)

                        
                        ############# INSERINDO EQUIPE #############
                        values_ie = [f"""((SELECT id_proj FROM projeu_projetos WHERE name_proj LIKE '%{str(nomeProjeto).strip()}%' LIMIT 1), (SELECT id_user FROM projeu_users WHERE Matricula = {list_colb[0]} limit 1), '{list_colb[1]}')""" for list_colb in list_colbs]
                        comand_insert_colabs = f"""INSERT INTO projeu_registroequipe(id_projeto, id_colab, papel) VALUES {str(values_ie).replace('[', '').replace(']', '').replace('"', '')} ;"""
                        
                        mycursor.execute(comand_insert_colabs)
                        conexao.commit()

                        print('COLABORADORES VINCULADOS')
                        sleep(0.1)
                        
                        ############# INSERINDO PRINCIPAIS ENTREGAS #############
                        if len(listEntregas) > 0:
                            values_pe = list([f"""('{name_entr}',(SELECT id_proj FROM projeu_projetos WHERE name_proj LIKE '%{str(nomeProjeto).strip()}%' LIMIT 1))""" 
                                            for name_entr in listEntregas])
                            
                            cmd_insert_princp = f'''INSERT INTO projeu_princEntregas (
                            entreg, 
                            id_proj_fgkey
                            )
                            values {str(values_pe).replace('[', '').replace(']', '').replace('"', '')};'''
                            
                            mycursor.execute(cmd_insert_princp)
                            conexao.commit()

                        st.toast('Sucesso na criação do Projeto!', icon='✅')
                        
                    except:
                        st.toast('Erro ao cadastrar projeto na base de dados.', icon='❌')
                    mycursor.close()
                else:
                    st.toast('Primeiramente, preencha todos os campos corretamente.', icon='❌')
            else:
                st.toast('Já existe um projeto com esse nome.', icon='❌')
        else:
            st.toast('Por gentileza, ajustar corretamente todas as funções da equipe selecionada.', icon='❌')

    
