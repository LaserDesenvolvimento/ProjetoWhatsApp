import requests
import json
import sys
import os
import menu
import senha


username = os.environ['username'] 
password = os.environ['password']

API = "https://levyauthserver.smarapd.com.br/connect/token"
data = {
"client_secret": os.environ['client_secret'],
"client_id": os.environ['client_id'],
"grant_type": "password",
"scope": "data_processing openid",
"username": username,
"password": password
}
r =  requests.post(url=API, data=data).json()
token ='Bearer ' + r['access_token']
headers = {'Authorization': token}



def GetMensagemTemplate(idComercial, idInterno): #GET
    url = 'https://levydataprocessing.smarapd.com.br/api/ProcessaTemplateOSWhatsApp/GetMensagemTemplate'
    params = {'idComercial':idComercial, 'idInterno':idInterno}
    resposta = requests.get(url, headers=headers, params=params)
    if(resposta.status_code == 200):
        templates = resposta.json()
        return templates['Observacao']
    else:
        print(resposta.text)
        sys.exit(1)

def GetMensagemTemplateMenu(idComercial, idInterno): #GET MENU
    url = 'https://levydataprocessing.smarapd.com.br/api/ProcessaTemplateOSWhatsApp/GetMensagemTemplate'
    params = {'idComercial':idComercial, 'idInterno':idInterno}
    resposta = requests.get(url, headers=headers, params=params)
    if(resposta.status_code == 200):
        return(json.dumps(resposta.json(), indent=3))

    else:
        return(str(resposta.status_code))

def GetMensagensTemplatesByIdComercial(idComercial): #GET
    url = 'https://levydataprocessing.smarapd.com.br/api/ProcessaTemplateOSWhatsApp/GetMensagensTemplatesByIdComercial'
    params = {'idComercial':idComercial}
    resposta = requests.get(url, headers=headers, params=params)
    if(resposta.status_code == 200):
        return resposta.json()
    else:
        print(resposta.text)
        sys.exit(1)

def GetMensagensTemplatesByIdComercialMenu(idComercial): #GET Menu
    url = 'https://levydataprocessing.smarapd.com.br/api/ProcessaTemplateOSWhatsApp/GetMensagensTemplatesByIdComercial'
    params = {'idComercial':idComercial}
    resposta = requests.get(url, headers=headers, params=params)
    if(resposta.status_code == 200):
        return(json.dumps(resposta.json(), indent=3))
    else:
        return(resposta.text)

def EstornaOSWhatsApp(idos): #DELETE
    url = 'https://levydataprocessing.smarapd.com.br/api/ProcessaTemplateOSWhatsApp/EstornaOSWhatsApp'
    params = {'idos':idos}
    resposta = requests.delete(url, headers=headers,params=params)
    if(resposta.status_code == 200):
        return(str(resposta.status_code))
    else:
        return(resposta.text)

def IniciaOsWhatsApp(idos, idOsEletronico): #POST                                                                                         
        if (idOsEletronico == ""):
            url = 'https://levydataprocessing.smarapd.com.br/api/ProcessaTemplateOSWhatsApp/IniciaOsWhatsApp'
            params = {'idos':idos}
            resposta = requests.post(url, headers=headers, params=params)           
        else:
            url = 'https://levydataprocessing.smarapd.com.br/api/ProcessaTemplateOSWhatsApp/IniciaOsWhatsApp'
            params = {'idos':idos,'idOsEletronico':idOsEletronico}
            resposta = requests.post(url, headers=headers, params=params)
        
        if(resposta.status_code == 200):
            return resposta.text
        else:
            with open(".\\Logs.txt", "a", encoding="ANSI") as new_arq:
                new_arq.write(resposta.text)
                print("Status: " + str(resposta.status_code) + " " + resposta.text)
                sys.exit()
    
