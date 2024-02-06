import datetime
import streamlit as st
import pandas as pd
from util import font_TITLE, string_to_datetime, cardGRANDE, displayInd, ninebox, css_9box, nineboxDatasUnidades, CalculoPrêmio
from time import sleep
import mysql.connector
from datetime import date, timedelta, datetime
from collections import Counter
from utilR import PlotCanvas, menuProjeuHtml, menuProjeuCss
import streamlit_authenticator as stauth
import plotly.graph_objects as go
from conexao import conexaoBD

st.set_page_config(
    page_title="Gerir Portfólio",
    layout="wide",
    initial_sidebar_state='collapsed')

conexao = conexaoBD()

mycursor = conexao.cursor()

setSession = "SET SESSION group_concat_max_len = 5000;"
mycursor.execute(setSession)

comand = f"""
SELECT 
    projeu_projetos.id_proj, 
    projeu_projetos.name_proj,
    (SELECT Nome FROM projeu_users WHERE id_user = projeu_projetos.gestor_id_fgkey) AS name_gestor, 
    (SELECT Matricula FROM projeu_users WHERE id_user = projeu_projetos.gestor_id_fgkey) AS matricula_gestor,
    (SELECT type_proj FROM projeu_type_proj WHERE id_type = projeu_projetos.type_proj_fgkey) AS type_proj,
    (SELECT macroprocesso FROM projeu_macropr WHERE id = projeu_projetos.macroproc_fgkey) AS macroprocesso,
    (SELECT nome_prog FROM projeu_programas WHERE id_prog = projeu_projetos.progrm_fgkey) AS programa,
    projeu_projetos.nome_mvp,
    projeu_projetos.investim_proj,
    projeu_projetos.result_esperad as objetivo_projet,
    projeu_projetos.produto_entrega_final,
    (
        SELECT GROUP_CONCAT(number_sprint SEPARATOR '~/>') 
        FROM projeu_sprints 
        WHERE projeu_sprints.id_proj_fgkey = projeu_projetos.id_proj
    ) as number_sprint,
    (
        SELECT GROUP_CONCAT(status_sprint SEPARATOR '~/>') 
        FROM projeu_sprints 
        WHERE projeu_sprints.id_proj_fgkey = projeu_projetos.id_proj
    ) as status_sprint,
    (
        SELECT GROUP_CONCAT(date_inic_sp SEPARATOR '~/>') 
        FROM projeu_sprints 
        WHERE projeu_sprints.id_proj_fgkey = projeu_projetos.id_proj
    ) as inic_sprint,
    (
        SELECT GROUP_CONCAT(date_fim_sp SEPARATOR '~/>') 
        FROM projeu_sprints 
        WHERE projeu_sprints.id_proj_fgkey = projeu_projetos.id_proj
    ) as fim_sprint,
    (
        SELECT GROUP_CONCAT(IFNULL(status_homolog, "NULO") SEPARATOR '~/>')
        FROM projeu_sprints 
        WHERE projeu_sprints.id_proj_fgkey = projeu_projetos.id_proj
    ) as status_homolog_sprint,
    (
        SELECT GROUP_CONCAT(nome_Entrega SEPARATOR '~/>') 
        FROM projeu_entregas 
        WHERE projeu_entregas.id_sprint IN (
            SELECT id_sprint 
            FROM projeu_sprints 
            WHERE projeu_sprints.id_proj_fgkey = projeu_projetos.id_proj
        )
    ) as entrega_name,
    (
        SELECT GROUP_CONCAT(executor SEPARATOR '~/>') 
        FROM projeu_entregas 
        WHERE projeu_entregas.id_sprint IN (
            SELECT id_sprint 
            FROM projeu_sprints 
            WHERE projeu_sprints.id_proj_fgkey = projeu_projetos.id_proj
        )
    ) as executor_entrega,
    (
        SELECT GROUP_CONCAT(hra_necess SEPARATOR '~/>') 
        FROM projeu_entregas 
        WHERE projeu_entregas.id_sprint IN (
            SELECT id_sprint 
            FROM projeu_sprints 
            WHERE projeu_sprints.id_proj_fgkey = projeu_projetos.id_proj
        )
    ) as hrs_entrega,
    (
        SELECT GROUP_CONCAT(compl_entrega SEPARATOR '~/>') 
        FROM projeu_entregas 
        WHERE projeu_entregas.id_sprint IN (
            SELECT id_sprint 
            FROM projeu_sprints 
            WHERE projeu_sprints.id_proj_fgkey = projeu_projetos.id_proj
        )
    ) as complex_entreg,
    (
        SELECT GROUP_CONCAT(id_registro SEPARATOR '~/>') 
        FROM projeu_registroequipe 
        WHERE projeu_registroequipe.id_projeto = projeu_projetos.id_proj
        AND projeu_registroequipe.status_reg = 'A'
    ) as id_registro,
    (
        SELECT GROUP_CONCAT(Nome SEPARATOR '~/>') 
        FROM projeu_users 
        WHERE id_user IN (
            SELECT id_colab 
            FROM projeu_registroequipe 
            WHERE projeu_registroequipe.id_projeto = projeu_projetos.id_proj
            AND projeu_registroequipe.status_reg = 'A'
        )
    ) as colaborador,
    (
        SELECT GROUP_CONCAT(papel SEPARATOR '~/>') 
        FROM projeu_registroequipe 
        WHERE projeu_registroequipe.id_projeto = projeu_projetos.id_proj
        AND projeu_registroequipe.status_reg = 'A'
    ) as PAPEL,
    (
        SELECT 
            GROUP_CONCAT(Matricula SEPARATOR '~/>') AS MATRICULA_EQUIPE
        FROM projeu_users AS PU
        INNER JOIN projeu_registroequipe AS PR ON PU.id_user = PR.id_colab 
        WHERE PR.id_projeto = projeu_projetos.id_proj
        AND PR.status_reg = 'A'
    ) as matriculaEQUIPE,
    projeu_projetos.status_proj AS STATUS_PROJETO,
    projeu_projetos.produto_mvp AS PRODUTO_MVP,
    projeu_projetos.prazo_entreg_final,
    (
        SELECT GROUP_CONCAT(id_sprint SEPARATOR '~/>') 
        FROM projeu_sprints 
        WHERE projeu_sprints.id_proj_fgkey = projeu_projetos.id_proj
    ) as id_sprint,
    projeu_projetos.date_aprov_proj,
    projeu_projetos.date_posse_gestor,
    projeu_projetos.date_imersao_squad,
    projeu_projetos.status_proj,
    (
		SELECT 
			GROUP_CONCAT(entreg SEPARATOR '~/>')
		FROM projeu_princEntregas 
		WHERE id_proj_fgkey = projeu_projetos.id_proj
	) AS PRINCIPAIS_ENTREGAS,
    (
		SELECT 
			GROUP_CONCAT(name_metric SEPARATOR '~/>') 
		FROM projeu_metricas 
		WHERE id_prj_fgkey = projeu_projetos.id_proj
	) AS METRICAS,
    (
		SELECT 
			GROUP_CONCAT(projeu_sprints.check_sprint SEPARATOR '~/>') 
		FROM projeu_sprints 
		WHERE id_proj_fgkey = projeu_projetos.id_proj
	) AS CHECK_SPRINT,
    (
		SELECT 
			GROUP_CONCAT(projeu_sprints.data_check SEPARATOR '~/>') 
		FROM projeu_sprints 
		WHERE id_proj_fgkey = projeu_projetos.id_proj
	) AS DATA_CHECK,
    PC.complxdd AS COMPLEXIDADE_PROJETO,
    PC.nivel AS NIVEL_COMPLEXIDADE,
    projeu_projetos.check_proj,
    (
		SELECT 
			group_concat(PPE.id_princ SEPARATOR '~/>') 
		FROM projeu_princEntregas AS PPE
        WHERE PPE.id_proj_fgkey = projeu_projetos.id_proj
	) AS ID_PRINCIPAIS_ENTREGAS,
    (
		SELECT 
			group_concat(PPE.status_princp SEPARATOR '~/>') 
		FROM projeu_princEntregas AS PPE
        WHERE PPE.id_proj_fgkey = projeu_projetos.id_proj
	) AS STATUS_PRINCIPAIS_ENTREGAS,
    (
		SELECT 
			GROUP_CONCAT(id_metric SEPARATOR '~/>') 
		FROM projeu_metricas 
		WHERE id_prj_fgkey = projeu_projetos.id_proj
	) AS ID_METRICAS,
    (
		SELECT 
			GROUP_CONCAT(status_metric SEPARATOR '~/>') 
		FROM projeu_metricas 
		WHERE id_prj_fgkey = projeu_projetos.id_proj
	) AS STATUS_METRICAS,
	(
        SELECT GROUP_CONCAT(date_homolog SEPARATOR '~/>') 
        FROM projeu_sprints 
        WHERE projeu_sprints.id_proj_fgkey = projeu_projetos.id_proj
    ) as date_homolog_sprint,
	 (
        SELECT GROUP_CONCAT(status_homolog SEPARATOR '~/>') 
        FROM projeu_sprints 
        WHERE projeu_sprints.id_proj_fgkey = projeu_projetos.id_proj
    ) as STATUS_HOMOLOG
FROM 
    projeu_projetos
JOIN 
	projeu_complexidade PC on PC.proj_fgkey = projeu_projetos.id_proj
GROUP BY
    projeu_projetos.id_proj;"""

mycursor.execute(comand)
ddPaging = mycursor.fetchall()


consult2AUX = '''
SELECT 
	projeu_param_premio.id_pp,
    TYP.type_proj,
    PCP.nome_parm,
    projeu_param_premio.typ_event,
    CAST(projeu_param_premio.porc AS DECIMAL(10, 2)) AS porc,
    projeu_param_premio.qntd_event 
FROM 
	projeu_param_premio
JOIN 
	projeu_type_proj TYP ON projeu_param_premio.typ_proj_fgkey = TYP.id_type
JOIN 
	projeu_compl_param PCP ON projeu_param_premio.complx_param_fgkey = PCP.id_compl_param;
'''
mycursor.execute(consult2AUX)
param_premiosBD = mycursor.fetchall()


comandUSERS = 'SELECT * FROM projeu_users WHERE perfil_proj IN ("A", "GV");'
mycursor.execute(comandUSERS)
dadosUser = mycursor.fetchall()

mycursor.execute("""SELECT Matricula, 
                 Nome FROM projeu_users;"""
)
users = mycursor.fetchall()

mycursor.close()

def tableGeral():
    dadosUnic = tableUnic()

    htmlGeral = f"""
        <div class="flex-container">
            <div class="flex-row">
                <div>{dadosUnic}</div>
            </div>
        </div>
    """
    return htmlGeral

canvaStyle = """
    @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Bungee+Inline&family=Koulen&family=Major+Mono+Display&family=Passion+One&family=Sansita+Swashed:wght@500&display=swap');
    bodyC{
        margin: 0;
        padding: 0;
        background-color: #fff;
    }
    
    .boxC{
        display: flex;
        align-items: flex-end;
        justify-content: center;
        width: 100%;
    }

    .box5C {
        width: 100%;
        height: auto;
        margin: 5px;
        overflow: auto;
        overflow-x: hidden;
        scrollbar-width: thin;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.0), 0 4px 6px -2px rgba(0, 0, 0, 0.0);
        border-radius: 25px;
    }

    .box5C:hover{
        transform: scale(0.98);
        border-radius: 20px;
    }

    .table5C{
        border-collapse: collapse;
        border-radius: 10px;
        overflow: hidden; 
        min-height: 220px;
        max-height: 220px;
    }

    .thead5C{
        background-color: #DADADA;
        position: sticky;
        top: 0;
        z-index: 1;
    }

    .thead5C{
        min-height: 50px;
        max-height: 50px;
    }

    .thead5C th{
        text-align: center;
        min-height: 50px;
        max-height: 50px;
        font-weight: bold;
        font-family: Bebas Neue;
        font-size: 22px;
    }

    .thead5C img{
        vertical-align: middle;
        margin-left: 10px;
        width: 20px;
        height: auto;
    }

    .tdata5C td{
        border-top: 1px solid #96008c93;
        background-color: #fff;
    }

    .flex-rowC {
        display: flex;
        justify-content: center;
        height: auto;
    }
    
    .box5C::-webkit-scrollbar{
        width: 6px;
        border-radius: 20px;
    }
    
    .box5C::-webkit-scrollbar-track{
        border-radius: 20px;
    }
    
    .box5C::-webkit-scrollbar-thumb{
        border-radius: 20px;
        border: 1px solid;
    }"""

