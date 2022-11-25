import csv
import cliente
import json
import acesso

ArquivoDados = {}
DadosProcessamentoWhatsAppDTO = {}
separador = ';'
teste = []

def make_json(csvFilePath):
    with open(csvFilePath, encoding='ANSI') as csvf:
        csvReader = csv.DictReader(csvf, delimiter='|')
       
        for rows in csvReader:
                key = rows['CodBarra2Via']
                ArquivoDados[key] = rows

def arquivoJSON(ArquivoDados, IdOS, IdOSEletronico):
    dadosOs = cliente.OsWhatsAppProcessamentoDTO(acesso.IniciaOsWhatsApp(IdOS, IdOSEletronico).replace('"',""))
    GuidOs = dadosOs.GuidOsWhatsAppEnvio
    jesus = GetvariavelTemplate()

    for i in range(len(ArquivoDados)): 
        for x in range(len(jesus)):
            teste.append(ArquivoDados[str(IdOSEletronico).zfill(8) + f'{(i + 1):06}'][jesus[x]])

        MensagemTemplate = [separador.join(teste)]      
        #print(result)      

        dados = cliente.DadosProcessamento(
            MensagemTemplate,#[json.dumps(jesus)],
            ArquivoDados[str(IdOSEletronico).zfill(8) + f'{(i + 1):06}']['CodBarra2Via'], 
            ArquivoDados[str(IdOSEletronico).zfill(8) + f'{(i + 1):06}']['vencimento'], 
            ArquivoDados[str(IdOSEletronico).zfill(8) + f'{(i + 1):06}']['Tradutor'], 
            ArquivoDados[str(IdOSEletronico).zfill(8) + f'{(i + 1):06}']['CodigoPix'], 
            ArquivoDados[str(IdOSEletronico).zfill(8) + f'{(i + 1):06}']['ContatoDestino'], 
    )

        DadosProcessamentoWhatsAppDTO["\"OsWhatsAppEnvio\""] = json.dumps(dadosOs.__dict__)
        DadosProcessamentoWhatsAppDTO["\"DadosProcessamento\""] = json.dumps(dados.__dict__)
        
        DadosProcessamentoReplace = str(DadosProcessamentoWhatsAppDTO).replace("'","").replace("[", "").replace("]", "")
        acesso.InsereMensagemTemplate(DadosProcessamentoReplace, GuidOs)

        teste.clear()


def GetvariavelTemplate():

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
 




            #fim = key+1

            #listaVariaveisTemplate.append(variaveisTemplate[inicio:fim])

    #return (listaVariaveisTemplate)

#GetvariavelTemplate()    