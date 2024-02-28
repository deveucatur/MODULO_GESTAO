import streamlit as st
import json
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib
from PIL import Image
import numpy as np
import random
from openpyxl import load_workbook
import ast
import datetime
from datetime import datetime
import mysql.connector


conexao = mysql.connector.connect(
    passwd='npmyY8%UZ041',
    port=3306,
    user='ninebox',
    host='192.168.10.71',
    database='Colaboradores'
)
mycursor = conexao.cursor()


st.set_option('deprecation.showPyplotGlobalUse', False)


def limpar_datas(datas):
    datas_ = []
    data1 = datas[:10]
    data2 = datas[13:]
    
    datas_.append(data1)
    datas_.append(data2)
    
    return datas_


def string_to_datetime(string):
    date = datetime.strptime(str(string), "%Y-%m-%d").date()
    return date


def displayInd(title, valor, min_val, max_val):
    max_val = float(max_val)
    # Estilos CSS para a janela
    styleJanela = '''
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@200;300;400;500;600&display=swap');
    .card2 {
        padding: 0.6rem;
        background-color: #fff;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        max-width: 100%;
        border-radius: 20px;
        text-align: center;
    }

    .title2 {
        align-items: center;
    }

    .title2-text {
    color: #374151;
    font-size: 18px;
    font-family: 'Poppins', sans-serif;
    }

    .data2 {
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
    }

    .data2 p {
        color: #1F2937;
        font-size: 2.25rem;
        line-height: 2.5rem;
        font-weight: 700;
        font-family: 'Poppins', sans-serif;
    }

    .data2 .range2 {
        position: relative;
        background-color: #E5E7EB;
        width: 100%;
        height: 0.5rem;
        border-radius: 0.25rem;
    }

    .data2 .range2 .fill2 {
        position: absolute;
        background-color: #D4AF37;
        height: 100%;
        border-radius: 0.25rem;
    }
    '''

    # Cálculo da porcentagem da barra de progresso
    valor = float(valor.replace(',', '.'))
    percent = min((valor - min_val) / (max_val - min_val) * 100, 100)

    # HTML da janela
    htmlJanela = f'''<div class="card2">
                  <div class="title2">
                      <p class="title2-text">{title}</p>
                  </div>
                  <div class="data2">
                      <p>{int(valor)}</p>
                      <div class="range2"><div class="fill2" style="width: {percent}%"></div></div>
                  </div>
              </div>'''

    st.write(f'<style>{styleJanela}</style>', unsafe_allow_html=True)
    st.write(f'<div>{htmlJanela}</div>', unsafe_allow_html=True)


def displayInd3(title, valor, min_val, max_val):
    max_val = float(max_val)
    # Estilos CSS para a janela
    styleJanela = '''
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@200;300;400;500;600&display=swap');
    .card4 {
        padding: 0.6rem;
        background-color: #fff;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        max-width: 100%;
        border-radius: 20px;
        text-align: center;
    }

    .title4 {
        align-items: center;
    }

    .title4-text {
        color: #374151;
        font-size: 18px;
        font-family: 'Poppins', sans-serif;
    }

    .data4 {
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        font-family: 'Poppins', sans-serif;
    }

    .data4 p {
        color: #1F2937;
        font-size: 2.25rem;
        line-height: 2.5rem;
        font-weight: 700;
    }

    .data4 .range4 {
        position: relative;
        background-color: #fff;
        width: 100%;
        height: 0.5rem;
        border-radius: 0.25rem;
    }

    .data4 .range4 .fill4 {
        position: absolute;
        background-color: #fff;
        height: 100%;
        border-radius: 0.25rem;
    }
    '''

    # Cálculo da porcentagem da barra de progresso
    valor = float(valor.replace(',', '.'))
    percent = min((valor - min_val) / (max_val - min_val) * 100, 100)

    # HTML da janela
    htmlJanela = f'''<div class="card4">
                  <div class="title4">
                      <p class="title4-text">{title}</p>
                  </div>
                  <div class="data4">
                      <p>{int(valor)}%</p>
                      <div class="range4"><div class="fill4" style="width: {percent}%"></div></div>
                  </div>
              </div>'''

    st.write(f'<style>{styleJanela}</style>', unsafe_allow_html=True)
    st.write(f'<div>{htmlJanela}</div>', unsafe_allow_html=True)


