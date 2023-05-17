import sys
import json
import acesso
from PyQt5.QtGui import QPalette, QColor, QIntValidator
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QGridLayout, QTableWidget, QTableWidgetItem, QStyleFactory, QLabel
from PyQt5 import QtCore 
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMessageBox, QPushButton, QWidget, QSizePolicy

titulos_colunas = ["OS's Pendentes", "Teste"]
teste_coluna = []

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Modo Dark
        set_dark_mode(self)

        teste = acesso.GetOSProcessamentoPendente()

        # Define o tamanho da janela principal
        self.setFixedSize(1200, 800)

        # Define o layout da janela principal como grid
        layout = QGridLayout()
        self.setLayout(layout)

        # Cria os botões e as caixas de texto e adiciona-os ao layout
        self.button1 = QPushButton('Mensagem' + '\n' + 'Template', self)
        self.button1.setGeometry(QtCore.QRect(10, 10, 93, 48))
        self.button1.clicked.connect(self.window_template)
                
        self.button2 = QPushButton('Template' + '\n' + 'Comercial', self)
        self.button2.setGeometry(QtCore.QRect(10, 68, 93, 48))
        self.button2.clicked.connect(self.window_template_idcomercial)

        self.button3 = QPushButton('Processamento' + '\n' + 'Pendente', self)
        self.button3.setGeometry(QtCore.QRect(10, 126, 93, 48))
        self.button3.clicked.connect(self.window_reload)

        self.button4 = QPushButton('Estorna' + '\n' + 'OSWhatsApp', self)
        self.button4.setGeometry(QtCore.QRect(10, 184, 93, 48))
        self.button4.clicked.connect(self.window_estorna)

        self.button5 = QPushButton('Agendamento', self)
        self.button5.setGeometry(QtCore.QRect(10, 242, 93, 48))
        self.button5.clicked.connect(self.window_AgendaEnvioOsWhats)

        self.button6 = QPushButton('Estorna' + '\n' + 'Agendamento', self)
        self.button6.setGeometry(QtCore.QRect(10, 300, 93, 48))
        self.button6.clicked.connect(self.window_RemoveAgendamento)

        cria_tabela(self)

        atualiza_tabela(self, teste, "OS's Pendentes")

        layout.addWidget(self.tabela)
        layout.setAlignment(self.tabela, Qt.AlignRight)

    def window_template(self):
        # Criação da nova janela        
        self.new_window = QWidget()
        self.new_window.setWindowTitle('Mensagem Template')
        self.new_window.setFixedSize(600,150)
        self.new_window.show()
        
        #Configuração do modo escuro
        set_dark_mode(self.new_window)
        
        layout = QGridLayout()
        self.new_window.setLayout(layout)
    
        botao_template_idcomercial, self.LabelIdComercial = adiciona_button_label(layout, self, 'idComercial', 0)
        botao_template_idinterno, self.LabelIdInterno = adiciona_button_label(layout, self, 'idInterno', 1)
    
        buttonWinTemplateOk = QPushButton('Concluído')
        layout.addWidget(buttonWinTemplateOk, 3, 3)
        buttonWinTemplateOk.setMinimumSize(100, 45)
        buttonWinTemplateOk.clicked.connect(self.get_template) 

    def window_template_idcomercial(self):
        # Criação da nova janela        
        self.new_window = QWidget()
        self.new_window.setWindowTitle('Nova janela')
        self.new_window.setFixedSize(600,150)
        self.new_window.show()
        set_dark_mode(self.new_window)

        layout = QGridLayout()
        self.new_window.setLayout(layout)

        botao_template_idcomercial, self.LabelIdComercial = adiciona_button_label(layout, self, 'idComercial', 0)
        
        buttonWinTemplateOk = QPushButton('Concluido')
        layout.addWidget(buttonWinTemplateOk, 3, 3)
        buttonWinTemplateOk.setMinimumSize(100, 45)
        buttonWinTemplateOk.clicked.connect(self.get_template_idcomercial)

    def window_reload(self):
        teste = acesso.GetOSProcessamentoPendente()

        atualiza_tabela(self, teste, "OS's Pendentes")


    def window_estorna(self):
        # Criação da nova janela        
        self.new_window = QWidget()
        self.new_window.setWindowTitle('Nova janela')
        self.new_window.setFixedSize(600,150)
        self.new_window.show()
        set_dark_mode(self.new_window)

        layout = QGridLayout()
        self.new_window.setLayout(layout)

        botao_template_idOS, self.LabelIdOIS = adiciona_button_label(layout, self, 'idOS', 0)
        
        buttonWinTemplateOk = QPushButton('Concluido')
        layout.addWidget(buttonWinTemplateOk, 3, 3)
        buttonWinTemplateOk.setMinimumSize(100, 45)
        buttonWinTemplateOk.clicked.connect(self.get_estornaOS)

    def window_AgendaEnvioOsWhats(self):
        # Criação da nova janela        
        self.new_window = QWidget()
        self.new_window.setWindowTitle('Nova janela')
        self.new_window.setFixedSize(600,150)
        self.new_window.show()
        set_dark_mode(self.new_window)

        layout = QGridLayout()
        self.new_window.setLayout(layout)
        
        botao_template_idOS, self.LabelIdOIS = adiciona_button_label(layout, self, 'IdOS', 0)
        botao_template_idinterno, self.LabelIdInterno = adiciona_button_label(layout, self, 'Minutos', 1)              
        
        buttonWinTemplateOk = QPushButton('Concluido')
        layout.addWidget(buttonWinTemplateOk, 3, 3)
        buttonWinTemplateOk.setMinimumSize(100, 45)
        buttonWinTemplateOk.clicked.connect(self.get_AgendaEnvioOsWhats)  

    def window_RemoveAgendamento(self):
        # Criação da nova janela        
        self.new_window = QWidget()
        self.new_window.setWindowTitle('Nova janela')
        self.new_window.setFixedSize(600,150)
        self.new_window.show()
        set_dark_mode(self.new_window)

        layout = QGridLayout()
        self.new_window.setLayout(layout)

        # Criação do botão "IdOS"
        botao_template_idOS, self.LabelIdOIS = adiciona_button_label(layout, self, 'IdOS', 0)
        
        buttonWinTemplateOk = QPushButton('Concluido')
        layout.addWidget(buttonWinTemplateOk, 3, 3)
        buttonWinTemplateOk.setMinimumSize(100, 45)
        buttonWinTemplateOk.clicked.connect(self.get_RemoveAgendamento)  
    
    def get_RemoveAgendamento(self):
        idOS = self.LabelIdOIS.text()
        teste2 = acesso.RemoveAgendamentoEnvioOsWhatsApp(idOS)

        if (teste2 == "200"):
            QMessageBox.information(self, "Agendamento da OS" + idOS + " estornada com sucesso!")
        else:
            QMessageBox.critical(self, "Mensagem de erro", teste2)

        self.new_window.close()                      
    
    def get_AgendaEnvioOsWhats(self):
        idOS = self.LabelIdOIS.text()
        qtdeMinutos = self.LabelIdInterno.text()
        teste2 = acesso.AgendaEnvioOsWhatsAppMenu(idOS, qtdeMinutos)

        if (teste2 == "200"):
            QMessageBox.information(self, "Concluido" ,"OS " + idOS + " agendada com sucesso!")
        else:
            QMessageBox.critical(self, "Mensagem de erro", teste2)

        self.new_window.close()                      

    def get_estornaOS(self):
        idOS = self.LabelIdOIS.text()
        teste2 = acesso.EstornaOSWhatsApp(idOS)

        if (teste2 == "200"):
            QMessageBox.critical(self, "Concluido" , "OS " + idOS + " estornada com sucesso!")
        else:
            QMessageBox.critical(self, "Mensagem de erro", teste2)

        self.new_window.close()
    
    def get_template(self):
        idComercial = self.LabelIdComercial.text()
        idInterno = self.LabelIdInterno.text()
        teste2 = acesso.GetMensagemTemplateMenu(idComercial, idInterno)

        if (teste2 == "400"):
            QMessageBox.critical(self, "Mensagem de erro", "Template não encontrado!!")
        else:
            atualiza_tabela(self, teste2, "Template")
        
        self.new_window.close()    
    
    def get_template_idcomercial(self):
        idComercial = self.LabelIdComercial.text()
        teste2 = acesso.GetMensagensTemplatesByIdComercialMenu(idComercial)

        if (teste2 == "400"):
            QMessageBox.critical(self, "Mensagem de erro", "Template não encontrado!!")
        else:
            atualiza_tabela(self, teste2, "Templates")
        
        self.new_window.close()

