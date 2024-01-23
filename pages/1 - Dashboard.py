import streamlit as st
import mysql.connector
from util import string_to_datetime, displayInd, font_TITLE
from utilR import statusProjetos, css_9box_home, ninebox_home, nineboxDatasUnidades_home
from datetime import date, datetime
import matplotlib.pyplot as plt
import plotly.graph_objects as go

st.set_page_config(layout="wide",
                   initial_sidebar_state="collapsed")

conexao = mysql.connector.connect(
    passwd='nineboxeucatur',
    port=3306,
    user='ninebox',
    host='nineboxeucatur.c7rugjkck183.sa-east-1.rds.amazonaws.com',
    database='projeu'
)
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
        SELECT GROUP_CONCAT(status_homolog SEPARATOR '~/>') 
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
        SELECT GROUP_CONCAT(check_consolid SEPARATOR '~/>')
        FROM projeu_sprints
        WHERE projeu_sprints.id_proj_fgkey = projeu_projetos.id_proj
    ) AS sprint_consolidada
FROM 
    projeu_projetos
JOIN 
	projeu_complexidade PC on PC.proj_fgkey = projeu_projetos.id_proj
GROUP BY
    projeu_projetos.id_proj;"""
mycursor.execute(comand)
ddPaging = mycursor.fetchall()

cmd_cadeia = '''
    SELECT 
        PMP.macroprocesso,
        PPG.nome_prog
    FROM 
        projeu_programas PPG
    JOIN projeu_macropr PMP ON PMP.id = PPG.macroprocesso_fgkey;'''
mycursor.execute(cmd_cadeia)
cadeiaBD = mycursor.fetchall()

mycursor.close()


fonte_Projeto = '''@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Bungee+Inline&family=Koulen&family=Major+Mono+Display&family=Passion+One&family=Sansita+Swashed:wght@500&display=swap');'''
font_TITLE('DASHBOARD DE PROJETOS', fonte_Projeto,"'Bebas Neue', sans-serif", 49, 'center')
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    displayInd('Total de Projetos', len(list(set([x[0] for x in ddPaging]))), min_val=0, max_val=len(list(set([x[0] for x in ddPaging]))))
with col2:
    displayInd('Concluídos', len(list(set([x[0] for x in ddPaging if x[24] == "Concluído"]))), min_val=0, max_val=len(list(set([x[0] for x in ddPaging]))))
with col3:
    projs_andament = len(list(set([x[0] for x in ddPaging if x[13] != None and string_to_datetime(str(x[13]).split("~/>")[0]) < date.today() and x[24] != "Concluído"])))
    displayInd('Andamento', projs_andament, min_val=0, max_val=len(list(set([x[0] for x in ddPaging]))))
with col4:
    projs_nao_inic = len(list(set([x[0] for x in ddPaging if x[13] == None or string_to_datetime(str(x[13]).split("~/>")[0]) > date.today()])))
    displayInd('Não Iniciado', projs_nao_inic, min_val=0, max_val=len(list(set([x[0] for x in ddPaging]))))
with col5:
    projs_paralis = len([x[1] for x in ddPaging if str(x[31]).strip() == "Paralisado"])
    displayInd('Paralisado', projs_paralis, min_val=0, max_val=len(list(set([x[0] for x in ddPaging]))))

nomeProj = [x[1] for x in ddPaging]
statusProj = [x[24] for x in ddPaging]
dadosProj = [f"{nomeProj} -- {statusProj}" for nomeProj, statusProj in zip(nomeProj, statusProj)]


sprints_pendents = []
for proj_list in ddPaging:
    pendt_aux = [f'SPRINT {str(proj_list[11]).split("~/>")[x]} - {str(proj_list[1]).strip()}' if str(str(proj_list[12]).split("~/>")[x]).strip() not in ['MVP', 'ENTREGA FINAL'] else f'{str(proj_list[12]).split("~/>")[x]} - {str(proj_list[1]).strip()}' for x in range(len(str(proj_list[44]).split('~/>'))) if str(proj_list[44]).split('~/>')[x] not in ['None', '1'] and str(str(proj_list[34]).split('~/>')[x]).strip() == '0']

    if len(pendt_aux) > 0:
        sprints_pendents.extend(pendt_aux)


col1, colaux, col2, col3 = st.columns([2, 0.1, 2, 2])
with col1: 
    ninebox_style = css_9box_home() 
    ddbox = [[nomeProj], [statusProj]]
    links = [None]*len(nomeProj)
    img_doc = ''
    
    html1 = ninebox_home(0, statusProjetos(ddbox), ddbox, 'Projetos', links, img_doc)
    st.write(f'<style>{ninebox_style}</style>', unsafe_allow_html=True)
    st.write(f'<div>{html1}</div>', unsafe_allow_html=True)

    ddbox = [[], [sprints_pendents]]
    
    html1 = ninebox_home(0, nineboxDatasUnidades_home(ddbox, ''), ddbox, 'Sprints Pendentes de Pagamento', links, img_doc)
    st.write(f'<style>{ninebox_style}</style>', unsafe_allow_html=True)
    st.write(f'<div>{html1}</div>', unsafe_allow_html=True)

with col2:
    font_TITLE('PROJETOS POR MACRO', fonte_Projeto,"'Bebas Neue', sans-serif", 25, 'left')
    mcr = list(set([str(x[0]).strip() for x in cadeiaBD]))
    
    qtdMcr = []
    for i in range(len(mcr)):
        contMcr = sum(1 for x in ddPaging if mcr[i] == x[5])
        qtdMcr.append(contMcr)

    macroDesconsiderado = [i for i, qtd in enumerate(qtdMcr) if qtd == 0]

    for i in reversed(macroDesconsiderado):
        del mcr[i]
        del qtdMcr[i]

    cores_personalizadas = ['#6E1423', '#BD1F36', '#A71E34', '#E01E37', '#a11d33']
    fig = go.Figure()
    fig.add_trace(go.Pie(labels=mcr, values=qtdMcr, automargin=True, marker=dict(colors=cores_personalizadas)))
    fig.update_layout(
    legend=dict(x=0, y=1.3, traceorder='normal', orientation='h'),
    margin=dict(l=0, r=650, t=0, b=30),  
    width=900
    )   
    st.text(' ')
    st.plotly_chart(fig)

with col3:
    font_TITLE('PROJETOS POR PROGRAMA', fonte_Projeto,"'Bebas Neue', sans-serif", 25, 'left')
    pgm = list(set([str(x[1]).strip() for x in cadeiaBD]))

    qtdPgm = []
    for i in range(len(pgm)):
        contPgm = sum(1 for x in ddPaging if pgm[i] == str(x[6]).strip())
        qtdPgm.append(contPgm)

    progDesconsiderado = [i for i, qtd in enumerate(qtdPgm) if qtd == 0]

    for i in reversed(progDesconsiderado):
        del pgm[i]
        del qtdPgm[i]

    cores_personalizadas = ['#0077b6', '#0096c7', '#00B4D8', '#023E8A', '#48CAE4', '#90E0EF', '#ADE8F4']
    fig = go.Figure()
    fig.add_trace(go.Pie(labels=[x[:70] for x in pgm], values=qtdPgm, automargin=True, marker=dict(colors=cores_personalizadas)))
    fig.update_layout(
    legend=dict(x=0, y=1.3, traceorder='normal', orientation='h'),
    margin=dict(l=0, r=650, t=0, b=1),  # Define as margens do gráfico
    width=900
    )  
    st.text(' ')
    st.plotly_chart(fig)


########## DADOS DE DESVIO ##########
desvio_by_project = {}
for id_proj in list(set([x[0] for x in ddPaging])):
    dadosOrigin = [x for x in ddPaging if x[0] == id_proj]

    dificuldade_proj = f'{dadosOrigin[0][36]} {dadosOrigin[0][37]}'
    type_proj = str(dadosOrigin[0][4]).strip()

    dat_inic_sprt = [datetime.strptime(str(x), "%Y-%m-%d").date() for x in list(str(dadosOrigin[0][13]).split("~/>"))]  if dadosOrigin[0][13] != None else [None]

    dat_fim_sprt = [datetime.strptime(str(x), "%Y-%m-%d").date() for x in list(str(dadosOrigin[0][14]).split("~/>"))]  if dadosOrigin[0][13] != None else [None]
    dat_homol = [datetime.strptime(str(x), "%Y-%m-%d").date() for x in list(str(dadosOrigin[0][43]).split("~/>"))] if dadosOrigin[0][43] != None and dadosOrigin[0][43] != 'None' else [None]

    dif_desvio_sprints = [int((dat_inic_sprt[x + 1] - dat_fim_sprt[x]).days) if x < int(len(dat_inic_sprt)-1) else None for x in range(len(dat_fim_sprt))]
    
    dif_desvio_homolog = [int((dat_homol[x] - dat_fim_sprt[x]).days) if dat_homol[x] != None else dat_homol[x] for x in range(len(dat_homol))]

    sprint_aux = [x for x in dif_desvio_sprints if x != None]
    homol_aux = [x for x in dif_desvio_homolog if x != None] 
    dic_aux = {'por_sprint': sum(sprint_aux) / len(sprint_aux) if len(sprint_aux) > 0 else None,
               'sprint_por_homol': sum(homol_aux) / len(homol_aux) if len(homol_aux) > 0 else None}

    desvio_by_project[id_proj] = dic_aux


font_TITLE('DESVIO DOS PROJETOS', fonte_Projeto,"'Bebas Neue', sans-serif", 25, 'left')
col1, col2 = st.columns([1, 3])
with col1:
    st.text(' ')
    st.text(' ')
    displayInd('Desvio Sprint x Sprint (Média)', round(sum([x['por_sprint'] for x in desvio_by_project.values() if x['por_sprint'] != None]) / len([x['por_sprint'] for x in desvio_by_project.values() if x['por_sprint'] != None]), 2), min_val=0, max_val=len(list(set([x[0] for x in ddPaging]))), padding=1.8, id=2)
    displayInd('Desvio Sprint x Homologação (Média)', round(sum([x['sprint_por_homol'] for x in desvio_by_project.values() if x['sprint_por_homol'] != None]) / len([x['sprint_por_homol'] for x in desvio_by_project.values() if x['sprint_por_homol'] != None]), 2), min_val=0, max_val=len(list(set([x[0] for x in ddPaging]))), padding=1.8, id=2)

with col2:
    data = {[str(x[1]).strip() for x in ddPaging if str(x[0]).strip() == str(id).strip()][0]: value for id, value in dict(desvio_by_project).items()}

    valid_data = {str(k): {'por_sprint': v["por_sprint"] if v["por_sprint"] is not None else 0,
                        'sprint_por_homol': v["sprint_por_homol"] if v["sprint_por_homol"] is not None else 0} for k, v in data.items()}

    keys = list(valid_data.keys())
    por_sprint_values = [valid_data[key]["por_sprint"] for key in keys]
    sprint_por_homol_values = [valid_data[key]["sprint_por_homol"] for key in keys]

    fig = go.Figure()

    fig.add_trace(go.Bar(x=[str(x)[:23] for x in keys], y=por_sprint_values, name='Desvio Sprint x Sprint (Média)', marker_color='rgba(78, 115, 223, 0.7)'))

    fig.add_trace(go.Bar(x=[str(x)[:23] for x in keys], y=sprint_por_homol_values, name='Desvio Sprint x Homologação (Média)', marker_color='rgba(255, 0, 0, 0.7)'))

    fig.update_layout(xaxis={'categoryorder': 'total ascending'},
                    xaxis_title='Chave', yaxis_title='Valores', barmode='group',
                    legend=dict(title=dict(text='Tipo'), orientation='h', x=0, y=1.15, traceorder='normal'),
                    width=1000, height=480)
    
    st.plotly_chart(fig)