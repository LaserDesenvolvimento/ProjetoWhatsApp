import requests
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
    """
    Realiza um get do template do idComercial e idInterno passado por parâmetro.

    Parâmetros:
        id_comercial (str): O ID comercial da mensagem.
        id_interno (str): O ID interno da mensagem.

    Return:
        retorna somente o campo (Observacao), onde é utilizado na mensagem do template, caso 
        de erro na requisição o mesmo é finalizado e informado o erro.
    """
    url = 'https://levydataprocessing.smarapd.com.br/api/ProcessaTemplateOSWhatsApp/GetMensagemTemplate'
    params = {'idComercial':id_comercial, 'idInterno':id_interno}
    resposta = requests.get(url, headers=headers, params=params)
    if(resposta.status_code == 200):
        templates = resposta.json()
        return templates['Observacao']
    else:
        print(resposta.text)
        sys.exit(1)

def get_mensagem_template_menu(id_comercial, id_interno):
    """
    Recebe dois parametros para realizar o get da mensagem do templante.

    Parâmetros:
        id_comercial (str): O ID comercial da mensagem.
        id_interno (str): O ID interno da mensagem.

    Return:
        Retorna um JSON da requisição GET para ser exibido no menu, caso aconteça o erro é informado o status do mesmo.

    """
    url = 'https://levydataprocessing.smarapd.com.br/api/ProcessaTemplateOSWhatsApp/GetMensagemTemplate'
    params = {'idComercial':id_comercial, 'idInterno':id_interno}
    resposta = requests.get(url, headers=headers, params=params)
    if(resposta.status_code == 200):
        return(json.dumps(resposta.json(), indent=3))

    else:
        return(str(resposta.status_code))

def get_mensagens_templates_by_id_comercial_menu(id_comercial):
    """
    Obtém os modelos de template associados a um ID comercial usando uma solicitação GET.

    Parâmetros:
        id_comercial (str): O ID comercial.

    Return:
        Retorna o resultado em formato JSON para ser visualizado no menu.
    """
    url = 'https://levydataprocessing.smarapd.com.br/api/ProcessaTemplateOSWhatsApp/GetMensagensTemplatesByIdComercial'
    params = {'idComercial':id_comercial}
    resposta = requests.get(url, headers=headers, params=params)
    if(resposta.status_code == 200):
        return(json.dumps(resposta.json(), indent=3))
    else:
        return(str(resposta.status_code))

def estorna_os_whatsapp(id_os_whats):
    """
    Cancela uma ordem de serviço do WhatsApp usando uma solicitação DELETE.

    Parâmetros:
        id_os_whats (str): O ID da ordem de serviço do WhatsApp.

    Return:
        Retorna o status da requisição.    

    """
    url = 'https://levydataprocessing.smarapd.com.br/api/ProcessaTemplateOSWhatsApp/EstornaOSWhatsApp'
    params = {'idos':id_os_whats}
    resposta = requests.delete(url, headers=headers,params=params)
    if(resposta.status_code == 200):
        return(str(resposta.status_code))
    else:
        return(resposta.text)

