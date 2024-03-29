import streamlit as st
from datetime import datetime

fonte = '''<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Passion+One&display=swap" rel="stylesheet">'''

fonte2 = '''<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Koulen&family=Passion+One&display=swap" rel="stylesheet">'''

fonte3 = '''<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bungee+Inline&family=Koulen&family=Passion+One&display=swap" rel="stylesheet">'''

fonte4 = '''@import url('https://fonts.googleapis.com/css2?family=Bungee+Inline&family=Koulen&family=Passion+One&family=Sansita+Swashed:wght@500&display=swap');'''


def string_to_datetime(string):
    date = datetime.strptime(str(string), "%Y-%m-%d").date()
    return date


def date_americ_by_brasil(data):
    data_aux = str(data)
    data_obj = datetime.strptime(data_aux, "%Y-%m-%d")

    data_formatada = data_obj.strftime("%d/%m/%Y")

    return data_formatada


def font_TITLE(texto, fonte, fonte1, tam_font, text_alinham = None, cor = 'gray11'):
#FONTE = URL DA FONTE
#FONTE1 = NOME DA FONTE DA QUE ESTÁ SENDO IMPORTADA
    css1 = f"""
        <style>
            {fonte} 
            .gold-text{tam_font} {{
                font-size: {tam_font}px;
                color: {cor};
                text-align: {text_alinham};
                margin-bottom: 0px;
            }}
            .custom-font{tam_font} {{
                font-family: {fonte1} 
            }}
        </style>"""

    st.markdown(css1, unsafe_allow_html=True)
    st.markdown(f'<p class="gold-text{tam_font} custom-font{tam_font}">{texto}</p>', unsafe_allow_html=True)


def card_traspent():
    html ="""<div class="cardContainer">
    <div class="card">
    <p class="city">PINK CITY</p>
    <p class="weather">PARTILY CLOUDY</p>
    <svg xml:space="preserve" viewBox="0 0 100 100" height="50px" width="50px" y="0px" x="0px" id="Layer_1" version="1.1" class="weather">  <image href="data:image/png;base64,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" y="0" x="0" height="100" width="100" id="image0"></image>
        </svg>
        <p class="temp">32°</p>
        <div class="minmaxContainer">
        <div class="min">
            <p class="minHeading">Min</p>
            <p class="minTemp">30°</p>
        </div>
        <div class="max"><p class="maxHeading">Max</p>
            <p class="maxTemp">32°</p></div>
        </div>
        
    </div>
    </div>""" 

    css=""".cardContainer {
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    }

    .card {
    position: relative;
    width: 220px;
    height: 170px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: space-between;
    padding: 20px 10px;
    border-radius: 10px;
    backdrop-filter: blur(30px);
    background-color: rgba(65, 65, 65, 0.308);
    border: 1px solid rgba(255, 255, 255, 0.089);
    cursor: pointer;
    }

    .city {
    font-weight: 700;
    font-size: 0.9em;
    letter-spacing: 1.2px;
    color: white;
    }

    .weather {
    font-weight: 500;
    font-size: 0.7em;
    letter-spacing: 1.2px;
    color: rgb(197, 197, 197);
    }

    .temp {
    font-size: 1.8em;
    color: white;
    }

    .minmaxContainer {
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: space-between;
    }

    .min,.max {
    width: 50%;
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    justify-content: center;
    padding: 0px 20px;
    gap: 4px;
    }

    .max {
    align-items: flex-start;
    border-left: 2px solid white;
    }

    .maxHeading,.minHeading {
    font-size: 0.7em;
    font-weight: 600;
    color: white;
    }

    .maxTemp,.minTemp {
    font-size: 0.6em;
    font-weight: 500;
    color: rgb(197, 197, 197);
    }

    """

    st.write(f"<style>{css}<style>", unsafe_allow_html=True)
    st.write(f"{html}", unsafe_allow_html=True)

def cardImg(image_url):
    st.markdown(
        f"""
        <style>
        .caixa {{
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            background-color: #FFFFFF;
            color: white;
            font-family: ;
            padding: 12px 35px;
            text-align: center;
            text-decoration: none;
            font-size: 15px;
            border-radius: 10px;
            border: 1px solid #ccc; /* Adiciona uma borda de 1px sólida */
            box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.2); /* Adiciona sombreamento */
            transition: background-color 0.3s ease;
        }}
        .botao-imagem {{
            height: 50px;
            width: 50px;
            margin-bottom: 10px;
        }}            
        </style>

        <div target="_self" class="caixa">
            <img src="{image_url}" class="botao-imagem">
        </div>
        """,
        unsafe_allow_html=True
    )

def displayInd(title, valor, min_val, max_val, padding=0.6, id=1):
    max_val = float(max_val)
    # Estilos CSS para a janela
    styleJanela = f'''
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@200;300;400;500;600&display=swap');
    .card{id} {{
        padding: {padding}rem;
        background-color: #fff;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        max-width: 100%;
        border-radius: 20px;
        text-align: center;
    }}

    .title{id} {{
        align-items: center;
    }}

    .title{id}-text {{
    color: #374151;
    font-size: 15px;
    font-family: 'Poppins', sans-serif;
    }}

    .data{id} {{
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
    }}

    .data{id} p {{
        color: #1F2937;
        font-size: 27px;
        line-height: 2.5rem;
        font-weight: 700;
        font-family: 'Poppins', sans-serif;
    }}

    '''

    # HTML da janela
    htmlJanela = f'''
                    <div class="card{id}">
                        <div class="title{id}">
                            <p class="title{id}-text">{title}</p>
                                </div>
                                <div class="data{id}">
                            <p>{valor}</p>
                        </div>
                    </div>
                '''

    st.write(f'<style>{styleJanela}</style>', unsafe_allow_html=True)
    st.write(f'<div>{htmlJanela}</div>', unsafe_allow_html=True)


def cardProject(listProject):
    var_css = """ 
    <style>
    .card {
        background-color: #ffffff;
        box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1), 0px 8px 16px rgba(0, 0, 0, 0.2);
        border-radius: 10px;
        padding: 20px;
        font-family: 'Poppins', sans-serif;
    }

    .card-content {
        margin-bottom: 10px;
        color: #374151;
        font-size: 18px;
    }
    </style>"""

    var_html = '<div class="card">'
    for a in listProject:
        var_html += f'''<div class="card-content">
                        <p>{a}</p>
                    </div>'''
    var_html += '</div>'

    st.write(var_css, unsafe_allow_html=True)
    st.write(f'<body>{var_html}</body>', unsafe_allow_html=True)


