from sources.interface_selecao_cortes_streamlit import *

#5C881A -> verde escuro

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
        update_mode=GridUpdateMode.MODEL_CHANGED,
        allow_unsafe_jscode=True,
    )
    return selection

def convert_df(df):
    return df.to_csv(sep=';',decimal=',',index=False).encode('utf-8')
def csv_to_df(df):
    return pd.read_csv(df,sep=';',decimal=',')
 
 
today = date.today()
delta = 1 ; next_day = today + timedelta(delta) # D + 1
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
    if st.session_state.check_login == 1:
        st.write(st.session_state.usuario, st.session_state.senha)
        st.session_state.objeto_atena = SelecaoLayout(usuario = st.session_state.usuario, senha = st.session_state.senha)
    
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
            st.session_state.objeto_atena = SelecaoLayout(usuario = st.session_state.usuario, senha = st.session_state.senha)
            
            



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
                #st.session_state.objeto_atena = SelecaoLayout(usuario = st.session_state.usuario, senha = st.session_state.senha)
                st.session_state.objeto_atena.importar_clusterconf(b=1)
                

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
        #cl1,cl2,cl3,cl4,cl5 = st.columns(5)
        #with cl1:
            #st.session_state.peso_mtvcob = st.number_input("Peso MTVCOB:", value=1, step=1, disabled=False)
        #with cl2:
            #st.session_state.peso_pecld = st.number_input("Peso PECLD:", value=2, step=1, disabled=False)
        #with cl3:
            #st.session_state.peso_pecld = st.number_input("Peso QTDFTVE:", value=0, step=1, disabled=False)
        #with cl4:
            #st.write("")
        #with cl4:
            #st.write("")
        submit = st.form_submit_button(label = "Realizar a Consulta")
        if submit:
            st.session_state.objeto_atena.consulta_selecao(b=1,usuario = st.session_state.usuario, senha = st.session_state.senha)
            #salvar_dados_consulta_e_realizar_consulta()
            
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
                #st.write(st.session_state.conf)
                st.session_state.objeto_atena.realizar_selecao_massiva( b = 1)
                 
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