def displayInd2(title, valor, min_val, max_val):
    max_val = float(max_val)
    # Estilos CSS para a janela
    styleJanela = '''
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@200;300;400;500;600&display=swap');
    .card3 {
        padding: 0.6rem;
        background-color: #0077B6;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        max-width: 100%;
        border-radius: 20px;
        text-align: center;
    }

    .title3 {
        align-items: center;
    }

    .title3-text {
        color: #fff;
        font-size: 18px;
        font-weight: bold;
        font-family: 'Poppins', sans-serif;
    }

    .data3 {
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        font-family: 'Poppins', sans-serif;
    }

    .data3 p {
        color: #fff;
        font-size: 2.25rem;
        line-height: 2.5rem;
        font-weight: 700;
    }

    .data3 .range3 {
        position: relative;
        background-color: #0077B6;
        width: 100%;
        height: 0.5rem;
        border-radius: 0.25rem;
    }

    .data3 .range3 .fill3 {
        position: absolute;
        background-color: #0077B6;
        height: 100%;
        border-radius: 0.25rem;
    }
    '''

    # Cálculo da porcentagem da barra de progresso
    valor = float(valor.replace(',', '.'))
    percent = min((valor - min_val) / (max_val - min_val) * 100, 100)

    # HTML da janela
    htmlJanela = f'''<div class="card3">
                  <div class="title3">
                      <p class="title3-text">{title}</p>
                  </div>
                  <div class="data3">
                      <p>{int(valor)}%</p>
                      <div class="range3"><div class="fill3" style="width: {percent}%"></div></div>
                  </div>
              </div>'''

    st.write(f'<style>{styleJanela}</style>', unsafe_allow_html=True)
    st.write(f'<div>{htmlJanela}</div>', unsafe_allow_html=True)


def displayInd4(title, valor, min_val, max_val):
    max_val = float(max_val)
    # Estilos CSS para a janela
    styleJanela = '''
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@200;300;400;500;600&display=swap');
    .card5 {
        padding: 0.6rem;
        background-color: #0077B6;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        max-width: 100%;
        border-radius: 20px;
        text-align: center;
    }

    .title5 {
        align-items: center;
    }

    .title5-text {
        color: #fff;
        font-size: 18px;
        font-weight: bold;
        font-family: 'Poppins', sans-serif;
    }

    .data5 {
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        font-family: 'Poppins', sans-serif;
    }

    .data5 p {
        color: #fff;
        font-size: 2.25rem;
        line-height: 2.5rem;
        font-weight: 700;
    }

    .data5 .range5 {
        position: relative;
        background-color: #0077B6;
        width: 100%;
        height: 0.5rem;
        border-radius: 0.25rem;
    }

    .data5 .range5 .fill5 {
        position: absolute;
        background-color: #0077B6;
        height: 100%;
        border-radius: 0.25rem;
    }
    '''

    # Cálculo da porcentagem da barra de progresso
    valor = float(valor.replace(',', '.'))
    percent = min((valor - min_val) / (max_val - min_val) * 100, 100)

    # HTML da janela
    htmlJanela = f'''<div class="card5">
                  <div class="title5">
                      <p class="title5-text">{title}</p>
                  </div>
                  <div class="data5">
                      <p>{int(valor)}</p>
                      <div class="range5"><div class="fill5" style="width: {percent}%"></div></div>
                  </div>
              </div>'''

    st.write(f'<style>{styleJanela}</style>', unsafe_allow_html=True)
    st.write(f'<div>{htmlJanela}</div>', unsafe_allow_html=True)


def soma_basica(lista):
  soma = 0
  for a in lista:
     soma += a

  return soma


def converte_data(data_americana):
    data_objeto = datetime.strptime(data_americana, '%Y-%m-%d')
    data_brasileira = data_objeto.strftime('%d/%m/%Y')
    return data_brasileira


