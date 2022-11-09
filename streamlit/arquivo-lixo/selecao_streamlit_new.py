#Importa a pasta com as configurações (bibliotecas, funções, variáveis) da ferramenta
from sources.bibliotecas_funcoes import *


menu_data_2 = [
    {'label':"LOGIN",'icon': 'bi bi-person'},
    #{'label':"CONSULTAS SQL",'icon': 'bi bi-search','submenu':[{'label':"CONSULTA CONTA CONTRATO", 'icon': "bi bi-bookmark-check"},{'icon':'bi bi-list-nested','label':"FORMATO SQL",}]},
    #{'label':"ATENA", 'icon':'bi bi-info-circle'},
    {'label':"SELEÇÃO", 'icon':'bi bi-scissors'},
    #{'label':"AÇÕES",'icon': "bi bi-gear"},
    {'label':"MAPA",'icon': "bi bi-geo-alt"},
    #{'label':"DASHBOARD", 'icon':'bi bi-graph-up'},
    {'label':"SUSCETIVEIS", 'icon':'bi bi-cash-coin'},
]

#over_theme_2 = {'txc_inactive': '#5C881A','menu_background':'#FFFFFF','txc_active':'#FFFFFF','option_active':'#73A616','font-size':'300%','font-style':'bold'}

#Deixa os valores infinitos (divisão por 0) como NaN
pd.set_option('use_inf_as_na', True)

data_hoje = date.today() - timedelta(0) 
st.session_state.data_hoje = date.today() - timedelta(0) 
data_ontem = date.today() - timedelta(1) 
data_amanha = date.today() + timedelta(1) 

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

#data de hoje str (usada para pegar o pedido de defasagem da programação comercial)
ano_hoje = str(data_hoje.year)
dia_hoje = str(data_hoje.day)
mes_hoje = str(data_hoje.month)
if len(dia_hoje) == 1:
    dia_hoje = '0' + dia_hoje
if len(mes_hoje) == 1:
    mes_hoje = '0' + mes_hoje

# Definicação do valor da meta proporcional, de acordo com o dia do mês.
if str(data_hoje.day) == '8' and str(data_hoje.month) == '9' and str(data_hoje.year) =='2022':
    st.session_state.percentual_meta_mes = 0.2857
    st.session_state.data_pedido = date.today() - timedelta(2)
    st.session_state.data_pedido_mapa = date.today() - timedelta(1)
if str(data_hoje.day) == '9' and str(data_hoje.month) == '9' and str(data_hoje.year) =='2022':
    st.session_state.percentual_meta_mes = 0.3333
if str(data_hoje.day) == '12' and str(data_hoje.month) == '9' and str(data_hoje.year) =='2022':
    st.session_state.percentual_meta_mes = 0.3809
if str(data_hoje.day) == '13' and str(data_hoje.month) == '9' and str(data_hoje.year) =='2022':
    st.session_state.percentual_meta_mes = 0.4285
if str(data_hoje.day) == '14' and str(data_hoje.month) == '9' and str(data_hoje.year) =='2022':
    st.session_state.percentual_meta_mes = 0.4761 - 0.04
if str(data_hoje.day) == '15' and str(data_hoje.month) == '9' and str(data_hoje.year) =='2022':
    st.session_state.percentual_meta_mes = 0.5238 - 0.04
if str(data_hoje.day) == '16' and str(data_hoje.month) == '9' and str(data_hoje.year) =='2022':
    st.session_state.percentual_meta_mes = 0.5714 - 0.04
if str(data_hoje.day) == '19' and str(data_hoje.month) == '9' and str(data_hoje.year) =='2022':
    st.session_state.percentual_meta_mes = 0.6190 - 0.04
if str(data_hoje.day) == '20' and str(data_hoje.month) == '9' and str(data_hoje.year) =='2022':
    st.session_state.percentual_meta_mes = 0.6666 - 0.04
if str(data_hoje.day) == '21' and str(data_hoje.month) == '9' and str(data_hoje.year) =='2022':
    st.session_state.percentual_meta_mes = 0.7142 - 0.04
if str(data_hoje.day) == '22' and str(data_hoje.month) == '9' and str(data_hoje.year) =='2022':
    st.session_state.percentual_meta_mes = 0.7619 - 0.04
if str(data_hoje.day) == '23' and str(data_hoje.month) == '9' and str(data_hoje.year) =='2022':
    st.session_state.percentual_meta_mes = 0.8095 - 0.04
if str(data_hoje.day) == '26' and str(data_hoje.month) == '9' and str(data_hoje.year) =='2022':
    st.session_state.percentual_meta_mes = 0.8571 - 0.04
if str(data_hoje.day) == '27' and str(data_hoje.month) == '9' and str(data_hoje.year) =='2022':
    st.session_state.percentual_meta_mes = 0.9047 - 0.04
if str(data_hoje.day) == '28' and str(data_hoje.month) == '9' and str(data_hoje.year) =='2022':
    st.session_state.percentual_meta_mes = 0.9523 - 0.04
if str(data_hoje.day) == '29' and str(data_hoje.month) == '9' and str(data_hoje.year) =='2022':
    st.session_state.percentual_meta_mes = 1.0 - 0.04
if str(data_hoje.day) == '30' and str(data_hoje.month) == '9' and str(data_hoje.year) =='2022':
    st.session_state.percentual_meta_mes = 1.0
if str(data_hoje.day) == '3' and str(data_hoje.month) == '10' and str(data_hoje.year) =='2022':
    st.session_state.percentual_meta_mes = 0.1 - 0.02
if str(data_hoje.day) == '4' and str(data_hoje.month) == '10' and str(data_hoje.year) =='2022':
    st.session_state.percentual_meta_mes = 0.15 - 0.02
if str(data_hoje.day) == '5' and str(data_hoje.month) == '10' and str(data_hoje.year) =='2022':
    st.session_state.percentual_meta_mes = 0.2 
if str(data_hoje.day) == '6' and str(data_hoje.month) == '10' and str(data_hoje.year) =='2022':
    st.session_state.percentual_meta_mes = 0.25 
if str(data_hoje.day) == '7' and str(data_hoje.month) == '10' and str(data_hoje.year) =='2022':
    st.session_state.percentual_meta_mes = 0.3 
if str(data_hoje.day) == '10' and str(data_hoje.month) == '10' and str(data_hoje.year) =='2022':
    st.session_state.percentual_meta_mes = 0.35 
if str(data_hoje.day) == '11' and str(data_hoje.month) == '10' and str(data_hoje.year) =='2022':
    st.session_state.percentual_meta_mes = 0.4 


if str(data_hoje.day) == '13' and str(data_hoje.month) == '10' and str(data_hoje.year) =='2022':
    st.session_state.percentual_meta_mes = 0.45
if str(data_hoje.day) == '14' and str(data_hoje.month) == '10' and str(data_hoje.year) =='2022':
    st.session_state.percentual_meta_mes = 0.5 
if str(data_hoje.day) == '16' and str(data_hoje.month) == '10' and str(data_hoje.year) =='2022':
    st.session_state.percentual_meta_mes = 0.55 
if str(data_hoje.day) == '17' and str(data_hoje.month) == '10' and str(data_hoje.year) =='2022':
    st.session_state.percentual_meta_mes = 0.55 
if str(data_hoje.day) == '18' and str(data_hoje.month) == '10' and str(data_hoje.year) =='2022':
    st.session_state.percentual_meta_mes = 0.6 
if str(data_hoje.day) == '19' and str(data_hoje.month) == '10' and str(data_hoje.year) =='2022':
    st.session_state.percentual_meta_mes = 0.65
if str(data_hoje.day) == '20' and str(data_hoje.month) == '10' and str(data_hoje.year) =='2022':
    st.session_state.percentual_meta_mes = 0.7 
if str(data_hoje.day) == '21' and str(data_hoje.month) == '10' and str(data_hoje.year) =='2022':
    st.session_state.percentual_meta_mes = 0.75 
if str(data_hoje.day) == '24' and str(data_hoje.month) == '10' and str(data_hoje.year) =='2022':
    st.session_state.percentual_meta_mes = 0.8 
if str(data_hoje.day) == '25' and str(data_hoje.month) == '10' and str(data_hoje.year) =='2022':
    st.session_state.percentual_meta_mes = 0.85 
if str(data_hoje.day) == '26' and str(data_hoje.month) == '10' and str(data_hoje.year) =='2022':
    st.session_state.percentual_meta_mes = 0.9 
if str(data_hoje.day) == '27' and str(data_hoje.month) == '10' and str(data_hoje.year) =='2022':
    st.session_state.percentual_meta_mes = 0.95 
if str(data_hoje.day) == '28' and str(data_hoje.month) == '10' and str(data_hoje.year) =='2022':
    st.session_state.percentual_meta_mes = 1.0 
if str(data_hoje.day) == '31' and str(data_hoje.month) == '10' and str(data_hoje.year) =='2022':
    st.session_state.percentual_meta_mes = 1.0
if str(data_hoje.day) == '1' and str(data_hoje.month) == '11' and str(data_hoje.year) =='2022':
    st.session_state.percentual_meta_mes = 0.1052 - 0.04
if str(data_hoje.day) == '3' and str(data_hoje.month) == '11' and str(data_hoje.year) =='2022':
    st.session_state.percentual_meta_mes = 0.1578 - 0.04
if str(data_hoje.day) == '4' and str(data_hoje.month) == '11' and str(data_hoje.year) =='2022':
    st.session_state.percentual_meta_mes = 0.2105 - 0.04
if str(data_hoje.day) == '7' and str(data_hoje.month) == '11' and str(data_hoje.year) =='2022':
    st.session_state.percentual_meta_mes = 0.2631 - 0.04
if str(data_hoje.day) == '8' and str(data_hoje.month) == '11' and str(data_hoje.year) =='2022':
    st.session_state.percentual_meta_mes = 0.3157 - 0.04
if str(data_hoje.day) == '9' and str(data_hoje.month) == '11' and str(data_hoje.year) =='2022':
    st.session_state.percentual_meta_mes = 0.3684 - 0.04
if str(data_hoje.day) == '10' and str(data_hoje.month) == '11' and str(data_hoje.year) =='2022':
    st.session_state.percentual_meta_mes = 0.4210 - 0.04
if str(data_hoje.day) == '11' and str(data_hoje.month) == '11' and str(data_hoje.year) =='2022':
    st.session_state.percentual_meta_mes = 0.4736 - 0.04
if str(data_hoje.day) == '16' and str(data_hoje.month) == '11' and str(data_hoje.year) =='2022':
    st.session_state.percentual_meta_mes = 0.5263 - 0.04
if str(data_hoje.day) == '17' and str(data_hoje.month) == '11' and str(data_hoje.year) =='2022':
    st.session_state.percentual_meta_mes = 0.5789 - 0.04
if str(data_hoje.day) == '18' and str(data_hoje.month) == '11' and str(data_hoje.year) =='2022':
    st.session_state.percentual_meta_mes = 0.6315 - 0.04
if str(data_hoje.day) == '21' and str(data_hoje.month) == '11' and str(data_hoje.year) =='2022':
    st.session_state.percentual_meta_mes = 0.6842 - 0.04
if str(data_hoje.day) == '22' and str(data_hoje.month) == '11' and str(data_hoje.year) =='2022':
    st.session_state.percentual_meta_mes = 0.7368 - 0.04
if str(data_hoje.day) == '23' and str(data_hoje.month) == '11' and str(data_hoje.year) =='2022':
    st.session_state.percentual_meta_mes = 0.7894 - 0.04
if str(data_hoje.day) == '24' and str(data_hoje.month) == '11' and str(data_hoje.year) =='2022':
    st.session_state.percentual_meta_mes = 0.8421 - 0.04
if str(data_hoje.day) == '25' and str(data_hoje.month) == '11' and str(data_hoje.year) =='2022':
    st.session_state.percentual_meta_mes = 0.8947 - 0.04
if str(data_hoje.day) == '28' and str(data_hoje.month) == '11' and str(data_hoje.year) =='2022':
    st.session_state.percentual_meta_mes = 0.9473 - 0.04
if str(data_hoje.day) == '29' and str(data_hoje.month) == '11' and str(data_hoje.year) =='2022':
    st.session_state.percentual_meta_mes = 1.0 - 0.04
if str(data_hoje.day) == '30' and str(data_hoje.month) == '11' and str(data_hoje.year) =='2022':
    st.session_state.percentual_meta_mes = 1.0
if str(data_hoje.day) == '1' and str(data_hoje.month) == '12' and str(data_hoje.year) =='2022':
    st.session_state.percentual_meta_mes = 0.1 - 0.04
if str(data_hoje.day) == '2' and str(data_hoje.month) == '12' and str(data_hoje.year) =='2022':
    st.session_state.percentual_meta_mes = 0.15 - 0.04
if str(data_hoje.day) == '5' and str(data_hoje.month) == '12' and str(data_hoje.year) =='2022':
    st.session_state.percentual_meta_mes = 0.2 - 0.04
if str(data_hoje.day) == '6' and str(data_hoje.month) == '12' and str(data_hoje.year) =='2022':
    st.session_state.percentual_meta_mes = 0.25 - 0.04
if str(data_hoje.day) == '7' and str(data_hoje.month) == '12' and str(data_hoje.year) =='2022':
    st.session_state.percentual_meta_mes = 0.3- 0.04
if str(data_hoje.day) == '12' and str(data_hoje.month) == '12' and str(data_hoje.year) =='2022':
    st.session_state.percentual_meta_mes = 0.35- 0.04
if str(data_hoje.day) == '13' and str(data_hoje.month) == '12' and str(data_hoje.year) =='2022':
    st.session_state.percentual_meta_mes = 0.4- 0.04
if str(data_hoje.day) == '14' and str(data_hoje.month) == '12' and str(data_hoje.year) =='2022':
    st.session_state.percentual_meta_mes = 0.45- 0.04
if str(data_hoje.day) == '15' and str(data_hoje.month) == '12' and str(data_hoje.year) =='2022':
    st.session_state.percentual_meta_mes = 0.5 - 0.04
if str(data_hoje.day) == '16' and str(data_hoje.month) == '12' and str(data_hoje.year) =='2022':
    st.session_state.percentual_meta_mes = 0.55 - 0.04
if str(data_hoje.day) == '19' and str(data_hoje.month) == '12' and str(data_hoje.year) =='2022':
    st.session_state.percentual_meta_mes = 0.6 - 0.04
if str(data_hoje.day) == '20' and str(data_hoje.month) == '12' and str(data_hoje.year) =='2022':
    st.session_state.percentual_meta_mes = 0.65 - 0.04
if str(data_hoje.day) == '21' and str(data_hoje.month) == '12' and str(data_hoje.year) =='2022':
    st.session_state.percentual_meta_mes = 0.7 - 0.04
if str(data_hoje.day) == '22' and str(data_hoje.month) == '12' and str(data_hoje.year) =='2022':
    st.session_state.percentual_meta_mes = 0.75 - 0.04
if str(data_hoje.day) == '23' and str(data_hoje.month) == '12' and str(data_hoje.year) =='2022':
    st.session_state.percentual_meta_mes = 0.8 - 0.04
if str(data_hoje.day) == '26' and str(data_hoje.month) == '12' and str(data_hoje.year) =='2022':
    st.session_state.percentual_meta_mes = 0.85 - 0.04
if str(data_hoje.day) == '27' and str(data_hoje.month) == '12' and str(data_hoje.year) =='2022':
    st.session_state.percentual_meta_mes = 0.9 - 0.04
if str(data_hoje.day) == '28' and str(data_hoje.month) == '12' and str(data_hoje.year) =='2022':
    st.session_state.percentual_meta_mes = 0.95 - 0.04
if str(data_hoje.day) == '29' and str(data_hoje.month) == '12' and str(data_hoje.year) =='2022':
    st.session_state.percentual_meta_mes = 1.0
# FINAL Definicação do valor da meta proporcional, de acordo com o dia do mês.

# Deixa a página ocupando todo o espaço da tela
st.set_page_config(layout="wide")

st.markdown(
        f"""
        <style>
        .appview-container .main .block-container{{padding-top: {0}rem;padding-right: {0}rem;padding-left: {0}rem;padding-bottom: {0}rem;   }}
        </style>
        """,
                unsafe_allow_html=True,
            )