def cardGRANDE(title, valor):
    # Estilos CSS para a janela
    styleJanela = '''
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@200;300;400;500;600&display=swap');
    .container {
        display: flex;
        justify-content: space-between;
    }

    .cardG {
        padding: 1.7rem;
        background-color: transparent;
        flex: 1;
        border-radius: 20px;
        text-align: center;
        border-bottom: 2px solid DarkGray;
    }

    .Allcolumms {
        display: flex; 
        justify-content: space-between;
        flex-wrap: wrap;
    }
    
    .titleG {
        align-items: center;
    }

    .titleG-text {
        color: #374151;
        font-size: 12px;
        font-family: 'Poppins', sans-serif;
    }

    .dataG {
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
    }

    .dataG p {
        color: #1F2937;
        font-size: 43px;
        line-height: 2.5rem;
        font-weight: 450;
        font-family: 'Poppins', sans-serif;
    }
    '''


    # HTML da janela
    htmlJanelaText = f'''
    <div class="cardG">
        <div class="Allcolumms">'''
            
    for a in range(len(title)):
        htmlJanelaText += f'''<div style="flex-basis: 105px;">
                                    <div class="titleG">
                                        <p class="titleG-text">{title[a]}</p>
                                    </div>
                                    <div class="dataG">
                                        <p>{valor[a]}</p>
                                    </div>
                                </div>'''

    st.write(f'<style>{styleJanela}</style>', unsafe_allow_html=True)
    st.write(f'{htmlJanelaText}</div></div>', unsafe_allow_html=True)