def ListaCellNineTodos(dadosNinebox):
    # Cria uma interface gráfica com uma grade de nine box e botões para adicionar, editar e excluir funcionários
    top_left_aux = sorted([(x[1] * x[2], x[0]) for x in dadosNinebox if classify_employee(x[1], x[2]) == 'top_left'],
                          reverse=False)
    top_left = [x[1] for x in top_left_aux]

    top_middle_aux = sorted(
        [(x[1] * x[2], x[0]) for x in dadosNinebox if classify_employee(x[1], x[2]) == 'top_middle'], reverse=False)
    top_middle = [x[1] for x in top_middle_aux]

    middle_left_aux = sorted(
        [(x[1] * x[2], x[0]) for x in dadosNinebox if classify_employee(x[1], x[2]) == 'middle_left'], reverse=False)
    middle_left = [x[1] for x in middle_left_aux]

    middle_middle_aux = sorted(
        [(x[1] * x[2], x[0]) for x in dadosNinebox if classify_employee(x[1], x[2]) == 'middle_middle'], reverse=False)
    middle_middle = [x[1] for x in middle_middle_aux]

    top_right_aux = sorted([(x[1] * x[2], x[0]) for x in dadosNinebox if classify_employee(x[1], x[2]) == 'top_right'],
                           reverse=False)
    top_right = [x[1] for x in top_right_aux]

    middle_right_aux = sorted(
        [(x[1] * x[2], x[0]) for x in dadosNinebox if classify_employee(x[1], x[2]) == 'middle_right'], reverse=False)
    middle_right = [x[1] for x in middle_right_aux]

    bottom_left_aux = sorted(
        [(x[1] * x[2], x[0]) for x in dadosNinebox if classify_employee(x[1], x[2]) == 'bottom_left'], reverse=False)
    bottom_left = [x[1] for x in bottom_left_aux]

    bottom_middle_aux = sorted(
        [(x[1] * x[2], x[0]) for x in dadosNinebox if classify_employee(x[1], x[2]) == 'bottom_middle'], reverse=False)
    bottom_middle = [x[1] for x in bottom_middle_aux]

    bottom_right_aux = sorted(
        [(x[1] * x[2], x[0]) for x in dadosNinebox if classify_employee(x[1], x[2]) == 'bottom_right'], reverse=False)
    bottom_right = [x[1] for x in bottom_right_aux]

    # Cria uma lista com os nomes das células da grade de nine box
    cell_names = ["Enigma", "Forte Potencial", "Alto Potencial", "Questionável", "Mantenedor", "Forte Desempenho",
                  "Insuficiente", "Eficaz", "Comprometido"]
    # Cria uma lista com os dados dos funcionários em cada célula da grade de nine box
    cell_data = [top_left, top_middle, top_right, middle_left, middle_middle, middle_right, bottom_left, bottom_middle,
                 bottom_right]

    #cell_porc = [round((len(x) / sum([len(y) for y in cell_data])) * 100, 1) if len(x) > 0 else x for x in cell_data]    
    
    cell_names = [f'{cell_names[x]} - {len(cell_data[x])}' if len(cell_data[x]) > 0 else cell_names[x] for x in range(len(cell_names))]
    
    return cell_names, cell_data


def ListaCellNineTodos2(dadosNinebox):
    # Cria uma interface gráfica com uma grade de nine box e botões para adicionar, editar e excluir funcionários
    top_left_aux = sorted([(x[1] * x[2], x[0]) for x in dadosNinebox if classify_employee(x[1], x[2]) == 'top_left'],
                          reverse=False)
    top_left = [x[1] for x in top_left_aux]

    top_middle_aux = sorted(
        [(x[1] * x[2], x[0]) for x in dadosNinebox if classify_employee(x[1], x[2]) == 'top_middle'], reverse=False)
    top_middle = [x[1] for x in top_middle_aux]

    middle_left_aux = sorted(
        [(x[1] * x[2], x[0]) for x in dadosNinebox if classify_employee(x[1], x[2]) == 'middle_left'], reverse=False)
    middle_left = [x[1] for x in middle_left_aux]

    middle_middle_aux = sorted(
        [(x[1] * x[2], x[0]) for x in dadosNinebox if classify_employee(x[1], x[2]) == 'middle_middle'], reverse=False)
    middle_middle = [x[1] for x in middle_middle_aux]

    top_right_aux = sorted([(x[1] * x[2], x[0]) for x in dadosNinebox if classify_employee(x[1], x[2]) == 'top_right'],
                           reverse=False)
    top_right = [x[1] for x in top_right_aux]

    middle_right_aux = sorted(
        [(x[1] * x[2], x[0]) for x in dadosNinebox if classify_employee(x[1], x[2]) == 'middle_right'], reverse=False)
    middle_right = [x[1] for x in middle_right_aux]

    bottom_left_aux = sorted(
        [(x[1] * x[2], x[0]) for x in dadosNinebox if classify_employee(x[1], x[2]) == 'bottom_left'], reverse=False)
    bottom_left = [x[1] for x in bottom_left_aux]

    bottom_middle_aux = sorted(
        [(x[1] * x[2], x[0]) for x in dadosNinebox if classify_employee(x[1], x[2]) == 'bottom_middle'], reverse=False)
    bottom_middle = [x[1] for x in bottom_middle_aux]

    bottom_right_aux = sorted(
        [(x[1] * x[2], x[0]) for x in dadosNinebox if classify_employee(x[1], x[2]) == 'bottom_right'], reverse=False)
    bottom_right = [x[1] for x in bottom_right_aux]

    # Cria uma lista com os nomes das células da grade de nine box
    cell_names = ["Enigma", "Forte Potencial", "Alto Potencial", "Questionável", "Mantenedor", "Forte Desempenho",
                  "Insuficiente", "Eficaz", "Comprometido"]
    # Cria uma lista com os dados dos funcionários em cada célula da grade de nine box
    cell_data = [top_left, top_middle, top_right, middle_left, middle_middle, middle_right, bottom_left, bottom_middle,
                 bottom_right]

    cell_porc = [[f'{round((len(x) / sum([len(y) for y in cell_data])) * 100, 1)} %'] if len(x) > 0 else ['0%'] for x in cell_data]    
    
    #cell_names = [f'{cell_names[x]} - {len(cell_data[x])}' if len(cell_data[x]) > 0 else cell_names[x] for x in range(len(cell_names))]
    
    return cell_names, cell_data, cell_porc


