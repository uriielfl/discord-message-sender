

# MessageSenderBot
O MessageSenderBot é um bot para Discord que envia mensagens personalizadas para canais específicos do servidor. Ele carrega a configuração das mensagens a serem enviadas a partir de um arquivo config.json e executa o envio das mensagens. O bot também é capaz de lidar com erros ao enviar mensagens e registrar essas mensagens em arquivos de registro.

- [Pular para Instalação](#instalação)
- [Pular para Configuração](#configuração)
- [Pular para Configuração](#projeto)

## Instalação <a name="instalação"></a>

### Criar venv:

```console
    foo@bar:~$ py -m venv myvenv
```

### Ativar venv:

**(Windows)**
```console
foo@bar:~$ ./myvenv/Scripts/activate
```
**(Linux)**
```console
foo@bar:~$ source ./myvenv/bin/activate
```


Para instalar as dependências, basta rodar o comando **py -m pip install -r requirements.txt** no diretório do bot

```console
foo@bar:~$ py -m pip install -r requirements.txt
```



## Configuração <a name="configuração"></a>

Antes de usar o bot, você deve configurar o arquivo .env com o token do seu bot Discord e o config.json com as mensagens a serem enviadas.

#### Configurando o token do bot
Exemplo de arquivo **.env**:
makefile

```
BOT_TOKEN=YOUR_TOKEN_GOES_HERE
```

#### Configuração de Mensagens
As mensagens a serem enviadas são configuradas no arquivo config.json. Cada entrada no arquivo configura uma mensagem com os seguintes campos:

- **message_id**: Um identificador único para a mensagem.
- **title**: O título da mensagem (opcional).
- **description**: A descrição da mensagem (opcional).
- **embed_description**: A descrição do embed da mensagem (opcional).
- **thumbnail**: URL de uma imagem em miniatura para o embed (opcional).
- **image**: URL de uma imagem para o embed (opcional).
- **channel_id**: O ID do canal para o qual a mensagem será enviada.
- **purge**: Um valor booleano que determina se as mensagens no canal devem ser apagadas antes de enviar a nova mensagem.

## Entendendo o projeto <a name="projeto"></a>

### main.py
O arquivo principal que contém a implementação do bot e a lógica para carregar configurações, enviar mensagens e gerenciar erros. Ele usa a biblioteca discord.py para interagir com a API do Discord.

### bcolors.py
Uma classe que define cores ANSI para saída no terminal, usada para imprimir mensagens coloridas para uma melhor visualização durante a execução do bot.

### channel.py
Uma classe simples que representa uma mensagem enviada com sucesso para um canal específico. É usada para rastrear as mensagens enviadas com sucesso e os erros.

### helpers/write.py
Um módulo que fornece uma função write_json para adicionar mensagens aos arquivos de registro. É usado para registrar mensagens que não puderam ser enviadas devido a erros ou falta de conteúdo.

## Uso
Após configurar o arquivo .env, você pode iniciar o bot executando main.py. O bot lerá a configuração de mensagens em config.json e tentará enviá-las para os canais especificados no servidor Discord.

## Registro de Erros e Mensagens Sem Conteúdo
Quando ocorrem erros durante o envio de mensagens ou quando uma mensagem não possui conteúdo para enviar, essas mensagens são registradas em arquivos de registro. Os arquivos de registro são **by_error.json** para mensagens com erros e **by_no_content.json** para mensagens sem conteúdo. Isso facilita a identificação e resolução de problemas.

## Contribuição
Este é um projeto simples destinado ao aprendizado. Sinta-se à vontade para contribuir, fazer melhorias e personalizações. Se você encontrar algum problema ou tiver sugestões, abra uma issue.