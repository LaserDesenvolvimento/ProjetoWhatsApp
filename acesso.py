import requests
import json
import json
import sys
import os
import senha

username = os.environ['username'] 
password = os.environ['password']



API = "https://levyauthserver.smarapd.com.br/connect/token"
data = {
"client_secret": "1EBB%lJ73D#F%mSm@r@pdF2$%wU5gT96SBS*F3Kkm5Drb$XgP",
"client_id": "22fc194-4827-4af0-9656-6a74047f4fe8",
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
        print(json.dumps(resposta.json(), indent=3))
    else:
        print(resposta.text)
    #menu()

def GetMensagensTemplatesByIdComercial(idComercial): #GET
    url = 'https://levydataprocessing.smarapd.com.br/api/ProcessaTemplateOSWhatsApp/GetMensagensTemplatesByIdComercial'
    params = {'idComercial':idComercial}
    resposta = requests.get(url, headers=headers, params=params)
    if(resposta.status_code == 200):
        #print(json.dumps(resposta.json(), indent=3))
        return resposta.json()
    else:
        print(resposta.text)
    #menu()

def EstornaOSWhatsApp(idos): #DELETE
    url = 'https://levydataprocessing.smarapd.com.br/api/ProcessaTemplateOSWhatsApp/EstornaOSWhatsApp'
    params = {'idos':idos}
    resposta = requests.delete(url, headers=headers,params=params)
    if(resposta.status_code == 200):
        print(json.dumps(resposta.json(), indent=3))
    else:
        print(resposta.text)
    #menu()

def IniciaOsWhatsApp(idos, idOsEletronico): #POST                                                                                         
        url = 'https://levydataprocessing.smarapd.com.br/api/ProcessaTemplateOSWhatsApp/IniciaOsWhatsApp'
        params = {'idos':idos,'idOsEletronico':idOsEletronico}
        resposta = requests.post(url, headers=headers, params=params)
        
        if(resposta.status_code == 200):
            return resposta.text
        else:
            print(resposta.text)
            sys.exit(1)
    
def InsereMensagemTemplate(processaMsg, GuidOs): #POST                                                                                    
    url = 'https://levydataprocessing.smarapd.com.br/api/ProcessaTemplateOSWhatsApp/InsereMensagemTemplate'
    headersjson = {'Authorization': token, 'Content-Type': 'application/json'}

    MsgTemplate = json.loads(processaMsg)
    resposta = requests.post(url, headers=headersjson, json=MsgTemplate)   
      
    if(resposta.status_code == 200):
            print(resposta.status_code)
            return resposta.text
    else:
        with open(".\\Logs.txt", "w", encoding="ANSI") as new_arq:
            new_arq.writelines(resposta.text + " GuidOsWhats:" + GuidOs)
            print(resposta.status_code)
            return resposta.text

def GetOSProcessamentoPendente(): #GET
    url = 'https://levydataprocessing.smarapd.com.br/api/ProcessaTemplateOSWhatsApp/GetOSProcessamentoPendente'
    resposta = requests.get(url, headers=headers)
    if(resposta.status_code == 200):
        print(json.dumps(resposta.json(), indent=3))
    else:
        print(resposta.text)
    #menu()

#a=1081878
#b=1029660
#jsonStr = json.dumps(dados.__dict__)
#print(DadosProcessamentoWhatsAppDTO)
#EstornaOSWhatsApp(a)
#IniciaOsWhatsApp(a, b)
#InsereMensagemTemplate(DadosProcessamentoWhatsAppDTO)
#GetOSProcessamentoPendente()
def menu():
    opc = int(input('''

1 - GetMensagemTemplate
2 - GetMensagensTemplatesByIdComercial
3 - Processamento Pendente
4 - Estorna OSWhatsApp
5 - Sair
opcao:  '''))
    if opc == 1:
        idComercial = int(input('idComercial-> '))
        idInterno = int(input('idInterno-> '))
        GetMensagemTemplate(idComercial,idInterno)
    elif opc == 2:
        idComercial = int(input('idComercial-> '))
        GetMensagensTemplatesByIdComercial(idComercial)
    elif opc == 3:
        GetOSProcessamentoPendente()
    elif opc == 4:
        estornaOS = int(input('idos-> '))
        EstornaOSWhatsApp(estornaOS)
    elif opc == 5:
        sys.exit()
    else:
        print("opção invalida, tente novamente.\n")
        
#menu()