def inicia_os_whatsapp(id_os_whats, id_os_eletronico):
    """
    Recebe dois parârametros para realizar a requisição de POST

    Parâmetros:
        id_os_whats (str): O ID da ordem de serviço do WhatsApp.
        id_os_eletronico (str): O ID da ordem de serviço eletrônico (opcional).

    Return:
        Retorna uma GUID de inicialização da OS do WhatsApp, ou caso aconteça um erro na requisição é cria um arquivo com o nome 
        "Logs.txt", informando os detalhes e o retorno da requisição.

    """                                                                                        
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
    """
    Recebe por parâmetros a mensagem em JSON e a guid de iniciação da OS, para a geração a mensagem
    de template e os dados variaveis.

    Parâmetros:
        processa_msg (str): O modelo de mensagem em formato JSON.
        guid_os (str): O GUID da ordem de serviço do WhatsApp.

    Return:
        Caso a requisição seja concluida, é gerado um arquivo "ProcessamentoLogs.txt", no qual é passado
        o nome do cliente, telefone, contato e a resposta da requisição. Se a requisição ocorreu um erro
        é gerado um arquivo com o nome "Logs.txt" onde é informado a resposta e GuidOsWhats da OS.        

    """
    url = 'https://levydataprocessing.smarapd.com.br/api/ProcessaTemplateOSWhatsApp/InsereMensagemTemplate'
    headersjson = {'Authorization': token, 'Content-Type': 'application/json'}

    msg_template = json.loads(processa_msg)
    resposta = requests.post(url, headers=headersjson, json=msg_template)
    resultado_msg = msg_template['DadosProcessamento']   
      
    if(resposta.status_code == 200):
        with open(".\\ProcessamentoLogs.txt", "a", encoding="ANSI") as new_arq:
            new_arq.write("Cliente: " + resultado_msg['Nome'] + " Telefone: " + resultado_msg['ContatoDestino'] + " " + resposta.text + '\n')
            print("Cliente: " + resultado_msg['Nome'], " Telefone: ", resultado_msg['ContatoDestino'], " Status: ", resposta.status_code)
            return resposta.text
    else:
        with open(".\\Logs.txt", "a", encoding="ANSI") as new_arq:
            new_arq.write(resposta.text + " GuidOsWhats: " + guid_os + '\n')
            print("Cliente: " + resultado_msg['Nome'], " Telefone: ", resultado_msg['ContatoDestino'], " Status: ", resposta.status_code)
            return resposta.text

def get_os_processamento_pendente():
    """
    Obtém as ordens de serviço de processamento pendentes usando uma solicitação GET.

    Return:
        Retorna em um JSON os casos que estão pendentes no sistema.

    """
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
    """
    Informa o término do processamento de uma ordem de serviço do WhatsApp usando uma solicitação PATCH.

    Parâmetros:
        guid_os (str): O GUID da ordem de serviço do WhatsApp.

    """
    url = 'https://levydataprocessing.smarapd.com.br/api/ProcessaTemplateOSWhatsApp/InformaTerminoProcessamento'
    params = {'guidOsWhatsAppEnvio':guid_os}
    
    resposta = requests.patch(url, headers=headers, params=params)

    if(resposta.status_code == 200):
        print(resposta.text)
    else:
        print(resposta.text)
        sys.exit(1)

def agenda_envio_os_whatsapp(id_os_whats, qtde_minutos):
    """
    Agenda o envio de uma ordem de serviço do WhatsApp usando uma solicitação PATCH.

    Parâmetros:
        id_os_whats (str): O ID da ordem de serviço do WhatsApp.
        qtde_minutos (str): A quantidade de minutos para agendar o envio (opcional).
    """
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
    """
    Agenda o envio de uma ordem de serviço do WhatsApp com opção de menu usando uma solicitação PATCH.

    Args:
        id_os_whats (str): O ID da ordem de serviço do WhatsApp.
        qtde_minutos (str): A quantidade de minutos para agendar o envio (opcional).

    Returns:
        str: O código de status da resposta em formato de string se for bem-sucedido, caso contrário, o texto da resposta.

    """
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
    """
    Remove o agendamento de envio de uma ordem de serviço do WhatsApp usando uma solicitação PATCH.

    Args:
        id_os_whats (str): O ID da ordem de serviço do WhatsApp.

    Returns:
        str: O texto da resposta.

    Raises:
        None
    """
    url = 'https://levydataprocessing.smarapd.com.br/api/ProcessaTemplateOSWhatsApp/RemoveAgendamentoEnvioOsWhatsApp'
    params = {'idos':id_os_whats}

    resposta = requests.patch(url, headers=headers, params=params)

    if(resposta.status_code == 200):
        return(resposta.text)
    else:
        return(resposta.text)