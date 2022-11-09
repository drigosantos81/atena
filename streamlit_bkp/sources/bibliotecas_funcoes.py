# Importação de Bibliotecas e Definição de constantes, pastas, arquivos...
import altair as alt
import numpy as np
from pathos.pools import ProcessPool
import os
import streamlit as st
from streamlit_option_menu import option_menu
import warnings
warnings.filterwarnings('ignore')
import getpass 
import datetime
import time ; from datetime import date,timedelta
from hdbcli import dbapi
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder
from st_aggrid.shared import GridUpdateMode
from copy import deepcopy
import hydralit_components as hc
import matplotlib.pyplot as plt
import numpy as np
from dateutil.relativedelta import relativedelta
from streamlit_folium import folium_static
import folium
import plotly.express as px
import folium.plugins as plugins
from folium.plugins import FastMarkerCluster
import json
import xlsxwriter
from io import BytesIO
import streamlit.components.v1 as components_html

import folium
from folium.plugins import Search
from folium.plugins import MarkerCluster


#pd.options.display.float_format = "{:,.2f}".format


# Definicação das datas para realização das consultas
dia_semana = datetime.datetime.today().weekday()
if dia_semana == 0: #segunda
    st.session_state.data_pedido = date.today() - timedelta(3)
    st.session_state.data_pedido_mapa = date.today() - timedelta(3)
    st.session_state.data_selecao_hoje = date.today()
elif dia_semana == 6: #domingo
    st.session_state.data_pedido = date.today() - timedelta(3)
    st.session_state.data_pedido_mapa = date.today() - timedelta(3)
    st.session_state.data_selecao_hoje = date.today() - timedelta(2)
elif dia_semana == 5: #sabado
    st.session_state.data_pedido = date.today() - timedelta(2)
    st.session_state.data_pedido_mapa = date.today() - timedelta(2)
    st.session_state.data_selecao_hoje = date.today() - timedelta(1)
else: #terça, quarta, quinta, sexta
    #alterado para 0 em 06-09-2022, voltar para 1 em 08/09
    st.session_state.data_pedido = date.today() - timedelta(1)
    st.session_state.data_pedido_mapa = date.today() - timedelta(1)
    st.session_state.data_selecao_hoje = date.today()




#def convert_defasagem_hoje_excel(df):
     #return df.to_excel('Defasagem Hoje.xlsx',index=False,encoding='utf-8-sig')


#icons: moeda -> cash-coin - 
#'icon':'fa fa-info-circle' -> exclamação no circulo
#'icon': "bi bi-hand-thumbs-up" -> "joinha"
#'icon': 'fa fa-times-circle' -> circulo com x
#5C881A -> verde escuro


#INICIO MENU PRINCIPAL
menu_data_2 = [
    {'label':"LOGIN",'icon': 'bi bi-person'},
    #{'label':"CONSULTAS SQL",'icon': 'bi bi-search','submenu':[{'label':"CONSULTA CONTA CONTRATO", 'icon': "bi bi-bookmark-check"},{'icon':'bi bi-list-nested','label':"FORMATO SQL",}]},
    #{'label':"ATENA", 'icon':'bi bi-info-circle'},
    {'label':"SELEÇÃO", 'icon':'bi bi-scissors','submenu':[{'label':"DEFASAGEM POR ZONAS", 'icon': "bi bi-bookmark-check"},{'label':"DEFASAGEM POR UTDs", 'icon': "bi bi-bookmark-check"},{'label':"SELEÇÃO D+1 (UTDs)", 'icon': "bi bi-tools"},{'label':"SELEÇÃO D+1 (ZONAS)", 'icon': "bi bi-tools"},
    #{'label':"PRONTIDAO", 'icon': "bi bi-tools"}
    ]},
    #{'label':"AÇÕES",'icon': "bi bi-gear"},
    {'label':"MAPA",'icon': "bi bi-geo-alt",'submenu':[{'label':"MAPA SELECAO", 'icon': "bi bi-bookmark-check"},{'label':"MAPA SUSCETIVEIS", 'icon': "bi bi-bookmark-check"}]},
    {'label':"DASHBOARD", 'icon':'bi bi-graph-up','submenu':[{'label':"ACOMPANHAMENTO GERACAO", 'icon': "bi bi-bookmark-check"}]},
    {'label':"SUSCETIVEIS", 'icon':'bi bi-cash-coin','submenu':[{'label':"SUSCETIVEIS", 'icon': 'bi bi-cash-coin'},{'label':"SUSCETIVEIS PARA MAPA", 'icon': 'bi bi-cash-coin'}]},
]
over_theme_2 = {'txc_inactive': '#5C881A','menu_background':'#FFFFFF','txc_active':'#FFFFFF','option_active':'#73A616','font-size':'300%','font-style':'bold'}
#FINAL MENU PRINCIPAL

def testar_login():
    try:
        connection_hana = dbapi.connect(address='BRNEO695',port='30015',user=st.session_state.usuario,password=st.session_state.senha,databasename='BNP',sslValidateCertificate=True)
        st.success('USUÁRIO LOGADO COM SUCESSO!')
        st.session_state.check_login = 1
        st.session_state.usuario_u = 'u'+st.session_state.usuario[3:]
        if str.lower(st.session_state.usuario) == 'clb344173':
            st.session_state.nome_usuario = 'Thiago Jonas'
        elif str.lower(st.session_state.usuario) == 'clb352618':
            st.session_state.nome_usuario = 'Rodrigo Emanuel'
    except Exception as e:
        st.session_state.check_login = 0
        st.error("ERRO NA CONEXÃO COM O SAP HANA")



#função para plotar em tabela
def aggrid_interactive_table(df: pd.DataFrame):
    options = GridOptionsBuilder.from_dataframe(
        df, enableRowGroup=True, enableValue=True, enablePivot=True
    )
    options.configure_side_bar()
    options.configure_selection("single")
    selection = AgGrid(
        df,
        enable_enterprise_modules=True,
        gridOptions=options.build(),
        theme="light",
        update_mode=GridUpdateMode.MANUAL,
        allow_unsafe_jscode=True,
    )
    return selection


def coletar_suscetiveis_total():

  txt_sql_consulta_suscetiveis = 'SuscetiveisTabela'
  consulta = ['../sources/Sqls/'+ txt_sql_consulta_suscetiveis + '.sql']
  arquivo_sql_consulta_suscetiveis = open(consulta[0], encoding="utf-8")
  sql_consulta_suscetiveis = arquivo_sql_consulta_suscetiveis.read()
  arquivo_sql_consulta_suscetiveis.close()
  sql_consulta_suscetiveis = sql_consulta_suscetiveis.format(carteira = "CONVENCIONAL",data_pedido = st.session_state.data_hoje, turma = "STC")
  connection_hana = dbapi.connect(address='BRNEO695',port='30015',user=st.session_state.usuario,password=st.session_state.senha,databasename='BNP',sslValidateCertificate=False)
  base_suscetiveis = pd.read_sql(sql_consulta_suscetiveis, connection_hana)  

  sql = """
          select ACAO, COUNT(DISTINCT TEMP_ATENA.ZCGACCOUN) AS QTD_SUSCETIVEIS,UTD,ZONA, SUM(ZCGMTVCOB) AS MONTANTE, SUM(PECLD_CONS) AS PECLD, SUM(PECLD_CONS)/COUNT(DISTINCT TEMP_ATENA.ZCGACCOUN) AS TICKET_PECLD, AVG(SCORE) AS MEDIA_SCORE, AVG(ZCGQTFTVE) AS MEDIA_FAT_VENCIDAS 
          from
          (SELECT DATAREF, CASE WHEN ACAO = 'DISJ' OR ACAO = 'DISJUNTOR' THEN 'CORTE' ELSE ACAO END AS ACAO,
      UTD, ZCGACCOUN, ZCGMTVCOB, PECLD_CONS, LATITUDE, LONGITUDE, ZONA, ZCGMUNICI, ZCGLOCALI, ZCGBAIRRO, SCORE, ZCGQTFTVE, ZCGTIPLOC
      FROM CLB961920.TEMP_ATENA) as TEMP_ATENA
  LEFT JOIN (SELECT ZCGNMLOGR AS RUA, ZCGACCOUN FROM CLB_CCS_ICC.ZCT_DS_CLI001 CLI001) AS CLI001
          ON CLI001.ZCGACCOUN =  TEMP_ATENA.ZCGACCOUN
      GROUP BY ACAO,UTD,ZONA
              ORDER BY SUM(PECLD_CONS) DESC, COUNT(DISTINCT TEMP_ATENA.ZCGACCOUN) DESC
      """ 
  base_suscetiveis_total = pd.read_sql(sql, connection_hana)  
  base_suscetiveis_total["TURMA"] = 'STC'
  base_suscetiveis_total["TIPO"] = 'CS'
  base_suscetiveis_total['ZONA'] = base_suscetiveis_total['ZONA'].fillna("-")

  txt_sql_consulta_suscetiveis = 'SuscetiveisTabela'
  consulta = ['../sources/Sqls/'+ txt_sql_consulta_suscetiveis + '.sql']
  arquivo_sql_consulta_suscetiveis = open(consulta[0], encoding="utf-8")
  sql_consulta_suscetiveis = arquivo_sql_consulta_suscetiveis.read()
  arquivo_sql_consulta_suscetiveis.close()
  sql_consulta_suscetiveis = sql_consulta_suscetiveis.format(carteira = "CONVENCIONAL",data_pedido = st.session_state.data_hoje, turma = "EPS")
  connection_hana = dbapi.connect(address='BRNEO695',port='30015',user=st.session_state.usuario,password=st.session_state.senha,databasename='BNP',sslValidateCertificate=False)
  base_suscetiveis = pd.read_sql(sql_consulta_suscetiveis, connection_hana)  

  sql = """
          select ACAO, COUNT(DISTINCT TEMP_ATENA.ZCGACCOUN) AS QTD_SUSCETIVEIS,UTD,ZONA, SUM(ZCGMTVCOB) AS MONTANTE, SUM(PECLD_CONS) AS PECLD, SUM(PECLD_CONS)/COUNT(DISTINCT TEMP_ATENA.ZCGACCOUN) AS TICKET_PECLD, AVG(SCORE) AS MEDIA_SCORE, AVG(ZCGQTFTVE) AS MEDIA_FAT_VENCIDAS 
          from
          (SELECT DATAREF, CASE WHEN ACAO = 'DISJ' OR ACAO = 'DISJUNTOR' THEN 'CORTE' ELSE ACAO END AS ACAO,
      UTD, ZCGACCOUN, ZCGMTVCOB, PECLD_CONS, LATITUDE, LONGITUDE, ZONA, ZCGMUNICI, ZCGLOCALI, ZCGBAIRRO, SCORE, ZCGQTFTVE, ZCGTIPLOC
      FROM CLB961920.TEMP_ATENA) as TEMP_ATENA
  LEFT JOIN (SELECT ZCGNMLOGR AS RUA, ZCGACCOUN FROM CLB_CCS_ICC.ZCT_DS_CLI001 CLI001) AS CLI001
          ON CLI001.ZCGACCOUN =  TEMP_ATENA.ZCGACCOUN
      GROUP BY ACAO,UTD,ZONA
              ORDER BY SUM(PECLD_CONS) DESC, COUNT(DISTINCT TEMP_ATENA.ZCGACCOUN) DESC
      """ 
  base_suscetiveis2 = pd.read_sql(sql, connection_hana) 
  base_suscetiveis2["TURMA"] = 'EPS'
  base_suscetiveis2["TIPO"] = 'CS' 
  base_suscetiveis2['ZONA'] = base_suscetiveis2['ZONA'].fillna("-")
  base_suscetiveis_total = pd.merge(base_suscetiveis_total, base_suscetiveis2, how = 'outer')

  txt_sql_consulta_suscetiveis = 'SuscetiveisTabela'
  consulta = ['../sources/Sqls/'+ txt_sql_consulta_suscetiveis + '.sql']
  arquivo_sql_consulta_suscetiveis = open(consulta[0], encoding="utf-8")
  sql_consulta_suscetiveis = arquivo_sql_consulta_suscetiveis.read()
  arquivo_sql_consulta_suscetiveis.close()
  sql_consulta_suscetiveis = sql_consulta_suscetiveis.format(carteira = "RECORTE",data_pedido = st.session_state.data_hoje, turma = "STC")
  connection_hana = dbapi.connect(address='BRNEO695',port='30015',user=st.session_state.usuario,password=st.session_state.senha,databasename='BNP',sslValidateCertificate=False)
  base_suscetiveis = pd.read_sql(sql_consulta_suscetiveis, connection_hana)  

  sql = """
          select ACAO, COUNT(DISTINCT TEMP_ATENA.ZCGACCOUN) AS QTD_SUSCETIVEIS,UTD,ZONA, SUM(ZCGMTVCOB) AS MONTANTE, SUM(PECLD_CONS) AS PECLD, SUM(PECLD_CONS)/COUNT(DISTINCT TEMP_ATENA.ZCGACCOUN) AS TICKET_PECLD, AVG(SCORE) AS MEDIA_SCORE, AVG(ZCGQTFTVE) AS MEDIA_FAT_VENCIDAS 
          from
          (SELECT DATAREF, CASE WHEN ACAO = 'DISJ' OR ACAO = 'DISJUNTOR' THEN 'CORTE' ELSE ACAO END AS ACAO,
      UTD, ZCGACCOUN, ZCGMTVCOB, PECLD_CONS, LATITUDE, LONGITUDE, ZONA, ZCGMUNICI, ZCGLOCALI, ZCGBAIRRO, SCORE, ZCGQTFTVE, ZCGTIPLOC
      FROM CLB961920.TEMP_ATENA) as TEMP_ATENA
  LEFT JOIN (SELECT ZCGNMLOGR AS RUA, ZCGACCOUN FROM CLB_CCS_ICC.ZCT_DS_CLI001 CLI001) AS CLI001
          ON CLI001.ZCGACCOUN =  TEMP_ATENA.ZCGACCOUN
      GROUP BY ACAO,UTD,ZONA
              ORDER BY SUM(PECLD_CONS) DESC, COUNT(DISTINCT TEMP_ATENA.ZCGACCOUN) DESC
      """ 
  base_suscetiveis2 = pd.read_sql(sql, connection_hana) 
  base_suscetiveis2["TURMA"] = 'RECORTE'
  base_suscetiveis2["TIPO"] = 'CA' 
  base_suscetiveis2['ZONA'] = base_suscetiveis2['ZONA'].fillna("-")
  st.session_state.base_suscetiveis_total = pd.merge(base_suscetiveis_total, base_suscetiveis2, how = 'outer')
  st.session_state.base_suscetiveis_total["TIPO_ZONA"] = st.session_state.base_suscetiveis_total["TIPO"] + st.session_state.base_suscetiveis_total["ZONA"]
  st.session_state.base_suscetiveis_total["TIPO_ZONA_TURMA"] = st.session_state.base_suscetiveis_total["TIPO"] + st.session_state.base_suscetiveis_total["ZONA"] + st.session_state.base_suscetiveis_total["TURMA"]
  cols =['TIPO_ZONA_TURMA','TIPO_ZONA','QTD_SUSCETIVEIS','PECLD','TICKET_PECLD','MONTANTE','ZONA','TURMA','ACAO','UTD']
  st.session_state.base_suscetiveis_total = st.session_state.base_suscetiveis_total[cols]
  st.session_state.base_suscetiveis_total['ZONA'] = st.session_state.base_suscetiveis_total['ZONA'].fillna("-")
  return st.session_state.base_suscetiveis_total

