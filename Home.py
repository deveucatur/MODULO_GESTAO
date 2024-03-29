import streamlit as st
from utilR import font_TITLE, ninebox_home, css_9box_home, nineboxDatasUnidades_home
from time import sleep
import streamlit_authenticator as stauth
from utilR import menuProjeuHtml, menuProjeuCss
from conexao import conexaoBD
import datetime
from PIL import Image

icone = Image.open('imagens/LogoProjeu.png')
st.set_page_config(
    layout="wide", 
    initial_sidebar_state='collapsed',
    page_icon=icone)

conexao = conexaoBD()

def cardMyProject(nome_user, dados_user):
    param = ['Atividades', 'Entregues', 'Horas Total', 'Complexidade']
    css = '''
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@200;300;400;500;600&display=swap');
    
    .card {
        font-family: Poppins, sans-serif;
        background-color: #ffffff;
        border-radius: 10px;
        padding: 13px;
        width: 100%;
        margin: 20px auto;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        max-width: 100%; 
    }

    .linha1 {
        font-size: 30px;
        text-align: left;
        margin-bottom: 10px;
    }

    .titulos2 {
        font-size: 12px;
        opacity: 60%
    }

    p {
        margin: 0%;
    }

    .linha2 {
        display: flex;
    }

    .coluna {
        flex: 1;
        background-color:#ffffff;
        padding: 0%;
    }
    .coluna p{
        font-size: 29px;    
    }
    '''

    html = f'''
    <body>
        <div class="card">
            <div class="linha1">
            <p style="font-size: 12px; opacity: 60%;">Nome</p>
            {nome_user}
            </div>
            <div class="linha2">'''
    
    for a in range(len(param)):
        html += f"""
                <div class="coluna">
                    <div class="titulos2">{param[a]}</div>
                    <p>{dados_user[a]}</p>
                </div>"""

    html += ''' 
            </div>
        </div>
    </body>'''    

    st.write(f'<style>{css}</style>', unsafe_allow_html=True)
    st.write(html, unsafe_allow_html=True)
        
def botao1(nomeBotao, link, image_path):
    st.markdown(
        f"""
        <style>
        .botao-estiloso {{
            text-decoration: none;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            background-color: #fff;
            padding: 12px 35px;
            text-align: center;
            font-size: 15px;
            border-radius: 10px;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
            max-width: 100%;
            border-radius: 20px;
            transition: background-color 0.5s ease;
        }}
        .botao-estiloso:hover {{
            background: linear-gradient(to bottom, #e990ff, #f2bcff, #fbeaff);
            border-radius: 20px;
        }}
        .botao-imagem {{
            height: 50px;
            width: 50px;
            margin-bottom: 10px;
        }}

        .botao-texto {{
            font-weight: bold;
            color: black;
        }}
            
        </style>
        <a href="{link}" target="_self" class="botao-estiloso" style="color: inherit; text-decoration: none;">
            <img src="{image_path}" class="botao-imagem">
            <span class="botao-texto">{nomeBotao}</span>
        </a>
        """,
        unsafe_allow_html=True
    )


fonte_Projeto = '''@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Bungee+Inline&family=Koulen&family=Major+Mono+Display&family=Passion+One&family=Sansita+Swashed:wght@500&display=swap');
'''

mycursor = conexao.cursor()

setSession = "SET SESSION group_concat_max_len = 5000;"
mycursor.execute(setSession)

# sqlProjetoLider = f"""SELECT p.name_proj, p.id_proj FROM projeu_projetos p JOIN projeu_complexidade c ON p.id_proj = c.proj_fgkey WHERE c.check_lider IS NULL OR c.check_lider = 0 GROUP BY p.id_proj;"""
# mycursor.execute(sqlProjetoLider)
# projetoNomeLider = mycursor.fetchall()

# sqlProjetoGover = f"""
# SELECT 
# 	p.name_proj, 
#     p.id_proj
# FROM 
# 	projeu_projetos p 
# JOIN projeu_complexidade c ON p.id_proj = c.proj_fgkey 
# WHERE c.check_govern IS NULL OR c.check_govern = 0 
# GROUP BY p.id_proj; """
# mycursor.execute(sqlProjetoGover)
# projetoNomeGover = mycursor.fetchall()

sqlProjetoAvaliar = f"""SELECT p.name_proj, p.id_proj, type_proj_fgkey FROM projeu_projetos p JOIN projeu_complexidade c ON p.id_proj = c.proj_fgkey WHERE c.check_avaliado IS NULL OR c.check_avaliado = 0 GROUP BY p.id_proj;"""
mycursor.execute(sqlProjetoAvaliar)
projetoAvaliar = mycursor.fetchall()

