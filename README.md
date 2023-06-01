# ProjetoWhatsApp

Este repositório contém um script para processar um arquivo, inserir dados do WhatsApp e exibir um menu caso nenhum parâmetro seja fornecido.

## Instalação

Para usar este script, é necessário ter o Python instalado. Além disso, você precisa instalar as dependências necessárias. Você pode instalá-las usando o seguinte comando:

```
pip install -r requirements.txt
```

## Uso

O script pode ser executado com o seguinte comando:

```
python main.py [arquivo] [id_os_whats] [agenda_envio] [qtde_minutos]
```

- `arquivo` (str): O caminho para o arquivo a ser processado.
- `id_os_whats` (str): O ID da ordem de serviço do WhatsApp.
- `agenda_envio` (str): Indica se a mensagem deve ser agendada para um horário posterior ou, por padrão, para 30 minutos.
- `qtde_minutos` (str): A quantidade de minutos para o envio agendado.

Se nenhum parâmetro for fornecido, o script exibirá um menu.

## Exemplos

1. Processar um arquivo e inserir dados do WhatsApp:
```
python whatsApp.py caminho/para/arquivo.txt 1234567 S 60
```

2. Exibir o menu:
```
python whatsApp.py
```

## Utilização do menu

1. Execute o arquivo `whatsApp.py` para iniciar a aplicação.
2. A janela principal da aplicação será exibida.
3. Na janela principal, você encontrará vários botões que representam as funcionalidades da aplicação.
4. Clique nos botões para acessar as diferentes funcionalidades e realizar as operações desejadas.

## Funcionalidades do menu

A aplicação possui as seguintes funcionalidades:

- Mensagem Template: Abre uma nova janela para buscar uma mensagem de template.
- Template Comercial: Abre uma nova janela para buscar uma mensagem de template comercial.
- Processamento Pendente: Atualiza a tabela de processamento pendente na janela principal.
- Estorna OSWhatsApp: Abre uma nova janela para estornar uma OS no WhatsApp.
- Agendamento: Abre uma nova janela para agendar o envio de uma OS no WhatsApp.
- Estorna Agendamento: Abre uma nova janela para remover um agendamento.

## Contribuição

Contribuições são bem-vindas! Se você quiser contribuir para este projeto, siga as etapas abaixo:

1. Faça um fork deste repositório.
2. Crie um branch com a sua feature ou correção de bug: `git checkout -b minha-feature`.
3. Faça as alterações necessárias no código.
4. Commit suas alterações: `git commit -m 'Minha nova feature'`.
5. Faça push para o branch: `git push origin minha-feature`.
6. Abra um pull request.