def get_metas_orcamento_cobranca():
  aba_metas = "Base (Planejado)"
  aba_orcamento = "Orçamento"
  ano_inteiro_hoje = str(date.today().year)
  ano_hoje = str(date.today().year)[2:]
  mes_hoje = int(date.today().month)
  mes_anterior = int(date.today().month) - 1
  mes_anterior_2 = int(date.today().month) - 2
  if len(str(mes_hoje)) == 1:
      mes_hoje_str = '0' + str(mes_hoje)
  if len(str(mes_anterior)) == 1:
      mes_anterior_str = '0' + str(mes_anterior)
  if len(str(mes_anterior_2)) == 1:
      mes_anterior_2_str = '0' + str(mes_anterior_2)
  filtro_mes_ref = int(ano_inteiro_hoje + mes_hoje_str)
  filtro_mes_ref_orcamento = int(ano_inteiro_hoje + mes_anterior_str)
  filtro_mes_ref_orcamento_2 = int(ano_inteiro_hoje + mes_anterior_2_str)

  if mes_hoje == 1:
      nome_arquivo = "Dashboard Cobranca Jan"+ano_hoje
  elif mes_hoje == 2:
      nome_arquivo = "Dashboard Cobranca Fev"+ano_hoje
      nome_arquivo_anterior = "Dashboard Cobranca Jan"+ano_hoje
  elif mes_hoje == 3:
      nome_arquivo = "Dashboard Cobranca Mar"+ano_hoje
      nome_arquivo_anterior = "Dashboard Cobranca Fev"+ano_hoje
  elif mes_hoje == 4:
      nome_arquivo = "Dashboard Cobranca Abr"+ano_hoje
      nome_arquivo_anterior = "Dashboard Cobranca Mar"+ano_hoje
  elif mes_hoje == 5:
      nome_arquivo = "Dashboard Cobranca Mai"+ano_hoje
      nome_arquivo_anterior = "Dashboard Cobranca Abr"+ano_hoje
  elif mes_hoje == 6:
      nome_arquivo = "Dashboard Cobranca Jun"+ano_hoje
      nome_arquivo_anterior = "Dashboard Cobranca Mai"+ano_hoje
  elif mes_hoje == 7:
      nome_arquivo = "Dashboard Cobranca Jul"+ano_hoje
      nome_arquivo_anterior = "Dashboard Cobranca Jun"+ano_hoje
  elif mes_hoje == 8:
      nome_arquivo = "Dashboard Cobranca Ago"+ano_hoje
      nome_arquivo_anterior = "Dashboard Cobranca Jul"+ano_hoje
  elif mes_hoje == 9:
      nome_arquivo = "Dashboard Cobranca Set"+ano_hoje + "p"
      nome_arquivo_anterior ="Dashboard Cobranca Ago"+ano_hoje
      nome_arquivo_alternativo =  "Dashboard Cobranca Set"+ano_hoje
  elif mes_hoje == 10:
      nome_arquivo = "Dashboard Cobranca Out"+ano_hoje + "p"
      nome_arquivo_anterior = "Dashboard Cobranca Set"+ano_hoje
      nome_arquivo_alternativo =  "Dashboard Cobranca Out" +ano_hoje
  elif mes_hoje == 11:
      nome_arquivo = "Dashboard Cobranca Nov"+ano_hoje + "p"
      nome_arquivo_anterior = "Dashboard Cobranca Out"+ano_hoje
      nome_arquivo_alternativo =  "Dashboard Cobranca Nov" +ano_hoje
  elif mes_hoje == 12:
      nome_arquivo = "Dashboard Cobranca Dez"+ano_hoje + "p"
      nome_arquivo_anterior = "Dashboard Cobranca Nov"+ano_hoje
      nome_arquivo_alternativo =  "Dashboard Cobranca Dez" +ano_hoje

  arquivo_dashboard = r'\\BRNEP242\Publico\DDT\PR\SCL\CCO\COGC\Equipe\CRRC\2. Plano de Recuperação de Créditos\\{}.xlsb'.format(nome_arquivo)

  try:
      df_metas = pd.read_excel(arquivo_dashboard,sheet_name = aba_metas)
      df_orcamento = pd.read_excel(arquivo_dashboard,sheet_name = aba_orcamento)
  except Exception as e:
      print(e)
      try:
          arquivo_dashboard = r'\\BRNEP242\Publico\DDT\PR\SCL\CCO\COGC\Equipe\CRRC\2. Plano de Recuperação de Créditos\\{}.xlsb'.format(nome_arquivo_alternativo)
          df_metas = pd.read_excel(arquivo_dashboard,sheet_name = aba_metas)
          df_orcamento = pd.read_excel(arquivo_dashboard,sheet_name = aba_orcamento)
      except Exception as e:
          print(e)
          try: 
              arquivo_dashboard = r'\\BRNEP242\Publico\DDT\PR\SCL\CCO\COGC\Equipe\CRRC\2. Plano de Recuperação de Créditos\\{}.xlsb'.format(nome_arquivo_anterior)
              df_metas = pd.read_excel(arquivo_dashboard,sheet_name = aba_metas)
              df_orcamento = pd.read_excel(arquivo_dashboard,sheet_name = aba_orcamento)
              filtro_mes_ref_orcamento = filtro_mes_ref_orcamento_2
          except Exception as e:
              print(e)
          
  df_metas = df_metas[['MESREF','SETOR','UTD','TURMA','ATIVIDADE','QTD']]
  df_metas = pd.DataFrame(df_metas.groupby(['MESREF','SETOR','UTD','TURMA','ATIVIDADE'])['QTD'].sum()).reset_index()

  df_metas.rename(columns = {'ATIVIDADE' : 'CARTEIRA','QTD':'QTD_META'}, inplace = True)
  df_metas['QTD_META'] = df_metas['QTD_META'].fillna(0)
  df_metas['QTD_META'] = df_metas['QTD_META'].astype(int)
  df_metas = df_metas[((df_metas['MESREF'] == filtro_mes_ref))]
  df_metas.loc[(df_metas.TURMA == "PRÓPRIA"), "TURMA"] = "STC"
  st.session_state.df_metas = df_metas[['UTD','TURMA','CARTEIRA','QTD_META']]


  df_orcamento = df_orcamento[['MÊS','SETOR','UTD','PLANEJADO','REALIZADO']]
  df_orcamento = df_orcamento[((df_orcamento['MÊS'] <= filtro_mes_ref_orcamento))]
  df_orcamento = pd.DataFrame(df_orcamento.groupby(['SETOR','UTD'])['PLANEJADO','REALIZADO'].sum()).reset_index()
  df_orcamento['PERCENT'] = df_orcamento['REALIZADO']/df_orcamento['PLANEJADO']
  df_orcamento['PERCENT'] = df_orcamento['PERCENT'].fillna(0.0)
  df_orcamento['PERCENT'] = df_orcamento['PERCENT'].astype(float)
  #df_orcamento['PERCENT'] = df_orcamento['PERCENT'].apply(lambda x: float("{:.2f}".format(x)))
  df_orcamento['TURMA'] = 'EPS'
  st.session_state.df_orcamento = df_orcamento[['UTD','TURMA','PERCENT']]

  return st.session_state.df_metas,st.session_state.df_orcamento

def get_quadro_geral_utd():
    get_metas_orcamento_cobranca()

    txt_sql_consulta_defasagem_hoje_UTD = 'Consulta_defasagem_hoje_UTD'
    consulta = ['sources/Sqls/'+ txt_sql_consulta_defasagem_hoje_UTD + '.sql',st.session_state.data_selecao_hoje]
    arquivo_sql_consulta_defasagem_hoje_UTD = open(consulta[0], encoding="utf-8")
    sql_consulta_defasagem_hoje_UTD = arquivo_sql_consulta_defasagem_hoje_UTD.read()
    arquivo_sql_consulta_defasagem_hoje_UTD.close()
    sql_consulta_defasagem_hoje_UTD = sql_consulta_defasagem_hoje_UTD.format(data_consulta = consulta[1])
    connection_hana = dbapi.connect(address='BRNEO695',port='30015',user=st.session_state.usuario,password=st.session_state.senha,databasename='BNP',sslValidateCertificate=False)
    df_defasagem_hoje_UTD = pd.read_sql(sql_consulta_defasagem_hoje_UTD, connection_hana)

    txt_sql_consulta_defasagem_hoje_mapa_UTD = 'Consulta_defasagem_hoje_mapa_UTD'
    consulta = ['sources/Sqls/'+ txt_sql_consulta_defasagem_hoje_mapa_UTD + '.sql', st.session_state.data_selecao_hoje]
    arquivo_sql_consulta_defasagem_hoje_mapa_UTD = open(consulta[0], encoding="utf-8")
    sql_consulta_defasagem_hoje_mapa_UTD = arquivo_sql_consulta_defasagem_hoje_mapa_UTD.read()
    arquivo_sql_consulta_defasagem_hoje_mapa_UTD.close()
    sql_consulta_defasagem_hoje_mapa_UTD = sql_consulta_defasagem_hoje_mapa_UTD.format(data_consulta = consulta[1])
    df_defasagem_hoje_mapa_UTD = pd.read_sql(sql_consulta_defasagem_hoje_mapa_UTD, connection_hana)

    txt_sql_consulta_defasagem_hoje_suscetiveis_UTD = 'Consulta_defasagem_hoje_suscetiveis_UTD'
    consulta = ['sources/Sqls/'+ txt_sql_consulta_defasagem_hoje_suscetiveis_UTD + '.sql']
    arquivo_sql_consulta_defasagem_hoje_suscetiveis_UTD = open(consulta[0], encoding="utf-8")
    sql_consulta_defasagem_hoje_suscetiveis_UTD = arquivo_sql_consulta_defasagem_hoje_suscetiveis_UTD.read()
    arquivo_sql_consulta_defasagem_hoje_suscetiveis_UTD.close()
    df_defasagem_hoje_suscetiveis_UTD = pd.read_sql(sql_consulta_defasagem_hoje_suscetiveis_UTD, connection_hana)

    txt_sql_consulta_geradas_mes_UTD = 'Consulta_geradas_mes_UTD'
    consulta = ['sources/Sqls/'+ txt_sql_consulta_geradas_mes_UTD + '.sql']
    arquivo_sql_consulta_geradas_mes_UTD = open(consulta[0], encoding="utf-8")
    sql_consulta_geradas_mes_UTD = arquivo_sql_consulta_geradas_mes_UTD.read()
    arquivo_sql_consulta_geradas_mes_UTD.close()
    df_geradas_mes_UTD = pd.read_sql(sql_consulta_geradas_mes_UTD, connection_hana)
    df_geradas_mes_UTD.loc[( (df_geradas_mes_UTD.TURMA == "PRONTIDAO") ), "TURMA"] = "PRONTIDÃO"

    txt_sql_consulta_executadas_mes_UTD = 'Consulta_executadas_mes_UTD'
    consulta = ['sources/Sqls/'+ txt_sql_consulta_executadas_mes_UTD + '.sql']
    arquivo_sql_consulta_executadas_mes_UTD = open(consulta[0], encoding="utf-8")
    sql_consulta_executadas_mes_UTD = arquivo_sql_consulta_executadas_mes_UTD.read()
    arquivo_sql_consulta_executadas_mes_UTD.close()
    df_executadas_mes_UTD = pd.read_sql(sql_consulta_executadas_mes_UTD, connection_hana)
    df_executadas_mes_UTD.loc[( (df_executadas_mes_UTD.TURMA == "PRONTIDAO") ), "TURMA"] = "PRONTIDÃO"

    txt_sql_consulta_pendentes_UTD = 'Consulta_pendentes_hoje_UTD'
    consulta = ['sources/Sqls/'+ txt_sql_consulta_pendentes_UTD + '.sql']
    arquivo_sql_consulta_pendentes_UTD = open(consulta[0], encoding="utf-8")
    sql_consulta_pendentes_UTD = arquivo_sql_consulta_pendentes_UTD.read()
    arquivo_sql_consulta_pendentes_UTD.close()
    df_pendentes_UTD = pd.read_sql(sql_consulta_pendentes_UTD, connection_hana)
    df_pendentes_UTD.loc[( (df_pendentes_UTD.TURMA == "PRONTIDAO") ), "TURMA"] = "PRONTIDÃO"

    txt_sql_consulta_anuladas_canceladas_UTD = 'Consulta_anuladas_canceladas_UTD'
    consulta = ['sources/Sqls/'+ txt_sql_consulta_anuladas_canceladas_UTD + '.sql']
    arquivo_sql_consulta_anuladas_canceladas_UTD = open(consulta[0], encoding="utf-8")
    sql_consulta_anuladas_canceladas_UTD = arquivo_sql_consulta_anuladas_canceladas_UTD.read()
    arquivo_sql_consulta_anuladas_canceladas_UTD.close()
    df_anuladas_canceladas_UTD = pd.read_sql(sql_consulta_anuladas_canceladas_UTD, connection_hana)
    df_anuladas_canceladas_UTD.loc[( (df_anuladas_canceladas_UTD.TURMA == "PRONTIDAO") ), "TURMA"] = "PRONTIDÃO"

    utd_configuracao = pd.read_csv('sources/utd_configuracao.csv',sep=';',encoding = "ISO-8859-1")
    utd_configuracao = utd_configuracao[['UTD','CONFIG']]

    base_final = pd.merge(st.session_state.df_metas, st.session_state.df_orcamento, how = 'outer', on=['UTD','TURMA'])
    base_final = pd.merge(base_final, df_defasagem_hoje_UTD, how = 'outer', on=['UTD','TURMA','CARTEIRA'])
    base_final = pd.merge(base_final, df_defasagem_hoje_mapa_UTD, how = 'outer', on=['UTD','TURMA','CARTEIRA'])
    base_final = pd.merge(base_final, df_defasagem_hoje_suscetiveis_UTD, how = 'outer', on=['UTD','CARTEIRA'])
    base_final = pd.merge(base_final, df_geradas_mes_UTD, how = 'outer', on=['UTD','TURMA','CARTEIRA'])
    base_final = pd.merge(base_final, df_executadas_mes_UTD, how = 'outer', on=['UTD','TURMA','CARTEIRA'])
    base_final = pd.merge(base_final, df_pendentes_UTD, how = 'outer', on=['UTD','TURMA','CARTEIRA'])
    base_final = pd.merge(base_final, df_anuladas_canceladas_UTD, how = 'outer', on=['UTD','TURMA','CARTEIRA'])
    base_final = pd.merge(base_final, utd_configuracao, how = 'left', on=['UTD'])
    
    base_final['QTD_META_TOTAL_MENOS_PENDENTE'] = base_final['QTD_META'] -  base_final['QTD_EXECUTADAS']- base_final['QTD_PENDENTES']
    base_final['QTD_META'] = base_final['QTD_META']*st.session_state.percentual_meta_mes
    base_final['QTD_META'] = base_final['QTD_META'].fillna(0.0)
    base_final['QTD_META'] = base_final['QTD_META'].astype(int)
    base_final['QTD_META_PARCIAL_MENOS_PENDENTE'] = base_final['QTD_META'] -  base_final['QTD_EXECUTADAS'] - base_final['QTD_PENDENTES']
    base_final[['QTD_META_TOTAL_MENOS_PENDENTE','QTD_META_PARCIAL_MENOS_PENDENTE']] = base_final[['QTD_META_TOTAL_MENOS_PENDENTE','QTD_META_PARCIAL_MENOS_PENDENTE']].fillna(0.0)
    base_final[['QTD_META_TOTAL_MENOS_PENDENTE','QTD_META_PARCIAL_MENOS_PENDENTE']] = base_final[['QTD_META_TOTAL_MENOS_PENDENTE','QTD_META_PARCIAL_MENOS_PENDENTE']].astype(int)
    base_final[['QTD_GERADAS','QTD_ANULADAS','QTD_EXECUTADAS','QTD_PENDENTES','TOTAL_ESPERADO_MAPA','NOTAS_ESPERADAS_ATENA','QTD_CLUSTER','QTD_SUSCETIVEIS','TICKET_PECLD']] = base_final[['QTD_GERADAS','QTD_ANULADAS','QTD_EXECUTADAS','QTD_PENDENTES','TOTAL_ESPERADO_MAPA','NOTAS_ESPERADAS_ATENA','QTD_CLUSTER','QTD_SUSCETIVEIS','TICKET_PECLD']].fillna(0.0)
    base_final[['QTD_GERADAS','QTD_ANULADAS','QTD_EXECUTADAS','QTD_PENDENTES','TOTAL_ESPERADO_MAPA','NOTAS_ESPERADAS_ATENA','QTD_CLUSTER','QTD_SUSCETIVEIS','TICKET_PECLD']] = base_final[['QTD_GERADAS','QTD_ANULADAS','QTD_EXECUTADAS','QTD_PENDENTES','TOTAL_ESPERADO_MAPA','NOTAS_ESPERADAS_ATENA','QTD_CLUSTER','QTD_SUSCETIVEIS','TICKET_PECLD']].astype(int)
    base_final['DEFASAGEM_MAPA'] = base_final['TOTAL_ESPERADO_MAPA'] - base_final['NOTAS_ESPERADAS_ATENA']

    base_final['DEFASAGEM_MAPA'] = base_final['DEFASAGEM_MAPA'].fillna(0.0)
    base_final['DEFASAGEM_MAPA'] = base_final['DEFASAGEM_MAPA'].astype(int)
    
    base_final['PERCENT_META'] = base_final['QTD_EXECUTADAS']/base_final['QTD_META']
    base_final['PERCENT_META'] = base_final['PERCENT_META'].fillna(0.0)

    base_final['PERCENT_GERA'] = base_final['QTD_GERADAS']/base_final['QTD_META']
    base_final['PERCENT_GERA'] = base_final['PERCENT_GERA'].fillna(0.0)

    base_final['PERCENT_ANULADAS'] = base_final['QTD_ANULADAS']/base_final['QTD_GERADAS']
    base_final['PERCENT_ANULADAS'] = base_final['PERCENT_ANULADAS'].fillna(0.0)

    base_final['PERCENT'] = base_final['PERCENT'].fillna(0.0)
    base_final['PERCENT'] = base_final['PERCENT'].astype(float)
    base_final['PERCENT'] = base_final['PERCENT'].apply(lambda x: float("{:.2f}".format(x)))
    base_final['UTD'] = base_final['UTD'].fillna("-")
    base_final.loc[( (base_final.CARTEIRA == "BAIXA") &(base_final.TURMA == "STC") ), "ACAO"] = "APAGAR"
    base_final.loc[( (base_final.CARTEIRA == "DISJUNTOR") &(base_final.TURMA == "EPS") ), "ACAO"] = "APAGAR"
    base_final.loc[( (base_final.CARTEIRA == "RELIGAÇÃO") ), "ACAO"] = "APAGAR"
    base_final.loc[( (base_final.CARTEIRA == "REMOTO") ), "ACAO"] = "APAGAR"
    base_final.loc[( (base_final.CARTEIRA == "CORTE") &(base_final.TURMA == "PRONTIDÃO")), "ACAO"] = "APAGAR"
    base_final = base_final[((base_final['ACAO'] != "APAGAR"))]
    base_final['ACAO'] = base_final['ACAO'].fillna("-")
    base_final['TURMA'] = base_final['TURMA'].fillna("-")
    base_final['CONFIG'] = base_final['CONFIG'].fillna("-")
    st.session_state.base_final_UTD = base_final.sort_values(['DEFASAGEM_MAPA'],ascending=[False])
    st.session_state.base_final_UTD  = st.session_state.base_final_UTD[['UTD','CARTEIRA','PERCENT','PERCENT_GERA','PERCENT_META','QTD_META','QTD_GERADAS','QTD_EXECUTADAS','QTD_PENDENTES','TOTAL_ESPERADO_MAPA','NOTAS_ESPERADAS_ATENA','QTD_CLUSTER','QTD_SUSCETIVEIS','TICKET_PECLD','DEFASAGEM_MAPA','TURMA','CONFIG','QTD_ANULADAS','PERCENT_ANULADAS','QTD_META_TOTAL_MENOS_PENDENTE','QTD_META_PARCIAL_MENOS_PENDENTE']]
    
