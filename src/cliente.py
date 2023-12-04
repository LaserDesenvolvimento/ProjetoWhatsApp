from datetime import datetime
class DadosProcessamento():    
    def __init__(self, guid, nome, contato_destino, mensagem_template, nro_documento, cod_barra_2via, tradutor, codigo_pix, vencimento):
         self.IdIndividuo = guid
         self.Nome = nome
         self.ContatoDestino = contato_destino
         self.DadosMensagemTemplate = mensagem_template
         self.dcNroDocumento = nro_documento
         self.cdControle = cod_barra_2via
         self.Tradutor = tradutor
         self.CodigoPix = codigo_pix
         self.DtVencimento = self.converte_data_vencimento(vencimento)
         self.QrCodePix = codigo_pix

    def converte_data_vencimento(self, data_str):
        # Converta a data para um objeto datetime
        data_formatada = datetime.strptime(data_str, "%d/%m/%Y")

        # Defina manualmente o dia como "00" e a hora como "00:00:00.000"
        data_formatada = data_formatada.replace(hour=0, minute=0, second=0, microsecond=0)

        # Crie a string no formato desejado
        data_formatada_str = data_formatada.strftime("%Y-%m-%d") + "T00:00:00.000Z"
        
        return data_formatada_str

class OsWhatsAppProcessamentoDTO():
    def __init__(self, guid_os_whats):
        self.GuidOsWhatsAppEnvio = guid_os_whats
