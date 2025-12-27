import discord
from discord.ext import commands
from discord import app_commands
from utils import (
    get_or_create_guild, get_or_create_user, create_mediator_panel_embed,
    create_room_info_embed, log_action
)
from models import get_session, Guild, User
import logging

logger = logging.getLogger(__name__)

class MediatorPanelView(discord.ui.View):
    """View para o painel de mediador"""
    
    def __init__(self, guild_id: str):
        super().__init__(timeout=None)
        self.guild_id = guild_id
    
    @discord.ui.button(label="Entrar", style=discord.ButtonStyle.success, emoji="✅")
    async def enter_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Botão para entrar como mediador"""
        
        session = get_session()
        try:
            user = session.query(User).filter_by(
                user_id=str(interaction.user.id),
                guild_id=str(self.guild_id)
            ).first()
            
            if not user:
                user = User(
                    user_id=str(interaction.user.id),
                    guild_id=str(self.guild_id),
                    username=interaction.user.name,
                    is_mediator=True
                )
                session.add(user)
            else:
                user.is_mediator = True
            
            session.commit()
            
            log_action(
                str(self.guild_id),
                str(interaction.user.id),
                "mediator_login"
            )
            
            await interaction.response.send_message(
                "✅ Você entrou como mediador!",
                ephemeral=True
            )
        
        finally:
            session.close()
    
    @discord.ui.button(label="Sair", style=discord.ButtonStyle.danger, emoji="❌")
    async def leave_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Botão para sair como mediador"""
        
        session = get_session()
        try:
            user = session.query(User).filter_by(
                user_id=str(interaction.user.id),
                guild_id=str(self.guild_id)
            ).first()
            
            if user:
                user.is_mediator = False
                session.commit()
                
                log_action(
                    str(self.guild_id),
                    str(interaction.user.id),
                    "mediator_logout"
                )
                
                await interaction.response.send_message(
                    "✅ Você saiu como mediador!",
                    ephemeral=True
                )
        
        finally:
            session.close()
    
    @discord.ui.button(label="Configurar Pix", style=discord.ButtonStyle.primary, emoji="💳")
    async def configure_pix_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Botão para configurar Pix"""
        
        modal = PixConfigModal(self.guild_id)
        await interaction.response.send_modal(modal)


class PixConfigModal(discord.ui.Modal, title="Configurar Pix"):
    """Modal para configurar dados de Pix"""
    
    bank = discord.ui.TextInput(
        label="Banco",
        placeholder="001",
        required=True
    )
    
    account_holder = discord.ui.TextInput(
        label="Nome",
        placeholder="Seu Nome",
        required=True
    )
    
    pix_key = discord.ui.TextInput(
        label="Chave Pix",
        placeholder="seu-email@email.com ou CPF",
        required=True
    )
    
    def __init__(self, guild_id: str):
        super().__init__()
        self.guild_id = guild_id
    
    async def on_submit(self, interaction: discord.Interaction):
        session = get_session()
        try:
            user = session.query(User).filter_by(
                user_id=str(interaction.user.id),
                guild_id=str(self.guild_id)
            ).first()
            
            if not user:
                user = User(
                    user_id=str(interaction.user.id),
                    guild_id=str(self.guild_id),
                    username=interaction.user.name
                )
                session.add(user)
            
            user.pix_bank = self.bank.value
            user.pix_account_holder = self.account_holder.value
            user.pix_key = self.pix_key.value
            
            session.commit()
            
            log_action(
                str(self.guild_id),
                str(interaction.user.id),
                "pix_configured"
            )
            
            await interaction.response.send_message(
                "✅ Dados de Pix configurados com sucesso!",
                ephemeral=True
            )
        
        finally:
            session.close()


class Mediador(commands.Cog):
    """Cog para comandos de mediador"""
    
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="tp-mediador", description="Define o canal do painel de mediador")
    @app_commands.describe(canal="Canal onde o painel será enviado")
    async def tp_mediador(self, interaction: discord.Interaction, canal: discord.TextChannel):
        """Comando /tp-mediador - Define canal do painel de mediador"""
        
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
                guild.mediator_panel_channel_id = str(canal.id)
                session.commit()
                
                # Enviar embed do painel
                embed = create_mediator_panel_embed()
                view = MediatorPanelView(guild_id)
                
                await canal.send(embed=embed, view=view)
                
                await interaction.response.send_message(
                    f"✅ Painel de mediador enviado para {canal.mention}",
                    ephemeral=True
                )
                
                log_action(guild_id, str(interaction.user.id), "mediator_panel_set", details=str(canal.id))
        
        finally:
            session.close()
    
    @app_commands.command(name="id", description="Informa o ID e senha da sala")
    @app_commands.describe(
        id_sala="ID da sala",
        senha="Senha da sala"
    )
    async def id_command(self, interaction: discord.Interaction, id_sala: str, senha: str):
        """Comando /id - Informa ID e senha da sala"""
        
        guild_id = str(interaction.guild.id)
        
        embed = create_room_info_embed(id_sala, senha)
        
        await interaction.response.send_message(embed=embed)
        
        log_action(
            guild_id,
            str(interaction.user.id),
            "room_info_sent",
            match_id=id_sala
        )


async def setup(bot):
    """Setup da cog"""
    await bot.add_cog(Mediador(bot))
