import streamlit as st
from PIL import Image
import mysql.connector
from utilR import font_TITLE
from time import sleep
from datetime import datetime 
from dateutil.relativedelta import relativedelta
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import tempfile
from relatorio import css_email, escopoGeral


icone = Image.open('imagens/icone.png')
st.set_page_config(
    page_title="Gestão de Prêmios",
    page_icon=icone,
    layout="wide")


conexao = mysql.connector.connect(
    passwd='nineboxeucatur',
    port=3306,
    user='ninebox',
    host='nineboxeucatur.c7rugjkck183.sa-east-1.rds.amazonaws.com',
    database='projeu'
    )

mycursor = conexao.cursor()

fonte_Projeto = '''@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Bungee+Inline&family=Koulen&family=Major+Mono+Display&family=Passion+One&family=Sansita+Swashed:wght@500&display=swap');'''
font_TITLE('GESTÃO DE PRÊMIOS', fonte_Projeto,"'Bebas Neue', sans-serif", 49, 'center')


cmd_premio = f"""
SELECT 
	PS.id_sprint,
    PS.number_sprint,
    PP.name_proj,
	PE.nome_Entrega,
    PU.Matricula,
	PU.Nome,
    PPE.funcao_premio as FUNCAO_PREMIO,
    PE.hra_necess as HORAS_NECESSÁRIAS,
    PPE.hrs_normalizadas AS HORAS_NORMALIZADAS,
    PPE.dificuldade,
    PPE.valor,
    PS.check_aprov,
    PU.email_pj,
    (
        SELECT 
            nome_empresa 
        FROM 
            projeu_empresas AS PEM 
        WHERE id_empresa = PU.empresa_fgkey
    ) AS NAME_EMPRESA,
    (
        SELECT 
            number_empresa
        FROM 
            projeu_empresas AS PEM 
        WHERE id_empresa = PU.empresa_fgkey
    ) AS NUMBER_EMPRESA
FROM projeu_premio_entr AS PPE
LEFT JOIN 
    projeu_sprints PS ON PS.id_sprint = PPE.id_sprint_fgkey
LEFT JOIN 
    projeu_users PU ON PU.id_user = PPE.bonificado_fgkey
LEFT OUTER JOIN 
    projeu_entregas PE ON PE.id_entr = PPE.id_entreg_fgkey
LEFT JOIN 
    projeu_projetos PP ON PP.id_proj = PS.id_proj_fgkey
WHERE 
    PS.check_consolid <> 1 OR PS.check_consolid IS NULL
GROUP BY PPE.id_premio;
"""
mycursor.execute(cmd_premio)
dadosBD = mycursor.fetchall()


cmd_equipe = '''
SELECT 
	PRE.id_registro,
    PP.name_proj,
    PU.Matricula,
    PU.Nome,
    PRE.papel
    FROM projeu_registroequipe AS PRE
JOIN projeu_projetos PP ON PP.id_proj = PRE.id_projeto
JOIN projeu_users PU ON PU.id_user = PRE.id_colab
WHERE status_reg = 'A'
GROUP BY PRE.id_registro;
'''
mycursor.execute(cmd_equipe)
equipeBD = mycursor.fetchall()
mycursor.close()


def enviar_email(destino, nome_colab = None, list_valores = None, txt_temporario = None, name_arquivo = None):
    
    msg = MIMEMultipart()
    msg['Subject'] = "Assunto"
    msg['From'] = 'automacao1.processos@gmail.com'
    msg['To'] = destino
    
    if nome_colab != None:
        html = escopoGeral(nome_colab, list_valores, '051.625.652-10', 'PJ')
        css = css_email()
        corpo_email = html
        msg.attach(MIMEText(corpo_email, 'html'))

    if txt_temporario is not None:
        with open(txt_temporario, 'rb') as f:
            attachment = MIMEApplication(f.read())
            attachment.add_header('Content-Disposition', 'attachment', filename=f'PremioProjeto_{name_arquivo}_{hoje.month}_{hoje.year}.txt')
            msg.attach(attachment)

    s = smtplib.SMTP('smtp.gmail.com: 587')
    s.starttls()

    password = 'zobl ekzk sljm zrwk'
    #LOGANDO NO EMAIL    
    s.login(msg['From'], password)

    #ENVIANDO EMAIL
    s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))
    print('Email enviado')


def complexidade_name(number):
    aux = {1: 'Fácil',
           2: 'Médio',
           3: 'Difícil'}
    
    return aux[number]


def funcao_premio(sigla):
    if sigla in ['G', 'E', 'EX']:
        aux = {'G': 'Gestor',
            'E': 'Especialista',
            'EX': 'Executor'}
        return aux[sigla]
    else:
        return None