#div.css-19quj5l.e1tzin5v2 {{
            #height: 40px;
           # index-z: 1;
       # }}
       #div.element-container.css-okk8xu.e1tzin5v3 {{
            #height: 70px;
  
        #}}

margem_titulo = "15px"


 
     



st.markdown(
    
        f"""
        <style>
         
        #adicionado aqui alteracao para diminuir tamanho da caixa do menu
        div.element-container.css-yzpfpm.e1tzin5v3 {{
            height: 20px;
        }}
        div.css-19quj5l.e1tzin5v2 {{
            height: {margem_titulo};
        }}
        #adicionado aqui alteracao para diminuir tamanho da caixa do menu

        
    
#adicionado para diminuir espaco entre sidebar e inicio das caixas
        div.css-hxt7ib.e1fqkh3o2 {{
      padding-top: 10px;
    }}
    div.css-1xtoq5p.e1fqkh3o1 {{
            height: 10px;
        }}

        .css-hxt7ib
        {{
            padding-top: 45px;
        }}


#adicionado para diminuir espaco entre sidebar e inicio das caixas



        
        
        
        .sidebar .main .block-container{{
                padding-top: {0}rem;    }}
        .appview-container .sidebar-content{{
                padding-top: {0}rem;    }}
        .appview-container .stHorizontalBlock{{
                padding-top: {0}rem;    }}
        .appview-container .stHorizontalBlock{{
                padding-bottom: {0}rem;    }}
        .appview-container .stVerticalBlock{{
                padding-top: {0}rem;    }}
        .appview-container .stVerticalBlock{{
                padding-bottom: {-20}rem;    }}

        </style>
        """,
                unsafe_allow_html=True,
            )


       
    

col_title1,col_title2, col_title3, col_title4  = st.columns([5,20,60,5])
col_title1.write("")
with col_title2:
    st.image('logo_2.png')
with col_title3:
    st.markdown("<h3 style='text-align: right; color: #5C881A;'>Recuperação de Crédito - Neoenergia Coelba <br> <em>Ferramenta de Apoio - Seleção de Serviços de Cobrança</em></h3>", unsafe_allow_html=True)
col_title4.write("")

opcao_menu = 2



   # {'label':"LOGIN",'icon': 'bi bi-person'},
    ##{'label':"CONSULTAS SQL",'icon': 'bi bi-search','submenu':[{'label':"CONSULTA CONTA CONTRATO", 'icon': "bi bi-bookmark-check"},{'icon':'bi bi-list-nested','label':"FORMATO SQL",}]},
    #{'label':"ATENA", 'icon':'bi bi-info-circle'},
  #  {'label':"SELEÇÃO", 'icon':'bi bi-scissors','submenu':[{'label':"DEFASAGEM POR ZONAS", 'icon': "bi bi-bookmark-check"},{'label':"DEFASAGEM POR UTDs", 'icon': "bi bi-bookmark-check"},{'label':"SELEÇÃO D+1 (UTDs)", 'icon': "bi bi-tools"},{'label':"SELEÇÃO D+1 (ZONAS)", 'icon': "bi bi-tools"},
   # {'label':"REGULADAS", 'icon': "bi bi-tools"}
   # ]},
   # #{'label':"AÇÕES",'icon': "bi bi-gear"},
   # {'label':"MAPA",'icon': "bi bi-geo-alt",'submenu':[{'label':"MAPA SELECAO", 'icon': "bi bi-bookmark-check"},{'label':"MAPA SUSCETIVEIS", 'icon': "bi bi-bookmark-check"}]},
   # {'label':"DASHBOARD", 'icon':'bi bi-graph-up','submenu':[{'label':"ACOMPANHAMENTO GERACAO", 'icon': "bi bi-bookmark-check"}]},
   # {'label':"SUSCETIVEIS", 'icon':'bi bi-cash-coin','submenu':[{'label':"SUSCETIVEIS", 'icon': 'bi bi-cash-coin'},{'label':"SUSCETIVEIS PARA MAPA", 'icon': 'bi bi-cash-coin'}]},





col_01,col_02, col_03 = st.columns([5,90,5])
col_01.write("")
with col_02:
    selected2 = option_menu(None, ["Login", 
"Seleção", 
"Mapas", 
'Suscetíveis',
'Dashboards',
'Sobre'
], 
icons=['bi bi-person', 
'bi bi-table', 
"bi bi-geo-alt", 
'bi bi-scissors',
'bi bi-graph-up',
'bi bi-info-circle'
], 
    menu_icon="cast", default_index=0, orientation="horizontal",
    styles={
        "container": {"margin": "0px", "margin-bottom": "0px"},
        "nav-link-selected": {"background-color": "#5C881A"},
        "nav-link": {"font-color": "#383838"},
    }
)
col_03.write("")

with st.sidebar:

    selected22 = option_menu(selected2, ["Loginn", 
    "Seleção", 
    "Mapas", 
    'Suscetíveis',
    'Dashboards',
    'Sobre'
    ], 
    icons=['bi bi-person', 
    'bi bi-table', 
    "bi bi-geo-alt", 
    'bi bi-scissors',
    'bi bi-graph-up',
    'bi bi-info-circle'
    ], 
        menu_icon="person", default_index=0, orientation="vertical",
        styles={
            "container": {"margin": "0px", "margin-bottom": "0px"},
            "nav-link-selected": {"background-color": "#5C881A"},
            "nav-link": {"font-color": "#383838"},
        }
    )







if 1 == 0:
    col_menu_1,col_menu_2 = st.columns([5,95])
    col_menu_1.write("")
    with col_menu_2:
        if opcao_menu == 2:
            st.session_state.pagina = menu_id = hc.nav_bar(
            menu_definition=menu_data_2,
            override_theme=over_theme_2,
            hide_streamlit_markers=True,
            sticky_nav=False
        )


with st.sidebar: # Menu lateral
    # Icons: home check-square scissors geo-alt:mapa search
    st.session_state.pagina = option_menu(None, ["Login", "Seleção", "Mapa", "Suscetiveis", "Dashboard","Sobre"],
                        icons=['person', 'bi bi-scissors','bi bi-geo-alt','bi bi-coin','graph-up','bi bi-info-circle'],
                        menu_icon="list", default_index=0,
                        styles={
        "container": {"padding": "5!important", "background-color": "#f0f2f6"},
        "icon": {"color": "#7F7F7F", "font-size": "25px"}, 
        "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#93ac46"},
        "nav-link-selected": {"background-color": "#93ac46","color": "#FFFFFF"},
    }
    )   


#Lista com as UTDs com a primeira opção sendo TODAS
st.session_state.opcao_utd = ["TODAS","ALAGOINHAS","AMARGOSA","BARREIRAS","BOM JESUS DA LAPA","BRUMADO","CAMACARI","CANDEIAS","CONCEICAO DO COITE","ESPLANADA","EUNAPOLIS","FEIRA DE SANTANA NORTE","FEIRA DE SANTANA SUL","GRACA","GUANAMBI","IBOTIRAMA","ILHEUS","IPIAU","IRECE","ITABERABA","ITABUNA","ITAPETINGA","ITAPOAN","JACOBINA","JEQUIE","JUAZEIRO","LAURO DE FREITAS","LIVRAMENTO DE NOSSA SENHORA","LUIS EDUARDO MAGALHAES","PAULO AFONSO","PERIPERI","PIRAJA","PITUBA","PORTO SEGURO","POSTO DA MATA","REMANSO","RIBEIRA DO POMBAL","SANTA MARIA DA VITORIA","SANTO AMARO","SANTO ANTONIO DE JESUS","SEABRA","SENHOR DO BONFIM","SERRINHA","TEIXEIRA DE FREITAS","VALENCA","VITORIA DA CONQUISTA"]
#Lista com as UTDs sem a opção TODAS
st.session_state.opcao_utds = ["ALAGOINHAS","AMARGOSA","BARREIRAS","BOM JESUS DA LAPA","BRUMADO","CAMACARI","CANDEIAS","CONCEICAO DO COITE","ESPLANADA","EUNAPOLIS","FEIRA DE SANTANA NORTE","FEIRA DE SANTANA SUL","GRACA","GUANAMBI","IBOTIRAMA","ILHEUS","IPIAU","IRECE","ITABERABA","ITABUNA","ITAPETINGA","ITAPOAN","JACOBINA","JEQUIE","JUAZEIRO","LAURO DE FREITAS","LIVRAMENTO DE NOSSA SENHORA","LUIS EDUARDO MAGALHAES","PAULO AFONSO","PERIPERI","PIRAJA","PITUBA","PORTO SEGURO","POSTO DA MATA","REMANSO","RIBEIRA DO POMBAL","SANTA MARIA DA VITORIA","SANTO AMARO","SANTO ANTONIO DE JESUS","SEABRA","SENHOR DO BONFIM","SERRINHA","TEIXEIRA DE FREITAS","VALENCA","VITORIA DA CONQUISTA"]

def convert_df(df):
    return df.to_csv(sep=';',decimal=',',index=False).encode('utf-8')
def csv_to_df(df):
    return pd.read_csv(df,sep=';',decimal=',')
 
today = date.today()
delta = 1 ; next_day = today + timedelta(delta) # D + 1

if 'pagina' not in st.session_state:
    st.session_state.pagina = "login"

if 'check_login' not in st.session_state:
    st.session_state.check_login = 0
    if st.session_state.check_login == 1:
        st.write(st.session_state.usuario, st.session_state.senha)
        
if 'check_consulta' not in st.session_state:
    st.session_state.check_consulta = 0

if 'check_configuracoes' not in st.session_state:
    st.session_state.check_configuracoes = 0


if str.lower(st.session_state.pagina) == 'login':
    st.markdown("<h3 style='text-align: center; color: #5C881A;'>LOGIN - SAP HANA</h1>", unsafe_allow_html=True)
    col_login1, col_login2,col_login3 = st.columns([25,50,25])
    col_login1.write("")
    with col_login2:
        with st.form(key = "form_login"):
            st.session_state.usuario = st.text_input("Usuário", help='Usuário do SAP HANA')
            st.session_state.senha = st.text_input("Senha", type="password", help='Senha do SAP HANA')
            submit = st.form_submit_button(label = "Acessar")
            if submit:
                testar_login()
                #st.session_state.objeto_atena = SelecaoLayout(usuario = st.session_state.usuario, senha = st.session_state.senha)
    col_login3.write("")
            
# Estilo dos metrics
st.markdown("""
    <style>
    div[data-testid="metric-container"] {
    background-color: #22142b
    border: 1px solid #FFFFFF;
    
    border-radius: 5px;
    color: #5C881A;
    overflow-wrap: break-word;
    }

    /* breakline for metric text         */
    div[data-testid="metric-container"] > label[data-testid="stMetricLabel"] > div {
    overflow-wrap: break-word;
    white-space: break-spaces;
    color: #5C881A;
    }
    </style>
    """
    , unsafe_allow_html=True)
 

