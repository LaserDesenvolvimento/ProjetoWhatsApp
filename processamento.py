import csv
import cliente
import json
import acesso
import os

ArquivoDados = {}
DadosProcessamentoWhatsAppDTO = {}
separador = ';'
VariaveisTemplates = []

def make_json(csvFilePath):
    with open(csvFilePath, encoding='ANSI') as csvf:
        csvReader = csv.DictReader(csvf, delimiter='|')
       
        for rows in csvReader:
                key = rows['CodBarra2Via']
                ArquivoDados[key] = rows

def arquivoJSON(IdOS, IdOSEletronico, idcomercial, idnterno, agendaEnvio, qtdeMinutos):
    dadosOs = cliente.OsWhatsAppProcessamentoDTO(acesso.IniciaOsWhatsApp(IdOS, IdOSEletronico).replace('"',""))
    GuidOs = dadosOs.GuidOsWhatsAppEnvio
    BuscaTemplate = GetvariavelTemplate(idcomercial, idnterno)

    for i in range(len(ArquivoDados)): 
        for x in range(len(BuscaTemplate)):
            VariaveisTemplates.append(ArquivoDados[str(IdOSEletronico).zfill(8) + f'{(i + 1):06}'][BuscaTemplate[x]])

        MensagemTemplate = [separador.join(VariaveisTemplates)]      

        dados = cliente.DadosProcessamento(
            ArquivoDados[str(IdOSEletronico).zfill(8) + f'{(i + 1):06}']['nome'],
            ArquivoDados[str(IdOSEletronico).zfill(8) + f'{(i + 1):06}']['ContatoDestino'],
            MensagemTemplate,
            ArquivoDados[str(IdOSEletronico).zfill(8) + f'{(i + 1):06}']['CodBarra2Via'], 
            ArquivoDados[str(IdOSEletronico).zfill(8) + f'{(i + 1):06}']['Tradutor'],
            ArquivoDados[str(IdOSEletronico).zfill(8) + f'{(i + 1):06}']['CodigoPix'],
            ArquivoDados[str(IdOSEletronico).zfill(8) + f'{(i + 1):06}']['vencimento']             
    )

        DadosProcessamentoWhatsAppDTO["\"OsWhatsAppEnvio\""] = json.dumps(dadosOs.__dict__)
        DadosProcessamentoWhatsAppDTO["\"DadosProcessamento\""] = json.dumps(dados.__dict__)
        
        DadosProcessamentoReplace = str(DadosProcessamentoWhatsAppDTO).replace("'","").replace("[", "").replace("]", "")
        acesso.InsereMensagemTemplate(DadosProcessamentoReplace, GuidOs)

        VariaveisTemplates.clear()

    os.system("cls")
    acesso.InformaTerminoProcessamento(GuidOs)
    if agendaEnvio == "S":
        acesso.AgendaEnvioOsWhatsApp(IdOS, qtdeMinutos)


def GetvariavelTemplate(idcomercial, idnterno):

    #idcomercial = 855
    #idnterno = 20586
    variaveisTemplate = acesso.GetMensagemTemplate(idcomercial,idnterno)
    listaVariaveisTemplate=[]
    for key,value in enumerate(variaveisTemplate):
        if (value == '-'):
            inicio = key+2
        if (value == ','):
            fim = key
            listaVariaveisTemplate.append(variaveisTemplate[inicio:fim])
        if (key+1 == len(variaveisTemplate)):
            fim = key+1
            listaVariaveisTemplate.append(variaveisTemplate[inicio:fim]) 

    return listaVariaveisTemplate