def organizar_por_funcao(dicionario):
    gestores = []
    especialistas = []
    executores = []

    for nome, (dados, funcao) in dicionario.items():
        if funcao == 'Gestor':
            gestores.append({nome: (dados, funcao)})
        elif funcao == 'Especialista':
            especialistas.append({nome: (dados, funcao)})
        elif funcao == 'Executor':
            executores.append({nome: (dados, funcao)})

    resultado = {}
    for gestor in gestores:
        resultado.update(gestor)
    for especialista in especialistas:
        resultado.update(especialista)
    for executor in executores:
        resultado.update(executor)

    return resultado


tab1, tab2 = st.tabs(['APROVAÇÃO', 'CONSOLIDADO'])

with tab1:
    dadosBD1 = [x for x in dadosBD if str(x[11]).lower() != '1']
    
    premios_proj_pendent = {name_proj: [x for x in dadosBD1 if str(x[2]).strip() == str(name_proj).strip()] for name_proj in list(set([x[2] for x in dadosBD1 if str(x[11]).strip() != str(1)]))}
    font_TITLE('PRÊMIOS PENDENTES DE APROVAÇÃO', fonte_Projeto,"'Bebas Neue', sans-serif", 26, 'left')
    if len(premios_proj_pendent) > 0:
        for proj_name, dd_premio in premios_proj_pendent.items():

            #DIVIDINDO POR SPRINT
            dd_premio_sprint = {number_sp: [x for x in dd_premio if str(x[1]).strip() == str(number_sp).strip()] for number_sp in list(set([x[1] for x in dd_premio]))}
            
            for sprint, dd_sprint in dd_premio_sprint.items():
                with st.expander(f'{proj_name} - Sprint {sprint}'):
                    
                    def colabs_proj(matricula = 0):
                        dados_by_project = [x for x in equipeBD if str(x[1]).lower().strip() == str(proj_name).strip().lower()]
                        Dic_aux = {str(matric): [x[4] for x in dados_by_project if str(x[2]).strip() == str(matric).strip()][0] for matric in list(set([x[2] for x in dados_by_project]))}
                        if matricula == 0:
                            retorno = Dic_aux
                        else:
                            retorno = Dic_aux[str(matricula)]    
                        
                        return retorno

                    font_TITLE(proj_name, fonte_Projeto,"'Bebas Neue', sans-serif", 24, 'left')
                    ########## CONSOLIDADE POR PESSOA ########## 
                    premios_pessoa = {[x[3] for x in equipeBD if str(x[2]).strip() == str(matric_pessoa).strip()][0]:[[x for x in dd_sprint if str(x[4]).strip() == str(matric_pessoa).strip()], colabs_proj(matric_pessoa)] for matric_pessoa in list(colabs_proj(0).keys())}

                    premios_pessoa_sequencia = organizar_por_funcao(premios_pessoa)
                    font_TITLE('PRÊMIO POR PESSOAS', fonte_Projeto,"'Bebas Neue', sans-serif", 20, 'left', '#228B22')
                    col0, col1, col2, col3, col4, col5, col6 = st.columns([0.19, 0.20, 0.18, 0.89, 0.14, 0.22, 0.17])
                    with col0:
                        st.caption('Empresa')
                    with col1:
                        st.caption('Função')
                    with col2:
                        st.caption('Matricula')
                    with col3:
                        st.caption('Nome')
                    with col4:
                        st.caption('Atividades')
                    with col5:
                        st.caption('Horas')
                    with col6:
                        st.caption('Valor Total')

                    for name, dd_name in premios_pessoa_sequencia.items():
                        with col0:
                            empresa_number = st.text_input('', 'EUCATUR', label_visibility='collapsed', key=f'Empresa{proj_name}- pessoa {name} - sprint{sprint}')
                        with col1:
                            funcao = st.text_input('', dd_name[1], label_visibility='collapsed', key=f'Funcao{proj_name}- pessoa {name}- sprint{sprint}')
                        with col2:
                            matricula_pessoa = st.text_input('', dd_name[0][0][4] if len(dd_name[0]) > 0 else 0, label_visibility='collapsed', key=f'Unidade{proj_name} - pessoa {name}- sprint{sprint}')
                        with col3:
                            nome_pessoa = st.text_input('', name, label_visibility='collapsed', key=f'Matricula{proj_name} - pessoa {name}- sprint{sprint}')
                        with col4:
                            qntd_atdd = st.text_input('', len(list(set([str(x[3]).strip() for x in dd_name[0] if x[3] != None]))) if len(dd_name[0]) > 0 else 0, label_visibility='collapsed', key=f'Nome{proj_name} - pessoa {name}- sprint{sprint}')
                        with col5:
                            horas_pessoa = st.text_input('', sum([x[7] if x[7] != None else 0 for x in dd_name[0]]) if len(dd_name[0]) > 0  else 0, label_visibility='collapsed', key=f'Cargo{proj_name} - pessoa {name}- sprint{sprint}')
                        with col6:
                            valor_total_pessoa = st.text_input('', sum([x[10] for x in dd_name[0]]) if len(dd_name[0]) > 0  else 0, label_visibility='collapsed', key=f'Valor{proj_name} - pessoa {name}- sprint{sprint}')

                    font_TITLE('VALOR POR ENTREGA', fonte_Projeto,"'Bebas Neue', sans-serif", 20, 'left', '#228B22')
                    col0, col1, col11, col2, col3, col4, col5 = st.columns([0.14, 0.32, 0.22, 1, 0.14, 0.22, 0.17])
                    with col0:
                        st.caption('Matricula')
                    with col1:
                        st.caption('Executor')
                    with col11:
                        st.caption('Função')
                    with col2:
                        st.caption('Entrega')
                    with col3:
                        st.caption('Horas')
                    with col4:
                        st.caption('Complexidade')
                    with col5:
                        st.caption('Valor')

                    for idx_premio in range(len(dd_sprint)):
                        with col0:
                            st.text_input('', dd_sprint[idx_premio][4], label_visibility='collapsed', key=f'matricula {proj_name} - {idx_premio} - sprint{sprint}')
                        with col1:
                            st.text_input('', dd_sprint[idx_premio][5], label_visibility='collapsed', key=f'executor {proj_name} - {idx_premio} - sprint{sprint}')
                        with col11:
                            st.text_input('', funcao_premio(dd_sprint[idx_premio][6]), label_visibility='collapsed', key=f'funcao {proj_name} - {idx_premio} - sprint{sprint}')
                        with col2:
                            st.text_input('', dd_sprint[idx_premio][3], label_visibility='collapsed', key=f'Entrega {proj_name} - {idx_premio} - sprint{sprint}')
                        with col3:
                            st.text_input('', dd_sprint[idx_premio][7], label_visibility='collapsed', key=f'Horas {proj_name} - {idx_premio} - sprint{sprint}')
                        with col4:
                            st.text_input('', complexidade_name(dd_sprint[idx_premio][9]) if dd_sprint[idx_premio][9] != None else ' ', label_visibility='collapsed', key=f'Complexidade {proj_name} - {idx_premio} - sprint{sprint}')
                        with col5:
                            st.text_input('', dd_sprint[idx_premio][10], label_visibility='collapsed', key=f'Valor {proj_name} - {idx_premio} - sprint{sprint}')    
                    
                    button_aprov = st.button('Aprovar', key=f'Aprovação {proj_name} - sprint{sprint}')
                    if button_aprov:
                        mycursor = conexao.cursor()
                        cmd_up = f'UPDATE projeu_sprints SET check_aprov = 1 WHERE id_sprint = {dd_sprint[0][0]};'
                        mycursor.execute(cmd_up)
                        conexao.commit()

                        st.toast('Prêmio Aprovado!', icon='✅')
                        sleep(5)
                        mycursor.close()
                        st.rerun()

    else:
        st.error('NÃO HÁ PRÊMIOS PARA SEREM APROVADOS')
        
