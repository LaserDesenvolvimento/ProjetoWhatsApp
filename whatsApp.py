import sys
import acesso
import processamento


try:
    arquivo = r'CSV_AET001_AET002.csv'
    IdOS = 1086189
    IdOSEletronico = 1029660

except:
    acesso.menu()


csvFilePath = arquivo

processamento.make_json(arquivo)
processamento.arquivoJSON(processamento.ArquivoDados, IdOS, IdOSEletronico)