def set_dark_mode(window):
    # Define um estilo escuro para os widgets da aplicação
    dark_mode = QStyleFactory.create("Fusion")
    QApplication.setStyle(dark_mode)

    # Define uma paleta de cores para a aplicação
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
    palette.setColor(QPalette.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))
    palette.setColor(QPalette.ToolTipText, QColor(255, 255, 255))
    palette.setColor(QPalette.Text, QColor(255, 255, 255))
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
    palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
    palette.setColor(QPalette.Highlight, QColor(0, 120, 215))
    palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))
    window.setPalette(palette)

def cria_tabela(self):
    self.tabela = QTableWidget(self)
    self.tabela.setFixedSize(1080, 780)
    self.tabela.setColumnCount(1)
    self.tabela.setColumnWidth(0, 1100)
    self.tabela.move(0, 10)

def atualiza_tabela(self, teste, titulo):

    #Quantidade de casos no JSON
    data = json.loads(teste)
    teste_coluna.append(titulo)
    self.tabela.setHorizontalHeaderLabels(teste_coluna)
    
    #Colocando os valores nas colunas
    if type(data) == list:
        self.tabela.setRowCount(len(data))
        for row,cell_data in enumerate(data):
            self.tabela.setRowHeight(row, 380) #setando o tamanho das linhas em 300px
            item = QTableWidgetItem(str(cell_data).replace(",", "\n"))
            self.tabela.setItem(row, 0, item)
    else:      
        self.tabela.setRowCount(1)        
        self.tabela.clear()
        self.tabela.setHorizontalHeaderLabels(teste_coluna)
        self.tabela.setRowHeight(0, 390) #setando o tamanho das linhas em 300px
        item = QTableWidgetItem(teste)
        self.tabela.setItem(0, 0, item)
    
    teste_coluna.clear()        

def adiciona_button_label(layout, self, text, row):
    button = QPushButton(text, self)
    layout.addWidget(button, row, 0)
    button.setContentsMargins(10, 10, 10, 10)
    button.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
    button.setMinimumSize(100, 30)
    button.setEnabled(False)
        
    label = QLineEdit(self)
    layout.addWidget(label, row, 1)
    label.setMinimumSize(100, 30)

    # Define o validador para aceitar somente números inteiros
    validator = QIntValidator(self)
    label.setValidator(validator)
        
    return button, label

def menu():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())