if str.lower(st.session_state.pagina) == "seleção":
    #with st.sidebar:
    col_def_01,col_def_1,col_def_2,col_def_3,col_def_4,col_def_5,col_def_05  = st.columns([1,30,20,20,20,20,1])
    with col_def_1:
        st.session_state.opcao_tipo_resumo = ["Defasagem por UTDs","Defasagem por Zonas","Seleção D+1 (UTDs)","Seleção D+1 (Zonas)"]
        st.session_state.pagina_resumo = st.selectbox('Opção da página:', st.session_state.opcao_tipo_resumo) 
    
    if (str.lower(st.session_state.pagina_resumo) == "seleção d+1 (utds)" or str.lower(st.session_state.pagina_resumo) == "seleção d+1 (zonas)") and st.session_state.check_login == 1:
        if str.lower(st.session_state.pagina_resumo) == "seleção d+1 (utds)":
            st.markdown("<h4 style='text-align: center; color: #5C881A;'> RESUMO SELEÇÃO DE COBRANÇA (D+1) UTDs</h4>", unsafe_allow_html=True)
            
            if 'base_final_UTD' not in st.session_state:
                with st.spinner('Carregando...'):
                    get_quadro_geral_utd() 
            st.session_state.opcao_filtrar_rank = ["Def. Mapa","Meta %","Gordura Geração %","% Anuladas","Qtd Meta - Pendentes"]
        else:
            st.markdown("<h4 style='text-align: center; color: #5C881A;'> RESUMO SELEÇÃO DE COBRANÇA (D+1) ZONAS</h4>", unsafe_allow_html=True)
            
            if 'base_final_ZONAS' not in st.session_state:
                with st.spinner('Carregando...'):
                    get_quadro_geral_zonas_d_mais_1() 
            st.session_state.opcao_filtrar_rank = ["Def. Mapa","% Anuladas"]
        def color_survived(val):
            if val > 7:
                color = '#FF5A00' 
            elif val > 4:
                color = '#0070C0' 
            else:
                color = '#383838'
            return f'color: {color}'    

        
        

        st.session_state.opcao_turma = ["STC","EPS","PRONTIDÃO"]
        st.session_state.opcao_carteira = ["TODAS","CORTE","RECORTE","DISJUNTOR","BAIXA"]
        
        
        #col_def_01,col_def_1,col_def_2,col_def_3,col_def_4,col_def_5,col_def_05  = st.columns([1,20,20,20,20,20,1])
        col_def_01.write("")
        col_def_05.write("")
        with col_def_2:
            st.session_state.turma = st.selectbox('Turma:', st.session_state.opcao_turma)  
        with col_def_3:
            st.session_state.carteira = st.selectbox('Carteira:', st.session_state.opcao_carteira)  
            
        #with col_def_3:
            #st.date_input('Data Pedido:',value=st.session_state.data_selecao_hoje,disabled=True) #data hoje
        #with col_def_4:
            #st.session_state.carteira = st.selectbox('Carteira:', st.session_state.opcao_carteira)  
        with col_def_4:
            st.session_state.opcao_filtro_rank = st.selectbox('Filtro/Rank:',  st.session_state.opcao_filtrar_rank)   
        with col_def_5:
            st.session_state.utd_def = st.selectbox('UTD:', st.session_state.opcao_utd) 

        if str.lower(st.session_state.pagina_resumo) == "seleção d+1 (utds)":
            st.session_state.base_final_temp = st.session_state.base_final_UTD[(st.session_state.base_final_UTD['TURMA'] == st.session_state.turma)].copy()
        else:
            st.session_state.base_final_temp = st.session_state.base_final_ZONAS[(st.session_state.base_final_ZONAS['TURMA'] == st.session_state.turma)].copy()
        if st.session_state.carteira != 'TODAS':
            st.session_state.base_final_temp = st.session_state.base_final_temp[(st.session_state.base_final_temp['CARTEIRA'] == st.session_state.carteira)]
        if st.session_state.utd_def != 'TODAS':
            st.session_state.base_final_temp = st.session_state.base_final_temp[(st.session_state.base_final_temp['UTD'] == st.session_state.utd_def)]
        if st.session_state.opcao_filtro_rank == 'Meta %':
            st.session_state.base_final_temp = st.session_state.base_final_temp.sort_values(['PERCENT_META'],ascending=[True])
        elif st.session_state.opcao_filtro_rank == 'Gordura Geração %':
            st.session_state.base_final_temp = st.session_state.base_final_temp.sort_values(['PERCENT_GERA'],ascending=[True])
        elif st.session_state.opcao_filtro_rank == 'Qtd Meta - Pendentes':
            st.session_state.base_final_temp = st.session_state.base_final_temp.sort_values(['QTD_META_PARCIAL_MENOS_PENDENTE'],ascending=[False])
        elif st.session_state.opcao_filtro_rank == '% Anuladas':
            st.session_state.base_final_temp = st.session_state.base_final_temp.sort_values(['PERCENT_ANULADAS'],ascending=[False])
        if str.lower(st.session_state.pagina_resumo) == "seleção d+1 (utds)":
            st.session_state.base_final_temp = st.session_state.base_final_temp[['UTD','CARTEIRA','PERCENT','PERCENT_GERA','PERCENT_META','QTD_META','QTD_GERADAS','QTD_EXECUTADAS','QTD_PENDENTES','TOTAL_ESPERADO_MAPA','NOTAS_ESPERADAS_ATENA','QTD_CLUSTER','QTD_SUSCETIVEIS','TICKET_PECLD','DEFASAGEM_MAPA','CONFIG','QTD_ANULADAS','PERCENT_ANULADAS','QTD_META_TOTAL_MENOS_PENDENTE','QTD_META_PARCIAL_MENOS_PENDENTE']]
        else:
            st.session_state.base_final_temp = st.session_state.base_final_temp[['UTD','ZONA','BASE CLICK','CARTEIRA','PERCENT','QTD_META','QTD_GERADAS','QTD_EXECUTADAS','QTD_PENDENTES','TOTAL_ESPERADO_MAPA','NOTAS_ESPERADAS_ATENA','QTD_CLUSTER','QTD_SUSCETIVEIS','TICKET_PECLD','DEFASAGEM_MAPA','CONFIG','QTD_ANULADAS','PERCENT_ANULADAS']]
        st.session_state.base_final_temp.rename(columns = {
            'CARTEIRA':'Carteira',
            'TOTAL_ESPERADO_MAPA' : 'Mapa',
            'NOTAS_ESPERADAS_ATENA' : 'Atena',
            'PERCENT_META' : 'Meta (%) (UTD)',
            'QTD_META' : 'Meta proporcional (UTD)',
            'DEFASAGEM_MAPA':'Def. Mapa',
            'QTD_CLUSTER':'Qtd. Turmas',
            'QTD_SUSCETIVEIS':'Qtd. Suscet.',
            'TICKET_PECLD':'Ticket PECLD',
            'QTD_GERADAS':'Qtd. Geradas (mês)',
            'QTD_EXECUTADAS':'Qtd. Executadas (mês)',
            'PERCENT':'% Orçamento UTD',
            'PERCENT_GERA':'Gordura Geração (%)',
            'QTD_PENDENTES':'Qtd. Pendentes',
            'QTD_ANULADAS':'Qtd. Anuladas',
            'PERCENT_ANULADAS':'% Anuladas',
            'ZONA':'Zona',
            'QTD_META_TOTAL_MENOS_PENDENTE':'Qtd. Meta Total - Pendentes',
            'QTD_META_PARCIAL_MENOS_PENDENTE':'Qtd. Meta Parcial - Pendentes'
            }, inplace = True)

        hide_table_row_index = """
                <style>
                thead tr th:first-child {display:none}
                tbody th {display:none}
                </style>
                """
        st.markdown(hide_table_row_index, unsafe_allow_html=True)

        col_def_11,col_def_12,col_def_13  = st.columns([1,102,1])
        col_def_11.write("")
        col_def_13.write("")
        with col_def_12:
            st.table(st.session_state.base_final_temp.style.format({'% Orçamento UTD': '{:,.0%}',
            'Gordura Geração (%)': '{:,.0%}',
            'Meta (%) (UTD)': '{:,.0%}',
            'Ticket PECLD': '{:,.1f}',
            '% Anuladas': '{:,.0%}'

            }).applymap(color_survived, subset=['Def. Mapa']))
            

        output = BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet()
        text_format = workbook.add_format({'align': 'left', 'bold': False})
        header_format = workbook.add_format({'align': 'left', 'fg_color': '#5C881A', 'bold': True, 'font_color': 'white'})
        start_row = 0
        start_col = 0
        if str.lower(st.session_state.pagina_resumo) == "seleção d+1 (utds)":
            worksheet.write_row(start_row, start_col, st.session_state.base_final_temp.columns, header_format)
            for i, column in enumerate(st.session_state.base_final_temp.columns, start=start_col):
                worksheet.write_column(start_row+1, i, st.session_state.base_final_temp[column], text_format)
            workbook.close()
            #with st.sidebar:
            st.write("Baixar em Excel:")
            st.download_button(
                label="Baixar",
                data=output.getvalue(),
                file_name="D+1 UTDs TURMA({}) - CARTEIRA({}) - UTD({}) {}.{}.{}.xlsx".format(st.session_state.turma,st.session_state.carteira,st.session_state.utd_def,dia_hoje,mes_hoje,ano_hoje),
                mime="application/vnd.ms-excel"
            )
        else:
            worksheet.write_row(start_row, start_col, st.session_state.base_final_temp.columns, header_format)
            for i, column in enumerate(st.session_state.base_final_temp.columns, start=start_col):
                worksheet.write_column(start_row+1, i, st.session_state.base_final_temp[column], text_format)
            workbook.close()
            #with st.sidebar:
            st.write("Baixar em Excel:")
            st.download_button(
                label="Baixar",
                data=output.getvalue(),
                file_name="D+1 ZONAS {} - {} - UTD: {} {}.{}.{}.xlsx".format(st.session_state.turma,st.session_state.carteira,st.session_state.utd_def,dia_hoje,mes_hoje,ano_hoje),
                mime="application/vnd.ms-excel"
            )


    elif (str.lower(st.session_state.pagina_resumo) == "defasagem por zonas" or str.lower(st.session_state.pagina_resumo) == "defasagem por utds") and st.session_state.check_login == 1:
        if str.lower(st.session_state.pagina_resumo) == "defasagem por zonas":
            st.markdown("<h4 style='text-align: center; color: #5C881A;'> ANÁLISE DEFASAGEM POR ZONA </h4>", unsafe_allow_html=True)
            st.markdown("<h6 style='text-align: center; color: #FF5A00;'><em> *Defasagem dos cortes selecionados para EPS devem ser desconsiderada na Sexta e deve ser analisada na segunda</em></h6>", unsafe_allow_html=True)
        else:
            st.markdown("<h4 style='text-align: center; color: #5C881A;'> ANÁLISE DEFASAGEM POR UTDs</h4>", unsafe_allow_html=True)
            st.markdown("<h6 style='text-align: center; color: #FF5A00;'><em> *Defasagem dos cortes selecionados para EPS devem ser desconsiderada na Sexta e deve ser analisada na segunda</em></h6>", unsafe_allow_html=True)
        #

        def color_survived(val):
            if val > 7:
                color = '#FF5A00' 
            elif val > 4:
                color = '#0070C0' 
            else:
                color = '#383838'
            return f'color: {color}'    
            
        #
        if str.lower(st.session_state.pagina_resumo) == "defasagem por zonas":
            if 'base_final' not in st.session_state:
                with st.spinner('Carregando...'):
                    consulta_defasagem_hoje()  
        else:
            if 'mudanca_pagina' not in st.session_state:
                with st.spinner('Carregando...'):
                    consulta_defasagem_hoje() 

        st.session_state.opcao_turma = ["STC","EPS"]
        st.session_state.opcao_carteira = ["TODAS","CORTE","RECORTE","DISJUNTOR"]
        st.session_state.opcao_pedido_programacao = ["TUDO","PEDIDO PROGRAMAÇÃO"]
        #st.session_state.lista_utds = list(st.session_state.base_final.UTD.unique())
        
        #col_def_01,col_def_1,col_def_2,col_def_3,col_def_4,col_def_5,col_def_05  = st.columns([1,20,20,20,20,20,1])
        #col_def_01.write("")
        #col_def_05.write("")
        
        with col_def_2:
            st.session_state.turma = st.selectbox('Turma:', st.session_state.opcao_turma)  
        with col_def_3:
            st.session_state.carteira = st.selectbox('Carteira:', st.session_state.opcao_carteira)  
        #with col_def_3:
            #if str.lower(st.session_state.pagina_resumo) == "defasagem por zonas":
                #st.date_input('Data Pedido:',value=st.session_state.data_pedido,disabled=True) #data_pedido
            #else:
                #st.date_input('Data Pedido:',value=st.session_state.data_pedido,disabled=True) #data hoje
        with col_def_4:
            if str.lower(st.session_state.pagina_resumo) == "defasagem por zonas":
                st.session_state.pedido_programcao = st.selectbox('Pedido Programação:', st.session_state.opcao_pedido_programacao) 
            else:
                st.text_input('Usuário:',value=st.session_state.nome_usuario,disabled=True) #nome
        with col_def_5:
            st.session_state.utd_def = st.selectbox('UTD:', st.session_state.opcao_utd)  
        


        if str.lower(st.session_state.pagina_resumo) == "defasagem por zonas":
            st.session_state.base_final_temp = st.session_state.base_final[(st.session_state.base_final['TURMA'] == st.session_state.turma)].copy()
            if st.session_state.carteira != 'TODAS':
                st.session_state.base_final_temp = st.session_state.base_final_temp[(st.session_state.base_final_temp['CARTEIRA'] == st.session_state.carteira)]
            if st.session_state.pedido_programcao != 'TUDO':
                st.session_state.base_final_temp = st.session_state.base_final_temp[(st.session_state.base_final_temp['JUSTIFICATIVA'] != "-")]
            if st.session_state.utd_def != 'TODAS':
                st.session_state.base_final_temp = st.session_state.base_final_temp[(st.session_state.base_final_temp['UTD'] == st.session_state.utd_def)]
        else:
            st.session_state.base_final_temp = st.session_state.base_final_2[(st.session_state.base_final_2['TURMA'] == st.session_state.turma)].copy()
            if st.session_state.carteira != 'TODAS':
                st.session_state.base_final_temp = st.session_state.base_final_temp[(st.session_state.base_final_temp['CARTEIRA'] == st.session_state.carteira)]
            if st.session_state.utd_def != 'TODAS':
                st.session_state.base_final_temp = st.session_state.base_final_temp[(st.session_state.base_final_temp['UTD'] == st.session_state.utd_def)]
        
        
        #st.session_state.base_final_temp = st.session_state.base_final_temp[['UTD','BASE CLICK','ZONA','TURMA','CARTEIRA','TOTAL_ESPERADO_MAPA','NOTAS_ESPERADAS_ATENA','NOTAS_GERADAS_TAB4','DEFASAGEM_GERACAO','DEFASAGEM_MAPA','DEFASAGEM_PROGRAMACAO','QTD_TURMAS','QTD_NOTAS','JUSTIFICATIVA','QTD_SUSCETIVEIS','VALOR_COBRAVEL','PECLD','TICKET_COBRAVEL','TICKET_PECLD']]
        if str.lower(st.session_state.pagina_resumo) == "defasagem por zonas":
            st.session_state.base_final_temp = st.session_state.base_final_temp[['UTD','BASE CLICK','ZONA','CARTEIRA','TOTAL_ESPERADO_MAPA','NOTAS_ESPERADAS_ATENA','NOTAS_GERADAS_TAB4','DEFASAGEM_GERACAO','DEFASAGEM_MAPA','NOTAS_DEFASAGEM_ATENA','DEFASAGEM_PROGRAMACAO','QTD_TURMAS','QTD_NOTAS','JUSTIFICATIVA','QTD_SUSCETIVEIS','TICKET_PECLD','QTD_META','QTD_GERADAS','QTD_EXECUTADAS','QTD_PENDENTES','QTD_ANULADAS','PERCENT_ANULADAS','PERCENT','TICKET_PECLD_GERADAS','TICKET_PECLD_EXECUTADAS','CONFIG']]
        else:
            st.session_state.base_final_temp = st.session_state.base_final_temp[['UTD','CARTEIRA','TOTAL_ESPERADO_MAPA','NOTAS_ESPERADAS_ATENA','NOTAS_GERADAS_TAB4','DEFASAGEM_GERACAO','DEFASAGEM_MAPA','NOTAS_DEFASAGEM_ATENA','QTD_SUSCETIVEIS','TICKET_PECLD','QTD_GERADAS','TICKET_PECLD_GERADAS','QTD_EXECUTADAS','QTD_PENDENTES','QTD_ANULADAS','PERCENT_ANULADAS','QTD_META','PERCENT_META','PERCENT','CONFIG','TICKET_PECLD_EXECUTADAS']]
        hide_table_row_index = """
                <style>
                thead tr th:first-child {display:none}
                tbody th {display:none}
                </style>
                """
        st.markdown(hide_table_row_index, unsafe_allow_html=True)
        
        st.session_state.base_final_temp.rename(columns = {'BASE CLICK':'Base Click',
        'CARTEIRA':'Carteira',
        'TOTAL_ESPERADO_MAPA' : 'Mapa',
        'NOTAS_ESPERADAS_ATENA' : 'Atena',
        'NOTAS_GERADAS_TAB4' : 'Geradas',
        'ZONA':'Zona',
        'DEFASAGEM_GERACAO':'Def. Gerad',
        'DEFASAGEM_MAPA':'Def. Mapa',
        'DEFASAGEM_PROGRAMACAO':'Def. Prog',
        'QTD_TURMAS':'Qtd. Turmas',
        'QTD_NOTAS':'Qtd. Notas',
        'JUSTIFICATIVA':'Justificativa',
        'QTD_SUSCETIVEIS':'Qtd. Suscet.',
        'TICKET_PECLD':'Ticket PECLD',
        'QTD_GERADAS':'Qtd. Geradas (mês)',
        'QTD_PENDENTES':'Qtd. Pendentes',
        'TICKET_PECLD_GERADAS':'Ticket geração (mês)',
        'QTD_EXECUTADAS':'Qtd. Executadas (mês)',
        'TICKET_PECLD_EXECUTADAS':'Ticket execução (mês)',
        'QTD_META':'Meta proporcional (UTD)',
        'PERCENT':'% Orçamento UTD',
        'PERCENT_ANULADAS':'% Anuladas',
        'QTD_ANULADAS':'Qtd. Anuladas',
        'PERCENT_META':'Meta (%) (UTD)',
        'NOTAS_DEFASAGEM_ATENA':'Inseridas na Defasagem!'
        }, inplace = True)
        
        


        col_def_11,col_def_12,col_def_13  = st.columns([1,102,1])
        col_def_11.write("")
        col_def_13.write("")
        with col_def_12:
            st.table(st.session_state.base_final_temp.style.format({'% Orçamento UTD': '{:,.0%}',
            'Gordura Geração (%)': '{:,.0%}',
            'Meta (%) (UTD)': '{:,.0%}',
            'Ticket PECLD': '{:,.1f}',
            '% Anuladas': '{:,.0%}'
            }).applymap(color_survived, subset=['Def. Gerad']))
            

            
            output = BytesIO()

            workbook = xlsxwriter.Workbook(output, {'in_memory': True})
            worksheet = workbook.add_worksheet()

            text_format = workbook.add_format({'align': 'left', 'bold': False})
            header_format = workbook.add_format({'align': 'left', 'fg_color': '#5C881A', 'bold': True, 'font_color': 'white'})

            start_row = 0
            start_col = 0
            worksheet.write_row(start_row, start_col, st.session_state.base_final_temp.columns, header_format)
            for i, column in enumerate(st.session_state.base_final_temp.columns, start=start_col):
                worksheet.write_column(start_row+1, i, st.session_state.base_final_temp[column], text_format)
            #worksheet.write('A1', st.session_state.base_final)
            workbook.close()
            if str.lower(st.session_state.pagina_resumo) == "defasagem por zonas":
                st.download_button(
                    label="Baixar Excel",
                    data=output.getvalue(),
                    file_name="Defasagem Zonas TURMA({}) - CARTEIRA({}) - UTD({}) {}.{}.{}.xlsx".format(st.session_state.turma,st.session_state.carteira,st.session_state.utd_def,dia_hoje,mes_hoje,ano_hoje),
                    mime="application/vnd.ms-excel"
                )
            else:
                st.download_button(
                    label="Baixar Excel",
                    data=output.getvalue(),
                    file_name="Defasagem UTDs TURMA({}) - CARTEIRA({}) - UTD({}) {}.{}.{}.xlsx".format(st.session_state.turma,st.session_state.carteira,st.session_state.utd_def,dia_hoje,mes_hoje,ano_hoje),
                    mime="application/vnd.ms-excel"
                )
        
            
    elif (str.lower(st.session_state.pagina_resumo) == "defasagem por zonas" or str.lower(st.session_state.pagina_resumo) == "seleção d+1") and st.session_state.check_login == 0:
        st.error("NECESSÁRIO EFETUAR LOGIN")



