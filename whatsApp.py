import sys
import acesso
import processamento
import menu

def main():
    try:
        arquivo = r'BancoCNH_WhatsApp.csv'
        IdOSWhats = 1116260
        agendaEnvio = "N"
        qtdeMinutos = "N"

        #arquivo = sys.argv[1]
        #IdOSWhats = sys.argv[2]
        #agendaEnvio = sys.argv[3]
        #qtdeMinutos = sys.argv[4]

        processamento.make_json(arquivo)
        processamento.arquivoJSON(IdOSWhats, agendaEnvio, qtdeMinutos)
    
    except IndexError:
        menu.menu()
        
if __name__ == '__main__':
    main()