def get_quadro_geral_zonas_d_mais_1():
    get_metas_orcamento_cobranca()

    txt_sql_consulta_defasagem_hoje_UTD = 'Consulta_defasagem_hoje_ZONAS'
    consulta = ['sources/Sqls/'+ txt_sql_consulta_defasagem_hoje_UTD + '.sql',st.session_state.data_selecao_hoje]
    arquivo_sql_consulta_defasagem_hoje_UTD = open(consulta[0], encoding="utf-8")
    sql_consulta_defasagem_hoje_UTD = arquivo_sql_consulta_defasagem_hoje_UTD.read()
    arquivo_sql_consulta_defasagem_hoje_UTD.close()
    sql_consulta_defasagem_hoje_UTD = sql_consulta_defasagem_hoje_UTD.format(data_consulta = consulta[1])
    connection_hana = dbapi.connect(address='BRNEO695',port='30015',user=st.session_state.usuario,password=st.session_state.senha,databasename='BNP',sslValidateCertificate=False)
    df_defasagem_hoje_UTD = pd.read_sql(sql_consulta_defasagem_hoje_UTD, connection_hana)
    df_defasagem_hoje_UTD['ZONA'] = df_defasagem_hoje_UTD['ZONA'].fillna(0.0)
    df_defasagem_hoje_UTD['ZONA']  = df_defasagem_hoje_UTD['ZONA'].astype(int)
    df_defasagem_hoje_UTD['ZONA'] = df_defasagem_hoje_UTD['ZONA'].astype(str).str.pad(4,'left','0')

    txt_sql_consulta_defasagem_hoje_mapa_UTD = 'Consulta_defasagem_hoje_mapa_ZONAS'
    consulta = ['sources/Sqls/'+ txt_sql_consulta_defasagem_hoje_mapa_UTD + '.sql', st.session_state.data_selecao_hoje]
    arquivo_sql_consulta_defasagem_hoje_mapa_UTD = open(consulta[0], encoding="utf-8")
    sql_consulta_defasagem_hoje_mapa_UTD = arquivo_sql_consulta_defasagem_hoje_mapa_UTD.read()
    arquivo_sql_consulta_defasagem_hoje_mapa_UTD.close()
    sql_consulta_defasagem_hoje_mapa_UTD = sql_consulta_defasagem_hoje_mapa_UTD.format(data_consulta = consulta[1])
    df_defasagem_hoje_mapa_UTD = pd.read_sql(sql_consulta_defasagem_hoje_mapa_UTD, connection_hana)
    df_defasagem_hoje_mapa_UTD['ZONA'] = df_defasagem_hoje_mapa_UTD['ZONA'].fillna(0.0)
    df_defasagem_hoje_mapa_UTD['ZONA']  = df_defasagem_hoje_mapa_UTD['ZONA'].astype(int)
    df_defasagem_hoje_mapa_UTD['ZONA'] = df_defasagem_hoje_mapa_UTD['ZONA'].astype(str).str.pad(4,'left','0')

    txt_sql_consulta_defasagem_hoje_suscetiveis_UTD = 'Consulta_defasagem_hoje_suscetiveis_ZONAS'
    consulta = ['sources/Sqls/'+ txt_sql_consulta_defasagem_hoje_suscetiveis_UTD + '.sql']
    arquivo_sql_consulta_defasagem_hoje_suscetiveis_UTD = open(consulta[0], encoding="utf-8")
    sql_consulta_defasagem_hoje_suscetiveis_UTD = arquivo_sql_consulta_defasagem_hoje_suscetiveis_UTD.read()
    arquivo_sql_consulta_defasagem_hoje_suscetiveis_UTD.close()
    df_defasagem_hoje_suscetiveis_UTD = pd.read_sql(sql_consulta_defasagem_hoje_suscetiveis_UTD, connection_hana)
    df_defasagem_hoje_suscetiveis_UTD['ZONA'] = df_defasagem_hoje_suscetiveis_UTD['ZONA'].fillna(0.0)
    df_defasagem_hoje_suscetiveis_UTD['ZONA']  = df_defasagem_hoje_suscetiveis_UTD['ZONA'].astype(int)
    df_defasagem_hoje_suscetiveis_UTD['ZONA'] = df_defasagem_hoje_suscetiveis_UTD['ZONA'].astype(str).str.pad(4,'left','0')

    txt_sql_consulta_geradas_mes_UTD = 'Consulta_geradas_mes_ZONAS'
    consulta = ['sources/Sqls/'+ txt_sql_consulta_geradas_mes_UTD + '.sql']
    arquivo_sql_consulta_geradas_mes_UTD = open(consulta[0], encoding="utf-8")
    sql_consulta_geradas_mes_UTD = arquivo_sql_consulta_geradas_mes_UTD.read()
    arquivo_sql_consulta_geradas_mes_UTD.close()
    df_geradas_mes_UTD = pd.read_sql(sql_consulta_geradas_mes_UTD, connection_hana)
    df_geradas_mes_UTD.loc[( (df_geradas_mes_UTD.TURMA == "PRONTIDAO") ), "TURMA"] = "PRONTIDÃO"
    df_geradas_mes_UTD['ZONA'] = df_geradas_mes_UTD['ZONA'].fillna(0.0)
    df_geradas_mes_UTD['ZONA']  = df_geradas_mes_UTD['ZONA'].astype(int)
    df_geradas_mes_UTD['ZONA'] = df_geradas_mes_UTD['ZONA'].astype(str).str.pad(4,'left','0')

    txt_sql_consulta_executadas_mes_UTD = 'Consulta_executadas_mes_ZONAS'
    consulta = ['sources/Sqls/'+ txt_sql_consulta_executadas_mes_UTD + '.sql']
    arquivo_sql_consulta_executadas_mes_UTD = open(consulta[0], encoding="utf-8")
    sql_consulta_executadas_mes_UTD = arquivo_sql_consulta_executadas_mes_UTD.read()
    arquivo_sql_consulta_executadas_mes_UTD.close()
    df_executadas_mes_UTD = pd.read_sql(sql_consulta_executadas_mes_UTD, connection_hana)
    df_executadas_mes_UTD.loc[( (df_executadas_mes_UTD.TURMA == "PRONTIDAO") ), "TURMA"] = "PRONTIDÃO"
    df_executadas_mes_UTD['ZONA'] = df_executadas_mes_UTD['ZONA'].fillna(0.0)
    df_executadas_mes_UTD['ZONA']  = df_executadas_mes_UTD['ZONA'].astype(int)
    df_executadas_mes_UTD['ZONA'] = df_executadas_mes_UTD['ZONA'].astype(str).str.pad(4,'left','0')

    txt_sql_consulta_pendentes_UTD = 'Consulta_pendentes_hoje_ZONAS'
    consulta = ['sources/Sqls/'+ txt_sql_consulta_pendentes_UTD + '.sql']
    arquivo_sql_consulta_pendentes_UTD = open(consulta[0], encoding="utf-8")
    sql_consulta_pendentes_UTD = arquivo_sql_consulta_pendentes_UTD.read()
    arquivo_sql_consulta_pendentes_UTD.close()
    df_pendentes_UTD = pd.read_sql(sql_consulta_pendentes_UTD, connection_hana)
    df_pendentes_UTD.loc[( (df_pendentes_UTD.TURMA == "PRONTIDAO") ), "TURMA"] = "PRONTIDÃO"
    df_pendentes_UTD['ZONA'] = df_pendentes_UTD['ZONA'].fillna(0.0)
    df_pendentes_UTD['ZONA']  = df_pendentes_UTD['ZONA'].astype(int)
    df_pendentes_UTD['ZONA'] = df_pendentes_UTD['ZONA'].astype(str).str.pad(4,'left','0')

    txt_sql_consulta_anuladas_canceladas_UTD = 'Consulta_anuladas_canceladas_ZONAS'
    consulta = ['sources/Sqls/'+ txt_sql_consulta_anuladas_canceladas_UTD + '.sql']
    arquivo_sql_consulta_anuladas_canceladas_UTD = open(consulta[0], encoding="utf-8")
    sql_consulta_anuladas_canceladas_UTD = arquivo_sql_consulta_anuladas_canceladas_UTD.read()
    arquivo_sql_consulta_anuladas_canceladas_UTD.close()
    df_anuladas_canceladas_UTD = pd.read_sql(sql_consulta_anuladas_canceladas_UTD, connection_hana)
    df_anuladas_canceladas_UTD.loc[( (df_anuladas_canceladas_UTD.TURMA == "PRONTIDAO") ), "TURMA"] = "PRONTIDÃO"
    df_anuladas_canceladas_UTD['ZONA'] = df_anuladas_canceladas_UTD['ZONA'].fillna(0.0)
    df_anuladas_canceladas_UTD['ZONA']  = df_anuladas_canceladas_UTD['ZONA'].astype(int)
    df_anuladas_canceladas_UTD['ZONA'] = df_anuladas_canceladas_UTD['ZONA'].astype(str).str.pad(4,'left','0')

    utd_configuracao = pd.read_csv('sources/utd_configuracao.csv',sep=';',encoding = "ISO-8859-1")
    utd_configuracao = utd_configuracao[['UTD','CONFIG']]
    
    base_final = pd.merge(df_geradas_mes_UTD, df_executadas_mes_UTD, how = 'outer', on=['UTD','TURMA','CARTEIRA','ZONA'])
    base_final = pd.merge(base_final, df_defasagem_hoje_UTD, how = 'outer', on=['UTD','TURMA','CARTEIRA','ZONA'])
    base_final = pd.merge(base_final, df_defasagem_hoje_mapa_UTD, how = 'outer', on=['UTD','TURMA','CARTEIRA','ZONA'])
    base_final = pd.merge(base_final, st.session_state.df_metas, how = 'outer', on=['UTD','TURMA','CARTEIRA'])
    base_final = pd.merge(base_final, st.session_state.df_orcamento, how = 'outer', on=['UTD','TURMA'])
    #base_final = pd.merge(base_final, df_defasagem_hoje_mapa_UTD, how = 'outer', on=['UTD','TURMA','CARTEIRA','ZONA'])
    base_final = pd.merge(base_final, df_defasagem_hoje_suscetiveis_UTD, how = 'outer', on=['UTD','CARTEIRA','ZONA'])
    base_final = pd.merge(base_final, df_pendentes_UTD, how = 'outer', on=['UTD','TURMA','CARTEIRA','ZONA'])
    base_final = pd.merge(base_final, df_anuladas_canceladas_UTD, how = 'outer', on=['UTD','TURMA','CARTEIRA','ZONA'])
    base_final = pd.merge(base_final, utd_configuracao, how = 'left', on=['UTD'])
    
    
    nomes_zonas = pd.read_csv('sources/nomes_zonas.csv',sep=';',encoding = "ISO-8859-1") #pegar nomes das zonas...
    nomes_zonas = nomes_zonas[['ZONA','BASE CLICK']]
    nomes_zonas['ZONA'] = nomes_zonas['ZONA'].astype(str).str.pad(4,'left','0')

    base_final = pd.merge(base_final, nomes_zonas, how = 'left', on=['ZONA'])
    base_final['ZONA'] = base_final['ZONA'].fillna(0.0)
    base_final['ZONA']  = base_final['ZONA'].astype(int)
    base_final['ZONA'] = base_final['ZONA'].astype(str).str.pad(4,'left','0')
    base_final.round(2)
    

    base_final['QTD_META'] = base_final['QTD_META']*st.session_state.percentual_meta_mes
    base_final['QTD_META'] = base_final['QTD_META'].fillna(0.0)
    base_final['QTD_META'] = base_final['QTD_META'].astype(int)

    base_final[['QTD_GERADAS','QTD_ANULADAS','QTD_EXECUTADAS','QTD_PENDENTES','TOTAL_ESPERADO_MAPA','NOTAS_ESPERADAS_ATENA','QTD_CLUSTER','QTD_SUSCETIVEIS','TICKET_PECLD']] = base_final[['QTD_GERADAS','QTD_ANULADAS','QTD_EXECUTADAS','QTD_PENDENTES','TOTAL_ESPERADO_MAPA','NOTAS_ESPERADAS_ATENA','QTD_CLUSTER','QTD_SUSCETIVEIS','TICKET_PECLD']].fillna(0.0)
    base_final[['QTD_GERADAS','QTD_ANULADAS','QTD_EXECUTADAS','QTD_PENDENTES','TOTAL_ESPERADO_MAPA','NOTAS_ESPERADAS_ATENA','QTD_CLUSTER','QTD_SUSCETIVEIS','TICKET_PECLD']] = base_final[['QTD_GERADAS','QTD_ANULADAS','QTD_EXECUTADAS','QTD_PENDENTES','TOTAL_ESPERADO_MAPA','NOTAS_ESPERADAS_ATENA','QTD_CLUSTER','QTD_SUSCETIVEIS','TICKET_PECLD']].astype(int)
    base_final['DEFASAGEM_MAPA'] = base_final['TOTAL_ESPERADO_MAPA'] - base_final['NOTAS_ESPERADAS_ATENA']

    base_final['DEFASAGEM_MAPA'] = base_final['DEFASAGEM_MAPA'].fillna(0.0)
    base_final['DEFASAGEM_MAPA'] = base_final['DEFASAGEM_MAPA'].astype(int)
    
    base_final['PERCENT_META'] = base_final['QTD_EXECUTADAS']/base_final['QTD_META']
    base_final['PERCENT_META'] = base_final['PERCENT_META'].fillna(0.0)

    base_final['PERCENT_GERA'] = base_final['QTD_GERADAS']/base_final['QTD_META']
    base_final['PERCENT_GERA'] = base_final['PERCENT_GERA'].fillna(0.0)

    base_final['PERCENT_ANULADAS'] = base_final['QTD_ANULADAS']/base_final['QTD_GERADAS']
    base_final['PERCENT_ANULADAS'] = base_final['PERCENT_ANULADAS'].fillna(0.0)

    base_final['PERCENT'] = base_final['PERCENT'].fillna(0.0)
    base_final['PERCENT'] = base_final['PERCENT'].astype(float)
    base_final['PERCENT'] = base_final['PERCENT'].apply(lambda x: float("{:.2f}".format(x)))
    base_final['UTD'] = base_final['UTD'].fillna("-")
    base_final.loc[( (base_final.CARTEIRA == "BAIXA") &(base_final.TURMA == "STC") ), "ACAO"] = "APAGAR"
    base_final.loc[( (base_final.CARTEIRA == "DISJUNTOR") &(base_final.TURMA == "EPS") ), "ACAO"] = "APAGAR"
    base_final.loc[( (base_final.CARTEIRA == "RELIGAÇÃO") ), "ACAO"] = "APAGAR"
    base_final.loc[( (base_final.CARTEIRA == "REMOTO") ), "ACAO"] = "APAGAR"
    base_final.loc[( (base_final.CARTEIRA == "CORTE") &(base_final.TURMA == "PRONTIDÃO")), "ACAO"] = "APAGAR"
    base_final = base_final[((base_final['ACAO'] != "APAGAR"))]
    base_final['ACAO'] = base_final['ACAO'].fillna("-")
    base_final['TURMA'] = base_final['TURMA'].fillna("-")
    base_final['CONFIG'] = base_final['CONFIG'].fillna("-")
    
    st.session_state.base_final_ZONAS = base_final.sort_values(['DEFASAGEM_MAPA'],ascending=[False])
    st.session_state.base_final_ZONAS  = st.session_state.base_final_ZONAS[['UTD','ZONA','BASE CLICK','CARTEIRA','PERCENT','PERCENT_GERA','PERCENT_META','QTD_META','QTD_GERADAS','QTD_EXECUTADAS','QTD_PENDENTES','TOTAL_ESPERADO_MAPA','NOTAS_ESPERADAS_ATENA','QTD_CLUSTER','QTD_SUSCETIVEIS','TICKET_PECLD','DEFASAGEM_MAPA','TURMA','CONFIG','QTD_ANULADAS','PERCENT_ANULADAS']]



