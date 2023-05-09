class DadosProcessamento():    
    def __init__(self, NomeConsorciado, ContatoDestino, MensagemTemplate, CodBarra2Via, Tradutor, CodigoPix, Vencimento ):
         self.IdIndividuo = "030E2A42-69A3-44F2-A782-E61184674190"
         self.Nome = NomeConsorciado
         self.ContatoDestino = ContatoDestino
         self.DadosMensagemTemplate = MensagemTemplate
         self.cdControle = CodBarra2Via
         self.Tradutor = Tradutor
         self.CodigoPix = CodigoPix
         self.vencimento = Vencimento
         self.DtVencimento = "2022-11-08T14:41:37.499Z"
         self.QrCodePix = CodigoPix

class OsWhatsAppProcessamentoDTO():
    def __init__(self, GuidOsWhats):
        self.GuidOsWhatsAppEnvio = GuidOsWhats
