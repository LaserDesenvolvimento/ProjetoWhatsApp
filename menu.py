import acesso
import sys


def menu_inicial():
    opc = int(input('''

    1 - GetMensagemTemplate
    2 - GetMensagensTemplatesByIdComercial
    3 - Processamento Pendente
    4 - Estorna OSWhatsApp
    5 - Agendamento de Envio
    6 - Remove agendamento
    7 - Sair
    opcao:  '''))
    
    if opc == 1:
        idComercial = int(input('idComercial-> '))
        idInterno = int(input('idInterno-> '))
        acesso.GetMensagemTemplateMenu(idComercial,idInterno)        
    elif opc == 2:
        idComercial = int(input('idComercial-> '))
        acesso.GetMensagensTemplatesByIdComercialMenu(idComercial)
    elif opc == 3:
        acesso.GetOSProcessamentoPendente()
    elif opc == 4:
        estornaOS = int(input('idos-> '))
        acesso.EstornaOSWhatsApp(estornaOS)
    elif opc == 5:
        idos = int(input('idos-> '))
        qtdeMinutos = input('Quantidade de minutos-> ')
        acesso.AgendaEnvioOsWhatsAppMenu(idos, qtdeMinutos)
    elif opc == 6:
        estornaOS = int(input('idos-> '))
        acesso.RemoveAgendamentoEnvioOsWhatsApp(estornaOS)    
    elif opc == 7:
        sys.exit()
    else:
        print("opção invalida, tente novamente.\n") 