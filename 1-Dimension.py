import streamlit as st
import pandas as pd
import humanize
import sqlite3
import numpy as np

#esconder os menus padrão
hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)

# conexão com base de dados criada no normaizer
conn = sqlite3.connect('firewall.db')
# na query usar aspas duplas
pa_trougthput = '''
                SELECT *
                FROM pa
                ORDER BY "Modelo", "App-ID firewall throughput", "Threat prevention throughput","IPSec VPN throughput";
                '''
#criar o dataframe para ser exibido
df = pd.read_sql(pa_trougthput, con=conn, )
# fechar a conexão com banco
conn.close()
#apresentar o dataframe no site
order = ['Modelo','App-ID firewall throughput',
        'Threat prevention throughput','IPSec VPN throughput',
        "Traffic - ', '0/100Gbps QSFP+/QSFP28", 'Traffic - 10/100/1000',
        'Traffic - 100/1000/10000', 'Traffic - 10Gbps SFP+',
        'Traffic - 1Gbps SFP', 'Traffic - 25Gbps SFP28',
        "Traffic - 4', '/1', 'Gbps QSFP+/QSFP28", "Traffic - 40/100Gbps QSFP+/QSFP', '8",
        'Traffic - 40/100Gbps QSFP+/QSFP28', '802.1q tags per device',
        '802.1q tags per physical interface', 'ARP table size per device',
        'Active and unique groups used in policy*', 'Address groups',
        'Address objects', 'App override rules', 'Base virtual systems',
        'Bidirectional Forwarding Detection (BFD) Sessions', 'Captive portal rules',
        'Clear text nodes per physical interface', 'Connections per second',
        'Custom App-ID signatures', 'Custom App-IDs (virtual system specific)',
        'DHCP relays*', 'DHCP servers', 'DSCP marking by policy',
        'Dataplane cache size for URL filtering', 'Decryption rules',
        'Default DIPP pool oversubscription*', 'Devices supported',
        'DoS protection rules', 'End-of-sale', 'FQDN address objects',
        'HSM Supported', 'IP-User mappings (data plane)',
        'IP-User mappings (management plane)', 'IPv4 forwarding table size*',
        'IPv6 forwarding table size*', 'IPv6 neighbor table size',
        'MAC table size per device', 'Management plane dynamic cache size',
        'Max ARP entries per broadcast domain', 'Max DAG IP addresses*',
        'Max IKE Peers', 'Max MAC entries per broadcast domain',
        'Max NAT rules (DIP)*', 'Max NAT rules (DIPP)', 'Max NAT rules (static)*',
        'Max SSL inbound certificates', 'Max SSL tunnels',
        'Max concurrent decryption sessions',
        'Max custom categories (virtual system specific)', 'Max custom categories',
        'Max interfaces (logical and physical)', 'Max number of DNS Domains per system',
        'Max number of IPs per system', 'Max number of URL per system',
        'Max number of assigned addresses', 'Max number of custom lists',
        'Max route maps per virtual router', 'Max routing peers (protocol dependent)',
        'Max security zones', 'Max sessions (IPv4 or IPv6)', 'Max translated IPs (DIP)',
        'Max translated IPs (DIPP)*', 'Max tunnels (SSL, IPSec, and IKE with XAUTH)',
        'Max virtual addresses', 'Max virtual systems*', 'Maximum SD-WAN virtual interfaces',
        'Maximum aggregate interfaces', 'Members per address group',
        'Members per service group', "Mgmt - ', '0Gbps high availability",
        'Mgmt - 10/100/1000 high availability', 'Mgmt - 10Gbps high availability',
        'Mgmt - 40Gbps high availability', 'Mgmt - out-of-band',
        'Monitored servers for User-ID', 'NAT rules', 'Number of QoS policies',
        'Number of User-ID agents', 'Physical interfaces supporting QoS',
        'Policy based forwarding rules', 'Replication (egress interfaces)',
        'Routes', 'SD-WAN IPSec tunnels', 'SD-WAN rules', 'SSL Decryption Broker',
        'SSL Port Mirror', 'SSL certificate cache (forward proxy)', 'Security profiles',
        'Security rule schedules', 'Security rules', 'Service groups', 'Service objects',
        'Shared custom App-IDs', 'Shortest check interval (min)',
        'Site to site (with proxy id)', 'Static entries - DNS proxy',
        'Subinterfaces supported', 'System total forwarding table size',
        'Tags per IP address', 'Tags per User*', 'Terminal server agents',
        'Total NAT rule capacity',
        'Total entries for allow list, block list and custom categories',
        'Tunnel content inspection rules', 'Virtual routers', 'Virtual wires'
        ]