def cardMyProject(nome_user, dados_user):
    param = ['Atividades', 'Entregues', 'Horas Total', 'Complexidade']
    css = '''
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@200;300;400;500;600&display=swap');
    
    .card {
        color: #1F2937;
        font-family: Poppins, sans-serif;
        background-color: #ffffff;
        border-radius: 20px;
        padding: 30px;
        width: 100%;
        margin: 20px auto;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        max-width: 100%; 
    }

    .linha1 {
        font-size: 27px;
        font-weight: 450; 
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
        flex-wrap: wrap;
    }

    .coluna {
        flex: 1;
        background-color:#ffffff;
        padding: 0%;
        flex-basis: 130px;
    }
    .coluna p{
        font-size: 2.5rem;
        line-height: 2.5rem;
        font-weight: 450;
    }    
    '''

    html = f'''
    <body>
        <div class="card">
            <div class="linha1">
                <p style="font-size: 12px; opacity: 60%;">Name</p>
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


class PlotCanvas:
    def __init__(self, projetos, mvps, prodProjetos, prodMvps, resultados, metricas, gestores, especialistas, squads, entregas, investimentos):
        self.projeto = projetos
        self.mvp = mvps
        self.prodProjeto = prodProjetos
        self.prodMvp = prodMvps
        self.resultado = resultados
        self.metrica = metricas
        self.gestores = gestores
        self.especialistas = especialistas
        self.squads = squads
        self.entregas = entregas
        self.investimentos = investimentos

    def CreateHTML(self):
        metricaCode = ""
        for i in range(len(self.metrica)):
            metricaCode += f"""<tr class="tdata7">
                    <td>{self.metrica[i]}</td>
                </tr>"""

        resultadoCode = ""
        for i in range(len(self.resultado)):
            resultadoCode += f"""<tr class="tdata6">
                    <td>{self.resultado[i]}</td>
                </tr>"""

        projetoCode = ""
        for i in range(len(self.projeto)):
            projetoCode += f"""<tr class="tdata1">
                    <td>{self.projeto[i]}</td>
                </tr>"""
            
        prodProjetoCode = ""
        for i in range(len(self.prodProjeto)):
            prodProjetoCode += f"""<tr class="tdata1">
                                <td>{self.prodProjeto[i]}
                            </tr>"""

        mvpCode = ""
        for i in range(len(self.mvp)):
            mvpCode += f"""<tr class="tdata2">
                    <td>{self.mvp[i]}</td>
                </tr>"""
            
        prodMvpCode = ""
        for i in range(len(self.prodMvp)):
            prodMvpCode += f"""<tr class="tdata2">
                        <td>{self.prodMvp[i]}</td>
                    </tr>"""

        htmlRow = f"""<div class="flex-row">
                <div class="box">
                    <div class="box1">
                        <table class="table1">
                            <tr class="thead1">
                                <th>Projeto<img src="https://cdn-icons-png.flaticon.com/128/10484/10484735.png" alt="Icone da tabela Projetos" class="table-icon"></th>
                            </tr>
                            <div>{projetoCode}</div>
                            <tr class="thead1-proj">
                                <th>Produto do Projeto</th>
                            </tr>
                            <div>{prodProjetoCode}</div>
                        </table>
                    </div>
                </div>
                <div class="box">
                    <div class="box2">
                        <table class="table2">
                            <tr class="thead2">
                                <th>MVP<img src="https://cdn-icons-png.flaticon.com/128/9238/9238294.png" alt="Icone da tabela MVPs" class="table-icon"></th>
                            </tr>
                            <div>{mvpCode}</div>
                            <tr class="thead2-mvp">
                                <th>Produto do MVP</th>
                            </tr>
                            <div>{prodMvpCode}</div>
                        </table>
                    </div>
                </div>
                <div class="flex-column">
                    <div class="box">
                        <div class="box6">
                            <table class="table6">
                                <tr class="thead7">
                                    <th>Métricas<img src="https://cdn-icons-png.flaticon.com/128/7931/7931125.png" alt="Icone da tabela Métricas" class="table-icon"></th>
                                </tr>
                                <div>{metricaCode}</div>
                                <tr class="thead6">
                                    <th>Resultado esperado<img src="https://cdn-icons-png.flaticon.com/128/9797/9797853.png" alt="Icone da tabela Resultado esperado" class="table-icon"></th>
                                </tr>
                                <div>{resultadoCode}</div>
                            </table>
                        </div>
                    </div>
                </div>
            </div>"""
        
        return htmlRow


    def tableEqp(self):
        gestor = self.gestores
        especialista = self.especialistas
        squad = self.squads

        gestorCode = ""
        for i in range(len(gestor)):
            gestorCode += f"""<tr class="tdata4">
                    <td>{gestor[i]}</td>
                </tr>"""

        especialistaCode = ""
        for i in range(len(especialista)):
            especialistaCode += f"""<tr class="tdata4">
                    <td>{especialista[i]}</td>
                </tr>"""

        squadCode = ""
        for i in range(len(squad)):
            squadCode += f"""<tr class="tdata4">
                    <td>{squad[i]}</td>
                </tr>"""

        htmlEqp = f"""
            <div class="box">
                <div class="box4">
                    <table class="table4">
                        <tr class="thead4">
                            <th>Equipe<img src="https://cdn-icons-png.flaticon.com/128/5069/5069162.png" alt="Icone da tabela Equipe" class="table-icon"></th>
                        </tr>
                        <tr class="thead4-eqp">
                            <th><img src="https://cdn-icons-png.flaticon.com/128/3916/3916615.png" alt="Ícone do gestor para a tabela de Equipe" class="table-icon"> Gestor</th>
                        </tr>
                        <div>{gestorCode}</div>
                        <tr class="thead4-eqp">
                            <th><img src="https://cdn-icons-png.flaticon.com/128/9795/9795619.png" alt="Ícone do especialista para a tabela de Equipe" class="table-icon"> Especialista</th>
                        </tr>
                        <div>{especialistaCode}</div>
                        <tr class="thead4-eqp">
                            <th><img src="https://cdn-icons-png.flaticon.com/128/9856/9856655.png" alt="Ícone do squad para a tabela de Equipe" class="table-icon"> Squad</th>
                        </tr>
                        <div>{squadCode}</div>
                    </table>
                </div>
            </div>
        """
        return htmlEqp


    def tableUnic(self):
        entrega = self.entregas

        entregaCode = ""
        for i in range(len(entrega)):
            entregaCode += f"""<tr class="tdata5">
                    <td>{entrega[i]}</td>
                </tr>"""

        htmlUnic = f"""
            <div class="box">
                <div class="box5">
                    <table class="table5">
                        <tr class="thead5">
                            <th>Principais entregas<img src="https://cdn-icons-png.flaticon.com/128/10801/10801807.png" alt="Icone da tabela Principais entregas" class="table-icon"></th>
                        </tr>
                        <div>{entregaCode}</div>
                    </table>
                </div>
            </div>
        """
        return htmlUnic


    def tableCol(self):
        investimento = self.investimentos

        investimentoCode = ""
        for i in range(len(investimento)):
            investimentoCode += f"""<tr class="tdata3">
                    <td>R${investimento[i]}</td>
                </tr>"""

        htmlCol1 = f"""<div class="box">
                <div class="box3">
                    <table class="table3">
                        <tr class="thead3">
                            <th>Investimento<img src="https://cdn-icons-png.flaticon.com/128/7928/7928255.png" alt="Icone da tabela Investimentos" class="table-icon"></th>
                        </tr>
                        <div>{investimentoCode}</div>
                    </table>
                </div>
            </div>
            </div>"""
        return htmlCol1

    @staticmethod
    def tableGeral(htmlRow, htmlEqp, htmlUnic, htmlCol1):
        dadosRow = htmlRow #CreateHTML
        dadosEqp = htmlEqp #tableEqp()
        dadosUnic = htmlUnic #tableUnic()
        dadosCol = htmlCol1 #tableCol()

        htmlGeral = f"""
            <div class="flex-container">
                <div>{dadosRow}</div>
                <div class="flex-row">
                    <div>{dadosEqp}</div>
                    <div>{dadosUnic}</div>
                    <div>{dadosCol}</div>
                </div>
            </div>
        """
        return htmlGeral

    @staticmethod
    def cssStyle():
        canvaStyle = """
        body{
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                background-color: #fff;
            }
            
            .box{
                display: flex;
                align-items: flex-end;
                justify-content: center;
            }

            .box1,
            .box2,
            .box3,
            .box4,
            .box5,
            .box6,
            .box7{
                width: 100%;
                height: auto;
                max-width: 400px;
                //min-height: 200px;
                max-height: 180px;
                margin: 5px;
                overflow: auto;
                overflow-x: hidden;
                scrollbar-width: thin;
            }

            .box1:hover,
            .box2:hover,
            .box3:hover,
            .box4:hover,
            .box5:hover,
            .box6:hover,
            .box7:hover{
                transform: scale(0.98);
                border-radius: 20px;
            }

            .box1:hover{
                box-shadow: 0px 0px 25px rgba(74, 172, 252, 1);
            }

            .box2:hover{
                box-shadow: 0px 0px 25px rgba(255, 161, 189, 1);
            }

            .box3:hover{
                box-shadow: 0px 0px 25px rgba(255, 115, 84, 1);
            }

            .box4:hover{
                box-shadow: 0px 0px 25px rgba(73, 197, 57, 1);
            }

            .box5:hover{
                box-shadow: 0px 0px 25px rgba(141, 52, 135, 1);
            }

            .box6:hover{
                box-shadow: 0px 0px 25px rgba(255, 187, 78, 1);
            }

            .box7:hover{
                box-shadow: 0px 0px 25px rgba(255, 255, 68, 1);
            }

            .table1,
            .table2,
            .table3,
            .table4,
            .table5,
            .table6,
            .table7{
                width: 400px;
                border-collapse: collapse;
                border-radius: 10px;
                overflow: hidden; 
                min-height: 180px;
                max-height: 180px;
                border-collapse: collapse;
            }

            .thead1{
                background-color: #4aacfc;
            }

            .thead2{
                background-color: #ffa1bd;
            }

            .thead3{
                background-color: #ff7354;
            }

            .thead4{
                background-color: #49c539;
            }

            .thead5{
                background-color: #8d348793;
            }

            .thead6{
                background-color: #ffff76;
            }

            .thead7{
                background-color: #ffff44;
            }

            .thead4-eqp,
            .thead1-proj,
            .thead2-mvp{
                align-items: center;
                border-bottom: 1px solid #1eff00;
            }

            .thead4-eqp{
                background-color: #99e38f;
            }

            .thead1-proj{
                background-color: #aad6fa;
            }

            .thead2-mvp{
                background-color: #ffbafc;
            }

            .thead1,
            .thead2,
            .thead3,
            .thead4,
            .thead5,
            .thead6,
            .thead7{
                min-height: 50px;
                max-height: 50px;
            }

            .thead1 th,
            .thead2 th,
            .thead3 th,
            .thead4 th,
            .thead5 th,
            .thead6 th,
            .thead7 th{
                text-align: center;
                position: sticky;
                top: 0;
                min-height: 50px;
                max-height: 50px;
            }

            .thead4-eqp,
            .thead1-proj,
            .thead2-mvp{
                text-align: center;
            }

            .thead1 img,
            .thead2 img,
            .thead3 img,
            .thead4 img,
            .thead5 img,
            .thead6 img,
            .thead7 img,
            .thead4-eqp img{
                vertical-align: middle;
                margin-left: 10px;
                width: 20px;
                height: auto;
            }

            .tdata1 td{
                border-top: 1px solid #008cff;
                background-color: #c8e6ff;
            }

            .tdata2 td{
                border-top: 1px solid #ffb7c9;
                background-color: #ffd8fd;
            }

            .tdata3 td{
                border-top: 1px solid #ff2600;
                background-color: #ffe1d7;
            }

            .tdata4 td{
                background-color: #cdffc6;
            }

            .tdata5 td{
                border-top: 1px solid #96008c93;
                background-color: #e2cee193;
            }

            .tdata6 td{
                border-top: 1px solid #b3b301;
                background-color: #ffffc3;
            }

            .tdata7 td{
                border-top: 1px solid #b3b301;
                background-color: #ffffc3;
            }

            .flex-container {
                max-width: 1200px;
                margin: 0 auto;
                display: flex;
                flex-direction: column;
                align-items: center;
            }

            .flex-row {
                display: flex;
                justify-content: center;
                height: auto;
            }

            .flex-column {
                flex-direction: column;
                height: auto;
                max-height: 200px;
                min-width: 400px;
                top: 0;
            }
            
            .box1::-webkit-scrollbar,
            .box2::-webkit-scrollbar,
            .box3::-webkit-scrollbar,
            .box4::-webkit-scrollbar,
            .box5::-webkit-scrollbar,
            .box6::-webkit-scrollbar,
            .box7::-webkit-scrollbar{
                width: 6px;
                border-radius: 20px;
            }
            
            .box1::-webkit-scrollbar-track,
            .box2::-webkit-scrollbar-track,
            .box3::-webkit-scrollbar-track,
            .box4::-webkit-scrollbar-track,
            .box5::-webkit-scrollbar-track,
            .box6::-webkit-scrollbar-track,
            .box7::-webkit-scrollbar-track{
                //background: #a8a8ff;
                border-radius: 20px;
            }
            
            .box1::-webkit-scrollbar-thumb,
            .box2::-webkit-scrollbar-thumb,
            .box3::-webkit-scrollbar-thumb,
            .box4::-webkit-scrollbar-thumb,
            .box5::-webkit-scrollbar-thumb,
            .box6::-webkit-scrollbar-thumb,
            .box7::-webkit-scrollbar-thumb{
                //background-color: #00004d;
                border-radius: 20px;
                //border: 3px solid #a8a8ff;
                border: 1px solid;
            }"""
        
        return canvaStyle


import mysql.connector

conexao = mysql.connector.connect(
    passwd='nineboxeucatur',
    port=3306,
    user='ninebox',
    host='nineboxeucatur.c7rugjkck183.sa-east-1.rds.amazonaws.com',
    database='projeu'
)
mycursor = conexao.cursor()

cmd_Pbase = ''' 
SELECT 
	PTP.type_proj,
    PCP.nome_parm,
    valor_base
