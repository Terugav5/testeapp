# 🐿️ Funcionalidades do Bot Esquilo Aposta

## ✅ Funcionalidades Implementadas

### 1. Sistema de Central de Configurações (`/central`)

**Descrição**: Menu principal para administradores gerenciarem toda a organização.

**Funcionalidades**:
- ✅ Menu de seleção com 4 opções principais
- ✅ Configurações Gerais
  - Editar valor da sala
  - Gerenciar valores de aposta (adicionar/remover)
  - Selecionar canal das threads
- ✅ Configurações de Partidas
  - Configurar coins para vencedor/perdedor
  - Ativar/desativar modalidades
  - Configurar canais por modalidade
- ✅ Central de Cargos
  - Definir cargo de mediador
  - Definir cargo de analista
- ✅ Sistema de Logs
  - Configurar canal de logs de mediadores
  - Configurar canal de logs de partidas

### 2. Sistema de Filas (`/filas`, `/filas-canal`)

**Descrição**: Gerenciar filas de partidas com suporte a múltiplas modalidades.

**Funcionalidades**:
- ✅ Enviar filas ativas para o canal configurado
- ✅ Suporte a 3 modalidades:
  - Mobile (1v1, 2v2, 3v3, 4v4)
  - Emulador (1v1, 2v2, 3v3, 4v4)
  - Misto (2v2, 3v3, 4v4)
- ✅ Múltiplos valores de aposta (R$ 1 a R$ 100)
- ✅ Botões interativos:
  - Entrar na fila
  - Sair da fila
  - Modos especiais (Full UMP, Gelo Infinito, Gelo Normal)
- ✅ Detecção automática de sala cheia
- ✅ Logs de entrada/saída

### 3. Painel de Mediador (`/tp-mediador`)

**Descrição**: Gerenciar mediadores e pagamentos.

**Funcionalidades**:
- ✅ Enviar painel de mediador para canal configurado
- ✅ Botões:
  - Entrar como mediador
  - Sair como mediador
  - Configurar dados de Pix
- ✅ Modal para configurar Pix:
  - Banco
  - Nome do titular
  - Chave Pix
- ✅ Verificação de permissões (cargo de mediador)

### 4. Informações de Sala (`/id`)

**Descrição**: Fornecer ID e senha da sala para os jogadores.

**Funcionalidades**:
- ✅ Exibir ID da sala
- ✅ Exibir senha da sala
- ✅ Embed formatado e profissional
- ✅ Logs de uso

### 5. Fluxo de Partida

#### Confirmação de Partida (`/confirmar-partida`)

**Funcionalidades**:
- ✅ Criar painel de confirmação
- ✅ Botões:
  - Confirmar (todos devem confirmar)
  - Encerrar (apenas mediador)
- ✅ Geração automática de QR Code Pix
- ✅ Envio de arquivo de QR Code
- ✅ Embed com informações de pagamento

#### Resultado de Partida (`/resultado`)

**Funcionalidades**:
- ✅ Registrar vencedor (team1 ou team2)
- ✅ Atualizar estatísticas dos jogadores:
  - Vitórias/Derrotas
  - Coins ganhos/perdidos
- ✅ Marcar partida como concluída
- ✅ Logs de resultado

### 6. Perfil do Usuário (`.p @usuario`)

**Descrição**: Visualizar estatísticas de um jogador.

**Funcionalidades**:
- ✅ Exibir vitórias
- ✅ Exibir derrotas
- ✅ Exibir coins
- ✅ Calcular taxa de vitória
- ✅ Embed formatado

### 7. Sistema de Banco de Dados

**Funcionalidades**:
- ✅ Suporte a MySQL/TiDB
- ✅ Modelos SQLAlchemy:
  - Guilds (configurações por servidor)
  - Users (dados dos jogadores)
  - Matches (partidas)
  - MatchParticipants (participantes)
  - Modalities (modalidades)
  - Modes (modos de jogo)
  - Logs (registro de ações)
  - BetValues (valores de aposta)
- ✅ Inicialização automática de tabelas
- ✅ Relacionamentos entre tabelas

### 8. Sistema de Pix

**Funcionalidades**:
- ✅ Geração de QR Code Pix em formato EMV
- ✅ Cálculo de CRC16 para validação
- ✅ Suporte a diferentes tipos de chave (CPF, CNPJ, Email, Telefone)
- ✅ Geração com valor da aposta
- ✅ Descrição automática da transação
- ✅ Envio como arquivo PNG

### 9. Sistema de Logs

**Funcionalidades**:
- ✅ Registro de todas as ações:
  - Abertura de central
  - Entrada/saída de filas
  - Login/logout de mediador
  - Confirmação de partidas
  - Resultados registrados
  - Configurações alteradas