sqlCanva = f"""SELECT 
	id_proj, 
	name_proj, 
    produto_entrega_final, 
    nome_mvp, produto_mvp, 
    (
		SELECT 
			GROUP_CONCAT(name_metric SEPARATOR '~/>') 
		FROM projeu_metricas 
        WHERE id_prj_fgkey = projeu_projetos.id_proj
	) AS metricas, 
    result_esperad, 
    (
        SELECT 
            GROUP_CONCAT(Nome SEPARATOR '~/>') 
        FROM projeu_users 
        WHERE id_user IN (
                            SELECT 
                                id_colab 
                            FROM 
                                projeu_registroequipe 
                            WHERE 
                                projeu_registroequipe.id_projeto = projeu_projetos.id_proj)
    ) AS colaborador, 
    (
        SELECT 
            GROUP_CONCAT(papel SEPARATOR '~/>') 
        FROM 
            projeu_registroequipe 
        WHERE 
            projeu_registroequipe.id_projeto = projeu_projetos.id_proj
    ) AS papel, 
    (
        SELECT 
            GROUP_CONCAT(entreg SEPARATOR '~/>') 
        FROM 
            projeu_princEntregas 
        WHERE id_proj_fgkey = projeu_projetos.id_proj
    ) AS entregas,
    investim_proj,
    PM.macroprocesso,
    PP.nome_prog
FROM projeu_projetos
JOIN 
    projeu_macropr PM ON PM.id = projeu_projetos.macroproc_fgkey
JOIN 
    projeu_programas PP ON PP.id_prog = projeu_projetos.progrm_fgkey;"""
mycursor.execute(sqlCanva)
dadosCanva = mycursor.fetchall()