df = df.reindex(columns=order)



#titulo da pagina
st.header(':blue[Firewall Dimension Tool]')
''' Selecione as opções abaixo para realizar um dimensionamento inicial de equipamentos NGFW Palo Alto Networks.
'''

#Entrada de troughput
st.write('**Selecione a topologia** *Entenda topologia como Gateway internet ou Gateway Leste/Oeste')

col1,col2,col3 = st.columns(3)
with col1:
    vel_lo = 0
    lo = st.selectbox('**Tipo de Gateway**', options=['Gateway internet', 'Gateway leste/oeste'])

    vel1 = 0
    link = st.slider(
        '**Adicione a quantidade de links (Internet/MPLS/P2P/outros)**',
        max_value = 10 
        )
    
count_link = 0
with col2:
    if lo =='Gateway leste/oeste':
        vel_lo = st.number_input('Adicione troghput do switch em MB:', max_value=20000)
    for i in range(link):
        count_link += 1
        vel = st.number_input('velocidade do link {} em MB'.format(i + 1), max_value = 30000)
        vel1 += vel
    


#apresentação de licenciamentos    
st.write('**Licenciamento: [Descrição de todas as licenças em português](https://docs-paloaltonetworks-com.translate.goog/pan-os/11-0/pan-os-admin/subscriptions/all-subscriptions?_x_tr_sl=en&_x_tr_tl=pt&_x_tr_hl=pt-BR&_x_tr_pto=wapp)**')

#tempo de licenciamento - validado o None
time_lic = st.selectbox('**Tempo de licenciamento desejado:**', options=[None,'1 ano', '3 anos', '5 anos'])
percentual = 0
if time_lic != None:
    percentual = st.number_input('**Previsão em percentual de Crescimento ANUAL**', max_value=100)

#entrada do panorama
col_pan1, col_pan2, col_pan3 = st.columns(3)
with col_pan1:
    st.write('**Plataforma de gerenciamento Panorama**')
with col_pan2:
    pan = st.selectbox('**Quantidade de licença Panorama**', options=[None,'até 25 NGFW', 'até 100 NGFW', 'até +1000 NGFW'])
with col_pan3:
    st.info('3 opções de licença: 25 NGFW, 100 NGFW, +1000 NGFW. Opções de upgrade disponível: 25>100, 100>+1.000 Disponível em appliance e VM.')

hiden_col1, hiden_col2 = st.columns([1,2])

colu1, colu2, colu3, colu4, colu5 = st.columns(5)
with colu1:
    url = st.radio('**URL Filtering**', ('no', 'yes'),horizontal=True)
    adv_url = st.radio('**Adv URL Filtering**',('no', 'yes'), horizontal=True)
    dns = st.radio('**DNS Security**', ('no' , 'yes'), horizontal=True)
with colu2:
    tp = st.radio('**Threat Prevention**', ('no', 'yes'),horizontal=True)
    adv_tp = st.radio('**Adv. T. Prevention**', ('no', 'yes'),horizontal=True)
    aut = st.radio('**AutoFocus**', ('no', 'yes'), horizontal=True)
with colu3:
    wf = st.radio('**WildFire**', ('no', 'yes'),horizontal=True)
    adv_wf = st.radio('**Adv WildFire**', ('no', 'yes'),horizontal=True)
    crt = st.radio('**Cortex Data Lake**', ('no', 'yes'), horizontal=True)
