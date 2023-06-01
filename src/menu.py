import sys
import json
import acesso

from PyQt5.QtGui import QPalette, QColor, QIntValidator
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QGridLayout, QTableWidget, QTableWidgetItem, QStyleFactory
from PyQt5 import QtCore 
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMessageBox, QPushButton, QWidget, QSizePolicy

titulos_colunas = []

class janela_principal(QWidget):
    def __init__(self):
        """
        Inicializa a janela principal da aplicação.

        - Define o modo Dark
        - Obtém o processamento pendente do sistema operacional
        - Define o tamanho fixo da janela
        - Cria o layout da janela como grid
        - Cria e adiciona os botões ao layout
        - Cria a tabela e a atualiza com os dados do processamento pendente
        - Adiciona a tabela ao layout
        """
        super().__init__()

        # Modo Dark
        set_dark_mode(self)

        processamento_pendente = acesso.get_os_processamento_pendente()

        # Define o tamanho da janela principal
        self.setFixedSize(1200, 800)

        # Define o layout da janela principal como grid
        layout = QGridLayout()
        self.setLayout(layout)

        # Cria os botões e as caixas de texto e adiciona-os ao layout

        # Botão 1: Mensagem Template
        self.button_msg_template = QPushButton('Mensagem' + '\n' + 'Template', self)
        self.button_msg_template.setGeometry(QtCore.QRect(10, 10, 93, 48))
        self.button_msg_template.clicked.connect(self.janela_template)

        # Botão 2: Template Comercial                
        self.button_template_comercial = QPushButton('Template' + '\n' + 'Comercial', self)
        self.button_template_comercial.setGeometry(QtCore.QRect(10, 68, 93, 48))
        self.button_template_comercial.clicked.connect(self.janela_template_idcomercial)

        # Botão 3: Processamento Pendente
        self.button_pendente = QPushButton('Processamento' + '\n' + 'Pendente', self)
        self.button_pendente.setGeometry(QtCore.QRect(10, 126, 93, 48))
        self.button_pendente.clicked.connect(self.janela_processamento_pendente)

        # Botão 4: Estorna OSWhatsApp
        self.button_estorna = QPushButton('Estorna' + '\n' + 'OSWhatsApp', self)
        self.button_estorna.setGeometry(QtCore.QRect(10, 184, 93, 48))
        self.button_estorna.clicked.connect(self.janela_estorna)

        # Botão 5: Agendamento
        self.button_agendamento = QPushButton('Agendamento', self)
        self.button_agendamento.setGeometry(QtCore.QRect(10, 242, 93, 48))
        self.button_agendamento.clicked.connect(self.janela_agenda_envio)

        # Botão 6: Estorna Agendamento
        self.button_estorna_agendamento = QPushButton('Estorna' + '\n' + 'Agendamento', self)
        self.button_estorna_agendamento.setGeometry(QtCore.QRect(10, 300, 93, 48))
        self.button_estorna_agendamento.clicked.connect(self.janela_estorna_agendamento)

        cria_tabela(self)

        atualiza_tabela(self, processamento_pendente, "OS's Pendentes")

        layout.addWidget(self.tabela)
        layout.setAlignment(self.tabela, Qt.AlignRight)

    def janela_template(self):
        """
        Abre uma nova janela para a criação de uma mensagem template.

        - Cria a nova janela
        - Configura o título e tamanho fixo da janela
        - Exibe a janela
        - Configura o modo escuro na nova janela
        - Cria um layout para a nova janela
        - Adiciona botões e rótulos ao layout
        - Adiciona um botão "Concluído" ao layout
        - Conecta o sinal do botão "Concluído" ao método get_template
        """
        # Criação da nova janela        
        self.nova_janela = QWidget()
        self.nova_janela.setWindowTitle('Mensagem Template')
        self.nova_janela.setFixedSize(600,150)
        self.nova_janela.show()
        
        #Configuração do modo escuro
        set_dark_mode(self.nova_janela)
        
        layout = QGridLayout()
        self.nova_janela.setLayout(layout)

        # Botão e rótulo para o idComercial
        botao_template_idcomercial, self.label_idcomercial = adiciona_button_label(layout, self, 'idComercial', 0)

        # Botão e rótulo para o idInterno
        botao_template_idinterno, self.label_idinterno = adiciona_button_label(layout, self, 'idInterno', 1)
    
        # Botão "Concluído"
        botao_concluido = QPushButton('Concluído')
        layout.addWidget(botao_concluido, 3, 3)
        botao_concluido.setMinimumSize(100, 45)
        botao_concluido.clicked.connect(self.busca_template) 

    def janela_template_idcomercial(self):
        """
        Abre uma nova janela para a criação de um template comercial.

        - Cria a nova janela
        - Configura o título e tamanho fixo da janela
        - Exibe a janela
        - Configura o modo escuro na nova janela
        - Cria um layout para a nova janela
        - Adiciona um botão e um rótulo para o idComercial ao layout
        - Adiciona um botão "Concluído" ao layout
        - Conecta o sinal do botão "Concluído" ao método get_template_idcomercial
        """
        # Criação da nova janela        
        self.nova_janela = QWidget()
        self.nova_janela.setWindowTitle('Template Comercial')
        self.nova_janela.setFixedSize(600,150)
        self.nova_janela.show()
        set_dark_mode(self.nova_janela)

        layout = QGridLayout()
        self.nova_janela.setLayout(layout)

        # Botão e rótulo para o idComercial
        botao_template_idcomercial, self.label_idcomercial = adiciona_button_label(layout, self, 'idComercial', 0)
        
        # Botão "Concluído"
        botao_concluido = QPushButton('Concluido')
        layout.addWidget(botao_concluido, 3, 3)
        botao_concluido.setMinimumSize(100, 45)
        botao_concluido.clicked.connect(self.get_template_idcomercial)

    def janela_processamento_pendente(self):
        """
        Atualiza a tabela de processamento pendente na janela principal.

        - Obtém o processamento pendente do sistema operacional
        - Atualiza a tabela com os dados do processamento pendente
        """
        # Obtém o processamento pendente do sistema operacional
        processamento_pendente = acesso.get_os_processamento_pendente()

        # Atualiza a tabela com os dados do processamento pendente
        atualiza_tabela(self, processamento_pendente, "OS's Pendentes")


    def janela_estorna(self):
        """
        Abre uma nova janela para a estornar uma OS.

        - Cria a nova janela
        - Configura o título e tamanho fixo da janela
        - Exibe a janela
        - Configura o modo escuro na nova janela
        - Cria um layout para a nova janela
        - Adiciona um botão e um rótulo para o idOS ao layout
        - Adiciona um botão "Concluído" ao layout
        - Conecta o sinal do botão "Concluído" ao método estorna_whatsapp
        """
        # Criação da nova janela        
        self.nova_janela = QWidget()
        self.nova_janela.setWindowTitle('Estorna OS')
        self.nova_janela.setFixedSize(600,150)
        self.nova_janela.show()
        set_dark_mode(self.nova_janela)

        layout = QGridLayout()
        self.nova_janela.setLayout(layout)

        # Botão e rótulo para o idOS
        botao_template_idos, self.label_idos = adiciona_button_label(layout, self, 'idOS', 0)
        
        # Botão "Concluído"
        botao_concluido = QPushButton('Concluido')
        layout.addWidget(botao_concluido, 3, 3)
        botao_concluido.setMinimumSize(100, 45)
        botao_concluido.clicked.connect(self.estorna_whatsapp)

    def janela_agenda_envio(self):
        """
        Abre uma nova janela para agendar o envio de uma OS no WhatsApp.

        - Cria a nova janela
        - Configura o título e tamanho fixo da janela
        - Exibe a janela
        - Configura o modo escuro na nova janela
        - Cria um layout para a nova janela
        - Adiciona botões e rótulos para o IdOS e Minutos ao layout
        - Adiciona um botão "Concluído" ao layout
        - Conecta o sinal do botão "Concluído" ao método agenda_envio_whats
        """
        # Criação da nova janela        
        self.nova_janela = QWidget()
        self.nova_janela.setWindowTitle('Agenda Envio OS')
        self.nova_janela.setFixedSize(600,150)
        self.nova_janela.show()
        set_dark_mode(self.nova_janela)

        layout = QGridLayout()
        self.nova_janela.setLayout(layout)
        
        # Botão e rótulo para o IdOS
        botao_template_idos, self.label_idos = adiciona_button_label(layout, self, 'IdOS', 0)
        
        # Botão e rótulo para os Minutos
        botao_template_idinterno, self.label_idinterno = adiciona_button_label(layout, self, 'Minutos', 1)              
        
        # Botão "Concluído"
        botao_concluido = QPushButton('Concluido')
        layout.addWidget(botao_concluido, 3, 3)
        botao_concluido.setMinimumSize(100, 45)
        botao_concluido.clicked.connect(self.agenda_whatsapp)  

    def janela_estorna_agendamento(self):
        """
        Abre uma nova janela para remover um agendamento.

        - Cria a nova janela
        - Configura o título e tamanho fixo da janela
        - Exibe a janela
        - Configura o modo escuro na nova janela
        - Cria um layout para a nova janela
        - Adiciona um botão e um rótulo para o IdOS ao layout
        - Adiciona um botão "Concluído" ao layout
        - Conecta o sinal do botão "Concluído" ao método remove_agendamento
        """
        # Criação da nova janela        
        self.nova_janela = QWidget()
        self.nova_janela.setWindowTitle('Remove Agendamento')
        self.nova_janela.setFixedSize(600,150)
        self.nova_janela.show()
        set_dark_mode(self.nova_janela)

        layout = QGridLayout()
        self.nova_janela.setLayout(layout)

        # Criação do botão "IdOS"
        botao_template_idos, self.label_idos = adiciona_button_label(layout, self, 'IdOS', 0)
        
        # Botão "Concluído"
        botao_concluido = QPushButton('Concluido')
        layout.addWidget(botao_concluido, 3, 3)
        botao_concluido.setMinimumSize(100, 45)
        botao_concluido.clicked.connect(self.remove_agendamento)  
    
    def remove_agendamento(self):
        """
        Remove o agendamento de envio de uma OS no WhatsApp.

        - Obtém o idOS a partir do rótulo correspondente na janela
        - Chama a função para remover o agendamento do sistema
        - Verifica o resultado do processo de remoção
        - Exibe uma mensagem informativa de sucesso ou uma mensagem de erro
        - Fecha a janela atual
        """
        # Obtém o idOS a partir do rótulo correspondente na janela
        id_os_whats = self.label_idos.text()

        # Chama a função para remover o agendamento do sistema
        remove_agendamento = acesso.remove_agendamento_envio_os_whatsapp(id_os_whats)

        # Verifica o resultado do processo de remoção
        if (remove_agendamento == "200"):
            QMessageBox.information(self, "Agendamento da OS" + id_os_whats + " estornada com sucesso!")
        else:
            QMessageBox.critical(self, "Mensagem de erro", remove_agendamento)

        # Fecha a janela atual
        self.nova_janela.close()                      
    
    def agenda_whatsapp(self):
        """
        Agenda o envio de uma OS no WhatsApp.

        - Obtém o idOS e a quantidade de minutos a partir dos rótulos correspondentes na janela
        - Chama a função para agendar o envio da OS no sistema
        - Verifica o resultado do processo de agendamento
        - Exibe uma mensagem informativa de sucesso ou uma mensagem de erro
        - Fecha a janela atual
        """
        
        # Obtém o idOS e a quantidade de minutos a partir dos rótulos correspondentes na janela
        id_os_whatsapp = self.label_idos.text()
        qtde_minutos = self.label_idinterno.text()

        # Chama a função para agendar o envio da OS no sistema
        agenda_envio_whatsapp = acesso.agenda_envio_os_whatsapp_menu(id_os_whatsapp, qtde_minutos)

        # Verifica o resultado do processo de agendamento
        if (agenda_envio_whatsapp == "200"):
            QMessageBox.information(self, "Concluido" ,"OS " + id_os_whatsapp + " agendada com sucesso!")
        else:
            QMessageBox.critical(self, "Mensagem de erro", agenda_envio_whatsapp)

        # Fecha a janela atual
        self.nova_janela.close()                      

    def estorna_whatsapp(self):
        """
        Estorna uma OS no WhatsApp.

        - Obtém o idOS a partir do rótulo correspondente na janela
        - Chama a função para estornar a OS no sistema
        - Verifica o resultado do processo de estorno
        - Exibe uma mensagem informativa de sucesso ou uma mensagem de erro
        - Fecha a janela atual
        """
        
        # Obtém o idOS a partir do rótulo correspondente na janela
        id_os_whatsapp = self.label_idos.text()

        # Chama a função para estornar a OS no sistema
        estorna_os_whatsapp = acesso.estorna_os_whatsapp(id_os_whatsapp)

        # Verifica o resultado do processo de estorno
        if (estorna_os_whatsapp == "200"):
            QMessageBox.critical(self, "Concluido" , "OS " + id_os_whatsapp + " estornada com sucesso!")
        else:
            QMessageBox.critical(self, "Mensagem de erro", estorna_os_whatsapp)

        # Fecha a janela atual
        self.nova_janela.close()
    
    def busca_template(self):
        """
        Obtém o template de mensagem.

        - Obtém os valores de idComercial e idInterno a partir dos rótulos correspondentes na janela
        - Chama a função para obter o template de mensagem no sistema
        - Verifica o resultado da obtenção do template
        - Exibe uma mensagem de erro se o template não for encontrado ou atualiza a tabela com o template obtido
        - Fecha a janela atual
        """
        
        # Obtém os valores de idComercial e idInterno a partir dos rótulos correspondentes na janela
        id_comercial = self.label_idcomercial.text()
        id_interno = self.label_idinterno.text()

        # Chama a função para obter o template de mensagem no sistema
        mensagem_template = acesso.get_mensagem_template_menu(id_comercial, id_interno)

        # Verifica o resultado da obtenção do template
        if (mensagem_template == "400"):
            QMessageBox.critical(self, "Mensagem de erro", "Template não encontrado!!")
        else:
            atualiza_tabela(self, mensagem_template, "Template")
        
        # Fecha a janela atual
        self.nova_janela.close()    
    
    def get_template_idcomercial(self):
        """
        Obtém os templates de mensagem por idComercial.

        - Obtém o valor de idComercial a partir do rótulo correspondente na janela
        - Chama a função para obter os templates de mensagem no sistema por idComercial
        - Verifica o resultado da obtenção dos templates
        - Exibe uma mensagem de erro se os templates não forem encontrados ou atualiza a tabela com os templates obtidos
        - Fecha a janela atual
        """
        
        # Obtém o valor de idComercial a partir do rótulo correspondente na janela
        id_comercial = self.label_idcomercial.text()

        # Chama a função para obter os templates de mensagem no sistema por idComercial
        mensagens_templates = acesso.get_mensagens_templates_by_id_comercial_menu(id_comercial)

        # Verifica o resultado da obtenção dos templates
        if (mensagens_templates == "400"):
            QMessageBox.critical(self, "Mensagem de erro", "Template não encontrado!!")
        else:
            atualiza_tabela(self, mensagens_templates, "Templates")
        
        # Fecha a janela atual
        self.nova_janela.close()