def formatar_lista_entrada_sql_3():
    tempo_inicial = time.time()
    lista = st.session_state.lista_entrada.split(' ')
    if st.session_state.opcao_formatacao_sql  == "Conta Contrato":
        st.markdown("<h5 style='text-align: left; color: #5C881A;'>LISTA CONTA CONTRATO FORMATADA:</h5>", unsafe_allow_html=True)
        for i in range(len(lista)):
            lista[i] = "'" + str(lista[i]).zfill(12) + "'"
        ultima_linha = lista[-1][0:14]
    elif st.session_state.opcao_formatacao_sql == "Instalação":
        st.markdown("<h5 style='text-align: left; color: #5C881A;'>LISTA INSTALAÇÃO FORMATADA:</h5>", unsafe_allow_html=True)
        for i in range(len(lista)):
            lista[i] = "'" + str(lista[i]).zfill(10) + "'"
    lista = list(filter(("'0000000000',").__ne__, lista))
    lista = list(filter(("'000000000000',").__ne__, lista))

    string_lista = ','.join([str(item) for item in lista])
    #st.session_state.lista_saida = string_lista
    st.text(string_lista)
    

def formatar_lista_entrada_sql():
    lista = st.session_state.lista_entrada.split(' ')
    for i in range(len(lista)):
        lista[i] = "'" + str(lista[i]).zfill(12) + "'"
    lista = list(filter(("'0000000000',").__ne__, lista))
    lista = list(filter(("'000000000000',").__ne__, lista))
    string_lista = ','.join([str(item) for item in lista])
    st.session_state.lista_saida = string_lista
    


def formatar_lista_entrada_sql2():
    tempo_inicial = time.time()
    lista = st.session_state.lista_entrada.split(' ')
    for i in range(len(lista)):
        lista[i] = str(lista[i]).zfill(12)
    lista = list(filter(("0000000000").__ne__, lista))
    lista = list(filter(("000000000000").__ne__, lista))
    string_lista = ','.join([str(item) for item in lista])
    st.session_state.lista_saida = string_lista
    tempo_final = time.time() ; duracao = tempo_final - tempo_inicial; st.session_state.total_contratos_consultados = len(lista)



def consulta_geral_sql_casa():
    txt_sql_consulta_geral = 'ConsultaPR'
    consulta = ['sources/Sqls/'+ txt_sql_consulta_geral + '.sql', st.session_state.lista_saida]
    arquivo_sql_consulta_geral = open(consulta[0], encoding="utf-8")
    sql_consulta_geral = arquivo_sql_consulta_geral.read()
    arquivo_sql_consulta_geral.close()
    sql_consulta_geral = sql_consulta_geral.format(lista_consultar = consulta[1])
    st.caption(sql_consulta_geral)


    

def tabela_resumo_pr():
    tabela_resumo_pr = """
                            
    <table style="border:1.1px solid #C3E98A; text-align: center;font-size:12px; font-style:bold" >
  <tr  style="border:1.1px solid #C3E98A"  >
    <th colspan="4" style="background-color:#5C881A;  color:#FFFFFF"; "border:1.1px solid #C3E98A">RESUMO GERAL</th>
  </tr>
  <tr style="border:1.1px solid #C3E98A">
    <th style="background-color:#5C881A;  color:#FFFFFF"; "border:1.1px solid #C3E98A">STATUS</th>
    <th style="background-color:#5C881A;  color:#FFFFFF"; "border:1.1px solid #C3E98A">QUANTIDADE</th>
    <th style="background-color:#5C881A;  color:#FFFFFF"; "border:1.1px solid #C3E98A">% TOTAL</th>
    <th style="background-color:#5C881A;  color:#FFFFFF"; "border:1.1px solid #C3E98A">AÇÃO/RESPONSÁVEL</th>
  </tr>
  <tr style="border:1.1px solid #C3E98A">
    <td style="border:1.1px solid #C3E98A"> Baixado </td>
    <td style="border:1.1px solid #C3E98A" > {0} </td>
    <td style="border:1.1px solid #C3E98A" > {13}% </td>
    <td style="border:1.1px solid #C3E98A"> - </td>
  </tr>
  <tr style="border:1.1px solid #C3E98A">
    <td style="border:1.1px solid #C3E98A"> Gerar Baixa ADM</td>
    <td style="border:1.1px solid #C3E98A">{1}</td>
    <td style="border:1.1px solid #C3E98A">{14}%</td>
    <td style="border:1.1px solid #C3E98A"> Cobrança </td>
  </tr>
   <tr style="border:1.1px solid #C3E98A">
    <td style="border:1.1px solid #C3E98A"> Complementar Baixa ADM</td>
    <td style="border:1.1px solid #C3E98A">{2}</td>
    <td style="border:1.1px solid #C3E98A">{15}%</td>
    <td style="border:1.1px solid #C3E98A"> Cobrança </td>
  </tr>
  <tr style="border:1.1px solid #C3E98A">
    <td style="border:1.1px solid #C3E98A"> Notas Pendentes Tratamento</td>
    <td style="border:1.1px solid #C3E98A">{27}</td>
    <td style="border:1.1px solid #C3E98A">{28}%</td>
    <td style="border:1.1px solid #C3E98A"> Cobrança </td>
  </tr>
  <tr style="border:1.1px solid #C3E98A">
    <td style="border:1.1px solid #C3E98A">Não Baixar</td>
    <td style="border:1.1px solid #C3E98A">{3}</td>
    <td style="border:1.1px solid #C3E98A">{16}%</td>
    <td style="border:1.1px solid #C3E98A">Corporativo</td>
  </tr>
  <tr style="border:1.1px solid #C3E98A">
    <td style="border:1.1px solid #C3E98A">Nota de Leitura divergente de B100, D100 e D110</td>
    <td style="border:1.1px solid #C3E98A">{4}</td>
    <td style="border:1.1px solid #C3E98A">{17}%</td>
    <td style="border:1.1px solid #C3E98A">Parecer da Leitura</td>
  </tr>
  <tr style="border:1.1px solid #C3E98A">
    <td style="border:1.1px solid #C3E98A">Existe FRA</td>
    <td style="border:1.1px solid #C3E98A">{5}</td>
    <td style="border:1.1px solid #C3E98A">{18}%</td>
    <td style="border:1.1px solid #C3E98A">Parecer de Perdas</td>
  </tr>
  <tr style="border:1.1px solid #C3E98A">
    <td style="border:1.1px solid #C3E98A">Nota CI Pendente</td>
    <td style="border:1.1px solid #C3E98A">{6}</td>
    <td style="border:1.1px solid #C3E98A">{19}%</td>
    <td style="border:1.1px solid #C3E98A">Parecer de Perdas</td>
  </tr>
  <tr style="border:1.1px solid #C3E98A">
    <td style="border:1.1px solid #C3E98A">Nota Comercial Pendente</td>
    <td style="border:1.1px solid #C3E98A">{7}</td>
    <td style="border:1.1px solid #C3E98A">{20}%</td>
    <td style="border:1.1px solid #C3E98A">UTD/Gestão Operacional</td>
  </tr>
  <tr style="border:1.1px solid #C3E98A">
    <td style="border:1.1px solid #C3E98A">Arrecadação 3 meses</td>
    <td style="border:1.1px solid #C3E98A">{8}</td>
    <td style="border:1.1px solid #C3E98A">{21}%</td>
    <td style="border:1.1px solid #C3E98A">Parecer Leitura</td>
  </tr>
  <tr style="border:1.1px solid #C3E98A">
    <td style="border:1.1px solid #C3E98A">Consumo médio (12 meses) superior a 300kWh</td>
    <td style="border:1.1px solid #C3E98A">{9}</td>
    <td style="border:1.1px solid #C3E98A">{22}%</td>
    <td style="border:1.1px solid #C3E98A">Avaliar</td>
  </tr>
  <tr style="border:1.1px solid #C3E98A">
    <td style="border:1.1px solid #C3E98A">Consumo médio (6 meses) anterior ao primeiro B100 superior a 300kWh</td>
    <td style="border:1.1px solid #C3E98A">{25}</td>
    <td style="border:1.1px solid #C3E98A">{26}%</td>
    <td style="border:1.1px solid #C3E98A">Avaliar</td>
  </tr>
  <tr style="border:1.1px solid #C3E98A">
    <td style="border:1.1px solid #C3E98A">Sem Repetibilidade</td>
    <td style="border:1.1px solid #C3E98A">{10}</td>
    <td style="border:1.1px solid #C3E98A">{23}%</td>
    <td style="border:1.1px solid #C3E98A">Avaliar</td>
  </tr>
  <tr style="border:1.1px solid #C3E98A">
    <td style="border:1.1px solid #C3E98A">Unidade Ligada (Gerar Corte)</td>
    <td style="border:1.1px solid #C3E98A">{11}</td>
    <td style="border:1.1px solid #C3E98A">{24}%</td>
    <td style="border:1.1px solid #C3E98A">Cobrança</td>
  </tr>
  
  <tr style="border:1.1px solid #C3E98A">
    <td style="border:1.1px solid #C3E98A">Total</td>
    <td style="border:1.1px solid #C3E98A">{12}</td>
    <td style="border:1.1px solid #C3E98A">100%</td>
    <td style="border:1.1px solid #C3E98A">-</td>
  </tr>
</table>
"""
    tabela_resumo_pr = tabela_resumo_pr.format(
    st.session_state.qtd_baixados, #0
    st.session_state.qtd_gerar_baixa, #1
    st.session_state.qtd_complementar, #2
    st.session_state.qtd_nao_baixar, #3
    st.session_state.qtd_nota_leitura_divergente, #4
    st.session_state.qtd_existe_fra, #5
    st.session_state.qtd_nota_ci_pendente,  #6
    st.session_state.qtd_nota_comercial_pendente, #7
    st.session_state.qtd_arrecad_3_meses, #8
    st.session_state.qtd_consumo_superior, #9
    st.session_state.qtd_sem_repetibilidade, #10
    st.session_state.qtd_gerar_corte, #11
    st.session_state.qtd_total, #12
    st.session_state.perc1, 
    st.session_state.perc2, 
    st.session_state.perc3, 
    st.session_state.perc4, 
    st.session_state.perc5, 
    st.session_state.perc6, 
    st.session_state.perc7, 
    st.session_state.perc8, 
    st.session_state.perc9, 
    st.session_state.perc10, 
    st.session_state.perc11, 
    st.session_state.perc12,
    st.session_state.qtd_consumo_6_meses,
    st.session_state.perc13,
    st.session_state.qtd_pendente_tratamento,
    st.session_state.perc14)
    return tabela_resumo_pr


