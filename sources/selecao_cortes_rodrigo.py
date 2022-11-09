import os
# import random
import pyhdb
import folium
import operator
import numpy as np
import progressbar
import pandas as pd
from money import Money
from hdbcli import dbapi
from itertools import islice
from tqdm import tqdm_notebook as tqdm
#import geopy.distance
# import matplotlib.pyplot as plt
#import math

from random import choices
import string

from tabulate import tabulate
from datetime import datetime
from sklearn.cluster import KMeans
from IPython.display import (FileLink, FileLinks, HTML, display, clear_output)

import locale
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

class SelecaoCorte():
    # Clientes que serão selecionados
    selecionados = None

    # Centroides dos clusters de clientes selecionados
    centroides = None
    
    # Cores utilizadas para plotagem de resultados
    cores = ['blue', 'red', 'orange', 'green', 'beige', 'white', 'darkgreen', 'darkblue',
             'lighgren', 'lightred']
    
    #identificador clusters, gambiarra
    m_a = 0
    
    #lista para o nome dos clusters
    nomes_clusters = []
    contasselecionadas = pd.DataFrame()
    
    #REFATORAR carteira, datapedido e consulta para ser uma lista. 
    def __init__(self, usuario: str, senha: str,consulta:list):
        """
            Classe para seleção através do método 2. #ToDo descrever posteriormente
        """
        try:
            self.importar_dados(usuario, senha,consulta)
        except Exception as e:
            print(e)
            print("Não foi possível autenticar-se ao HANA com as informações de login informadas. ")

    def importar_dados(self, usuario: str, senha: str, consulta: list):
        #inf_consulta: list consulta, carteira opcional, data pedido opcional
        """
            Classe para importação das contas contrados suscetíveis ao corte
            :param usuario:  login de usuario do HANA
            :param senha:  senha do usuario HANA
        """

        connection_hana = dbapi.connect(
                   address='BRNEO695',
                   port='30015',
                   user=usuario,
                   password=senha,
                   databasename='BNP',
                   sslValidateCertificate=True
              )

        # Importação do sql da consulta de clientes convencionais susceptíveis ao corte
        
        #rquivo_sql_susceptiveis_convencionais = open(inf_consulta[0], encoding="utf-8")
        arquivo_sql_susceptiveis_convencionais = open(consulta[0], encoding="utf-8")
        sql_susceptiveis_convencionais = arquivo_sql_susceptiveis_convencionais.read()
        arquivo_sql_susceptiveis_convencionais.close()
        if len(consulta) > 1:
            sql_susceptiveis_convencionais = sql_susceptiveis_convencionais.format(
                carteira = consulta[1],
                data_pedido = consulta[2],
                turma = consulta[3]
            )
        
        #print("Consultando clientes suscetíveis.")
        df = pd.read_sql(sql_susceptiveis_convencionais, connection_hana)
        #print("Importação dos dados concluída.")

        df.columns = df.columns.str.replace(" ", '')

        df[['LATITUDE', 'LONGITUDE']] = df[['LATITUDE', 'LONGITUDE']].replace(regex=',', value='.')
        df[['LATITUDE', 'LONGITUDE']] = df[['LATITUDE', 'LONGITUDE']].replace(regex=' ', value='')
        df[['LATITUDE', 'LONGITUDE']] = df[['LATITUDE', 'LONGITUDE']].replace(to_replace='?', value=None)
        df[['LATITUDE', 'LONGITUDE']] = df[['LATITUDE', 'LONGITUDE']].astype(float)
        df['ZONA'] = df['ZONA'].astype(str)

        df = df.replace(regex = '^ +| +$', value = '')

        # normalização
        df = df.rename(columns = {"ZCGQTFTVE": "QTFTVE"})
        cols_norm = ['ZCGMTVCOB', 'PECLD_CONS', 'QTFTVE']
        dfn = df.copy()
        dfn[cols_norm] = ((df[cols_norm] - df[cols_norm].min()) / (df[cols_norm].max() - df[cols_norm].min()))

        #if not 'irr' in dfn.columns: 
        #    dfn['irr'] = dfn['ZCGMTVCOB'] + dfn['PECLD_CONS'] 
        #    dfn = dfn.sort_values('irr', ascending=False)
        dfn[['MTV_COB', 'PECLD','ZCGQTFTVE']] = df[['ZCGMTVCOB', 'PECLD_CONS','QTFTVE']].copy()
        
        dfn = dfn.drop_duplicates(subset =['ZCGACCOUN'])
        #dfn = dfn.dropna(subset=['LATITUDE', 'LONGITUDE'])
    
        self.dfn = dfn

    def selecionar(self, UTD: str,locali: list = None,zona: list = None, municipio: list = None, bairros: list = None, metodo: str = 'nkcnk',
                   peso_mtvcob: float = 1.0,
                   peso_pecld: float = 1.2, 
                   peso_qtftve: float = 0, n: int = 2, k: int = 50, r: int = 500,
                   min_selecionados: int = 0, local: str = None,
                   r_max_preciso: bool = False,
                   calcular_irr: bool = True,
                   servico: str = None,
                   mista: bool = False,
                   plot: bool = True):
        """
        Função que realiza a seleção chamando uma outra função de seleção

        :param metodo:  qual o método será usado para a seleção
        :param UTD: UTD que realizará os cortes
        :param zona: Zona em que devem ser realizados os cortes
        :param bairros: bairros dos clientes a serem selecionados
        :param municipio: municipio dos clientes a serem selecionados
        :param n: número de clusters em que os clientes selecionados serão divididos
        :param k: Número máximo de clientes em um cluster
        :param r: raio (em metros) utilizado para primeira seleção de clusters
        :param r_max_preciso: maior precisão na seleção do raio máximo do cluster, mas pode diminui o IRR
        :param min_selecionados: número mínimos de clientes a serem selecionados por cluster
        :param plot: Se o resultado da seleção deve ser plotado em um mapa
        """
        # IRR = INDICE DE RECUPERACAO DE RECEITA
        self.nomes_clusters = []
        self.cores = ['blue', 'red', 'orange', 'green', 'beige', 'white', 'darkgreen', 'darkblue',
             'lighgren', 'lightred']
        for i in range(n):
            self.nomes_clusters.append("Cluster_"+str(i))
            if i > 9:
                self.cores.append('blue')
            
        if not 'IRR' in self.dfn.columns or calcular_irr == True:
            self.dfn['irr'] = (peso_mtvcob * self.dfn['ZCGMTVCOB'] + peso_pecld * self.dfn['PECLD_CONS']
                               + peso_qtftve * self.dfn['QTFTVE'])*100
        else: 
            self.dfn['irr'] = self.dfn['IRR'].copy()
        if UTD:
            UTD = UTD.upper().replace('_', ' ')

        self.bairros = bairros
        self.UTD = UTD
        self.locali = locali
        self.zona = zona
        self.municipio = municipio
        self.n = n
        self.r = r
        self.k = k
        self.r_max_preciso = r_max_preciso
        
        if zona and zona !="":
            if len(zona) == 1:
                #zona = zona.upper()
                marc_zona = zona[0]
                #print(marc_zona)
            else:
                marc_zona = 'MIX'
        else:
            zona = None
            marc_zona = 'MIX'
        
        if municipio == "":
            municipio = None

        if bairros == "":
            bairros = None
        if locali == "":
            locali = None
        if UTD == "":
            UTD = None
        if servico =="":
            servico = None
        
        if metodo == 'nkcnk':
            self.nkcnk(UTD=UTD, locali=locali, zona=zona, municipio=municipio, bairros=bairros, n=n, k=k, r=r,
                       min_selecionados=min_selecionados, r_max_preciso=r_max_preciso, 
                       local=local, fast=False,servico=servico, mista = mista,
                       plot=plot)               
        elif metodo == 'fast nkcnk':
            self.nkcnk(UTD=UTD, locali=locali,zona=zona, municipio=municipio, bairros=bairros, n=n, k=k, r=r,
                       min_selecionados=min_selecionados, local=local, r_max_preciso=r_max_preciso,
                       fast=True,servico=servico, mista = mista,
                       plot=plot)
        
      
        self.centroides['r'] = None

        novas_contas_selecionadas = []
        clusters = []
        """ 
            Correção de seleção: verifica (e corrige em caso positivo) se algum cliente dentro do cluster ficou fora da 
            seleção mesmo que o máximo do cluster não tenha sido atingido ou se algum cliente com maior indíce de 
            recuperação (em relação a algum dos clientes já selecionados) e dentro do raio final ficou de fora.
            
        """
        for i in range(n):
            #calcula o raio do cluster de acordo com o cliente com maior distância em relação ao centroide
            r_cluster = self.calcular_distancia(
                self.selecionados.loc[self.selecionados['cluster'] == i][['LATITUDE', 'LONGITUDE']],
                self.centroides.iloc[i][['LATITUDE', 'LONGITUDE']]
            ).max()
            self.centroides.loc[i, 'r'] = r_cluster

            """-----> Atualização do cluster: 
                     A partir do centroide, busca-se todos os clientes que estão dentro do raio e que não foram 
                     selecionados ainda por outro cluster e seleciona-se os k clientes com maior indice de recuperação
            """
            self.suscetiveis['dist'] = self.calcular_distancia(
                self.centroides.iloc[i][['LATITUDE', 'LONGITUDE']],
                self.suscetiveis[['LATITUDE', 'LONGITUDE']])

            contas_selecionadas = self.selecionados[self.selecionados.cluster != i]['ZCGACCOUN'].tolist()
            
            # Define o raio máximo da última etapa de seleção do cluster
            r_max = self.r if r_max_preciso == True else r_cluster 

            # Que não pertenciam a outro na seleção anterior cluster e que ainda não foram selecionados na atual
            novas_contas_selecionadas_cluster = self.suscetiveis[
                (~self.suscetiveis.ZCGACCOUN.isin(contas_selecionadas))&
                (~self.suscetiveis.ZCGACCOUN.isin(novas_contas_selecionadas))&
                (self.suscetiveis.dist <= r_max)
            ].sort_values('irr', ascending=False)[:self.k]['ZCGACCOUN'].tolist()

            self.suscetiveis.loc[self.suscetiveis.ZCGACCOUN.isin(novas_contas_selecionadas_cluster), 'cluster'] = int(i)
            novas_contas_selecionadas += novas_contas_selecionadas_cluster
            clusters += [i]*len(novas_contas_selecionadas_cluster)
            """<-----"""

        self.selecionados = self.suscetiveis[self.suscetiveis.ZCGACCOUN.isin(novas_contas_selecionadas)].copy()
        self.selecionados['cluster'] = self.selecionados['cluster'].astype(int)
        self.recalcular_centroides()
        self.selecionados['RAIO']= r
        #self.selecionados[['cluster']] = self.selecionados[['cluster']].apply(lambda x: x+1)
    
        self.selecionados['MARCACAO'] = ""
        
        for i in self.selecionados.cluster.unique():
            self.m_a = self.m_a + 1
            self.selecionados.loc[self.selecionados['cluster'] == i,'MARCACAO'] = self.m_a
            self.selecionados.loc[self.selecionados['cluster'] == i,'MARC_ZONA'] = marc_zona
          
        if plot:
            self.printar_resultados()
            return self.plotar()
        else:
            return self.resultados()

    def nkcnk(self, UTD: str, locali: list = None,zona: list = None, municipio: list = None, bairros: list = None, n: int = 2,
              k: int = 50, min_selecionados: int = 0,
              r: int = 500, r_max_preciso: bool = False,
              fast: bool = False, local: str = None,servico: str = None, mista: bool = False, 
              plot: bool = True):
        """
        Seleciona os clientes a serem cortados através do método nkn

        :param UTD: UTD que realizará os cortes
        :param zona: Zona em que devem ser realizados os cortes
        :param bairros: bairros dos clientes a serem selecionados
        :param municipio: municipio dos clientes a serem selecionados
        :param n: número de clusters em que os clientes selecionados serão divididos
        :param k: Número máximo de clientes em um cluster
        :param r: raio (em metros) utilizado para primeira seleção de clusters
        :param min_selecionados: número mínimos de clientes a serem selecionados por cluster
        :param plot: Se o resultado da seleção deve ser plotado em um mapa
        """
        clusters = []
        accoun_selecionadas = []

        ucs = self.dfn.copy()
        ucs = ucs.dropna(subset=['LATITUDE', 'LONGITUDE'])
        
        if mista:
            if servico != "" or servico != " ":
                #ucs = ucs.loc[~ucs['ZCGACCOUN'].isin(self.contasselecionadas)]
                ucs = ucs.loc[ucs['SERVICO'] == servico]
        
        if UTD:
            ucs = ucs.loc[ucs['UTD'] == UTD]
        
        if zona:
            ucs = ucs.loc[ucs['ZONA'].isin(zona)]

        if municipio:
            ucs = ucs.loc[ucs['ZCGMUNICI'].isin(municipio)]

        if bairros:
            ucs = ucs.loc[ucs['ZCGBAIRRO'].isin(bairros)]
        if locali:
            ucs = ucs.loc[ucs['ZCGLOCALI'].isin(locali)]
        if local == 'R':
            ucs = ucs.loc[ucs['ZCGTIPLOC'] == 'R']
        elif local == 'U':
            ucs = ucs.loc[ucs['ZCGTIPLOC'] == 'U']
        
        
        if fast:
            #Busca os clusters a partir de apenas 25% dos clientes filtrados
            #print("fast", fast, ucs.sort_values('irr', ascending=False)[:ucs.UTD.count()//4].UTD.count())
            ccs_lista = list(ucs.sort_values('irr', ascending=False)[:ucs.UTD.count()//4].iterrows())
        else:
            #print("normal", fast, ucs.UTD.count())
            ccs_lista = list(ucs.iterrows())

        #Possíveis cortes
        self.suscetiveis = ucs.copy()
        
       
        for i in range(n):
       
            selecoes = []
            # Filtra-se os clientes já selecionados
            ucs = ucs[~ucs.ZCGACCOUN.isin(accoun_selecionadas)]

            first = True
        
            for index, cc in ccs_lista:
                """ 
                    Para cada cliente, seleciona-se os k clientes com maior indice de rec a uma distância r dele.
                    Em seguida calcula-se a latitude e longitude media (centroide) desses clientes e seleciona-se o k 
                    clientes com maior índice de recuperação a uma distância <= r do centroide. Não necessariamente o 
                    segundo grupo de k clientes será igual primeiro.   
                """
          
                ucs['raio'] = self.calcular_distancia(cc[['LATITUDE', 'LONGITUDE']],
                                                              ucs[['LATITUDE', 'LONGITUDE']])
                
                selecionados_aux = ucs.loc[ucs['raio'] <= r].sort_values('irr', ascending=False)[:k]
                ucs['raio'] = self.calcular_distancia(selecionados_aux[['LATITUDE', 'LONGITUDE']].mean(),
                                                              ucs[['LATITUDE', 'LONGITUDE']])
                selecionados_aux = ucs.loc[ucs['raio'] <= r].sort_values('irr', ascending=False)[:k]
                
                if first:
                    selecionados = selecionados_aux.copy()
                    first = False
                else:
                    if selecionados_aux.shape[0] >= min_selecionados and selecionados.shape[0]<min_selecionados:
                        selecionados = selecionados_aux.copy()
                    elif (selecionados_aux.shape[0] < min_selecionados and selecionados.shape[0]< min_selecionados) and (selecionados_aux.shape[0]>selecionados.shape[0]):
                        selecionados = selecionados_aux.copy()
                    elif selecionados_aux.shape[0] == selecionados.shape[0]:
                        if selecionados_aux['irr'].sum() > selecionados['irr'].sum():
                            selecionados = selecionados_aux.copy()                        
                    elif selecionados_aux.shape[0] >= min_selecionados and selecionados.shape[0]>= min_selecionados:
                        if selecionados_aux['irr'].sum() > selecionados['irr'].sum():
                            selecionados = selecionados_aux.copy()
                    

            #clusters += [selecoes[0].copy()]

            accoun_selecionadas += selecionados['ZCGACCOUN'].tolist()

        selecionados = self.dfn[self.dfn.ZCGACCOUN.isin(accoun_selecionadas)].copy()
     
        kmeans = KMeans(n_clusters=n).fit(selecionados[['LATITUDE', 'LONGITUDE']])
     
        selecionados['cluster'] = kmeans.labels_
       
        centroides = pd.DataFrame(kmeans.cluster_centers_, columns=['LATITUDE', 'LONGITUDE'])
        selecionados['ordem'] = None

        ordem = []

        for i, selecionado in selecionados.iterrows():
            distancias_centroides = (((selecionado['LATITUDE'] - centroides['LATITUDE']) ** 2 +
                                      (selecionado['LONGITUDE'] - centroides['LONGITUDE']) ** 2
                                      ) ** (1 / 2)).sort_values(ascending=True)
            ordem += [distancias_centroides.iloc[0] - distancias_centroides.iloc[n - 1]]

        selecionados['ordem'] = ordem
        selecionados = selecionados.sort_values('ordem', ascending=True)

        clusters = []

        for i, selecionado in selecionados.iterrows():
            distancias_centroides = ((((selecionado['LATITUDE'] - centroides['LATITUDE']) ** 2 +
                                       (selecionado['LONGITUDE'] - centroides['LONGITUDE']) ** 2
                                       ) ** (1 / 2)) * 40030000 / 360).sort_values(ascending=True)

            for cluster in distancias_centroides.index:
                if clusters.count(cluster) < k:
                    clusters += [cluster]
                    break
                # ToDo Descobrir origem do problema e retirar essa gambiarra
                if len(clusters) >= k*n and len(clusters) < selecionados.shape[0]:
                    clusters += [cluster]
                
    
        selecionados['cluster'] = clusters
 
        
        self.selecionados = selecionados

        self.centroides = centroides
       
        self.recalcular_centroides()

        
                 

            

    def plotar(self):
        """
        Plota o resultado da seleção
        """

        mapa = folium.Map(
            location=[self.selecionados.iloc[0]['LATITUDE'], self.selecionados.iloc[0]['LONGITUDE']],
            zoom_start=13, prefer_canvas=True
        )
        
        nao_selecionados = self.suscetiveis[~self.suscetiveis.isin(self.selecionados['ZCGACCOUN'].tolist())].copy()
        nao_selecionados = nao_selecionados.dropna(subset=['LATITUDE', 'LONGITUDE'])
        # Plotagem dos clientes com maiores indice de recuperacao que não foram selecionados
        for i_ns, nao_selecionado in nao_selecionados.sort_values('irr', ascending=False)[
                                     :15].iterrows():
            cor = 'gray' if nao_selecionado['MTV_COB'] >= 1000 else 'lightgray'
            folium.Marker(
                location=[nao_selecionado['LATITUDE'], nao_selecionado['LONGITUDE']],
                popup="""<strong>ACC:</strong> {0} <br> 
                                <strong>UTD:</strong> {1} <br> 
                                <strong>MUN:</strong> {2} <br> 
                                <strong>BAIRRO:</strong> {3} <br> 
                                <strong>ZONA:</strong> {4} <br> 
                                <strong>ZGCMTVCOB:</strong> R${5:.2F}<br> 
                                <strong>PECLD:</strong> R${6:.2F}<br>
                                <strong>QTFTVE:</strong> {7}<br>
                                <strong>TIPLOC:</strong> {8}<br>
                                <a target="_blank" href="https://www.google.com.br/maps/place/{9}+{10}/@{9},{10},12z">
                                google maps</a>""".format(
                    nao_selecionado['ZCGACCOUN'],
                    nao_selecionado['UTD'],
                    nao_selecionado['ZCGMUNICI'],
                    nao_selecionado['ZCGBAIRRO'],
                    nao_selecionado['ZONA'],
                    nao_selecionado['MTV_COB'],
                    nao_selecionado['PECLD'],
                    nao_selecionado['ZCGQTFTVE'],
                    nao_selecionado['ZCGTIPLOC'],
                    nao_selecionado['LATITUDE'],
                    nao_selecionado['LONGITUDE'],
                ),
                icon=folium.Icon(color=cor, icon='home')
            ).add_to(mapa)
        
        # Para identificação de possíveis erros de cadastro
        nao_selecionados = self.dfn[~self.dfn.ZCGACCOUN.isin(self.selecionados['ZCGACCOUN'].tolist())].copy()

        # Plotagem dos clientes selecionados divididos por cluster através das cores
        for index, cc in self.selecionados.iterrows():
         
            distancia = self.calcular_distancia(cc[['LATITUDE', 'LONGITUDE']],
                                                self.centroides.iloc[cc['cluster']][['LATITUDE', 'LONGITUDE']])
          
            folium.Marker(
                location=[cc['LATITUDE'], cc['LONGITUDE']],
                popup="""
                            <strong>ACC:</strong> {0} <br> 
                            <strong>MUN:</strong> {1} <br> 
                            <strong>BAIRRO:</strong> {2} <br> 
                            <strong>ZONA:</strong> {3} <br> 
                            <strong>ZGCMTVCOB:</strong> R${4:.2F}<br> 
                            <strong>PECLD:</strong> R${5:.2F}<br>
                            <strong>QTFTVE:</strong> {6}<br>
                            <strong>TIPLOC:</strong> {7}<br>
                            <strong>Dist:</strong> {8:.2F}m<br>
                            <a target="_blank" href="https://www.google.com.br/maps/place/{9}+{10}/@{9},{10},19z">
                            google maps</a>""".format(
                    cc['ZCGACCOUN'],
                    cc['ZCGMUNICI'],
                    cc['ZCGBAIRRO'],
                    cc['ZONA'],
                    cc['MTV_COB'],
                    cc['PECLD'],
                    cc['ZCGQTFTVE'],
                    cc['ZCGTIPLOC'],
                    distancia,
                    cc['LATITUDE'],
                    cc['LONGITUDE'],
                ),
                icon=folium.Icon(color=self.cores[cc['cluster']], icon='home')
            ).add_to(mapa)
      
        # Plotagem da área dos clusters e seus centroides
        for i, centroide in self.centroides.iterrows():
            nao_selecionados['dist'] = self.calcular_distancia(nao_selecionados[['LATITUDE', 'LONGITUDE']],
                                                               centroide[['LATITUDE', 'LONGITUDE']])

            nao_selecionados_proximos = nao_selecionados.loc[nao_selecionados['dist'] <= self.r + 1000].sort_values(
                'dist')

            # plotagem dos clientes não selecionados que estão a 1.5r de distância do centroide
            for i_ns, nao_selecionado in nao_selecionados_proximos[:30].iterrows():
                cor = 'gray' if nao_selecionado['ZCGQTFTVE'] >= 10 else 'lightgray'
                folium.Marker(
                    location=[nao_selecionado['LATITUDE'], nao_selecionado['LONGITUDE']],
                    popup="""<strong>ACC:</strong> {0} <br> 
                            <strong>MUN:</strong> {1} <br> 
                            <strong>BAIRRO:</strong> {2} <br> 
                            <strong>ZONA:</strong> {3} <br> 
                            <strong>ZGCMTVCOB:</strong> R${4:.2F}<br> 
                            <strong>PECLD:</strong> R${5:.2F}<br>
                            <strong>QTFTVE:</strong> {6}<br>
                            <strong>TIPLOC:</strong> {7}<br>
                            <strong>Dist:</strong> {8:.2F}m<br>
                            <a target="_blank" href="https://www.google.com.br/maps/place/{9}+{10}/@{9},{10},19z">
                            google maps</a>""".format(
                        nao_selecionado['ZCGACCOUN'],
                        nao_selecionado['ZCGMUNICI'],
                        nao_selecionado['ZCGBAIRRO'],
                        nao_selecionado['ZONA'],
                        nao_selecionado['MTV_COB'],
                        nao_selecionado['PECLD'],
                        nao_selecionado['ZCGQTFTVE'],
                        nao_selecionado['ZCGTIPLOC'],
                        nao_selecionado['dist'],
                        nao_selecionado['LATITUDE'],
                        nao_selecionado['LONGITUDE'],
                    ),
                    icon=folium.Icon(color=cor, icon='home')
                ).add_to(mapa)
           
            # Plotagem do centroide
            folium.Marker(
                location=[centroide['LATITUDE'], centroide['LONGITUDE']],
                popup="""Centroide do cluster <strong style="color: {};">{}</strong>""".format(self.cores[i],
                                                                                               self.nomes_clusters[i]),
                icon=folium.Icon(color='purple')
            ).add_to(mapa)

            mtv_cluster = self.selecionados.loc[self.selecionados['cluster'] == i]['MTV_COB'].sum()
            pecld_cluster = self.selecionados.loc[self.selecionados['cluster'] == i]['PECLD'].sum()

            folium.Circle(location=[centroide['LATITUDE'], centroide['LONGITUDE']], radius=centroide['r'],
                          popup="""Área dentro do raio de {:.2F}m do cluster <strong style="color: {};">{}</strong>. <br>
                                     <strong>MTVCOB:</strong> R${:.2F} <br>
                                     <strong>PECLD:</strong> R${:.2F} <br>
                                  """.format(centroide['r'], self.cores[i], self.nomes_clusters[i], mtv_cluster,
                                             pecld_cluster),
                          color=self.cores[i], fill=True, fill_color=self.cores[i]).add_to(mapa)
        
        
        nome = self.gerar_nome_arquivo()
        
        self.nome_mapa = "selecao_{}_{}.html".format(nome, datetime.now().strftime("%d-%m-%Y %H-%M-%S"))
        
        self.mapa = mapa

        return mapa
    
    def gerar_nome_arquivo(self):
        UTD = self.UTD if self.UTD else ''
        #zona = self.zona if self.zona else ''
        #municipio = self.municipio if self.municipio else ''
        if self.zona:
            zona = ("_".join(self.zona))
        else:
            zona = ''
                 
        if self.municipio:
            municipio = ("_".join(self.municipio))
        else:
            municipio = ''
        
        
        if self.locali:
            locali = ("_".join(self.locali))
        else:
            locali = ''
        if self.bairros:
            bairro = ("_".join(self.bairros))
        else:
            bairro = ''
        
        return UTD+zona+municipio+locali+bairro
        

    def gerar_csv(self, nome: str = None):
        """
        Gera um arquivo csv com os clientes selecionados
        :param nome: nome do arquivo csv (opcional)
        """
        #zona = self.zona if self.zona else ''
        nome_arquivo = self.gerar_nome_arquivo()
        

        if not nome:
            nome_csv = "selecao_{}_{}.csv".format(nome_arquivo,
                                                      datetime.now().strftime("%d-%m-%Y %H-%M-%S"))
        else:
            nome_csv = nome

        self.nome_csv = nome_csv
        self.selecionados[['ZCGACCOUN', 'MTV_COB', 'PECLD', 'ZCGMUNICI', 'ZCGBAIRRO',
                           'LATITUDE', 'LONGITUDE', 'cluster']].to_csv("resultados\{}".format(nome_csv), sep=';',
                                                                       decimal=',', index=False)

        print("\nArquivo csv gerado com sucesso: {}\n".format(nome_csv))

    def gerar_excel(self, nome: str = None):
        """
        Gera um arquivo excel com os clientes selecionados

        :param nome: nome do arquivo csv (opcional)
        """
        nome_arquivo = self.gerar_nome_arquivo()
        
        
        
        if not nome:
            nome_excel = "selecao_{}_{}.xls".format(nome_arquivo,
                                                        datetime.now().strftime("%d-%m-%Y %H-%M-%S"))
        else:
            nome_excel = nome

        self.nome_excel = nome_excel
        self.selecionados[['ZCGACCOUN', 'MTV_COB', 'PECLD', 'ZCGMUNICI', 'ZCGBAIRRO',
                           'LATITUDE', 'LONGITUDE', 'cluster']].to_excel("resultados\{}".format(nome_excel),
                                                                         float_format = ":,", index=False)

        print("\nArquivo csv gerado com sucesso: {}\n".format(nome_excel))
        

         

    def salvar_mapa(self):
        """ Salva o mapa em um arquivo html """
        self.mapa.save("resultados\{}".format(self.nome_mapa))

    def recalcular_centroides(self):
        """ Recalcula os centroides e a distancia deles aos selecionados """
        for i, centroide in self.centroides.iterrows():
            centroide['LATITUDE'] = self.selecionados.loc[self.selecionados['cluster'] == i]['LATITUDE'].mean()
            centroide['LONGITUDE'] = self.selecionados.loc[self.selecionados['cluster'] == i]['LONGITUDE'].mean()
            centroide['r'] = self.calcular_distancia(
                self.selecionados.loc[self.selecionados['cluster'] == i][['LATITUDE', 'LONGITUDE']],
                centroide[['LATITUDE', 'LONGITUDE']]
            ).max()
            self.selecionados.loc[self.selecionados['cluster'] == i, 'dist'] = self.calcular_distancia(
                self.selecionados.loc[self.selecionados['cluster'] == i][['LATITUDE', 'LONGITUDE']],
                centroide[['LATITUDE', 'LONGITUDE']]
            ) #.max()
            self.centroides.loc[i, 'LATITUDE'] = centroide['LATITUDE']
            self.centroides.loc[i, 'LONGITUDE'] = centroide['LONGITUDE']
            self.centroides.loc[i, 'r'] = centroide['r']










     
    def preencher_cluster(self,r:int,UTD: str=None,n:int = 0, locali: list = None,zona: list = None, municipio: list = None, bairros: list = None, 
                     min_selecionados: int = 0, r_max_preciso: bool = False, local: str = None,
                     preencher: str = None, qtd_preencher:int = 0):
                    
        """
        Função que realiza o preenchimento de um cluster com outro tipo de serviço

        :param UTD: UTD para filtrar os clientes
        :param zona: Zona para filtrar os clientes
        :param bairros: bairros para filtrar os clientes
        :param municipio: municipio dos clientes a serem selecionados
        :param r_max_preciso: maior precisão na seleção do raio máximo do cluster, mas pode diminui o IRR
        :param min_selecionados: número mínimos de clientes a serem selecionados por cluster original
        :preencher: carteira para realizar o preenchimento do cluster
        :qtd_preencher: quantidade de clientes para ser adicionado ao cluster, caso seja passado o valor 0 o cluster original será preenchido conforme defasagem
        """             


        selecionados_tot = pd.DataFrame()
        accoun_selecionadas = []

        ucs = self.dfn.copy()
        ucs = ucs.dropna(subset=['LATITUDE', 'LONGITUDE'])
                

        ucs = ucs.loc[ucs['SERVICO'] == preencher]
        
        if UTD:
            ucs = ucs.loc[ucs['UTD'] == UTD]
        
        if zona:
            ucs = ucs.loc[ucs['ZONA'].isin(zona)]

        if municipio:
            ucs = ucs.loc[ucs['ZCGMUNICI'].isin(municipio)]

        if bairros:
            ucs = ucs.loc[ucs['ZCGBAIRRO'].isin(bairros)]
        if locali:
            ucs = ucs.loc[ucs['ZCGLOCALI'].isin(locali)]
        if local == 'R':
            ucs = ucs.loc[ucs['ZCGTIPLOC'] == 'R']
        elif local == 'U':
            ucs = ucs.loc[ucs['ZCGTIPLOC'] == 'U']
        
        ucs = ucs.loc[~ucs['ZCGACCOUN'].isin(self.selecionados['ZCGACCOUN'].to_list())]

   
            
        
        
        for i in range(n):
            ucs = ucs[~ucs.ZCGACCOUN.isin(accoun_selecionadas)]

            if qtd_preencher >0:
                defn = qtd_preencher
            else:
                defn = min_selecionados - self.selecionados.loc[self.selecionados['cluster']==i].shape[0] 
           
          
            if defn > 0:
                
                if r_max_preciso:
                    r_dist = r
                else:
                    r_dist = self.centroides.iloc[i]['r']
                  
                ucs['raio'] = self.calcular_distancia(self.centroides.iloc[i][['LATITUDE', 'LONGITUDE']],
                                                                ucs[['LATITUDE', 'LONGITUDE']]) 
                selecionados = ucs.loc[ucs['raio'] <= r_dist].sort_values('irr', ascending=False)[:defn]
                

                selecionados['dist'] = self.calcular_distancia(
                    self.centroides.iloc[i][['LATITUDE', 'LONGITUDE']],
                    selecionados[['LATITUDE', 'LONGITUDE']])

               #5
                selecionados.drop(columns = ['raio'],inplace=True)
                selecionados['CARTEIRA'] = preencher
                selecionados['cluster'] =  i
                selecionados['MARCACAO'] = self.selecionados.loc[self.selecionados['cluster']==i]['MARCACAO'].iloc[0]
                selecionados['MARC_ZONA'] = self.selecionados.loc[self.selecionados['cluster']==i]['MARC_ZONA'].iloc[0]
                selecionados['RAIO'] = r

                accoun_selecionadas.append(selecionados['ZCGACCOUN'].to_list())
              
                selecionados_tot = selecionados_tot.append(selecionados)
            
        
        self.selecionados = self.selecionados.append(selecionados_tot)    
        #self.selecionados = self.selecionados.append(sel ecionados_tot)
        self.recalcular_centroides()
        
        return selecionados_tot

            
        
            
    def resultados(self):
        """
            Printa os resultados da seleção: MTVCOB total, PECLD_CONS total e raio de cada cluster
        """

        # print("\nmtvcob_tot : R$ {:.2F}".format(self.selecionados['MTV_COB'].sum()))
        # print("\npecld_cons : R$ {:.2F}\n".format(self.selecionados['PECLD'].sum()))

        resultados = []
        for i in range(self.n):
            resultados += [[self.nomes_clusters[i],
                            self.selecionados['cluster'].tolist().count(i),
                            round(self.centroides.iloc[i]['r'], 2),
                            round(self.selecionados.loc[self.selecionados['cluster'] == i]['MTV_COB'].sum(),
                                  2),
                            round(self.selecionados.loc[self.selecionados['cluster'] == i]['PECLD'].sum(),
                                  2)]]

        resultados += [
            ['TOTAL', self.selecionados['ZCGACCOUN'].count(), '', round(self.selecionados['MTV_COB'].sum(), 2),
             round(self.selecionados['PECLD'].sum(), 2)]]

        return resultados

    def printar_resultados(self):
        """
            Printa os resultados da seleção: MTVCOB total, PECLD_CONS total e raio de cada cluster
        """

        # print("\nmtvcob_tot : R$ {:.2F}".format(self.selecionados['MTV_COB'].sum()))
        # print("\npecld_cons : R$ {:.2F}\n".format(self.selecionados['PECLD'].sum()))

        dados_tabela = [['TODOS', self.selecionados['ZCGACCOUN'].count(), '', self.selecionados['MTV_COB'].sum(),
                         self.selecionados['PECLD'].sum()]]
        for i in range(self.n):
            dados_tabela += [[self.nomes_clusters[i],
                              self.selecionados['cluster'].tolist().count(i),
                              round(self.centroides.iloc[i]['r'], 2),
                              round(self.selecionados.loc[self.selecionados['cluster'] == i]['MTV_COB'].sum(),
                                    2),
                              round(self.selecionados.loc[self.selecionados['cluster'] == i]['PECLD'].sum(),
                                    2)
                              ]]

        # print(tabulate(dados_tabela, headers=['Cluster', 'Clientes', 'Raio', 'MTVCOB', 'PECLDCONS'], tablefmt='orgtbl'))

    def remover_cliente(self, contas: list, plot: bool = True):
        """
        Remove um cliente da seleção

        :param contas: lista de contas contratos dos clientes a serem removidos da seleção
        """
        # Verifica se as contas a serem removidas realmente estão contidas na seleção. ToDo tentar fazer isso com numpy
        if (all(cc in self.selecionados['ZCGACCOUN'].tolist() for cc in contas)):
            self.selecionados = self.selecionados.loc[~self.selecionados['ZCGACCOUN'].isin(contas)]

            self.recalcular_centroides()
            self.printar_resultados()

            if plot:
                return self.plotar()
        else:
            print("Cliente(s) não consta(m) na seleção.")

    def set_cluster(self, contas: list, plot: bool = True):
        """
        Seta manualmente o cluster dos clientes indicados. Recebe uma lista de tuplas em que cada tupla deve conter o cliente
        e ocluster

        :param contas: lista de tuplas com número da conta contrato e cluster. Ex: contas=[(855347199, 'Azul'), (7007360716, 'Azul')]
        """
        # Verifica se as contas a serem removidas realmente estão contidas na seleção. ToDo tentar fazer isso com numpy
        if (all(cc[0] in self.selecionados['ZCGACCOUN'].tolist() for cc in contas)):
            for conta in contas:
                row_indexer = self.selecionados['ZCGACCOUN'] == conta[0]
                self.selecionados.loc[row_indexer, 'cluster'] = self.nomes_clusters.index(conta[1])

            self.recalcular_centroides()
            self.printar_resultados()

            if plot:
                return self.plotar()
        else:
            print("Cliente(s) não consta(m) na seleção.")

    def selecionar_clientes(self, contas: list, plot: bool = True):
        """
        Seta manualmente clientes não-selecionados na seleção. Recebe uma lista de tuplas em que cada tupla deve conter o cliente
        e ocluster

        :param contas: lista de tuplas com número da conta contrato e cluster. Ex: contas=[(855347199, 'Azul'), (7007360716, 'Azul')]
        """
        # Verifica se as contas a serem removidas realmente estão contidas na seleção. ToDo tentar fazer isso com numpy
        if (all(cc[0] not in self.selecionados['ZCGACCOUN'].tolist() for cc in contas)):
            for conta in contas:
                novo_selecionado = self.dfn.loc[self.dfn['ZCGACCOUN'] == conta[0]].copy()
                novo_selecionado['cluster'] = self.nomes_clusters.index(conta[1])
                novo_selecionado[['PECLD', 'MTV_COB']] = novo_selecionado[
                    ['PECLD', 'MTV_COB']]
                self.selecionados = pd.concat([self.selecionados, novo_selecionado], sort=False)

            self.recalcular_centroides()
            self.printar_resultados()

            if plot:
                return self.plotar()
        else:
            print("Cliente(s) já consta(m) na seleção.")
            
    def calcular_distancia_h(self, ponto1, ponto2) -> float:
        """
        Calcula a distância em metros entre duas coordenadas geográficas
        :param ponto 1: df com as coordenadas do ponto 1
        :param ponto 2: df com as coordenadas do ponto 2
        :return distância em metros entre os dois pontos"""

        return (
                       (
                               (ponto1['LATITUDE'] - ponto2['LATITUDE']) ** 2 +
                               (ponto1['LONGITUDE'] - ponto2['LONGITUDE']) ** 2
                       ) ** 0.5
               ) * 40030000 / 360
    
    def calcular_distancia(self,ponto1,ponto2)-> float:
        
        """Calcula a distância em metros entre dois pontos, utilizando a equação de harversine
        ponto1 - dataframe com as coordenadas do ponto1, ponto2 dataframe com as coordenas dos pontos 2.
        Execução um pouco mais lenta que o método simplificado utilizado."""
        
        # convert decimal degrees to radians

        ponto1['LATITUDE'] = np.radians(ponto1['LATITUDE'])
        ponto2['LATITUDE'] = np.radians(ponto2['LATITUDE'])
        ponto1['LONGITUDE'] = np.radians(ponto1['LONGITUDE'])
        ponto2['LONGITUDE'] = np.radians(ponto2['LONGITUDE'])


    
        dlon = ponto2['LONGITUDE'] - ponto1['LONGITUDE']

        dlat = ponto2['LATITUDE'] - ponto1['LATITUDE']
        a = np.power(np.sin(dlat/2),2) + np.cos(ponto1['LATITUDE']) * np.cos(ponto2['LATITUDE']) * np.power(np.sin(dlon/2),2)
        c = 2 * np.arcsin(np.sqrt(a)) 
        r = 6371 # Radius of earth in kilometers. Use 3956 for miles. Determines return value units.
        return c * r*1000
        
    

    def multiprocess_zonas(self,zonas,metodo,calcular_irr,r_max_preciso,mista):
        selecionados_sm = pd.DataFrame()
        n_selecionados_sm = pd.DataFrame()
        erros_sm = pd.DataFrame()
        erros = []
        
        for i, zona in zonas.loc[zonas.SELECIONAR=="SIM"].iterrows(): 
            try:
                
                raio = zona.RAIO_IDEAL 
                zona_concluida = False
                clusterid = ""

                if mista:
                    clusterid = str(zona.CARTEIRA[0:1]) + "_" 
                if zona.UTD and not zona.ZONA:
                    clusterid = clusterid + str(zona.UTD) + "_"

                if zona.ZONA and zona.ZONA !="":
                    zona_s = list(zona.ZONA.split(','))
                    for i in range(len(zona_s)):
                        zona_s[i] = str(zona_s[i]).zfill(4)
                    clusterid = clusterid+(".".join(zona_s)) + "_"
                else:
                    zona_s = None

                if zona.MUNICIPIO and zona.MUNICIPIO !="":
                    municipio = list(zona.MUNICIPIO.split(','))
                    municipio_c = [municipio[i][0] for  i in range(len(municipio))]
                    clusterid = clusterid+(".".join(municipio_c)) + "_"
                else:
                    municipio = None

                if zona.BAIRRO and zona.BAIRRO !="":
                    bairro = list(zona.BAIRRO.split(','))
                    bairro_c = [bairro[i][0] for  i in range(len(bairro))]
                    clusterid = clusterid+(".".join(bairro_c)) + "_"
                else:
                    bairro = None
                if zona.LOCALI and zona.LOCALI !="":
                    locali = list(zona.LOCALI.split(','))
                    locali_c = [locali[i][0] for  i in range(len(locali))]
                    clusterid = clusterid+(".".join(locali_c)) + "_"
                else:
                    locali = None
                
                if zona.PREENCHER:
                    if zona.QTD_PREENCHER:
                        qtd_preencher = int(zona.QTD_PREENCHER)
                    else:
                        qtd_preencher = 0

               
                
                while raio <= zona.RAIO_MAX and zona_concluida == False: 
                    
                    self.selecionar(metodo=metodo, 
                                            peso_mtvcob=zona.PESO_MTVCOB,
                                            peso_pecld=zona.PESO_PECLD,
                                            peso_qtftve = zona.PESO_QTDFTVE,
                                            UTD=zona.UTD,
                                            locali=locali,
                                            zona=zona_s,
                                            calcular_irr=calcular_irr, 
                                            municipio=municipio,
                                            bairros=bairro,
                                            n=zona.CLUSTERS, 
                                            k=zona.QTD_MAX, 
                                            r=raio,
                                            min_selecionados=zona.QTD_MIN,
                                            r_max_preciso=r_max_preciso, 
                                            local=zona.TIPO_LOCAL, 
                                            servico = zona.CARTEIRA,
                                            mista = mista,
                                            plot=False) 

                    resultado = self.selecionados.copy()
              
                    #if resultado.shape[0] >= zona.QTD_MIN*zona.CLUSTERS:
                    if self.selecionados.groupby(by="cluster").count()['ZCGACCOUN'].min() >= zona.QTD_MIN:
                        
                        self.selecionados['CARTEIRA'] = zona.CARTEIRA
                        
                        
                        if zona.PREENCHER !="" and qtd_preencher >0:
                            preenchidos = self.preencher_cluster(UTD = zona.UTD, r= zona.RAIO_MAX, n = zona.CLUSTERS,locali = locali, zona = zona_s,
                            municipio = municipio, bairros = bairro, min_selecionados=zona.QTD_MIN,
                            preencher = zona.PREENCHER, local = zona.TIPO_LOCAL, qtd_preencher=qtd_preencher)
                            
                            #self.selecionados = self.selecionados.append(preenchidos)
                            self.selecionados['TURMA'] = zona.TURMA
                            #self.selecionados[['cluster']] = self.selecionados[['cluster']].apply(lambda x: x + 1)
                            #self.selecionados['cluster_id'] = clusterid + self.selecionados['cluster'].astype(str) 

                            self.selecionados[['cluster']] = self.selecionados[['cluster']].apply(lambda x: x + 1)
                            self.selecionados['cluster_id'] = clusterid  + self.selecionados['cluster'].astype(str)
                            selecionados_sm = selecionados_sm.append(self.selecionados) 
                            

                        else:
                            self.selecionados['TURMA'] = zona.TURMA
                            self.selecionados[['cluster']] = self.selecionados[['cluster']].apply(lambda x: x + 1)
                            self.selecionados['cluster_id'] = clusterid  + self.selecionados['cluster'].astype(str) 
                            selecionados_sm = selecionados_sm.append(self.selecionados)

                        
                        zona_concluida = True
                    else: 
                        raio = raio + zona.RAIO_STEP
                        if raio > zona.RAIO_MAX:
                                
                            self.selecionados['CARTEIRA'] = zona.CARTEIRA
                            if zona.PREENCHER != "":
                         
                                preenchidos = self.preencher_cluster(UTD = zona.UTD, r= raio, n = zona.CLUSTERS,locali = locali, zona = zona_s,
                                municipio = municipio, bairros = bairro, min_selecionados=zona.QTD_MIN,
                                preencher = zona.PREENCHER, local = zona.TIPO_LOCAL, qtd_preencher=qtd_preencher)

                                #self.selecionados = self.selecionados.append(preenchidos)
                                self.selecionados['TURMA'] = zona.TURMA
                                self.selecionados[['cluster']] = self.selecionados[['cluster']].apply(lambda x: x + 1)
                                self.selecionados['cluster_id'] = clusterid + self.selecionados['cluster'].astype(str) 
                                n_selecionados_sm = n_selecionados_sm.append(self.selecionados)
                                clusters_erro = self.selecionados.loc[self.selecionados['SERVICO']==zona.CARTEIRA].groupby(by="cluster_id").size()
                                erro = zona

                                erro['QTD_POR_CLUSTER'] = ",".join(list(map(str,clusters_erro)))  
                                
                                pr = self.selecionados.loc[self.selecionados['SERVICO']==zona.PREENCHER]
                                preenchidos_qtd = pr.groupby(by="cluster_id").size()
                                #clusters_preenchidos= pr['cluster_id'].unique()
                                n_selecionados_sm = n_selecionados_sm.append(self.selecionados)
                                qtd_preen =  list(map(str,preenchidos_qtd.to_list()))
                                id_preen= list(map(str,preenchidos_qtd.index.to_list()))
                                
                                erro['QTD_PREENCHIDA'] = ", ".join([id_preen[i][-1] + ":"+ qtd_preen[i] for i in range(len(id_preen))])
                                erro['QTD_TOTAL'] = self.selecionados.shape[0]
                                erro['PECLD'] = locale.format("%.2f",self.selecionados.PECLD.sum(),grouping=True)
                                erro['DIST'] = ','.join([str(int(self.selecionados.loc[self.selecionados['cluster_id']==i]['dist'].max())) for i in self.selecionados.cluster_id.unique()])
 
                                erro['cluster_id'] = (",".join(list(map(str,clusters_erro.index.to_list()))))
                               
                                
                                erros_sm = erros_sm.append(erro)

                            else:
                                n_selecionados_sm = n_selecionados_sm.append(self.selecionados)
                                erro = zona
                                self.selecionados['TURMA'] = zona.TURMA
                                self.selecionados[['cluster']] = self.selecionados[['cluster']].apply(lambda x: x + 1)
                                self.selecionados['cluster_id'] = clusterid + self.selecionados['cluster'].astype(str) 
                                n_selecionados_sm = n_selecionados_sm.append(self.selecionados)
                                clusters_erro = self.selecionados.groupby(by="cluster_id").size()

                                erro['QTD_POR_CLUSTER'] = ",".join(list(map(str,clusters_erro.to_list())))    
                                erro['QTD_PREENCHIDA'] = ""
                                erro['QTD_TOTAL'] = self.selecionados.shape[0]
                                erro['PECLD'] = locale.format("%.2f",self.selecionados.PECLD.sum(),grouping=True)
                                erro['DIST'] = ','.join([str(int(self.selecionados.loc[self.selecionados['cluster_id']==i]['dist'].max())) for i in self.selecionados.cluster_id.unique()])
                                erro['cluster_id'] = (",".join(list(map(str,clusters_erro.index.to_list()))))
                                erros_sm = erros_sm.append(erro)
                            
                        
                        
                            break   
            except Exception as e:
            
                erro = zona
                erro['QTD_POR_CLUSTER'] = ""
                erro['QTD_TOTAL'] = self.suscetiveis.shape[0]
                erro['QTD_PREENCHIDA'] = ""
                erros_sm = erros_sm.append(erro)
                erros.append(str(e))

        return selecionados_sm,n_selecionados_sm,erros_sm,erros

def testar_selecoes(self, r_lista: list, selecao: object, UTD: str, municipio: str = None, zona: str = None,
                    bairros: list = None, metodo: str = 'nkcnk',
                    peso_mtvcob: float = 1.0,
                    peso_pecld: float = 1.2, 
                    peso_qtftve: float = 0,
                    n: int = 2, k: int = 50,
                    min_selecionados: int = 0,
                    status: object = None):

    self.status_testagem_r_lista.value = """Downloading progress: <progress value="100" max="100" style="width:100%;"></progress>"""
    resultados = []
    style = """ 
            <style>
                .python-iframe > iframe {
                  height:1000px !important;
                }
                table {
                  font-family: arial, sans-serif;
                  border-collapse: collapse;
                  width: 100%;
                }

                td, th {
                  border: 1px solid #dddddd;
                  text-align: center !important;
                  align: center !important; 
                  padding: 8px;
                }

                tr:nth-child(even) {
                  background-color: #dddddd;
                }
            </style>
        """

    tabela_resultados = """<table>
                    <tr>
                        <th>CLUSTER</th>
                        <th>CLIENTES</th>
                        <th>RAIO (m)</th>
                        <th>MTVCOB</th>
                        <th>PECLD CONS</th>
                    </tr>
                  """
    bar = progressbar.ProgressBar(maxval=len(r_lista),
                                  widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
    bar.start()
    for i, r in enumerate(r_lista):
        tabela_resultados += """<tr><td colspan=5, style='background-color:#95a63b;'>
        r = <b>{} METROS</b></td></tr>""".format(r)
        resultado = selecao.selecionar(metodo=metodo, peso_mtvcob=peso_mtvcob, peso_pecld=peso_pecld,peso_qtftve=peso_qtftve,
                                       UTD=UTD, zona=zona, municipio=municipio, bairros=bairros, n=n, k=k, r=r,
                                       min_selecionados=min_selecionados, plot=False)
        mtv_metro_tot = 0
        pecld_metro_tot = 0
        r_tot = 0

        for cluster in resultado:
            if cluster[0] == 'TOTAL':
                tabela_resultados += """
                                        <tr>
                                            <td>{0}</td>
                                            <td>{1} clientes</td>
                                            <td>{2}</td>
                                            <td><strong>{3} ({4}) por metro</strong></td>
                                            <td><strong>{5} ({6} por metro) </strong></td>
                                        </tr>
                                     """.format(cluster[0], cluster[1], cluster[2],
                                                Money(cluster[3], 'BRA').format('es_ES'),
                                                Money(mtv_metro_tot / r_tot, 'BRA').format('es_ES'),
                                                Money(cluster[4], 'BRA').format('es_ES'),
                                                Money(pecld_metro_tot / r_tot, 'BRA').format('es_ES')
                                                )
                                                

            else:
                mtv_metro = round(cluster[3] / cluster[2], 2)
                pecld_metro = round(cluster[4] / cluster[2], 2)

                r_tot += cluster[2]
                pecld_metro_tot += cluster[4]
                mtv_metro_tot += cluster[3]

                tabela_resultados += u"""
                                        <tr>
                                            <td>{0}</td>
                                            <td>{1} clientes</td>
                                            <td>{2} metros </td>
                                            <td>{3} ({4} por metro)</td>
                                            <td>{5} ({6} por metro)</td>
                                        </tr>
                                     """.format(cluster[0],
                                                cluster[1],
                                                cluster[2],
                                                Money(cluster[3], 'BRA').format('es_ES'),
                                                Money(mtv_metro, 'BRA').format('es_ES'),
                                                Money(cluster[4], 'BRA').format('es_ES'),
                                                Money(pecld_metro, 'BRA').format('es_ES')
                                                )
        bar.update(i + 1)
    bar.finish()

    tabela_resultados += "</table>"
    # display(HTML(style + tabela_resultados))
    return style + tabela_resultados