with colu4:
    iot = st.radio('**IoT Security**', ('no', 'yes'),horizontal=True)
    sdw = st.radio('**SDWAN**', ('no', 'yes'),horizontal=True)
    dlp = st.radio( '**DLP**', ('no', 'yes'), horizontal=True)
with colu5:
    gp = st.radio('**Global Protect**', ('no', 'yes'),horizontal=True)
    vs = st.radio('**Virtual System**', ('no', 'yes'),horizontal=True)
    saas = st.radio('**SaaS Security Inline**', ('no', 'yes'), horizontal=True)
with colu1:
    int_rj45 = st.number_input('**Interfaces RJ45 1GB**', max_value=20)
with colu2:
    int_SFP = st.number_input('**Interface SFP 1GB**', max_value=20)
with colu3:
    int_SFPP = st.number_input('**Interface SFP+ 10GB**', max_value=20)
with colu4:
    int_SFP25 = st.number_input('**Interface SFP+ 25GB**', max_value=20)
with colu5:
    int_sfp100 = st.number_input('**Interface SFP+ 100GB**', max_value=20)



# controlando as entradas de licença
vel1 = vel1/1000
vel_lo = vel_lo/1000
not_human= 1000 * 1000 * 1000 * (vel1 + vel_lo)
vel2 = humanize.naturalsize(not_human)
soma_total = 0 
perc_au = 0
vel_total = 0
if percentual != 0:
    aumento = not_human * percentual/100
    soma_perc = aumento + not_human

    aumento_2ano = soma_perc * percentual/100
    soma_perc1 = aumento_2ano + soma_perc
    aumento_total2 = aumento + aumento_2ano

    aumento_3ano = soma_perc1 * percentual/100
    soma_perc2 = aumento_3ano + soma_perc1
    aumento_total3 = aumento_total2 + aumento_3ano

    aumento_4ano = soma_perc2 * percentual/100
    soma_perc3 = aumento_4ano + soma_perc2
    aumento_total4 = aumento_total3 + aumento_4ano

    aumento_5ano = soma_perc3 * percentual/100
    soma_perc4 = aumento_5ano + soma_perc3
    aumento_total5 = aumento_total4 + aumento_5ano

    if time_lic == '1 ano':
        perc_au = humanize.naturalsize(aumento)
        soma_total = soma_perc
    if time_lic == '3 anos':
        perc_au = humanize.naturalsize(aumento_total3)
        soma_total = soma_perc2
    if time_lic == '5 anos':
        perc_au = humanize.naturalsize(aumento_total5)
        soma_total = soma_perc4
    
    vel_total = humanize.naturalsize(soma_total)

soma_total = soma_total/1000000000
if gp == 'yes':
    with hiden_col1:
        usuarios = st.number_input('**Total de usuarios Global Protect:**', max_value= 10000)
    with hiden_col2:
        st.error('**Global Protect requer quantidade de usuarios**')
if tp == 'yes' or adv_tp == 'yes' or adv_url == 'yes' or url == 'yes':
    label_1 = "Throughput Threat Prevention"
    if soma_total != 0:
        df_mask = df['Threat prevention throughput'] >= soma_total
        filter_df = df[df_mask].sort_values(by=['Threat prevention throughput'], ascending=True)
    else:
        vel1 = vel1 + vel_lo
        df_mask = df['Threat prevention throughput'] >= vel1
        filter_df = df[df_mask].sort_values(by=['Threat prevention throughput'], ascending=True) 
else:
    label_1 = "Throughput Firewall"
    if soma_total != 0:
        df_mask = df['App-ID firewall throughput'] >= soma_total
        filter_df = df[df_mask].sort_values(by=['App-ID firewall throughput'], ascending=True)
    else:
        vel1 = vel1 + vel_lo
        df_mask = df['App-ID firewall throughput'] >= vel1
        filter_df = df[df_mask].sort_values(by=['App-ID firewall throughput'], ascending=True)
    
    
