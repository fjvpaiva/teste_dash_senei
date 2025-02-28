import streamlit as st
import pandas as pd
import plotly.express as px
import datetime
import numpy as np
from streamlit import plotly_chart

st.title("Controle de Produção e Entregas")

data_inicial = datetime.datetime.strptime("01/11/2024", "%d/%m/%Y").date()
data_final = datetime.datetime.strptime("15/04/2025", "%d/%m/%Y").date()
lista_dias_prod = []

col1, col2 = st.columns(2)
col3, col4, col5 = st.columns(3)

    # Calcula o número de dias entre as datas
num_dias = (data_final - data_inicial).days + 1

    # Gera a lista de datas usando um laço for
data_atual = data_inicial  # Inicializa data_atual fora do loop
for _ in range(num_dias):  # Use _ se o índice não for necessário
    lista_dias_prod.append(data_atual)
    data_atual = data_atual + datetime.timedelta(days=1) # Adiciona sempre um dia

lista_prod = []
for i in range(len(lista_dias_prod)):
  x = int(10000.0*(1.05-np.random.rand()/10))
  lista_prod.append(x)

df = pd.DataFrame({'Dias de Produção': lista_dias_prod, 'Produção Diária': lista_prod})
df['Dias de Produção'] = pd.to_datetime(df['Dias de Produção'])
df['Mês'] = df['Dias de Produção'].dt.strftime('%B')

df_entrega = df.copy()
df_entrega['Dias de Produção'] = pd.to_datetime(df_entrega['Dias de Produção'])
df_entrega['Mês'] = df_entrega['Dias de Produção'].dt.strftime('%B')
df_entrega = df_entrega.drop('Dias de Produção', axis=1)
df_entrega = df_entrega.groupby(["Mês"])['Produção Diária'].sum().reset_index()
df_entrega.iloc[0, 1] = 0
ordem_meses = ['November', 'December', 'January', 'February', 'March', 'April']
df_entrega['Mês'] = pd.Categorical(df_entrega['Mês'], categories=ordem_meses, ordered=True)

total_contrato = 2400000
producao_total = df['Produção Diária'].sum()
producao_entrega = df_entrega['Produção Diária'].sum()
pendente = producao_total - producao_entrega
perda = 20412

data = {
    'Categoria': ['Contrato', 'Produção Aprovada', 'Perda'],
    'Quantidade': [total_contrato, producao_total, perda]}

df_contrato = pd.DataFrame(data)

data_pendencia = {
    'Categoria': ['Produção Aprovada', 'Entregue', 'Entrega Pendente'],
    'Quantidade': [producao_total, producao_entrega, pendente]}

df_pendencia = pd.DataFrame(data_pendencia)

x = [0.05, perda/producao_total]
df_perda = pd.DataFrame({'Legenda':['Limite de Perda','Perda'], 'Valor': [0.05,perda/producao_total]})
df_perda['Valor'] *= 100
#df_perda = pd.DataFrame('Perda': [0.05,perda/producao_total]})

fig_prod = px.bar(df, x="Dias de Produção", y="Produção Diária", color="Mês",
                     title="Produção Diária")
fig_prod.update_layout(yaxis_range=[9000, max(df['Produção Diária'])])


fig_entrega = px.bar(df_entrega, x="Mês", y="Produção Diária", color="Mês",
                     title="Entregas Mensais", category_orders={"Mês": ordem_meses})
fig_entrega.update_layout(yaxis_range=[250000, max(df_entrega['Produção Diária'])])

cores = {'Contrato': 'rgb(0, 0, 255)', 'Produção Aprovada': 'rgb(0, 255, 0)', 'Entrega Pendente': 'rgb(255, 255, 0)',
         'Perda': 'rgb(255, 0, 0)'}
fig_contrato = px.bar(df_contrato, x="Categoria", y="Quantidade", color="Categoria",
                      color_discrete_map=cores, title="Resumo da Produção")

fig_pendencia = px.bar(df_pendencia, x="Categoria", y="Quantidade", color="Categoria",
                      color_discrete_map=cores, title="Resumo das Entregas")

color_perda= {'Perda': 'rgb(255, 0, 0)', 'Limite de Perda': 'rgb(255, 102, 0)'}
fig_perda = px.bar(df_perda, x="Valor", y=[0,0], orientation='h', color= 'Legenda',  color_discrete_map=color_perda,
                   text=df_perda['Valor'].apply(lambda x: f'{x:.2f}%'), title="Perda Apurada")
fig_perda.update_layout(barmode='overlay', xaxis_title=None, yaxis_title=None, showlegend=True,
                        yaxis={'visible': False}, xaxis={'visible': False})

col1.plotly_chart(fig_prod)
col2.plotly_chart(fig_contrato)
col3.plotly_chart(fig_entrega)
col4.plotly_chart(fig_pendencia)
col5.plotly_chart(fig_perda)