if str.lower(st.session_state.pagina) == "consulta conta contrato" and st.session_state.check_login == 1:
    def consulta_geral_conta_contrato_sql():
        txt_sql_consulta_geral = 'Consulta_geral_conta_contrato'
        consulta = ['sources/Sqls/'+ txt_sql_consulta_geral + '.sql', st.session_state.lista_saida]
        arquivo_sql_consulta_geral = open(consulta[0], encoding="utf-8")
        sql_consulta_geral = arquivo_sql_consulta_geral.read()
        arquivo_sql_consulta_geral.close()
        sql_consulta_geral = sql_consulta_geral.format(lista_consultar = consulta[1])
        connection_hana = dbapi.connect(address='BRNEO695',port='30015',user=st.session_state.usuario,password=st.session_state.senha,databasename='BNP',sslValidateCertificate=False)
        st.session_state.df_consulta_geral_conta = pd.read_sql(sql_consulta_geral, connection_hana)
        #st.caption(sql_consulta_geral) #comentar

    st.markdown("<h5 style='text-align: center; color: #5C881A;'> CONSULTA GERAL</h5>", unsafe_allow_html=True)
    with st.sidebar:
        with st.form(key='form_consulta_geral',clear_on_submit = False):
            st.session_state.lista_entrada = st.text_input("CONTA CONTRATO:", help='Cole a conta contrato a ser pesquisada:',max_chars=10)
            submit = st.form_submit_button(label = "Realizar a Consulta")
    if submit:
        with st.spinner('Carregando...'):
            formatar_lista_entrada_sql()
            consulta_geral_conta_contrato_sql()
        
            cl0,cl1,cl2,cl3,cl4,cl5,cl6,cl7 = st.columns([5,15,15,15, 15, 15, 15,5])
            cl0.write("")
            cl1.metric(label="Status Sistema", value=st.session_state.df_consulta_geral_conta['SIT_CC'][0])
            cl2.metric(label="PECLD", value="R$" + str(round(st.session_state.df_consulta_geral_conta['PECLD_ATUAL'][0],1)))
            cl3.metric(label="Dívida", value="R$" + str(round(st.session_state.df_consulta_geral_conta['MONT_CR'][0],1)))
            if st.session_state.df_consulta_geral_conta['BLOQ_TIPO_CC'][0] != "?":
                cl4.metric(label="Bloqueio CC", value=st.session_state.df_consulta_geral_conta['BLOQ_TIPO_CC'][0])
            else:
                cl4.metric(label="Bloqueio CC", value="Não")
            if st.session_state.df_consulta_geral_conta['BLOQ_TIPO_FAT'][0] != "?":
                cl5.metric(label="Bloqueio Fatura", value=st.session_state.df_consulta_geral_conta['BLOQ_TIPO_FAT'][0])
            else:
                cl5.metric(label="Bloqueio Fatura", value="Não")
            if st.session_state.df_consulta_geral_conta['ZCGNNVLAD'][0] != "?":
                cl6.metric(label="ZCGNNVLAD", value=st.session_state.df_consulta_geral_conta['ZCGNNVLAD'][0])
            else:
                cl6.metric(label="ZCGNNVLAD", value="Não")
            cl7.write("")
            

            col0, col1, col2, col3,col4 = st.columns([5,45,2,45,5])
            col0.write("")
            col2.write("")
            with col1:
                lista = ["FAT_ZCGDTDOCT","FAT_ZCGNOMED"]
                st.session_state.df_consulta_geral_conta_consumo = st.session_state.df_consulta_geral_conta[lista].copy()
                st.session_state.df_consulta_geral_conta_consumo = st.session_state.df_consulta_geral_conta_consumo.drop_duplicates(subset=["FAT_ZCGDTDOCT"])
                source = pd.DataFrame({'x' :st.session_state.df_consulta_geral_conta_consumo["FAT_ZCGDTDOCT"],'y': st.session_state.df_consulta_geral_conta_consumo["FAT_ZCGNOMED"]})
                st.altair_chart(alt.Chart(source, title='CONSUMO (kWh) MENSAL').mark_line(point=alt.OverlayMarkDef(color="#5C881A")).encode(alt.X('x',title='Meses'),alt.Y('y',title='Consumo (kWh)'),color=alt.value("#5C881A")).properties(width=500))
                
                lista = ["NT_LEIT","DT_LEIT"]
                st.session_state.df_consulta_geral_conta_leitura = st.session_state.df_consulta_geral_conta[lista].copy()
                st.session_state.df_consulta_geral_conta_leitura.drop_duplicates(inplace=True)
                #aggrid_interactive_table(df=st.session_state.df_consulta_geral_conta_leitura)
                st.session_state.df_consulta_geral_conta_leitura = st.session_state.df_consulta_geral_conta_leitura.drop('DT_LEIT', 1)
                st.session_state.df_leitura_frequencia = st.session_state.df_consulta_geral_conta_leitura.value_counts()
                
                #st.table(st.session_state.df_leitura_frequencia)
                #aggrid_interactive_table(df= st.session_state.df_consulta_geral_conta_leitura)
                #source = pd.DataFrame({'x' :st.session_state.df_leitura_frequencia.iloc[:,0].index,'y': st.session_state.df_leitura_frequencia.iloc[:,0].values})
                #st.altair_chart(alt.Chart(source, title='CONSUMO (kWh) MENSAL').mark_line(point=alt.OverlayMarkDef(color="#5C881A")).encode(alt.X('x',title='Meses'),alt.Y('y',title='Consumo (kWh)'),color=alt.value("#5C881A")).properties(width=500))

            with col3:
                lista = ["ARR_ZCGDTCOMP","ARR_ZCGAMOUNTDIA"]
                st.session_state.df_consulta_geral_conta_arr = st.session_state.df_consulta_geral_conta[lista].copy()
                st.session_state.df_consulta_geral_conta_arr = st.session_state.df_consulta_geral_conta_arr.drop_duplicates(subset=["ARR_ZCGDTCOMP"])
                source = pd.DataFrame({'x' :st.session_state.df_consulta_geral_conta_arr["ARR_ZCGDTCOMP"],'y': st.session_state.df_consulta_geral_conta_arr["ARR_ZCGAMOUNTDIA"]})
                st.altair_chart(alt.Chart(source, title='ARRECADAÇÃO (R$) MENSAL').mark_line(point=alt.OverlayMarkDef(color="#5C881A")).encode(alt.X('x',title='Meses'),alt.Y('y',title='Arrecadação'),color=alt.value("#5C881A")).properties(width=500))
            col4.write("")
elif st.session_state.pagina == "consulta_geral" and st.session_state.check_login == 0:
    st.error("NECESSÁRIO EFETUAR LOGIN")

            
                

            
            
if str.lower(st.session_state.pagina) == "mapaaa":
    def consulta_geral_mapa_sql():
        txt_sql_consulta_geral = 'consulta_geral_pecld'
        consulta = ['sources/Sqls/'+ txt_sql_consulta_geral + '.sql']
        arquivo_sql_consulta_geral = open(consulta[0], encoding="utf-8")
        sql_consulta_geral = arquivo_sql_consulta_geral.read()
        arquivo_sql_consulta_geral.close()
        sql_consulta_geral = sql_consulta_geral
        connection_hana = dbapi.connect(address='BRNEO695',port='30015',user=st.session_state.usuario,password=st.session_state.senha,databasename='BNP',sslValidateCertificate=False)
        st.session_state.df_consulta_mapa = pd.read_sql(sql_consulta_geral, connection_hana)
        #st.caption(sql_consulta_geral) #comentar

    with st.spinner('Carregando...'):
        if 'df_consulta_mapa'  not in st.session_state:
                consulta_geral_mapa_sql()
    with st.sidebar:
        st.session_state.lista_opcoes = ["PECLD","TURMAS"]
        st.session_state.categoria = st.selectbox('Selecione a Categoria:', st.session_state.lista_opcoes)
        st.session_state.lista_utds = list(st.session_state.df_consulta_mapa.UTD.unique())
        st.session_state.utd = st.selectbox('Selecione a UTD:', st.session_state.lista_utds)
        st.session_state.df_consulta_mapa_temp = st.session_state.df_consulta_mapa[(st.session_state.df_consulta_mapa['UTD'] == st.session_state.utd)].copy()
        st.session_state.df_consulta_mapa_temp = st.session_state.df_consulta_mapa_temp.reset_index(drop=True)
        st.session_state.df_consulta_mapa_temp = st.session_state.df_consulta_mapa_temp.dropna().reset_index(drop=True)
        st.session_state.qtd_total_temp = len(st.session_state.df_consulta_mapa_temp)
        st.write(st.session_state.qtd_total_temp)
    col1, col2, col3 = st.columns([5,90,5])
    col1.write("")
    col3.write("")
    teste =2
    if teste == 1:
        m = folium.Map(location=[st.session_state.df_consulta_mapa["ZCGLATITU"][2], st.session_state.df_consulta_mapa["ZCGLONGIT"][2]], zoom_start=16)
        tooltip = "Liberty Bell"
        folium.Marker(
            [st.session_state.df_consulta_mapa["ZCGLATITU"][2], st.session_state.df_consulta_mapa["ZCGLONGIT"][2]], popup="Liberty Bell", tooltip=tooltip
        ).add_to(m)
        folium_static(m)

    if teste == 0:
        st.session_state.df_consulta_mapa = st.session_state.df_consulta_mapa.dropna().reset_index(drop=True)
        st.session_state.df_consulta_mapa = st.session_state.df_consulta_mapa[(st.session_state.df_consulta_mapa['UTD'] == "ITABUNA")].copy()
        st.session_state.df_consulta_mapa['ZCGLATITU'] = st.session_state.df_consulta_mapa['ZCGLATITU'].astype(float)
        st.session_state.df_consulta_mapa['ZCGLONGIT'] = st.session_state.df_consulta_mapa['ZCGLONGIT'].astype(float)

        centro_mapa = {'lat':st.session_state.df_consulta_mapa.ZCGLATITU.mean(), 'lon':st.session_state.df_consulta_mapa.ZCGLONGIT.mean()}
        mapa = px.density_mapbox(st.session_state.df_consulta_mapa, lat='ZCGLATITU', lon='ZCGLONGIT', z='PECLD', radius=20,
                center=centro_mapa, zoom=10,
                mapbox_style='stamen-terrain')
        mapa.show()
    with col2:
        with st.spinner('Carregando...'):
            m = folium.Map(location=[st.session_state.df_consulta_mapa_temp["ZCGLATITU"][0], st.session_state.df_consulta_mapa_temp["ZCGLONGIT"][0]], zoom_start=16,width='100%',height='100%')
            tooltip = "Liberty Bell"
            
            for i in range(st.session_state.qtd_total_temp):
                iframe = folium.IFrame('INTALACAO: ' + str(st.session_state.df_consulta_mapa_temp['INTALACAO'][i]) + '<br>' + 'PECLD: ' + str(st.session_state.df_consulta_mapa_temp['PECLD'][i]) + '<br>'  )      
                popup = folium.Popup(iframe, min_width=330, max_width=390, min_height=250)
                #if demanda_tmp['TIPO_PRIO'][i] in colors_prio.keys():
                folium.Marker(
                    location=[st.session_state.df_consulta_mapa_temp["ZCGLATITU"][i], st.session_state.df_consulta_mapa_temp["ZCGLONGIT"][i]],
                    popup=popup,
                    icon=plugins.BeautifyIcon(icon_shape="marker", 
                    border_color= "#5C881A", background_color="#5C881A")
                                ).add_to(m)

            folium_static(m,width=1050)
            #aggrid_interactive_table(df=st.session_state.df_consulta_mapa)
             
            
            
if str.lower(st.session_state.pagina) == "plano ação":
    st.markdown("<h5 style='text-align: center; color: #5C881A;'> ACOMPANHAMENTO PLANO AÇÃO - FATURAMENTO/LEITURA</h5>", unsafe_allow_html=True)
        
    if 'df_consulta_pr' not in st.session_state:
        with st.spinner('Carregando...'):
            consulta_geral_sql_pr()
    
    with st.spinner('Carregando...'):
        col_dash1, col_dash2,col_dash3,col_dash4 = st.columns([5,45,45,5])
        col_dash1.write("")
        with col_dash2:
            st.markdown(tabela_resumo_pr(), unsafe_allow_html=True)
        col_dash3.write("")
        col_dash4.write("")
    with st.sidebar:
        st.session_state.categoria = st.selectbox('Selecione a Categoria:', st.session_state.lista_opcoes)
        st.session_state.df_consulta_pr_temp = st.session_state.df_consulta_pr[(st.session_state.df_consulta_pr['ACAO'] == st.session_state.categoria) & (st.session_state.df_consulta_pr['MEDIA_CONSUMO_12_MESES'] > 0) & (st.session_state.df_consulta_pr['MEDIA_CONSUMO_12_MESES'] != 'nan')].copy()
        st.session_state.df_consulta_pr_temp = st.session_state.df_consulta_pr_temp.reset_index(drop=True)
        st.session_state.qtd_total_temp = len(st.session_state.df_consulta_pr_temp.index)
        st.session_state.rank_consumo = st.number_input('Selecione no rank (consumo):', min_value=0, max_value=st.session_state.qtd_total_temp)
        #st.write(st.session_state.qtd_total_temp)

    cl_aux1, cl_aux2, cl_aux3 = st.columns([5,90,5])
    cl_aux1.write("")
    cl_aux2.write("")
    cl_aux3.write("")
    
    cl1,cl02, cl2, cl3, cl4, cl5, cl6 = st.columns([5,18,18,18,18,18,5])
    cl1.write("")
    cl6.write("")
    
    col_graf1, col_graf2,col_graf3,col_graf4 = st.columns([5,45,45,5])
    col_graf1.write("")
    with col_graf2:
        st.write("")
        graficos_pr_chart()
    with col_graf3:
        #st.table(st.session_state.freq_leitura_pr.iloc[:,0].index)
        #source = pd.DataFrame({'x' :st.session_state.freq_leitura_pr.iloc[:,1].index,'y': st.session_state.freq_leitura_pr.iloc[:,1].values})
        #st.altair_chart(alt.Chart(source, title='CONSUMO (kWh) MENSAL (12 meses)').mark_line(point=alt.OverlayMarkDef(color="#5C881A")).encode(
        #    alt.X('x',title='Meses'),
        #    alt.Y('y',title='Consumo (kWh)'),
        #color=alt.value("#5C881A")).properties(width=500))
        st.write("")
        st.markdown(tabela_consumo_6_meses(), unsafe_allow_html=True)
        
        
    col_graf4.write("")
    cl_aux2.markdown("<h5 style='text-align: left; color: #5C881A;'> Análise PR pelo consumo médio e notas de leitura - Conta Contrato: {}</h5>".format(st.session_state.conta), unsafe_allow_html=True)
    cl02.metric(label="Status Sistema", value=st.session_state.status_sistema)
    cl2.metric("Consumo Médio (12 meses)", str(round(st.session_state.consumo_medio,1)) + " kWh")
    cl3.metric("PECLD","R$" + str(round(st.session_state.pecld,1))  )
    cl4.metric("Dívida","R$" + str(round(st.session_state.mont_cr,1))  )
    cl5.metric("Repetibilidade",  str(st.session_state.repetibilidade)  )
    
    cl_1, cl_2, cl_3 = st.columns([5,90,5])
    cl_1.write("")
    with cl_2:
        st.write("")
        st.markdown(tabela_repetibilidade_pr(), unsafe_allow_html=True)
        
    cl_3.write("")
    


    with st.form(key='form_tabela_geral',clear_on_submit = False):
        submit = st.form_submit_button(label = "Exibir Base Geral")
    if submit:
        with st.spinner('Carregando...'):
            col_tab1, col_tab2,col_tab3 = st.columns([5,90,5])
            col_tab1.write("")
            with col_tab2:
                aggrid_interactive_table(df=st.session_state.df_consulta_pr)
            col_tab3.write("")



if str.lower(st.session_state.pagina) == "formato sql":
    col1,col2, col3  = st.columns([10,80,10])
    col1.write("")
    with col2:
        st.markdown("<h5 style='text-align: center; color: #5C881A;'>FORMATAÇÃO DE CONTAS E INSTALAÇÃO PARA CONSULTA SQL</h5>", unsafe_allow_html=True)
        st.session_state.opcao_formatacao_sql = st.radio("CONTA CONTRATO OU INSTALAÇÃO",('Conta Contrato', 'Instalação'),horizontal=True)
        with st.form(key='form_consulta_formato_sql',clear_on_submit = False):
            st.session_state.lista_entrada = st.text_input("LISTA:", help='Cole a lista das contas contratos ou instalações a serem formatadas:')
            submit = st.form_submit_button(label = "ALTERAR FORMATAÇÃO")
        if submit:
            formatar_lista_entrada_sql_3()
            
    col3.write("")
        