def calculoDesempenho(linhaBD, listDados2):
    if str(listDados2[linhaBD][33]) == '1':
        nomeIndProc = string_to_list(listDados2[linhaBD][29])
        N_metasProc = string_to_list(listDados2[linhaBD][30])
        N_DesProc = string_to_list(listDados2[linhaBD][31])
        P_IndProc = string_to_list(listDados2[linhaBD][32])
        procCola = listDados2[linhaBD][4].split(",")
        lauxmedProc = []
        for i in range(len(procCola)):
            for j in range(len(nomeIndProc[i])):
                if P_IndProc[i][j] == 'Positivo':
                    auxI = round(float(N_DesProc[i][j]),2) * 100 / round(float(N_metasProc[i][j]),2)
                    auxI = int(auxI)
                else:
                    auxI = round(float(N_metasProc[i][j]),2) * 100 / round(float(N_DesProc[i][j]),2)
                    auxI = int(auxI)                                                      
                lauxmedProc.append(auxI)
                
        medProc = sum(lauxmedProc) / len(lauxmedProc)
    else:
        medProc = 0

    if listDados2[linhaBD][34] != None and listDados2[linhaBD][34] != "" and not "" in string_to_list(
            listDados2[linhaBD][39]):
        nomeIndProj = string_to_list(listDados2[linhaBD][34])
        N_metasProj = string_to_list(listDados2[linhaBD][35])
        N_DesProj = string_to_list(listDados2[linhaBD][36])
        P_IndProj = string_to_list(listDados2[linhaBD][37])
        nameProj = string_to_list(listDados2[linhaBD][39])
        lauxmedProj = []
        for i in range(len(nameProj)):
            for j in range(len(nomeIndProj[i])):
               
                if P_IndProj[i][j] == 'Positivo':
                    auxI = round(float(N_DesProj[i][j]),2) * 100 / round(float(N_metasProj[i][j]),2)
                    auxI = int(auxI)
                else:
                    auxI = round(float(N_metasProj[i][j]),2) * 100 / round(float(N_DesProj[i][j]),2)
                    auxI = int(auxI)                                                      
                lauxmedProj.append(auxI)

        medProj = sum(lauxmedProj) / len(lauxmedProj)
    else:
        medProj = 0
    if medProc == "" or medProc == 0 or medProc == "None":
        medDes = medProj
    elif medProj == "" or medProj == 0 or medProj == "None":
        medDes = medProc
    else:
        medDes = (medProc + medProj) / 2
    return int(medDes)


def PlotDisperssao(skills, behaviors):
    
    # Cria o gráfico
    fig, ax = plt.subplots(figsize=(7, 7))
    # ax.pcolormesh(x, y, Z, shading='flat', vmin=Z.min(), vmax=Z.max())

    ax.plot(skills, behaviors, ls="", marker="o", ms=40, c="k")
    ax.plot(skills, behaviors, ls="", marker="o", ms=25, c="w")
    ax.plot(skills, behaviors, ls="", marker="o", ms=10, c="r")

    rect_top_left = matplotlib.patches.Rectangle((0, 85), 70, 1000, color='greenyellow')
    rect_top_middle = matplotlib.patches.Rectangle((70, 85), 15, 1000, color='deepskyblue')
    rect_top_right = matplotlib.patches.Rectangle((85, 85), 1000, 1000, color='b')
    rect_middle_left = matplotlib.patches.Rectangle((0, 70), 70, 15, color='khaki')
    rect_middle_middle = matplotlib.patches.Rectangle((70, 70), 15, 15, color='greenyellow')
    rect_middle_right = matplotlib.patches.Rectangle((85, 70), 1000, 15, color='deepskyblue')
    rect_bottom_left = matplotlib.patches.Rectangle((0, 0), 70, 70, color='lightcoral')
    rect_bottom_middle = matplotlib.patches.Rectangle((70, 0), 15, 70, color='khaki')
    rect_bottom_right = matplotlib.patches.Rectangle((85, 0), 1000, 70, color='greenyellow')

    ax.add_patch(rect_bottom_left)
    ax.add_patch(rect_bottom_middle)
    ax.add_patch(rect_bottom_right)
    ax.add_patch(rect_middle_left)
    ax.add_patch(rect_middle_middle)
    ax.add_patch(rect_middle_right)
    ax.add_patch(rect_top_left)
    ax.add_patch(rect_top_middle)
    ax.add_patch(rect_top_right)

    plt.xlabel("Desempenho", fontsize=15)
    plt.ylabel("Competência", fontsize=15)

    plt.xlim(-1, max(skills) + 20)  # definir limite do eixo
    plt.ylim(-1, max(behaviors) + 20)  # definir limite do eixo
    
    plt.gca().set_facecolor('none')
    # Define o fundo transparente
    plt.rcParams["figure.facecolor"] = "none"
    plt.rcParams["savefig.facecolor"] = "none"
    # Define as fontes na cor gray
    plt.rcParams["text.color"] = "gray"
    plt.rcParams["xtick.color"] = "gray"
    plt.rcParams["ytick.color"] = "gray"
    # Exibe o gráfico
    plt.show()
    st.pyplot(fig)


