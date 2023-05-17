import sys
import acesso
import processamento
import menu

def main():
    try:
        #arquivo = r'CSV_WhatsApp.csv'
        #id_os_whats = 1119743
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