def tableUnic():
    entrega = entregas
    entregaCode = ""
    for i in range(len(entrega)):
        entregaCode += f"""<tr class="tdata5C">
                <td>{entrega[i]}</td>
            </tr>"""

    htmlUnic = f"""
        <div class="boxC">
            <div class="box5C">
                <table class="table5C">
                    <tr class="thead5C">
                        <th>PROJETOS</th>
                    </tr>
                    <div>{entregaCode}</div>
                </table>
            </div>
        </div>
    """
    return htmlUnic

    
def mapear_dificuldade(dificuldade):
    if dificuldade == 'Fácil':
        return 'F'
    elif dificuldade == 'Médio':
        return 'M'
    elif dificuldade == 'Difícil':
        return 'D'
    else:
        return '---' 

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

    matriUser = [x[1] for x in dadosUser if x[3] == username][0]
    user = [x[2] for x in dadosUser if x[3] == username][0]

    primeiroNome = user.split()[0]

    menuHtml = menuProjeuHtml(primeiroNome)
    menuCss = menuProjeuCss()
    st.write(f'<div>{menuHtml}</div>', unsafe_allow_html=True)
    st.write(f'<style>{menuCss}</style>', unsafe_allow_html=True)
    
    fonte_Projeto = '''@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Bungee+Inline&family=Koulen&family=Major+Mono+Display&family=Passion+One&family=Sansita+Swashed:wght@500&display=swap');'''
    font_TITLE('GERIR PORTFÓLIO', fonte_Projeto,"'Bebas Neue', sans-serif", 49, 'center')

    st.text(' ')
    font_TITLE('ACOMPANHAMENTO DOS PROJETOS', fonte_Projeto,"'Bebas Neue', sans-serif", 30, 'left', '#228B22')
    st.text(' ')
    #############INFORMAÇÕES GERAIS DE PROJETOS#############
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        displayInd('Total', f'{len(id_projcts:=list(set([x[0] for x in ddPaging])))}', 1, 3)
    with col2:
        displayInd('Não Iniciado', f'{len(list(set([x[0] for x in ddPaging if x[13] == None or string_to_datetime(str(x[13]).split("~/>")[0]) > date.today()])))}', 1, 3)
    with col3:
        displayInd('Em Andamento', f'{len(list(set([x[0] for x in ddPaging if x[13] != None and string_to_datetime(str(x[13]).split("~/>")[0]) < date.today() and x[24] != "Concluído"])))}', 1, 3)
    with col4:
        displayInd('Paralisado', f'{len([x[1] for x in ddPaging if str(x[31]).strip() == "Paralisado"])}', 1, 3)
    with col5:
        displayInd('Concluído', f'{len(list(set([x[0] for x in ddPaging if x[24] == "Concluído"])))}', 1, 3)
    #AGUARDANDO INÍCIO, EM ANDAMENTO, PARALISADO
    dadosbox = [[],[[x[1] for x in ddPaging if str(x[31]).strip() == 'Aguardando Início'], 
                    [x[1] for x in ddPaging if str(x[31]).strip() == 'Em Andamento'], 
                    [x[1] for x in ddPaging if str(x[31]).strip() == 'Paralisado']]]
    ninebox_style = css_9box()

    colbox, colbox1, colbox2 = st.columns(3)
    with colbox:
        html1 = ninebox(2, nineboxDatasUnidades(dadosbox), dadosbox, 'Aguardando Início')
        st.write(f'<style>{ninebox_style}</style>', unsafe_allow_html=True)
        st.write(f'<div>{html1}</div>', unsafe_allow_html=True)
        
    with colbox1:
        html1 = ninebox(1, nineboxDatasUnidades(dadosbox), dadosbox, 'Em Andamento')
        st.write(f'<style>{ninebox_style}</style>', unsafe_allow_html=True)
        st.write(f'<div>{html1}</div>', unsafe_allow_html=True)    
            
    with colbox2:
        html1 = ninebox(0, nineboxDatasUnidades(dadosbox), dadosbox, 'Paralisado')
        st.write(f'<style>{ninebox_style}</style>', unsafe_allow_html=True)
        st.write(f'<div>{html1}</div>', unsafe_allow_html=True)
    
    st.text(' ')
    font_TITLE('ACOMPANHAMENTO POR PROJETO', fonte_Projeto,"'Bebas Neue', sans-serif", 30, 'left', '#228B22')
    with st.expander('Filtro Projetos', expanded=False):
        macropr_filter = st.multiselect('Macroprocesso', set([x[5] for x in ddPaging]), set([x[5] for x in ddPaging]))
        program_filter = st.multiselect('Programas', set([x[6] for x in ddPaging if x[5] in macropr_filter]), set([x[6] for x in ddPaging if x[5] in macropr_filter]))
        project_filter = st.selectbox('Projetos', [x[1] for x in ddPaging if x[6] in program_filter])
        
        dadosOrigin = [x for x in ddPaging if x[1] == project_filter]

        cmd_entregas_planejameto = f"""SELECT 
                                (SELECT number_sprint FROM projeu_sprints WHERE id_sprint = projeu_entregas_planejamento.id_sprint) AS NUMERO_SPRINT, 
                                nome_Entrega AS NOME_ENTREGA, 
                                (select Nome FROM projeu_users WHERE id_user = executor) AS EXECUTOR, 
                                hra_necess AS HORAS, 
                                compl_entrega AS COMPLEXIDADE,
                                stt_entrega AS STATUS,
                                id_entr,
                                id_sprint,
                                (SELECT Matricula FROM projeu_users WHERE id_user = executor) AS MATRICULA_EXECUTOR
                            FROM projeu_entregas_planejamento 
                                WHERE 
                                    id_sprint IN ( 
                                        SELECT id_sprint 
                                        FROM projeu_sprints 
                                        WHERE id_proj_fgkey = (
                                            SELECT id_proj 
                                            FROM projeu_projetos 
                                            WHERE name_proj LIKE '%{str(project_filter).strip()}%'
                                            ) 
                                        );"""

        cmd_entregas = f"""SELECT 
                                (SELECT number_sprint FROM projeu_sprints WHERE id_sprint = projeu_entregas.id_sprint) AS NUMERO_SPRINT, 
                                nome_Entrega AS NOME_ENTREGA, 
                                (select Nome FROM projeu_users WHERE id_user = executor) AS EXECUTOR, 
                                hra_necess AS HORAS, 
                                compl_entrega AS COMPLEXIDADE,
                                stt_entrega AS STATUS,
                                id_entr,
                                (
                                    SELECT 
                                        id_sprint 
                                    FROM 
                                        projeu_sprints 
                                    WHERE 
                                        id_sprint = projeu_entregas.id_sprint
                                ) AS ID_SPRINT,
                                (SELECT Matricula FROM projeu_users WHERE id_user = executor) AS MATRICULA_EXECUTOR
                            FROM projeu_entregas 
                                WHERE 
                                    id_sprint IN ( 
                                        SELECT id_sprint 
                                        FROM projeu_sprints 
                                        WHERE id_proj_fgkey = (
                                            SELECT id_proj 
                                            FROM projeu_projetos 
                                            WHERE name_proj LIKE '%{str(project_filter).strip()}%'
                                            ) 
                                        );"""
        
        cmd_observcao = f"""SELECT 
                                id_observ AS ID_OBSERVAÇÃO, 
                                id_sprint_fgkey AS ID_SPRINT, 
                                PS.number_sprint AS NUMBER_SPRINT, 
                                observacao AS TEXTO_OBSERVACAO, 
                                data_observ AS DATA_OBSERVACAO, 
                                (
                                    SELECT Nome FROM projeu_users WHERE id_user = ultm_edicao LIMIT 1
                                ) AS ULTIMA_EDICAO
                            FROM 
                                projeu_projt_observ 
                            JOIN 
                                projeu_sprints PS ON id_sprint = id_sprint_fgkey
                            WHERE 
                                PS.id_sprint IN ({dadosOrigin[0][27].replace('~/>', ',') if dadosOrigin[0][27] != None else 'null'});"""

        cmd_especialist_sprint = f"""SELECT
                                        PES.id_sp, 
                                        PES.id_sprt_fgkey, 
                                        PS.number_sprint,
                                        PES.id_colab_fgkey, 
                                        PU.Matricula,
                                        PU.Nome,
                                        PES.status_sp
                                    FROM projeu_especialist_sprint PES
                                    JOIN projeu_users PU ON PU.id_user = PES.id_colab_fgkey
                                    JOIN projeu_sprints PS ON PS.id_sprint = PES.id_sprt_fgkey
                                    WHERE PS.id_proj_fgkey IN (SELECT PP_AUX.id_proj FROM projeu_projetos PP_AUX WHERE PP_AUX.name_proj LIKE '%{str(dadosOrigin[0][1]).strip()}%');"""

    st.text(' ')
    st.text(' ')
    if len(dadosOrigin) > 0:
        #CONSULTADO ENTREGAS DO PLANEJAMENTO
        mycursor = conexao.cursor()
        mycursor.execute(cmd_entregas_planejameto)
        EntregasPlanjBD = mycursor.fetchall()

        #CONSULTANDO OS DADOS DAS ENTREGAS
        mycursor.execute(cmd_entregas)
        EntregasBD = mycursor.fetchall()
        
        #CONSULTANDO OS DADOS DE OBSERVAÇÕES
        mycursor.execute(cmd_observcao)
        ObservBD = mycursor.fetchall()
        
        #CONSULTANDO OS ESPECIALISTAS POR SPRINT
        mycursor.execute(cmd_especialist_sprint)
        especialist_by_proj = mycursor.fetchall()
        
        mycursor.close()


        tab1, tab2 = st.tabs(['Canvas', 'Editar'])
        with tab1:
            font_TITLE(f'{dadosOrigin[0][1]}', fonte_Projeto,"'Bebas Neue', sans-serif", 31, 'center', '#228B22')
            ########CANVAS DO PROJETO SELECIONADO########
            projetos = [dadosOrigin[0][1]] if dadosOrigin[0][1] != "None" else " "
            mvps = [dadosOrigin[0][7]] if dadosOrigin[0][7] != "None" else " "  
            investimentos = [f"{dadosOrigin[0][8]}"] if f"{dadosOrigin[0][8]}" != "None" else " "
            gestores = [f"{dadosOrigin[0][2]}"] if f"{dadosOrigin[0][2]}" != "None" else " "
            
            pessoas = str(dadosOrigin[0][21]).split("~/>") if dadosOrigin[0][21] != None else ''
            funcao = str(dadosOrigin[0][22]).split("~/>") if dadosOrigin[0][22] != None else ''
            equipBD = [[pessoas[x], funcao[x]] for x in range(len(pessoas))]

            resultados = []
            for i in range(len(dadosOrigin)):
                if dadosOrigin[i][9] != None:
                    resultados.append(f"{dadosOrigin[i][9]}")
                else:
                    resultados = " "
            
            if dadosOrigin[0][32] != None:
                entregas = [str(dadosOrigin[0][32]).split("~/>")[x] for x in range(len(str(dadosOrigin[0][40]).split("~/>"))) if str(str(dadosOrigin[0][40]).split("~/>")[x]).strip() == 'A']
            else:
                entregas = ''

            metricas = [str(dadosOrigin[0][33]).split("~/>")[x] for x in range(len(str(dadosOrigin[0][33]).split("~/>"))) if str(str(dadosOrigin[0][42]).split("~/>")[x]).strip() == 'A'] if dadosOrigin[0][33] != None else ''
            prodProjetos = str(dadosOrigin[0][10]).split("~/>") if dadosOrigin[0][10] != None else ""
            prodMvps = str(dadosOrigin[0][25]).split("~/>") if dadosOrigin[0][24] != None else ""

            
        #SEQUÊNCIA --> projetos, mvps, prodProjetos, prodMvps, resultados, metricas, gestores, especialistas, squads, entregas, investimentos
            canvas = PlotCanvas(projetos, mvps, prodProjetos, prodMvps, resultados, metricas, gestores, [x[0] for x in equipBD if x[1] == 'Especialista'], [x[0] for x in equipBD if x[1] == 'Executor'], entregas, investimentos)
            htmlRow = canvas.CreateHTML()
            htmlEqp = canvas.tableEqp()
            htmlUnic = canvas.tableUnic()
            htmlCol = canvas.tableCol()

            html = canvas.tableGeral(htmlRow, htmlEqp, htmlUnic, htmlCol)
            canvaStyle = canvas.cssStyle()

            st.write(f'<div>{html}</div>', unsafe_allow_html=True)
            st.write(f'<style>{canvaStyle}</style>', unsafe_allow_html=True)

        with tab2:
            def status_aux(sigla_status, func=0):
                dic_aux = {'A': 'Ativo',
                            'I': 'Inativo',
                            'E': 'Irregular'}
                
                if func == 0:
                    retorno = dic_aux[str(sigla_status).strip().upper()] if str(sigla_status).strip().upper() in list(dic_aux.keys()) else 'Irregular'
                else:
                    dic_invertido = {valor: chave for chave, valor in dic_aux.items()}
                    retorno = dic_invertido[str(sigla_status).strip()]
                
                return retorno

            font_TITLE(f'EDITAR CANVAS', fonte_Projeto,"'Bebas Neue', sans-serif", 24, 'left', 'black')
            nomeproj_edit = st.text_input('Nome Projeto', projetos[0])
            produtproj_edit = st.text_area('Produto Projeto', str(prodProjetos[0]).strip())
            mvp_edit = st.text_input('MVP', mvps[0])
            produtmvp_edit = st.text_input('Produto MVP', prodMvps[0])
            Resultado_edit = st.text_input('Resultado Esperado', resultados[0])
            
            ############################# MÉTRICAS #############################
            font_TITLE(f'MÉTRICAS', fonte_Projeto,"'Bebas Neue', sans-serif", 24, 'left', 'black')
            
            metricas_bd = [(str(dadosOrigin[0][41]).split("~/>")[x], str(dadosOrigin[0][33]).split("~/>")[x], str(dadosOrigin[0][42]).split("~/>")[x]) for x in range(len(str(dadosOrigin[0][41]).split("~/>"))) if str(dadosOrigin[0][41]).split("~/>")[x] != 'None']
            qntd_metrc_edit = st.number_input('Quantidade', key='qntd Métricas', min_value=0, step=1, value=len(metricas_bd))
            if qntd_metrc_edit > len(metricas_bd):
                metricas_bd.extend([(None, '', 'A') for x in range(qntd_metrc_edit - len(metricas_bd))])

            list_metric_edit = []
            if qntd_metrc_edit > 0:
                col1, col2 = st.columns([4,1])
                with col1:
                    st.caption('Métrica')
                with col2:
                    st.caption('Status')

                for idx_metr in range(qntd_metrc_edit):
                    with col1:
                        edit_metric_name = st.text_input('metricas_edit', value=metricas_bd[idx_metr][1], label_visibility='collapsed', key=f'edit metric {idx_metr}') 
                    with col2:
                        edit_metric_status = st.selectbox('status_edit', ['Ativo', 'Inativo', 'Irregular'], ['Ativo', 'Inativo', 'Irregular'].index(status_aux(str(metricas_bd[idx_metr][2]).strip())), label_visibility='collapsed', key=f'edit status {idx_metr}')
                    list_metric_edit.append([metricas_bd[idx_metr][0], edit_metric_name, edit_metric_status])
   
            ############################ ENTREGAS #############################
            st.text(' ')
            font_TITLE(f'PRINCIPAIS ENTREGAS', fonte_Projeto,"'Bebas Neue', sans-serif", 24, 'left', 'black')
            
            #ENTREGAS ORIGINAIS DO BANCO DE DADOS
            
            entregas_bd = [(str(dadosOrigin[0][39]).split("~/>")[x],  str(dadosOrigin[0][32]).split("~/>")[x], str(dadosOrigin[0][40]).split("~/>")[x]) for x in range(len(list(str(dadosOrigin[0][39]).split("~/>")))) if str(dadosOrigin[0][39]).split("~/>")[x] != None and str(dadosOrigin[0][39]).split("~/>")[x] != 'None']
            qntd_princ_edit = st.number_input('Quantidade', key='qntd Principais entregas', min_value=0, step=1, value=len(entregas_bd))
            entregas = list(entregas_bd)
            if qntd_princ_edit > len(entregas): #PEGANDO A QUANTIDADE DE VEZES A MAIS QUE O USUÁRIO SELECIONOU E ADCIONANDO NA MINHA LISTA
                entregas.extend([(None, '', 'A') for x in range(qntd_princ_edit - len(entregas))])
                
            list_entreg_edit = []
            if qntd_princ_edit > 0:
                
                col1, col2 = st.columns([4,1])
                with col1:
                    st.caption('Entrega')
                with col2:
                    st.caption('Status')

                for idx_princ_i in range(qntd_princ_edit):                        
                    with col1:
                        mome_edit = st.text_input('principais_edit', value=entregas[idx_princ_i][1], label_visibility='collapsed', key=f'edit principais entreg{idx_princ_i}')
                    with col2:
                        status_edit = st.selectbox('status_edit', ['Ativo', 'Inativo', 'Irregular'], ['Ativo', 'Inativo', 'Irregular'].index(status_aux(str(entregas[idx_princ_i][2]).strip())) ,label_visibility='collapsed', key=f'edit status entreg{idx_princ_i}')
                    list_entreg_edit.append((entregas[idx_princ_i][0], mome_edit, status_edit))

            list_metric_edit = [x for x in list_metric_edit if len(str(x[1]).strip()) > 0]
            list_entreg_edit = [x for x in list_entreg_edit if len(str(x[1]).strip()) > 0]
            edit_canv_button = st.button('Enviar')
            if edit_canv_button:
                mycursor_edit = conexao.cursor()
                ###################### FAZENDO A ATUALIZAÇÃO DAS INFORMAÇÕES GERAIS DO PROJETO ######################
                columns1 = ['name_proj', 'produto_entrega_final', 'nome_mvp', 'produto_mvp', 'result_esperad']
                values = [nomeproj_edit, produtproj_edit, mvp_edit, produtmvp_edit, Resultado_edit]
                values_aux = [projetos[0], str(prodProjetos[0]).strip(), mvps[0], prodMvps[0], resultados[0]]
                
                #LISTA range_aux VAI RETORNAR 1 ONDE O INDEX DOS VALORES FOR DIFERENTE DOS VALORES ANTIGOS
                #A IDEIA É DESCOBRIR EM QUAL INDEX ESTÁ O VALOR DIFERENTE E SOMENTE USAR O UPDATE ONDE DE FATO OUVER ALGUMA DIFERENÇA
                range_aux = [1 if str(values[x]).strip() != str(values_aux[x]).strip() else 0 for x in range(len(values))]
                for idx_clm in range(len(columns1)):
                    if range_aux[idx_clm] == 1:         
                        cmd = f'UPDATE projeu_projetos SET {columns1[idx_clm]} = "{values[idx_clm]}" WHERE id_proj = {dadosOrigin[0][0]};'
                        
                        mycursor_edit.execute(cmd)
                        conexao.commit()

                ###################### FAZENDO ATUALIZAÇÃO DAS PRINCIPAIS ENTREGAS DO PROJETO ######################
                for idx_entrg_edit in range(len(list_entreg_edit)):
                    if list_entreg_edit[idx_entrg_edit][0] == None:
                        cmd_insert_entrg = f'INSERT INTO projeu_princEntregas(entreg, id_proj_fgkey) VALUES ("{list_entreg_edit[idx_entrg_edit][1]}", {dadosOrigin[0][0]});'
                        mycursor_edit.execute(cmd_insert_entrg)
                        conexao.commit()

                    else:
                        id_entrg = list_entreg_edit[idx_entrg_edit][0]
                        entr_original = [x for x in entregas_bd if x[0] == id_entrg]
                        entr_editadad = [(x[0], x[1], status_aux(x[2], 1)) for x in list_entreg_edit if x[0] == id_entrg]
                        
                        if sum([1 if entr_original[x] != entr_editadad[x] else 0 for x in range(len(entr_original))]) > 0: #DESCOBRINDO SE HÁ ALGUMA DIFERENÇA ENTRE A LISTA ORIGINAL E A LISTA EDITADO
                            cmd_edit_entrg = f'UPDATE projeu_princEntregas SET entreg = "{entr_editadad[0][1]}", status_princp = "{entr_editadad[0][2]}" WHERE id_princ = {entr_editadad[0][0]};'
                            
                            mycursor_edit.execute(cmd_edit_entrg)
                            conexao.commit()
                
                ###################### FAZENDO ATUALIZAÇÃO DAS MÉTRICAS DO PROJETO ######################
                for idx_metric_edit in range(len(list_metric_edit)):
                    if list_metric_edit[idx_metric_edit][0] == None:
                        cmd_insert_metrc = f'INSERT INTO projeu_metricas (id_prj_fgkey, name_metric) VALUES ({dadosOrigin[0][0]} ,"{list_metric_edit[idx_metric_edit][1]}");'
                        
                        mycursor_edit.execute(cmd_insert_metrc)
                        conexao.commit()
                    
                    else:
                        id_metric = list_metric_edit[idx_metric_edit][0]
                        metric_original = [x for x in metricas_bd if x[0] == id_metric]
                        metric_editadad = [(x[0], x[1], status_aux(x[2], 1)) for x in list_metric_edit if x[0] == id_metric]
                        
                        if sum([1 if metric_original[x] != metric_editadad[x] else 0 for x in range(len(metric_original))]) > 0: #DESCOBRINDO SE HÁ ALGUMA DIFERENÇA ENTRE A LISTA ORIGINAL E A LISTA EDITADO
                            cmd_edit_metric = f'UPDATE projeu_metricas SET name_metric = "{metric_editadad[0][1]}", status_metric = "{metric_editadad[0][2]}" WHERE id_metric = {metric_editadad[0][0]};'
                            
                            mycursor_edit.execute(cmd_edit_metric)
                            conexao.commit()

                st.toast('Canvas Atualizado!', icon='✅') 
                mycursor_edit.close()
        ########APRESENTAÇÃO DOS DADOS DO PROJETO SELECIONADO########
        st.text(' ')
        st.text(' ')
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            displayInd('Status do Projeto', f'{dadosOrigin[0][31]}', 1, 3)
        with col2:
            displayInd('Progresso do Projeto', f'{50}%', 1, 3)
        with col3:
            displayInd('Sprint Atual', f'{len(str(dadosOrigin[0][11]).split("~/>"))}', 1, 3)
        with col4:
            displayInd('Total de Horas', f'{sum([int(x) for x in str(dadosOrigin[0][18]).split("~/>")]) if dadosOrigin[0][18] != None else 0}', 1, 3)

        st.text(' ')
        dados_control = [string_to_datetime(dadosOrigin[0][28]) if dadosOrigin[0][28] != None else None,  
                        string_to_datetime(dadosOrigin[0][29]) if dadosOrigin[0][29] != None else None, 
                        string_to_datetime(dadosOrigin[0][30]) if dadosOrigin[0][30] != None else None, 
                        dadosOrigin[0][31]]


        ################################## APRESENTAÇÃO DO GRÁFICO EM LINHA DO DESVIO EM DIAS ##################################
        dificuldade_proj = f'{dadosOrigin[0][36]} {dadosOrigin[0][37]}'
        type_proj = str(dadosOrigin[0][4]).strip()

        dat_inic_sprt = [datetime.strptime(str(x), "%Y-%m-%d").date() for x in list(str(dadosOrigin[0][13]).split("~/>"))]  if dadosOrigin[0][13] != None else [None]

        dat_fim_sprt = [datetime.strptime(str(x), "%Y-%m-%d").date() for x in list(str(dadosOrigin[0][14]).split("~/>"))]  if dadosOrigin[0][13] != None else [None]
        dat_homol = [datetime.strptime(str(x), "%Y-%m-%d").date() for x in list(str(dadosOrigin[0][43]).split("~/>"))]  if dadosOrigin[0][43] != None else [None]

        
        dif_desvio_sprints = [int((dat_inic_sprt[x + 1] - dat_fim_sprt[x]).days) if x < int(len(dat_inic_sprt)-1) else 0 for x in range(len(dat_fim_sprt))]
        dif_desvio_homolog = [int((dat_homol[x] - dat_fim_sprt[x]).days) if dat_homol[x] != None else 0 for x in range(len(dat_homol))]
        
        ########## PREPARAÇÃO DOS DADOS DO PROJETO ##########
                              #id_sprint                                                         number_sprint                      evento                                                       data_inicio_sprint                                                                                          id_proj                 nome_projeto
        dados_for_grafic_aux = [[list(str(dadosOrigin[0][27]).split('~/>'))[x], list(str(dadosOrigin[0][11]).split('~/>'))[x], list(str(dadosOrigin[0][12]).split("~/>"))[x], datetime.strptime(list(str(dadosOrigin[0][13]).split('~/>'))[x], "%Y-%m-%d").date() if dadosOrigin[0][13] != None else 0, dadosOrigin[0][0], str(dadosOrigin[0][1]).strip()] for x in range(len(list(str(dadosOrigin[0][11]).split('~/>'))))]

        dd_proj_grafic = {}
        for list_sprt in dados_for_grafic_aux:
            name_dic = f'SPRINT {str(list_sprt[2]).strip()} - {list_sprt[1]}' if str(list_sprt[2]).strip() not in ['MVP', 'ENTREGA FINAL'] else str(list_sprt[2]).strip()
            dd_proj_grafic[name_dic] = list_sprt[3]

        dd_proj_grafic = {} if list(dd_proj_grafic.values())[0] == 0 else dd_proj_grafic
        col1, col2 = st.columns([1, 3])
        with col1:
            displayInd('Desvio entre Sprints (Média)', round(sum([x for x in dif_desvio_sprints if x != None]) / len([x for x in dif_desvio_sprints if x != None]), 2), 1, 3,padding=1.7, id=2)
            displayInd('Desvio Sprint X Homologação (Média)', round(sum(dif_desvio_homolog) / len(dif_desvio_homolog), 2), 1, 3,padding=1.7, id=2)

        with col2:
            def fqntd_sprints_por_event(typ_proj, complexid):
                typ_proj = str(typ_proj).strip()
                complexid = str(complexid).strip().upper()
                
                eventos = ['SPRINT PRÉ MVP', 'MVP', 'SPRINT PÓS MVP', 'ENTREGA FINAL']
                
                sprints_proj = {event: sum([x[5] for x in param_premiosBD if x[1] == typ_proj and x[2] == complexid and str(x[3]).strip() == str(event).strip()]) for event in eventos}
                
                return sprints_proj


            def tratar_number_sprint():
                dic_aux = {}
                sprints_by_event = fqntd_sprints_por_event(type_proj, dificuldade_proj)
                cont_sprint = 0
                list_sprint = []
                for key, value in dict(sprints_by_event).items():
                    for sprt_aux in range(value):
                        cont_sprint += 1
                        list_sprint.append(cont_sprint)
                        
                    dic_aux[str(key).strip()] = list_sprint[-value:]

                return dic_aux


            def retornar_evento(number_sprint):
                sprints_and_events = tratar_number_sprint()
                spt_evet_user = {evt: sprts for evt, sprts in dict(sprints_and_events).items() if int(number_sprint) in sprts}

                return spt_evet_user


            def pausa_sprints(evento):
                pausa_by_evento = {'SPRINT PRÉ MVP': 20,
                                'MVP': 10,
                                'SPRINT PÓS MVP': 20,
                                'ENTREGA FINAL': 5}
                return pausa_by_evento[str(evento).strip().upper()]

            sprints_by_evnt = fqntd_sprints_por_event(type_proj, dificuldade_proj)

            inic_proj = datetime.strptime(list(str(dadosOrigin[0][13]).split("~/>"))[0], "%Y-%m-%d").date() if dadosOrigin[0][13] != None else datetime.strptime(list(str(dadosOrigin[0][29]).split("~/>"))[0], "%Y-%m-%d").date()
            
            PrazosProjOriginal = {}

            soma_aux = 0
            for key, values in sprints_by_evnt.items():
                for a in range(values):
                    
                    if key not in ['MVP', 'ENTREGA FINAL']:
                        soma_aux += 1
                        name_event = f'{key} - {soma_aux}'
                    else:
                        name_event = str(key).strip()
                        
                    PrazosProjOriginal[name_event] = inic_proj
                    
                    inic_proj += timedelta(days=pausa_sprints(key))

            linha1_x = list(PrazosProjOriginal.keys())
            linha1_y = list(PrazosProjOriginal.values())

            linha2_x = list(dd_proj_grafic.keys())
            linha2_y = list(dd_proj_grafic.values())

            fig = go.Figure()

            fig.add_trace(go.Scatter(x=linha1_x, y=linha1_y, mode='lines+markers', name='Ideal'))
            fig.add_trace(go.Scatter(x=linha2_x, y=linha2_y, mode='lines+markers', name=f'{str(dadosOrigin[0][1]).strip()}'))

            fig.update_layout(
                                    xaxis_title='Sprints',
                                    yaxis_title='Datas',
                                    title='Desvio do Projeto',
                                    legend=dict(x=0.2, y=1.15, orientation='h')
                                )

            fig.update_yaxes(tickformat='%y/%m/%d')

            st.plotly_chart(fig, use_container_width=True)

        st.text(' ')
        func_split = lambda x: x.split("~/>") if x is not None else [x]
        #ESPAÇO PARA MANIPULAR OS COLABORADORES VINCULADOS À AQUELE PROJETO
        with st.expander('Equipe do Projeto'):
            matriculasEQUIP = func_split(dadosOrigin[0][23])

            equipe_atual = {matriculasEQUIP[idx_mat]: [matriculasEQUIP[idx_mat], func_split(dadosOrigin[0][21])[idx_mat], func_split(dadosOrigin[0][22])[idx_mat],  func_split(dadosOrigin[0][20])[idx_mat]] for idx_mat in range(len(matriculasEQUIP)) if matriculasEQUIP[idx_mat] != str(dadosOrigin[0][3]).strip()}

            tab1, tab2 = st.tabs(['Adcionar', 'Excluir'])
            
            with tab1:
                col1, col2 = st.columns([3,1])
                with col2:
                    qntd_clb = st.number_input('Quantidade', min_value=0, step=1)
                
                for a in range(qntd_clb):
                    equipe_atual[f'{a}'] = [None, None, 'Executor']        

                with st.form('FORMS ATUALIZAR EQUIPE'):
                        
                    col_equip1, col_equip2, col_equip3 = st.columns([0.3, 2, 1])
                    with col_equip1:
                        st.caption('Matricula')
                    with col_equip2:
                        st.caption('Colaboradores')
                    with col_equip3:
                        st.caption('Função')

                    list_colbs = []
                    equipe_list = [x for x in equipe_atual.values()]

                    for colb_a in range(len(equipe_list)):
                        with col_equip2:
                            colb_name = st.selectbox('Colaboradores', [x[1] for x in users], list([x[1] for x in users]).index(equipe_list[colb_a][1]) if equipe_list[colb_a][0] != None else None,label_visibility="collapsed", key=f'Nome Colab{colb_a}')        
                        with col_equip1:
                            colab_matric = st.text_input('Matricula', list(set([x[0] for x in users if x[1] == colb_name]))[0] if colb_name != None else None, label_visibility="collapsed", disabled=True, key=f'MatriculaColabs{colb_a}')
                        with col_equip3:
                            colb_funç = st.selectbox('Função', ['Especialista', 'Executor'],list(['Especialista', 'Executor']).index(equipe_list[colb_a][2]) if colb_name != None else None, label_visibility="collapsed", key=f'funcaoColab{colb_a}')
                        list_colbs.append([colab_matric, colb_funç])
                    
                    button_att_equipe = st.form_submit_button('Atualizar')
                    if button_att_equipe:
                        equipe_limp = [x for x in list_colbs if str(x[0]).strip() != '0']
                        mycursor = conexao.cursor()

                        for matric, func in equipe_limp:
                            if str(matric).strip() in [str(x).strip() for x in equipe_atual.keys()]: #VERIFICANDO SE O COLABORADOR JÁ ESTÁ VINCULADO A EQUIPE
                                if str(equipe_atual[matric][2]).strip() != str(func).strip(): #VERIFICANDO SE OUVE ALGUMA MUDANÇA NOS COLABORADORES JÁ VINCULADOS
                                    cmd_att_equipe = f'UPDATE projeu_registroequipe SET papel = "{func}" WHERE id_registro = {equipe_atual[matric][3]}'
                                    mycursor.execute(cmd_att_equipe)
                                    conexao.commit()
                            else: #SE FOR UM COLABORADOR NOVO NA EQUIPE
                                cmd_new_equip = f'''INSERT INTO projeu_registroequipe(id_projeto, id_colab, papel)
                                                VALUES (
                                                    {dadosOrigin[0][0]}, 
                                                    (SELECT id_user FROM projeu_users WHERE Matricula = {matric}), 
                                                    '{func}');'''
                                mycursor.execute(cmd_new_equip)
                                conexao.commit()
                            
                        mycursor.close()
                        st.toast('Equipe Atualizada!', icon='✅') 
            with tab2:                
                font_TITLE('EXCLUIR COLABORADOR DA EQUIPE', fonte_Projeto,"'Bebas Neue', sans-serif", 25, 'left')

                if len(equipe_atual) > 0:
                
                    st.text(' ')
                    col1, col2, col3 = st.columns([0.6,3,2])
                    with col2:
                        colab_ex = st.selectbox('Colaborador', [str(x[1]).strip() for x in equipe_atual.values()])                
                    with col1:
                        matric_ex = st.text_input('Matricula', [x[0] for x in users if str(x[1]).strip().lower() == str(colab_ex).strip().lower()][0], disabled=True)
                    with col3:
                        funca_ex = st.text_input('Função', equipe_atual[matric_ex][2], disabled=True)

                    button_ex_equip = st.button('Excluir', key='EXCLUIR COLABORADOR DO PROJETO')
                    if button_ex_equip:
                        mycursor = conexao.cursor()
                        cmd_ex_equip = f'UPDATE projeu_registroequipe SET status_reg = "I" WHERE id_registro = {equipe_atual[matric_ex][3]};'

                        mycursor.execute(cmd_ex_equip)
                        conexao.commit()

                else:
                    st.error('Não há colaboradores vinculados a equipe do projeto.', icon='❌')
                
            
        with st.expander('Controle do Projeto', expanded=False): 
            
            font_TITLE('DATAS', fonte_Projeto,"'Bebas Neue', sans-serif", 26, 'left')  
            dt_aprov = st.date_input('Aprovação do Projeto', dados_control[0])
            dt_poss_gtr = st.date_input('Posse do Gestor', dados_control[1])
            dt_ims_sqd = st.date_input('Imersão Squad', dados_control[2])
            
            st.text(' ')
            font_TITLE('STATUS PROJETO', fonte_Projeto,"'Bebas Neue', sans-serif", 26, 'left')
            opc_stt = ['Aguardando Início', 'Em Andamento', 'Concluído', 'Paralisado', 'Cancelado']
            stt_proj = st.selectbox('stt', opc_stt, opc_stt.index(str(dados_control[3]).strip()), label_visibility='collapsed')

            st.text(' ')
            btt_control_proj = st.button('Atualizar', key='btt_control_proj')
            if btt_control_proj:
                try:
                    mycursor = conexao.cursor()
                    columns_control = ['date_aprov_proj', 'date_posse_gestor', 'date_imersao_squad', 'status_proj']
                    values_control = [dt_aprov, dt_poss_gtr, dt_ims_sqd, stt_proj]

                    for idx_control in range(len(columns_control)):
                        if values_control[idx_control] != None:
                            cmd_up_control_proj = f'UPDATE projeu_projetos SET {columns_control[idx_control]} = "{values_control[idx_control]}" WHERE id_proj = 1;'
                            mycursor.execute(cmd_up_control_proj)
                            conexao.commit()
                    
                    mycursor.close()
                    st.toast('Dados Atualizados!', icon='✅')

                except:
                    st.toast('Erro ao atualizar dados de controle do projeto.', icon='❌')

        param_sprint = ['PRÉ MVP', 'MVP', 'PÓS MVP', 'ENTREGA FINAL']
        font_TITLE('SPRINTS DO PROJETO', fonte_Projeto,"'Bebas Neue', sans-serif", 28, 'left', '#228B22')
        with st.expander('Adcionar Sprint'):
            #FUNÇÃO PARA IDENTIFICAR SE A COLUNA DO BANCO DE DADOS ESTÁ VAZIA 
            maior_idx = max([param_sprint.index(x)+1 if x != None else 0 for x in func_split(dadosOrigin[0][12])])
 
            if None in func_split(dadosOrigin[0][11]):
                on_ex = False
            else:    
                on_ex = st.toggle('Excluir sprint')

            listAddSprOF_EX = [max([int(x) for x in func_split(dadosOrigin[0][11]) if x != None]) if len([int(x) for x in func_split(dadosOrigin[0][11]) if x != None]) != 0 else 0, param_sprint[:maior_idx+1], datetime.today()]
            
            listAddSprON_EX = [[int(x) if x != None else '' for x in func_split(dadosOrigin[0][11])], func_split(dadosOrigin[0][12]), [string_to_datetime(x) if x != None and x != " " else datetime.today() for x in func_split(dadosOrigin[0][13])]]

            disabledON = True if on_ex else False
            disabledOF = False if on_ex else True

            col0, col1, col2, col3 = st.columns([0.5,3,1,1])
            with col1:
                type_sprint_new = st.selectbox('Tipo', [listAddSprON_EX[1][listAddSprON_EX[0].index(max(listAddSprON_EX[0]))]] if on_ex else listAddSprOF_EX[1], disabled=disabledON)
            with col0:
                number_sprt =listAddSprOF_EX[0] + 1 if type_sprint_new != 'MVP' else None
                number_sprint_new = st.text_input('Sprint', max(listAddSprON_EX[0]) if on_ex else number_sprt, disabled=True)

            with col2:
                dat_inc_new = st.date_input('Início', value=listAddSprON_EX[2][listAddSprON_EX[0].index(max(listAddSprON_EX[0]))] if on_ex else listAddSprOF_EX[2], disabled=disabledON)
            with col3:
                dat_fim_new = st.date_input('Fim', value=dat_inc_new + timedelta(days=14), disabled=True)

            colAdd, colExc = st.columns([1,7])
            with colAdd:
                button_addSprint = st.button('Adcionar Sprint', disabled=disabledON)
            with colExc:
                button_exSprint = st.button('Excluir Sprint', disabled=disabledOF)
            
            if button_addSprint:
                mycursor = conexao.cursor()
                columns = 'id_proj_fgkey, status_sprint, date_inic_sp, date_fim_sp'
                values = f'''(SELECT id_proj FROM projeu_projetos WHERE name_proj LIKE '%{str(project_filter).strip()}%'), '{type_sprint_new}', STR_TO_DATE('{dat_inc_new}', '%Y-%m-%d'), STR_TO_DATE('{dat_fim_new}', '%Y-%m-%d')'''
                
                if number_sprint_new != None:
                    columns += ', number_sprint'
                    values += f', {number_sprint_new}'

                cmd_addSprint = f'''INSERT INTO projeu_sprints({columns}) 
                VALUES ({values});'''
                
                mycursor.execute(cmd_addSprint)
                conexao.commit()
                
                if number_sprint_new == 1:
                    cmdUP_stt_proj = f'UPDATE projeu_projetos SET status_proj = "Em Andamento" WHERE id_proj = {dadosOrigin[0][0]};'
                    mycursor.execute(cmdUP_stt_proj)
                    conexao.commit()
                    
                mycursor.close()
                st.toast('Sucesso na adição da sprint!', icon='✅')
                st.text(' ')
                

            if button_exSprint:
                NotEntrg = False
                if on_ex:
                    mycursor = conexao.cursor()

                    #CHECANDO SE HÁ ENTREGAS VINCULADAS A SPRINT
                    if len(EntregasBD) == 0:
                        NotEntrg = True
                    else:
                        NotEntrg = True if number_sprint_new not in list(set([x[0] for x in EntregasBD])) else False
                    
                    if NotEntrg:
                        cmdDEL = f'''DELETE FROM projeu_sprints 
                                    WHERE number_sprint = {listAddSprOF_EX[0]} 
                                    AND id_proj_fgkey = (SELECT id_proj FROM projeu_projetos 
                                        WHERE name_proj LIKE '%{str(project_filter).strip()}%') 
                                    AND status_sprint = '{type_sprint_new}'
                                    AND date_inic_sp = STR_TO_DATE('{dat_inc_new}', '%Y-%m-%d')
                                    AND date_fim_sp = STR_TO_DATE('{dat_fim_new}', '%Y-%m-%d');'''                

                        mycursor.execute(cmdDEL)
                        conexao.commit()

                        mycursor.close()
                        st.toast('Excluido!', icon='✅') 

                        sleep(1.5)
                        # st.rerun()
                    else:
                        st.toast('Primeiramente, é necessário excluir todas as atividades dessa sprint.', icon='❌')
                else:
                    st.toast('Primeiramente, ative a opção de excluir sprint.', icon='❌')

        func_split = lambda x: x.split("~/>") if x is not None else [x]
        if func_split(dadosOrigin[0][11])[0] != None:
            # ----> DADOS [NUMBER_SPRINT, STATUS_SPRINT,  DATA INC SPRINT, DATA FIM SPRINT, ID_SPRINT, CHECK_SPRINT]
            sprints = [[func_split(dadosOrigin[0][11])[x], func_split(dadosOrigin[0][12])[x], func_split(dadosOrigin[0][13])[x], func_split(dadosOrigin[0][14])[x], func_split(dadosOrigin[0][27])[x], func_split(dadosOrigin[0][34])[x]] for x in range(len(func_split(dadosOrigin[0][11])))]

            for idx_parm in range(len(param_sprint)):
                #INFORMAÇÕES DAS SPRINTS DAQUELE EVENTO
                ddSprint = [sprints[x] for x in range(len(sprints)) if str(sprints[x][1]) == str(param_sprint[idx_parm])] #DESCOBRINDO QUAL A SPRINT DAQUELE STATUS

                #FUNÇÃO PARA LIMPAR AS ENTREGAS DAQUELA SPRINT
                # ----> DADOS [NUMBER_SPRINT, NOME_ENTREGA, EXECUTOR, HORAS, COMPLEXIDADE, STATUS]
                SpritNotEntreg = [[int(sprt[0]), None, None, 0 , '---', '🟨 Backlog', None, int(sprt[1])] for sprt in [[i[0], i[4]] for i in ddSprint] if sprt not in list(set([ab_x[0] for ab_x in EntregasBD]))]
                
                SprintsEntregs = [list(x) for x in EntregasBD if str(x[0]) in [str(i[0]) for i in ddSprint]]
                SprintsEntregs.extend(SpritNotEntreg)

                SprintsEntregsPlan = [list(x) for x in EntregasPlanjBD if str(x[0]) in [str(i[0]) for i in ddSprint]]

                cont_sprint = 0 
                if len(ddSprint)> 0:
                    font_TITLE(f'{param_sprint[idx_parm]}', fonte_Projeto,"'Bebas Neue', sans-serif", 25, 'left')

                                                    #COLOCANDO EM ORDEM CRESCENTE AS SPRINTS
                    for idx_spr_tupl in sorted(list(set([(x[7], x[0]) for x in SprintsEntregs])), key=lambda x: x[1]):
                        idx_spr = idx_spr_tupl[0]
                        listDadosAux = []
                        cont_sprint += 1

                        name_expander = f'Sprint {int(ddSprint[[x[4] for x in ddSprint].index(str(idx_spr))][0])}' if param_sprint[idx_parm] != 'MVP' else 'Evento - MVP'
                        with st.expander(name_expander):
                            id_sprint = idx_spr

                            #FILTRANDO ENTREGAS DAQUELA SPRINT

                            spEntregas = [x for x in SprintsEntregs if x[7] == idx_spr]

                            spEntregasPlan = [x for x in SprintsEntregsPlan if x[8] == idx_spr]

                            block_sprint = True if str(ddSprint[list(x[4] for x in ddSprint).index(str(id_sprint))][5]) == str(0) else False

                            #PREPARANDO OS DADOS PARA APRESENTAR NO CARD DA SPRINT
                            contagem_dif = Counter([x[4] for x in spEntregas])                
                            dif_comum = contagem_dif.most_common(1)
                            
                            porc_avan = f'{int((len([x for x in spEntregas if str(x[5]).strip() == "🟩 Concluído"]) / len([x for x in spEntregas if x[1] != None])) * 100) if len([x for x in spEntregas if x[1] != None]) > 0 else 0}%'           
                            cardGRANDE(['Colaboradores', 'Atividades', 'Entregues', 'Avanço', 'Horas', 'Complexidade'], [len(list(set([x[2] for x in spEntregas if x[2] != None]))), len([x for x in spEntregas if x[1] != None]), len([x for x in spEntregas if str(x[5]).strip() == '🟩 Concluído']), porc_avan, sum([x[3] for x in spEntregas]), mapear_dificuldade(dif_comum[0][0])])
                            st.text(' ')

                            st.text(' ')
                            colPROJ1, colPROJ2 = st.columns([2,1])
                            with colPROJ1:
                                font_TITLE('ENTREGAS', fonte_Projeto,"'Bebas Neue', sans-serif", 25, 'left','#228B22')
                            with colPROJ2:
                                font_TITLE('STATUS DO PROJETO - EM ANDAMENTO', fonte_Projeto,"'Bebas Neue', sans-serif", 25, 'left','#228B22')

                            especialistBD_sprint = [x for x in especialist_by_proj if str(x[1]) == str(id_sprint)]  #ESPECIALISTAS ATIVOS E NÃO ATIVOS VINCULADOS A SPRINT                        
                            
                            especialist_proj = [list(func_split(dadosOrigin[0][21]))[x] for x in range(len(func_split(dadosOrigin[0][22]))) if str(list(func_split(dadosOrigin[0][22]))[x]).upper() == 'ESPECIALISTA']
                            
                            especialist_opc = especialist_proj if len(especialistBD_sprint) == 0 else [str(x[5]).strip() for x in especialistBD_sprint if str(x[6]).strip() == 'A']
               
                            especialist_sprint = st.multiselect('Especialistas', list(set(especialist_proj)), list(set(especialist_opc)), key=f'especialista multi{idx_spr}')
                            
                            def tratamento_especialist():
                                for espec_bd in especialist_proj:
                                    espec_bd = str(espec_bd).strip()
                                    dd_espec = {matric: lista for matric, lista in dict(equipe_atual).items() if str(lista[1]).strip() == str(espec_bd)} 
                                    
                                    matricula_especil = str(list(dict(dd_espec).keys())[0]).strip()

                                    cmd_aux = None
                                    matric_all_espc = [str(x[4]) for x in especialistBD_sprint] #MATRICULA DE TODOS OS ESPECIALISTAS VINCULADOS A SPRINT
                                    
                                    if matricula_especil not in matric_all_espc and espec_bd in [str(x).strip() for x in especialist_sprint]: #SE SIM, NOVO ESPECIALISTA
                                        cmd_aux = f'''
                                                INSERT INTO projeu_especialist_sprint (
                                                    id_sprt_fgkey, 
                                                    id_colab_fgkey
                                                ) VALUES (
                                                    {id_sprint}, 
                                                    (SELECT id_user FROM projeu_users WHERE Matricula = {matricula_especil}));'''
                                                            
                                    else: #ESTÁ VINCULADO A SPRINT DO PROJETO
                                        if espec_bd in [str(x).strip() for x in especialist_sprint] and especialistBD_sprint[0][6] == 'I': #FOI SELECIONADO
                                            cmd_aux = f'''
                                                        UPDATE 
                                                            projeu_especialist_sprint SET status_sp = "A" 
                                                        WHERE 
                                                            id_colab_fgkey = (SELECT id_user FROM projeu_users WHERE Matricula = {matricula_especil}) 
                                                                AND id_sprt_fgkey = {id_sprint};'''
                                        
                                        elif espec_bd not in [str(x).strip() for x in especialist_sprint] and especialistBD_sprint[0][6] == 'A': #FOI RETIRADO
                                            cmd_aux = f'''
                                                        UPDATE 
                                                            projeu_especialist_sprint SET status_sp = "I" 
                                                        WHERE 
                                                            id_colab_fgkey = (SELECT id_user FROM projeu_users WHERE Matricula = {matricula_especil}) 
                                                                AND id_sprt_fgkey = {id_sprint};'''
                                    #cmd_aux=''
                                    return cmd_aux
                                

                            st.text(' ')
                            spEntregas = [x for x in spEntregas if x[1] != None and x[2] != None and x[3] != None]
                            
                            tab1, tab2, tab3, tab4 = st.tabs(['Entregas', 'Excluir', 'Homologação', 'Observação'])
                            with tab1:
                                #FORMULÁRIO APRESENTANDO AS ENTREGAS
                                col1, col2, col3 = st.columns([3,1,1])
                                qnt_att = st.number_input('Adcionar Atividade', min_value=0, step=1, key=f'add{idx_spr} - {idx_parm}')
                                
                                spEntregas.extend([[idx_spr, None, None, 0 , '---', '🟨 Backlog', None] for x in range(qnt_att)])

                                if len(spEntregas) > 0:
                                    with st.form(f'Formulário Entregas {idx_parm} - {id_sprint}'):
                                        st.text(' ')
                                        
                                        for ativIDX in range(len(spEntregas)): 
                                            col1, col2, col4 = st.columns([0.6, 0.3, 0.12])
                                            with col1:
                                                st.caption(f'Entrega {ativIDX+1}')
                                            with col2:
                                                st.caption('Status | Executor')
                                            with col4:
                                                st.caption('Hr | Compl')
                                            with col1:
                                                name_entreg = st.text_area('Atividade', spEntregas[ativIDX][1] if spEntregas[ativIDX][1] != None else '', key=f'atividade{idx_spr} - {ativIDX} - {idx_parm}', disabled=False, label_visibility="collapsed")
                                            with col4:
                                                horas_entreg = st.number_input('Horas', value=spEntregas[ativIDX][3],min_value=0, step=1, key=f'horas{idx_spr} - {ativIDX} - {idx_parm}',disabled=block_sprint, label_visibility="collapsed")

                                                opc_compl = ['Fácil', 'Médio', 'Difícil']

                                                compl_entreg = st.selectbox('Compl.', opc_compl, opc_compl.index(spEntregas[ativIDX][4]) if spEntregas[ativIDX][4] != None and spEntregas[ativIDX][4] != '---' else 0, key=f'complex{idx_spr}  - {idx_parm}- {ativIDX}', disabled=block_sprint, label_visibility="collapsed")

                                            with col2:
                                                opc_stt = ['🟨 Backlog', '🟥 Impeditivo', '🟦 Executando',  '🟩 Concluído']
                                                status_entreg = st.selectbox('Status', opc_stt, opc_stt.index(str(spEntregas[ativIDX][5]).strip()) if spEntregas[ativIDX][5] != None and spEntregas[ativIDX][5] != '' else 0, key=f'status{idx_spr}  - {idx_parm} - {ativIDX}', disabled=block_sprint, label_visibility="collapsed")
                                                opc_colb = func_split(dadosOrigin[0][21])
                                                colab_entreg = st.selectbox('Colaborador', opc_colb, opc_colb.index(spEntregas[ativIDX][2]) if spEntregas[ativIDX][2] != None and spEntregas[ativIDX][2] != '' else 0, key=f'colab{idx_spr} - {ativIDX} - {idx_parm}',disabled=block_sprint, label_visibility="collapsed")

                                            listDadosAux.append([name_entreg, colab_entreg, horas_entreg, status_entreg, compl_entreg, spEntregas[ativIDX][6]]) 
                                        
                                        listDadosAux = [x for x in listDadosAux if x[0] != '' and x[0] != None]
                                        entrgasBD_by_sprint = [x for x in EntregasBD if str(x[7]).strip() == str(idx_spr).strip()]


                                        limp_entrg = lambda entr: str(entr).strip().replace('"', "'")
                                        if len(entrgasBD_by_sprint) > 0:
                                            col1, col2, col3 = st.columns([1,3,7])
                                            with col1:
                                                button_atual = st.form_submit_button('Atualizar', disabled=block_sprint)        
                                            with col2:
                                                button_final = st.form_submit_button('Finalizar Sprint', disabled=block_sprint) 
                                        
                                                if button_final:
                                                    mycursor = conexao.cursor()
                                                    columns_final = ['check_sprint', 'data_check']
                                                    values_final = [0, f'"{datetime.today()}"']

                                                    for idx_column in range(len(columns_final)):
                                                        cmd_final = f'''UPDATE projeu_sprints SET {columns_final[idx_column]} = {values_final[idx_column]} WHERE id_sprint = {int(id_sprint)};'''
                                                        mycursor.execute(cmd_final)
                                                        conexao.commit()

                                                    mycursor.close()
                                                    st.toast('Sprint Finalizada!', icon='✅')

                                            if button_atual:
                                                mycursor = conexao.cursor()

                                                for list_atual in listDadosAux:
                                                    if list_atual[5] != None: #SE A ENTREGA DA "list_atual" JÁ ESTIVER DENTRO DO BANCO DE DADOS SOMENTE VAI ATUALIZAR AS INFORMAÇÕES SOBRE A ENTREGA
                                                        columnsUP = ['nome_Entrega', 'executor', 'hra_necess', 'stt_entrega', 'compl_entrega']

                                                        for idxColum in range(len(columnsUP)):
                                                            cmd_update = f'''UPDATE projeu_entregas SET {columnsUP[idxColum]} = {f'"{list_atual[idxColum]}"' if idxColum != 1 else f'(SELECT id_user FROM projeu_users WHERE Nome = "{list_atual[idxColum]}" LIMIT 1)'} WHERE id_entr = {list_atual[5]};'''
                                                            mycursor.execute(cmd_update)
                                                            conexao.commit()


                                                    else: #INSERT DA ENTREGA CASO ELA NÃO ESTEJA PRESENTE DENTRO DO BANCO DE DADOS
                                                        if list_atual[0] != None and list_atual[0] != '': 
                                                            tables = ['projeu_entregas', 'projeu_entregas_planejamento']

                                                            for table_name in tables:
                                                                cmd_insert = f'''
                                                                    INSERT INTO {table_name} (id_sprint, nome_Entrega, executor, hra_necess, stt_entrega, compl_entrega) 
                                                                        values((SELECT id_sprint FROM projeu_sprints WHERE number_sprint = {spEntregas[0][0]}  
                                                                            AND id_proj_fgkey = 
                                                                                (SELECT id_proj FROM projeu_projetos WHERE name_proj = '{dadosOrigin[0][1]}') LIMIT 1),
                                                                                "{limp_entrg(list_atual[0])}", 
                                                                                (SELECT id_user FROM projeu_users WHERE Nome = '{list_atual[1]}' LIMIT 1),
                                                                                {list_atual[2]},
                                                                                "{list_atual[3]}",
                                                                                "{list_atual[4]}");'''
                                                                mycursor.execute(cmd_insert)
                                                                conexao.commit()

                                                    cmd_especialist = tratamento_especialist()
                                                    mycursor.execute(cmd_especialist)
                                                    conexao.commit()

                                                mycursor.close()
                                                st.toast('Dados Atualizados!', icon='✅')

                                        else:
                                            button_inic_entreg = st.form_submit_button('Enviar')
                                            if button_inic_entreg:
                                                mycursor = conexao.cursor()
                                                tables = ['projeu_entregas', 'projeu_entregas_planejamento']

                                                for table_name in tables:
                                                    for list_atual in listDadosAux:
                                                        cmd_insert = f'''
                                                            INSERT INTO {table_name} (id_sprint, nome_Entrega, executor, hra_necess, stt_entrega, compl_entrega) 
                                                                 values({spEntregas[0][0]},
                                                                        "{limp_entrg(list_atual[0])}", 
                                                                        (SELECT id_user FROM projeu_users WHERE Nome = '{list_atual[1]}' LIMIT 1),
                                                                        {list_atual[2]},
                                                                        "{list_atual[3]}",
                                                                        "{list_atual[4]}");'''

                                                        mycursor.execute(cmd_insert)
                                                        conexao.commit()

                                                for i in range(len(especialist_sprint)):
                                                    cmd_insert_espc = f"""INSERT INTO projeu_especialist_sprint (
                                                                            id_sprt_fgkey, 
                                                                            id_colab_fgkey
                                                                        ) VALUES (
                                                                            {id_sprint}, 
                                                                            (SELECT id_user FROM projeu_users WHERE Nome LIKE '%{str(especialist_sprint[i]).strip()}%'));"""
                                                    
                                                    mycursor.execute(cmd_insert_espc)
                                                    conexao.commit()

                                                st.toast('Entregas Enviadas!', icon='✅')
                                                mycursor.close()

                            with tab2:
                                if len(spEntregas) > 0:
                                    font_TITLE('EXCLUIR', fonte_Projeto,"'Bebas Neue', sans-serif", 26, 'left')
                                
                                    atvdd_exc = st.selectbox('Atividade', [x[1] for x in spEntregas if x[1] != None and x[1] != ' '], key=f'NameExAtivid {idx_spr} - {idx_parm}')

                                    col_sel0, col_sel1, col_sel2, col_sel3 = st.columns([3,1,1,1])
                                    with col_sel0:
                                        exec_exc = st.text_input('Executor', value=f'{[x[2] for x in spEntregas if x[1] == atvdd_exc][0]}', disabled=True, key=f'ExcutExAtivid {idx_spr} - {idx_parm}')
                                    with col_sel1:
                                        compl_exc = st.text_input('Complexidade', value=[x[4] for x in spEntregas if x[1] == atvdd_exc and str(x[2]) == str(exec_exc)][0], disabled=True, key=f'ComplexidadeExAtivid {idx_spr} - {idx_parm}')
                                    with col_sel2:
                                        hrs_exc = st.text_input('Horas', value=[x[3] for x in spEntregas if x[1] == atvdd_exc and str(x[2]) == str(exec_exc)][0], disabled=True, key=f'HorsExAtivid {idx_spr} - {idx_parm}')
                                    with col_sel3:
                                        stt_exc = st.text_input('Status', value=[x[5] for x in spEntregas if x[1] == atvdd_exc and str(x[2]) == str(exec_exc)][0], disabled=True, key=f'StatusExAtivid {idx_spr} - {idx_parm}')
                                    
                                    buttonEX = st.button('Excluir', key=f'Excluir{idx_spr} - {idx_parm}')

                                    id_entr = [x[6] for x in spEntregas if str(x[1]).strip().lower() == str(atvdd_exc).strip().lower() and str(x[3]).strip() == str(hrs_exc).strip() and x[1] != None and x[1] != ' ']
                                    if buttonEX:
                                        if len(id_entr) > 0:
                                            mycursor = conexao.cursor()
                                            cmd_exc = f"""DELETE FROM projeu_entregas 
                                                        WHERE 
                                                            nome_entrega = '{atvdd_exc}' 
                                                            AND executor = (SELECT id_user FROM projeu_users WHERE Nome = '{exec_exc}' LIMIT 1)
                                                            AND compl_entrega = '{compl_exc}'
                                                            AND stt_entrega = '{stt_exc}';"""

                                            mycursor.execute(cmd_exc)
                                            conexao.commit()

                                            st.toast('Entrega Excluida!', icon='✅')
                                            mycursor.close()
                  
                                        else:
                                            st.toast('Entrega não encontrada no banco de dados!', icon='❌')

                            with tab3:
                                font_TITLE('HOMOLOGAÇÃO', fonte_Projeto, "'Bebas Neue', sans-serif", 26, 'left')
                                col1, col2, col3 = st.columns([2, 1, 1])
                                with col1:
                                    st.caption('Tipo de Homologação')
                                    type_homol = st.selectbox('Tipo de Homologação',
                                                              [param_sprint[idx_parm]], label_visibility="collapsed",
                                                              key=f' - {idx_spr} typHomo')
                                with col2:
                                    st.caption('Data Homologação')
                                    date_homol = st.date_input('Fím Sprint', label_visibility="collapsed",
                                                               key=f'Homo_sprint{idx_spr}')
                                with col3:
                                    st.caption('Status Homologação')
                                    stt_homol = st.selectbox('Fím Sprint', ['PARA AGENDAR', 'AGUARDANDO HOMOLOGAÇÃO',
                                                                            'HOMOLOGADO COM AJUSTES', 'HOMOLOGADO',
                                                                            'NÃO HOMOLOGADO'],
                                                             label_visibility="collapsed", key=f'status_homo{idx_spr}')
                                
                                st.caption('Parecer Homologação')
                                parec_homol = st.text_area('Planejamento Sprint', label_visibility="collapsed",
                                                           key=f'parec_homol{idx_spr}')
                                
                            
                                status_homolog = [func_split(dadosOrigin[0][15])[x] for x in range(len(func_split(dadosOrigin[0][11]))) if str(func_split(dadosOrigin[0][27])[x]) == str(id_sprint)][0]

                                btt_homo = st.button('Enviar', key=f'btt homolog {idx_spr}', disabled=True if str(status_homolog).strip() == 'HOMOLOGADO' else False)
                                
                                if btt_homo:
                                    if len(parec_homol) > 0:
                                        if dadosOrigin[0][36] != None and dadosOrigin[0][37] != None and len(dadosOrigin[0][36]) > 0 and len(dadosOrigin[0][37]) > 0:
                                            try:
                                                def trat_homol(name_hmo):
                                                    aux_dic = {'PRÉ MVP' : 'SPRINT PRÉ MVP',
                                                            'PÓS MVP': 'SPRINT PÓS MVP',
                                                            'MVP': 'MVP',
                                                            'ENTREGA FINAL': 'ENTREGA FINAL'}
                                                    
                                                    retorno = aux_dic[str(name_hmo).strip().upper()]
                                                    if str(dadosOrigin[0][38]) == '1':
                                                        retorno = 'ENTREGA FINAL'

                                                    return retorno
                                                
                                                type_homol = trat_homol(type_homol)
                                                
                                                cont_erro = 0
                                                mycursor1 = conexao.cursor()
                                                columns = ['tip_homolog', 'date_homolog', 'status_homolog',
                                                            'parecer_homolog']
                                                
                                                values = [f'"{type_homol}"', f'STR_TO_DATE("{date_homol}", "%Y-%m-%d")',
                                                            f'"{stt_homol}"', f'"{parec_homol}"']
                                                
                                                for idx_clm in range(len(columns)):
                                                    cmdHOMO = f'UPDATE projeu_sprints SET {columns[idx_clm]} = {values[idx_clm]} WHERE id_sprint = {ddSprint[cont_sprint - 1][4]};'
                                                    
                                                    mycursor1.execute(cmdHOMO)
                                                    conexao.commit()

                                                if str(stt_homol).strip() in ['HOMOLOGADO COM AJUSTES', 'HOMOLOGADO']:
                                                    
                                                    if str(ddSprint[list([x[4] for x in ddSprint]).index(str(id_sprint))][5]) == str(0):   
    
                                                        premio_aux = CalculoPrêmio(
                                                            str(project_filter).strip(),
                                                            str(f'{dadosOrigin[0][36]} {dadosOrigin[0][37]}').upper(), dadosOrigin[0][4])
    
                                                        valores = premio_aux.valorEvento()

                                                        bonif_sprints = [int(ddSprint[[x[4] for x in ddSprint].index(str(idx_spr))][0])] if str(type_homol).strip() != 'MVP' and str(type_homol).strip() != 'ENTREGA FINAL' else [int(x) for x in func_split(dadosOrigin[0][11])]
                                                        
                                                        bonific_calcul = premio_aux.CalculaSprint(valores[type_homol]['ValorPorSprint'], bonif_sprints)
                                                        
                                                        ################### SEPARANDO O VALOR QUE CADA COLABORADOR RECEBEU ###################
                                                                                                    
                                                        if str(type_homol).strip() != 'MVP' and str(dadosOrigin[0][38]) != '1': #AQUI É ONDE É TRATADO OS DADOS DE EVENTOS TRADICIONAIS - PRÉ-MVP E PÓS-MVP
                                                            #PEGANDO OS DADOS DOS GESTORES
                                                            bonific_list = [[dadosOrigin[0][3], bonific_calcul['GESTOR'], 'G']]
                                                            
                                                            #PEGANDO OS DADOS DOS ESPECIALISTAS
                                                            bonific_list_aux = [[f'{matr}', f'{float(list(dict(value).values())[0])}', 'E'] for matr, value in dict(bonific_calcul['ESPECIALISTA']['ValorParaMVP']).items()]

                                                            columns_p = ['id_sprint_fgkey', 'valor',
                                                                        'bonificado_fgkey', 'funcao_premio', 'id_entreg_fgkey',
                                                                        'hrs_normalizadas', 'dificuldade']

                                                            #PEGANDO OS DADOS DA SQUAD
                                                            bonific_list_aux1 = [[entrega[8], #MATRICULA
                                                                                    bonific_calcul['SQUAD'][entrega[2]]['Entregas'][entrega[1]]['Bonificação'], #VALOR DA BONIFICAÇÃO
                                                                                    'EX',
                                                                                    entrega[6], #ID DA ENTREGA
                                                                                    bonific_calcul['SQUAD'][entrega[2]]['Entregas'][entrega[1]]['HorasNormalizadas'], #HORAS NORMALIZADAS
                                                                                    bonific_calcul['SQUAD'][entrega[2]]['Entregas'][entrega[1]]['Dificuldade'], #DIFICULDADE
                                                                                    entrega[2], #NOME DA PESSOA
                                                                                    entrega[0] #ID DA SPRINT
                                                                                    ] for entrega in [entr for entr in spEntregas if entr[1] != None]]
                                                            
                                                        else: #AQUI PARA CASO SEJA MVP OU ENTREGA FINAL
                                                            #PEGANDO OS DADOS DOS GESTORES
                                                            bonific_list = [[dadosOrigin[0][3], bonific_calcul['GESTOR'], 'G', f'"{str(type_homol).strip().upper()}"']] 

                                                            #PEGANDO OS DADOS DOS ESPECIALISTAS
                                                            bonific_list_aux = [[f'{matr}', f'{float(list(dict(value).values())[0])}', 'E', f'"{str(type_homol).strip().upper()}"'] for matr, value in dict(bonific_calcul['ESPECIALISTA']['ValorParaMVP']).items()]

                                                            columns_p = ['id_sprint_fgkey', 'valor',
                                                                        'bonificado_fgkey', 'funcao_premio', 'opcional_evento',
                                                                        'hrs_normalizadas', 'dificuldade', 'opcional_hrs_necess']
                                                            
                                                            #PEGANDO OS DADOS DA SQUAD
                                                            bonific_list_aux1 = [[
                                                                                f'(SELECT Matricula FROM projeu_users WHERE Nome = "{name}")',
                                                                                bonific_calcul['SQUAD'][name]['BonificacaoSprint'],
                                                                                'EX',
                                                                                f'"{str(type_homol).strip().upper()}"',
                                                                                bonific_calcul['SQUAD'][name]['HorasNormalTotal'],
                                                                                int(sum([x['Dificuldade'] for x in dict(bonific_calcul['SQUAD'][name]['Entregas']).values()]) / len(dict(bonific_calcul['SQUAD'][name]['Entregas']))),
                                                                                name,
                                                                                ddSprint[cont_sprint - 1][4],
                                                                                sum([x['Horas'] for x in dict(bonific_calcul['SQUAD'][name]['Entregas']).values()])
                                                                                ] for name in dict(bonific_calcul['SQUAD']).keys()]
                                                        
                                                        bonific_list.extend(bonific_list_aux)
                                                        bonific_list.extend(bonific_list_aux1)
                                                        
                                                        limp_columns = lambda list_columns, range: str(list_columns[:range]).replace("'", "").replace("[", "").replace("]","")
                                                        
                                                        for entr_premio in bonific_list:
                                                            range_aux = 4
                                                            values = f"""{idx_spr},
                                                                        {round(float(entr_premio[1]), 2)},
                                                                        (SELECT id_user FROM projeu_users WHERE Matricula = {entr_premio[0]}), 
                                                                        '{entr_premio[2]}'
                                                                        """
                                                            if len(entr_premio) > 3:
                                                                range_aux = 5
                                                                values += f""", {entr_premio[3]}"""
                                                            
                                                            if len(entr_premio) > 4:
                                                                range_aux = 8
                                                                values += f""", {entr_premio[4]}, {entr_premio[5]}"""
                                                            
                                                            if len(entr_premio) > 8:
                                                                values += f', {entr_premio[8]}'
            
                                                            cmd_insert_premio = f'''
                                                            INSERT INTO projeu_premio_entr ({limp_columns(columns_p, range_aux)})
                                                            VALUES ({values});'''
                                                            
                                                            mycursor1.execute(cmd_insert_premio)
                                                            conexao.commit()
                                            
                                                    else:
                                                        cont_erro =+ 1
                                                        st.toast('Primeiramente, para homologação final é necessário finalizar a sprint', icon='❌')
                                                    
                                                mycursor1.close()
                                            except:
                                                cont_erro =+ 1
                                                st.toast('Erro ao adcionar homologação ao banco de dados.', icon='❌')
                                            if cont_erro < 1:
                                                st.toast('Dados de homologação atualizados', icon='✅')
                                        else:
                                            st.toast('Primeiramente, é necessário preencher a complexidade do projeto corretamente.', icon='❌')
                                                    
                                    else:
                                        st.toast('Primeiramente, preencha todos os campos corretamente.', icon='❌')

                                st.text(' ')
                                st.divider()
                                st.text(' ')
                                st.text(' ')
                                font_TITLE(f'COMPARAÇÃO DAS ENTREGAS',
                                           fonte_Projeto, "'Bebas Neue', sans-serif", 27, 'center', '#228B22')
                                font_TITLE(f'Planejamento da Sprint', fonte_Projeto, "'Bebas Neue', sans-serif", 25,
                                           'left')

                                col1, col2, col3, col4, col5 = st.columns([1, 0.22, 0.32, 0.13, 0.17])
                                with col1:
                                    st.caption('Atividades')
                                with col2:
                                    st.caption('Status')
                                with col3:
                                    st.caption('Executor')
                                with col4:
                                    st.caption('Hrs Neces')
                                with col5:
                                    st.caption('Compl')

                                for ativIDX in range(len(spEntregasPlan)):
                                    with col1:
                                        name_entreg = st.text_input('Atividade',
                                                                    spEntregasPlan[ativIDX][1] if
                                                                    spEntregasPlan[ativIDX][
                                                                        1] != None else '',
                                                                    key=f'Planj atividade{idx_spr} - {ativIDX} - {idx_parm}',
                                                                    disabled=False, label_visibility="collapsed")
                                    with col4:
                                        horas_entreg = st.text_input('Horas', value=spEntregasPlan[ativIDX][3],
                                                                     key=f' Planj horas{idx_spr} - {ativIDX} - {idx_parm}',
                                                                     disabled=block_sprint,
                                                                     label_visibility="collapsed")
                                    with col3:
                                        opc_colb = func_split(dadosOrigin[0][21])
                                        colab_entreg = st.text_input('Colaborador', opc_colb[
                                            opc_colb.index(spEntregasPlan[ativIDX][2]) if
                                            spEntregasPlan[ativIDX][2] != None and
                                            spEntregasPlan[ativIDX][2] != '' else 0],
                                                                     key=f'Planj colab{idx_spr} - {ativIDX} - {idx_parm}',
                                                                     disabled=block_sprint,
                                                                     label_visibility="collapsed")
                                    with col2:
                                        opc_stt = ['🟨 Backlog', '🟥 Impeditivo', '🟦 Executando', '🟩 Concluído']
                                        status_entreg = st.text_input('Status', opc_stt[opc_stt.index(
                                            str(spEntregasPlan[ativIDX][5]).strip()) if spEntregasPlan[ativIDX][
                                                                                            5] != None and
                                                                                        spEntregasPlan[ativIDX][
                                                                                            5] != '' else 0],
                                                                      key=f'Planj status{idx_spr}  - {idx_parm} - {ativIDX}',
                                                                      label_visibility="collapsed")
                                    with col5:
                                        opc_compl = ['Fácil', 'Médio', 'Difícil']
                                        compl_entreg = st.text_input('Compl.', opc_compl[
                                            opc_compl.index(spEntregasPlan[ativIDX][4]) if
                                            spEntregasPlan[ativIDX][4] != None and
                                            spEntregasPlan[ativIDX][4] != '---' else 0],
                                                                     key=f'Planj complex{idx_spr}  - {idx_parm}- {ativIDX}',
                                                                     label_visibility="collapsed")

                                st.text(' ')
                                font_TITLE(f'Realizado da Sprint', fonte_Projeto, "'Bebas Neue', sans-serif", 25,
                                           'left')
                                col1, col2, col3, col4, col5 = st.columns([1, 0.22, 0.32, 0.13, 0.17])
                                with col1:
                                    st.caption('Atividades')
                                with col2:
                                    st.caption('Status')
                                with col3:
                                    st.caption('Executor')
                                with col4:
                                    st.caption('Hrs Neces')
                                with col5:
                                    st.caption('Compl')

                                for ativIDX in range(len([x for x in spEntregas if x[1] != None and x[1] != ''])):
                                    with col1:
                                        name_entreg = st.text_input('Atividade',
                                                                    spEntregas[ativIDX][1],
                                                                    key=f'Realiz atividade{idx_spr} - {ativIDX} - {idx_parm}',
                                                                    disabled=False, label_visibility="collapsed")
                                    with col4:
                                        horas_entreg = st.text_input('Horas', value=spEntregas[ativIDX][3],
                                                                     key=f' Realiz horas{idx_spr} - {ativIDX} - {idx_parm}',
                                                                     disabled=block_sprint,
                                                                     label_visibility="collapsed")
                                    with col3:
                                        opc_colb = func_split(dadosOrigin[0][21])
                                        colab_entreg = st.text_input('Colaborador',
                                                                     opc_colb[opc_colb.index(spEntregas[ativIDX][2]) if
                                                                     spEntregas[ativIDX][2] != None and
                                                                     spEntregas[ativIDX][2] != '' else 0],
                                                                     key=f'Realiz colab{idx_spr} - {ativIDX} - {idx_parm}',
                                                                     disabled=block_sprint,
                                                                     label_visibility="collapsed")
                                    with col2:
                                        opc_stt = ['🟨 Backlog', '🟥 Impeditivo', '🟦 Executando', '🟩 Concluído']
                                        status_entreg = st.text_input('Status', opc_stt[opc_stt.index(
                                            str(spEntregas[ativIDX][5]).strip()) if spEntregas[ativIDX][5] != None and
                                                                                    spEntregas[ativIDX][
                                                                                        5] != '' else 0],
                                                                      key=f'Realiz status{idx_spr}  - {idx_parm} - {ativIDX}',
                                                                      label_visibility="collapsed")

                                    with col5:
                                        opc_compl = ['Fácil', 'Médio', 'Difícil']
                                        compl_entreg = st.text_input('Compl.', opc_compl[
                                            opc_compl.index(spEntregas[ativIDX][4]) if
                                            spEntregas[ativIDX][4] != None and
                                            spEntregas[ativIDX][4] != '---' else 0],
                                                                     key=f'Realiz complex{idx_spr}  - {idx_parm}- {ativIDX}',
                                                                     label_visibility="collapsed")

                                st.text(' ')
                                st.text(' ')
                                font_TITLE(f'DIFERENÇAS', fonte_Projeto, "'Bebas Neue', sans-serif", 27, 'center')
                                col1D, col2D, col3D = st.columns(3)
                                with col1D:
                                    displayInd('Diferênça Horas',
                                               f'{sum([x[3] for x in spEntregas]) - sum([x[3] for x in spEntregasPlan])}', 1, 3)
                                with col2D:
                                    displayInd('Diferênça Entregas',
                                               f'{len([x[1] for x in spEntregas if x[1] != None and x[1] != ""]) - len([x[1] for x in spEntregasPlan if x[1] != None and x[1] != ""])}', 1, 3)
                                with col3D:
                                    displayInd('Diferênça Colaboradores',
                                               f'{len(set([x[2] for x in spEntregas if x[1] != None and x[1] != ""])) - len(set([x[2] for x in spEntregasPlan if x[1] != None and x[1] != ""]))}', 1, 3)

                                entreg_diferent1 = set([x[1] for x in spEntregas]) - set([x[1] for x in spEntregasPlan])
                                entreg_diferent2 = set([x[1] for x in spEntregasPlan]) - set([x[1] for x in spEntregas])

                                font_TITLE(f'Entregas a Mais', fonte_Projeto, "'Bebas Neue', sans-serif", 22, 'left')
                                if len([x for x in list(entreg_diferent2) if x != None]) > 0:
                                    entr_mais = [x for x in spEntregas if
                                                 str(x[1]).strip().lower() in [str(x).strip().lower() for x in
                                                                               list(entreg_diferent1)] and x[1] != None]
                                else:
                                    entr_mais = [['', '', '', 0, '', '']]

                                col1, col2, col3, col4, col5 = st.columns([1, 0.22, 0.32, 0.13, 0.17])
                                with col1:
                                    st.caption('Atividades')
                                with col2:
                                    st.caption('Status')
                                with col3:
                                    st.caption('Executor')
                                with col4:
                                    st.caption('Hrs Neces')
                                with col5:
                                    st.caption('Compl')

                                for entr_idx in range(len(entr_mais)):
                                    with col1:
                                        st.text_input(f'', value=entr_mais[entr_idx][1], label_visibility="collapsed",
                                                      key=f'Atividades Mais{entr_idx} {idx_spr}')
                                    with col2:
                                        st.text_input(f'', value=entr_mais[entr_idx][5], label_visibility="collapsed",
                                                      key=f'Status Mais{entr_idx} {idx_spr}')
                                    with col3:
                                        st.text_input(f'', value=entr_mais[entr_idx][2], label_visibility="collapsed",
                                                      key=f'Executor Mais{entr_idx} {idx_spr}')
                                    with col4:
                                        st.text_input(f'', value=entr_mais[entr_idx][3], label_visibility="collapsed",
                                                      key=f'Hrs Mais{entr_idx} {idx_spr}')
                                    with col5:
                                        st.text_input(f'', value=entr_mais[entr_idx][4], label_visibility="collapsed",
                                                      key=f'Compl Mais{entr_idx} {idx_spr}')

                                font_TITLE(f'Entregas a Menos', fonte_Projeto, "'Bebas Neue', sans-serif", 22, 'left')
                                if len([x for x in list(entreg_diferent1) if x != None]) > 0:
                                    ent_menos = [x for x in spEntregasPlan if
                                                 str(x[1]).strip().lower() in [str(x).strip().lower() for x in
                                                                               list(entreg_diferent2)]]
                                else:
                                    ent_menos = [['', '', '', 0, '', '']]

                                col1, col2, col3, col4, col5 = st.columns([1, 0.22, 0.32, 0.13, 0.17])
                                with col1:
                                    st.caption('Atividades')
                                with col2:
                                    st.caption('Status')
                                with col3:
                                    st.caption('Executor')
                                with col4:
                                    st.caption('Hrs Neces')
                                with col5:
                                    st.caption('Compl')

                                for entr_idx in range(len(ent_menos)):
                                    with col1:
                                        st.text_input(f'', value=ent_menos[entr_idx][1], label_visibility="collapsed",
                                                      key=f'Atividades Menos{entr_idx} {idx_spr}')
                                    with col2:
                                        st.text_input(f'', value=ent_menos[entr_idx][5], label_visibility="collapsed",
                                                      key=f'Status Menos{entr_idx} {idx_spr}')
                                    with col3:
                                        st.text_input(f'', value=ent_menos[entr_idx][2], label_visibility="collapsed",
                                                      key=f'Executor Menos{entr_idx} {idx_spr}')
                                    with col4:
                                        st.text_input(f'', value=ent_menos[entr_idx][3], label_visibility="collapsed",
                                                      key=f'Hrs Menos{entr_idx} {idx_spr}')
                                    with col5:
                                        st.text_input(f'', value=ent_menos[entr_idx][4], label_visibility="collapsed",
                                                      key=f'Compl Menos{entr_idx} {idx_spr}')

                                    st.text(' ')
                                    st.text(' ')
                            with tab4:
                                #OBSERVAÇÃO DA SPRINT SELECIONADA
                                obsv_sprint = [x for x in ObservBD if x[1] == idx_spr]
                                if len(obsv_sprint)>0:
                                    font_TITLE('Histórico de Observações', fonte_Projeto,"'Bebas Neue', sans-serif", 26, 'left')
                                    for idx_spt in range(len(obsv_sprint)):
                                        font_TITLE(f'{str(obsv_sprint[idx_spt][5])} - {str(obsv_sprint[idx_spt][4])}', fonte_Projeto,"'Bebas Neue', sans-serif", 17, 'left', '#228B22')
                                        st.markdown(obsv_sprint[idx_spt][3])

                                    st.text(' ')                                
                                
                                font_TITLE('ADCIONAR OBSERVAÇÃO', fonte_Projeto,"'Bebas Neue', sans-serif", 26, 'left')  
                                obs_sprt = st.text_area('awdadad',label_visibility="collapsed", key=f'OBSERVAÇAÕ{idx_spr}')
                                btt_obs = st.button('Enviar', key=f'btt obsrv {idx_spr}')