def PlotDisperssao1(dadosNinebox):

    employees = [x[0] for x in dadosNinebox]
    skills = [x[1] for x in dadosNinebox]
    behaviors = [x[2] for x in dadosNinebox]

    # Cria o gráfico
    fig, ax = plt.subplots(figsize=(10, 10))
    # ax.pcolormesh(x, y, Z, shading='flat', vmin=Z.min(), vmax=Z.max())
    ax.plot(skills, behaviors, ls="", marker="o", ms=10, c="k")
    ax.plot(skills, behaviors, ls="", marker="o", ms=5, c="w")
    ax.plot(skills, behaviors, ls="", marker="o", ms=2, c="r")
    rect_top_left = matplotlib.patches.Rectangle((0, 85), 70, 1000, color='greenyellow')
    rect_top_middle = matplotlib.patches.Rectangle((70, 85), 15, 1000, color='deepskyblue')
    rect_top_right = matplotlib.patches.Rectangle((85, 85), 1000, 1000, color='b')
    rect_middle_left = matplotlib.patches.Rectangle((0, 70), 70, 15, color='khaki')
    rect_middle_middle = matplotlib.patches.Rectangle((70, 70), 15, 15, color='greenyellow')
    rect_middle_right = matplotlib.patches.Rectangle((85, 70), 1000, 15, color='deepskyblue')
    rect_bottom_left = matplotlib.patches.Rectangle((0, 0), 70, 70, color='lightcoral')
    rect_bottom_middle = matplotlib.patches.Rectangle((70, 0), 15, 70, color='khaki')
    rect_bottom_right = matplotlib.patches.Rectangle((85, 0), 1000, 70, color='greenyellow')

    ax.add_patch(rect_bottom_left)
    ax.add_patch(rect_bottom_middle)
    ax.add_patch(rect_bottom_right)
    ax.add_patch(rect_middle_left)
    ax.add_patch(rect_middle_middle)
    ax.add_patch(rect_middle_right)
    ax.add_patch(rect_top_left)
    ax.add_patch(rect_top_middle)
    ax.add_patch(rect_top_right)

    # Adiciona o nome de cada funcionário dentro do círculo
    for i, txt in enumerate(employees):
        ax.annotate(txt, (skills[i], behaviors[i] + 1), fontsize=10, ha="center", va='bottom')

    plt.xlabel("Desempenho", fontsize=15)
    plt.ylabel("Competência", fontsize=15)

    plt.xlim(-1, max(skills) + 20)  # definir limite do eixo
    plt.ylim(-1, max(behaviors) + 20)  # definir limite do eixo
    
    
    plt.gca().set_facecolor('none')
    # Define o fundo transparente
    plt.rcParams["figure.facecolor"] = "none"
    plt.rcParams["savefig.facecolor"] = "none"
    # Define as fontes na cor gray
    plt.rcParams["text.color"] = "black"
    plt.rcParams["xtick.color"] = "black"
    plt.rcParams["ytick.color"] = "black"
    
    
    # Exibe o gráfico
    plt.show()
    st.pyplot(fig)


def ListaCellNine(listDadosAux, medDes, MedCom):
    # Cria uma interface gráfica com uma grade de nine box e botões para adicionar, editar e excluir funcionários
    top_left = [x[1] for x in listDadosAux if classify_employee(medDes, MedCom) == 'top_left']
    top_middle = [x[1] for x in listDadosAux if classify_employee(medDes, MedCom) == 'top_middle']
    middle_left = [x[1] for x in listDadosAux if classify_employee(medDes, MedCom) == 'middle_left']
    middle_middle = [x[1] for x in listDadosAux if classify_employee(medDes, MedCom) == 'middle_middle']
    top_right = [x[1] for x in listDadosAux if classify_employee(medDes, MedCom) == 'top_right']
    middle_right = [x[1] for x in listDadosAux if classify_employee(medDes, MedCom) == 'middle_right']
    bottom_left = [x[1] for x in listDadosAux if classify_employee(medDes, MedCom) == 'bottom_left']
    bottom_middle = [x[1] for x in listDadosAux if classify_employee(medDes, MedCom) == 'bottom_middle']
    bottom_right = [x[1] for x in listDadosAux if classify_employee(medDes, MedCom) == 'bottom_right']

    cell_names = ["Enigma", "Forte Potencial", "Alto Potencial", "Questionável", "Mantenedor", "Forte Desempenho",
                  "Insuficiente", "Eficaz", "Comprometido"]
    cell_data = [top_left, top_middle, top_right, middle_left, middle_middle, middle_right, bottom_left, bottom_middle,
                 bottom_right]

    return cell_names, cell_data


