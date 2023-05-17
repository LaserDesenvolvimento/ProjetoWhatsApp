import sys
import csv
import cliente
import json
import acesso
from io import StringIO
import os

arquivo_dados = {}
DadosProcessamentoWhatsAppDTO = {}
separador = ';'

def processa_arquivo(arquivo):
    try:
        with open(arquivo, encoding='ANSI') as csvf:

            arquivo_csv = csv.DictReader(csvf, delimiter='|')

            for k, value in enumerate(arquivo_csv.fieldnames):
                arquivo_csv.fieldnames[k] = value.lower()

            for linha in arquivo_csv:
                chave = linha['codbarra2via']
                arquivo_dados[chave] = linha
    except FileNotFoundError:
        print("O arquivo não foi encontrado!")
        exit(1)
    except csv.Error as e:
        print(f"Erro na leitura do arquivo CSV: {e}")
        exit(1)
                
def insere_dados_whatsapp(id_os_whats, agenda_envio, qtde_minutos):
    try:
        cod_barra_2via = list(arquivo_dados.keys())[0]
        id_os_2via = cod_barra_2via[:8]
        id_os_eletronico = arquivo_dados[str(id_os_2via).zfill(8) + f'{(1):06}']['idoseletronico']

        dados_os = cliente.OsWhatsAppProcessamentoDTO(acesso.IniciaOsWhatsApp(id_os_whats, id_os_eletronico).replace('"',""))
        guid_os = dados_os.GuidOsWhatsAppEnvio

        id_comercial = arquivo_dados[str(id_os_2via).zfill(8) + f'{(1):06}']['idcomercial']
        id_interno = arquivo_dados[str(id_os_2via).zfill(8) + f'{(1):06}']['idinterno']
        busca_template = get_variavel_template(id_comercial, id_interno)

        for i in range(len(arquivo_dados)):
            variaveis_templates = []
            for x in range(len(busca_template)):
                variaveis_templates.append(arquivo_dados[str(id_os_2via).zfill(8) + f'{(i + 1):06}'][busca_template[x]])

            mensagem_template = [separador.join(variaveis_templates)]

            dados = cliente.DadosProcessamento(
                arquivo_dados[str(id_os_2via).zfill(8) + f'{(i + 1):06}']['guid'],
                arquivo_dados[str(id_os_2via).zfill(8) + f'{(i + 1):06}']['nome'],
                arquivo_dados[str(id_os_2via).zfill(8) + f'{(i + 1):06}']['contatodestino'],
                mensagem_template,
                arquivo_dados[str(id_os_2via).zfill(8) + f'{(i + 1):06}']['nrodocumento'],
                arquivo_dados[str(id_os_2via).zfill(8) + f'{(i + 1):06}']['codbarra2via'],
                arquivo_dados[str(id_os_2via).zfill(8) + f'{(i + 1):06}']['tradutor'],
                arquivo_dados[str(id_os_2via).zfill(8) + f'{(i + 1):06}']['codigopix'],
                arquivo_dados[str(id_os_2via).zfill(8) + f'{(i + 1):06}']['vencimento']
            )

            #Não foi colocado em snake_case, pois precisa seguir o mesmo nome da API
            DadosProcessamentoWhatsAppDTO["\"OsWhatsAppEnvio\""] = json.dumps(dados_os.__dict__)
            DadosProcessamentoWhatsAppDTO["\"DadosProcessamento\""] = json.dumps(dados.__dict__)

            dados_processamento_whats_replace = str(DadosProcessamentoWhatsAppDTO).replace("'","").replace("[", "").replace("]", "")
            acesso.InsereMensagemTemplate(dados_processamento_whats_replace, guid_os)

        os.system("cls")

        checa_processamento(id_os_whats, guid_os)

        #Verificar agendamento
        if agenda_envio == "S":
            acesso.AgendaEnvioOsWhatsApp(id_os_whats, qtde_minutos)
    
    except Exception as e:
        with open(".\\Logs.txt", "a", encoding="ANSI") as new_arq:
                new_arq.write(f"Ocorreu um erro: {str(e)}")
                print(f"Ocorreu um erro: {str(e)}")
                sys.exit(1)
        
def get_variavel_template(id_comercial, id_interno):
    try:
        variaveis_template = acesso.GetMensagemTemplate(id_comercial,id_interno)
    except TypeError:
        with open(".\\Logs.txt", "a", encoding="ANSI") as new_arq:
                new_arq.write("Erro: argumentos inválidos ou valor de retorno inválido")
                print("Erro: argumentos inválidos ou valor de retorno inválido")
                sys.exit(1)

    lista_variaveis_template=[]
    inicio = 0
    try:
        for key,value in enumerate(variaveis_template):
            if (value == '-'):
                inicio = key + 2
            if (value == ','):
                fim = key
                lista_variaveis_template.append(variaveis_template[inicio:fim])
            if (key+1 == len(variaveis_template)):
                fim = key+1
                lista_variaveis_template.append(variaveis_template[inicio:fim])
    except NameError:
        print("Erro: variáveis não definidas")
        return None
    except IndexError:
        print("Erro: índice fora do intervalo")
        return None

    return lista_variaveis_template

def checa_processamento(id_os_whats, guid_os):
    if os.path.isfile("Logs.txt"):
        acesso.EstornaOSWhatsApp(id_os_whats)
        print("Verificar arquivo Logs.txt!!")
        sys.exit(1)
    else:
        acesso.InformaTerminoProcessamento(guid_os)