with col3:
    link = st.metric(label='**{}**'.format(label_1), value=vel2)
    if time_lic != None:
        aum_link = st.metric('**% aumento pelo periodo de:{}**'.format(time_lic), value=perc_au)
        link_prev = st.metric('**Troughput somado ao % de crescimento:**', value=vel_total)
    st.info('A seleção de licenças alteram automaticamente a seleção de troughput do firewall')

if vs == 'yes':
    with hiden_col1:
        usuarios_vs = st.number_input('**Total de Virtual Systems:**', max_value= 10000)
    with hiden_col2:
        st.error('**Numero total de Virtual Systems requerido**')
    df["Max virtual systems*"].replace("-", np.nan, inplace=True)
    df['Max virtual systems*'] = pd.to_numeric(df['Max virtual systems*'], errors='coerce').astype('Int64')
    if usuarios_vs >= 2:
        df_mask = df['Max virtual systems*'] >= usuarios_vs
        filter_df = df[df_mask]


#controlando as entradas de interfaces
#interface rj45 de 1gb
df1 = filter_df
df1["Traffic - 10/100/1000"].replace("undefined", np.nan, inplace=True)
df1['Traffic - 10/100/1000'] = pd.to_numeric(df1['Traffic - 10/100/1000'], errors='coerce').astype('Int64')
if int_rj45 > 0:
    df_mask = df1['Traffic - 10/100/1000'] >= int_rj45
    filter_df1 = df1[df_mask]
else:
    filter_df1 = df1

filter_df1["Traffic - 10/100/1000"] = filter_df1["Traffic - 10/100/1000"].apply(str)
filter_df1["Traffic - 10/100/1000"].replace( '<NA>',"undefined", inplace=True)


#interface SFP 1GB
df2 = filter_df1
df2["Traffic - 1Gbps SFP"] = df2["Traffic - 1Gbps SFP"].str.replace("0/", '')
df2["Traffic - 1Gbps SFP"] = df2["Traffic - 1Gbps SFP"].str.replace("4/", '')
df2['Traffic - 1Gbps SFP'] = pd.to_numeric(df2['Traffic - 1Gbps SFP'], errors='coerce').astype('Int64')
if int_SFP > 0:
    df_mask = df2['Traffic - 1Gbps SFP'] >= int_SFP
    filter_df2 = df2[df_mask]
else:
    filter_df2 = df2

#interface SFP+ 10GB
df3 = filter_df2
df3['Traffic - 10Gbps SFP+'] = df3['Traffic - 10Gbps SFP+'].str.replace("0/", '')
df3['Traffic - 10Gbps SFP+'] = pd.to_numeric(df3['Traffic - 10Gbps SFP+'], errors='coerce').astype('Int64')
if int_SFPP > 0:
    df_mask = df3['Traffic - 10Gbps SFP+'] >= int_SFPP
    filter_df3 = df3[df_mask]
else:
    filter_df3 = df3

# interface Traffic - 25Gbps SFP28
df4 = filter_df3
df4['Traffic - 25Gbps SFP28'] = pd.to_numeric(df4['Traffic - 25Gbps SFP28']).astype('Int64')
if int_SFP25 > 0:
    df_mask = df4['Traffic - 25Gbps SFP28'] >= int_SFP25
    filter_df4 = df4[df_mask]
else:
    filter_df4 = df4

#interface 40gb 100gb
# corrigir apresentação final da tabela

df5 = filter_df4
replacers = {'None':'0','undefined':'0','4x40/100':'4.100','4X40':'4.40'}
df5['Traffic - 40/100Gbps QSFP+/QSFP28'] = df5['Traffic - 40/100Gbps QSFP+/QSFP28'].replace(replacers)
df5['Traffic - 40/100Gbps QSFP+/QSFP28'] = pd.to_numeric(df5['Traffic - 40/100Gbps QSFP+/QSFP28'], errors='coerce').astype('float64')

if int_sfp100 > 0:
    df_mask = df5['Traffic - 40/100Gbps QSFP+/QSFP28'] >= int_sfp100
    filter_df5 = df5[df_mask]
else:
    filter_df5 = df5