# Cria uma função para plotar todos os gráficos de barras horizontal em um único subplot
def plot_all_employees(cell_name, cell_employees, ploname=True):
    # Define o tamanho do gráfico
    plt.figure(figsize=(5, 5))
    # Percorre a lista com os nomes das células da grade de nine box e a lista com os dados dos funcionários
    for i, (cell_name, cell_employees) in enumerate(zip(cell_name, cell_employees)):
        # Cria um subplot
        plt.subplot(3, 3, i + 1)
        # Define uma lista de cores para as barras
        colors = ["greenyellow", "deepskyblue", "b", "khaki", "greenyellow", "deepskyblue", "lightcoral", "khaki",
                  "greenyellow"]
        # Plota o gráfico de barras horizontal para a célula da grade de nine box atual
        plt.barh(cell_employees, [1] * len(cell_employees))
        # Define o título do gráfico
        plt.title(cell_name)
        # Define o rótulo do eixo x
        # plt.xlabel("Funcionários")
        # Define o rótulo do eixo y
        plt.tick_params(left=False, right=False, labelleft=False,
                        labelbottom=False, bottom=False)
        # Percorre os nomes dos funcionários
        for j, employee_name in enumerate(cell_employees):
            # Adiciona um rótulo com o nome do funcionário no centro da barra
            if ploname:
                plt.text(0.5, employee_name, employee_name, horizontalalignment="center")
            # Define a cor da barra atual como uma cor aleatória
            plt.barh(cell_employees[j], 1, color=colors[i])
        plt.gca().set_facecolor('none')
        
    # Define o fundo transparente
    plt.rcParams["figure.facecolor"] = "none"
    plt.rcParams["savefig.facecolor"] = "none"
    # Define as fontes na cor gray
    plt.rcParams["text.color"] = "black"
    plt.rcParams["xtick.color"] = "black"
    plt.rcParams["ytick.color"] = "black"
    
    # Ajusta o espaçamento entre os subplots
    plt.tight_layout()
    plt.subplots_adjust(top=0.9)


def plot_all_employees1(cell_name, cell_employees):
    # Define o tamanho do gráfico
    plt.figure(figsize=(10, 10))
    # Percorre a lista com os nomes das células da grade de nine box e a lista com os dados dos funcionários
    for i, (cell_name, cell_employees) in enumerate(zip(cell_name, cell_employees)):
        # Cria um subplot
        plt.subplot(3, 3, i + 1)
        # Define uma lista de cores para as barras
        colors = ["greenyellow", "deepskyblue", "b", "khaki", "greenyellow", "deepskyblue", "lightcoral", "khaki",
                  "greenyellow"]
        # Plota o gráfico de barras horizontal para a célula da grade de nine box atual
        plt.barh(cell_employees, [1] * len(cell_employees))
        # Define o título do gráfico
        plt.title(cell_name)
        # Define o rótulo do eixo x
        # plt.xlabel("Funcionários")
        # Define o rótulo do eixo y
        plt.tick_params(left=False, right=False, labelleft=False,
                        labelbottom=False, bottom=False)
        # Percorre os nomes dos funcionários
        for j, employee_name in enumerate(cell_employees):
            # Adiciona um rótulo com o nome do funcionário no centro da barra
            plt.text(0.5, employee_name, employee_name, horizontalalignment="center", fontsize=45)
            # Define a cor da barra atual como uma cor aleatória
            plt.barh(cell_employees[j], 1, color=colors[i])
    
    plt.gca().set_facecolor('none')
    # Define o fundo transparente
    plt.rcParams["figure.facecolor"] = "none"
    plt.rcParams["savefig.facecolor"] = "none"

    # Define as fontes na cor gray
    plt.rcParams["text.color"] = "black"
    plt.rcParams["xtick.color"] = "black"
    plt.rcParams["ytick.color"] = "black"
    
    # Ajusta o espaçamento entre os subplots
    plt.tight_layout()
    plt.subplots_adjust(top=0.9)

     
