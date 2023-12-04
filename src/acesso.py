import requests
import datetime
import json
import sys
import os
import senha


username = os.environ['username'] 
password = os.environ['password']

api = "https://levyauthserver.smarapd.com.br/connect/token"
data = {
"client_secret": os.environ['client_secret'],
"client_id": os.environ['client_id'],
"grant_type": "password",
"scope": "data_processing openid",
"username": username,
"password": password
}
r =  requests.post(url=api, data=data).json()
token ='Bearer ' + r['access_token']
headers = {'Authorization': token}

def get_mensagem_template(id_comercial, id_interno):
    url = 'https://levydataprocessing.smarapd.com.br/api/ProcessaTemplateOSWhatsApp/GetTemplateMessageByType'
    params = {'idComercial':id_comercial, 'idInterno':id_interno}
    resposta = requests.get(url, headers=headers, params=params)
    if(resposta.status_code == 200):
        templates = resposta.json()
        return templates['Observacao']
    else:
        print(resposta.text)
        sys.exit(1)

def get_mensagem_template_menu(id_comercial, id_interno):
    url = 'https://levydataprocessing.smarapd.com.br/api/ProcessaTemplateOSWhatsApp/GetTemplateMessageByType'
    params = {'idComercial':id_comercial, 'idInterno':id_interno}
    resposta = requests.get(url, headers=headers, params=params)
    if(resposta.status_code == 200):
        return(json.dumps(resposta.json(), indent=3))

    else:
        return(str(resposta.status_code))

def get_mensagens_templates_by_id_comercial_menu(id_comercial):
    url = 'https://levydataprocessing.smarapd.com.br/api/ProcessaTemplateOSWhatsApp/GetTemplateMessagesByIdComercial'
    params = {'idComercial':id_comercial}
    resposta = requests.get(url, headers=headers, params=params)
    if(resposta.status_code == 200):
        return(json.dumps(resposta.json(), indent=3))
    else:
        return(str(resposta.status_code))

def estorna_os_whatsapp(id_os_whats):
    url = 'https://levydataprocessing.smarapd.com.br/api/ProcessaTemplateOSWhatsApp/EstornaOSWhatsApp'
    params = {'idos':id_os_whats}
    resposta = requests.delete(url, headers=headers,params=params)
    if(resposta.status_code == 200):
        return(str(resposta.status_code))
    else:
        return(resposta.text)

def inicia_os_whatsapp(id_os_whats, id_os_eletronico):
    if (id_os_eletronico == ""):
        url = 'https://levydataprocessing.smarapd.com.br/api/ProcessaTemplateOSWhatsApp/IniciaOsWhatsApp'
        params = {'idos':id_os_whats}
        resposta = requests.post(url, headers=headers, params=params)           
    else:
        url = 'https://levydataprocessing.smarapd.com.br/api/ProcessaTemplateOSWhatsApp/IniciaOsWhatsApp'
        params = {'idos':id_os_whats,'idOsEletronico':id_os_eletronico}
        resposta = requests.post(url, headers=headers, params=params)
        
    if(resposta.status_code == 200):
        return resposta.text
    else:
        with open(".\\Logs.txt", "a", encoding="ANSI") as new_arq:
            new_arq.write(resposta.text)
            print("Status: " + str(resposta.status_code) + " " + resposta.text)
            sys.exit(1)
    
def insere_mensagem_template(processa_msg, guid_os):
    #url = 'https://levydataprocessing.smarapd.com.br/api/ProcessaTemplateOSWhatsApp/InsereMensagemTemplate'
    url = 'https://levydataprocessing.smarapd.com.br/api/ProcessaTemplateOSWhatsApp/InsereListMensagemTemplate'
    headersjson = {'Authorization': token, 'Content-Type': 'application/json'}

    # Converte para JSON
    msg_template = json.loads(processa_msg)

    resposta = requests.post(url, headers=headersjson, json=msg_template)

    # Verifica se msg_template['DadosProcessamento'] é uma lista de dicionários
    if isinstance(msg_template, list):
        for item in msg_template:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Obtém o timestamp atual
            if resposta.status_code == 200:
                resultado_msg = item.get('DadosProcessamento', {})  # Acessa os dados do dicionário
                with open(".\\ProcessamentoLogs.txt", "a", encoding="ANSI") as new_arq:
                    new_arq.write(f"Timestamp: {timestamp} - Cliente: {resultado_msg.get('Nome')} Telefone: {resultado_msg.get('ContatoDestino')} {resposta.text}\n")
                print(f"Timestamp: {timestamp} - Cliente: {resultado_msg.get('Nome')} Telefone: {resultado_msg.get('ContatoDestino')} Status: {resposta.status_code}")
            else:
                with open(".\\Logs.txt", "a", encoding="ANSI") as new_arq:
                    new_arq.write(f"Timestamp: {timestamp} - {resposta.text} GuidOsWhats: {guid_os}\n")

        return resposta.text

def get_os_processamento_pendente():
    url = 'https://levydataprocessing.smarapd.com.br/api/ProcessaTemplateOSWhatsApp/GetOSProcessamentoPendente'
    resposta = requests.get(url, headers=headers)
    if(resposta.status_code == 200):
        if (json.dumps(resposta.json(), indent=3)) == '[]':
            return("Não possui nenhuma OS pendente!")

        else:
            return(json.dumps(resposta.json(), indent=3))

    else:
        return(resposta.text)

def informa_termino_processamento(guid_os):
    url = 'https://levydataprocessing.smarapd.com.br/api/ProcessaTemplateOSWhatsApp/InformaTerminoProcessamento'
    params = {'guidOsWhatsAppEnvio':guid_os}
    
    resposta = requests.patch(url, headers=headers, params=params)

    if(resposta.status_code == 200):
        print(resposta.text)
    else:
        print(resposta.text)
        sys.exit(1)

def agenda_envio_os_whatsapp(id_os_whats, qtde_minutos):
    url = 'https://levydataprocessing.smarapd.com.br/api/ProcessaTemplateOSWhatsApp/AgendaEnvioOsWhatsApp'
    params = {'idos':id_os_whats,'qtdeMinutos':qtde_minutos}

    if qtde_minutos == "":
        params = {'idos':id_os_whats}
    else:
        params = {'idos':id_os_whats,'qtdeMinutos':qtde_minutos}

    resposta = requests.patch(url, headers=headers, params=params)

    if(resposta.status_code == 200):
        os.system("cls")
        print(resposta.text)
    else:
        print(resposta.text)
        sys.exit(1)

def agenda_envio_os_whatsapp_menu(id_os_whats, qtde_minutos):
    url = 'https://levydataprocessing.smarapd.com.br/api/ProcessaTemplateOSWhatsApp/AgendaEnvioOsWhatsApp'
    params = {'idos':id_os_whats,'qtdeMinutos':qtde_minutos}

    if qtde_minutos == "":
        params = {'idos':id_os_whats}
    else:
        params = {'idos':id_os_whats,'qtdeMinutos':qtde_minutos}

    resposta = requests.patch(url, headers=headers, params=params)

    if(resposta.status_code == 200):
        return(str(resposta.status_code))
    else:
        return(resposta.text)

def remove_agendamento_envio_os_whatsapp(id_os_whats):
    url = 'https://levydataprocessing.smarapd.com.br/api/ProcessaTemplateOSWhatsApp/RemoveAgendamentoEnvioOsWhatsApp'
    params = {'idos':id_os_whats}

    resposta = requests.patch(url, headers=headers, params=params)

    if(resposta.status_code == 200):
        return(resposta.text)
    else:
        return(resposta.text)