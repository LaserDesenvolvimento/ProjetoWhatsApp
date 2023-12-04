import sys
import csv
import cliente
import json
import acesso
from io import StringIO
import os

arquivo_dados = {}
separador = ';'

def processa_arquivo(arquivo):
    try:
        with open(arquivo, encoding='ANSI') as csvf:
            # Lê o arquivo CSV como um dicionário
            arquivo_csv = csv.DictReader(csvf, delimiter='|')

            # Converte os nomes das colunas para letras minúsculas
            for k, value in enumerate(arquivo_csv.fieldnames):
                arquivo_csv.fieldnames[k] = value.lower()

            # Processa cada linha do arquivo e armazena os dados no dicionário
            for linha in arquivo_csv:
                chave = linha['codbarra2via']
                arquivo_dados[chave] = linha
    except FileNotFoundError:
        # Trata o erro de arquivo não encontrado
        print("O arquivo não foi encontrado!")
        exit(1)
    except csv.Error as e:
        # Trata o erro de leitura do arquivo CSV
        print(f"Erro na leitura do arquivo CSV: {e}")
        exit(1)
                
def insere_dados_whatsapp(id_os_whats, agenda_envio, qtde_minutos):
    try:
        # Obtém os dados necessários para inserir no WhatsApp
        cod_barra_2via = list(arquivo_dados.keys())[0]
        #id_os_2via = cod_barra_2via[:8]
        id_os_eletronico = arquivo_dados[cod_barra_2via]['idoseletronico']

         # Inicia a ordem de serviço no WhatsApp
        dados_os = cliente.OsWhatsAppProcessamentoDTO(acesso.inicia_os_whatsapp(id_os_whats, id_os_eletronico).replace('"',""))
        guid_os = dados_os.GuidOsWhatsAppEnvio

        # Obtém as informações do template
        id_comercial = arquivo_dados[cod_barra_2via]['idcomercial']
        id_interno = arquivo_dados[cod_barra_2via]['idinterno']
        busca_template = get_variavel_template(id_comercial, id_interno)

        # Setando as variaveis para iniciar a inserção dos dados
        dados_processamento_whats = []
        lote = 20
        total_casos = len(arquivo_dados)

        for i in range(total_casos):
            variaveis_templates = []
            cod_2via = list(arquivo_dados.keys())[i]
            
            for x in range(len(busca_template)):
                variaveis_templates.append(arquivo_dados[cod_2via][busca_template[x]])

            mensagem_template = separador.join(variaveis_templates).replace("[","").replace("]","")

            dados = cliente.DadosProcessamento(
                arquivo_dados[cod_2via]['guid'],
                arquivo_dados[cod_2via]['nome'],
                arquivo_dados[cod_2via]['contatodestino'],
                mensagem_template,
                arquivo_dados[cod_2via]['nrodocumento'],
                arquivo_dados[cod_2via]['codbarra2via'],
                arquivo_dados[cod_2via]['tradutor'],
                arquivo_dados[cod_2via]['codigopix'],
                arquivo_dados[cod_2via]['vencimento']
            )

            dados_os_json = json.dumps(dados_os.__dict__)
            dados_json = json.dumps(dados.__dict__)

            novo_dados_whatsapp = {
                "\"OsWhatsAppEnvio\"": dados_os_json,
                "\"DadosProcessamento\"": dados_json
            }

            dados_processamento_whats.append(novo_dados_whatsapp)

            if (i + 1) % lote == 0 or (i + 1) == total_casos:
                dados_json = str(dados_processamento_whats).replace("\'", "")

                acesso.insere_mensagem_template(dados_json, guid_os)
                dados_processamento_whats = []

        os.system("cls")

        # Verifica o processamento
        checa_processamento(id_os_whats, guid_os)

        #Verificar agendamento
        if agenda_envio == "S":
            acesso.agenda_envio_os_whatsapp(id_os_whats, qtde_minutos)
    
    except Exception as e:
        # Tratamento de erro e registro de log
        with open(".\\Logs.txt", "a", encoding="ANSI") as new_arq:
                new_arq.write(f"Ocorreu um erro: {str(e)}")
                print(f"Ocorreu um erro: {str(e)}")
                sys.exit(1)
        
def get_variavel_template(id_comercial, id_interno):
    try:
        # Obtém as variáveis do template
        variaveis_template = acesso.get_mensagem_template(id_comercial,id_interno)

        if not(variaveis_template is None):
            lista_variaveis_template=[]
            inicio = 0
            for key,value in enumerate(variaveis_template):
                if (value == '-'):
                    inicio = key + 2
                if (value == ','):
                    fim = key
                    lista_variaveis_template.append(variaveis_template[inicio:fim])
                if (key+1 == len(variaveis_template)):
                    fim = key+1
                    lista_variaveis_template.append(variaveis_template[inicio:fim])
    
            return lista_variaveis_template
        else:
            lista_variaveis_template = ""
            return lista_variaveis_template

    except TypeError:
        # Tratamento de erro e registro de log
        with open(".\\Logs.txt", "a", encoding="ANSI") as new_arq:
            new_arq.write("Erro: argumentos inválidos ou valor de retorno inválido")
            print("Erro: argumentos inválidos ou valor de retorno inválido")
            sys.exit(1)
            return None   
    
    except NameError:
        # Tratamento de erro e registro de log
        print("Erro: variáveis não definidas")
        return None
    except IndexError:
        print("Erro: índice fora do intervalo")
        return None

def checa_processamento(id_os_whats, guid_os):
    if os.path.isfile("Logs.txt"):
        # Estorna a ordem de serviço do WhatsApp e trata o arquivo de log
        acesso.estorna_os_whatsapp(id_os_whats)
        print("Verificar arquivo Logs.txt!!")
        sys.exit(1)
    else:
        # Informa o término do processamento
        acesso.informa_termino_processamento(guid_os)