def plot_all_employees2(cell_name, cell_employees):
    from plotly.subplots import make_subplots
    import plotly.graph_objects as go

    # Define as cores
    colors = ["#ADFF2F", "#00BFFF", "#0000FF", "#F0E68C", "#ADFF2F", "#00BFFF", "#F08080", "#F0E68C", "#ADFF2F"]

    # Cria uma figura com subplots
    fig = make_subplots(rows=3, cols=3, subplot_titles=cell_name)

    # Percorre a lista com os nomes das células da grade de nine box e a lista com os dados dos funcionários
    for i, employees in enumerate(cell_employees):

        # Cria um gráfico de barras horizontal para a célula da grade de nine box atual
        fig.add_trace(
            go.Bar(
                y=employees,
                x=[1] * len(employees),
                orientation='h',
                marker_color=colors[i]
            ),
            row=(i // 3) + 1,
            col=(i % 3) + 1
        )
        # adiciona o nome da célula no centro da barra
        #[ x.split()[0] for x in cell_employees[i]]
        fig.update_traces(text= cell_employees[i], 
                          insidetextanchor='middle', 
                          textposition='auto', 
                          row=(i // 3) + 1, 
                          col=(i % 3) + 1)

    # Remove as linhas dos eixos e os valores do eixo x e y  
    fig.update_xaxes(showgrid=False, showline=False, showticklabels=False)
    fig.update_yaxes(showgrid=False, showline=False, showticklabels=False)

    # Define o layout
    fig.update_layout(
        plot_bgcolor='ghostwhite',
        height=800,
        showlegend=False,
        margin=dict(l=0, r=0, t=20, b=30),
        xaxis_visible=False,
        yaxis_visible=False,
        xaxis_showticklabels=False,
        yaxis_showticklabels=False,
    )

    # Adiciona a figura ao Streamlit
    st.plotly_chart(fig, use_container_width = True)
      
    
# Cria uma função para classificar os funcionários em uma das nove células da grade de nine box
def classify_employee(skills, behavior):
    if behavior >= 85 and skills >= 85:
        return "top_right"
    elif behavior >= 85 and skills >= 70:
        return "top_middle"
    elif behavior >= 85 and skills < 70:
        return "top_left"
    elif behavior >= 70 and skills >= 85:
        return "middle_right"
    elif behavior >= 70 and skills >= 70:
        return "middle_middle"
    elif behavior >= 70 and skills < 70:
        return "middle_left"
    elif behavior < 70 and skills >= 85:
        return "bottom_right"
    elif behavior < 70 and skills >= 70:
        return "bottom_middle"
    elif behavior < 70 and skills < 70:
        return "bottom_left"


def string_to_list(string):
    return ast.literal_eval(string)


import plotly.graph_objects as go
def plotarRadar(data, categories, Nomes):
    #CRIANDO A FIGURA DO GRÁFICO
    fig = go.Figure()

    for idxName in range(len(Nomes)):
        fig.add_trace(go.Scatterpolar(
            r=data[idxName],#DADOS
            theta=categories,#CATEGORIAS
            fill='toself',
            name=f'{Nomes[idxName]}'))#NOME DA PESSOA

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100])
        ),
        showlegend=True,
        width=1200,  #ESQUERDA E DIREITA
        height=800,  #TAMANHO
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='center', x=0.5)#CENTRALIZANDO OS TITULOS 
    )

    st.plotly_chart(fig)

def plotarRadar2(data, categories, Nomes):
    #CRIANDO A FIGURA DO GRÁFICO
    fig = go.Figure()

    for idxName in range(len(Nomes)):
        fig.add_trace(go.Scatterpolar(
            r=data[idxName],#DADOS
            theta=categories,#CATEGORIAS
            fill='toself',
            name=f'{Nomes[idxName]}'))#NOME DA PESSOA

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100])
        ),
        showlegend=True,
        width=750,  #ESQUERDA E DIREITA
        height=800,  #TAMANHO
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='center', x=0.5)#CENTRALIZANDO OS TITULOS 
    )

    return fig


def listaCompNon0(data, categories):
    lisaux = []
    for i in range(len(data)):
        aux = []
        for j in range(len(data[i])):
            aux.append([data[i][j], categories[j]])
        lisaux.append(aux)
    lisaux1 = []
    for i in range(len(lisaux[0])):
        aux = []
        aux1 = []
        for j in range(len(lisaux)):
            aux1.append(lisaux[j][i][0])
            aux.append(lisaux[j][i])

        if aux1.count(0) < len(aux1):
            lisaux1.append(aux)

    return [[lisaux1[x][y][0] for x in range(len(lisaux1))] for y in range(len(lisaux1[0]))], \
           [[lisaux1[x][y][1] for x in range(len(lisaux1))] for y in range(1)][0]