def InsereMensagemTemplate(processaMsg, GuidOs): #POST                                                                                    
    url = 'https://levydataprocessing.smarapd.com.br/api/ProcessaTemplateOSWhatsApp/InsereMensagemTemplate'
    headersjson = {'Authorization': token, 'Content-Type': 'application/json'}

    MsgTemplate = json.loads(processaMsg)
    resposta = requests.post(url, headers=headersjson, json=MsgTemplate)
    resultMsg = MsgTemplate['DadosProcessamento']   
      
    if(resposta.status_code == 200):
        with open(".\\ProcessamentoLogs.txt", "a", encoding="ANSI") as new_arq:
            new_arq.write("Cliente: " + resultMsg['Nome'] + " Telefone: " + resultMsg['ContatoDestino'] + " " + resposta.text + '\n')
            print("Cliente: " + resultMsg['Nome'], " Telefone: ", resultMsg['ContatoDestino'], " Status: ", resposta.status_code)
            return resposta.text
    else:
        with open(".\\Logs.txt", "a", encoding="ANSI") as new_arq:
            new_arq.write(resposta.text + " GuidOsWhats: " + GuidOs + '\n')
            print("Cliente: " + resultMsg['Nome'], " Telefone: ", resultMsg['ContatoDestino'], " Status: ", resposta.status_code)
            return resposta.text

def GetOSProcessamentoPendente(): #GET
    url = 'https://levydataprocessing.smarapd.com.br/api/ProcessaTemplateOSWhatsApp/GetOSProcessamentoPendente'
    resposta = requests.get(url, headers=headers)
    if(resposta.status_code == 200):
        if (json.dumps(resposta.json(), indent=3)) == '[]':
            #os.system("cls")
            return("Não possui nenhuma OS pendente!")
            #os.system("pause")
            #os.system("cls")
        else:    
            #os.system("cls")
            return(json.dumps(resposta.json(), indent=3))
            #os.system("pause")
            #os.system("cls")

    else:
        return(resposta.text)
    #menu.menu_inicial()

def InformaTerminoProcessamento(GuidOs): #Patch
    url = 'https://levydataprocessing.smarapd.com.br/api/ProcessaTemplateOSWhatsApp/InformaTerminoProcessamento'
    params = {'guidOsWhatsAppEnvio':GuidOs}
    
    resposta = requests.patch(url, headers=headers, params=params)

    if(resposta.status_code == 200):
        print(resposta.text)
    else:
        print(resposta.text)
        sys.exit(1)

def AgendaEnvioOsWhatsApp(idos, qtdeMinutos): #Patch 
    url = 'https://levydataprocessing.smarapd.com.br/api/ProcessaTemplateOSWhatsApp/AgendaEnvioOsWhatsApp'
    params = {'idos':idos,'qtdeMinutos':qtdeMinutos}

    if qtdeMinutos == "":
        params = {'idos':idos}
    else:
        params = {'idos':idos,'qtdeMinutos':qtdeMinutos}

    resposta = requests.patch(url, headers=headers, params=params)

    if(resposta.status_code == 200):
        os.system("cls")
        print(resposta.text)
    else:
        print(resposta.text)
        sys.exit(1)

def AgendaEnvioOsWhatsAppMenu(idos, qtdeMinutos): #Patch Menu
    url = 'https://levydataprocessing.smarapd.com.br/api/ProcessaTemplateOSWhatsApp/AgendaEnvioOsWhatsApp'
    params = {'idos':idos,'qtdeMinutos':qtdeMinutos}

    if qtdeMinutos == "":
        params = {'idos':idos}
    else:
        params = {'idos':idos,'qtdeMinutos':qtdeMinutos}

    resposta = requests.patch(url, headers=headers, params=params)

    if(resposta.status_code == 200):
        return(str(resposta.status_code))
    else:
        return(resposta.text)      

def RemoveAgendamentoEnvioOsWhatsApp(idos):
    url = 'https://levydataprocessing.smarapd.com.br/api/ProcessaTemplateOSWhatsApp/RemoveAgendamentoEnvioOsWhatsApp'
    params = {'idos':idos}

    resposta = requests.patch(url, headers=headers, params=params)

    if(resposta.status_code == 200):
        return(resposta.text)
    else:
        return(resposta.text)