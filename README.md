# 🐿️ Bot Esquilo Aposta

Um bot Discord completo para gerenciar apostas, filas de partidas, mediadores e pagamentos via Pix.

## 📋 Requisitos

- Python 3.8+
- MySQL 5.7+ ou TiDB
- Token de Bot Discord
- Chave Pix (para gerar QR Codes)

## 🚀 Instalação

### 1. Clonar ou criar o projeto

```bash
cd /home/ubuntu/bot-esquilo-aposta
```

### 2. Instalar dependências

```bash
pip install -r requirements.txt
```

### 3. Configurar banco de dados

Crie um banco de dados MySQL:

```sql
CREATE DATABASE bot_esquilo_aposta;
```

### 4. Configurar variáveis de ambiente

Copie o arquivo `.env.example` para `.env` e preencha com seus dados:

```bash
cp .env.example .env
```

Edite o arquivo `.env` com suas configurações:

```env
# Discord Bot Configuration
DISCORD_TOKEN=seu_token_aqui
DISCORD_GUILD_ID=seu_guild_id_aqui

# MySQL Database Configuration
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=sua_senha_aqui
DB_NAME=bot_esquilo_aposta
DB_PORT=3306

# Pix Configuration
PIX_KEY=sua_chave_pix_aqui
PIX_BANK_CODE=001
PIX_ACCOUNT_HOLDER=Seu Nome
PIX_ACCOUNT_NUMBER=123456789

# Bot Configuration
BOT_PREFIX=.
ROOM_PRICE=0.40
COINS_WINNER=1
COINS_LOSER=0
```

### 5. Executar o bot

```bash
python bot.py
```

## 📖 Comandos

### Comandos Slash (/)

#### `/central`
Abre a central de configurações da organização. Apenas administradores podem usar.

**Opções:**
- **Configs gerais**: Configurar valor da sala e valores de aposta
- **Partidas**: Configurar modalidades e coins
- **Cargos**: Definir cargos de mediador e analista
- **Sistema de Logs**: Configurar canais de logs

#### `/filas`
Envia as filas ativas para o canal configurado. Apenas administradores podem usar.

#### `/filas-canal`
Define o canal onde as filas serão enviadas.

**Parâmetros:**
- `canal`: Canal de destino

#### `/tp-mediador`
Define o canal do painel de mediador e envia o painel.

**Parâmetros:**
- `canal`: Canal de destino

#### `/id`
Informa o ID e senha da sala.

**Parâmetros:**
- `id_sala`: ID da sala
- `senha`: Senha da sala

#### `/confirmar-partida`
Cria um painel de confirmação de partida.

**Parâmetros:**
- `match_id`: ID da partida
- `mediador`: Usuário mediador

#### `/resultado`
Registra o resultado da partida.

**Parâmetros:**
- `match_id`: ID da partida
- `vencedor`: Time vencedor (team1 ou team2)

### Comandos de Texto (.)

#### `.p @usuario`
Mostra o perfil de um usuário com estatísticas.

**Exemplo:**
```
.p @usuario
```

## 🎮 Fluxo de Partida

1. **Criação de Fila**: Admin usa `/filas` para criar filas
2. **Entrada de Jogadores**: Jogadores clicam em "Entrar" para entrar na fila
3. **Sala Cheia**: Quando a sala fica cheia, o status muda para "full"
4. **Confirmação**: Mediador cria painel com `/confirmar-partida`
5. **Pagamento**: QR Code Pix é gerado automaticamente
6. **Resultado**: Mediador registra resultado com `/resultado`

## 🛠️ Estrutura do Projeto

```
bot-esquilo-aposta/
├── bot.py                 # Arquivo principal do bot
├── config.py              # Configurações
├── models.py              # Modelos do banco de dados
├── utils.py               # Funções utilitárias
├── pix_utils.py           # Funções para gerar QR Code Pix
├── requirements.txt       # Dependências
├── .env.example           # Exemplo de variáveis de ambiente
├── .env                   # Variáveis de ambiente (não commitar)
└── cogs/                  # Extensões do bot
    ├── __init__.py
    ├── central.py         # Comando /central
    ├── filas.py           # Comando /filas
    ├── mediador.py        # Comandos /tp-mediador e /id
    ├── perfil.py          # Comando .p
    └── match_flow.py      # Fluxo de partida
```

## 💾 Banco de Dados

O bot usa SQLAlchemy com MySQL. As tabelas são criadas automaticamente na primeira execução.

### Tabelas principais:

- **guilds**: Configurações por servidor
- **users**: Dados dos usuários
- **matches**: Partidas
- **match_participants**: Participantes das partidas
- **modalities**: Modalidades (Mobile, Emulador, Misto)
- **modes**: Modos de jogo (1v1, 2v2, etc)
- **logs**: Registro de ações

## 🔐 Segurança

- **Permissões**: Apenas administradores podem acessar `/central` e `/filas`
- **Chave Pix**: Armazenada em variável de ambiente
- **Banco de dados**: Use senhas fortes
- **Token do bot**: Nunca commitar o arquivo `.env`

## 🐛 Troubleshooting

### Erro: "DISCORD_TOKEN não configurado"
- Verifique se o arquivo `.env` existe e tem `DISCORD_TOKEN` preenchido

### Erro: "Conexão com banco de dados falhou"
- Verifique as credenciais do MySQL em `.env`
- Certifique-se de que o banco de dados existe
- Verifique se o MySQL está rodando

### Erro: "Comando não aparece no Discord"
- Aguarde alguns minutos após iniciar o bot
- Tente usar `/` para ver os comandos disponíveis
- Verifique se o bot tem permissão para usar comandos slash

### Erro ao gerar QR Code Pix
- Verifique se `PIX_KEY` está configurada em `.env`
- Certifique-se de que a chave Pix é válida

## 📝 Logs

Os logs são armazenados no banco de dados na tabela `logs`. Você pode visualizar:

- Entrada/saída de filas
- Confirmação de partidas
- Resultados registrados
- Configurações alteradas
- Ações de mediadores

## 🤝 Contribuindo

Para adicionar novos recursos:

1. Crie uma nova cog em `cogs/`
2. Implemente a classe herdando de `commands.Cog`
3. Adicione o método `async def setup(bot)`
4. O bot carregará automaticamente

## 📄 Licença

Este projeto é fornecido como está.

## 🆘 Suporte

Para reportar bugs ou sugerir melhorias, entre em contato com o desenvolvedor.

---

**Desenvolvido com ❤️ para a comunidade Esquilo Aposta**