def menu9BoxHtml(nome, page):
    menu9Box = f"""<div class="fixed">
            <div class="menu">
                <div class="logo">
                    <img src="https://raw.githubusercontent.com/RahyanRamos/LogoNineBox/main/logo.png" alt="Logo do 9Box">
                </div>
                <div class="botoes">
                    <!-- <a href="https://meusprojetos-mpjj.streamlit.app/" target="_self"><button type="button" id="home">Home</button></a>
                    <a href="https://meusprojetos-mpjj.streamlit.app/Meus_Projetos" target="_self"><button type="button" id="projetos">Projetos</button></a>
                    <a href="https://meusprojetos-mpjj.streamlit.app/Pr%C3%AAmio" target="_self"><button type="button" id="premio">Prêmio</button></a> -->
                    <div class="page"><p>{page}</p></div>
                </div>
                <div class="nome"><p>{nome}</p></div>
                <div class="icone">
                    <!-- <button type="button"><img src="https://cdn-icons-png.flaticon.com/128/5261/5261124.png" alt="ícone de configurações para alteração do módulo de uso"></button>
                    <div class="modulo">
                        <a href="https://meusprojetos-mpjj.streamlit.app/"><button type="button">Módulo de Execução</button></a>
                        <a href="https://meusprojetos-mpjj-mg.streamlit.app/"><button type="button">Módulo de Gestão</button></a>
                    </div> -->
                </div>
            </div>
        </div>"""
    return menu9Box

def menu9BoxCss():
    styleMenu9Box = f""".fixed{{
            position: fixed;
            top: 0;
            z-index: 999990;
            left: 50px;
            right: 50px;
        }}

        .menu{{
            display: flex;
            position: absolute;
            align-items: center;
            /*background: linear-gradient(to bottom, #06405c);*/
            background-color: #06405c;
            color: #fff;
            padding: 10px 20px;
            width: 100%;
            height: 46px;
            border-bottom-left-radius: 15px;
            border-bottom-right-radius: 15px;
        }}

        .logo,
        .botoes{{
            margin-right: auto;
        }}

        .logo img{{
            width: 100px;
            font-family: 'M PLUS Rounded 1c', sans-serif;
            font-size: 10px;
            margin: 0;
        }}

        .botoes{{
            margin-top: 10px;
        }}

        .botoes p{{
            font-weight: bold;
            background-color: #ffc000;
            padding: 0px 15px;
            border-radius: 8px;
            font-size: 18px;
            color: #06405c;
        }}

        .botoes button{{
            margin-right: 10px;
            padding: 0px 10px;
            border: none;
            background-color: transparent;
            color: #fff;
            cursor: pointer;
            font-weight: bold;
            font-size: 16px;
            transition: border-color 0.5s ease;
        }}

        .nome p{{
            margin-right: 10px;
            color: #ffc000;
            font-weight: bold;
            font-size: 16px;
            margin-top: 12px;
        }}

        .icone img{{
            width: 35px;
            height: 35px;
        }}

        .icone button{{
            background-color: #9fdafc;
            border-radius: 50%;
            cursor: pointer;
            border: none;
            width: 40px;
            height: 40px;
        }}

        .modulo{{
            display: none;
            position: absolute;
            top: auto;
            right: 0;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
            background-color: #9fdafc;
            height: auto;
            width: 175px;
            border-radius: 10px;
            padding: 10px;
            margin-top: 10px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
        }}

        .modulo button{{
            border-radius: 8px;
        }}

        .modulo:after{{
            content: "";
            width: 0;
            height: 0;
            position: absolute;
            border-left: 15px solid transparent;
            border-right: 15px solid transparent;
            border-bottom: 20px solid #9fdafc;
            top: -15px;
            right: 25px
        }}

        .icone:hover .modulo{{
            display: block;
        }}

        .modulo button{{
            display: block;
            width: 100%;
            padding: 5px;
            text-align: left;
            background-color: transparent;
            border: none;
            cursor: pointer;
            font-weight: bold;
            color: #000;
            margin-bottom: 5px;
        }}

        .botoes button:hover{{
            border: none;
            border-bottom: 2px solid #26eda2;
            cursor: pointer;
        }}

        .modulo button:hover{{
            background-color: #91c1dd;
        }}

        .logo:hover{{
            text-decoration: underline;
        }}
        
        @media screen and (max-width: 650px){{
            .menu{{
                flex-direction: column;
                height: auto;
                max-height: 50px;
            }}

            .botoes{{
                margin-top: 10px;
            }}

            button{{
                margin: 5px 0;
            }}

            .icone{{
                margin-top: 10px;
            }}

            .modulo{{
                right: -20px;
            }}
        }}"""
    return styleMenu9Box