def consulta_geral_sql_pr():
    txt_sql_consulta_geral = 'ConsultaPR_total'
    consulta = ['sources/Sqls/'+ txt_sql_consulta_geral + '.sql']
    arquivo_sql_consulta_geral = open(consulta[0], encoding="utf-8")
    sql_consulta_geral = arquivo_sql_consulta_geral.read()
    arquivo_sql_consulta_geral.close()
    st.write(sql_consulta_geral)
    connection_hana = dbapi.connect(address='BRNEO695',port='30015',user=st.session_state.usuario,password=st.session_state.senha,databasename='BNP',sslValidateCertificate=False)
    st.session_state.df_consulta_pr = pd.read_sql(sql_consulta_geral, connection_hana)
  
    st.session_state.qtd_total = len(st.session_state.df_consulta_pr.index)
    st.session_state.df_consulta_pr.loc[(((st.session_state.df_consulta_pr.ACAO == "Unidade Ligada (Gerar Corte)") | (st.session_state.df_consulta_pr.ACAO == "Nota Pendente Tratamento")) & (st.session_state.df_consulta_pr.REPETIBILIDADE_B100_D100_D110 < 5)), "ACAO"] = "Sem repetibilidade"
    st.session_state.df_consulta_pr.loc[(((st.session_state.df_consulta_pr.ACAO == "Gerar Baixa ADM") | (st.session_state.df_consulta_pr.ACAO == "Nota Pendente Tratamento") | (st.session_state.df_consulta_pr.ACAO == "Complementar Baixa ADM")) & (st.session_state.df_consulta_pr.REPETIBILIDADE_B100_D100_D110 < 3)), "ACAO"] = "Sem repetibilidade"

    st.session_state.df_consulta_pr.loc[(((st.session_state.df_consulta_pr.ACAO == "Unidade Ligada (Gerar Corte)") | (st.session_state.df_consulta_pr.ACAO == "Nota Pendente Tratamento") | (st.session_state.df_consulta_pr.ACAO == "Complementar Baixa ADM") | (st.session_state.df_consulta_pr.ACAO == "Gerar Baixa ADM")) & (st.session_state.df_consulta_pr.MEDIA_CONSUMO_6_MESES_PRE > 270)), "ACAO"] = "Consumo médio (6 meses) anterior ao primeiro B100 superior a 300kWh"
    #st.session_state.df_consulta_pr.loc[((st.session_state.df_consulta_pr.LEIT_MES_0 == "0000") & (st.session_state.df_consulta_pr.LEIT_MES_1 == "0000")) & ((st.session_state.df_consulta_pr.ACAO == "Unidade Ligada (Gerar Corte)") | (st.session_state.df_consulta_pr.ACAO == "Complementar Baixa ADM") | (st.session_state.df_consulta_pr.ACAO == "Gerar Baixa ADM") ), "ACAO"] = "Sem repetibilidade"
    #st.session_state.df_consulta_pr.loc[((st.session_state.df_consulta_pr.LEIT_MES_1 == "0000") & (st.session_state.df_consulta_pr.LEIT_MES_2 == "0000") )  & ((st.session_state.df_consulta_pr.ACAO == "Unidade Ligada (Gerar Corte)") | (st.session_state.df_consulta_pr.ACAO == "Complementar Baixa ADM") | (st.session_state.df_consulta_pr.ACAO == "Gerar Baixa ADM") ), "ACAO"] = "Sem repetibilidade"
    #st.session_state.df_consulta_pr.loc[((((st.session_state.df_consulta_pr.LEIT_MES_2 == "0000") & (st.session_state.df_consulta_pr.LEIT_MES_3 == "0000") ) )) & ((st.session_state.df_consulta_pr.ACAO == "Unidade Ligada (Gerar Corte)") | (st.session_state.df_consulta_pr.ACAO == "Complementar Baixa ADM") | (st.session_state.df_consulta_pr.ACAO == "Gerar Baixa ADM") ), "ACAO"] = "Sem repetibilidade"
    #st.session_state.df_consulta_pr.loc[((((st.session_state.df_consulta_pr.LEIT_MES_3 == "0000") & (st.session_state.df_consulta_pr.LEIT_MES_4 == "0000") ) )) & ((st.session_state.df_consulta_pr.ACAO == "Unidade Ligada (Gerar Corte)") | (st.session_state.df_consulta_pr.ACAO == "Complementar Baixa ADM") | (st.session_state.df_consulta_pr.ACAO == "Gerar Baixa ADM") ), "ACAO"] = "Sem repetibilidade"
    #st.session_state.df_consulta_pr.loc[((((st.session_state.df_consulta_pr.LEIT_MES_4 == "0000") & (st.session_state.df_consulta_pr.LEIT_MES_5 == "0000") ) )) & ((st.session_state.df_consulta_pr.ACAO == "Unidade Ligada (Gerar Corte)") | (st.session_state.df_consulta_pr.ACAO == "Complementar Baixa ADM") | (st.session_state.df_consulta_pr.ACAO == "Gerar Baixa ADM") ), "ACAO"] = "Sem repetibilidade"
    
    st.session_state.df_consulta_pr = st.session_state.df_consulta_pr.sort_values(['MEDIA_CONSUMO_12_MESES'],ascending=[False])
    st.session_state.df_consulta_pr = st.session_state.df_consulta_pr.reset_index(drop=True)
    
    
    

    df_temp = st.session_state.df_consulta_pr[(st.session_state.df_consulta_pr['ACAO'] == "Baixado")].copy()
    df_temp = df_temp.reset_index(drop=True)
    st.session_state.qtd_baixados = len(df_temp.index)
    df_temp = st.session_state.df_consulta_pr[(st.session_state.df_consulta_pr['ACAO'] == "Gerar Baixa ADM")].copy()
    df_temp = df_temp.reset_index(drop=True)
    st.session_state.qtd_gerar_baixa = len(df_temp.index)
    df_temp = st.session_state.df_consulta_pr[(st.session_state.df_consulta_pr['ACAO'] == "Não Baixar")].copy()
    df_temp = df_temp.reset_index(drop=True)
    st.session_state.qtd_nao_baixar = len(df_temp.index)
    df_temp = st.session_state.df_consulta_pr[(st.session_state.df_consulta_pr['ACAO'] == "Nota de Leitura divergente de B100, D100 e D110")].copy()
    df_temp = df_temp.reset_index(drop=True)
    st.session_state.qtd_nota_leitura_divergente = len(df_temp.index)
    df_temp = st.session_state.df_consulta_pr[(st.session_state.df_consulta_pr['ACAO'] == "Existe FRA")].copy()
    df_temp = df_temp.reset_index(drop=True)
    st.session_state.qtd_existe_fra = len(df_temp.index)
    df_temp = st.session_state.df_consulta_pr[(st.session_state.df_consulta_pr['ACAO'] == "Nota CI Pendente")].copy()
    df_temp = df_temp.reset_index(drop=True)
    st.session_state.qtd_nota_ci_pendente = len(df_temp.index)
    df_temp = st.session_state.df_consulta_pr[(st.session_state.df_consulta_pr['ACAO'] == "Nota Comercial Pendente")].copy()
    df_temp = df_temp.reset_index(drop=True)
    st.session_state.qtd_nota_comercial_pendente = len(df_temp.index)
    df_temp = st.session_state.df_consulta_pr[(st.session_state.df_consulta_pr['ACAO'] == "Arrecadação 3 meses")].copy()
    df_temp = df_temp.reset_index(drop=True)
    st.session_state.qtd_arrecad_3_meses = len(df_temp.index)
    df_temp = st.session_state.df_consulta_pr[(st.session_state.df_consulta_pr['ACAO'] == "Consumo superior a 300kWh")].copy()
    df_temp = df_temp.reset_index(drop=True)
    st.session_state.qtd_consumo_superior = len(df_temp.index)
    df_temp = st.session_state.df_consulta_pr[(st.session_state.df_consulta_pr['ACAO'] == "Sem repetibilidade")].copy()
    df_temp = df_temp.reset_index(drop=True)
    st.session_state.qtd_sem_repetibilidade = len(df_temp.index)
    df_temp = st.session_state.df_consulta_pr[(st.session_state.df_consulta_pr['ACAO'] == "Unidade Ligada (Gerar Corte)")].copy()
    df_temp = df_temp.reset_index(drop=True)
    st.session_state.qtd_gerar_corte = len(df_temp.index)
    df_temp = st.session_state.df_consulta_pr[(st.session_state.df_consulta_pr['ACAO'] == "Complementar Baixa ADM")].copy()
    df_temp = df_temp.reset_index(drop=True)
    st.session_state.qtd_complementar = len(df_temp.index)

    df_temp = st.session_state.df_consulta_pr[(st.session_state.df_consulta_pr['ACAO'] == "Consumo médio (6 meses) anterior ao primeiro B100 superior a 300kWh")].copy()
    df_temp = df_temp.reset_index(drop=True)
    st.session_state.qtd_consumo_6_meses = len(df_temp.index)
    df_temp = st.session_state.df_consulta_pr[(st.session_state.df_consulta_pr['ACAO'] == "Nota Pendente Tratamento")].copy()
    df_temp = df_temp.reset_index(drop=True)
    st.session_state.qtd_pendente_tratamento = len(df_temp.index)

    
    
    st.session_state.perc1 = round((st.session_state.qtd_baixados/st.session_state.qtd_total)*100,2)
    st.session_state.perc2 = round((st.session_state.qtd_gerar_baixa/st.session_state.qtd_total)*100,2)
    st.session_state.perc3 = round((st.session_state.qtd_complementar/st.session_state.qtd_total)*100,2)
    st.session_state.perc4 = round((st.session_state.qtd_nao_baixar/st.session_state.qtd_total)*100,2)
    st.session_state.perc5 = round((st.session_state.qtd_nota_leitura_divergente/st.session_state.qtd_total)*100,2)
    st.session_state.perc6 = round((st.session_state.qtd_existe_fra/st.session_state.qtd_total)*100,2)
    st.session_state.perc7 = round((st.session_state.qtd_nota_ci_pendente/st.session_state.qtd_total)*100,2)
    st.session_state.perc8 = round((st.session_state.qtd_nota_comercial_pendente/st.session_state.qtd_total)*100,2)
    st.session_state.perc9 = round((st.session_state.qtd_arrecad_3_meses/st.session_state.qtd_total)*100,2)
    st.session_state.perc10 = round((st.session_state.qtd_consumo_superior/st.session_state.qtd_total)*100,2)
    st.session_state.perc11 = round((st.session_state.qtd_sem_repetibilidade/st.session_state.qtd_total)*100,2)
    st.session_state.perc12 = round( (st.session_state.qtd_gerar_corte/st.session_state.qtd_total)*100,2)
    st.session_state.perc13 = round( (st.session_state.qtd_consumo_6_meses/st.session_state.qtd_total)*100,2)
    st.session_state.perc14 = round( (st.session_state.qtd_pendente_tratamento/st.session_state.qtd_total)*100,2)

    df_consulta_pr_temp2 = st.session_state.df_consulta_pr[(st.session_state.df_consulta_pr['MEDIA_CONSUMO_12_MESES'] > 0)].copy()
    st.session_state.lista_opcoes = list(df_consulta_pr_temp2.ACAO.unique())

def graficos_pr():
    st.session_state.df_consulta_pr_temp = st.session_state.df_consulta_pr[(st.session_state.df_consulta_pr['ACAO'] == st.session_state.categoria) & (st.session_state.df_consulta_pr['MEDIA_CONSUMO_12_MESES'] > 0) & (st.session_state.df_consulta_pr['MEDIA_CONSUMO_12_MESES'] != 'nan')].copy()
    
    st.session_state.df_consulta_pr_temp = st.session_state.df_consulta_pr_temp.reset_index(drop=True)
    st.session_state.df_consulta_pr_temp_temp = st.session_state.df_consulta_pr_temp[(st.session_state.df_consulta_pr_temp['ZCGACCOUN'] == st.session_state.df_consulta_pr_temp['ZCGACCOUN'].iloc[st.session_state.rank_consumo])].copy()
    
    st.session_state.consumo_medio = st.session_state.df_consulta_pr_temp_temp['MEDIA_CONSUMO_12_MESES'].iloc[0]
    st.session_state.pecld = st.session_state.df_consulta_pr_temp_temp['PECLD_ATUAL'].iloc[0]
    st.session_state.mont_cr = st.session_state.df_consulta_pr_temp_temp['MONT_CR'].iloc[0]
    st.session_state.repetibilidade = st.session_state.df_consulta_pr_temp_temp['REPETIBILIDADE_B100_D100_D110'].iloc[0]
    st.session_state.status_sistema = st.session_state.df_consulta_pr_temp_temp['SIT_CC'].iloc[0]

    st.session_state.conta = st.session_state.df_consulta_pr_temp_temp['ZCGACCOUN'].iloc[0]
    st.session_state.cat = st.session_state.df_consulta_pr_temp_temp['ACAO'].iloc[0]



    st.session_state.leit_0 = st.session_state.df_consulta_pr_temp_temp['LEIT_MES_0'].iloc[0]
    st.session_state.leit_1 = st.session_state.df_consulta_pr_temp_temp['LEIT_MES_1'].iloc[0]
    st.session_state.leit_2 = st.session_state.df_consulta_pr_temp_temp['LEIT_MES_2'].iloc[0]
    st.session_state.leit_3 = st.session_state.df_consulta_pr_temp_temp['LEIT_MES_3'].iloc[0]
    st.session_state.leit_4 = st.session_state.df_consulta_pr_temp_temp['LEIT_MES_4'].iloc[0]
    st.session_state.leit_5 = st.session_state.df_consulta_pr_temp_temp['LEIT_MES_5'].iloc[0]
    st.session_state.leit_6 = st.session_state.df_consulta_pr_temp_temp['LEIT_MES_6'].iloc[0]
    st.session_state.leit_7 = st.session_state.df_consulta_pr_temp_temp['LEIT_MES_7'].iloc[0]
    st.session_state.leit_8 = st.session_state.df_consulta_pr_temp_temp['LEIT_MES_8'].iloc[0]
    st.session_state.leit_9 = st.session_state.df_consulta_pr_temp_temp['LEIT_MES_9'].iloc[0]
    st.session_state.leit_10 = st.session_state.df_consulta_pr_temp_temp['LEIT_MES_10'].iloc[0]
    st.session_state.leit_11 = st.session_state.df_consulta_pr_temp_temp['LEIT_MES_11'].iloc[0]
    st.session_state.leit_12 = st.session_state.df_consulta_pr_temp_temp['LEIT_MES_12'].iloc[0]

    st.session_state.con_0 = st.session_state.df_consulta_pr_temp_temp['CON_MES_0'].iloc[0]
    st.session_state.con_1 = st.session_state.df_consulta_pr_temp_temp['CON_MES_1'].iloc[0]
    st.session_state.con_2 = st.session_state.df_consulta_pr_temp_temp['CON_MES_2'].iloc[0]
    st.session_state.con_3 = st.session_state.df_consulta_pr_temp_temp['CON_MES_3'].iloc[0]
    st.session_state.con_4 = st.session_state.df_consulta_pr_temp_temp['CON_MES_4'].iloc[0]
    st.session_state.con_5 = st.session_state.df_consulta_pr_temp_temp['CON_MES_5'].iloc[0]
    st.session_state.con_6 = st.session_state.df_consulta_pr_temp_temp['CON_MES_6'].iloc[0]
    st.session_state.con_7 = st.session_state.df_consulta_pr_temp_temp['CON_MES_7'].iloc[0]
    st.session_state.con_8 = st.session_state.df_consulta_pr_temp_temp['CON_MES_8'].iloc[0]
    st.session_state.con_9 = st.session_state.df_consulta_pr_temp_temp['CON_MES_9'].iloc[0]
    st.session_state.con_10 = st.session_state.df_consulta_pr_temp_temp['CON_MES_10'].iloc[0]
    st.session_state.con_11 = st.session_state.df_consulta_pr_temp_temp['CON_MES_11'].iloc[0]
    st.session_state.con_12 = st.session_state.df_consulta_pr_temp_temp['CON_MES_12'].iloc[0]

    st.session_state.con_6_meses_0 = st.session_state.df_consulta_pr_temp_temp['CON_PRE_MES_0'].iloc[0]
    st.session_state.con_6_meses_1 = st.session_state.df_consulta_pr_temp_temp['CON_PRE_MES_1'].iloc[0]
    st.session_state.con_6_meses_2 = st.session_state.df_consulta_pr_temp_temp['CON_PRE_MES_2'].iloc[0]
    st.session_state.con_6_meses_3 = st.session_state.df_consulta_pr_temp_temp['CON_PRE_MES_3'].iloc[0]
    st.session_state.con_6_meses_4 = st.session_state.df_consulta_pr_temp_temp['CON_PRE_MES_4'].iloc[0]
    st.session_state.con_6_meses_5 = st.session_state.df_consulta_pr_temp_temp['CON_PRE_MES_5'].iloc[0]
    
    st.session_state.con_6_meses_media = round(st.session_state.df_consulta_pr_temp_temp['MEDIA_CONSUMO_6_MESES_PRE'].iloc[0],0)



    x_freq_leit = pd.DataFrame({'leituras':[st.session_state.df_consulta_pr_temp_temp['LEIT_MES_0'].iloc[0] , st.session_state.df_consulta_pr_temp_temp['LEIT_MES_1'].iloc[0] , st.session_state.df_consulta_pr_temp_temp['LEIT_MES_2'].iloc[0] , st.session_state.df_consulta_pr_temp_temp['LEIT_MES_3'].iloc[0] , st.session_state.df_consulta_pr_temp_temp['LEIT_MES_4'].iloc[0] , st.session_state.df_consulta_pr_temp_temp['LEIT_MES_5'].iloc[0] , st.session_state.df_consulta_pr_temp_temp['LEIT_MES_6'].iloc[0] , st.session_state.df_consulta_pr_temp_temp['LEIT_MES_7'].iloc[0] , st.session_state.df_consulta_pr_temp_temp['LEIT_MES_8'].iloc[0] , st.session_state.df_consulta_pr_temp_temp['LEIT_MES_9'].iloc[0] , st.session_state.df_consulta_pr_temp_temp['LEIT_MES_10'].iloc[0] , st.session_state.df_consulta_pr_temp_temp['LEIT_MES_11'].iloc[0] , st.session_state.df_consulta_pr_temp_temp['LEIT_MES_12'].iloc[0]]})
    st.session_state.freq_leitura_pr = x_freq_leit.value_counts()
    
    #st.table(st.session_state.freq_leitura_pr)
    
    lista_consumo = ['CON_MES_0','CON_MES_1','CON_MES_2','CON_MES_3','CON_MES_4','CON_MES_5','CON_MES_6','CON_MES_7','CON_MES_8','CON_MES_9','CON_MES_10','CON_MES_11','CON_MES_12']
    st.session_state.df_consulta_pr_temp_temp = st.session_state.df_consulta_pr_temp_temp[lista_consumo].copy()
    if 'ano_mes_0' not in st.session_state:
        today_date = datetime.today()
        month = today_date - relativedelta(months=1)
        Year = month.year
        st.session_state.ano_mes_0 = str(Year) + str(month.strftime('%m'))
        today_date = datetime.today()
        one_month_ago = today_date - relativedelta(months=2)
        Year = one_month_ago.year
        st.session_state.ano_mes_1 = str(Year) + str(one_month_ago.strftime('%m'))
        two_month_ago = today_date - relativedelta(months=3)
        Year = two_month_ago.year
        st.session_state.ano_mes_2 = str(Year) + str(two_month_ago.strftime('%m'))
        three_month_ago = today_date - relativedelta(months=4)
        Year = three_month_ago.year
        st.session_state.ano_mes_3 = str(Year) + str(three_month_ago.strftime('%m'))
        four_month_ago = today_date - relativedelta(months=5)
        Year = four_month_ago.year
        st.session_state.ano_mes_4 = str(Year) + str(four_month_ago.strftime('%m'))
        five_month_ago = today_date - relativedelta(months=6)
        Year = five_month_ago.year
        st.session_state.ano_mes_5 = str(Year) + str(five_month_ago.strftime('%m'))
        six_month_ago = today_date - relativedelta(months=7)
        Year = six_month_ago.year
        st.session_state.ano_mes_6 = str(Year) + str(six_month_ago.strftime('%m'))
        seven_month_ago = today_date - relativedelta(months=8)
        Year = seven_month_ago.year
        st.session_state.ano_mes_7 = str(Year) + str(seven_month_ago.strftime('%m'))
        eight_month_ago = today_date - relativedelta(months=9)
        Year = eight_month_ago.year
        st.session_state.ano_mes_8 = str(Year) + str(eight_month_ago.strftime('%m'))
        nine_month_ago = today_date - relativedelta(months=10)
        Year = nine_month_ago.year
        st.session_state.ano_mes_9 = str(Year) + str(nine_month_ago.strftime('%m'))
        ten_month_ago = today_date - relativedelta(months=11)
        Year = ten_month_ago.year
        st.session_state.ano_mes_10 = str(Year) + str(ten_month_ago.strftime('%m'))
        eleven_month_ago = today_date - relativedelta(months=12)
        Year = eleven_month_ago.year
        st.session_state.ano_mes_11 = str(Year) + str(eleven_month_ago.strftime('%m'))
        twelve_month_ago = today_date - relativedelta(months=13)
        Year = twelve_month_ago.year
        st.session_state.ano_mes_12 = str(Year) + str(twelve_month_ago.strftime('%m'))

    st.session_state.df_consulta_pr_temp_temp = st.session_state.df_consulta_pr_temp_temp.rename(columns={'CON_MES_0':'{}'.format(st.session_state.ano_mes_0),'CON_MES_1':'{}'.format(st.session_state.ano_mes_1),'CON_MES_2':'{}'.format(st.session_state.ano_mes_2),'CON_MES_3':'{}'.format(st.session_state.ano_mes_3),'CON_MES_4':'{}'.format(st.session_state.ano_mes_4),'CON_MES_5':'{}'.format(st.session_state.ano_mes_5),'CON_MES_6':'{}'.format(st.session_state.ano_mes_6),'CON_MES_7':'{}'.format(st.session_state.ano_mes_7),'CON_MES_8':'{}'.format(st.session_state.ano_mes_8),'CON_MES_9':'{}'.format(st.session_state.ano_mes_9),'CON_MES_10':'{}'.format(st.session_state.ano_mes_10),'CON_MES_11':'{}'.format(st.session_state.ano_mes_11),'CON_MES_12':'{}'.format(st.session_state.ano_mes_12)})
    st.session_state.df_consulta_pr_temp_temp = st.session_state.df_consulta_pr_temp_temp.T
    
    



