import sys
import acesso
import processamento
import menu

def main():
    try:
        #arquivo = r'CSV_AET001_AET002.csv'
        #IdOSWhats = 1116260
        #IdOSEletronico = 1115285
        #agendaEnvio = "N"
        #qtdeMinutos = "N"

        arquivo = sys.argv[1]
        IdOSWhats = sys.argv[2]
        IdOSEletronico = sys.argv[3]
        agendaEnvio = sys.argv[6]
        qtdeMinutos = sys.argv[7]

        processamento.make_json(arquivo)
        processamento.arquivoJSON(IdOSWhats, IdOSEletronico, agendaEnvio, qtdeMinutos)
    
    except IndexError:
        menu.menu_inicial()

if __name__ == '__main__':
    main()
