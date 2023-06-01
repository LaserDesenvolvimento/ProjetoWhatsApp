class DadosProcessamento():    
    def __init__(self, guid, nome, contato_destino, mensagem_template, nro_documento, cod_barra_2via, tradutor, codigo_pix, vencimento):#
         #self.IdIndividuo = guid
         self.IdIndividuo = "030E2A42-69A3-44F2-A782-E61184674190"
         self.Nome = nome
         self.ContatoDestino = contato_destino
         self.DadosMensagemTemplate = mensagem_template
         self.dcNroDocumento = nro_documento
         self.cdControle = cod_barra_2via
         self.Tradutor = tradutor
         self.CodigoPix = codigo_pix
         self.vencimento = vencimento
         self.DtVencimento = "2022-11-08T14:41:37.499Z"
         self.QrCodePix = codigo_pix

class OsWhatsAppProcessamentoDTO():
    def __init__(self, guid_os_whats):
        self.GuidOsWhatsAppEnvio = guid_os_whats