def set_dark_mode(window):
    """
    Define o modo escuro para a janela da aplicação.
    
    Args:
        window: A janela da aplicação.
    """
    # Define um estilo escuro para os widgets da aplicação
    dark_mode = QStyleFactory.create("Fusion")
    QApplication.setStyle(dark_mode)

    # Define uma paleta de cores para a aplicação
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53)) # Cor de fundo da janela
    palette.setColor(QPalette.WindowText, QColor(255, 255, 255)) # Cor do texto na janela
    palette.setColor(QPalette.Base, QColor(25, 25, 25)) # Cor base
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53)) # Cor alternativa
    palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255)) # Cor de fundo da dica de ferramenta
    palette.setColor(QPalette.ToolTipText, QColor(255, 255, 255)) # Cor de fundo da dica de ferramenta
    palette.setColor(QPalette.Text, QColor(255, 255, 255)) # Cor do texto
    palette.setColor(QPalette.Button, QColor(53, 53, 53)) # Cor dos botões
    palette.setColor(QPalette.ButtonText, QColor(255, 255, 255)) # Cor do texto nos botões
    palette.setColor(QPalette.BrightText, QColor(255, 0, 0)) # Cor do texto em destaque
    palette.setColor(QPalette.Highlight, QColor(0, 120, 215)) # Cor de destaque
    palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255)) # Cor do texto destacado
    window.setPalette(palette)