# filtro final
st.dataframe(filter_df5.T, use_container_width=False)


# relatorio final
st.subheader(':blue[Relatório de dimensionamento]')
if vel1 > 0 and tp == 'no' and adv_tp == 'no' and adv_url == 'no' and url == 'no':
    st.error('**Você não selecionou nenhuma licença relacionada a analise de trafego.**', icon="🚨")

col_rel1, col_rel2 = st.columns(2)
name = ''
try:
    name = filter_df5['Modelo'].iloc[0]
except:
    st.write('erro generico')

#paticularidades das escolhas
if name == 'PA-410':
    st.error('**{} Este equipamento não tem disco de log**'.format(name), icon="🚨")
    st.write()

with col_rel1:
    st.write('**Tipo de Gateway:**')
    st.write("**Modelo Selecionado:**")
    st.write('**Quantidade de Links:**')
    st.write('**Throughput:**')
    st.write('**Throughput + taxa crescimento total:**')
    st.write('**Tipo de taxa de tranferência**')

with col_rel2:
    st.write('**{}**'.format(lo))
    st.write('**{}**'.format(name))
    st.write("**{}**".format(count_link))
    st.write('**{}**'.format(vel2))
    st.write('**{}**'.format(vel_total))
    st.write('**{}**'.format(label_1))

# area de interfaces 
st.subheader(':blue[Tipo de interfaces Selecionadas]')
col_int1, col_int2 = st.columns(2)
with col_int1:
    if int_rj45 > 0:
        st.write('**Interfaces UTP RJ45 10/100/1000:**')
    if int_SFP > 0:
        st.write('**Interface Fibra SFP 1GB:**')
    if int_SFPP > 0 :
        st.write('**Interface SFP+ 10GB:**')
    if int_SFP25 > 0 :
        st.write('**Interface SFP28 25GB:**')
    if int_sfp100 > 0:
        st.write('**Interface QSFP+ 40/100GB:**')
with col_int2:
    if int_rj45 > 0:
        st.write('**{}**'.format(int_rj45))
    if int_SFP > 0:
        st.write('**{}**'.format(int_SFP))
    if int_SFPP > 0 :
        st.write('**{}**'.format(int_SFPP))
    if int_SFP25 > 0 :
        st.write('**{}**'.format(int_SFP25))
    if int_sfp100 > 0:
        st.write('**{}**'.format(int_sfp100))


# area de licenças
st.subheader(':blue[Licenças selecionadas:]')
itens_lic = [url, adv_url,tp,adv_tp,wf,adv_wf,dns,gp,saas,sdw,iot,dlp,crt] 
col_rel3, col_rel4 = st.columns(2)
with col_rel3:
    if time_lic != None:
        st.write('**Tempo de licenciamento: {}**'.format(time_lic))
    if pan != None:
        st.write('**Licenciamento Panorama: {}**'.format(pan))
    if gp == 'yes':
        st.write('**Global Protect : yes -- QT de usuarios: {}**'.format(usuarios))

    if url == 'yes':
        st.write('**Url Filtering : yes**')

    if adv_url == 'yes':
        st.write('**Advanced Url Filtering : yes**')

    if tp == 'yes':
        st.write('**Threat Prevention : yes**')

    if adv_tp == 'yes':
        st.write('**Advanced Threat Prevention : yes**')
    if wf == 'yes':
        st.write('**WildFire : yes**')

    if adv_wf == 'yes':
        st.write('**Advanced WildFire : yes**')

with col_rel4:
    if dns == 'yes':
        st.write('**DNS Security : yes**')

    if dlp == 'yes':
        st.write('**Data Loss Prevention : yes**')

    if crt == 'yes':
        st.write('**Cortex Data Lake: yes**')

    if sdw == 'yes':
        st.write('**PAN-OS SDWAN: yes**')

    if iot =='yes':
        st.write('**IoT Security: yes**')

    if saas == 'yes':
        st.write('**SaaS Security Inline: yes**')




# SDWAN - equipamento concentrador

# bundle de licenças

