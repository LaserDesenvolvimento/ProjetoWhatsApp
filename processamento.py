import csv
import cliente
import json
import acesso
from io import StringIO
import os

ArquivoDados = {}
DadosProcessamentoWhatsAppDTO = {}
separador = ';'
VariaveisTemplates = []

def make_json(csvFilePath):
    try:
        with open(csvFilePath, encoding='ANSI') as csvf:

            csvReader = csv.DictReader(csvf, delimiter='|')

            for k, value in enumerate(csvReader.fieldnames):
                csvReader.fieldnames[k] = value.lower()

            for rows in csvReader:
                key = rows['codbarra2via']
                ArquivoDados[key] = rows
    except FileNotFoundError:
        print("O arquivo não foi encontrado!")
        exit(1)
    except csv.Error as e:
        print(f"Erro na leitura do arquivo CSV: {e}")
        exit(1)
                
def arquivoJSON(IdOSWhats, IdOSEletronico, agendaEnvio, qtdeMinutos):
    try:
        dadosOs = cliente.OsWhatsAppProcessamentoDTO(acesso.IniciaOsWhatsApp(IdOSWhats, IdOSEletronico).replace('"',""))
        GuidOs = dadosOs.GuidOsWhatsAppEnvio

        CodBarra2Via = list(ArquivoDados.keys())[0]
        IdOS = CodBarra2Via[:8]

        idcomercial = ArquivoDados[str(IdOS).zfill(8) + f'{(1):06}']['idcomercial']
        idnterno = ArquivoDados[str(IdOS).zfill(8) + f'{(1):06}']['idinterno']
        BuscaTemplate = GetvariavelTemplate(idcomercial, idnterno)

        for i in range(len(ArquivoDados)):
            VariaveisTemplates = []
            for x in range(len(BuscaTemplate)):
                VariaveisTemplates.append(ArquivoDados[str(IdOS).zfill(8) + f'{(i + 1):06}'][BuscaTemplate[x]])

            MensagemTemplate = [separador.join(VariaveisTemplates)]

            dados = cliente.DadosProcessamento(
                ArquivoDados[str(IdOS).zfill(8) + f'{(i + 1):06}']['nome'],
                ArquivoDados[str(IdOS).zfill(8) + f'{(i + 1):06}']['contatodestino'],
                MensagemTemplate,
                ArquivoDados[str(IdOS).zfill(8) + f'{(i + 1):06}']['codbarra2via'],
                ArquivoDados[str(IdOS).zfill(8) + f'{(i + 1):06}']['tradutor'],
                ArquivoDados[str(IdOS).zfill(8) + f'{(i + 1):06}']['codigopix'],
                ArquivoDados[str(IdOS).zfill(8) + f'{(i + 1):06}']['vencimento']
            )

            DadosProcessamentoWhatsAppDTO["\"OsWhatsAppEnvio\""] = json.dumps(dadosOs.__dict__)
            DadosProcessamentoWhatsAppDTO["\"DadosProcessamento\""] = json.dumps(dados.__dict__)

            DadosProcessamentoReplace = str(DadosProcessamentoWhatsAppDTO).replace("'","").replace("[", "").replace("]", "")
            acesso.InsereMensagemTemplate(DadosProcessamentoReplace, GuidOs)

        os.system("cls")

        acesso.InformaTerminoProcessamento(GuidOs)

        #Verificar agendamento
        if agendaEnvio == "S":
            acesso.AgendaEnvioOsWhatsApp(IdOS, qtdeMinutos)
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def GetvariavelTemplate(idcomercial, idnterno):
    try:
        variaveisTemplate = acesso.GetMensagemTemplate(idcomercial,idnterno)
    except TypeError:
        print("Erro: argumentos inválidos ou valor de retorno inválido")
        return None

    listaVariaveisTemplate=[]
    inicio = 0
    try:
        for key,value in enumerate(variaveisTemplate):
            if (value == '-'):
                inicio = key+2
            if (value == ','):
                fim = key
                listaVariaveisTemplate.append(variaveisTemplate[inicio:fim])
            if (key+1 == len(variaveisTemplate)):
                fim = key+1
                listaVariaveisTemplate.append(variaveisTemplate[inicio:fim])
    except NameError:
        print("Erro: variáveis não definidas")
        return None
    except IndexError:
        print("Erro: índice fora do intervalo")
        return None

    return listaVariaveisTemplate