def cria_tabela(self):
    """
    Cria uma tabela na interface gráfica.
    """

    # Cria uma instância de QTableWidget e define como widget pai a própria janela (self)
    self.tabela = QTableWidget(self)

    # Define o tamanho fixo da tabela
    self.tabela.setFixedSize(1080, 780)

    # Define o número de colunas da tabela
    self.tabela.setColumnCount(1)

    # Define a largura da primeira coluna da tabela
    self.tabela.setColumnWidth(0, 1100)

    # Define a posição da tabela na janela
    self.tabela.move(0, 10)

def atualiza_tabela(self, teste, titulo):
    """
    Atualiza a tabela na interface gráfica com os dados fornecidos.

    Args:
        self: A referência à instância da classe.
        teste: Os dados a serem exibidos na tabela.
        titulo: O título da coluna da tabela.
    """
    # Quantidade de casos no JSON
    data = json.loads(teste)

    # Adiciona o título da coluna na lista de títulos de colunas
    titulos_colunas.append(titulo)

    # Define os rótulos das colunas da tabela
    self.tabela.setHorizontalHeaderLabels(titulos_colunas)
    
    #Colocando os valores nas colunas
    if type(data) == list:
        # Se os dados forem uma lista, configura o número de linhas da tabela
        self.tabela.setRowCount(len(data))
        for row,cell_data in enumerate(data):
            # Define a altura da linha na tabela
            self.tabela.setRowHeight(row, 380) # Setando o tamanho das linhas em 380px

            # Cria um QTableWidgetItem com o dado e substitui as vírgulas por quebras de linha
            item = QTableWidgetItem(str(cell_data).replace(",", "\n"))

            # Define o item na posição da linha e coluna correspondente
            self.tabela.setItem(row, 0, item)
    else:
        # Se os dados não forem uma lista
        self.tabela.setRowCount(1)        
        self.tabela.clear()

        # Define novamente os rótulos das colunas da tabela
        self.tabela.setHorizontalHeaderLabels(titulos_colunas)

        # Define a altura da primeira linha na tabela
        self.tabela.setRowHeight(0, 390) # Setando o tamanho da linha em 390px

        # Cria um QTableWidgetItem com o dado
        item = QTableWidgetItem(teste)

        # Define o item na posição da primeira linha e coluna
        self.tabela.setItem(0, 0, item)
    
    # Limpa a lista de títulos de colunas
    titulos_colunas.clear()