casa = "sim"


if str.lower(st.session_state.pagina) == "dashboard":
    #import io 
    #buffer = io.StringIO() 
    #st.session_state.df_consulta_pr.info(buf=buffer)
    #s = buffer.getvalue() 
    #with open("df_info.txt", "w", encoding="utf-8") as f:
        #f.write(s) 
    if casa == "sim":
        nome_arquivo_excel = 'consulta_pr' 
        caminho_arquivo_excel = r'C:\\Users\\thiag\\OneDrive - IBERDROLA S.A\\Cobrança\\cobranca_streamlit\\{}.xlsx'.format(nome_arquivo_excel)
        st.session_state.df_consulta_pr = pd.read_excel(caminho_arquivo_excel)
        st.session_state.df_consulta_pr.columns = st.session_state.df_consulta_pr.columns.str.replace(' ', '')
        st.session_state.df_consulta_pr.loc[(st.session_state.df_consulta_pr.OBSERVACAO == "N? Baixar"), "OBSERVACAO"] = "Não Baixar"
        st.session_state.df_consulta_pr.loc[(st.session_state.df_consulta_pr.ACAO == "N? Baixar"), "ACAO"] = "Não Baixar"
        st.session_state.df_consulta_pr.loc[(st.session_state.df_consulta_pr.ACAO == "Arrecada?o 3 meses"), "ACAO"] = "Arrecadação 3 meses"
        st.session_state.qtd_total = len(st.session_state.df_consulta_pr.index)
        st.session_state.df_consulta_pr.loc[(((st.session_state.df_consulta_pr.ACAO == "Unidade Ligada (Gerar Corte)") | (st.session_state.df_consulta_pr.ACAO == "Gerar Baixa ADM")) & (st.session_state.df_consulta_pr.REPETIBILIDADE_B100_D100_D110 < 5)), "ACAO"] = "Sem repetibilidade"
        df_temp = st.session_state.df_consulta_pr[(st.session_state.df_consulta_pr['ACAO'] == "Baixado")].copy()
        df_temp = df_temp.reset_index(drop=True)
        
        st.session_state.perc1 = round((st.session_state.qtd_baixados/st.session_state.qtd_total)*100,2)









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
if str.lower(st.session_state.pagina) == "acompanhamento geracao":
    st.markdown("<h4 style='text-align: center; color: #5C881A;'> ANÁLISE GERAÇÃO DE SERVIÇOS DE COBRANÇA</h4>", unsafe_allow_html=True)
    st.session_state.opcao_visualizacao = ["CONTA CONTRATO","RUAS","BAIRROS","MUNICIPIOS","ZONAS","UTDS"]
    st.session_state.opcao_turma_geradas_executadas = ["STC","EPS","PRONTIDAO"]
    st.session_state.opcao_carteira_geradas_executadas = ["CORTE","RECORTE","DISJUNTOR","BAIXA"]

    col_def_01,col_def_001,col_def_1,col_def_2,col_def_3,col_def_4,col_def_05  = st.columns([1,20,20,20,20,20,1])
    col_def_01.write("")
    col_def_05.write("")
    with col_def_001:
        st.session_state.visualizacao_suscetiveis = st.selectbox('Opção:', st.session_state.opcao_visualizacao)  
    with col_def_1:
        st.session_state.turma_geradas_executadas = st.selectbox('Turma:', st.session_state.opcao_turma_geradas_executadas)  
    with col_def_2:
        st.session_state.carteira_geradas_executadas = st.selectbox('Carteira:', st.session_state.opcao_carteira_geradas_executadas)  
    with col_def_3:
        st.session_state.data_referencia_geradas_executadas = st.date_input('Data Referencia:',disabled=True) #data hoje
    with col_def_4:
        st.session_state.utd_geradas_executadas = st.selectbox('UTD:', st.session_state.opcao_utds) 
    def coleta_geradas_executadas():
        txt_sql_consulta_geradas_executadas = 'Consulta_geradas_executadas_anuladas'
        consulta = ['sources/Sqls/'+ txt_sql_consulta_geradas_executadas + '.sql',st.session_state.turma_geradas_executadas,st.session_state.carteira_geradas_executadas,st.session_state.data_referencia_geradas_executadas,st.session_state.utd_geradas_executadas]
        arquivo_sql_consulta_geradas_executadas = open(consulta[0], encoding="utf-8")
        sql_consulta_geradas_executadas = arquivo_sql_consulta_geradas_executadas.read()
        arquivo_sql_consulta_geradas_executadas.close()
        #sql_consulta_geradas_executadas = sql_consulta_hoje_UTD.format(data_consulta = consulta[1])
        connection_hana = dbapi.connect(address='BRNEO695',port='30015',user=st.session_state.usuario,password=st.session_state.senha,databasename='BNP',sslValidateCertificate=False)
        st.session_state.base_geradas_executadas = pd.read_sql(sql_consulta_geradas_executadas, connection_hana)
    if 'base_geradas_executadas' not in st.session_state:
        with st.spinner('Carregando...'):
            coleta_geradas_executadas()
    
    #st.write(st.session_state.base_geradas_executadas)

    total_teste = st.session_state.base_geradas_executadas.groupby(['ZCGDTNOTA','DIA_MES'])[['QTD_GERADAS','QTD_EXECUTADAS']].sum().reset_index()
    
    #st.write(total_teste)
    labels = total_teste['ZCGDTNOTA']
    labels_nomes = total_teste['DIA_MES']
    qtd_geradas = total_teste['QTD_GERADAS']
    qtd_executadas = total_teste['QTD_EXECUTADAS']
    x = np.arange(len(labels))
    width = 0.4
    fig,ax = plt.subplots()
    rects1 = ax.bar(x - width/2, qtd_geradas, width, label='Geradas')
    rects2 = ax.bar(x + width/2, qtd_executadas, width, label='Executadas')
    #ax.set_ylabel('Qtd. Notas')
    ax.set_title('Notas Geradas,Executadas e Anuladas últimos 30 dias')
    ax.set_xticks(x)
    ax.set_xticklabels(labels_nomes)
    ax.tick_params(axis='x', labelrotation = 90)
    ax.set(yticklabels=[])
    ax.tick_params(axis='y',left=False)
    ax.legend()
    ax.bar_label(rects1, padding=3)
    ax.bar_label(rects2, padding=3)
    ax.set_ylim([0, max(qtd_geradas) + max(qtd_geradas)*0.2])
    fig.tight_layout()
    
    #fig = plt.figure(figsize = (10, 5))
    col_graf1, col_graf2, col_graf3,col_graf4 = st.columns([1,1,50,1])
    col_graf1.write("")
    col_graf4.write("")
    col_graf2.write("")
    with col_graf3:
        st.pyplot(fig)


        
if str.lower(st.session_state.pagina) == "suscetiveis":
    
    col_def_01,col_def_001,col_def_1,col_def_2,col_def_3,col_def_4,col_def_5,col_def_05  = st.columns([1,20,15,20,20,15,25,1])
    col_def_01.write("")
    col_def_05.write("")
    with col_def_001:
        st.session_state.opcao_tipo_suscetiveis = ["Suscetiveis","Suscetiveis para Mapa"]
        st.session_state.pagina_suscetiveis = st.selectbox('Opção da página:', st.session_state.opcao_tipo_suscetiveis) 
    if str.lower(st.session_state.pagina_suscetiveis) == "suscetiveis":
        st.markdown("<h4 style='text-align: center; color: #5C881A;'> SELEÇÃO DE SUSCETIVEIS</h4>", unsafe_allow_html=True)
        st.session_state.opcao_visualizacao = ["CONTA CONTRATO","RUAS","BAIRROS","MUNICIPIOS","ZONAS","UTDS"]
        st.session_state.opcao_turma_suscetiveis = ["STC","EPS","PRONTIDAO"]
        st.session_state.opcao_carteira_suscetiveis = ["CORTE","RECORTE","DISJUNTOR","BAIXA"]

        
    
        
        with col_def_1:
            st.session_state.turma_suscetiveis = st.selectbox('Turma:', st.session_state.opcao_turma_suscetiveis)  
        with col_def_2:
            st.session_state.carteira_suscetiveis = st.selectbox('Carteira:', st.session_state.opcao_carteira_suscetiveis)  
        
        with col_def_3:
            st.session_state.visualizacao_suscetiveis = st.selectbox('Opção:', st.session_state.opcao_visualizacao)  
        with col_def_4:
            st.session_state.data_referencia_suscetiveis = st.date_input('Data Referencia:',disabled=True) #data hoje
        with col_def_5:
            st.session_state.utd_suscetiveis = st.selectbox('UTD:', st.session_state.opcao_utd) 
        
        # coleta suscetiveis aqui!!!!!
        with st.spinner('Carregando...'):
            coleta_suscetiveis()
        
        st.write(st.session_state.base_suscetiveis)
        output = BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet()
        text_format = workbook.add_format({'align': 'left', 'bold': False})
        header_format = workbook.add_format({'align': 'left', 'fg_color': '#5C881A', 'bold': True, 'font_color': 'white'})
        start_row = 0
        start_col = 0
        worksheet.write_row(start_row, start_col, st.session_state.base_suscetiveis.columns, header_format)
        for i, column in enumerate(st.session_state.base_suscetiveis.columns, start=start_col):
            worksheet.write_column(start_row+1, i, st.session_state.base_suscetiveis[column], text_format)
        workbook.close()

        #with st.sidebar:
        st.write("Baixar em Excel:")
        st.download_button(
            label="Baixar",
            data=output.getvalue(),
            file_name="Suscetiveis TURMA({}) - CARTEIRA({}) - UTD({}) {}.{}.{}.xlsx".format(st.session_state.turma_suscetiveis,st.session_state.carteira_suscetiveis,st.session_state.utd_suscetiveis,dia_hoje,mes_hoje,ano_hoje),
            mime="application/vnd.ms-excel"
        )


    if str.lower(st.session_state.pagina_suscetiveis) == "suscetiveis para mapa":
    #if str.lower(st.session_state.pagina) == "suscetiveis para mapa":
        st.markdown("<h4 style='text-align: center; color: #5C881A;'> SUSCETIVEIS PARA MAPA </h4>", unsafe_allow_html=True)
        with st.spinner('Carregando...'):
            if 'base_suscetiveis_total' not in st.session_state:
                coletar_suscetiveis_total()
            if 'base_final_ZONAS' not in st.session_state:
                get_quadro_geral_zonas_d_mais_1() 
                base_final_temp = st.session_state.base_final_ZONAS[['UTD','ZONA','TURMA','CARTEIRA','QTD_GERADAS','QTD_EXECUTADAS','QTD_PENDENTES','QTD_ANULADAS','PERCENT_ANULADAS']]
                base_final_temp.rename(columns = {
                'CARTEIRA':'ACAO'}, inplace = True)
                st.session_state.base_suscetiveis_total = pd.merge(st.session_state.base_suscetiveis_total, base_final_temp, how = 'left', on=['UTD','TURMA','ACAO','ZONA'])
                st.session_state.base_suscetiveis_total[['QTD_GERADAS','QTD_EXECUTADAS','QTD_PENDENTES','QTD_ANULADAS','PERCENT_ANULADAS']] = st.session_state.base_suscetiveis_total[['QTD_GERADAS','QTD_EXECUTADAS','QTD_PENDENTES','QTD_ANULADAS','PERCENT_ANULADAS']].fillna(0)
        st.session_state.base_suscetiveis_total.to_excel('../Mapa/base_suscetiveis.xlsx',index=False,encoding='utf-8-sig')
        st.write(st.session_state.base_suscetiveis_total)
        
        

        output = BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet()
        text_format = workbook.add_format({'align': 'left', 'bold': False})
        header_format = workbook.add_format({'align': 'left', 'fg_color': '#5C881A', 'bold': True, 'font_color': 'white'})
        start_row = 0
        start_col = 0
        worksheet.write_row(start_row, start_col, st.session_state.base_suscetiveis_total.columns, header_format)
        for i, column in enumerate(st.session_state.base_suscetiveis_total.columns, start=start_col):
            worksheet.write_column(start_row+1, i, st.session_state.base_suscetiveis_total[column], text_format)
        workbook.close()

        st.download_button(
            label="Baixar Excel",
            data=output.getvalue(),
            file_name="Suscetiveis para Mapa {}.{}.{}.xlsx".format(dia_hoje,mes_hoje,ano_hoje),
            mime="application/vnd.ms-excel"
        )

