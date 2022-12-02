import sys
import acesso
import processamento
import menu


try:
    # arquivo = sys.argv[1] #CSV_AET001_AET002.csv
    # IdOS = sys.argv[2]
    # IdOSEletronico = sys.argv[3]
    # idcomercial = sys.argv[4]
    # idnterno = sys.argv[5]
    # agendaEnvio = sys.argv[6]
    # qtdeMinutos = sys.argv[7]

    arquivo = r'CSV_AET001_AET002.csv'
    IdOS = 1086189
    IdOSEletronico = 1029660
    idcomercial = 855
    idnterno = 20586
    agendaEnvio = "N"
    qtdeMinutos = "N"

    if IdOSEletronico == "N":
        IdOSEletronico = ""

    if qtdeMinutos == "N":
        qtdeMinutos = ""

    processamento.make_json(arquivo)
    processamento.arquivoJSON(IdOS, IdOSEletronico, idcomercial, idnterno, agendaEnvio, qtdeMinutos)
    
except:
    if 'arquivo' in locals() or 'IdOS' in locals() or 'IdOSEletronico' in locals():
        sys.exit()
    else:
        menu.menu_inicial()