def graficos_pr_chart():
  
  graficos_pr()
  #st.table(st.session_state.df_consulta_pr_temp_temp.iloc[:,0].index)
  #st.table(st.session_state.df_consulta_pr_temp_temp.iloc[:,0].values)
  source = pd.DataFrame({
      #'x': ["a","b","b","b","b","b","b","b","b","b","b","b"],
      'x' :st.session_state.df_consulta_pr_temp_temp.iloc[:,0].index,
      'y': st.session_state.df_consulta_pr_temp_temp.iloc[:,0].values
      
    })

  st.altair_chart(alt.Chart(source, 
                  title='CONSUMO (kWh) MENSAL (12 meses)').mark_line(
    point=alt.OverlayMarkDef(color="#5C881A")
    ).encode(
  alt.X('x',title='Meses'),
  alt.Y('y',title='Consumo (kWh)'),
  color=alt.value("#5C881A")
  ).properties(width=500))

  

def graficos_pr_chart_2():
    
    
    base = alt.Chart(st.session_state.df_consulta_pr_temp_temp, 
                  title='ROC Curve of KNN'
                  ).properties(width=300)

    roc_curve = base.mark_line(point=True).encode(
      alt.X(st.session_state.df_consulta_pr_temp_temp.iloc[:,0].index, title='False Positive Rate (FPR)'),
      alt.Y(st.session_state.df_consulta_pr_temp_temp.iloc[:,0].values, title='True Positive Rate (TPR) (a.k.a Recall)'),
    )

    st.altair_chart(roc_curve)











def tabela_repetibilidade_pr():
    

    tabela_repetibilidade = """
                            
    <table style="border:1.1px solid #C3E98A; text-align: center;font-size:12px; font-style:bold" >
  <tr  style="border:1.1px solid #C3E98A"  >
    <th colspan="14" style="background-color:#5C881A;  color:#FFFFFF"; "border:1.1px solid #C3E98A">REPETIBILIDADE B100, D100 e D110</th>
  </tr>
  <tr style="border:1.1px solid #C3E98A">
    <th style="background-color:#5C881A;  color:#FFFFFF"; "border:1.1px solid #C3E98A">CATEGORIA</th>
    <th style="background-color:#5C881A;  color:#FFFFFF"; "border:1.1px solid #C3E98A">{12}</th>
    <th style="background-color:#5C881A;  color:#FFFFFF"; "border:1.1px solid #C3E98A">{11}</th>
    <th style="background-color:#5C881A;  color:#FFFFFF"; "border:1.1px solid #C3E98A">{10}</th>
    <th style="background-color:#5C881A;  color:#FFFFFF"; "border:1.1px solid #C3E98A">{9}</th>
    <th style="background-color:#5C881A;  color:#FFFFFF"; "border:1.1px solid #C3E98A">{8}</th>
    <th style="background-color:#5C881A;  color:#FFFFFF"; "border:1.1px solid #C3E98A">{7}</th>
    <th style="background-color:#5C881A;  color:#FFFFFF"; "border:1.1px solid #C3E98A">{6}</th>
    <th style="background-color:#5C881A;  color:#FFFFFF"; "border:1.1px solid #C3E98A">{5}</th>
    <th style="background-color:#5C881A;  color:#FFFFFF"; "border:1.1px solid #C3E98A">{4}</th>
    <th style="background-color:#5C881A;  color:#FFFFFF"; "border:1.1px solid #C3E98A">{3}</th>
    <th style="background-color:#5C881A;  color:#FFFFFF"; "border:1.1px solid #C3E98A">{2}</th>
    <th style="background-color:#5C881A;  color:#FFFFFF"; "border:1.1px solid #C3E98A">{1}</th>
    <th style="background-color:#5C881A;  color:#FFFFFF"; "border:1.1px solid #C3E98A">{0}</th>
  </tr>
  <tr style="border:1.1px solid #C3E98A">
    <td style="border:1.1px solid #C3E98A"> Nota Leitura</td>
    <td style="border:1.1px solid #C3E98A">{25}</td>
    <td style="border:1.1px solid #C3E98A">{24}</td>
    <td style="border:1.1px solid #C3E98A">{23}</td>
    <td style="border:1.1px solid #C3E98A">{22}</td>
    <td style="border:1.1px solid #C3E98A">{21}</td>
    <td style="border:1.1px solid #C3E98A">{20}</td>
    <td style="border:1.1px solid #C3E98A">{19}</td>
    <td style="border:1.1px solid #C3E98A">{18}</td>
    <td style="border:1.1px solid #C3E98A">{17}</td>
    <td style="border:1.1px solid #C3E98A">{16}</td>
    <td style="border:1.1px solid #C3E98A">{15}</td>
    <td style="border:1.1px solid #C3E98A">{14}</td>
    <td style="border:1.1px solid #C3E98A">{13}</td>
  </tr>
  <tr style="border:1.1px solid #C3E98A">
    <td style="border:1.1px solid #C3E98A"> Consumo (kWh)</td>
    <td style="border:1.1px solid #C3E98A">{38}</td>
    <td style="border:1.1px solid #C3E98A">{37}</td>
    <td style="border:1.1px solid #C3E98A">{36}</td>
    <td style="border:1.1px solid #C3E98A">{35}</td>
    <td style="border:1.1px solid #C3E98A">{34}</td>
    <td style="border:1.1px solid #C3E98A">{33}</td>
    <td style="border:1.1px solid #C3E98A">{32}</td>
    <td style="border:1.1px solid #C3E98A">{31}</td>
    <td style="border:1.1px solid #C3E98A">{30}</td>
    <td style="border:1.1px solid #C3E98A">{29}</td>
    <td style="border:1.1px solid #C3E98A">{28}</td>
    <td style="border:1.1px solid #C3E98A">{27}</td>
    <td style="border:1.1px solid #C3E98A">{26}</td>
  </tr>
  
</table>
"""
    tabela_repetibilidade = tabela_repetibilidade.format(st.session_state.ano_mes_0,st.session_state.ano_mes_1,st.session_state.ano_mes_2,st.session_state.ano_mes_3,st.session_state.ano_mes_4,st.session_state.ano_mes_5,st.session_state.ano_mes_6,st.session_state.ano_mes_7,st.session_state.ano_mes_8,st.session_state.ano_mes_9,st.session_state.ano_mes_10,st.session_state.ano_mes_11,st.session_state.ano_mes_12,st.session_state.leit_0,st.session_state.leit_1,st.session_state.leit_2,st.session_state.leit_3,st.session_state.leit_4,st.session_state.leit_5,st.session_state.leit_6,st.session_state.leit_7,st.session_state.leit_8,st.session_state.leit_9,st.session_state.leit_10,st.session_state.leit_11,st.session_state.leit_12,st.session_state.con_0,st.session_state.con_1,st.session_state.con_2,st.session_state.con_3,st.session_state.con_4,st.session_state.con_5,st.session_state.con_6,st.session_state.con_7,st.session_state.con_8,st.session_state.con_9,st.session_state.con_10,st.session_state.con_11,st.session_state.con_12)
    return tabela_repetibilidade




def tabela_consumo_6_meses():
    
    

    tabela_consumo_6_meses = """
                            
    <table style="border:1.1px solid #C3E98A; text-align: center;font-size:12px; font-style:bold" >
  <tr  style="border:1.1px solid #C3E98A"  >
    <th colspan="2" style="background-color:#5C881A;  color:#FFFFFF"; "border:1.1px solid #C3E98A">MÉDIA CONSUMO 6 MESES ANTERIORES A PRIMEIRA OCLE</th>
  </tr>
  <tr style="border:1.1px solid #C3E98A">
    <th style="background-color:#5C881A;  color:#FFFFFF"; "border:1.1px solid #C3E98A">MÊS</th>
    <th style="background-color:#5C881A;  color:#FFFFFF"; "border:1.1px solid #C3E98A">CONSUMO (kWh)</th>
  </tr>
  <tr style="border:1.1px solid #C3E98A">
    <td style="border:1.1px solid #C3E98A"> MÊS 0</td>
    <td style="border:1.1px solid #C3E98A">{0}</td>
  </tr>
  <tr style="border:1.1px solid #C3E98A">
    <td style="border:1.1px solid #C3E98A"> MÊS 1</td>
    <td style="border:1.1px solid #C3E98A">{1}</td>
  </tr>
  <tr style="border:1.1px solid #C3E98A">
    <td style="border:1.1px solid #C3E98A"> MÊS 2</td>
    <td style="border:1.1px solid #C3E98A">{2}</td>
  </tr>
    <tr style="border:1.1px solid #C3E98A">
    <td style="border:1.1px solid #C3E98A"> MÊS 3</td>
    <td style="border:1.1px solid #C3E98A">{3}</td>
  </tr>
  </tr>
    <tr style="border:1.1px solid #C3E98A">
    <td style="border:1.1px solid #C3E98A"> MÊS 4</td>
    <td style="border:1.1px solid #C3E98A">{4}</td>
  </tr>
  </tr>
    <tr style="border:1.1px solid #C3E98A">
    <td style="border:1.1px solid #C3E98A"> MÊS 5</td>
    <td style="border:1.1px solid #C3E98A">{5}</td>
  </tr>
  </tr>
    <tr style="border:1.1px solid #C3E98A">
    <td style="border:1.1px solid #C3E98A"> MÉDIA</td>
    <td style="border:1.1px solid #C3E98A">{6}</td>
  </tr>


  

</table>
"""
    tabela_consumo_6_meses = tabela_consumo_6_meses.format(st.session_state.con_6_meses_0,st.session_state.con_6_meses_1,st.session_state.con_6_meses_2,st.session_state.con_6_meses_3,st.session_state.con_6_meses_4,st.session_state.con_6_meses_5,st.session_state.con_6_meses_media)
    return tabela_consumo_6_meses
  
