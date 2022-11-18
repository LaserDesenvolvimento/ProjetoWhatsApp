import requests
import json
import json
import sys
#usuario = input("E-mail: ")
#senha = getpass.getpass("Senha: ")

API = "https://levyauthserver.smarapd.com.br/connect/token"
data = {
    "client_secret": "1EBB%lJ73D#F%mSm@r@pdF2$%wU5gT96SBS*F3Kkm5Drb$XgP",
    "client_id": "22fc194-4827-4af0-9656-6a74047f4fe8",
    "grant_type": "password",
    "scope": "data_processing openid",
    "username": "rogeriokamada@hotmail.com",
    "password": '@Crr3470'
}

r =  requests.post(url=API, data=data).json()
token ='Bearer ' + r['access_token']
headers = {'Authorization': token}

def GetMensagensTemplatesByIdComercial(idComercial): #GET
    url = 'https://levydataprocessing.smarapd.com.br/api/ProcessaTemplateOSWhatsApp/GetMensagensTemplatesByIdComercialidComercial'
    params = {'idComercial':idComercial}
    resposta = requests.get(url, headers=headers, params=params)

def EstornaOSWhatsApp(idos): #DELETE
    url = 'https://levydataprocessing.smarapd.com.br/api/ProcessaTemplateOSWhatsApp/EstornaOSWhatsApp'
    params = {'idos':idos}
    resposta = requests.delete(url, headers=headers,params=params)

def IniciaOsWhatsApp(idos, idOsEletronico): #POST                                                                                         
        url = 'https://levydataprocessing.smarapd.com.br/api/ProcessaTemplateOSWhatsApp/IniciaOsWhatsApp'
        params = {'idos':idos,'idOsEletronico':idOsEletronico}
        resposta = requests.post(url, headers=headers, params=params)
        
        if(resposta.status_code == 200):
            return resposta.text
        else:
            print(resposta.text)
            sys.exit(1)
    
def InsereMensagemTemplate(processaMsg): #POST                                                                                    
    url = 'https://levydataprocessing.smarapd.com.br/api/ProcessaTemplateOSWhatsApp/InsereMensagemTemplate'
    headersjson = {'Authorization': token, 'Content-Type': 'application/json'}

    MsgTemplate = json.loads(processaMsg)
    resposta = requests.post(url, headers=headersjson, json=MsgTemplate)   

    if(resposta.status_code == 200):
            print(resposta.status_code)
            return resposta.text
    else:
        with open(".\\Logs.txt", "w", encoding="ANSI") as new_arq:
            new_arq.writelines(resposta.text)
            print(resposta.status_code)
            return resposta.text

def GetOSProcessamentoPendente(): #GET
    url = 'https://levydataprocessing.smarapd.com.br/api/ProcessaTemplateOSWhatsApp/GetOSProcessamentoPendente'
    resposta = requests.get(url, headers=headers)

#a=1081878
#b=1029660

#jsonStr = json.dumps(dados.__dict__)
#print(DadosProcessamentoWhatsAppDTO)
#EstornaOSWhatsApp(a)
#IniciaOsWhatsApp(a, b)
#InsereMensagemTemplate(DadosProcessamentoWhatsAppDTO)
#GetOSProcessamentoPendente()