comandUSERS = "SELECT * FROM projeu_users WHERE perfil_proj in ('A', 'L', 'GV') AND status_user = 'A';"
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

    matriUser = [x[1] for x in dadosUser if x[3] == username][0]
    perfilUsuario = [x[8] for x in dadosUser if str(x[1]).strip() == str(matriUser).strip()][0]
    user = [x[2] for x in dadosUser if x[3] == username][0]

    primeiroNome = user.split()[0]

    menuHtml = menuProjeuHtml(primeiroNome)
    menuCss = menuProjeuCss()
    st.write(f'<div>{menuHtml}</div>', unsafe_allow_html=True)
    st.write(f'<style>{menuCss}</style>', unsafe_allow_html=True)

    font_TITLE('HOME', fonte_Projeto,"'Bebas Neue', sans-serif", 42, 'left')

    sqlEntregas = f"""SELECT 
            projeu_entregas.id_sprint, 
            projeu_entregas.nome_Entrega, 
            projeu_entregas.executor, 
            projeu_entregas.stt_entrega,
            projeu_sprints.number_sprint,
            projeu_projetos.name_proj
        FROM projeu_entregas
        JOIN projeu_sprints ON projeu_entregas.id_sprint = projeu_sprints.id_sprint
        JOIN projeu_projetos ON projeu_sprints.id_proj_fgkey = projeu_projetos.id_proj
        WHERE projeu_entregas.stt_entrega NOT LIKE '%Concluído%' AND projeu_entregas.executor = {matriUser};"""
    mycursor.execute(sqlEntregas)
    entregaProj = mycursor.fetchall()
    mycursor.close()

    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("")
        nomeBotão = "DASHBOARD"
        link = "https://943d-186-232-176-19.ngrok-free.app/Dashboard"
        image_url=  "https://cdn-icons-png.flaticon.com/128/4882/4882406.png"
        botao1(nomeBotão,link,image_url)
    with col2:
        st.write("")
        nomeBotão = "PORTFÓLIO"
        link = 'https://943d-186-232-176-19.ngrok-free.app/Portfólio'
        image_url=  "https://cdn-icons-png.flaticon.com/128/3222/3222498.png"
        botao1(nomeBotão,link,image_url)
    with col3:    
        st.write("")
        nomeBotão = 'PRÊMIOS'
        link = 'https://943d-186-232-176-19.ngrok-free.app/Gestão_de_Prêmios'
        image_url="https://cdn-icons-png.flaticon.com/128/5517/5517593.png"
        botao1(nomeBotão,link,image_url)

    st.text(' ')

    col1, col2 = st.columns([1, 1.7])
    with col1:    
        # ddbox = [[], [['Projeto para teste', 'Projeto Teste 2', 'teste teste projeto 123']]]
        # links = [None, None, None]
        # img_doc = '''https://cdn-icons-png.flaticon.com/128/2665/2665632.png'''
        
        # html1 = ninebox_home(0, nineboxDatasUnidades_home(ddbox, links), ddbox, 'Ranking de Projetos', links, img_doc)
        # ninebox_style = css_9box_home()
        # st.write(f'<style>{ninebox_style}</style>', unsafe_allow_html=True)
        # st.write(f'<div>{html1}</div>', unsafe_allow_html=True) 
        
        links = ["https://drive.google.com/file/d/1HitZgZkpMxlpj6_hDVlnTdg8ja_uuZYJ/view?usp=sharing", "https://drive.google.com/file/d/1TL-H33TrjgwdBM_eUD8gA9udqNNkkYrw/view?usp=sharing", "https://drive.google.com/file/d/1Wiz1EoiHNrZw4exVUdNVaWlN7AXH_Q3x/view?usp=sharing", "https://drive.google.com/file/d/1IjKIIIfFqZcFSKddc3ZWFnxrwdmlZznS/view?usp=sharing"]
        img_doc = 'https://cdn-icons-png.flaticon.com/128/6802/6802306.png'
        matApoio = [[], [['Manual do gestor de projeto', 'Práticas de idealização, Planejamento, Implantação e Avaliação de Projetos', 'Política - Gerenciamento do portfólio de projetos', 'Produto MVP-Final']]]

        html1 = ninebox_home(0, nineboxDatasUnidades_home(matApoio, links), matApoio, 'Material de Apoio', links, img_doc)
        ninebox_style = css_9box_home()
        st.write(f'<style>{ninebox_style}</style>', unsafe_allow_html=True)
        st.write(f'<div>{html1}</div>', unsafe_allow_html=True)

        

    with col2:
        font_TITLE('Atividades Pendentes', fonte_Projeto,"'Bebas Neue', sans-serif", 25, 'left')
        if str(perfilUsuario).upper() in ['A']:
            if len(projetoAvaliar) == 'None' or len(projetoAvaliar) <= 0:
                st.info("Você não possui atividades pendentes no momento.")

            for i in range(len(projetoAvaliar)):
                with st.expander(f"Avaliar Complexidade | {projetoAvaliar[i][0]}"):
                    if projetoAvaliar[i][2] != 3:
                        titleClass = ["Orientação do Projeto", "Impacto do Projeto", "Escopo do Projeto", "Squads do Projeto"]
                        infoClass = [["Orientação para Inovação em Produtos/Serviços  atuais", "Orientação para desenvolvimento de novos Produtos/Serviços", "Orientação para Aumento de Receita", "Orientação para Aumento de Produtividade", "Orientação para Redução de Custos/Despesas", "Orientação para Transformação de processos de Negócio"],["Impacto na Percepção de Valor do Cliente", "Pressão Por Prazos", "Investimento necessário", "Nível de transformação organizacional", "Valor para o Negócio"],["Impacto do escopo no Planejamento Estratégico", "Incerteza do escopo", "Complexidade  do escopo"], ["Senioridade da Squad", "Senioridade do Especialista", "Senioridade do Gestor do Projeto"]]
                        optionClass = [["1 - Nenhum(a)", "2 - Baixo(a)", "3 - Médio(a)", "4 - Forte"]] * 17
                    else:
                        titleClass = ["Foco do Projeto", "Impacto do Projeto", "Escopo do Projeto", "Maturidade da Squad"]
                        infoClass = [["Aumento de Receita", "Aumento de Produtividade", "Redução de custos/despesa"], ["Cadeia de Valor", "Nivel de Transformação", "Nivel de Integração entre pessoas"], ["Depedência de Fornecedor externo", "Incerteza Tecnológica", "Riscos e Restrições", "Marco"], ["Gestor do Projeto", "Especialista", "Squad"]]
                        optionClass = [[["1 - Nenhum(a)", "2 - Baixo(a)", "3 - Médio(a)", "4 - Forte"], ["1 - Nenhum(a)", "2 - Baixo(a)", "3 - Médio(a)", "4 - Forte"], ["1 - Nenhum(a)", "2 - Baixo(a)", "3 - Médio(a)", "4 - Forte"]], [["1 - Procedimento", "2 - Processo", "3 - Marco Processo", "4 - Toda a Cadeia"], ["1 - Nenhum(a)", "2 - Baixo(a)", "3 - Médio(a)", "4 - Forte"], ["1 - Nenhum(a)", "2 - Baixo(a)", "3 - Médio(a)", "4 - Forte"]], [["1 - Forte", "2 - Médio(a)", "3 - Baixo(a)", "4 - Nenhum(a)"], ["1 - Forte", "2 - Médio(a)", "3 - Baixo(a)", "4 - Nenhum(a)"], ["1 - Fortíssimo", "2 - Forte", "3 - Médio(a)", "4 - Baixo(a)"], ["1 - 3 Marco", "2 - 5 Marco", "3 - 7 Marco", "4 - 8 Marco"]], [["1 - Baixo(a)", "2 - Médio(a)", "3 - Forte", "4 - Fortíssimo"], ["1 - Baixo(a)", "2 - Médio(a)", "3 - Forte", "4 - Fortíssimo"], ["1 - Baixo(a)", "2 - Médio(a)", "3 - Forte", "4 - Fortíssimo"]]]

                    font_TITLE(f'{projetoAvaliar[i][0]}', fonte_Projeto, "'Bebas Neue', sans-serif", 30, 'center')

                    canva = [x for x in dadosCanva if x[1] == projetoAvaliar[i][0]][0]
                    listaEquipe = []
                    gestores = []
                    especialistas = []
                    squads = []

                    projetos = [canva[1]] if canva[1] != None else " "
                    mvps = [canva[3]] if canva[3] != None else " "
                    prodProjetos = [canva[2]] if canva[2] != None else " "
                    prodMvps = [canva[4]] if canva[4] != None else " "
                    resultados = [canva[6]] if canva[6] != None else " "
                    metricas = [canva[5]] if canva[5] != None else " "
                    
                    for j in range(len(canva[7].split('/>'))):
                        colab = str(canva[7]).split('~/>')[j]
                        funcao = str(canva[8]).split('~/>')[j]
                        listaEquipe.append([colab, funcao])

                    for j in range(len(listaEquipe)):
                        if listaEquipe[j][1] == "Gestor":
                            gest = listaEquipe[j][0]
                            listaEquipe.append(gest)
                            gestores.append(gest)
                        elif listaEquipe[j][1] == "Especialista":
                            espec = listaEquipe[j][0]
                            listaEquipe.append(espec)
                            especialistas.append(espec)
                        else:
                            executor = listaEquipe[j][0]
                            listaEquipe.append(executor)
                            squads.append(executor)
                    if len(gestores) == 0:
                        gestores = " "
                    if len(especialistas) == 0:
                        especialistas = " "
                    if len(squads) == 0:
                        squads = " "

                    entregas = str(canva[9]).split(';') if ';' in str(canva[9]) else str(canva[9]).split('~/>')
                    investimentos = [canva[10]] if canva[10] != None else " "

                    col1, col2, col3 = st.columns([1,1,0.6])
                    with col1:
                        st.text_input('Gestor', gestores[0], key=f'{projetos} 1')
                    with col2:
                        st.text_input('Macroprocesso', canva[11], key=f'{projetos} 2')#MACROPROCESSO
                    with col3:
                        st.text_input('Investimento', investimentos[0], key=f'{projetos} 6')
                        
                    st.text_input('Programa', canva[12], key=f'{projetos} 3')#PROGRAMA
                    st.text_input('MVP', mvps[0], key=f'{projetos} 4')
                    
                    col1, col2 = st.columns([3,2])
                    with col1:
                        st.multiselect('Squad', squads, squads, disabled=True, key=f'{projetos} 9')
                    with col2:
                        st.text_input('Especialistas', str(especialistas).replace("[","").replace("]","").replace("'", ""), key=f'{projetos} 7')
                    
                    font_TITLE(f'Principais Entregas', fonte_Projeto,"'Bebas Neue', sans-serif", 21, 'left')
                    for entrg_idx in range(len(entregas)):
                        st.text_input('Entregas', entregas[entrg_idx], label_visibility='collapsed', key=f'entregas nomes{entrg_idx} {projetos[0]}')

                    notaGrau = []
                    for j in range(len(titleClass)):
                        font_TITLE(f'{titleClass[j]}', fonte_Projeto,"'Bebas Neue', sans-serif", 24, 'left')
                        listNota = []
                        for k in range(len(infoClass[j])):
                            if projetoAvaliar[i][2] != 3:
                                nota = int(st.select_slider(infoClass[j][k], optionClass[j], key=f"chave{i}_{j}_{k}", value=optionClass[j][0])[0][0:1])
                            else:
                                nota = int(st.select_slider(infoClass[j][k], optionClass[j][k], key=f"chave{i}_{j}_{k}", value=optionClass[j][k][0])[0][0:1])

                            listNota.append(nota)
                            st.text(' ')
                            st.text(' ')
                        notaGrau.append(listNota)

                    if projetoAvaliar[i][2] != 3:
                        mediaImpacto = round(sum(notaGrau[1]) / len(notaGrau[1]), 2)
                        maiorOrientacao = max(notaGrau[0])
                        grauProjeto = round(((mediaImpacto + maiorOrientacao) / 2), 2)
                        
                        grauEscopo = round(sum(notaGrau[2]) / len(notaGrau[2]), 2)
                        grauSquad = round(sum(notaGrau[3]) / len(notaGrau[3]), 2)
                        mediaGov = round(((grauEscopo + grauSquad) / 2), 2)
                        
                        if grauProjeto == 0:
                            complexidade = ""
                        elif grauProjeto <= 1:
                            complexidade = "Seguro"
                        elif grauProjeto <= 2:
                            complexidade = "Acessível"
                        elif grauProjeto <= 3:
                            complexidade = "Abstrato"
                        elif grauProjeto <= 4:
                            complexidade = "Singular"
                        else:
                            complexidade = "Valor inválido"

                        if mediaGov == 0:
                            nivel = ""
                        elif mediaGov <= 2:
                            nivel = "I"
                        elif mediaGov <= 3:
                            nivel = "II"
                        elif mediaGov <= 4:
                            nivel = "III"
                        else:
                            nivel = "Valor inválido"
                    else:
                        mediaFoco = round(sum(notaGrau[0]) / len(notaGrau[0]), 2)
                        mediaImpacto = round(sum(notaGrau[1]) / len(notaGrau[1]), 2)
                        mediaEscopo = round(sum(notaGrau[2]) / len(notaGrau[2]), 2)
                        mediaMaturidade = round(sum(notaGrau[3]) / len(notaGrau[3]), 2)

                        mediaComplex = round((mediaFoco + mediaImpacto) / 2, 2)
                        mediaNivel = round((mediaEscopo + mediaMaturidade) / 2, 2)

                        if mediaComplex == 0:
                            complexidade = " "
                        elif mediaComplex <= 1.5:
                            complexidade = "Incremental"
                        elif mediaComplex <= 2.5:
                            complexidade = "Radical"
                        elif mediaComplex <= 4:
                            complexidade = "Disruptiva"
                        else:
                            complexidade = "Valor inválido"

                        if mediaNivel == 0:
                            nivel = " "
                        elif mediaNivel <= 1.5:
                            nivel = "I"
                        elif mediaNivel <= 2.5:
                            nivel = "II"
                        elif mediaNivel <= 4:
                            nivel = "III"
                        else:
                            nivel = "Valor inválido"

                    st.write("---")
                    st.info(f"Complexidade: {complexidade} {nivel}")

                    finalizar = st.button("Finalizar avaliação", key=f"notaLider_{i}")

                    if finalizar:
                        mycursor = conexao.cursor()
                        dataEdic = datetime.datetime.now().date()
                        if projetoAvaliar[i][2] != 3:
                            colunas = ["grauProjeto", "complxdd", "check_lider", "grauEscopo", "grauSquad", "nivel", "check_govern", "id_edic_fgkey", "check_avaliado", "date_edic"]
                            dados = [grauProjeto, f"'{complexidade}'", 1, grauEscopo, grauSquad, f"'{nivel}'", 1, matriUser, 1, f"'{dataEdic}'"]
                        else:
                            colunas = ["grauFoco", "grauImpacto", "complxdd", "check_lider", "grauEscopo", "grauSquad", "nivel", "check_govern", "id_edic_fgkey", "check_avaliado", "date_edic"]
                            dados = [mediaFoco, mediaImpacto, f"'{complexidade}'", 1, mediaEscopo, mediaMaturidade, f"'{nivel}'", 1, matriUser, 1, f"'{dataEdic}'"]

                        for j in range(len(colunas)):
                            sqlUpdate = f"UPDATE projeu_complexidade SET {colunas[j]} = {dados[j]} WHERE proj_fgkey = {projetoAvaliar[i][1]}"
                            mycursor.execute(sqlUpdate)
                            conexao.commit()
                        st.toast('Dados Atualizados!', icon='✅')
                        sleep(1)
                        st.rerun()

        #     for k in range(len(projetoNomeLider)):
        #         with st.expander(f"Avaliar Complexidade | {projetoNomeLider[k][0]}"):
        #             titleClass = ["Orientação do Projeto", "Impacto do Projeto"]
        #             infoClass = [["Orientação para Inovação em Produtos/Serviços  atuais", "Orientação para desenvolvimento de novos Produtos/Serviços", "Orientação para Aumento de Receita", "Orientação para Aumento de Produtividade", "Orientação para Redução de Custos/Despesas", "Orientação para Transformação de processos de Negócio"],["Impacto na Percepção de Valor do Cliente", "Pressão Por Prazos", "Investimento necessário", "Nível de transformação organizacional", "Valor para o Negócio"]]
        #             optionClass = ["1 - Nenhum(a)", "2 - Baixo(a)", "3 - Médio(a)", "4 - Forte"]

        #             font_TITLE(f'{projetoNomeLider[k][0]}', fonte_Projeto,"'Bebas Neue', sans-serif", 30, 'center')

        #             canva = [x for x in dadosCanva if x[1] == projetoNomeLider[k][0]][0]
        #             listaEquipe = []
        #             gestores = []
        #             especialistas = []
        #             squads = []

        #             projetos = [canva[1]] if canva[1] != None else " "
        #             mvps = [canva[3]] if canva[3] != None else " "
        #             prodProjetos = [canva[2]] if canva[2] != None else " "
        #             prodMvps = [canva[4]] if canva[4] != None else " "
        #             resultados = [canva[6]] if canva[6] != None else " "
        #             metricas = [canva[5]] if canva[5] != None else " "
        #             for i in range(len(canva[7].split('~/>'))):
        #                 colab = str(canva[7]).split('~/>')[i]
        #                 funcao = str(canva[8]).split('~/>')[i]
        #                 listaEquipe.append([colab, funcao])

        #             for i in range(len(listaEquipe)):
        #                 if listaEquipe[i][1] == "Gestor":
        #                     gest = listaEquipe[i][0]
        #                     listaEquipe.append(gest)
        #                     gestores.append(gest)
        #                 elif listaEquipe[i][1] == "Especialista":
        #                     espec = listaEquipe[i][0]
        #                     listaEquipe.append(espec)
        #                     especialistas.append(espec)
        #                 else:
        #                     executor = listaEquipe[i][0]
        #                     listaEquipe.append(executor)
        #                     squads.append(executor)
        #             if len(gestores) == 0:
        #                 gestores = " "
        #             if len(especialistas) == 0:
        #                 especialistas = " "
        #             if len(squads) == 0:
        #                 squads = " "

        #             entregas = str(canva[9]).split(';') if ';' in str(canva[9]) else str(canva[9]).split('~/>')
        #             investimentos = [canva[10]] if canva[10] != None else " "

        #             col1, col2, col3 = st.columns([1,1,0.6])
        #             with col1:
        #                 st.text_input('Gestor', gestores[0], key=f'{projetos} 1')
        #             with col2:
        #                 st.text_input('Macroprocesso', canva[11], key=f'{projetos} 2')#MACROPROCESSO
        #             with col3:
        #                 st.text_input('Investimento', investimentos[0], key=f'{projetos} 6')
                        
        #             st.text_input('Programa', canva[12], key=f'{projetos} 3')#PROGRAMA
        #             st.text_input('MVP', mvps[0], key=f'{projetos} 4')
                    
        #             col1, col2 = st.columns([3,2])
        #             with col1:
        #                 st.multiselect('Squad', squads, squads, disabled=True, key=f'{projetos} 9')
        #             with col2:
        #                 st.text_input('Especialistas', str(especialistas).replace("[","").replace("]","").replace("'", ""), key=f'{projetos} 7')
                    
        #             font_TITLE(f'Principais Entregas', fonte_Projeto,"'Bebas Neue', sans-serif", 21, 'left')
        #             for entrg_idx in range(len(entregas)):
        #                 st.text_input('Entregas', entregas[entrg_idx], label_visibility='collapsed', key=f'entregas nomes{entrg_idx} {projetos[0]}')

        #             notaGrau = []
        #             for i in range(len(titleClass)):
        #                 font_TITLE(f'{titleClass[i]}', fonte_Projeto,"'Bebas Neue', sans-serif", 24, 'left')
        #                 listNota = []
        #                 for j in infoClass[i]:
        #                     nota = int(st.select_slider(j, optionClass, key=f"chave{k}_{i}_{j}", value=optionClass[0])[0][0:1])
        #                     listNota.append(nota)
        #                     st.text(' ')
        #                     st.text(' ')
        #                 notaGrau.append(listNota)
        #             mediaImpacto = round(sum(notaGrau[1]) / len(notaGrau[1]), 2)
        #             maiorOrientacao = max(notaGrau[0])
        #             grauProjeto = round(((mediaImpacto + maiorOrientacao) / 2), 2)
                    
        #             if grauProjeto == 0:
        #                 complexidade = ""
        #             elif grauProjeto <= 1:
        #                 complexidade = "Seguro"
        #             elif grauProjeto <= 2:
        #                 complexidade = "Acessível"
        #             elif grauProjeto <= 3:
        #                 complexidade = "Abstrato"
        #             elif grauProjeto <= 4:
        #                 complexidade = "Singular"
        #             else:
        #                 complexidade = "Valor inválido"

        #             finalizar = st.button("Finalizar avaliação", key=f"notaLider_{k}")

        #             if finalizar:
        #                 mycursor = conexao.cursor()
        #                 colunas = ["grauProjeto", "complxdd", "check_lider", "id_edic_fgkey"]
        #                 dadosLider = [grauProjeto, f"'{complexidade}'", 1, matriUser]

        #                 for i in range(len(colunas)):
        #                     sqlUpdate = f"UPDATE projeu_complexidade SET {colunas[i]} = {dadosLider[i]} WHERE proj_fgkey = {projetoNomeLider[k][1]}"
        #                     mycursor.execute(sqlUpdate)
        #                     conexao.commit()
        #                 st.toast('Dados Atualizados!', icon='✅')
        #                 sleep(3)
        #                 st.rerun()

        # if str(perfilUsuario).strip().upper() in ['GV', 'A']:
        #     if projetoNomeGover == None or len(projetoNomeGover) <= 0:
        #         st.info("Você não possui atividades pendentes no momento.")

            
        #     for k in range(len(projetoNomeGover)):
        #         with st.expander(f"Avaliar Complexidade | {projetoNomeGover[k][0]} - Governança"):
        #             titleClass = ["Escopo do Projeto", "Squads do Projeto"]
        #             infoClass = [["Impacto do escopo no Planejamento Estratégico", "Incerteza do escopo", "Complexidade  do escopo"], ["Senioridade da Squad", "Senioridade do Especialista", "Senioridade do Gestor do Projeto"]]
        #             optionClass = ["1 - Nenhum(a)", "2 - Baixo(a)", "3 - Médio(a)", "4 - Forte"]

        #             font_TITLE(f'{projetoNomeGover[k][0]}', fonte_Projeto,"'Bebas Neue', sans-serif", 23, 'center')

        #             st.text(' ')
        #             canva = [x for x in dadosCanva if x[1] == projetoNomeGover[k][0]][0]
                    
        #             listaEquipe = []
        #             gestores = []
        #             especialistas = []
        #             squads = []

        #             projetos = [canva[1]] if canva[1] != None else " "
        #             mvps = [canva[3]] if canva[3] != None else " "
        #             prodProjetos = [canva[2]] if canva[2] != None else " "
        #             prodMvps = [canva[4]] if canva[4] != None else " "
        #             resultados = [canva[6]] if canva[6] != None else " "
        #             metricas = [canva[5]] if canva[5] != None else " "
        #             for i in range(len(canva[7].split('~/>'))):
        #                 colab = str(canva[7]).split('~/>')[i]
        #                 funcao = str(canva[7]).split('~/>')[i]
        #                 listaEquipe.append([colab, funcao])

        #             for i in range(len(listaEquipe)):
        #                 if listaEquipe[i][1] == "Gestor":
        #                     gest = listaEquipe[i][0]
        #                     listaEquipe.append(gest)
        #                     gestores.append(gest)
        #                 elif listaEquipe[i][1] == "Especialista":
        #                     espec = listaEquipe[i][0]
        #                     listaEquipe.append(espec)
        #                     especialistas.append(espec)
        #                 else:
        #                     executor = listaEquipe[i][0]
        #                     listaEquipe.append(executor)
        #                     squads.append(executor)
        #             if len(gestores) == 0:
        #                 gestores = " "
        #             if len(especialistas) == 0:
        #                 especialistas = " "
        #             if len(squads) == 0:
        #                 squads = " "

        #             entregas = str(canva[9]).split(';') if ';' in str(canva[9]) else str(canva[9]).split('~/>')
        #             investimentos = [canva[10]] if canva[10] != None else " "

        #             col1, col2, col3 = st.columns([1,1,0.6])
        #             with col1:
        #                 st.text_input('Gestor', gestores, key=f'Gestor{projetos[0]} 1')
        #             with col2:
        #                 st.text_input('Macroprocesso', canva[11], key=f'{projetos[0]} 2')#MACROPROCESSO
        #             with col3:
        #                 st.text_input('Investimento', investimentos[0], key=f'{projetos[0]} 6')
                        
        #             st.text_area('Programa', canva[12], key=f'{projetos[0]} 3')#PROGRAMA
        #             st.text_input('MVP', mvps[0], key=f'{projetos[0]} 4')
                    
        #             col1, col2 = st.columns([3,2])
        #             with col1:
        #                 st.multiselect('Squad', squads, squads, disabled=True, key=f'{projetos[0]} 9')
        #             with col2:
        #                 st.text_input('Especialistas', especialistas, key=f'{projetos[0]} 7')
                    
        #             font_TITLE(f'Principais Entregas', fonte_Projeto,"'Bebas Neue', sans-serif", 21, 'left')
        #             for entrg_idx in range(len(entregas)):
        #                 st.text_input('Entregas', entregas[entrg_idx], label_visibility='collapsed', key=f'entrega{entrg_idx} {projetos[0]} 5')
    
        #             st.text(' ')
        #             notaGov = []
        #             for i in range(len(titleClass)):
        #                 font_TITLE(f'{titleClass[i]}', fonte_Projeto,"'Bebas Neue', sans-serif", 21, 'left')
        #                 listNota = []
        #                 for j in infoClass[i]:
        #                     nota = int(st.select_slider(j, optionClass, key=f"chave{k}_{i}_{j}", value=optionClass[0])[0][0:1])
        #                     listNota.append(nota)
        #                     st.write("---")
        #                 notaGov.append(listNota)
        #             grauEscopo = round(sum(notaGov[0]) / len(notaGov[0]), 2)
        #             grauSquad = round(sum(notaGov[1]) / len(notaGov[1]), 2)
        #             mediaGov = round(((grauEscopo + grauSquad) / 2), 2)

        #             if mediaGov == 0:
        #                 nivel = ""
        #             elif mediaGov <= 2:
        #                 nivel = "I"
        #             elif mediaGov <= 3:
        #                 nivel = "II"
        #             elif mediaGov <= 4:
        #                 nivel = "III"
        #             else:
        #                 nivel = "Valor médio fora do intervalo válido"

        #             finalizar = st.button("Finalizar avaliação", key=f"notaGovernanca_{k}")

        #             if finalizar:
        #                 mycursor = conexao.cursor()
        #                 colunas = ["grauEscopo", "grauSquad", "nivel", "check_govern", "id_edic_fgkey"]
        #                 dadosGover = [grauEscopo, grauSquad, f"'{nivel}'", 1, matriUser]

        #                 for i in range(len(colunas)):
        #                     sqlUpdate = f"UPDATE projeu_complexidade SET {colunas[i]} = {dadosGover[i]} WHERE proj_fgkey = {projetoNomeGover[k][1]}"
        #                     mycursor.execute(sqlUpdate)
        #                     conexao.commit()
        #                 st.toast('Dados Atualizados!', icon='✅')
        #                 sleep(3)
        #                 st.rerun()
        else:
            if entregaProj == 'None' or len(entregaProj) <= 0:
                st.info("Você não possui atividades pendentes no momento.")

        for i in range(len(entregaProj)):
            cardEntregaHtml = f"""<div class="main">
                    <div class="card">
                        <div class="sprint">Sprint {str(entregaProj[i][4])}</div>
                        <div class="entrega">Entrega: {entregaProj[i][1]}</div>
                        <div class="status">Status: {entregaProj[i][3]}</div>
                    </div>
                </div>"""
            
            cardEntregaCss = """.main{
                    display: flex;
                    align-items: center;
                }

                .card{
                    max-width: 100%;
                    min-width: 100%;
                }

                .card:hover{
                    transform: scale(1.03);
                }

                .sprint{
                    font-size: 18px;
                    font-weight: bold;
                }

                .entrega{
                    margin-top: 10px;
                    font-size: 16px;
                }

                .status{
                    margin-top: 10px;
                    font-size: 16px;
                }"""
            
            with st.expander(f"{str(entregaProj[i][5])} || {entregaProj[i][1]}"):
                st.write(f"{cardEntregaHtml}", unsafe_allow_html=True)
                st.write(f"<style>{cardEntregaCss}<style>", unsafe_allow_html=True)
