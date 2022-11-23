import csv
import cliente
import acesso
import json
import os
import sys

ArquivoDados = {}
DadosProcessamentoWhatsAppDTO = {}
IdOS = 1081878
IdOSEletronico = 1029660

def make_json(csvFilePath):
    with open(csvFilePath, encoding='ANSI') as csvf:
        csvReader = csv.DictReader(csvf, delimiter='|')
       
        for rows in csvReader:
                key = rows['CodBarra2Via']
                ArquivoDados[key] = rows

def arquivoJSON(ArquivoDados, IdOS, IdOSEletronico):
    dadosOs = cliente.OsWhatsAppProcessamentoDTO(acesso.IniciaOsWhatsApp(IdOS, IdOSEletronico).replace('"',""))
    GuidOs = dadosOs.GuidOsWhatsAppEnvio
    for i in range(len(ArquivoDados)):        
        dados = cliente.DadosProcessamento(
            ArquivoDados[str(IdOSEletronico).zfill(8) + f'{(i + 1):06}']['NomeConsorciado'],
            ArquivoDados[str(IdOSEletronico).zfill(8) + f'{(i + 1):06}']['CodBarra2Via'], 
            ArquivoDados[str(IdOSEletronico).zfill(8) + f'{(i + 1):06}']['Vencimento'], 
            ArquivoDados[str(IdOSEletronico).zfill(8) + f'{(i + 1):06}']['Tradutor'], 
            ArquivoDados[str(IdOSEletronico).zfill(8) + f'{(i + 1):06}']['CodigoPix'], 
            ArquivoDados[str(IdOSEletronico).zfill(8) + f'{(i + 1):06}']['ContatoDestino'], 
    )
        DadosProcessamentoWhatsAppDTO["\"OsWhatsAppEnvio\""] = json.dumps(dadosOs.__dict__)
        DadosProcessamentoWhatsAppDTO["\"DadosProcessamento\""] = json.dumps(dados.__dict__)
        
        DadosProcessamentoReplace = str(DadosProcessamentoWhatsAppDTO).replace("'","")
        acesso.InsereMensagemTemplate(DadosProcessamentoReplace, GuidOs)


idcomercial = 855
idnterno = 20586
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

print (listaVariaveisTemplate)



csvFilePath = r'arquivos/CSV_AET001_AET002.csv'
make_json(csvFilePath)
arquivoJSON(ArquivoDados, IdOS, IdOSEletronico)

#acesso.menu()
 






