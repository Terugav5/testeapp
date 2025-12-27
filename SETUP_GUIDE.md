# 🐿️ Guia de Configuração - Bot Esquilo Aposta

## Passo 1: Criar um Bot Discord

1. Acesse [Discord Developer Portal](https://discord.com/developers/applications)
2. Clique em "New Application"
3. Digite o nome: "Esquilo Aposta"
4. Vá para "Bot" e clique "Add Bot"
5. Copie o token em "TOKEN" (este é seu `DISCORD_TOKEN`)
6. Em "Privileged Gateway Intents", ative:
   - Message Content Intent
   - Server Members Intent

## Passo 2: Configurar Permissões do Bot

1. Vá para "OAuth2" > "URL Generator"
2. Selecione os scopes:
   - `bot`
   - `applications.commands`
3. Selecione as permissões:
   - Send Messages
   - Embed Links
   - Attach Files
   - Read Message History
   - Use Slash Commands
   - Manage Channels
   - Create Public Threads
   - Create Private Threads
4. Copie a URL gerada e abra em seu navegador para adicionar o bot ao seu servidor

## Passo 3: Configurar MySQL

### Opção A: MySQL Local

```bash
# Instalar MySQL (Ubuntu/Debian)
sudo apt-get install mysql-server

# Iniciar MySQL
sudo service mysql start

# Acessar MySQL
mysql -u root -p

# Criar banco de dados
CREATE DATABASE bot_esquilo_aposta;
CREATE USER 'bot_user'@'localhost' IDENTIFIED BY 'senha_segura';
GRANT ALL PRIVILEGES ON bot_esquilo_aposta.* TO 'bot_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### Opção B: MySQL na Nuvem

Use serviços como:
- AWS RDS
- Google Cloud SQL
- DigitalOcean Managed Database

## Passo 4: Configurar Chave Pix

1. Acesse seu banco ou instituição financeira
2. Gere uma chave Pix (pode ser CPF, Email, Telefone ou Aleatória)
3. Copie a chave

## Passo 5: Configurar Arquivo .env

```bash
# Copiar exemplo
cp .env.example .env

# Editar com seus dados
nano .env
```

Preencha com:

```env
# Discord
DISCORD_TOKEN=seu_token_do_bot_aqui
DISCORD_GUILD_ID=seu_guild_id_aqui

# MySQL
DB_HOST=localhost
DB_USER=bot_user
DB_PASSWORD=senha_segura
DB_NAME=bot_esquilo_aposta
DB_PORT=3306

# Pix
PIX_KEY=sua_chave_pix_aqui
PIX_BANK_CODE=001
PIX_ACCOUNT_HOLDER=Seu Nome
PIX_ACCOUNT_NUMBER=123456789

# Bot
BOT_PREFIX=.
ROOM_PRICE=0.40
COINS_WINNER=1
COINS_LOSER=0
```

## Passo 6: Instalar Dependências

### No PC (Windows/Linux):
```bash
pip install -r requirements.txt
```

### No Termux (Android):
```bash
# 1. Instalar dependências de sistema para o Pillow
pkg install libjpeg-turbo zlib

# 2. Instalar as dependências do projeto
pip install -r requirements.txt
```

## Passo 7: Executar o Bot

```bash
python bot.py
```

Você deve ver:
```
Bot conectado como Esquilo Aposta#0000
Banco de dados inicializado com sucesso
X comandos slash sincronizados
```

## Passo 8: Configurar Canais no Discord

1. Crie um canal chamado `#filas`
2. Crie um canal chamado `#mediadores`
3. Crie um canal chamado `#logs-mediadores`
4. Crie um canal chamado `#logs-partidas`

## Passo 9: Usar o Bot

### Como Admin:

1. Use `/central` para acessar as configurações
2. Configure os canais em "Configs gerais"
3. Defina os cargos em "Cargos"
4. Configure os logs em "Sistema de Logs"

### Como Mediador:

1. Vá ao canal `#mediadores`
2. Clique em "Entrar" para entrar como mediador
3. Clique em "Configurar Pix" e preencha seus dados
4. Aguarde os jogadores entrarem nas filas

### Como Jogador:

1. Vá ao canal `#filas`
2. Clique em "Entrar" na fila desejada
3. Aguarde a sala ficar cheia
4. Confirme a partida quando o mediador pedir
5. Escaneie o QR Code Pix para pagar
6. Jogue!

## 🔧 Troubleshooting

### Bot não aparece online

- Verifique se o token está correto
- Verifique se o bot tem permissões no servidor
- Reinicie o bot

### Comandos slash não aparecem

- Aguarde 5-10 minutos
- Tente usar `/` no Discord
- Verifique se o bot tem permissão "Use Slash Commands"

### Erro de conexão com banco de dados

- Verifique se MySQL está rodando
- Verifique as credenciais em `.env`
- Verifique se o banco de dados existe

### QR Code Pix não é gerado

- Verifique se `PIX_KEY` está preenchida em `.env`
- Verifique se a chave Pix é válida
- Verifique os logs do bot

## 📊 Monitorar o Bot

### Ver logs do banco de dados

```bash
# Conectar ao MySQL
mysql -u bot_user -p bot_esquilo_aposta

# Ver ações registradas
SELECT * FROM logs ORDER BY created_at DESC LIMIT 10;

# Ver estatísticas de usuários
SELECT user_id, username, wins, losses, coins FROM users;

# Ver partidas
SELECT * FROM matches ORDER BY created_at DESC;
```

### Ver logs do bot

Os logs são exibidos no console onde o bot está rodando.

## 🚀 Deploy em Produção

### Usar systemd (Linux)

Crie `/etc/systemd/system/bot-esquilo.service`:

```ini
[Unit]
Description=Bot Esquilo Aposta
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/bot-esquilo-aposta
ExecStart=/usr/bin/python3 /home/ubuntu/bot-esquilo-aposta/bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Ativar:

```bash
sudo systemctl enable bot-esquilo
sudo systemctl start bot-esquilo
sudo systemctl status bot-esquilo
```

### Usar Docker

Crie `Dockerfile`:

```dockerfile
FROM python:3.11

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "bot.py"]
```

Build e run:

```bash
docker build -t bot-esquilo .
docker run -d --name bot-esquilo --env-file .env bot-esquilo
```

## 📞 Suporte

Para problemas ou dúvidas, consulte:
- [Discord.py Documentation](https://discordpy.readthedocs.io/)
- [Discord Developer Portal](https://discord.com/developers/docs)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)

---

**Boa sorte com seu bot! 🐿️**
