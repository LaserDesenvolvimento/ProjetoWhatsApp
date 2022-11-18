import csv
import cliente
import acesso
import json

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
        acesso.InsereMensagemTemplate(DadosProcessamentoReplace)

csvFilePath = r'CSV_AET001_AET002.csv'
make_json(csvFilePath)
arquivoJSON(ArquivoDados, IdOS, IdOSEletronico)