def adiciona_button_label(layout, self, text, row):
    """
    Adiciona um botão e uma caixa de texto em um layout na interface gráfica.

    Args:
        layout: O layout onde o botão e a caixa de texto serão adicionados.
        self: A referência à instância da classe.
        text: O texto do botão.
        row: O índice da linha onde o botão e a caixa de texto serão posicionados.

    Returns:
        Uma tupla contendo o botão e a caixa de texto criados.
    """
    
    # Cria um QPushButton com o texto fornecido
    botao = QPushButton(text, self)

    # Adiciona o botão ao layout, na posição (row, 0)
    layout.addWidget(botao, row, 0)

    # Define as margens do botão
    botao.setContentsMargins(10, 10, 10, 10)

    # Define a política de tamanho do botão
    botao.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)

     # Define o tamanho mínimo do botão
    botao.setMinimumSize(100, 30)

    # Desabilita o botão inicialmente
    botao.setEnabled(False)
        
    # Cria uma QLineEdit        
    label = QLineEdit(self)

    # Adiciona a caixa de texto ao layout, na posição (row, 1)
    layout.addWidget(label, row, 1)

    # Define o tamanho mínimo da caixa de texto
    label.setMinimumSize(100, 30)

    # Define o validador para aceitar somente números inteiros na caixa de texto
    validator = QIntValidator(self)
    label.setValidator(validator)
        
    return botao, label

def menu():
    """
    Função principal para iniciar o menu da aplicação.
    """

    # Cria uma instância da aplicação QApplication
    app = QApplication(sys.argv)

    # Cria a janela principal da aplicação
    main_window = janela_principal()

    # Exibe a janela principal
    main_window.show()

     # Executa o loop de eventos da aplicação
    sys.exit(app.exec_())