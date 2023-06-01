# ProjetoWhatsApp
# README

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
python main.py caminho/para/arquivo.txt 1234567 True 60
```

2. Exibir o menu:
```
python main.py
```

## Licença

Este projeto está licenciado sob a [Licença MIT](LICENSE).
