import sys
import acesso
import processaJSON


try:
    arquivo = r'CSV_AET001_AET002.csv'
    IdOS = 1086188
    IdOSEletronico = 1029660

except:
    acesso.menu()


csvFilePath = arquivo

processaJSON.make_json(arquivo)
processaJSON.arquivoJSON(processaJSON.ArquivoDados, IdOS, IdOSEletronico)
