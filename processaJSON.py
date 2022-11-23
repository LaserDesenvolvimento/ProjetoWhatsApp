import csv
import cliente
import acesso
import json
import os

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


#idcomercial = 855
#templates = acesso.GetMensagensTemplatesByIdComercial(idcomercial)
#for key, obs in enumerate(templates):
#    print(templates[key]['IdInterno'])
#    print(templates[key]['Observacao'])
#    #for x in templates[key]['Observacao']:
#    print('\n')

if os.listdir("arquivos") == []:
    acesso.menu()
else:
    csvFilePath = r'arquivos/CSV_AET001_AET002.csv'
    make_json(csvFilePath)
    arquivoJSON(ArquivoDados, IdOS, IdOSEletronico)
    