def consulta_defasagem_hoje():
    get_metas_orcamento_cobranca()
    if str.lower(st.session_state.pagina) == "defasagem por zonas" or str.lower(st.session_state.pagina) == "suscetiveis para mapa":
        txt_sql_consulta_defasagem_hoje = 'Consulta_defasagem_hoje'
        consulta = ['sources/Sqls/'+ txt_sql_consulta_defasagem_hoje + '.sql', st.session_state.data_pedido]
    else:
        st.session_state.mudanca_pagina = 1
        txt_sql_consulta_defasagem_hoje = 'Consulta_defasagem_hoje_D0_UTD'
        consulta = ['sources/Sqls/'+ txt_sql_consulta_defasagem_hoje + '.sql',st.session_state.data_pedido]
    arquivo_sql_consulta_defasagem_hoje = open(consulta[0], encoding="utf-8")
    sql_consulta_defasagem_hoje = arquivo_sql_consulta_defasagem_hoje.read()
    arquivo_sql_consulta_defasagem_hoje.close()
    sql_consulta_defasagem_hoje = sql_consulta_defasagem_hoje.format(data_consulta = consulta[1])
    connection_hana = dbapi.connect(address='BRNEO695',port='30015',user=st.session_state.usuario,password=st.session_state.senha,databasename='BNP',sslValidateCertificate=False)
    df_defasagem_hoje = pd.read_sql(sql_consulta_defasagem_hoje, connection_hana)
    if str.lower(st.session_state.pagina) == "defasagem por zonas" or str.lower(st.session_state.pagina) == "suscetiveis para mapa":
        df_defasagem_hoje['ZONA'] = df_defasagem_hoje['ZONA'].fillna(0.0)
        df_defasagem_hoje['ZONA']  = df_defasagem_hoje['ZONA'].astype(int)
        df_defasagem_hoje['ZONA'] = df_defasagem_hoje['ZONA'].astype(str).str.pad(4,'left','0')

    #st.write(df_defasagem_hoje)

    if str.lower(st.session_state.pagina) == "defasagem por zonas" or str.lower(st.session_state.pagina) == "suscetiveis para mapa":
        txt_sql_consulta_defasagem_hoje = 'Consulta_inserido_atena_defasagem_hoje'
        consulta = ['sources/Sqls/'+ txt_sql_consulta_defasagem_hoje + '.sql',st.session_state.data_hoje]
    else:
        st.session_state.mudanca_pagina = 1
        txt_sql_consulta_defasagem_hoje = 'Consulta_inserido_atena_defasagem_hoje_UTD'
        consulta = ['sources/Sqls/'+ txt_sql_consulta_defasagem_hoje + '.sql',st.session_state.data_hoje]
    arquivo_sql_consulta_defasagem_hoje = open(consulta[0], encoding="utf-8")
    sql_consulta_defasagem_hoje = arquivo_sql_consulta_defasagem_hoje.read()
    arquivo_sql_consulta_defasagem_hoje.close()
    sql_consulta_defasagem_hoje = sql_consulta_defasagem_hoje.format(data_consulta = consulta[1])
    connection_hana = dbapi.connect(address='BRNEO695',port='30015',user=st.session_state.usuario,password=st.session_state.senha,databasename='BNP',sslValidateCertificate=False)
    df_inserido_hoje = pd.read_sql(sql_consulta_defasagem_hoje, connection_hana)
    if str.lower(st.session_state.pagina) == "defasagem por zonas" or str.lower(st.session_state.pagina) == "suscetiveis para mapa":
        df_inserido_hoje['ZONA'] = df_inserido_hoje['ZONA'].fillna(0.0)
        df_inserido_hoje['ZONA']  = df_inserido_hoje['ZONA'].astype(int)
        df_inserido_hoje['ZONA'] = df_inserido_hoje['ZONA'].astype(str).str.pad(4,'left','0')

    
    if str.lower(st.session_state.pagina) == "defasagem por zonas" or str.lower(st.session_state.pagina) == "suscetiveis para mapa":
        txt_sql_consulta_defasagem_hoje_mapa = 'Consulta_defasagem_hoje_mapa'
        consulta = ['sources/Sqls/'+ txt_sql_consulta_defasagem_hoje_mapa + '.sql', st.session_state.data_pedido_mapa] 
    else:
        txt_sql_consulta_defasagem_hoje_mapa = 'Consulta_defasagem_hoje_mapa_UTD'
        consulta = ['sources/Sqls/'+ txt_sql_consulta_defasagem_hoje_mapa + '.sql', st.session_state.data_pedido_mapa]
    arquivo_sql_consulta_defasagem_hoje_mapa = open(consulta[0], encoding="utf-8")
    sql_consulta_defasagem_hoje_mapa = arquivo_sql_consulta_defasagem_hoje_mapa.read()
    arquivo_sql_consulta_defasagem_hoje_mapa.close()
    sql_consulta_defasagem_hoje_mapa = sql_consulta_defasagem_hoje_mapa.format(data_consulta = consulta[1])
    df_defasagem_hoje_mapa = pd.read_sql(sql_consulta_defasagem_hoje_mapa, connection_hana)
    #st.write(df_defasagem_hoje_mapa)
    # COMENTAR ESSA LINHA 06-09-2022 DUAS ABAIXO
    #if str.lower(st.session_state.pagina) == "defasagem por zonas":
        #df_defasagem_hoje_mapa.drop('DATA_PEDIDO', axis=1, inplace=True)

    
    if str.lower(st.session_state.pagina) == "defasagem por zonas" or str.lower(st.session_state.pagina) == "suscetiveis para mapa":
        txt_sql_consulta_defasagem_hoje_suscetiveis = 'Consulta_defasagem_hoje_suscetiveis'
    else:
        txt_sql_consulta_defasagem_hoje_suscetiveis = 'Consulta_defasagem_hoje_suscetiveis_UTD'
    consulta = ['sources/Sqls/'+ txt_sql_consulta_defasagem_hoje_suscetiveis + '.sql']
    arquivo_sql_consulta_defasagem_hoje_suscetiveis = open(consulta[0], encoding="utf-8")
    sql_consulta_defasagem_hoje_suscetiveis = arquivo_sql_consulta_defasagem_hoje_suscetiveis.read()
    arquivo_sql_consulta_defasagem_hoje_suscetiveis.close()
    df_defasagem_hoje_suscetiveis = pd.read_sql(sql_consulta_defasagem_hoje_suscetiveis, connection_hana)

    if str.lower(st.session_state.pagina) == "defasagem por zonas" or str.lower(st.session_state.pagina) == "suscetiveis para mapa":
        txt_sql_consulta_geradas_mes = 'Consulta_geradas_mes'
    else:
        txt_sql_consulta_geradas_mes = 'Consulta_geradas_mes_UTD'
    consulta = ['sources/Sqls/'+ txt_sql_consulta_geradas_mes + '.sql']
    arquivo_sql_consulta_geradas_mes = open(consulta[0], encoding="utf-8")
    sql_consulta_geradas_mes = arquivo_sql_consulta_geradas_mes.read()
    arquivo_sql_consulta_geradas_mes.close()
    df_geradas_mes = pd.read_sql(sql_consulta_geradas_mes, connection_hana)
    if str.lower(st.session_state.pagina) == "defasagem por zonas":
        df_geradas_mes['ZONA'] = df_geradas_mes['ZONA'].fillna(0.0)
        df_geradas_mes['ZONA']  = df_geradas_mes['ZONA'].astype(int)
        df_geradas_mes['ZONA'] = df_geradas_mes['ZONA'].astype(str).str.pad(4,'left','0')

    if str.lower(st.session_state.pagina) == "defasagem por zonas" or str.lower(st.session_state.pagina) == "suscetiveis para mapa":
        txt_sql_consulta_executadas_mes = 'Consulta_executadas_mes'
    else:
        txt_sql_consulta_executadas_mes = 'Consulta_executadas_mes_UTD'
    consulta = ['sources/Sqls/'+ txt_sql_consulta_executadas_mes + '.sql']
    arquivo_sql_consulta_executadas_mes = open(consulta[0], encoding="utf-8")
    sql_consulta_executadas_mes = arquivo_sql_consulta_executadas_mes.read()
    arquivo_sql_consulta_executadas_mes.close()
    df_executadas_mes = pd.read_sql(sql_consulta_executadas_mes, connection_hana)
    if str.lower(st.session_state.pagina) == "defasagem por zonas" or str.lower(st.session_state.pagina) == "suscetiveis para mapa":
        df_executadas_mes['ZONA'] = df_executadas_mes['ZONA'].fillna(0.0)
        df_executadas_mes['ZONA']  = df_executadas_mes['ZONA'].astype(int)
        df_executadas_mes['ZONA'] = df_executadas_mes['ZONA'].astype(str).str.pad(4,'left','0')

    if str.lower(st.session_state.pagina) == "defasagem por zonas" or str.lower(st.session_state.pagina) == "suscetiveis para mapa":
        txt_sql_consulta_pendentes_UTD = 'Consulta_pendentes_hoje'
    else:
        txt_sql_consulta_pendentes_UTD = 'Consulta_pendentes_hoje_UTD'
    consulta = ['sources/Sqls/'+ txt_sql_consulta_pendentes_UTD + '.sql']
    arquivo_sql_consulta_pendentes_UTD = open(consulta[0], encoding="utf-8")
    sql_consulta_pendentes_UTD = arquivo_sql_consulta_pendentes_UTD.read()
    arquivo_sql_consulta_pendentes_UTD.close()
    df_pendentes_UTD = pd.read_sql(sql_consulta_pendentes_UTD, connection_hana)
    df_pendentes_UTD.loc[( (df_pendentes_UTD.TURMA == "PRONTIDAO") ), "TURMA"] = "PRONTIDÃO"
    if str.lower(st.session_state.pagina) == "defasagem por zonas":
        df_pendentes_UTD['ZONA'] = df_pendentes_UTD['ZONA'].fillna(0.0)
        df_pendentes_UTD['ZONA']  = df_pendentes_UTD['ZONA'].astype(int)
        df_pendentes_UTD['ZONA'] = df_pendentes_UTD['ZONA'].astype(str).str.pad(4,'left','0')

    if str.lower(st.session_state.pagina) == "defasagem por zonas" or str.lower(st.session_state.pagina) == "suscetiveis para mapa":
        txt_sql_consulta_anuladas_canceladas_UTD = 'Consulta_anuladas_canceladas_ZONAS'
    else:
        txt_sql_consulta_anuladas_canceladas_UTD = 'Consulta_anuladas_canceladas_UTD'
    consulta = ['sources/Sqls/'+ txt_sql_consulta_anuladas_canceladas_UTD + '.sql']
    arquivo_sql_consulta_anuladas_canceladas_UTD = open(consulta[0], encoding="utf-8")
    sql_consulta_anuladas_canceladas_UTD = arquivo_sql_consulta_anuladas_canceladas_UTD.read()
    arquivo_sql_consulta_anuladas_canceladas_UTD.close()
    df_anuladas_canceladas_UTD = pd.read_sql(sql_consulta_anuladas_canceladas_UTD, connection_hana)
    df_anuladas_canceladas_UTD.loc[( (df_anuladas_canceladas_UTD.TURMA == "PRONTIDAO") ), "TURMA"] = "PRONTIDÃO"
    if str.lower(st.session_state.pagina) == "defasagem por zonas" or str.lower(st.session_state.pagina) == "suscetiveis para mapa":
        df_anuladas_canceladas_UTD['ZONA'] = df_anuladas_canceladas_UTD['ZONA'].fillna(0.0)
        df_anuladas_canceladas_UTD['ZONA']  = df_anuladas_canceladas_UTD['ZONA'].astype(int)
        df_anuladas_canceladas_UTD['ZONA'] = df_anuladas_canceladas_UTD['ZONA'].astype(str).str.pad(4,'left','0')

    if str.lower(st.session_state.pagina) == "defasagem por zonas" or str.lower(st.session_state.pagina) == "suscetiveis para mapa":
        #coletar dados do pedido de defasagem da programação comercial
        nome_arquivo = "Defasagem 2022"
        arquivo_defasagem = r'C:\\Users\\{}\\OneDrive - IBERDROLA S.A\\GESTÃO DA DEMANDA - PROGRAMAÇÃO COMERCIAL\\{}.xlsx'.format(st.session_state.usuario_u,nome_arquivo)
        
        if dia_semana != 4: #sexta
            data_ped_programacao = date.today() + timedelta(1) 
        else:
            data_ped_programacao = date.today() + timedelta(3) 
        
        ano_ped_prog = str(data_ped_programacao.year)
        dia_ped_prog = str(data_ped_programacao.day)
        mes_ped_prog = str(data_ped_programacao.month)
        if len(dia_ped_prog) == 1:
            dia_ped_prog = '0' + dia_ped_prog
        if len(mes_ped_prog) == 1:
            mes_ped_prog = '0' + mes_ped_prog
        try:
            aba = dia_ped_prog +"." + mes_ped_prog
            df_pedido_defasagem = pd.read_excel(arquivo_defasagem,sheet_name = aba)
        except Exception as e:
            
            try: 
                aba = dia_ped_prog +"." + mes_ped_prog +" " 
                df_pedido_defasagem = pd.read_excel(arquivo_defasagem,sheet_name = aba)
            except Exception as e:
                try: 
                    aba = dia_ped_prog +"." + mes_ped_prog +"   " 
                    df_pedido_defasagem = pd.read_excel(arquivo_defasagem,sheet_name = aba)
                except Exception as e:
                    try:
                        aba = dia_ped_prog +"." + mes_ped_prog +"  " 
                        df_pedido_defasagem = pd.read_excel(arquivo_defasagem,sheet_name = aba)
                    except Exception as e:
                        try:
                            aba = dia_ped_prog +"." + mes_ped_prog +"     " 
                            df_pedido_defasagem = pd.read_excel(arquivo_defasagem,sheet_name = aba)
                        except Exception as e:
                            data = []
                            df_pedido_defasagem = pd.DataFrame(data)
                            df_pedido_defasagem['SETOR'] = '' ; df_pedido_defasagem['UTD'] = '' ; df_pedido_defasagem['ID'] = ''; df_pedido_defasagem['TIPO'] = ''; df_pedido_defasagem['QTD. TURMAS'] = ''; df_pedido_defasagem['QTD. NOTAS/TURMA'] = ''; df_pedido_defasagem['OBS']= ''


        df_pedido_defasagem = df_pedido_defasagem[['SETOR','UTD','ID','TIPO','QTD. TURMAS','QTD. NOTAS/TURMA','OBS']]
        df_pedido_defasagem.rename(columns = {'ID' : 'ZONA','TIPO':'TIPO_SERVICO','QTD. TURMAS':'QTD_TURMAS','QTD. NOTAS/TURMA':'QTD_NOTAS','OBS':'JUSTIFICATIVA'}, inplace = True)
        df_pedido_defasagem[['QTD_TURMAS','QTD_NOTAS']] = df_pedido_defasagem[['QTD_TURMAS','QTD_NOTAS']].fillna(0)
        df_pedido_defasagem[['QTD_TURMAS','QTD_NOTAS']] = df_pedido_defasagem[['QTD_TURMAS','QTD_NOTAS']].astype(int)
        df_pedido_defasagem[['TIPO_SERVICO','JUSTIFICATIVA']] = df_pedido_defasagem[['TIPO_SERVICO','JUSTIFICATIVA']].fillna('-')
        df_pedido_defasagem['ZONA'] = df_pedido_defasagem['ZONA'].fillna(0)
        df_pedido_defasagem['ZONA'] = df_pedido_defasagem['ZONA'].astype(int)
        df_pedido_defasagem['ZONA']  = df_pedido_defasagem['ZONA'].astype(str).str.pad(4,'left','0')
        df_pedido_defasagem['ACAO'] = ""
        df_pedido_defasagem['CARTEIRA'] = ""
        df_pedido_defasagem['TURMA'] = "STC"
        df_pedido_defasagem.loc[((df_pedido_defasagem.JUSTIFICATIVA == "-") &(df_pedido_defasagem.TIPO_SERVICO == "-") & (df_pedido_defasagem.QTD_TURMAS == 0) & (df_pedido_defasagem.QTD_NOTAS == 0)), "ACAO"] = "APAGAR"
        df_pedido_defasagem = df_pedido_defasagem[((df_pedido_defasagem['ACAO'] != "APAGAR"))]
        df_pedido_defasagem.loc[(df_pedido_defasagem.TIPO_SERVICO == "CA"), "CARTEIRA"] = "RECORTE"
        df_pedido_defasagem.loc[(df_pedido_defasagem.TIPO_SERVICO == "CS"), "CARTEIRA"] = "CORTE"
        df_pedido_defasagem['DEFASAGEM_PROGRAMACAO'] = df_pedido_defasagem['QTD_TURMAS'] * df_pedido_defasagem['QTD_NOTAS']
        df_pedido_defasagem = df_pedido_defasagem.dropna().reset_index(drop=True)        
        data_hoje = date.today()
        data_insercao = data_hoje
        df_pedido_defasagem.loc[(df_pedido_defasagem.UTD == "GRAÇA"), "UTD"] = "GRACA"
        df_pedido_defasagem.loc[(df_pedido_defasagem.UTD == "IRECÊ"), "UTD"] = "IRECE"
        df_pedido_defasagem.loc[(df_pedido_defasagem.UTD == "SANTO ANTÔNIO DE JESUS"), "UTD"] = "SANTO ANTONIO DE JESUS"
        df_pedido_defasagem.loc[(df_pedido_defasagem.UTD == "VALENÇA"), "UTD"] = "VALENCA"
        df_pedido_defasagem.loc[(df_pedido_defasagem.UTD == "JEQUIÉ"), "UTD"] = "JEQUIE"
        df_pedido_defasagem.loc[(df_pedido_defasagem.UTD == "EUNÁPOLIS"), "UTD"] = "EUNAPOLIS"
        cursor = connection_hana.cursor() 
        query = """
            DELETE FROM CLB344173.HISTORICO_SOLICITACAO_DEFASAGEM 
            WHERE DATA_INSERCAO = '{var_data_insercao}'
            """
        myRow = cursor.execute(query.format(var_data_insercao=data_insercao))
        for i in range(len(df_pedido_defasagem.index)):
            setor = str(df_pedido_defasagem["SETOR"][i])
            utd = str(df_pedido_defasagem["UTD"][i])
            zona = str(df_pedido_defasagem["ZONA"][i])
            tipo_servico = str(df_pedido_defasagem["TIPO_SERVICO"][i])
            qtd_turmas = int(df_pedido_defasagem["QTD_TURMAS"][i])
            qtd_notas = int(df_pedido_defasagem["QTD_NOTAS"][i])
            justificativa = str(df_pedido_defasagem["JUSTIFICATIVA"][i])

            insert_list = [(setor,utd,zona,tipo_servico,qtd_turmas,qtd_notas,justificativa,st.session_state.data_pedido,data_insercao)]
            cursor.executemany("""
            INSERT INTO CLB344173.HISTORICO_SOLICITACAO_DEFASAGEM ("SETOR","UTD","ZONA","TIPO_SERVICO","QTD_TURMAS","QTD_NOTAS","JUSTIFICATIVA","DATA_PEDIDO","DATA_INSERCAO")
            VALUES(?,?,?,?,?,?,?,?,?)
            """,insert_list)
    
    utd_configuracao = pd.read_csv('sources/utd_configuracao.csv',sep=';',encoding = "ISO-8859-1")
    utd_configuracao = utd_configuracao[['UTD','CONFIG']]

    nomes_zonas = pd.read_csv('sources/nomes_zonas.csv',sep=';',encoding = "ISO-8859-1") #pegar nomes das zonas...
    nomes_zonas = nomes_zonas[['ZONA','BASE CLICK']]
    nomes_zonas['ZONA'] = nomes_zonas['ZONA'].astype(str).str.pad(4,'left','0')
    if str.lower(st.session_state.pagina) == "defasagem por zonas" or str.lower(st.session_state.pagina) == "suscetiveis para mapa":
        df_pedido_defasagem = df_pedido_defasagem[['UTD','ZONA','DEFASAGEM_PROGRAMACAO','QTD_TURMAS','QTD_NOTAS','JUSTIFICATIVA','CARTEIRA','TURMA']]
        base_defasagens = pd.merge(df_defasagem_hoje, df_defasagem_hoje_mapa, how = 'outer', on=['UTD','ZONA','TURMA','CARTEIRA'])
        
        base_defasagens = pd.merge(base_defasagens, df_inserido_hoje, how = 'outer', on=['UTD','ZONA','TURMA','CARTEIRA'])
        
        base_defasagens = pd.merge(base_defasagens, df_pedido_defasagem, how = 'outer', on=['ZONA','CARTEIRA','TURMA','UTD'])
        base_final = pd.merge(df_defasagem_hoje_suscetiveis, base_defasagens, how = 'outer', on=['ZONA','CARTEIRA'])
        base_final = pd.merge(base_final, df_geradas_mes, how = 'left', on=['UTD','ZONA','CARTEIRA','TURMA'])
        base_final = pd.merge(base_final, df_executadas_mes, how = 'left', on=['UTD','ZONA','CARTEIRA','TURMA'])
        base_final = pd.merge(base_final, df_pendentes_UTD, how = 'left', on=['UTD','ZONA','CARTEIRA','TURMA'])
        base_final = pd.merge(base_final, df_anuladas_canceladas_UTD, how = 'outer', on=['UTD','TURMA','CARTEIRA','ZONA'])

        base_final = pd.merge(base_final, st.session_state.df_metas, how = 'left', on=['UTD','CARTEIRA','TURMA'])
        base_final = pd.merge(base_final, st.session_state.df_orcamento, how = 'left', on=['UTD','TURMA'])
        base_final.loc[((base_final.NOTAS_ESPERADAS_ATENA >0) |(base_final.NOTAS_GERADAS_TAB4 > 0) | (base_final.DEFASAGEM_GERACAO > 0) | (base_final.TOTAL_ESPERADO_MAPA > base_final.NOTAS_ESPERADAS_ATENA) | (base_final.DEFASAGEM_PROGRAMACAO >= 0) |(base_final.TOTAL_ESPERADO_MAPA > 0) ), "ACAO"] = "MANTER"
        base_final = base_final[((base_final['ACAO'] == "MANTER"))]
        base_final = pd.merge(base_final, nomes_zonas, how = 'left', on=['ZONA'])

        base_final[['BASE CLICK']] = base_final[['BASE CLICK']].fillna('-')
    else:
        base_defasagens = pd.merge(df_defasagem_hoje, df_defasagem_hoje_mapa, how = 'outer', on=['UTD','TURMA','CARTEIRA'])
        base_defasagens = pd.merge(base_defasagens, df_inserido_hoje, how = 'outer', on=['UTD','TURMA','CARTEIRA'])

        base_final = pd.merge(df_defasagem_hoje_suscetiveis, base_defasagens, how = 'outer', on=['UTD','CARTEIRA'])
        base_final = pd.merge(base_final, df_geradas_mes, how = 'left', on=['UTD','CARTEIRA','TURMA'])
        base_final = pd.merge(base_final, df_executadas_mes, how = 'left', on=['UTD','CARTEIRA','TURMA'])
        base_final = pd.merge(base_final, df_pendentes_UTD, how = 'left', on=['UTD','CARTEIRA','TURMA'])
        base_final = pd.merge(base_final, df_anuladas_canceladas_UTD, how = 'left', on=['UTD','TURMA','CARTEIRA'])
        base_final = pd.merge(base_final, st.session_state.df_metas, how = 'left', on=['UTD','CARTEIRA','TURMA'])
        base_final = pd.merge(base_final, st.session_state.df_orcamento, how = 'left', on=['UTD','TURMA'])
    
    
    #base_final = base_final[['ZONA','TURMA','CARTEIRA','TOTAL_ESPERADO_MAPA','NOTAS_ESPERADAS_ATENA','NOTAS_GERADAS_TAB4','DEFASAGEM_GERACAO','DEFASAGEM_PROGRAMACAO','QTD_TURMAS','QTD_NOTAS','JUSTIFICATIVA','QTD_SUSCETIVEIS','VALOR_COBRAVEL','PECLD','TICKET_COBRAVEL','TICKET_PECLD']]
    base_final['DEFASAGEM_MAPA'] = base_final['TOTAL_ESPERADO_MAPA'] - base_final['NOTAS_ESPERADAS_ATENA']
    base_final = pd.merge(base_final, utd_configuracao, how = 'left', on=['UTD'])
    base_final[['TOTAL_ESPERADO_MAPA','NOTAS_ESPERADAS_ATENA','NOTAS_DEFASAGEM_ATENA']] = base_final[['TOTAL_ESPERADO_MAPA','NOTAS_ESPERADAS_ATENA','NOTAS_DEFASAGEM_ATENA']].fillna(0.0)
    base_final[['TOTAL_ESPERADO_MAPA','NOTAS_ESPERADAS_ATENA','NOTAS_DEFASAGEM_ATENA']] = base_final[['TOTAL_ESPERADO_MAPA','NOTAS_ESPERADAS_ATENA','NOTAS_DEFASAGEM_ATENA']].astype(int)
    
    base_final[['PERCENT','QTD_META']] = base_final[['PERCENT','QTD_META']].fillna(0.0)
    base_final[['QTD_META']] = base_final[['QTD_META']]*st.session_state.percentual_meta_mes
    base_final[['QTD_META']] = base_final[['QTD_META']].astype(int)
    base_final[['UTD']] = base_final[['UTD']].fillna('-')

    

    base_final['PERCENT_ANULADAS'] = base_final['QTD_ANULADAS']/base_final['QTD_GERADAS']
    base_final['PERCENT_ANULADAS'] = base_final['PERCENT_ANULADAS'].fillna(0.0)

    if str.lower(st.session_state.pagina) == "defasagem por zonas" or str.lower(st.session_state.pagina) == "suscetiveis para mapa":
        base_final = base_final[['UTD','ZONA','BASE CLICK','TURMA','CARTEIRA','PERCENT','QTD_META','TOTAL_ESPERADO_MAPA','NOTAS_ESPERADAS_ATENA','NOTAS_GERADAS_TAB4','DEFASAGEM_GERACAO','DEFASAGEM_MAPA','DEFASAGEM_PROGRAMACAO','QTD_TURMAS','QTD_NOTAS','JUSTIFICATIVA','QTD_SUSCETIVEIS','VALOR_COBRAVEL','PECLD','TICKET_COBRAVEL','TICKET_PECLD','QTD_GERADAS','TICKET_PECLD_GERADAS','QTD_EXECUTADAS','TICKET_PECLD_EXECUTADAS','QTD_PENDENTES','CONFIG','QTD_ANULADAS','PERCENT_ANULADAS','NOTAS_DEFASAGEM_ATENA']]
        base_final[['DEFASAGEM_MAPA','DEFASAGEM_PROGRAMACAO','QTD_TURMAS','QTD_NOTAS','QTD_SUSCETIVEIS','VALOR_COBRAVEL','PECLD','TICKET_COBRAVEL','TICKET_PECLD','QTD_GERADAS','TICKET_PECLD_GERADAS','QTD_EXECUTADAS','TICKET_PECLD_EXECUTADAS','QTD_PENDENTES','QTD_ANULADAS']] = base_final[['DEFASAGEM_MAPA','DEFASAGEM_PROGRAMACAO','QTD_TURMAS','QTD_NOTAS','QTD_SUSCETIVEIS','VALOR_COBRAVEL','PECLD','TICKET_COBRAVEL','TICKET_PECLD','QTD_GERADAS','TICKET_PECLD_GERADAS','QTD_EXECUTADAS','TICKET_PECLD_EXECUTADAS','QTD_PENDENTES','QTD_ANULADAS']].fillna(0.0)
        base_final[['DEFASAGEM_MAPA','DEFASAGEM_PROGRAMACAO','QTD_TURMAS','QTD_NOTAS','QTD_SUSCETIVEIS','VALOR_COBRAVEL','PECLD','TICKET_COBRAVEL','TICKET_PECLD','QTD_GERADAS','TICKET_PECLD_GERADAS','QTD_EXECUTADAS','TICKET_PECLD_EXECUTADAS','QTD_PENDENTES','QTD_ANULADAS']] = base_final[['DEFASAGEM_MAPA','DEFASAGEM_PROGRAMACAO','QTD_TURMAS','QTD_NOTAS','QTD_SUSCETIVEIS','VALOR_COBRAVEL','PECLD','TICKET_COBRAVEL','TICKET_PECLD','QTD_GERADAS','TICKET_PECLD_GERADAS','QTD_EXECUTADAS','TICKET_PECLD_EXECUTADAS','QTD_PENDENTES','QTD_ANULADAS']].astype(int)
        base_final[['JUSTIFICATIVA']] = base_final[['JUSTIFICATIVA']].fillna('-')
        base_final[['NOTAS_GERADAS_TAB4','DEFASAGEM_GERACAO','PERCENT_ANULADAS']] = base_final[['NOTAS_GERADAS_TAB4','DEFASAGEM_GERACAO','PERCENT_ANULADAS']] .fillna(0.0)
        base_final[['NOTAS_GERADAS_TAB4','DEFASAGEM_GERACAO']]  = base_final[['NOTAS_GERADAS_TAB4','DEFASAGEM_GERACAO']] .astype(int)
        base_final[['NOTAS_GERADAS_TAB4','DEFASAGEM_GERACAO']] = base_final[['NOTAS_GERADAS_TAB4','DEFASAGEM_GERACAO']] .fillna(0.0)
        base_final[['NOTAS_GERADAS_TAB4','DEFASAGEM_GERACAO']]  = base_final[['NOTAS_GERADAS_TAB4','DEFASAGEM_GERACAO']] .astype(int)
        st.session_state.base_final = base_final.sort_values(['DEFASAGEM_GERACAO'],ascending=[False])
        return st.session_state.base_final
    else:
        base_final = base_final[['UTD','TURMA','CARTEIRA','TOTAL_ESPERADO_MAPA','NOTAS_ESPERADAS_ATENA','NOTAS_GERADAS_TAB4','DEFASAGEM_GERACAO','DEFASAGEM_MAPA','QTD_SUSCETIVEIS','PECLD','TICKET_PECLD','QTD_GERADAS','TICKET_PECLD_GERADAS','QTD_EXECUTADAS','TICKET_PECLD_EXECUTADAS','PERCENT','QTD_META','QTD_PENDENTES','CONFIG','QTD_ANULADAS','PERCENT_ANULADAS','NOTAS_DEFASAGEM_ATENA']]
        base_final[['DEFASAGEM_MAPA','QTD_SUSCETIVEIS','PECLD','TICKET_PECLD','QTD_GERADAS','TICKET_PECLD_GERADAS','QTD_EXECUTADAS','TICKET_PECLD_EXECUTADAS','QTD_PENDENTES','QTD_ANULADAS']] = base_final[['DEFASAGEM_MAPA','QTD_SUSCETIVEIS','PECLD','TICKET_PECLD','QTD_GERADAS','TICKET_PECLD_GERADAS','QTD_EXECUTADAS','TICKET_PECLD_EXECUTADAS','QTD_PENDENTES','QTD_ANULADAS']].fillna(0.0)
        base_final[['DEFASAGEM_MAPA','QTD_SUSCETIVEIS','PECLD','TICKET_PECLD','QTD_GERADAS','TICKET_PECLD_GERADAS','QTD_EXECUTADAS','TICKET_PECLD_EXECUTADAS','QTD_PENDENTES','QTD_ANULADAS']] = base_final[['DEFASAGEM_MAPA','QTD_SUSCETIVEIS','PECLD','TICKET_PECLD','QTD_GERADAS','TICKET_PECLD_GERADAS','QTD_EXECUTADAS','TICKET_PECLD_EXECUTADAS','QTD_PENDENTES','QTD_ANULADAS']].astype(int)
        base_final['PERCENT_META'] = base_final['QTD_EXECUTADAS']/base_final['QTD_META']
        base_final.replace([np.inf, -np.inf], np.nan, inplace=True)
        base_final['PERCENT_META'] = base_final['PERCENT_META'].fillna(0.0)
        base_final[['NOTAS_GERADAS_TAB4','DEFASAGEM_GERACAO','PERCENT_ANULADAS']] = base_final[['NOTAS_GERADAS_TAB4','DEFASAGEM_GERACAO','PERCENT_ANULADAS']] .fillna(0.0)
        base_final[['NOTAS_GERADAS_TAB4','DEFASAGEM_GERACAO']]  = base_final[['NOTAS_GERADAS_TAB4','DEFASAGEM_GERACAO']] .astype(int)
        st.session_state.base_final_2 = base_final.sort_values(['DEFASAGEM_GERACAO'],ascending=[False])
        return st.session_state.base_final_2
    #st.write(st.session_state.base_final_2)






    