if str.lower(st.session_state.pagina) == "mapa":
 
    #adicionado 
    #with st.sidebar:
    col_def_01,col_def_1,col_def_2,col_def_3,col_def_4,col_def_5,col_def_6,col_def_7,col_def_05  = st.columns([1,25,15,20,20,25,15,15,1])
    col_def_01.write("")
    #st.markdown("<h3 style='text-align: center; color: #5C881A;'> ANÁLISE SELEÇÃO DE SERVIÇOS DE COBRANÇA (MAPA)</h3>", unsafe_allow_html=True)
    with col_def_1:
        st.session_state.opcao_tipo_mapa = ["Mapa Suscetíveis","Mapa Seleção","Mapa PECLD"]
        st.session_state.pagina_mapa = st.selectbox('Escolha o Mapa:', st.session_state.opcao_tipo_mapa) 
        if st.session_state.pagina_mapa == "Mapa Seleção":
            
            st.session_state.opcao_turma = ["STC","EPS"]
            st.session_state.opcao_carteira = ["TODAS","CORTE","RECORTE","DISJUNTOR","BAIXA"]
            
            with col_def_2:
                st.session_state.turma = st.selectbox('Turma:', st.session_state.opcao_turma)  
            with col_def_3:
                st.session_state.carteira = st.selectbox('Carteira:', st.session_state.opcao_carteira)  
            
            with col_def_4:
                st.session_state.data_pedido_folium = st.date_input('Data Pedido:',disabled=False) #data hoje
            with col_def_5:
                st.session_state.utd_folium = st.selectbox('UTD:', st.session_state.opcao_utds) 
            
        

            if st.session_state.data_pedido_folium == date.today():
                txt_sql_consulta_mapa_notas_selecionadas = 'Consulta_notas_selecionadas_HOJE'
            else:
                txt_sql_consulta_mapa_notas_selecionadas = 'Consulta_notas_selecionadas'
            consulta = ['sources/Sqls/'+ txt_sql_consulta_mapa_notas_selecionadas + '.sql',st.session_state.utd_folium,st.session_state.turma,st.session_state.data_pedido_folium]
            arquivo_sql_consulta_mapa_notas_selecionadas = open(consulta[0], encoding="utf-8")
            sql_consulta_mapa_notas_selecionadas = arquivo_sql_consulta_mapa_notas_selecionadas.read()
            arquivo_sql_consulta_mapa_notas_selecionadas.close()
            sql_consulta_mapa_notas_selecionadas = sql_consulta_mapa_notas_selecionadas.format(utd_mapa_folium = consulta[1],turma_mapa_folium = consulta[2],data_mapa_folium= consulta[3])
            connection_hana = dbapi.connect(address='BRNEO695',port='30015',user=st.session_state.usuario,password=st.session_state.senha,databasename='BNP',sslValidateCertificate=False)
            base_df = pd.read_sql(sql_consulta_mapa_notas_selecionadas, connection_hana) 
            #st.write(base_df)


            base_df['LATITUDE'] = base_df['LATITUDE'].str.replace(',','.')
            base_df['LONGITUDE'] = base_df['LONGITUDE'].str.replace(',','.')
            base_df = base_df.dropna(subset = ['LATITUDE']).reset_index(drop = True)
            base_df['PECLD'] = base_df['PECLD'].fillna(0.0)
            base_df = base_df.drop_duplicates(subset=["ZCGACCOUN"], keep='first')
            if len(base_df) > 0:
                sql = """
                SELECT COUNT( DISTINCT (case when TIPO_NOTA = 'CS'  then ZCGACCOUN end)) AS QTD_CORTE,
                COUNT( DISTINCT (case when TIPO_NOTA = 'CA'  then ZCGACCOUN end)) AS QTD_RECORTE,
                COUNT( DISTINCT (case when TIPO_NOTA = 'CB'  then ZCGACCOUN end)) AS QTD_BAIXA,
                CAST(SUM(PECLD)/COUNT(DISTINCT ZCGACCOUN) AS INTEGER) AS TICKET_PECLD,
                COUNT( DISTINCT PACOTE  ) AS QTD_PACOTES
                FROM (
                {}
                )
                """.format(sql_consulta_mapa_notas_selecionadas)
                #st.write(sql)
                resumo_mapa_selecao = pd.read_sql(sql, connection_hana) 
                
            with st.sidebar:
                st.markdown("<h3 style='text-align: center; color: #5C881A;'> ANÁLISE SELEÇÃO DE SERVIÇOS DE COBRANÇA (MAPA)</h3>", unsafe_allow_html=True)
                if len(base_df) > 0:
                    clll1,clll2,clll3,clll4  = st.columns([50,50,50,50])
                    clll1_1,clll2_1  = st.columns([50,50])
                    clll1.metric(label="Pacotes", value=resumo_mapa_selecao['QTD_PACOTES'][0])
                    clll2.metric(label="CS Total", value=resumo_mapa_selecao['QTD_CORTE'][0])
                    clll3.metric(label="CA Total", value=resumo_mapa_selecao['QTD_RECORTE'][0])
                    clll4.metric(label="CB Total", value=resumo_mapa_selecao['QTD_BAIXA'][0])
                    clll1_1.metric(label="Ticket PECLD", value="R$ " + str(resumo_mapa_selecao['TICKET_PECLD'][0]))
                    with clll2_1:
                        st.write("")

            with st.sidebar:
                clll1_11,clll2_22  = st.columns([50,50])
                with clll1_11:
                    st.session_state.larg_mapa = st.slider('Largura do Mapa', min_value=1300, max_value=1600, step=10,value=1400)
                    ColorMinMax = st.markdown(''' <style> div.stSlider > div[data-baseweb = "slider"] > div[data-testid="stTickBar"] > div {
                        background: rgb(1 1 1 / 0%); } </style>''', unsafe_allow_html = True)
                    Slider_Cursor = st.markdown(''' <style> div.stSlider > div[data-baseweb="slider"] > div > div > div[role="slider"]{
                        background-color: rgb(92, 136, 26); box-shadow: rgb(92, 136, 26 / 20%) 0px 0px 0px 0.2rem;} </style>''', unsafe_allow_html = True)
                    Slider_Number = st.markdown(''' <style> div.stSlider > div[data-baseweb="slider"] > div > div > div > div
                                                    { color: rgb(84, 84, 84); } </style>''', unsafe_allow_html = True)
                    col = f''' <style> div.stSlider > div[data-baseweb = "slider"] > div > div {{
                        background: linear-gradient(to right, rgb(92, 136, 26) 0%, 
                                                    rgb(92, 136, 26) {st.session_state.larg_mapa}%, 
                                                    rgba(92, 136, 26, 0.25) {st.session_state.larg_mapa}%, 
                                                    rgba(92, 136, 26, 0.25) 100%); }} </style>'''
                    ColorSlider = st.markdown(col, unsafe_allow_html = True)  
                with clll2_22:
                    st.session_state.alt_mapa = st.slider('Altura do Mapa', min_value=400, max_value=800, step=10,value=550)

                    col2 = f''' <style> div.stSlider > div[data-baseweb = "slider"] > div > div {{
                        background: linear-gradient(to right, rgb(92, 136, 26) 0%, 
                                                    rgb(92, 136, 26) {st.session_state.alt_mapa}%, 
                                                    rgba(92, 136, 26, 0.25) {st.session_state.alt_mapa}%, 
                                                    rgba(92, 136, 26, 0.25) 100%); }} </style>'''
                    ColorSlider2 = st.markdown(col2, unsafe_allow_html = True)  

            #base_final = base_final[((base_final['ACAO'] == "MANTER"))]
            #base_df
            st.session_state.opcao_nao_sim = ["NÃO","SIM"]
            with col_def_6:
                st.session_state.exibir_legenda = st.selectbox('Exibir Legenda:', st.session_state.opcao_nao_sim)  
            with col_def_7:
                st.session_state.exibir_mini_mapa = st.selectbox('Exibir Mini Mapa:', st.session_state.opcao_nao_sim)  
                with col_def_1:
                    if len(base_df) > 0:
                        base_df[['PACOTE','ZONA']] = base_df[['PACOTE','ZONA']].fillna(0.0)
                        base_df[['PACOTE','ZONA']]  = base_df[['PACOTE','ZONA']].astype(int)
                        #base_df['default_rank'] = base_df['PACOTE'].rank(pct=True)
                        base_df['Average'] = base_df.groupby('PACOTE')['PACOTE'].transform('mean')
                        base_df['default_rank'] = base_df['Average'].rank(method='dense', ascending=True)

                

                        base_df['default_rank'] = base_df['default_rank'].fillna(0.0)
                        base_df['default_rank']  = base_df['default_rank'].astype(int)
                        base_df[['LATITUDE','LONGITUDE']] = base_df[['LATITUDE','LONGITUDE']].astype(float)
                        centroides = base_df[['LATITUDE','LONGITUDE','NOTA','PACOTE']].copy()
                        centroides[['LATITUDE','LONGITUDE']] = centroides[['LATITUDE','LONGITUDE']].astype(float)
                        centroides = centroides.groupby(by =['PACOTE'],as_index= False).mean()

                        centroides_utd = base_df[['LATITUDE','LONGITUDE','UTD']].copy()
                        centroides_utd[['LATITUDE','LONGITUDE']] = centroides_utd[['LATITUDE','LONGITUDE']].astype(float)
                        centroides_utd = centroides_utd.groupby(by =['UTD'],as_index= False).mean()

                        

                        mp = folium.Map(location=[base_df.LATITUDE.mean(), 
                                                base_df.LONGITUDE.mean()], zoom_start=8)
                        #marker_cluster = MarkerCluster(maxClusterRadius=3).add_to(mp)
                        folium.raster_layers.TileLayer('Open Street Map').add_to(mp)
                        #folium.raster_layers.TileLayer(tiles = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',attr = 'Esri',name = 'Esri Satellite',overlay = True,control = True).add_to(mp)
                        
                        folium.raster_layers.TileLayer('Stamen Terrain').add_to(mp)
                    
                        titulo_legenda = "Legenda Mapa de Seleção <br>"
                        titulo_legenda_2 = "{} - UTD ({}) <br>".format(st.session_state.turma,st.session_state.utd_folium)
                        titulo_legenda_3 = "Data Pedido {}".format(st.session_state.data_pedido_folium)
                        titulo_legenda = titulo_legenda + titulo_legenda_2 + titulo_legenda_3
                        if max(base_df['default_rank']) <= 3:
                            lgnd = """<li><span style='background:#5C881A;opacity:1;'></span>Pacote 1</li>
                            <li><span style='background:#0070C0;opacity:1;'></span>Pacote 2</li>
                            <li><span style='background:#383838;opacity:1;'></span>Pacote 3</li>"""
                        elif max(base_df['default_rank']) <= 6:
                            lgnd = """<li><span style='background:#5C881A;opacity:1;'></span>Pacote 1</li>
                            <li><span style='background:#0070C0;opacity:1;'></span>Pacote 2</li>
                            <li><span style='background:#383838;opacity:1;'></span>Pacote 3</li>
                            <li><span style='background:#FF5A00;opacity:1;'></span>Pacote 4</li>
                            <li><span style='background:#C3E98A;opacity:1;'></span>Pacote 5</li>
                            <li><span style='background:#ffb200;opacity:1;'></span>Pacote 6</li>
            """
                        elif max(base_df['default_rank']) <= 8:
                            lgnd = """<li><span style='background:#5C881A;opacity:1;'></span>Pacote 1</li>
                            <li><span style='background:#0070C0;opacity:1;'></span>Pacote 2</li>
                            <li><span style='background:#383838;opacity:1;'></span>Pacote 3</li>
                            <li><span style='background:#FF5A00;opacity:1;'></span>Pacote 4</li>
                            <li><span style='background:#C3E98A;opacity:1;'></span>Pacote 5</li>
                            <li><span style='background:#ffb200;opacity:1;'></span>Pacote 6</li>
                            <li><span style='background:#86B8D6;opacity:1;'></span>Pacote 7</li>
                            <li><span style='background:#A6A6A6;opacity:1;'></span>Pacote 8</li>"""
                        elif max(base_df['default_rank']) <= 12:
                            lgnd = """<li><span style='background:#5C881A;opacity:1;'></span>Pacote 1</li>
                            <li><span style='background:#0070C0;opacity:1;'></span>Pacote 2</li>
                            <li><span style='background:#383838;opacity:1;'></span>Pacote 3</li>
                            <li><span style='background:#FF5A00;opacity:1;'></span>Pacote 4</li>
                            <li><span style='background:#C3E98A;opacity:1;'></span>Pacote 5</li>
                            <li><span style='background:#ffb200;opacity:1;'></span>Pacote 6</li>
                            <li><span style='background:#86B8D6;opacity:1;'></span>Pacote 7</li>
                            <li><span style='background:#A6A6A6;opacity:1;'></span>Pacote 8</li>
                            <li><span style='background:#FF4409;opacity:1;'></span>Pacote 9</li>
                            <li><span style='background:#85d2ee;opacity:1;'></span>Pacote 10</li>
                            <li><span style='background:#159f99;opacity:1;'></span>Pacote 11</li>
                            <li><span style='background:#5C881A;opacity:1;'></span>Pacote 12</li>"""
                        elif max(base_df['default_rank']) <= 100:
                            lgnd = """<li><span style='background:#5C881A;opacity:1;'></span>Pacote 1 </li>
                            <li><span style='background:#0070C0;opacity:1;'></span>Pacote 2</li>
                            <li><span style='background:#383838;opacity:1;'></span>Pacote 3</li>
                            <li><span style='background:#FF5A00;opacity:1;'></span>Pacote 4</li>
                            <li><span style='background:#C3E98A;opacity:1;'></span>Pacote 5</li>
                            <li><span style='background:#ffb200;opacity:1;'></span>Pacote 6</li>
                            <li><span style='background:#86B8D6;opacity:1;'></span>Pacote 7</li>
                            <li><span style='background:#A6A6A6;opacity:1;'></span>Pacote 8</li>
                            <li><span style='background:#FF4409;opacity:1;'></span>Pacote 9</li>
                            <li><span style='background:#85d2ee;opacity:1;'></span>Pacote 10</li>
                            <li><span style='background:#159f99;opacity:1;'></span>Pacote 11</li>
                            <li><span style='background:#5C881A;opacity:1;'></span>Pacote 12</li>
                            <li><span style='background:#545454;opacity:1;'></span>Pacote 13</li>
                            <li><span style='background:#35402d;opacity:1;'></span>Pacote 14</li>
                            <li><span style='background:#F6B283;opacity:1;'></span>Pacote 15</li>"""


                        for i, row in base_df.iterrows():
                            atalho_pacote =  row['ATALHO_PACOTE']
                            atalho_pacote_2 =  row['ATALHO_PACOTE_2']
                            rank_pacote = str(row['default_rank'])
                            cor_texto = '#5C881A'
                            if rank_pacote  == '1':
                                cor = '#5C881A'
                                cor_fundo = '#5C881A'
                                cor_texto =  "#FFFFFF"
                            elif rank_pacote  == '2':
                                cor = '#0070C0'
                                cor_fundo = '#0070C0'
                                cor_texto =  "#FFFFFF"
                            elif rank_pacote  == '3':
                                cor = '#383838'
                                cor_fundo = '#383838'
                                cor_texto =  "#FFFFFF"
                            elif rank_pacote  == '4':
                                cor = '#FF5A00'
                                cor_fundo = '#FF5A00'
                                cor_texto =  "#FFFFFF"
                            elif rank_pacote  == '5':
                                cor = '#C3E98A'
                                cor_fundo = '#C3E98A'
                                cor_texto =  "#545454"
                            elif rank_pacote  == '6':
                                cor = '#ffb200'
                                cor_fundo = '#ffb200'
                                cor_texto =  "#FFFFFF"
                            elif rank_pacote  == '7':
                                cor = '#86B8D6'
                                cor_fundo = "#86B8D6"
                                cor_texto =  "#545454"
                            elif rank_pacote  == '8':
                                cor = '#A6A6A6'
                                cor_fundo = '#A6A6A6'
                                cor_texto =  "#545454"
                            elif rank_pacote  == '9':
                                cor = '#FF4409'
                                cor_fundo = '#FF4409'
                                cor_texto =  "#FFFFFF"
                            elif rank_pacote  == '10':
                                cor = ' #85d2ee'
                                cor_fundo =  '#85d2ee'
                                cor_texto =  "#545454"
                            elif rank_pacote  == '11':
                                cor = '#159f99'
                                cor_fundo =  '#159f99'
                                cor_texto =  "#545454"
                            elif rank_pacote  == '12':
                                cor =  '#545454'
                                cor_fundo = '#5C881A'
                                cor_texto =  "#FFFFFF"
                            elif rank_pacote  == '13':
                                cor = '#383838'
                                cor_fundo = '#545454'
                                cor_texto =  "#FFFFFF"
                            elif rank_pacote  == '14':
                                cor = '#35402d'
                                cor_fundo = '#35402d'
                                cor_texto =  "#FFFFFF"
                            elif rank_pacote  == '15':
                                cor = '#F6B283'
                                cor_fundo = '#F6B283'
                                cor_texto =  "#545454"
                            elif rank_pacote  == '16':
                                cor = '#FFE653'
                                cor_fundo = '#FFE653'
                                cor_texto =  "#545454"
                            else:
                                cor =  'gray'
                                cor_fundo = cor
                            
                            utd = row['UTD']
                            conta_contrato = row['ZCGACCOUN']
                            viatura = row['PACOTE']
                            nota = row['NOTA']
                            tipo_nota = row['TIPO_NOTA']
                            rua= row['ZCGNMLOGR']
                            bairro = row['ZCGBAIRR']
                            local= row['MUNICIPIO']
                            poligonal= row['ZONA']
                            latitude = row['LATITUDE']
                            longitude = row['LONGITUDE']
                            pecld = int(row['PECLD'])
                            legenda = '''

                                <b>UTD:</b> {} <br>
                                <b>Pacote:</b> {} <br>
                                <b>Nota:</b> {} <br>
                                <b>Conta Contrato:</b> {} <br>
                                <b>Tipo de Nota:</b> {} <br>
                                
                                <b>Rua:</b> {} <br>
                                <b>Bairro:</b> {} <br>
                                <b>Local:</b> {} <br>
                                <b>Zona:</b> {} <br>
                                <b>Latitude:</b> {} <br>
                                <b>Longitude:</b> {} <br>
                                <b>PECLD:</b> R${} <br>

                                '''.format(utd,viatura,nota,conta_contrato,tipo_nota,rua,bairro,local,poligonal,latitude,longitude,pecld)
                            iframe = folium.IFrame(legenda,width=380, height=230)
                            folium.Marker(location = [row['LATITUDE'],row['LONGITUDE']],
                                                        popup=folium.Popup(iframe),
                                        
                                        icon=plugins.BeautifyIcon(icon="leaf",icon_shape="marker", number=row['RANK_PECLD'], 
                                            border_color= cor, background_color=cor_fundo,text_color=cor_texto,borderWidth=1)
                                        
                                                    ).add_to(mp)
                            
                            
                        def get_json_nota(df):
                            geo_json = {
                            "type": "FeatureCollection",
                            "features":[]
                            }

                            for i,row in df.iterrows():
                                temp_dict = {
                                "type": "Feature",
                                "geometry": {
                                    "type": "Point",
                                    "coordinates":[row['LONGITUDE'], row['LATITUDE']],

                                },"properties": {"nota": row['NOTA']}
                                }
                                geo_json["features"].append(temp_dict)
                            return geo_json

                        geo_json_markers = get_json_nota(base_df)

                        geojson_obj = folium.GeoJson(geo_json_markers, show = False, overlay =True).add_to(mp)


                        def get_json_centroide(df):
                            geo_json = {
                            "type": "FeatureCollection",
                            "features":[]
                            }

                            for i,row in df.iterrows():
                                temp_dict = {
                                "type": "Feature",
                                "geometry": {
                                    "type": "Point",
                                    "coordinates":[row['LONGITUDE'], row['LATITUDE']],

                                },"properties": {"Viatura": row['PACOTE']}
                                }
                                geo_json["features"].append(temp_dict)
                            return geo_json

                        geo_json_c_markers = get_json_centroide(centroides)

                        geojson_obj_c = folium.GeoJson(geo_json_c_markers, show = False, overlay =True).add_to(mp)



                        def get_json_centroide_utd(df):
                            geo_json = {
                            "type": "FeatureCollection",
                            "features":[]
                            }

                            for i,row in df.iterrows():
                                temp_dict = {
                                "type": "Feature",
                                "geometry": {
                                    "type": "Point",
                                    "coordinates":[row['LONGITUDE'], row['LATITUDE']],

                                },"properties": {"UTD": row['UTD']}
                                }
                                geo_json["features"].append(temp_dict)
                            return geo_json

                        geo_json_utd_markers = get_json_centroide_utd(centroides_utd)

                        geojson_obj_utd = folium.GeoJson(geo_json_utd_markers, show = False, overlay =True).add_to(mp)



                        servicesearch = Search(
                                layer=geojson_obj,
                                search_label='nota',
                                placeholder='Procure uma Nota',
                                collapsed=False,
                                search_zoom = 20
                            ).add_to(mp)

                        servicesearch_centroide = Search(
                                layer=geojson_obj_c,
                                search_label='Viatura',
                                placeholder='Procure um Pacote',
                                collapsed=False,
                                search_zoom = 14
                            ).add_to(mp)

                        #servicesearch_centroide_utd = Search(
                        #        layer=geojson_obj_utd,
                        #        search_label='UTD',
                        #        placeholder='Procure uma UTD',
                        #        collapsed=False,
                        #        search_zoom = 8
                        #    ).add_to(mp)

                        folium.LayerControl().add_to(mp)
                        #mp.save("2teste.html")
                        if st.session_state.exibir_mini_mapa == "SIM":
                            minimap = plugins.MiniMap(toggle_display=True)
                            mp.add_child(minimap)
                        plugins.Fullscreen(position='topright').add_to(mp)
                        draw = plugins.Draw(export=False)
                        draw.add_to(mp)
                        

                        
                        template = """
                        {% macro html(this, kwargs) %}

                        <!doctype html>
                        <html lang="en">
                        <head>
                        <meta charset="utf-8">
                        <meta name="viewport" content="width=device-width, initial-scale=1">
                        <title>jQuery UI Draggable - Default functionality</title>
                        <link rel="stylesheet" href="//code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css">

                        <script src="https://code.jquery.com/jquery-1.12.4.js"></script>
                        <script src="https://code.jquery.com/ui/1.12.1/jquery-ui.js"></script>
                        
                        <script>
                        $( function() {
                            $( "#maplegend" ).draggable({
                                            start: function (event, ui) {
                                                $(this).css({
                                                    right: "auto",
                                                    top: "auto",
                                                    bottom: "auto"
                                                });
                                            }
                                        });
                        });

                        </script>
                        </head>
                        <body>

                        
                        <div id='maplegend' class='maplegend' 
                            style='position: fixed; z-index:-9999; border:2px solid grey; background-color:rgba(255, 255, 255, 0.8);
                            border-radius:6px; padding: 10px; font-size:14px; right: 20px; bottom: 20px;'>
                        <div class='legend-title'>
                        """
                        
                        template_1_1 = """</div>
                        <div class='legend-scale'>
                        <ul class='legend-labels'>"""
                        
                        template_2 = """
                            
                            
                        

                        </ul>
                        </div>
                        </div>
                        
                        </body>
                        </html>

                        <style type='text/css'>
                        .maplegend .legend-title {
                            text-align: left;
                            margin-bottom: 5px;
                            font-weight: bold;
                            font-size: 90%;
                            }
                        .maplegend .legend-scale ul {
                            margin: 0;
                            margin-bottom: 5px;
                            padding: 0;
                            float: left;
                            list-style: none;
                            }
                        .maplegend .legend-scale ul li {
                            font-size: 80%;
                            list-style: none;
                            margin-left: 0;
                            line-height: 18px;
                            margin-bottom: 2px;
                            }
                        .maplegend ul.legend-labels li span {
                            display: block;
                            float: left;
                            height: 16px;
                            width: 30px;
                            margin-right: 5px;
                            margin-left: 0;
                            border: 1px solid #999;
                            }
                        .maplegend .legend-source {
                            font-size: 80%;
                            color: #777;
                            clear: both;
                            }
                        .maplegend a {
                            color: #777;
                            }
                        </style>
                        {% endmacro %}"""
                        template = template +titulo_legenda +template_1_1 + lgnd + template_2
                        template_st = template.replace("{% endmacro %}","")
                        template_st = template_st.replace("{% macro html(this, kwargs) %}","")
                        
                        macro = MacroElement()
                        macro._template = Template(template)

                        mp.get_root().add_child(macro)
                        if st.session_state.exibir_legenda == "SIM":
                            st.markdown(template_st, unsafe_allow_html=True)
                        #st.markdown(template_st, unsafe_allow_html=True)
                #st.write(st.session_state.base)      
    if st.session_state.pagina_mapa == "Mapa Seleção":
        try:
            cl_mapa_1,cl_mapa_2,cl_mapa_3 = st.columns([1,100,1])
            cl_mapa_1.write("")
            cl_mapa_3.write("")
            with cl_mapa_2:
                #folium_static(mp,width=1300,height=900)
                
                folium_static(mp,width=st.session_state.larg_mapa,height=st.session_state.alt_mapa)
            botao_salvar_mapa = st.button('Baixar Mapa')
            if botao_salvar_mapa:
                ano_data_selecao = str(st.session_state.data_pedido_folium.year)
                dia_data_selecao = str(st.session_state.data_pedido_folium.day)
                mes_data_selecao = str(st.session_state.data_pedido_folium.month)
                if len(dia_data_selecao) == 1:
                    dia_data_selecao = '0' + dia_data_selecao
                if len(mes_data_selecao) == 1:
                    mes_data_selecao = '0' + mes_data_selecao
                mp.save('Selecao Turma({}) Carteira({}) UTD({}) {}.{}.{}.html'.format(st.session_state.turma,st.session_state.carteira,
                st.session_state.utd_folium,dia_data_selecao,mes_data_selecao,ano_data_selecao))
        except Exception as e:
            #st.write(e)
            st.error("Nenhuma nota selecionada (e criada) para a UTD para data informada.")

    elif st.session_state.pagina_mapa == "Mapa Suscetíveis":
        
        #st.session_state.opcao_visualizacao = ["CONTA CONTRATO","RUAS","BAIRROS","MUNICIPIOS","ZONAS","UTDS"]
        st.session_state.opcao_visualizacao = ["CONTA CONTRATO"]
        st.session_state.opcao_turma_suscetiveis = ["STC","EPS","PRONTIDAO"]
        st.session_state.opcao_carteira_suscetiveis = ["CORTE","RECORTE","DISJUNTOR","BAIXA"]
        with col_def_2:
            st.session_state.turma_suscetiveis = st.selectbox('Turma:', st.session_state.opcao_turma_suscetiveis)  
        with col_def_3:
            st.session_state.carteira_suscetiveis = st.selectbox('Carteira:', st.session_state.opcao_carteira_suscetiveis)  
        
        with col_def_4:
            st.session_state.visualizacao_suscetiveis = st.selectbox('Opção:', st.session_state.opcao_visualizacao)  
        with col_def_6:
            st.session_state.data_referencia_suscetiveis = st.date_input('Data Referencia:',disabled=True) #data hoje
        with col_def_5:
            st.session_state.utd_suscetiveis = st.selectbox('UTD:', st.session_state.opcao_utd) 
        with st.sidebar:
            st.markdown("<h3 style='text-align: center; color: #5C881A;'> MAPA DE SUSCETÍVEIS</h3>", unsafe_allow_html=True)
        with st.sidebar:
            botao_consulta_suscetiveis = st.button('Atualizar Consulta')
            if botao_consulta_suscetiveis:
                with st.spinner('Carregando...'):
                    coleta_suscetiveis()
        
        st.session_state.base_suscetiveis['quantile'] = pd.qcut(st.session_state.base_suscetiveis['PECLD'], 4, labels=False)
        
        base_df = st.session_state.base_suscetiveis
        #base_df['LATITUDE'] = base_df['LATITUDE'].str.replace(',','.')
        #base_df['LONGITUDE'] = base_df['LONGITUDE'].str.replace(',','.')
        base_df = base_df.dropna(subset = ['LATITUDE']).reset_index(drop = True)
        base_df['PECLD'] = base_df['PECLD'].fillna(0.0)
        total_total = str(len(base_df))
        #st.write(base_df)
        base_df_temp = base_df[(base_df['quantile'] == 0)].copy()
        base_df_temp = base_df_temp.reset_index(drop=True)
        maior_0 = str(int(max(base_df_temp['PECLD'])))
        menor_0 = str(int(min(base_df_temp['PECLD'])))
        total_0 = str(len(base_df_temp))
        tit_0 = menor_0 + "-" + maior_0
        base_df_temp = base_df[(base_df['quantile'] == 1)].copy()
        base_df_temp = base_df_temp.reset_index(drop=True)
        maior_1 = str(int(max(base_df_temp['PECLD'])))
        menor_1 = str(int(min(base_df_temp['PECLD'])))
        total_1 = str(len(base_df_temp))
        tit_1 = menor_1 + "-" + maior_1
        base_df_temp = base_df[(base_df['quantile'] == 2)].copy()
        base_df_temp = base_df_temp.reset_index(drop=True)
        maior_2 = str(int(max(base_df_temp['PECLD'])))
        menor_2 = str(int(min(base_df_temp['PECLD'])))
        total_2 = str(len(base_df_temp))
        tit_2 = menor_2 + "-" + maior_2
        base_df_temp = base_df[(base_df['quantile'] == 3)].copy()
        base_df_temp = base_df_temp.reset_index(drop=True)
        maior_3 = str(int(max(base_df_temp['PECLD'])))
        menor_3 = str(int(min(base_df_temp['PECLD'])))
        total_3 = str(len(base_df_temp))
        tit_3 = menor_3 + "-" + maior_3

        mp = folium.Map(location=[base_df.LATITUDE.mean(), 
                                base_df.LONGITUDE.mean()], zoom_start=8)
        #marker_cluster = MarkerCluster(maxClusterRadius=3).add_to(mp)
        folium.raster_layers.TileLayer('Open Street Map').add_to(mp)
        #folium.raster_layers.TileLayer(tiles = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',attr = 'Esri',name = 'Esri Satellite',overlay = True,control = True).add_to(mp)
        
        folium.raster_layers.TileLayer('Stamen Terrain').add_to(mp)

        for i, row in base_df.iterrows():            
            rank_conta = str(row['quantile'])
            if rank_conta  == '0' or rank_conta  == 0:
                cor = '#5C881A'
                cor_fundo = '#5C881A'
                cor_texto =  "#FFFFFF"
            elif rank_conta  == '1' or rank_conta  == 1:
                cor = '#0070C0'
                cor_fundo = '#0070C0'
                cor_texto =  "#FFFFFF"
            elif rank_conta  == '2' or rank_conta  == 2:
                cor = '#FFC000'
                cor_fundo = '#FFC000'
                cor_texto =  "#FFFFFF"
            elif rank_conta  == '3' or rank_conta  == '3':
                cor = '#FF5A00'
                cor_fundo = '#FF5A00'
                cor_texto =  "#FFFFFF"
            
            utd = row['UTD']
            conta_contrato = row['CONTA_CONTRATO']
            acao = row['ACAO']
            cnae = row['CNAE']
            bx_renda = row['BX_RENDA']
            rua= row['RUA']
            bairro = row['BAIRRO']
            local= row['MUNICIPIO']
            poligonal= row['ZONA']
            latitude = row['LATITUDE']
            longitude = row['LONGITUDE']
            pecld = int(row['PECLD'])
            if acao == "CORTE":
                tipo_nota = "CS"
            else:
                tipo_nota = "CA"
            legenda = '''

                <b>UTD:</b> {} <br>
                <b>Acao:</b> {} <br>
                <b>CNAE:</b> {} <br>
                <b>Conta Contrato:</b> {} <br>
                <b>Baixa Renda:</b> {} <br>
                
                <b>Rua:</b> {} <br>
                <b>Bairro:</b> {} <br>
                <b>Local:</b> {} <br>
                <b>Zona:</b> {} <br>
                <b>Latitude:</b> {} <br>
                <b>Longitude:</b> {} <br>
                <b>PECLD:</b> R${} <br>

                '''.format(utd,acao,cnae,conta_contrato,bx_renda,rua,bairro,local,poligonal,latitude,longitude,pecld)
            iframe = folium.IFrame(legenda,width=380, height=230)

           

            folium.Marker(location = [row['LATITUDE'],row['LONGITUDE']],
                                       popup=folium.Popup(iframe),
                        
                        icon=plugins.BeautifyIcon(icon="leaf",icon_shape="doughnut", number=tipo_nota, 
                            border_color= cor, background_color=cor_fundo,text_color=cor_texto,borderWidth=0.1)
                        
                                    ).add_to(mp)
        folium.LayerControl().add_to(mp)
        plugins.Fullscreen(position='topright').add_to(mp)
        draw = plugins.Draw(export=False)
        draw.add_to(mp)
        #st.error("Em construção")
        
        
        #st.write(maior_0 ,menor_0)
        #st.write(maior_1 ,menor_1)
        #st.write(maior_2 ,menor_2)
        #st.write(maior_3 ,menor_3)

        tit_0 = "<li><span style='background:#5C881A;'></span> R$" + menor_0 + "- R$" + maior_0 + "<br>" + total_0 + " Contratos</li>"
        tit_1 = "<li><span style='background:#0070C0;'></span> R$" + menor_1 + "- R$" + maior_1 + "<br>" + total_1 + " Contratos</li>"
        tit_2 = "<li><span style='background:#FFC000;'></span> R$" + menor_2 + "- R$" + maior_2 + "<br>" + total_2 + " Contratos</li>"
        tit_3 = "<li><span style='background:#FF5A00;'></span> R$" + menor_3 + "- R$" + maior_3 + "<br>" + total_3 + " Contratos</li>"

        legend_mapa_0 = """

        <div class='my-legend'>"""
        legend_mapa_1 = "<div class='legend-title'> Legenda Mapa UTD {} ({} suscetíveis a {}) </div>".format(str.lower(st.session_state.utd_suscetiveis),total_total,st.session_state.carteira_suscetiveis)
        legend_mapa_2 = """<div class='legend-scale'>
  <ul class='legend-labels'>"""

    #<li><span style='background:#F1EEF6;'></span>0 - 20%</li>
    #<li><span style='background:#BDC9E1;'></span>40%</li>
    #<li><span style='background:#74A9CF;'></span>60%</li>
    #<li><span style='background:#2B8CBE;'></span>80%</li>
    #<li><span style='background:#045A8D;'></span>100%</li>

        legend_mapa_3 = """
  </ul>
</div>

</div>

<style type='text/css'>
  .my-legend .legend-title {
    text-align: left;
    margin-bottom: 8px;
    margin-left: 12px;
    font-size: 90%;
    }
  .my-legend .legend-scale ul {
    margin: 0;
    padding: 0;
    float: left;
    list-style: none;
    }
  .my-legend .legend-scale ul li {
    display: block;
    float: left;
    width: 90px;
    margin-bottom: 3px;
    text-align: center;
    font-size: 80%;
    list-style: none;
    }
  .my-legend ul.legend-labels li span {
    display: block;
    float: left;
    height: 15px;
    width: 95px;
    }
  .my-legend .legend-source {
    font-size: 70%;
    color: #999;
    clear: both;
    }
  .my-legend a {
    color: #777;
    }
</style>
"""

        
        legend_mapa = legend_mapa_0 + legend_mapa_1 + legend_mapa_2 + tit_0+ tit_1 + tit_2 + tit_3 + legend_mapa_3
        
        #mp.get_root().html.add_child(folium.Element(legend_mapa))
        folium_static(mp,width=st.session_state.larg_mapa,height=st.session_state.alt_mapa)
        st.write(legend_mapa, unsafe_allow_html=True)

      
        
        mp.save("teste.html")

    elif st.session_state.pagina_mapa == "Mapa PECLD":
        with st.sidebar:
            st.markdown("<h3 style='text-align: center; color: #5C881A;'> MAPA DE PECLD</h3>", unsafe_allow_html=True)
        st.error("Em construção")
    #else:
        #st.error("Nenhuma nota selecionada (e criada) para a UTD")
    
    
