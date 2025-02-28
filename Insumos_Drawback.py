import streamlit as st
from Producao_Entregas import producao_total
from Producao_Entregas import perda
from Producao_Entregas import total_contrato
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.title("Insumos e Drawback")

tx_perda_esperada = 0.05
tx_consumo_esperada = (producao_total/(1-tx_perda_esperada))/total_contrato
tx_consumo_real = (producao_total+perda)/total_contrato

insumos = ['papel', 'papel','papel','papel', 'holograma', 'spark', 'spark', 'spark', 'outros']
qntd = [50, 50, 50, 90, 45, 80, 20, 40, 150]
drwbck = ['sim', 'sim', 'sim', 'sim', 'sim', 'nao', 'nao', 'nao', 'nao']
registro_drwbck = ['d1256', 'd2536', 'd8569', 'd8963', 'd5698', 0, 0, 0, 0]
df_insumos = pd.DataFrame({'Insumo': insumos, 'Quantidade': qntd, 'Drawback': drwbck, 'Registro': registro_drwbck})

qntd_papel = df_insumos.loc[df_insumos["Insumo"] == "papel", "Quantidade"].sum()
qntd_holograma = df_insumos.loc[df_insumos["Insumo"] == "holograma", "Quantidade"].sum()
qntd_spark = df_insumos.loc[df_insumos["Insumo"] == "spark", "Quantidade"].sum()
qntd_outros = df_insumos.loc[df_insumos["Insumo"] == "outros", "Quantidade"].sum()

tx_consumo_papel_esperada = 100*qntd_papel*tx_consumo_esperada/qntd_papel
tx_consumo_holograma_esperada = 100*qntd_holograma*tx_consumo_esperada/qntd_holograma
tx_consumo_spark_esperada = 100*qntd_spark*tx_consumo_esperada/qntd_spark
tx_consumo_outros_esperada = 100*qntd_outros*tx_consumo_esperada/qntd_outros

tx_consumo_papel_real = 98
tx_consumo_holograma_real = 98.5
tx_consumo_spark_real = 102
tx_consumo_outros_real = 97.5


lista_tx_consumo_esperado = [tx_consumo_papel_esperada, tx_consumo_holograma_esperada,tx_consumo_spark_esperada, tx_consumo_outros_esperada]
lista_tx_consumo_real = [tx_consumo_papel_real,tx_consumo_holograma_real,tx_consumo_spark_real,tx_consumo_outros_real]
insumos_agg = ['papel', 'holograma', 'spark', 'outros']

df_tx_consumo = pd.DataFrame({'Insumo': insumos_agg, 'Esperado':lista_tx_consumo_esperado,'Real':lista_tx_consumo_real})

#fig_consumo_insumo = px.bar(df_tx_consumo, y="Real", text_auto=True)
#fig_consumo_insumo.update_traces(marker_color=["blue" if valor <= 1 else "red" for valor in df_tx_consumo['Real']])
#fig_consumo_insumo.add_shape(type="line", x0=-0.5, x1=len(df_tx_consumo) - 0.5, y0=1, y1=1, line=dict(color="orange", dash="dot", width=2))
#fig_consumo_insumo.update_layout(yaxis_tickformat=".0%", showlegend=False)

fig_consumo_insumo = px.bar(df_tx_consumo, x="Insumo", y="Real", text=df_tx_consumo['Real'].apply(lambda x: f'{x:.2f}%'))
fig_consumo_insumo.update_layout(xaxis_title=None, yaxis_title=None, showlegend=True, yaxis={'visible': False}, xaxis={'visible': True})
fig_consumo_insumo.update_traces(marker_color=["blue" if valor <= 100 else "red" for valor in df_tx_consumo['Real']])
fig_consumo_insumo.add_shape(type="line", x0=-0.5, x1=len(df_tx_consumo) - 0.5, y0=100, y1=100, line=dict(color="orange", dash="dot", width=2))

df_draw = df_insumos[df_insumos["Drawback"] == 'sim']
qntd_papel_consumida = qntd_papel*tx_consumo_papel_real*tx_consumo_real/100
qntd_holograma_consumida = qntd_holograma*tx_consumo_holograma_real*tx_consumo_real/100

df_draw['Saldo'] = [100*50/qntd[0],100*50/qntd[1],100*50/qntd[2],100*(qntd_papel_consumida-qntd[0]-qntd[1]-qntd[2])/qntd[3],100*qntd_holograma_consumida/qntd[4]]
df_draw['Saldo'] = df_draw['Saldo'].apply(lambda x: f'{x:.1f}%')

fig_draw = px.bar(df_draw, x='Saldo', y='Registro', orientation='h', color= 'Insumo', text=df_draw['Saldo'])
fig_draw.update_layout(xaxis_title=None, yaxis_title=None, showlegend=True,
                       yaxis={'visible': True}, xaxis={'visible': False})


col1, col2 = st.columns(2)
col3, col4 = st.columns(2)

with col1:
    st.header("Registro de Insumos")
    st.dataframe(df_insumos)

with col2:
    st.header("Controle da Taxa de Consumo")
    col2.plotly_chart(fig_consumo_insumo)

with col3:
    st.header("Controle Drawback")
    col3.plotly_chart(fig_draw)

with col4:
    st.header("Saldo Drawback")
    st.text(f'Saldo em Estoque:\nPapel: {round(qntd_papel - qntd_papel_consumida,1)}kg\nHolograma: {round(qntd_holograma - qntd_holograma_consumida,1)}kg')
