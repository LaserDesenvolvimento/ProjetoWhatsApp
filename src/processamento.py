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
    """
    Processa um arquivo CSV e armazena os dados em um dicionário, utilizando o campo CodBarra2Via como chave.

    Parâmetros:
    - arquivo (str): O caminho para o arquivo CSV a ser processado.
    """
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
    """
    Insere os dados do WhatsApp utilizando o dicionario gerado na função processa_arquivo e agenda o envio, se necessário.

    Args:
        id_os_whats (int): O ID da ordem de serviço do WhatsApp.
        agenda_envio (str): Indica se o envio deve ser agendado ou não ("S" ou "N").
        qtde_minutos (int): A quantidade de minutos para agendamento do envio.

    """
    try:
        # Obtém os dados necessários para inserir no WhatsApp
        cod_barra_2via = list(arquivo_dados.keys())[0]
        id_os_2via = cod_barra_2via[:8]
        id_os_eletronico = arquivo_dados[str(id_os_2via).zfill(8) + f'{(1):06}']['idoseletronico']

         # Inicia a ordem de serviço no WhatsApp
        dados_os = cliente.OsWhatsAppProcessamentoDTO(acesso.inicia_os_whatsapp(id_os_whats, id_os_eletronico).replace('"',""))
        guid_os = dados_os.GuidOsWhatsAppEnvio

        # Obtém as informações do template
        id_comercial = arquivo_dados[str(id_os_2via).zfill(8) + f'{(1):06}']['idcomercial']
        id_interno = arquivo_dados[str(id_os_2via).zfill(8) + f'{(1):06}']['idinterno']
        busca_template = get_variavel_template(id_comercial, id_interno)

        # Percorre os dados e insere na API
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

            # Prepara os dados para inserção
            DadosProcessamentoWhatsAppDTO["\"OsWhatsAppEnvio\""] = json.dumps(dados_os.__dict__)
            DadosProcessamentoWhatsAppDTO["\"DadosProcessamento\""] = json.dumps(dados.__dict__)
            dados_processamento_whats_replace = str(DadosProcessamentoWhatsAppDTO).replace("'","").replace("[", "").replace("]", "")

            # Insere a mensagem no WhatsApp
            acesso.insere_mensagem_template(dados_processamento_whats_replace, guid_os)

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
    """
    Obtém as variáveis de um template, exemplo (nome, vencimento, etc).

    Parâmetros:
        id_comercial (int): O ID comercial do template.
        id_interno (int): O ID interno do template.

    Returns:
        list: Retorna uma lista de variáveis do template.

    """
    try:
        # Obtém as variáveis do template
        variaveis_template = acesso.get_mensagem_template(id_comercial,id_interno)

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
    """
    Verifica o se o processamento foi concluido e informa o termino dele, caso o mesmo de erro é gerado um
    arquivo log e estornado a OS do WhatsApp.

    Parâmetros:
        id_os_whats (int): O ID da ordem de serviço do WhatsApp.
        guid_os (str): O GUID(IdIndividuo) da ordem de serviço do WhatsApp.

    """
    if os.path.isfile("Logs.txt"):
        # Estorna a ordem de serviço do WhatsApp e trata o arquivo de log
        acesso.estorna_os_whatsapp(id_os_whats)
        print("Verificar arquivo Logs.txt!!")
        sys.exit(1)
    else:
        # Informa o término do processamento
        acesso.informa_termino_processamento(guid_os)