with tab2:
    font_TITLE('PRÊMIOS CONSOLIDADOS', fonte_Projeto,"'Bebas Neue', sans-serif", 26, 'left')
    st.text(' ')
    dadosBD = [x for x in dadosBD if str(x[11]).strip() == str(1).strip()]
    
    matric_and_names = list(set((x[4], x[5]) for x in dadosBD)) 

    consolid_pendent = {matric_and_names[list([x[0] for x in matric_and_names]).index(matric)][1]: [x for x in dadosBD if str(x[4]).strip() == str(matric).strip()] for matric in list(set([x[4] for x in dadosBD]))}

    if len(consolid_pendent) > 0:
        def colabs_proj(matricula):
            dados_by_project = {matri:equipeBD[list([str(x[2]) for x in equipeBD]).index(matri)][4] for matri in [str(x[0]).strip() for x in matric_and_names]}

            return dados_by_project[str(matricula)]
        
        col0, col2, col3, col4, col5, col6 = st.columns([0.19, 0.18, 0.89, 0.14, 0.17, 0.17])
        with col0:
            st.caption('Empresa')
        with col2:
            st.caption('Matricula')
        with col3:
            st.caption('Nome')
        with col4:
            st.caption('Atividades')
        with col5:
            st.caption('Horas')
        with col6:
            st.caption('Valor Total')

        for name_colab, dd_consolid in consolid_pendent.items():
            with col0:
                empresa_number = st.text_input('', 'EUCATUR', label_visibility='collapsed', key=f'Consolidado Empresa {name_colab}')
            with col2:
                matricula_pessoa = st.text_input('', dd_consolid[0][4], label_visibility='collapsed', key=f'Consolidado Matricula{name_colab}')
            with col3:
                nome_pessoa = st.text_input('', dd_consolid[0][5], label_visibility='collapsed', key=f'Consolidado Nome{name_colab}')
            with col4:
                qntd_atdd = st.text_input('', len(list(set([str(x[3]).strip().lower() for x in dd_consolid]))), label_visibility='collapsed', key=f'Consolidado Atividade{name_colab}')
            with col5:
                horas_pessoa = st.text_input('', sum([int(x[7]) if x[7] != None else 0 for x in dd_consolid]), label_visibility='collapsed', key=f'Consolidado horas{name_colab}')
            with col6:
                valor_total_pessoa = st.text_input('', sum([x[10] for x in dd_consolid]), label_visibility='collapsed', key=f'Consolidado Valor{name_colab}')
        
        st.text(' ')
        button_consolid = st.button('Consolidar') 
        if button_consolid:
            sprints = list(set([x[0] for x in dadosBD]))

            for id_sprint in sprints:
                mycursor = conexao.cursor()
                cmd_consolid = f"UPDATE projeu_sprints SET check_consolid = 1 WHERE id_sprint = {id_sprint};"
            
                mycursor.execute(cmd_consolid)
                conexao.commit()

            mycursor.close()
            st.toast('Prêmio Consolidado!', icon='✅')
            sleep(4)
            
            sum_horas = 0
            sum_valor = 0
            fun_digits = lambda x, y=[6, 4, 2, 4, 2, 4, 1, 2, 16]: [f'{"0"*(int(y[idx])-len(str(x[idx])))}{str(x[idx])}' for idx in range(len(x))]

            hoje = datetime.today() + relativedelta(months=1)        
            #ENVIADO EMAIL PARA O DEPARTAMENTO PESSOAL
            dados_by_empres = {name_empr: {mat: [x for x in dadosBD if str(x[14]).strip() == str(name_empr).strip() and str(x[4]).strip() == str(mat).strip()] for mat in list(set([x[4] for x in dadosBD if str(x[14]).strip() == str(name_empr).strip()]))} for name_empr in list(set([dd[14] for dd in dadosBD if str(dd[13]).strip().upper() != 'PJ']))}
            for cod_empres, dd_empres in dados_by_empres.items():
                
                #CRIANDO ARQUIVO TEMPORÁRIO TXT
                with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
                    info_txt = ""

                    for matric_colab, dd_consolid in dd_empres.items():
                        horas_colab = sum([int(x[7]) if x[7] != None else 0 for x in dd_consolid])
                        valor_colab = sum([x[10] for x in dd_consolid])

                        sum_horas += horas_colab
                        sum_valor += valor_colab
                        
                        dd_txt = fun_digits([matric_colab, '1204', hoje.month, hoje.year,hoje.month, hoje.year, 0, 5, str(round(sum_valor, 2)).replace('.', ',')])

                        info_txt += f'''{dd_txt[0]};{dd_txt[1]};{dd_txt[2]};{dd_txt[3]};{dd_txt[4]};{dd_txt[5]};{dd_txt[6]};{dd_txt[7]};;;;{dd_txt[8]}
'''
                    temp_file.write(info_txt)
                    arquivo_temporario = temp_file.name
                
                #DESTINO, NOME_COLAB, LIST_VALORES, TXT_TEMPORARIO, NAME_ARQUIVO
                enviar_email(destino='processos.eucatur@gmail.com',  txt_temporario=arquivo_temporario, name_arquivo=cod_empres)
            
            #ENVIADO EMAIL PARA OS PJ
            consolid_pj = {name_colab: dd_consolid for name_colab, dd_consolid in consolid_pendent.items() if 'PJ' in [str(x[13]).strip().upper() for x in dd_consolid]}
            for name_colab, dd_consolid in consolid_pj.items():
                by_proj = {str(proj).strip():[x for x in dd_consolid if str(x[2]).strip().lower() == str(proj).strip().lower()] for proj in list(set([x[2] for x in dd_consolid]))}                               
            
                #DESTINO, NOME_COLAB, LIST_VALORES, TXT_TEMPORARIO, NAME_ARQUIVO
                enviar_email(destino='processos.eucatur@gmail.com',  nome_colab=name_colab, list_valores=by_proj)

                sleep(1)
            st.rerun()

    else:
        st.error('NÃO HÁ PRÊMIOS PARA SEREM CONSOLIDADOS')
                    