import discord
from discord.ext import commands
from discord import app_commands
import os
from dotenv import load_dotenv
from config import DISCORD_TOKEN, DISCORD_GUILD_ID
from models import init_db
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Carregar variáveis de ambiente
load_dotenv()

# Criar bot
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix=".", intents=intents)

# Inicializar banco de dados
@bot.event
async def on_ready():
    """Evento disparado quando o bot está pronto"""
    logger.info(f"Bot conectado como {bot.user}")
    
    # Inicializar banco de dados
    try:
        init_db()
        logger.info("Banco de dados inicializado com sucesso")
    except Exception as e:
        logger.error(f"Erro ao inicializar banco de dados: {e}")
    
    # Sincronizar comandos slash
    try:
        synced = await bot.tree.sync()
        logger.info(f"{len(synced)} comandos slash sincronizados")
    except Exception as e:
        logger.error(f"Erro ao sincronizar comandos: {e}")

# Carregar cogs (extensões)
async def load_cogs():
    """Carrega todos os cogs do bot"""
    cogs_dir = "cogs"
    
    if not os.path.exists(cogs_dir):
        os.makedirs(cogs_dir)
    
    for filename in os.listdir(cogs_dir):
        if filename.endswith(".py") and not filename.startswith("_"):
            try:
                await bot.load_extension(f"cogs.{filename[:-3]}")
                logger.info(f"Cog carregado: {filename}")
            except Exception as e:
                logger.error(f"Erro ao carregar cog {filename}: {e}")

@bot.event
async def setup_hook():
    """Hook chamado antes do bot ficar pronto"""
    await load_cogs()

# Comando de teste
@bot.tree.command(name="ping", description="Verifica se o bot está online")
async def ping(interaction: discord.Interaction):
    """Comando de teste para verificar latência"""
    await interaction.response.send_message(f"Pong! {round(bot.latency * 1000)}ms")

# Tratador de erros
@bot.event
async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    """Tratador de erros para comandos slash"""
    logger.error(f"Erro no comando {interaction.command.name}: {error}")
    
    if not interaction.response.is_done():
        await interaction.response.send_message(
            f"❌ Erro ao executar comando: {str(error)}",
            ephemeral=True
        )

# Executar bot
if __name__ == "__main__":
    if not DISCORD_TOKEN:
        logger.error("DISCORD_TOKEN não configurado no arquivo .env")
        exit(1)
    
    bot.run(DISCORD_TOKEN)
