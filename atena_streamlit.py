# Importação de Bibliotecas e Definição de constantes, pastas, arquivos...
import numpy as np
from pathos.pools import ProcessPool
import os
import streamlit as st
from streamlit_option_menu import option_menu
import warnings
import getpass 
from datetime import datetime
from datetime import date
import time ; from datetime import timedelta
from hdbcli import dbapi
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder
from st_aggrid.shared import GridUpdateMode
from copy import deepcopy

#5C881A -> verde escuro



def calcular_distancia_h(ponto1, ponto2) -> float:
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



def calcular_distancia(ponto1,ponto2)-> float:
        
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
        update_mode=GridUpdateMode.MODEL_CHANGED,
        allow_unsafe_jscode=True,
    )
    return selection

def convert_df(df):
    return df.to_csv(sep=';',decimal=',',index=False).encode('utf-8')
def csv_to_df(df):
    return pd.read_csv(df,sep=';',decimal=',')

def selecionar(UTD: str,locali: list = None,zona: list = None, municipio: list = None, bairros: list = None, metodo: str = 'nkcnk',
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
        nomes_clusters = []
        cores = ['blue', 'red', 'orange', 'green', 'beige', 'white', 'darkgreen', 'darkblue',
             'lighgren', 'lightred']
        for i in range(n):
            nomes_clusters.append("Cluster_"+str(i))
            if i > 9:
                cores.append('blue')
        dfn = st.session_state.selecao_m 
        if not 'IRR' in dfn.columns or calcular_irr == True:
            dfn['irr'] = (peso_mtvcob * dfn['ZCGMTVCOB'] + peso_pecld * dfn['PECLD_CONS']
                               + peso_qtftve * dfn['QTFTVE'])*100
        else: 
            dfn['irr'] = dfn['IRR'].copy()
        if UTD:
            UTD = UTD.upper().replace('_', ' ')

        bairros = bairros
        UTD = UTD
        locali = locali
        zona = zona
        municipio = municipio
        n = n
        r = r
        k = k
        r_max_preciso = r_max_preciso
        
        if zona and zona !="":
            if len(zona) == 1:
                marc_zona = zona[0]
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
            nkcnk(UTD=UTD, locali=locali, zona=zona, municipio=municipio, bairros=bairros, n=n, k=k, r=r,
                       min_selecionados=min_selecionados, r_max_preciso=r_max_preciso, 
                       local=local, fast=False,servico=servico, mista = mista,
                       plot=plot)               
        elif metodo == 'fast nkcnk':
            nkcnk(UTD=UTD, locali=locali,zona=zona, municipio=municipio, bairros=bairros, n=n, k=k, r=r,
                       min_selecionados=min_selecionados, local=local, r_max_preciso=r_max_preciso,
                       fast=True,servico=servico, mista = mista,
                       plot=plot)
        
        st.session_state.centroides = pd.DataFrame()
        st.session_state.centroides['r'] = None

        novas_contas_selecionadas = []
        clusters = []
        """ 
            Correção de seleção: verifica (e corrige em caso positivo) se algum cliente dentro do cluster ficou fora da 
            seleção mesmo que o máximo do cluster não tenha sido atingido ou se algum cliente com maior indíce de 
            recuperação (em relação a algum dos clientes já selecionados) e dentro do raio final ficou de fora.
        """
        suscetiveis = st.session_state.selecao_m 
        selecionados = suscetiveis[suscetiveis.ZCGACCOUN.isin(novas_contas_selecionadas)].copy()
        selecionados['cluster'] = selecionados['cluster'].astype(int)
        recalcular_centroides()
        selecionados['RAIO']= r
        #self.selecionados[['cluster']] = self.selecionados[['cluster']].apply(lambda x: x+1)
    
        selecionados['MARCACAO'] = ""

        for i in range(n):
            #calcula o raio do cluster de acordo com o cliente com maior distância em relação ao centroide
            r_cluster = calcular_distancia(
                selecionados.loc[selecionados['cluster'] == i][['LATITUDE', 'LONGITUDE']],
                st.session_state.centroides.iloc[i][['LATITUDE', 'LONGITUDE']]
            ).max()
            st.session_state.centroides.loc[i, 'r'] = r_cluster
            """-----> Atualização do cluster: 
                     A partir do centroide, busca-se todos os clientes que estão dentro do raio e que não foram 
                     selecionados ainda por outro cluster e seleciona-se os k clientes com maior indice de recuperação
            """
            suscetiveis['dist'] = calcular_distancia(
                st.session_state.centroides.iloc[i][['LATITUDE', 'LONGITUDE']],
                suscetiveis[['LATITUDE', 'LONGITUDE']])

            contas_selecionadas = selecionados[selecionados.cluster != i]['ZCGACCOUN'].tolist()
            
            # Define o raio máximo da última etapa de seleção do cluster
            r_max = r if r_max_preciso == True else r_cluster 

            # Que não pertenciam a outro na seleção anterior cluster e que ainda não foram selecionados na atual
            novas_contas_selecionadas_cluster = suscetiveis[
                (~suscetiveis.ZCGACCOUN.isin(contas_selecionadas))&
                (~suscetiveis.ZCGACCOUN.isin(novas_contas_selecionadas))&
                (suscetiveis.dist <= r_max)
            ].sort_values('irr', ascending=False)[:k]['ZCGACCOUN'].tolist()

            suscetiveis.loc[suscetiveis.ZCGACCOUN.isin(novas_contas_selecionadas_cluster), 'cluster'] = int(i)
            novas_contas_selecionadas += novas_contas_selecionadas_cluster
            clusters += [i]*len(novas_contas_selecionadas_cluster)
            """<-----"""

        
        
        for i in selecionados.cluster.unique():
            m_a = m_a + 1
            selecionados.loc[selecionados['cluster'] == i,'MARCACAO'] = m_a
            selecionados.loc[selecionados['cluster'] == i,'MARC_ZONA'] = marc_zona
          
        if plot:
            printar_resultados()
            return plotar()
        else:
            return resultados()

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

        ucs = dfn.copy()
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
        suscetiveis = ucs.copy()
        
       
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
          
                ucs['raio'] = calcular_distancia(cc[['LATITUDE', 'LONGITUDE']],
                                                              ucs[['LATITUDE', 'LONGITUDE']])
                
                selecionados_aux = ucs.loc[ucs['raio'] <= r].sort_values('irr', ascending=False)[:k]
                ucs['raio'] = calcular_distancia(selecionados_aux[['LATITUDE', 'LONGITUDE']].mean(),
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

        selecionados = dfn[dfn.ZCGACCOUN.isin(accoun_selecionadas)].copy()
     
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
 
        
        selecionados = selecionados

        centroides = centroides
        st.session_state.centroides = centroides
       
        recalcular_centroides()



def multiprocess_zonas(zonas,metodo,calcular_irr,r_max_preciso,mista):
        selecionados_sm = pd.DataFrame()
        n_selecionados_sm = pd.DataFrame()
        erros_sm = pd.DataFrame()
        erros = []
        zonas = st.session_state.conf
        for i, zona in zonas.loc[zonas['SELECIONAR']=="SIM"].iterrows(): 
            #try:
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

                selecionar(metodo=metodo, 
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

                resultado = selecionados.copy()
            
                #if resultado.shape[0] >= zona.QTD_MIN*zona.CLUSTERS:
                if selecionados.groupby(by="cluster").count()['ZCGACCOUN'].min() >= zona.QTD_MIN:
                    
                    selecionados['CARTEIRA'] = zona.CARTEIRA
                    
                    
                    if zona.PREENCHER !="" and qtd_preencher >0:
                        preenchidos = preencher_cluster(UTD = zona.UTD, r= zona.RAIO_MAX, n = zona.CLUSTERS,locali = locali, zona = zona_s,
                        municipio = municipio, bairros = bairro, min_selecionados=zona.QTD_MIN,
                        preencher = zona.PREENCHER, local = zona.TIPO_LOCAL, qtd_preencher=qtd_preencher)
                        
                        #self.selecionados = self.selecionados.append(preenchidos)
                        selecionados['TURMA'] = zona.TURMA
                        #self.selecionados[['cluster']] = self.selecionados[['cluster']].apply(lambda x: x + 1)
                        #self.selecionados['cluster_id'] = clusterid + self.selecionados['cluster'].astype(str) 

                        selecionados[['cluster']] = self.selecionados[['cluster']].apply(lambda x: x + 1)
                        selecionados['cluster_id'] = clusterid  + self.selecionados['cluster'].astype(str)
                        selecionados_sm = selecionados_sm.append(self.selecionados) 
                        

                    else:
                        selecionados['TURMA'] = zona.TURMA
                        selecionados[['cluster']] = selecionados[['cluster']].apply(lambda x: x + 1)
                        selecionados['cluster_id'] = clusterid  + selecionados['cluster'].astype(str) 
                        selecionados_sm = selecionados_sm.append(selecionados)

                    
                    zona_concluida = True
                else: 
                    raio = raio + zona.RAIO_STEP
                    if raio > zona.RAIO_MAX:
                            
                        selecionados['CARTEIRA'] = zona.CARTEIRA
                        if zona.PREENCHER != "":
                        
                            preenchidos = preencher_cluster(UTD = zona.UTD, r= raio, n = zona.CLUSTERS,locali = locali, zona = zona_s,
                            municipio = municipio, bairros = bairro, min_selecionados=zona.QTD_MIN,
                            preencher = zona.PREENCHER, local = zona.TIPO_LOCAL, qtd_preencher=qtd_preencher)

                            #self.selecionados = self.selecionados.append(preenchidos)
                            selecionados['TURMA'] = zona.TURMA
                            selecionados[['cluster']] = selecionados[['cluster']].apply(lambda x: x + 1)
                            selecionados['cluster_id'] = clusterid + selecionados['cluster'].astype(str) 
                            n_selecionados_sm = n_selecionados_sm.append(selecionados)
                            clusters_erro = selecionados.loc[selecionados['SERVICO']==zona.CARTEIRA].groupby(by="cluster_id").size()
                            erro = zona

                            erro['QTD_POR_CLUSTER'] = ",".join(list(map(str,clusters_erro)))  
                            
                            pr = selecionados.loc[selecionados['SERVICO']==zona.PREENCHER]
                            preenchidos_qtd = pr.groupby(by="cluster_id").size()
                            #clusters_preenchidos= pr['cluster_id'].unique()
                            n_selecionados_sm = n_selecionados_sm.append(self.selecionados)
                            qtd_preen =  list(map(str,preenchidos_qtd.to_list()))
                            id_preen= list(map(str,preenchidos_qtd.index.to_list()))
                            
                            erro['QTD_PREENCHIDA'] = ", ".join([id_preen[i][-1] + ":"+ qtd_preen[i] for i in range(len(id_preen))])
                            erro['QTD_TOTAL'] = selecionados.shape[0]
                            erro['PECLD'] = locale.format("%.2f",selecionados.PECLD.sum(),grouping=True)
                            erro['DIST'] = ','.join([str(int(selecionados.loc[selecionados['cluster_id']==i]['dist'].max())) for i in self.selecionados.cluster_id.unique()])

                            erro['cluster_id'] = (",".join(list(map(str,clusters_erro.index.to_list()))))
                            
                            
                            erros_sm = erros_sm.append(erro)

                        else:
                            n_selecionados_sm = n_selecionados_sm.append(selecionados)
                            erro = zona
                            selecionados['TURMA'] = zona.TURMA
                            selecionados[['cluster']] = selecionados[['cluster']].apply(lambda x: x + 1)
                            selecionados['cluster_id'] = clusterid + selecionados['cluster'].astype(str) 
                            n_selecionados_sm = n_selecionados_sm.append(selecionados)
                            clusters_erro = selecionados.groupby(by="cluster_id").size()

                            erro['QTD_POR_CLUSTER'] = ",".join(list(map(str,clusters_erro.to_list())))    
                            erro['QTD_PREENCHIDA'] = ""
                            erro['QTD_TOTAL'] = selecionados.shape[0]
                            erro['PECLD'] = locale.format("%.2f",self.selecionados.PECLD.sum(),grouping=True)
                            erro['DIST'] = ','.join([str(int(self.selecionados.loc[selecionados['cluster_id']==i]['dist'].max())) for i in self.selecionados.cluster_id.unique()])
                            erro['cluster_id'] = (",".join(list(map(str,clusters_erro.index.to_list()))))
                            erros_sm = erros_sm.append(erro)
                            
                        
                        
                            #break   
            #except Exception as e:
            
                #erro = zona
                #erro['QTD_POR_CLUSTER'] = ""
                #erro['QTD_TOTAL'] = suscetiveis.shape[0]
                #erro['QTD_PREENCHIDA'] = ""
                #erros_sm = erros_sm.append(erro)
                #erros.append(str(e))

        return selecionados_sm,n_selecionados_sm,erros_sm,erros

tabelasuscetiveis = 'SuscetiveisTabela'
today = date.today()
delta = 1 ; next_day = today + timedelta(delta) # D + 1
path_config = 'sources/Sqls/ImportacaoConfiguracao.sql'
lista_carteiras = ['CONVENCIONAL','DISJUNTOR','RECORTE','RECORTE_BAIXA','BAIXA MIX','MISTA']

# Deixa a página ocupando todo o espaço da tela
#st.set_page_config(layout="wide")
# Logo da Coelba no topo do sidebar
st.sidebar.image('logo_1.png')
st.markdown("<h2 style='text-align: center; color: #5C881A;'>ATENA - Neoenergia Coelba</h1>", unsafe_allow_html=True)
#st.markdown('## ATENA - Neoenergia Coelba')
st.markdown("<h3 font-style: italic; style='text-align: center; color: #5C881A;'><em>Ferrramenta de Seleção Estratégica de Serviços de Cobrança</em></h1>", unsafe_allow_html=True)
#st.markdown('#### *Ferrramenta de Seleção Estratégica de Serviços de Cobrança*')

if 'pagina' not in st.session_state:
    st.session_state.pagina = "Login"

if 'check_login' not in st.session_state:
    st.session_state.check_login = 0
    
if 'check_consulta' not in st.session_state:
    st.session_state.check_consulta = 0

if 'check_configuracoes' not in st.session_state:
    st.session_state.check_configuracoes = 0


with st.sidebar: # Menu lateral
    # Icons: home check-square scissors
    st.session_state.pagina = option_menu("MENU", ["Login", "Configurações", "Seleção", "Mapa", "Dashboard","Sobre"],
                        icons=['person', 'gear','coin', 'geo-alt','graph-up','info-circle'],
                        menu_icon="list", default_index=0,
                        styles={
        "container": {"padding": "5!important", "background-color": "#f0f2f6"},
        "icon": {"color": "#7F7F7F", "font-size": "25px"}, 
        "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#93ac46"},
        "nav-link-selected": {"background-color": "#93ac46"},
    }
    )   

def testar_login():
    try:
        connection_hana = dbapi.connect(address='BRNEO695',port='30015',user=st.session_state.usuario,password=st.session_state.senha,databasename='BNP',sslValidateCertificate=True)
        st.success('USUÁRIO LOGADO COM SUCESSO!')
        st.session_state.check_login = 1
    except Exception as e:
        st.session_state.check_login = 0
        st.error("ERRO NA CONEXÃO COM O SAP HANA")
if st.session_state.pagina == 'Login':
    st.markdown("<h3 style='text-align: center; color: #5C881A;'>LOGIN - SAP HANA</h1>", unsafe_allow_html=True)
    #st.markdown('#### LOGIN - SAP HANA')
    st.markdown("***")
    with st.form(key = "form_login"):
        st.session_state.usuario = st.text_input("Usuário", help='Usuário do SAP HANA')
        st.session_state.senha = st.text_input("Senha", type="password", help='Senha do SAP HANA')
        submit = st.form_submit_button(label = "Acessar")
        if submit:
            testar_login()
            

def importar_clusterconf():   
    sql_conf = open(path_config, encoding="utf-8")  
    sql_conf = sql_conf.read()
    sql_conf = sql_conf.format(cart=st.session_state.carteira_consultar, data = str(st.session_state.data_pedido_consultar),turma = st.session_state.turma_consultar)
    carteira = st.session_state.turma_consultar + "_" + st.session_state.carteira_consultar

    try:
        connection_hana = dbapi.connect(address='BRNEO695',port='30015',user=st.session_state.usuario,password=st.session_state.senha,databasename='BNP',sslValidateCertificate=True)
        conf = pd.read_sql(sql_conf, connection_hana)
        conf['PESO_MTVCOB'] = 1
        conf['PESO_PECLD'] = 2
        conf['PESO_QTDFTVE']= 0
        conf['SELECIONAR'] = 'SIM'
        conf['MUNICIPIO'] = ""
        conf['LOCALI'] = ""
        conf['BAIRRO'] = ""
        conf['TIPO_LOCAL'] = ""
        conf = conf[['UTD','SELECIONAR','ZONA','LOCALI','MUNICIPIO','BAIRRO','TIPO_LOCAL','CLUSTERS','QTD_MAX','QTD_MIN','RAIO_IDEAL','RAIO_MAX','RAIO_STEP','CARTEIRA','TURMA','PESO_MTVCOB','PESO_PECLD','PESO_QTDFTVE','PREENCHER','QTD_PREENCHER']]
        conf['QTD_PREENCHER'].replace(to_replace= 0,value = "",inplace=True)
        conf = conf[conf['CLUSTERS'] != 0]
        conf = conf[conf['QTD_MIN'] != 0]
        st.session_state.conf = conf.copy()
        #conf.to_excel('Configuracoes/'+'CONFIGURACAO_'+str(carteira)+'.xlsx',index=False)
        #conf.to_csv('Configuracoes/' + 'CONFIGURACAO_'+str(carteira)+'.csv',index=False,sep=';',decimal=',')
        
        #resultado_conf = """<a href='Configuracoes/{val}.xlsx' target='_blank'>Arquivo de Configuração xlsx</a><br>
    #""".format(val='CONFIGURACAO_'+str(carteira))
        #resultado_conf_csv = """<a href='Configuracoes/{val}.csv' target='_blank'>Arquivo de Configuração csv</a><br>
    #""".format(val='CONFIGURACAO_'+str(carteira))
        connection_hana.close()  
        st.session_state.check_configuracoes = 1

    except Exception as e:
        st.write("ERRO NA CONEXÃO COM O SAP HANA")




if st.session_state.pagina == "Configurações" and st.session_state.check_login == 1:
    st.markdown("<h3 style='text-align: center; color: #5C881A;'>CONFIGURAÇÃO - CLUSTERS</h1>", unsafe_allow_html=True)
    #st.markdown('#### CONFIGURAÇÃO - CLUSTERS')
    st.markdown("***")
    st.session_state.opcao_configuracao = st.selectbox('Selecione a fonte das configurações', ['IMPORTAR_MAPA','ARQUIVO_CSV'])
    st.markdown("***")
    if st.session_state.opcao_configuracao == "IMPORTAR_MAPA":
        with st.form(key = "form_configuracoes"):
            st.session_state.turma_consultar = st.selectbox('Turma:', ['STC', 'EPS'])
            st.session_state.carteira_consultar = st.selectbox('Selecione Carteira:', lista_carteiras)
            st.session_state.data_pedido_consultar = st.date_input('Data do pedido:',value = next_day)
            submit = st.form_submit_button(label = "Importar Configurações (Mapa de Seleção)")
            if submit:
                importar_clusterconf()
                

        if st.session_state.check_configuracoes == 1:  
            st.success('Foram importadas {linhas} linhas de configuração'.format(linhas = st.session_state.conf.shape[0]))
            st.markdown("***")  
            st.markdown("<h5 style='text-align: left; color: #5C881A;'>BAIXAR CONFIGURAÇÕES:</h1>", unsafe_allow_html=True)
            #st.markdown('#### BAIXAR CONFIGURAÇÕES:')
            st.session_state.conf_csv = convert_df(st.session_state.conf)
            st.download_button(label="Baixar configurações (csv)",data=st.session_state.conf_csv,file_name='Configuracao_Clusters.csv',mime='text/csv',)
            st.markdown("***")  
            st.markdown("<h5 style='text-align: left; color: #5C881A;'>MAPA (TABELA):</h1>", unsafe_allow_html=True)
            #st.markdown('#### MAPA (TABELA):')
            selection = aggrid_interactive_table(df=st.session_state.conf)
    elif st.session_state.opcao_configuracao == "ARQUIVO_CSV":
        uploadedFile = st.file_uploader("Importar Configurações", type=['csv'],accept_multiple_files=False,key="fileUploader")
        if 'uploadedFile' not in st.session_state:
            if uploadedFile is not None:
                st.session_state.conf = csv_to_df(uploadedFile) 
            
                st.session_state.check_configuracoes = 1
                if st.session_state.check_configuracoes == 1:  
                    st.markdown("***")  
                    st.markdown("<h5 style='text-align: left; color: #5C881A;'>MAPA (TABELA):</h1>", unsafe_allow_html=True)
                    #st.markdown('#### MAPA (TABELA):')
                    selection = aggrid_interactive_table(df=st.session_state.conf)
    

elif st.session_state.pagina == "Configurações" and st.session_state.check_login == 0:
    st.error("NECESSÁRIO EFETUAR LOGIN")

if st.session_state.pagina == "Mapa":
    uploadedFile = st.file_uploader("Importar Configurações", type=['csv'],accept_multiple_files=False,key="fileUploader")
    if uploadedFile is not None:
        st.session_state.conf = csv_to_df(uploadedFile) 
        selection = aggrid_interactive_table(df=st.session_state.conf)

def salvar_dados_consulta_e_realizar_consulta():
    if st.session_state.onde_consultar == 'Tabela Suscetiveis':
        nome_consulta = st.session_state.turma_consultar + "_" + st.session_state.carteira_consultar
        list_confg = ['sources/Sqls/'+tabelasuscetiveis+'.sql',st.session_state.carteira_consultar,st.session_state.data_pedido_consultar,st.session_state.turma_consultar]
        connection_hana = dbapi.connect(address='BRNEO695',port='30015',user=st.session_state.usuario,password=st.session_state.senha,databasename='BNP',sslValidateCertificate=True)
        arquivo_sql_susceptiveis_convencionais = open(list_confg[0], encoding="utf-8")
        sql_susceptiveis_convencionais = arquivo_sql_susceptiveis_convencionais.read()
        arquivo_sql_susceptiveis_convencionais.close()
        
        if len(list_confg)>1:
            sql_susceptiveis_convencionais = sql_susceptiveis_convencionais.format(carteira = list_confg[1],data_pedido = list_confg[2],turma =list_confg[3])
            #st.write(sql_susceptiveis_convencionais)
        df = pd.read_sql(sql_susceptiveis_convencionais, connection_hana)
        #st.table(df)
        df.columns = df.columns.str.replace(" ", '')

        df[['LATITUDE', 'LONGITUDE']] = df[['LATITUDE', 'LONGITUDE']].replace(regex=',', value='.')
        df[['LATITUDE', 'LONGITUDE']] = df[['LATITUDE', 'LONGITUDE']].replace(regex=' ', value='')
        df[['LATITUDE', 'LONGITUDE']] = df[['LATITUDE', 'LONGITUDE']].replace(to_replace='?', value=None)
        df[['LATITUDE', 'LONGITUDE']] = df[['LATITUDE', 'LONGITUDE']].astype(float)
        df['ZONA'] = df['ZONA'].astype(str)

        df = df.replace(regex='^ +| +$', value='')

        # normalização
        df = df.rename(columns={"ZCGQTFTVE": "QTFTVE"})
        cols_norm = ['ZCGMTVCOB', 'PECLD_CONS', 'QTFTVE']
        dfn = df.copy()
        dfn[cols_norm] = ((df[cols_norm] - df[cols_norm].min()) /
                          (df[cols_norm].max() - df[cols_norm].min()))
        
        dfn[['MTV_COB', 'PECLD','ZCGQTFTVE']] = df[['ZCGMTVCOB', 'PECLD_CONS','QTFTVE']].copy()
        
        dfn = dfn.drop_duplicates(subset =['ZCGACCOUN'])
        st.session_state.selecao_m =  deepcopy(dfn)
        st.session_state.quatidade_suscetiveis = len(dfn.index)
        #st.table(dfn)
        st.session_state.check_consulta = 1
    


def realizar_selecao_massiva():    
        #try: 
        #self.set_metodo_sm(self.metodo_sm_text) -> st.session_state.metodo_selecao_massiva
        #self.set_calcular_irr_sm(self.calcular_irr_sm_text) -> DESCONSIDERADO
        #self.set_r_max_preciso_sm(self.r_max_preciso_sm_text) -> DESCONSIDERADO
        #self.set_importar_conf_sm(self.importar_conf_sm_text) -> DESCONSIDERADO
        #self.set_plotar_clusters_sm(self.plotar_clusters_sm_text) -> DESCONSIDERADO
        #self.set_multiprocess_sm(self.multiprocess_sm_text) -> st.session_state.metodo_processamento_selecao_massiva !!!! alterado para sim e não
        
        #!!!!!!!!!!!!
        #self.html_tabela_resultados_sm.value = """"""
        #self.html_link_selecao_massiva_erros.value = """"""
        #self.html_link_selecao_massiva_mapa.value = """"""
        #self.html_link_selecao_massiva_csv.value = """"""

        n_processos = os.cpu_count()
        nome_selecao = st.session_state.nome_arquivo_saida
        #self.botao_sm_arquivo._counter = 0 -> DESCONSIDERADO


        #st.session_state.selecionados_sm = pd.DataFrame()
        #st.session_state.n_selecionados_sm = pd.DataFrame()
        #st.session_state.erros_sm = pd.DataFrame()
        #self.selecionados_sm = pd.DataFrame()
        #self.n_selecionados_sm = pd.DataFrame()
        #self.erros_sm = pd.DataFrame()

        zonas_sm = st.session_state.conf
            #try: 
        for i in zonas_sm.CARTEIRA.unique():
            selecionados_sm = pd.DataFrame()
            n_selecionados_sm = pd.DataFrame()

            if st.session_state.metodo_processamento_selecao_massiva == "SIM":
                #MULTIPROCESSAMENTO:
                metodo = []
                calcularirr = []
                r_max_preciso = []

                #CASO O ARQUIVO DE CONFG TENHA MENOS QUE 5 LINHAS SERÁ UTILIZADA O NÚMERO DE LINHAS PARA A POOL DE PROCESSOS.

                if n_processos > len(zonas_sm.index):      
                    n_processos = len(zonas_sm.index)

                p = ProcessPool(n_processos)
            
                divididos = np.array_split(zonas_sm.loc[zonas_sm['CARTEIRA']==i].sample(frac=1),n_processos)
                metodo = [st.session_state.metodo_selecao_massiva]*n_processos
                calcularirr = [0]*n_processos
                r_max_preciso = [1]*n_processos
                mista = [0]*n_processos
                #zonas = st.session_state.selecao_m
                zonas = st.session_state.conf
                res = list(p.imap(multiprocess_zonas(st.session_state.conf,metodo = metodo, calcular_irr = calcularirr,r_max_preciso = r_max_preciso, mista = mista ), divididos,metodo,calcularirr,r_max_preciso,mista))

                for i in range(len(res)):
                    selecionados_sm = selecionados_sm.append(res[i][0])
                    n_selecionados_sm = n_selecionados_sm.append(res[i][1])

            
                    erros_sm = erros_sm.append(res[i][2])

                    if selecionados_sm.shape[0] > 0:  
                        for j in selecionados_sm.MARCACAO.unique():
                            marc_iter = marc_iter + 1
                            selecionados_sm.loc[selecionados_sm['MARCACAO'] == j,'MARCACAO'] = selecionados_sm.loc[selecionados_sm['MARCACAO']==j]['MARC_ZONA'] + str(marc_iter).zfill(4)

                    if n_selecionados_sm.shape[0] >0: 
                        for j in n_selecionados_sm.MARCACAO.unique():
                            marc_iter = marc_iter + 1
                            n_selecionados_sm.loc[n_selecionados_sm['MARCACAO'] == j,'MARCACAO'] = n_selecionados_sm.loc[n_selecionados_sm['MARCACAO']==j]['MARC_ZONA'] + str(marc_iter).zfill(4) 

            
                teste = res    
            else:   
                selecionados_sm,n_selecionados_sm,erros_sm, erro = selecao.multiprocess_zonas(zonas_sm,metodo_sm,calcular_irr_sm,r_max_preciso_sm,mista)
                erros_sm = erros_sm.append(erros_sm)

                if selecionados_sm.shape[0] > 0:  
                    for j in selecionados_sm.MARCACAO.unique():
                        marc_iter = marc_iter + 1
                        selecionados_sm.loc[selecionados_sm['MARCACAO'] == j,'MARCACAO'] = selecionados_sm.loc[selecionados_sm['MARCACAO']==j]['MARC_ZONA'] + str(marc_iter).zfill(4)

                if n_selecionados_sm.shape[0] >0: 
                    for j in n_selecionados_sm.MARCACAO.unique():
                        marc_iter = marc_iter + 1
                        n_selecionados_sm.loc[n_selecionados_sm['MARCACAO'] == j,'MARCACAO'] = n_selecionados_sm.loc[n_selecionados_sm['MARCACAO']==j]['MARC_ZONA'] + str(marc_iter).zfill(4) 


            
            
            selecionados_sm = selecionados_sm.append(selecionados_sm)
            n_selecionados_sm = n_selecionados_sm.append(n_selecionados_sm)
            


        if erros_sm.shape[0] > 0:
            if 'cluster_id' in erros_sm.columns:
                erros_sm = erros_sm [['PESO_MTVCOB','PESO_PECLD','PESO_QTDFTVE','LOCALI','MUNICIPIO','BAIRRO','TIPO_LOCAL','SELECIONAR','UTD','ZONA','RAIO_IDEAL','RAIO_MAX','RAIO_STEP','CARTEIRA','TURMA','PREENCHER','QTD_PREENCHER','CLUSTERS','QTD_MAX','QTD_MIN','QTD_POR_CLUSTER','QTD_PREENCHIDA','QTD_TOTAL','PECLD','DIST','cluster_id']]
            else:
                erros_sm = erros_sm [['UTD','SELECIONAR','ZONA','LOCALI','MUNICIPIO','BAIRRO','TIPO_LOCAL','RAIO_IDEAL','RAIO_MAX','RAIO_STEP','CLUSTERS','QTD_MAX','QTD_MIN','PESO_MTVCOB','PESO_PECLD','PESO_QTDFTVE','CARTEIRA','TURMA','PREENCHER','QTD_PREENCHER']]
        #if  selecionados_sm.shape[0]> 0:
            #self.selecionados_sm = self.selecionados_sm.drop(columns=['MARC_ZONA']) 


            #selecionados_sm.to_excel('resultados/'+nome_selecao+'.xlsx', index=False)
            

            #add_cliente_clusterid_sm.options = selecionados_sm['cluster_id'].unique().tolist() + ["Nenhum"]
            #att_consulta_cluster_hist()
            #arquivo_hana.value = nome_selecao + ".xlsx"

        #if erros_sm.shape[0] > 0:
            #if 'MARC_ZONA' in self.n_selecionados_sm:
                #self.n_selecionados_sm = self.n_selecionados_sm.drop(columns=['MARC_ZONA'])  

            # erros_sm.to_excel('resultados/erros_selecao_'+self.nome_selecao+'.xlsx', index=False) 
            
        #try:
            #if plotar_clusters:
                #plotar_resultados_sm()
            #tabela_resultado_sm()
        #except Exception as e: 
            #html_tabela_resultados_sm.value = """<label class="status-label error-label">Não foi possível selecionar nenhum cliente {e}.</label>""".format(e = e)
    
        if selecionados_sm.shape[0] > 0:
            clientes = selecionados_sm.shape[0]
            mtv = locale.format("%.2f",round(self.selecionados_sm.MTV_COB.sum(),2),grouping = True)
            pecld = locale.format("%.2f",round(self.selecionados_sm.PECLD.sum(),2),grouping = True)
            zonas =  selecionados_sm['ZONA'].nunique()
        else:
            clientes = 0
            mtv = 0
            pecld = 0
            zonas = 0
            
        n_selecionadas = erros_sm.shape[0]

        st.write(clientes)
        st.write(pecld)
        
        #except Exception as e:
            #st.error("Ocorreu um erro: ", e)
        #except Exception as e:
            #st.error("ERRO")




if st.session_state.pagina == "Seleção" and st.session_state.check_login == 1 and st.session_state.check_configuracoes == 1:
    st.markdown("<h3 style='text-align: center; color: #5C881A;'>CONSULTA SUSCETÍVEIS E SELEÇÃO DE SERVIÇOS</h1>", unsafe_allow_html=True)
    #st.markdown('#### CONSULTA DE CONTAS SUSCETÍVEIS')
    st.markdown("***")
    #coluna1, coluna2 = st.columns([80,20])
    #with coluna1:
    with st.form(key = "form_consulta"):
        st.session_state.onde_consultar = st.selectbox('Onde Consultar:', ['Tabela Suscetiveis', 'Arquivo SQL'],disabled=True) #consulta
        st.text_input('Turma:',value=st.session_state.turma_consultar,disabled=True) #turma
        st.text_input('Carteira:',value=st.session_state.carteira_consultar,disabled=True) #carteira_sql
        st.date_input('Data do pedido:',value=st.session_state.data_pedido_consultar,disabled=True) #data_pedido
        submit = st.form_submit_button(label = "Realizar a Consulta")
        if submit:
            salvar_dados_consulta_e_realizar_consulta()
            
    if st.session_state.check_consulta == 1:
        st.markdown("***")
        st.markdown("<h5 style='text-align: left; color: #5C881A;'>RESULTADO CONSULTA:</h1>", unsafe_allow_html=True)
        #st.markdown('#### RESULTADO CONSULTA:')
        col1, col2 = st.columns(2)
        with col1:
            st.text_input('Nome Consulta:',value=st.session_state.turma_consultar + "_" + st.session_state.carteira_consultar,disabled=True)
        with col2:
            st.text_input('Quantidade de Suscetíveis:',value=st.session_state.quatidade_suscetiveis,disabled=True)
        #with coluna2:
            #st.markdown("<h3 style='text-align: center; color: black;'>PROGRESSO SELEÇÃO</h1>", unsafe_allow_html=True)
            #st.checkbox("STC CONVENCIONAL")
        st.markdown("***")
        st.markdown("<h5 style='text-align: left; color: #5C881A;'>SELEÇÃO MASSIVA:</h1>", unsafe_allow_html=True)
        with st.form(key = "form_selecao"):
            coluna1, coluna2 = st.columns(2)
            with coluna1:
                st.session_state.metodo_selecao_massiva = st.selectbox('Método de Seleção:', ['fast nkcnk', 'nkcnk']) #metodo_sm
                st.session_state.metodo_processamento_selecao_massiva = st.selectbox('Utilizar Multiprocessamento:', ['SIM', 'NÃO'])
                st.session_state.destaque_mtvcob = st.number_input("Destaque MTVCOB:", value=10000, step=1, disabled=False)
            with coluna2:
                st.session_state.nome_arquivo_saida = st.text_input('Nome Arquivo de Saída:',value=st.session_state.turma_consultar + "_" + st.session_state.carteira_consultar+ "_" +str(st.session_state.data_pedido_consultar),disabled=False)
                st.session_state.destaque_pecld = st.number_input("Destaque PECLD:", value=4000, step=1, disabled=False)
                st.session_state.destaque_qtdtve = st.number_input("Destaque QTFTVE:", value=1, step=1, disabled=False)
            submit = st.form_submit_button(label = "Realizar Seleção Massiva")
            if submit:
                st.write(st.session_state.conf)
                realizar_selecao_massiva()
                st.write("ok")
            #salvar_dados_consulta_e_realizar_consulta()
        
            #st.table(st.session_state.dfn)
elif st.session_state.pagina == "Seleção" and st.session_state.check_login == 0:
    st.error("NECESSÁRIO EFETUAR LOGIN")
elif st.session_state.pagina == "Seleção" and st.session_state.check_configuracoes == 0:
    st.error("NECESSÁRIO DEFINIR A CONFIGURAÇÃO DAS TURMAS E CARTEIRA")










        
 




if st.session_state.pagina == "Sobre":
    
    st.markdown('#### DESCRIÇÃO DA FERRAMENTA')
    st.markdown("***")
    st.markdown('#### Objetivo')
    '''
    - A ferramenta tem como objetivo realizar a seleção de serviços de cobrança de forma automática e inteligente utlizando...
    '''
    st.markdown('#### Login')
    '''
    - O usuário deve inserir o seu login e senha de acesso ao SAP HANA.
    - Através do login e senha informados é realizada uma tentativa de conexão com o SAP HANA, caso a tentativa de conexão tenha êxito o usuário tem acesso as demais abas da ferramenta.
    '''
    st.markdown('#### Configurações')
    '''
    - Nesta etapa deve ser definido qual a fonte para realizar a seleção dos serviços (UTDs, zonas, turmas, quantidade de notas), as opções disponíveis são:
        - Utilizar o mapa de seleção onde estão dispostos a quantidade de serviços a serem gerados informados pelos focais.
        - Inserir um arquivo csv com as informações dos serviços que devem ser selecionados. 
    '''
    st.markdown('#### Seleção')
    '''
    - Nesta etapa o usuário deve realizar a consulta das contas suscetiveis para todas as carteiras que serão geradas, seguindo a ordem de prioridade:
    - STC CONVENCIONAL -> STC RECORTE -> STC MIX -> EPS CONVENCIONAL
    '''
    

    #atena = SelecaoLayout(st.session_state.usuario, st.session_state.senha)
    #st.write(atena)
    #st.text("Acessou")
    #st.write(st.session_state.usuario)

#apagar
#st.markdown('# Título *Secundário*')
# Tudo que estiver entre 3 aspas é lido como linguagem markdown
#'''

#- lista de itens
#- lista de itens

#'''
#apagar





#inserir um dropdown...
#lista_utds = ['ILHEUS','ITABUNA','TEIXEIRA DE FREITAS','EUNÁPOLIS']
#var = st.selectbox('Selecione uma variável', lista_utds)
#var2 = st.sidebar.selectbox('Selecione uma variável', lista_utds)

# obter os dados com o pandas de um csv
# Inserir uma tabela com a média de salário por categoria...
#dados = pd.read_csv('prof-dados-resumido.csv')
#st.write(dados)
#ms = dados['Salário'].groupby(dados[var]).mean()
#st.write(ms)

# Mostrar os dados em tabela:
#st.table(ms)

# Gráfico de barras
#plot = dados['Profissão'].value_counts().plot(kind = 'bar')
#st.pyplot(plot.figure)

# Botão: Guarda valor true ou false
#st.button(label = '-> CLique aqui! <-', help='É só clicar ali')
#if(st.button("About")):
# Botão de Rádio: Guarda o item do botão selecionado index é a escolha default
#st.radio('Botões de Rádio', options = [100, 'Python', [1,2,3]], index = 1, help='Ajuda')
# Caixas de Seleção Múltipla: Guarda a lista de itens selecionados
#st.multiselect('Selecione quantas opções desejar', options = ['A','B','C'])


