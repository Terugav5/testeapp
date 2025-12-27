import discord
from discord.ext import commands
from discord import app_commands
from utils import (
    get_or_create_guild, get_or_create_user, create_match_embed, log_action,
    generate_room_id, generate_room_password
)
from models import get_session, Guild, Match, Modality, Mode, MatchParticipant, User
from config import MODALITIES, BET_VALUES
import logging

logger = logging.getLogger(__name__)

class QueueView(discord.ui.View):
    """View para a fila de partidas"""
    
    def __init__(self, match_id: int, modality_name: str, mode_name: str, price: float):
        super().__init__(timeout=None)
        self.match_id = match_id
        self.modality_name = modality_name
        self.mode_name = mode_name
        self.price = price
        self.players = []
    
    @discord.ui.button(label="Entrar", style=discord.ButtonStyle.success, emoji="✅")
    async def enter_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Botão para entrar na fila"""
        
        session = get_session()
        try:
            match = session.query(Match).filter_by(id=self.match_id).first()
            
            if not match:
                await interaction.response.send_message(
                    "❌ Partida não encontrada",
                    ephemeral=True
                )
                return
            
            # Verificar se já está na fila
            existing = session.query(MatchParticipant).filter_by(
                match_id=self.match_id,
                user_id=str(interaction.user.id)
            ).first()
            
            if existing:
                await interaction.response.send_message(
                    "⚠️ Você já está nesta fila",
                    ephemeral=True
                )
                return
            
            # Adicionar à fila
            participant = MatchParticipant(
                match_id=self.match_id,
                user_id=str(interaction.user.id),
                team=None
            )
            session.add(participant)
            session.commit()
            
            # Atualizar lista de jogadores
            self.players.append(interaction.user.mention)
            
            log_action(
                str(interaction.guild.id),
                str(interaction.user.id),
                "join_queue",
                match_id=match.match_id
            )
            
            await interaction.response.send_message(
                f"✅ Você entrou na fila de {self.modality_name} {self.mode_name}",
                ephemeral=True
            )
            
            # Verificar se a sala está cheia
            total_players = session.query(MatchParticipant).filter_by(match_id=self.match_id).count()
            mode_size = int(self.mode_name.split('v')[0]) * 2
            
            if total_players >= mode_size:
                match.status = 'full'
                session.commit()
                
                # Enviar mensagem de sala cheia
                await interaction.channel.send(
                    f"🎮 **Sala cheia!** {self.modality_name} {self.mode_name} está pronta para começar!"
                )
        
        finally:
            session.close()
    
    @discord.ui.button(label="Sair", style=discord.ButtonStyle.danger, emoji="❌")
    async def leave_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Botão para sair da fila"""
        
        session = get_session()
        try:
            match = session.query(Match).filter_by(id=self.match_id).first()
            
            if not match:
                await interaction.response.send_message(
                    "❌ Partida não encontrada",
                    ephemeral=True
                )
                return
            
            # Remover da fila
            participant = session.query(MatchParticipant).filter_by(
                match_id=self.match_id,
                user_id=str(interaction.user.id)
            ).first()
            
            if participant:
                session.delete(participant)
                session.commit()
                
                if interaction.user.mention in self.players:
                    self.players.remove(interaction.user.mention)
                
                log_action(
                    str(interaction.guild.id),
                    str(interaction.user.id),
                    "leave_queue",
                    match_id=match.match_id
                )
                
                await interaction.response.send_message(
                    f"✅ Você saiu da fila de {self.modality_name} {self.mode_name}",
                    ephemeral=True
                )
            else:
                await interaction.response.send_message(
                    "⚠️ Você não está nesta fila",
                    ephemeral=True
                )
        
        finally:
            session.close()
    
    @discord.ui.button(label="Full ump xm8", style=discord.ButtonStyle.primary, emoji="🎮")
    async def full_ump_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Botão para modo Full UMP"""
        await interaction.response.send_message(
            "🎮 Modo Full UMP ativado",
            ephemeral=True
        )
    
    @discord.ui.button(label="Gelo Infinito", style=discord.ButtonStyle.primary, emoji="❄️")
    async def infinite_ice_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Botão para modo Gelo Infinito"""
        await interaction.response.send_message(
            "❄️ Modo Gelo Infinito ativado",
            ephemeral=True
        )
    
    @discord.ui.button(label="Gelo Normal", style=discord.ButtonStyle.primary, emoji="🧊")
    async def normal_ice_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Botão para modo Gelo Normal"""
        await interaction.response.send_message(
            "🧊 Modo Gelo Normal ativado",
            ephemeral=True
        )


class Filas(commands.Cog):
    """Cog para o comando /filas"""
    
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="filas", description="Envia as filas ativas para o canal configurado")
    async def filas(self, interaction: discord.Interaction):
        """Comando /filas - Envia as filas ativas"""
        
        # Verificar permissões
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message(
                "❌ Você precisa ser administrador para usar este comando",
                ephemeral=True
            )
            return
        
        guild_id = str(interaction.guild.id)
        guild = get_or_create_guild(guild_id)
        
        await interaction.response.defer()
        
        session = get_session()
        try:
            # Criar filas para cada modalidade ativa
            for modality_name, modality_config in MODALITIES.items():
                if not modality_config['enabled']:
                    continue
                
                for mode_name in modality_config['modes']:
                    for price in BET_VALUES:
                        # Criar match
                        match = Match(
                            guild_id=guild_id,
                            modality_id=None,
                            mode_id=None,
                            bet_value=price,
                            status='waiting',
                            match_id=generate_room_id(),
                            match_password=generate_room_password()
                        )
                        session.add(match)
                        session.flush()
                        
                        # Criar embed
                        embed = create_match_embed(modality_name, mode_name, price)
                        
                        # Criar view
                        view = QueueView(match.id, modality_name, mode_name, price)
                        
                        # Enviar para o canal
                        if guild.queue_channel_id:
                            channel = interaction.guild.get_channel(int(guild.queue_channel_id))
                            if channel:
                                await channel.send(embed=embed, view=view)
            
            session.commit()
            
            await interaction.followup.send(
                "✅ Filas enviadas com sucesso!",
                ephemeral=True
            )
            
            log_action(guild_id, str(interaction.user.id), "filas_sent")
        
        except Exception as e:
            logger.error(f"Erro ao enviar filas: {e}")
            await interaction.followup.send(
                f"❌ Erro ao enviar filas: {str(e)}",
                ephemeral=True
            )
        
        finally:
            session.close()
    
    @app_commands.command(name="filas-canal", description="Define o canal para as filas")
    @app_commands.describe(canal="Canal onde as filas serão enviadas")
    async def filas_canal(self, interaction: discord.Interaction, canal: discord.TextChannel):
        """Comando para definir o canal das filas"""
        
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message(
                "❌ Você precisa ser administrador para usar este comando",
                ephemeral=True
            )
            return
        
        guild_id = str(interaction.guild.id)
        
        session = get_session()
        try:
            guild = session.query(Guild).filter_by(guild_id=guild_id).first()
            if guild:
                guild.queue_channel_id = str(canal.id)
                session.commit()
                
                await interaction.response.send_message(
                    f"✅ Canal das filas definido para {canal.mention}",
                    ephemeral=True
                )
                
                log_action(guild_id, str(interaction.user.id), "queue_channel_set", details=str(canal.id))
        
        finally:
            session.close()


def create_match_embed(modality: str, mode: str, price: float, players: list = None) -> discord.Embed:
    """Cria o embed de partida"""
    if players is None:
        players = []
    
    embed = discord.Embed(
        title=modality,
        description=f"{modality} {mode}\nR$ {price:.2f}",
        color=discord.Color.random()
    )
    
    if players:
        players_text = "\n".join([f"@{p}" for p in players])
    else:
        players_text = "Nenhum jogador ainda"
    
    embed.add_field(
        name="🎮 Jogadores",
        value=players_text,
        inline=False
    )
    
    embed.set_footer(text="🐿️ Esquilo Aposta")
    return embed


async def setup(bot):
    """Setup da cog"""
    await bot.add_cog(Filas(bot))