if str.lower(st.session_state.pagina) == "mapa suscetiveis":
    
    st.session_state.opcao_turma = ["STC","EPS","PRONTIDAO"]
    st.session_state.opcao_carteira_suscetiveis = ["CORTE","RECORTE","DISJUNTOR","BAIXA"]
   
    
    
    #col_def_01,col_def_1,col_def_2,col_def_3,col_def_4,col_def_5,col_def_6,col_def_7,col_def_05  = st.columns([1,25,15,20,20,25,15,15,1])
    #col_def_01.write("")
    st.write("teste")
    with col_def_6:
        st.session_state.turma = st.selectbox('Turma:', st.session_state.opcao_turma)  
    with col_def_3:
        st.session_state.carteira = st.selectbox('Carteira:', st.session_state.opcao_carteira_suscetiveis)  
    with col_def_4:
        st.session_state.data_pedido_suscetiveis = st.date_input('Data Pedido:',disabled=False) #data hoje
    with col_def_2:
        st.session_state.utd_suscetiveis = st.selectbox('UTD:', st.session_state.opcao_utds) 
    
    if 'base_final_suscetiveis' not in st.session_state:
        with st.spinner('Carregando...'):
            tempo_inicial = time.time()
            coletar_suscetiveis_total()
            tempo_final = time.time() 
            duracao = tempo_final - tempo_inicial 
            st.write("Tempo Total: {}".format(duracao))
    
    st.session_state.base_suscetiveis_temp = st.session_state.base_final_suscetiveis[(st.session_state.base_final_suscetiveis['UTD'] == st.session_state.utd_suscetiveis) & (st.session_state.base_final_suscetiveis['TURMA'] == st.session_state.turma) & (st.session_state.base_final_suscetiveis['CARTEIRA'] == st.session_state.carteira)].copy()
    st.write(st.session_state.base_suscetiveis_temp)


