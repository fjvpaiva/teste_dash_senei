import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import datetime
import numpy as np
from pandas.io.sas.sas_constants import page_size_offset

from Producao_Entregas import producao_total
from Producao_Entregas import total_contrato
from Producao_Entregas import df
from Producao_Entregas import df_entrega

st.title("Financeiro")

custo_milheiro = 12.15

df_embarque = df_entrega.copy()
df_embarque = df_embarque.rename(columns={'Produção Diária': 'Entrega Total'})

mes_ano =[]
mes_in = df_embarque['Mês'].to_list()
for i in mes_in:
    if i in ['January', 'February', 'March', 'April']:
        mes_ano.append(i+'/2025')
    else:
        mes_ano.append(i+'/2024')
df_embarque['Mês'] = pd.to_datetime(mes_ano, format='%B/%Y')
df_embarque['Mês'] = df_embarque['Mês'].dt.strftime('%Y-%m')
df_embarque = df_embarque.sort_values(by='Mês')

lista_nf = ['01/2024', '02/2024', '01/2025', '02/2025', '03/2025',0]
df_embarque['Nota Fiscal'] = lista_nf
df_embarque['Valor da NF (U$)'] = df_embarque['Entrega Total']*custo_milheiro
df_embarque['Pagamento'] = ['efetivado','efetivado','efetivado','efetivado','no prazo',0]

contratado = total_contrato*custo_milheiro
emitido = df_embarque['Valor da NF (U$)'].sum()
pago = df_embarque.loc[df_embarque['Pagamento'] == 'efetivado', 'Valor da NF (U$)'].sum()
prazo = df_embarque.loc[df_embarque['Pagamento'] == 'no prazo', 'Valor da NF (U$)'].sum()

fig_finan = go.Figure(go.Waterfall(name = "20", orientation = "v", measure = ["absolute", "relative", "relative", "relative", "total"],
                                   x = ['Valor do Contrato', 'Pago', 'Aguardando Pagamento','Atraso', 'Não Emitido'], textposition = "outside",
                                   y = [contratado, -pago, -prazo, 0, -contratado + emitido],connector = {"line":{"color":"rgb(63, 63, 63)"}}))


col1, col2 = st.columns(2)
col3, col4 = st.columns(2)
col1.dataframe(df_embarque)
col2.text(f'Valor total do contrato: U${round(contratado,2):,}\nValor total das Notas Fiscais emitidas: U${round(emitido,2):,}\n'
          f'Valor total das Notas Fiscais pagas: U${round(pago,2):,}\nValor total das Notas Fiscais aguardando pagamento: U${round(prazo,2):,}\n'
          f'Valor total das Notas Fiscais em atraso: U$0.00')
col3.plotly_chart(fig_finan)    