- ✅ Armazenamento em banco de dados
- ✅ Timestamps automáticos

### 10. Gerenciamento de Permissões

**Funcionalidades**:
- ✅ Verificação de permissões de administrador
- ✅ Verificação de cargo de mediador
- ✅ Mensagens de erro apropriadas
- ✅ Respostas efêmeras para ações sensíveis

## 🎯 Suporte a 100 Partidas Simultâneas

**Implementações**:
- ✅ Banco de dados otimizado com índices
- ✅ Queries eficientes
- ✅ Relacionamentos apropriados
- ✅ Cache de configurações
- ✅ Views reutilizáveis

## 📊 Atualizações em Tempo Real

**Funcionalidades**:
- ✅ Embeds atualizados ao entrar/sair
- ✅ Status de sala atualizado
- ✅ Notificações de sala cheia
- ✅ Logs imediatos

## 🔒 Robustez

**Implementações**:
- ✅ Tratamento de erros em todos os comandos
- ✅ Validação de entrada
- ✅ Verificação de permissões
- ✅ Mensagens de erro informativas
- ✅ Logging completo
- ✅ Persistência em banco de dados

## 📁 Estrutura de Arquivos

```
bot-esquilo-aposta/
├── bot.py                    # Arquivo principal
├── config.py                 # Configurações
├── models.py                 # Modelos do banco
├── utils.py                  # Utilitários gerais
├── pix_utils.py              # Geração de Pix
├── test_bot.py               # Testes
├── requirements.txt          # Dependências
├── .env.example              # Exemplo de env
├── .gitignore                # Git ignore
├── README.md                 # Documentação
├── SETUP_GUIDE.md            # Guia de setup
├── FUNCIONALIDADES.md        # Este arquivo
└── cogs/
    ├── __init__.py
    ├── central.py            # /central
    ├── filas.py              # /filas
    ├── mediador.py           # /tp-mediador, /id
    ├── perfil.py             # .p
    └── match_flow.py         # /confirmar-partida, /resultado
```

## 🚀 Como Usar Cada Funcionalidade

### 1. Configurar o Bot (Admin)

```
/central → Configs gerais → Editar valor da sala
/central → Cargos → Definir mediador
/central → Sistema de Logs → Configurar canais
/filas-canal #filas
/tp-mediador #mediadores
```

### 2. Criar Filas (Admin)

```
/filas
```

### 3. Entrar em Fila (Jogador)

```
Clique em "Entrar" na fila desejada
```

### 4. Confirmar Partida (Mediador)

```
/confirmar-partida <match_id> @mediador
Clique em "Confirmar"
Escaneie o QR Code Pix
```

### 5. Registrar Resultado (Mediador)

```
/resultado <match_id> team1
```

### 6. Ver Perfil (Qualquer Um)

```
.p @usuario
```

## 🔄 Fluxo Completo de uma Partida

1. **Admin** usa `/filas` para criar filas
2. **Jogadores** clicam em "Entrar" nas filas
3. Quando sala fica cheia, status muda para "full"
4. **Mediador** usa `/confirmar-partida` para criar painel
5. **Jogadores** clicam em "Confirmar"
6. **QR Code Pix** é gerado automaticamente
7. **Jogadores** escaneiam e pagam
8. **Mediador** usa `/resultado` para registrar vencedor
9. **Estatísticas** são atualizadas automaticamente

## 📈 Métricas Rastreadas

- Vitórias por jogador
- Derrotas por jogador
- Coins ganhos/perdidos
- Taxa de vitória
- Histórico de partidas
- Ações de mediadores
- Configurações alteradas

## 🎮 Modalidades Suportadas

| Modalidade | Modos | Descrição |
|-----------|-------|-----------|
| Mobile | 1v1, 2v2, 3v3, 4v4 | Jogos em celular |
| Emulador | 1v1, 2v2, 3v3, 4v4 | Jogos em emulador |
| Misto | 2v2, 3v3, 4v4 | Celular + Emulador |

## 💰 Valores de Aposta

R$ 1.00, R$ 2.00, R$ 3.00, R$ 5.00, R$ 10.00, R$ 20.00, R$ 30.00, R$ 50.00, R$ 100.00

## 🔐 Segurança

- ✅ Verificação de permissões em todos os comandos
- ✅ Validação de entrada
- ✅ Senhas aleatórias para salas
- ✅ Chave Pix em variável de ambiente
- ✅ Logs de todas as ações

## ✨ Recursos Extras

- ✅ Suporte a múltiplos servidores (Guilds)
- ✅ Configurações independentes por servidor
- ✅ Sistema de cargos personalizáveis
- ✅ Logs detalhados
- ✅ Testes unitários
- ✅ Documentação completa

---

**Desenvolvido com ❤️ para a comunidade Esquilo Aposta**