if str.lower(st.session_state.pagina) == "mapa pecld":
    def consulta_geral_mapa_sql():
        txt_sql_consulta_geral = 'consulta_geral_pecld'
        consulta = ['sources/Sqls/'+ txt_sql_consulta_geral + '.sql']
        arquivo_sql_consulta_geral = open(consulta[0], encoding="utf-8")
        sql_consulta_geral = arquivo_sql_consulta_geral.read()
        arquivo_sql_consulta_geral.close()
        sql_consulta_geral = sql_consulta_geral
        connection_hana = dbapi.connect(address='BRNEO695',port='30015',user=st.session_state.usuario,password=st.session_state.senha,databasename='BNP',sslValidateCertificate=False)
        st.session_state.df_consulta_mapa = pd.read_sql(sql_consulta_geral, connection_hana)
        #st.caption(sql_consulta_geral) #comentar

    #with st.spinner('Carregando...'):
        #if 'df_consulta_mapa'  not in st.session_state:
                #consulta_geral_mapa_sql()
    with st.sidebar:
        st.session_state.lista_opcoes_mapa_pecld = ["UTD","MUNICIPIO"]
        st.session_state.categoria = st.selectbox('Selecione a Categoria:', st.session_state.lista_opcoes_mapa_pecld)
        #st.session_state.lista_utds = list(st.session_state.df_consulta_mapa.UTD.unique())
        #st.session_state.utd = st.selectbox('Selecione a UTD:', st.session_state.lista_utds)
        #st.session_state.df_consulta_mapa_temp = st.session_state.df_consulta_mapa[(st.session_state.df_consulta_mapa['UTD'] == st.session_state.utd)].copy()
        #st.session_state.df_consulta_mapa_temp = st.session_state.df_consulta_mapa_temp.reset_index(drop=True)
        #st.session_state.df_consulta_mapa_temp = st.session_state.df_consulta_mapa_temp.dropna().reset_index(drop=True)
        #st.session_state.qtd_total_temp = len(st.session_state.df_consulta_mapa_temp)
        #st.write(st.session_state.qtd_total_temp)
    col1, col2, col3 = st.columns([5,90,5])
    col1.write("")
    col3.write("")
    with col2:
        with st.spinner('Carregando...'):
            sql = """
            SELECT DISTINCT 
            SUM(PECLD_CONS) AS PECLD,
            PLA_CLI.MUNICIPIO AS mun
            FROM CLB142840.MPRED_HIST mh
            LEFT JOIN CLP123432.PLANILHAO_CLIENTE AS PLA_CLI 
            ON PLA_CLI.ZCGACCOUN = mh.ZCGACCOUN 
            WHERE DATA_CRIACAO BETWEEN ADD_DAYS(CURRENT_DATE, -7) AND CURRENT_DATE
            AND PECLD_CONS IS NOT NULL AND MUNICIPIO IS NOT NULL
            GROUP BY PLA_CLI.MUNICIPIO
            """
            connection_hana = dbapi.connect(address='BRNEO695',port='30015',user=st.session_state.usuario,password=st.session_state.senha,databasename='BNP',sslValidateCertificate=False)
            base_pecld_mun = pd.read_sql(sql,connection_hana)
            

            state_data = pd.read_excel('data_pecld.xlsx')
            state_data = pd.merge(state_data, base_pecld_mun, how = 'left', on='MUN')
            state_data['GEOCODIGO'] = state_data['GEOCODIGO'].astype(str)
            state_data = state_data.round({'PECLD': 2})
            state_data['PECLD'][334] = 0
            state_data['PECLD'][130] = 0
            state_data['PECLD'][70] = 0
            #st.write(state_data)
            with open('municipios_json.json') as jsonFile:
                jsonObject = json.load(jsonFile)
                state_geo =  jsonObject
                env = "features"
                script = "properties"
                for k1, v1 in state_geo.items():
                    if k1 == env:
                        for u in range(416):
                            for k2, v2 in v1[u].items():
                                if k2 == script:
                                    v2['PECLD'] = str(state_data['PECLD'][u])

                jsonFile.close()

            
            #state_data.columns = state_data.columns.str.replace(' ', '')
            #Criação do mapa centralizado no Brasil (14.2350° S, 51.9253° W)

            map = folium.Map(
                location=[-12.467141,-41.027963],
                tiles='cartodbpositron', #cartodbpositron, Stamen Terrain, Stamen Toner
                zoom_start=5.5,
            )
            #Colorindo o mapa
            choropleth = folium.Choropleth(
                geo_data=state_geo,
                data=state_data,
                columns=['GEOCODIGO', 'PECLD'],
                key_on='feature.properties.GEOCODIGO',
                fill_color='YlOrRd', #OrRd#'BuGn’, ‘BuPu’, ‘GnBu’, ‘OrRd’, ‘PuBu’, ‘PuBuGn’, ‘PuRd’, ‘RdPu’, ‘YlGn’, ‘YlGnBu’, ‘YlOrBr’, and ‘YlOrRd’.
                fill_opacity=0.7,
                line_opacity=0.5,
                line_color='black',
                highlight=True,
                legend_name='PECLD',
                
            ).add_to(map)

            # and finally adding a tooltip/hover to the choropleth's geojson
            folium.GeoJsonTooltip(['MUNICIPIO','PECLD']).add_to(choropleth.geojson)

            folium.LayerControl().add_to(map)


            folium_static(map,width=1100)
            



#-----------------------------------------------------------------------------------------------ATENA------------------------------------------------------------------------------------------------
if str.lower(st.session_state.pagina) == "atena" and st.session_state.check_login == 1:
    from sources.interface_selecao_cortes_streamlit import *
    st.session_state.objeto_atena = SelecaoLayout(usuario = st.session_state.usuario, senha = st.session_state.senha)
    with st.sidebar: # Menu lateral
        st.session_state.pagina_atena = option_menu("", [ "CONFIGURAÇÕES", "Seleção", "Mapa", "Dashboard","Sobre"],
                            icons=[ 'gear','coin', 'geo-alt','graph-up','info-circle'],
                            menu_icon="list", default_index=0,
                            styles={"container": {"padding": "5!important", "background-color": "#f0f2f6"},"icon": {"color": "#7F7F7F", "font-size": "25px"}, "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#93ac46"},"nav-link-selected": {"background-color": "#93ac46"},
        }
        )   
    if str.lower(st.session_state.pagina_atena) == "configurações" :
        st.markdown("<h5 style='text-align: center; color: #5C881A;'> CONFIGURAÇÃO - CLUSTERS</h5>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([20,60,20])
        col1.write("") ; col2.write("")
        col2.markdown("***")
        with col2:
            st.session_state.opcao_configuracao = st.selectbox('Selecione a fonte das configurações', ['IMPORTAR_MAPA','ARQUIVO_CSV'])
        col2.markdown("***")
        if st.session_state.opcao_configuracao == "IMPORTAR_MAPA":
            with col2:
                with st.form(key = "form_configuracoes"):
                    st.session_state.consulta_fonte = st.selectbox('Fonte Consulta:', ['Tabela Suscetiveis', 'Arquivo SQL'])
                    st.session_state.turma_consultar = st.selectbox('Turma:', ['STC', 'EPS'])
                    if st.session_state.turma_consultar == "STC":
                        st.session_state.carteira_consultar = st.selectbox('Selecione Carteira:', st.session_state.opcoes_suscetiveis_eps)
                    elif st.session_state.turma_consultar == "EPS":
                        st.session_state.carteira_consultar = st.selectbox('Selecione Carteira:', st.session_state.opcoes_suscetiveis_eps)

                    st.session_state.data_pedido_consultar = st.date_input('Data do pedido:',value = next_day)
                    submit = st.form_submit_button(label = "Importar Configurações (Mapa de Seleção)")
                    if submit:
                        st.session_state.objeto_atena = SelecaoLayout(usuario = st.session_state.usuario, senha = st.session_state.senha)
                        st.session_state.objeto_atena.importar_clusterconf(b=1)
                        st.session_state.check_configuracoes = 1
                    

                        if st.session_state.check_configuracoes == 1:  
                            st.success('Foram importadas {linhas} linhas de configuração'.format(linhas = st.session_state.conf.shape[0]))
                            st.markdown("***")  
                            st.markdown("<h5 style='text-align: left; color: #5C881A;'>BAIXAR CONFIGURAÇÕES:</h1>", unsafe_allow_html=True)
                            st.session_state.conf_csv = convert_df(st.session_state.conf)
                            st.download_button(label="Baixar configurações (csv)",data=st.session_state.conf_csv,file_name='Configuracao_Clusters.csv',mime='text/csv',)
                            st.markdown("***")  
                            st.markdown("<h5 style='text-align: left; color: #5C881A;'>MAPA (TABELA):</h1>", unsafe_allow_html=True)
                            selection = aggrid_interactive_table(df=st.session_state.conf)

        elif st.session_state.opcao_configuracao == "ARQUIVO_CSV":
            with col2:
                uploadedFile = st.file_uploader("Importar Configurações", type=['csv'],accept_multiple_files=False,key="fileUploader")
                if 'uploadedFile' not in st.session_state:
                    if uploadedFile is not None:
                        st.session_state.conf = csv_to_df(uploadedFile) 
                    
                        st.session_state.check_configuracoes = 1
                        if st.session_state.check_configuracoes == 1:  
                            st.markdown("***")  
                            st.markdown("<h5 style='text-align: left; color: #5C881A;'>MAPA (TABELA):</h1>", unsafe_allow_html=True)
                            selection = aggrid_interactive_table(df=st.session_state.conf)


    if str.lower(st.session_state.pagina) == "seleção" and st.session_state.check_login == 1 and st.session_state.check_configuracoes == 1:
        st.markdown("<h3 style='text-align: center; color: #5C881A;'>CONSULTA SUSCETÍVEIS E SELEÇÃO DE SERVIÇOS</h1>", unsafe_allow_html=True)

        st.markdown("***")

        with st.form(key = "form_consulta"):
            st.session_state.onde_consultar = st.selectbox('Onde Consultar:', ['Tabela Suscetiveis', 'Arquivo SQL'],disabled=True) #consulta
            st.text_input('Turma:',value=st.session_state.turma_consultar,disabled=True) #turma
            st.text_input('Carteira:',value=st.session_state.carteira_consultar,disabled=True) #carteira_sql
            st.date_input('Data do pedido:',value=st.session_state.data_pedido_consultar,disabled=True) #data_pedido
            submit = st.form_submit_button(label = "Realizar a Consulta")
            if submit:
                st.session_state.objeto_atena.consulta_selecao(b=1,usuario = st.session_state.usuario, senha = st.session_state.senha)       
        
        if st.session_state.check_consulta == 1:
            st.markdown("***")
            st.markdown("<h5 style='text-align: left; color: #5C881A;'>RESULTADO CONSULTA:</h1>", unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                st.text_input('Nome Consulta:',value=st.session_state.turma_consultar + "_" + st.session_state.carteira_consultar,disabled=True)
            with col2:
                st.text_input('Quantidade de Suscetíveis:',value=st.session_state.quatidade_suscetiveis,disabled=True)
            
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
                    st.session_state.objeto_atena.realizar_selecao_massiva( b = 1)
                    
                    st.write("ok")

    elif str.lower(st.session_state.pagina) == "seleção" and st.session_state.check_configuracoes == 0:
        st.error("NECESSÁRIO DEFINIR A CONFIGURAÇÃO DAS TURMAS E CARTEIRA")


elif st.session_state.pagina == "atena" and st.session_state.check_login == 0:
    st.error("NECESSÁRIO EFETUAR LOGIN")





if str.lower(st.session_state.pagina) == "reguladas":
    st.markdown("<h4 style='text-align: center; color: #5C881A;'> PROJETO PILOTO - GERAÇÃO COM BASE EM NOTAS REGULADAS </h4>", unsafe_allow_html=True)
    if 'base_reguladas' not in st.session_state:
        with st.spinner('Carregando...'):
            coletar_base_reguladas()
    #st.write(st.session_state.base_reguladas)
    mapa_reguladas_suscetiveis(base_reguladas = st.session_state.base_reguladas)
    
 
elif st.session_state.pagina == "reguladas" and st.session_state.check_login == 0:
    st.error("NECESSÁRIO EFETUAR LOGIN")




if 1 == 0:
    import streamlit as st
    from streamlit_option_menu import option_menu

    # 1=sidebar menu, 2=horizontal menu, 3=horizontal menu w/ custom menu
    EXAMPLE_NO = 3


    def streamlit_menu(example=1):
        if example == 1:
            # 1. as sidebar menu
            with st.sidebar:
                selected = option_menu(
                    menu_title="Main Menu",  # required
                    options=["Home", "Projects", "Contact"],  # required
                    icons=["house", "book", "envelope"],  # optional
                    menu_icon="cast",  # optional
                    default_index=0,  # optional
                )
            return selected

        if example == 2:
            # 2. horizontal menu w/o custom style
            selected = option_menu(
                menu_title=None,  # required
                options=["Home", "Projects", "Contact"],  # required
                icons=["house", "book", "envelope"],  # optional
                menu_icon="cast",  # optional
                default_index=0,  # optional
                orientation="horizontal",
            )
            return selected

        if example == 3:
            # 2. horizontal menu with custom style
            selected = option_menu(
                menu_title=None,  # required
                options=["Home", "Projects", "Contact"],  # required
                icons=["house", "book", "envelope"],  # optional
                menu_icon="cast",  # optional
                default_index=0,  # optional
                orientation="horizontal",
                styles={
                    "container": {"padding": "0!important", "background-color": "#fafafa"},
                    "icon": {"color": "orange", "font-size": "25px"},
                    "nav-link": {
                        "font-size": "25px",
                        "text-align": "left",
                        "margin": "0px",
                        "--hover-color": "#eee",
                    },
                    "nav-link-selected": {"background-color": "green"},
                },
            )
            return selected


    selected = streamlit_menu(example=EXAMPLE_NO)

    if selected == "Home":
        st.title(f"You have selected {selected}")
    if selected == "Projects":
        st.title(f"You have selected {selected}")
    if selected == "Contact":
        st.title(f"You have selected {selected}")