FROM projeu_premio_base
JOIN projeu_compl_param PCP on PCP.id_compl_param = complx_param_fgkey
JOIN projeu_type_proj PTP on PTP.id_type = typ_proj_fgkey;
'''
mycursor.execute(cmd_Pbase)
premioBaseBD = mycursor.fetchall()


cmd_Psprint = '''
SELECT 
	typ_proj_fgkey,
    typ_event,
    CAST(porc AS DECIMAL(2, 2)) AS porc,
    qntd_event,
    PCP.nome_parm,
    complx_param_fgkey
FROM projeu_param_premio
JOIN projeu_compl_param PCP ON id_compl_param = complx_param_fgkey
ORDER BY id_pp;'''
mycursor.execute(cmd_Psprint)
premioSprintBD = mycursor.fetchall()


cmd_Pfuncao = '''
SELECT 
	PCF.tip_fun,
    PCP.nome_parm,
    PCF.porcentual
FROM projeu_porc_func AS PCF
JOIN projeu_compl_param PCP ON PCP.id_compl_param = complx_fgkey 
ORDER BY PCF.tip_fun DESC;'''
mycursor.execute(cmd_Pfuncao)
premioFuncaoBD = mycursor.fetchall()
mycursor.close()



class CalculoPrêmio:
    def __init__(self, name_proj, complexidProj, typProj):
        self.premioSprint = None
        self.number_sprint = None
        self.name_proj = name_proj
        self.complexidProj = complexidProj
        self.typProj = typProj
        self.marcos = ['MARCO 1', 'MARCO 2', 'MARCO 3', 'MARCO 4', 'MARCO 5', 'MARCO 6', 'MARCO 7', 'MARCO 8']
        
        mycursor2 = conexao.cursor()
        mycursor2.execute(f"""
                SELECT 
                    PS.number_sprint,
                    PE.nome_Entrega, 
                    PU.Nome,
                    PU.Matricula,
                    PE.hra_necess,
                    PE.compl_entrega,
                    PE.stt_entrega,
                    (
                       SELECT id_proj FROM projeu_projetos WHERE id_proj = PS.id_proj_fgkey
                    ) AS ID_PROJ,
                    (
                       SELECT name_proj FROM projeu_projetos WHERE id_proj = PS.id_proj_fgkey
                    ) AS NAME_PROJ,
                    (
                       SELECT check_proj FROM projeu_projetos WHERE id_proj = PS.id_proj_fgkey
                    ) AS STATUS_PROJ,
                    PS.status_sprint AS EVENTO_SPRINT,
                    PE.id_sprint,
                    (
                        SELECT PRE.papel FROM projeu_registroequipe PRE WHERE PRE.id_colab = PU.id_user AND PRE.id_projeto = PS.id_proj_fgkey
                    ) AS PAPEL
                FROM 
                    projeu_entregas AS PE
                JOIN 
                    projeu_users PU ON PU.id_user = PE.executor
                JOIN 
                    projeu_sprints PS ON PS.id_sprint = PE.id_sprint
                WHERE 
                    PE.id_sprint IN (
                        SELECT 
                            PS_sub.id_sprint AS ID_SPRINT
                        FROM 
                            projeu_sprints AS PS_sub
                        JOIN 
                            projeu_projetos PP 
                            ON PP.id_proj = PS_sub.id_proj_fgkey
                        WHERE PP.name_proj LIKE '%{self.name_proj}%');""")

        self.entregas_do_projeto = mycursor2.fetchall()

        mycursor2.execute(f'''
                SELECT 
                    PPPD.id_pppd,
                    PP.id_proj, 
                    PP.name_proj,
                    PPPD.valor_base AS VALOR_BASE,
                    PPPD.porc_pre_mvp,
                    PPPD.porc_mvp,
                    PPPD.porc_pos_mvp,
                    PPPD.porc_entrega,
                    PPPD.porc_gestor,
                    PPPD.porc_espec,
                    PPPD.porc_squad,
                    PCX.complxdd,
                    PCX.nivel
                FROM 
                    projeu_premio_proj_diferent AS PPPD
                JOIN
                    projeu_projetos PP ON PP.id_proj = PPPD.id_proj_fgkey
                JOIN 
                    projeu_complexidade PCX ON PCX.id_compl = PPPD.complex_fgkey
                WHERE PP.name_proj LIKE '%{self.name_proj}%';
                ''')
        self.proj_especial = mycursor2.fetchall()
        
        mycursor2.execute(f'''
        SELECT 
            PES.id_sp,
            PU.id_user,
            PU.Matricula,
            PU.Nome,
            PS.id_sprint,
            PS.number_sprint,
            PES.status_sp
        FROM projeu_especialist_sprint PES
        JOIN
            projeu_users PU ON PU.id_user = PES.id_colab_fgkey
        JOIN
            projeu_sprints PS ON PS.id_sprint = PES.id_sprt_fgkey
        WHERE 
            PS.id_sprint IN ({str(list(set([x[11] for x in self.entregas_do_projeto]))).replace("[", "").replace("]", "")})
            AND
                PES.status_sp = "A";''')
          
        self.especialist_by_sprint = mycursor2.fetchall()
        
        mycursor2.execute(
            f'''SELECT 
                sum(PPE.valor) AS VALOR_TOTAL
            FROM 
                projeu_sprints AS PS
            JOIN
                projeu_premio_entr PPE ON id_sprint_fgkey = PS.id_sprint
            WHERE 
                PS.id_proj_fgkey IN (
                    SELECT id_proj FROM projeu_projetos
                        WHERE name_proj LIKE '%{str(self.name_proj).strip()}%'
        );''')
        self.valor_total = mycursor2.fetchall()

        mycursor2.close()


    def param_especial_event(self, evento):
        dic_aux = {'PRÉ MVP': self.proj_especial[0][4], 
                'PÓS MVP': self.proj_especial[0][6], 
                'ENTREGA FINAL': self.proj_especial[0][7], 
                'MVP': self.proj_especial[0][5]}
        
        if evento in [str(x).strip() for x in list(dic_aux.keys())]:
            retorno = dic_aux[evento]
        else:
            retorno = 'EVENTO ESPECIAL COM NOMENCLATURA INCORRETA.'
        
        return retorno


    @staticmethod
    def dificEntreg(dif):
        dic_aux = {'Difícil': 3,
                   'Médio': 2,
                   'Fácil': 1}

        return dic_aux[dif]
    
    
    #PEGANDO O VALOR TOTAL DOS PROJETOS DE IMPLANTAÇÃO
    def impl_valorEvento(self):#RADICAL II
        valor_base = [float(x[2]) for x in premioBaseBD if str(x[1]).strip().upper() == str(self.complexidProj).strip().upper()][0]     
        
        valor_total = {'VALOR_MARCOS': sum([int(x[3]) for x in premioSprintBD if str(x[4]).strip().upper() == str(self.complexidProj).strip().upper() and str(x[1]).strip().upper() in self.marcos]) * valor_base, 
                   'ENTREGA FINAL': sum([int(x[3]) for x in premioSprintBD if str(x[4]).strip().upper() == str(self.complexidProj).strip().upper() and str(x[1]).strip().upper() == 'ENTREGA FINAL']) * valor_base}
        
        return valor_total
    
    
    #PARÂMETROS DO CALCULO DE EVENTOS
    def param_eventos(self, evento):
        if evento in list(set([typEvent[1] for typEvent in premioSprintBD])):
            if len(self.proj_especial) > 0:
                premioSprint = {f'{nameEvent}':
                                    {'Complexidade': [x[4] for x in premioSprintBD if x[1] == nameEvent],
                                    'Porcentagem': [self.param_especial_event(evento) for x in range(len(premioSprintBD)) if premioSprintBD[x][1] == nameEvent],
                                    'QuantidadeEventos': [x[3] for x in premioSprintBD if x[1] == nameEvent]}
                    for nameEvent in list(set([typEvent[1] for typEvent in premioSprintBD]))}
            else:
                premioSprint = {f'{nameEvent}':
                                    {'Complexidade': [x[4] for x in premioSprintBD if x[1] == nameEvent],
                                    'Porcentagem': [x[2] for x in premioSprintBD if x[1] == nameEvent],
                                    'QuantidadeEventos': [x[3] for x in premioSprintBD if x[1] == nameEvent]}
                    for nameEvent in list(set([typEvent[1] for typEvent in premioSprintBD]))}
                                
            retorno = premioSprint[evento]
        else:
            retorno = f'EVENTO INFORMADO NÃO EXISTENTE. EVENTOS DISPONÍVEIS {list(set([typEvent[1] for typEvent in premioSprintBD]))}'

        return retorno
    
    
    #PEGA O VALOR TOTAL DO PROJETO E DIVIDE ENTRE OS EVENTOS
    def valorEvento(self):
        if len(self.proj_especial) < 1:
            valor_base = [x[2] for x in premioBaseBD if str(x[0]).strip().upper() == str(self.typProj).strip().upper()  # VALOR BASE DAQUELA COMPLEXIDADE
                        and str(x[1]).strip().upper() == str(self.complexidProj).strip().upper()]
        else:
            valor_base = [round(float(self.proj_especial[0][3]), 2)] #VALOR BASE DAQUELE PROJETO EM ESPECIAL  # VALOR BASE DAQUELA COMPLEXIDADE
        
        if str(self.typProj).strip().upper() == 'IMPLANTAÇÃO':
            impl_valor_base = self.impl_valorEvento()['VALOR_MARCOS'] / sum([int(x[3]) for x in premioSprintBD if str(x[4]).strip().upper() == str(self.complexidProj).strip().upper() and str(x[1]).strip() not in list(self.marcos)+['ENTREGA FINAL']])
        
        eventos = list(set([typEvent[1] for typEvent in premioSprintBD if str(typEvent[4]).strip().upper() == str(self.complexidProj).strip().upper()]))  # SPRINT PRÉ-MVP, MVP, PÓS-MVP, ENTREGA FINAL
        
        AuxDDComplx = {}
        for event in eventos:
            
            auxParam = self.param_eventos(event)
            
            idx_complx = list(auxParam['Complexidade']).index(self.complexidProj)

            porct = list(auxParam['Porcentagem'])[idx_complx]  # PORCENTAGEM DO VALOR TOTAL DESTINADO PARA AQUELE EVENTO
            qntdSprint = list(auxParam['QuantidadeEventos'])[
                idx_complx]  # QUANTIDADE DE SPRINTS QUE AQUELE EVENTO VAI TER

            valorEvent = round(((float(valor_base[0]) / 100) * (float(porct) * 100)), 2)  # VALOR TOTAL QUE O EVENTO VAI TER
            valorPorSprint = valorEvent / qntdSprint  # VALOR PAGO POR SPRINT

            AuxDDComplx[event] = {'ValorEvento': valorEvent,
                                  'ValorPorSprint': valorPorSprint,
                                  'Porcentagem': float(porct),
                                  'QuantidadeSprints': qntdSprint}
        return AuxDDComplx

    #FUNÇÃO PARA CALCULAR O VALOR QUE FALTA CASO O PROJETO SEJA FINALIZADO ANTES DO PERÍODO PRÉVIO 
    def valor_restante(self):
        status = list(set([x[9] for x in self.entregas_do_projeto]))[0]
        if 'ENTREGA FINAL' in list(set([str(x[10]).strip() for x in self.entregas_do_projeto])) and status == 1:
            sprints_aux = list(set([(x[0],x[7]) for x in self.entregas_do_projeto]))

            eventos = list(set([typEvent[1] for typEvent in premioSprintBD if typEvent[0] != 4]))

            aux_sum = []

            valores_base_por_event = self.valorEvento()

            for event in eventos:
                aux_sum.append(valores_base_por_event[str(event).strip().upper()]['ValorEvento'])#VOU PEGAR O OBJETO VALOR EVENTO QUE NOS FORNECE A VALOR TOTAL DIVIDIDO POR SPRINT

            dif_valor = sum(aux_sum) - float(self.valor_total[0][0]) #PEGANDO O VALOR TOTAL QUE JÁ FOI PAGO NAS ENTREGAS

            retorno = dif_valor
        else:
            retorno = 0

        return retorno

    
    def entreg_projeto(self):
        return self.entregas_do_projeto

    #FUNÇÃO PENSADA PARA CALCULAR A BONIFICAÇÃO DA SQUAD
    # ---> RECEBE O VALOR QUE FOI SEPARADO PARA AQUELA SPRINT E DIVIDE ENTRE O SQUAD
    def CalculaSquad(self, entregas, valor_sprint):
        #EXEMPLO DE USO
        # sprint = 1                     ---> [[LISTA DE ENTREGAS], VALOR DISTRIBUIDO PARA A SPRINT]
        # exemplo_de_como_chamar = CalculaSquad([list(x) for x in entregasBD if x[0] == sprint], 1200)
        
        if len(list(set([x[0] for x in entregas if int(x[0]) in [int(x) for x in self.number_sprint]]))) > 0:
            entregas_sprint = []
            for entr in entregas:
                if str(entr[12]).strip() == 'Gestor':
                    entr[4] = 0
                
                entregas_sprint.append(entr)

            # MATRICULA, NOME COLABORADOR
            colbs = list(set([(x[3], x[2]) for x in entregas_sprint]))
            
            hrs_normaliz = {colb[1]: sum([float(x[4] * self.dificEntreg(x[5])) for x in entregas_sprint if x[3] == colb[0]])
                            for colb in colbs}
                        
            hrs_total = sum([hrs_normaliz[x] for x in hrs_normaliz.keys()])

            valor_colab = {name_colab: {'BonificacaoSprint': valor_sprint * (hrs_normaliz[name_colab] / hrs_total),
                                        'HorasNormalTotal': hrs_normaliz[name_colab],
                                        'Entregas': {x[1]: {'Horas': x[4],
                                                            'HorasNormalizadas': x[4] * self.dificEntreg(x[5]),
                                                            'Bonificação': valor_sprint * (
                                                                        (x[4] * self.dificEntreg(x[5])) / hrs_total),
                                                            'Dificuldade': self.dificEntreg(x[5]),
                                                            'Status': x[6]} for x in entregas_sprint if
                                                     str(x[2]).strip().lower() == str(name_colab).strip().lower()}}
                           for name_colab in hrs_normaliz.keys()}

        else:
            valor_colab = {'error': 'Sprint informada não possui dados'}
        
        return valor_colab

    def CalculaSprint(self, valorSprint, sprint):
        dd_especialist = [x for x in self.especialist_by_sprint if x[5] in list(sprint)]#DADOS SOBRE ESPECIALISTAS DAQUELAS SPRINTS
        
        qntd_contrib_espc = {id_espc: len([d for d in dd_especialist if d[1] == id_espc]) for id_espc in list(set([x[1] for x in dd_especialist]))}
        
        porc_contrib = {id_user: qntd_contr/sum(qntd_contrib_espc.values()) for id_user, qntd_contr in qntd_contrib_espc.items()}
        
        qntdEspecial = len(porc_contrib)
        status = list(set([x[9] for x in self.entregas_do_projeto]))[0]
        if self.entregas_do_projeto != None:
            self.number_sprint = sprint
            
            #IDÊNTIFICANDO O VALOR RESTANTE PARA CASO O PROJETO JÁ TENHA SIDO FINALIZADO ANTES DO PRAZO
            if str(status).strip() == str(1) and 'ENTREGA FINAL' in list(set([str(x[10]).strip() for x in self.entregas_do_projeto])) and str(self.typProj).strip() not in ('Rápido'):
                valor_restante = self.valor_restante()
                valorSprint = valor_restante
            
            if len(self.proj_especial) > 0:
                porcEquipe = [['GESTOR', f'{str(self.proj_especial[0][11]).strip()} {str(self.proj_especial[0][12]).strip()}', self.proj_especial[0][8]],
                            ['ESPECIALISTA', f'{str(self.proj_especial[0][11]).strip()} {str(self.proj_especial[0][12]).strip()}', self.proj_especial[0][9]],
                            ['SQUAD', f'{str(self.proj_especial[0][11]).strip()} {str(self.proj_especial[0][12]).strip()}', self.proj_especial[0][10]]]
            else:
                porcEquipe = [list(x) for x in premioFuncaoBD if x[1] == self.complexidProj]
            
            
            if len(dd_especialist) == 0:
                idx_time_fun = lambda equipe: list([str(x[0]).strip().upper() for x in porcEquipe]).index(
                    f'{str(equipe).upper()}')

                porcEquipe[idx_time_fun('SQUAD')][2] = porcEquipe[idx_time_fun('ESPECIALISTA')][2] + \
                                                       porcEquipe[idx_time_fun('SQUAD')][2]
                porcEquipe[idx_time_fun('ESPECIALISTA')][2] = 0.0

            valoresEquipe = {}
            valoresEquipe['GESTOR'] = valorSprint * float(
                [x[2] for x in porcEquipe if str(x[0]).upper() == 'GESTOR'][0])

            TotalEspecialist = valorSprint * float([x[2] for x in porcEquipe if str(x[0]).upper() == 'ESPECIALISTA'][0] if len([x[2] for x in porcEquipe if str(x[0]).upper() == 'ESPECIALISTA']) > 0 else 0)
            
            valoresEquipe['ESPECIALISTA'] = {'ValorTotal': TotalEspecialist,
                                             'ValorPorEspecialist': (TotalEspecialist/qntdEspecial) if qntdEspecial > 0 else 0,
                                             'QuantidadeEspecialista': qntdEspecial,
                                             'ValorParaMVP': {[str(x[2]).strip() for x in dd_especialist if x[1] == id_user][0]:{
                                                                  [str(x[3]).strip() for x in dd_especialist if x[1] == id_user][0]: TotalEspecialist * porct_epc}
                                                              for id_user, porct_epc in porc_contrib.items()}    
                                            }
            
            valoresEquipe['SQUAD'] = self.CalculaSquad([list(x) for x in self.entregas_do_projeto if x[0] in self.number_sprint],
                                                  valorSprint * float(
                                                      [x[2] for x in porcEquipe if str(x[0]).upper() == 'SQUAD'][0]))

            retorno = valoresEquipe
        else:
            retorno = 'PRIMAIRAMENTE, É NECESSÁRIO CONSUMIR O BANCO DADOS PARA PEGAR AS ENTREGAS DO PROJETO'
        return retorno



######################## FUNÇÕES PARA PLOTAR CAIXINHA DO 9BOX ########################
def ninebox(quadrante, nineboxDatasUnidadesAux, dadosNineboxUni, nome_quadrante):
        #INTEIRO // DADOS TRATADOS COM HTML // LISTA DE UNIDADES NO LISTCELLNINETODOS
    
    style = ["yellow", "green", "blue"]
    
    dados_html = nineboxDatasUnidadesAux #DADOS TRATADOS DENTRO DO HTML
    qtdUnidades = dadosNineboxUni[1] #LISTCELLNINETODOS --> INFORMAÇÕES DAS UNIDADES EM UMA LISTA
    
    totalUnidades = sum([len(x) for x in qtdUnidades])

    quadrante = quadrante - 1
    boxTable = f"""<div class="box">
                        <div class="box-{style[quadrante]}">
                            <div class="header-{style[quadrante]}">
                                <div class="title-{style[quadrante]}">{nome_quadrante}</div>
                                <div class="data-{style[quadrante]}">{len(qtdUnidades[quadrante])}</div>
                                <div class="datap-{style[quadrante]}">{round((len(qtdUnidades[quadrante]*100)/totalUnidades), 2)}%</div>
                            </div>
                            <div class="data-box">
                                <div>{dados_html[quadrante]}</div>
                            </div>
                        </div>
                    </div>"""
    
    return boxTable

def nineboxDatasUnidades(dadosNineboxUni):
                        #LISTA DE UNIDADES NO LISTCELLNINETODOS
    qtdUnidades = dadosNineboxUni[1] 
    style = ["yellow", "green", "blue"]
    txtHtml = []
    for i in range(len(qtdUnidades)):
        txtAux = ""

        if len(qtdUnidades[i]) > 0:
            for j in range(len(qtdUnidades[i])):
                dados_ninebox = f"""<table class="tb">
                        <tr class="tb-person-{style[i]}">
                            <td>{qtdUnidades[i][j]}</td>
                        </tr>
                    </table>"""
                
                txtAux += dados_ninebox
        txtHtml.append(txtAux)

    return txtHtml

def css_9box():
    ninebox_style = """
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@200;300;400;500;600&display=swap');
    *{
        margin: 0;
        padding: 0;
    }

    main{
        width: 100%;
        display: flex;
        justify-content: center;
        align-items: center;
    }

    .box{
        display: flex;
        align-items: flex-end;
        justify-content: center;
        font-family: 'Poppins', sans-serif;
    }

    .box-blue,
    .box-yellow,
    .box-green{
        margin: 10px 0px;
        border-radius: 8px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        width: 100%;
        max-height: 200px;
        min-height: 200px;
        overflow: auto;
        overflow-x: hidden;
        scrollbar-width: thin;
        padding-right: 10px;
        z-index: 2;

    }

    .box-yellow:hover,
    .box-green:hover,
    .box-blue:hover{
        transform: scale(1.05);
    }


    .box-blue {
        background-color: #FFEBEE;
    }

    .box-yellow {
        background-color: #E0F7FA;
    }

    .box-green {
        background-color: #E0F2F1;
    }

    .header-blue,
    .header-yellow,
    .header-green{
        display: flex;
        justify-content: space-between;
        align-items: center;
        position: sticky;
        top: 0;
        z-index: 1;
        width: 100%;
        height: 60px;
    }

    .header-blue {
        background-color: #FFEBEE;
    }

    .header-yellow {
        background-color: #E0F7FA;
    }

    .header-green{
        background-color: #E0F2F1;
    }


    @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Bungee+Inline&family=Koulen&family=Major+Mono+Display&family=Passion+One&family=Sansita+Swashed:wght@500&display=swap');
    .title-blue,
    .title-yellow,
    .title-green{
        font-size: 18px;
        text-align: left;
        margin: 0 5px;
        width: auto;
        height: 15px;
        padding-left: 5px;
        flex: 1;
        color: #374151;
       }

    .data-blue,
    .data-yellow,
    .data-green{
        font-size: 14px;
        font-weight: bold;
        color: #000;
        text-align:center;
        margin: 5px 0px;
        border-radius: 20%;
        width: 30px;
        height: auto;
        padding: 5px;
    }

    .data-blue {
        background-color: #F8BBD0; 
        color: #00004d;
    }

    .data-yellow {
        background-color: #BBDEFB; 
        color: #384200;
    }

    .data-green{
        background-color: #C8E6C9; 
        color: #002100;
    }

    .datap-blue,
    .datap-yellow,
    .datap-green{
        font-size: 14px;
        font-weight: bold;
        color: #000;
        text-align:center;
        margin: 5px 10px;
        border-radius: 20%;
        width: auto;
        height: auto;
        padding: 5px;
    }

    .datap-blue {
        background-color: #F8BBD0; 
        color: #00004d;
    }

    .datap-yellow {
        background-color: #BBDEFB; 
        color: #384200;
    }

    .datap-green{
        background-color: #C8E6C9; 
        color: #002100;
    }



    .tb {
        width: 100%;
        border-collapse: collapse;
        margin-top: 10px;
        margin: 5px;
    }

    .tb-person-blue td,
    .tb-person-yellow td,
    .tb-person-green td{
        padding: 5px 5px;
        border-radius: 5px;
        color: #000;
        font-size: 13px;
    }

    .st-emotion-cache-uvn0xz tr {
        border-top: 0px
    }
    .tb-person-blue td {
        background-color: #FFCDD2;
    }

    .tb-person-yellow td {
        background-color: #BBDEFB;
    }

    .tb-person-green{
        background-color: #C8E6C9;
    }

    .tb-person-blue:last-child td,
    .tb-person-yellow:last-child td,
    .tb-person-green:last-child td{
        border: none;
    }

    .box-blue::-webkit-scrollbar {
        width: 12px;
        border-radius: 20px;
    }

    .box-blue::-webkit-scrollbar-track {
        background: #FFCDD2;
        border-radius: 20px;
    }

    .box-blue::-webkit-scrollbar-thumb {
        background-color: #00004d;
        border-radius: 20px;
        border: 3px solid #FFCDD2;
    }

    .box-yellow::-webkit-scrollbar {
        width: 12px;
        border-radius: 20px;
    }

    .box-yellow::-webkit-scrollbar-track {
        background: #BBDEFB;
        border-radius: 20px;
    }

    .box-yellow::-webkit-scrollbar-thumb {
        background-color: #384200;
        border-radius: 20px;
        border: 3px solid #BBDEFB;
    }

    .box-green::-webkit-scrollbar {
        width: 12px;
        border-radius: 20px;
    }

    .box-green::-webkit-scrollbar-track {
        background: #C8E6C9;
        border-radius: 20px;
    }


    .box-green::-webkit-scrollbar-thumb {
        background-color: #002100;
        border-radius: 20px;
        border: 3px solid #C8E6C9;
    }

    .box-orange::-webkit-scrollbar {
        width: 12px;
        border-radius: 20px;
    }

    .box-orange::-webkit-scrollbar-track {
        background: #f8cda9;
        border-radius: 20px;
    }

    .box-orange::-webkit-scrollbar-thumb {
        background-color: #492100;
        border-radius: 20px;
        border: 3px solid #f8cda9;
    }

    .box-red::-webkit-scrollbar {
        width: 12px;
        border-radius: 20px;
    }

    .box-red::-webkit-scrollbar-track {
        background: #fcbcbc;
        border-radius: 20px;
    }

    .box-red::-webkit-scrollbar-thumb {
        background-color: #410000;
        border-radius: 20px;
        border: 3px solid #fcbcbc;
    }

    .tb-person-blue:hover td{
        background-color: #92c2d3;
        font-size: 13px;
    }

    .tb-person-green:hover td{
        background-color: #c0ffa9;
    }

    .tb-person-yellow:hover td{
        background-color: #BBDEFB;
    }


    @media(max-width: 1400px){
        .header-blue,
        .header-yellow,
        .header-green{
            display: flex;
            justify-content: space-between;
            align-items: center;
            position: sticky;
            top: 0;
            z-index: 1;
            width: 100%;
            height: auto;
        }   
    }
    }

    @media(max-width: 1000px){
        .main{
            flex-direction: column;
            align-items: stretch;
        }

        .line1,
        .line2,
        .line3{
            width: 100%;
            display: flex;
            flex-direction: column;
            align-items: center;
        }

        .box-blue,
        .box-yellow,
        .box-green{
            width: 90%;
            min-height: auto;
            margin: 10px 5px;
        }

        .header-blue,
        .header-yellow,
        .header-green{
            display: flex;
            justify-content: space-between;
            align-items: center;
            position: sticky;
            top: 0;
            z-index: 1;
            width: 100%;
            height: auto;
        }
    }"""

    return ninebox_style


def divisaoSecao2(title, id, cor='#06405c', tam_font=14, negrito=400, padding=6, font_color='White'):
    style23 = f"""
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@200;300;400;500;600&display=swap');
    .card{id} {{
        width: 100%;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        border-radius: 10px;
        overflow: hidden;
        border: none; /* Adiciona esta propriedade para remover a borda */
        font-family: 'Poppins', sans-serif;
    }}
    .header{id} {{
        background-color:{cor};
        color: {font_color};
        padding: {padding}px;
        text-align: center;
        font-size: {tam_font}px;
        font-weight: {negrito};
    }}
    """
    html23 = f"""<div class="card{id}"><div class="header{id}">{title}</div>"""
    st.write(f'<style>{style23}</style>', unsafe_allow_html=True)
    st.write(f'<div>{html23}</div>', unsafe_allow_html=True)
    st.write("")
