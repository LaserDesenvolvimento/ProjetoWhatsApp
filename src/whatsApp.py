import sys
import acesso
import processamento
import menu

def main():
    """
    Função principal que processa um arquivo, insere dados do WhatsApp e caso não seja passado nenhum paramentro exibe um menu.
    
    Parâmetros:
    - arquivo (str): O caminho para o arquivo a ser processado.
    - id_os_whats (str): O ID da ordem de serviço do WhatsApp.
    - agenda_envio (str): Indica se a mensagem deve ser agendado depois de x tempo, ou por 30 minutos pelo padrão.
    - qtde_minutos (str): A quantidade de minutos para o envio agendado.
    """
    try:
        #arquivo = r'C:\\Users\\rcrustiguel\\Documents\\GitHub\\ProjetoWhatsApp\\src\\CSV_WhatsApp.csv'
        #id_os_whats = 1132658
        #agenda_envio = "N"
        #qtde_minutos = "N"
        
        arquivo = sys.argv[1]
        id_os_whats = sys.argv[2]
        agenda_envio = sys.argv[3]
        qtde_minutos = sys.argv[4]

        processamento.processa_arquivo(arquivo)
        processamento.insere_dados_whatsapp(id_os_whats, agenda_envio, qtde_minutos)
    
    except IndexError:
        menu.menu()
        
if __name__ == '__main__':
    main()
