import discord
from discord.ext import commands
from discord import app_commands
from utils import (
    get_or_create_guild, create_central_embed, create_general_config_embed,
    create_matches_config_embed, create_roles_config_embed, create_logs_config_embed,
    create_modality_config_embed, log_action
)
from models import get_session, Guild, Modality, Mode
from config import MODALITIES, BET_VALUES
import logging

logger = logging.getLogger(__name__)

class CentralView(discord.ui.View):
    """View para o menu principal da central"""
    
    def __init__(self, guild_id: str):
        super().__init__(timeout=None)
        self.guild_id = guild_id
    
    @discord.ui.select(
        placeholder="Escolha uma opção",
        options=[
            discord.SelectOption(label="Configs gerais", value="general", emoji="⚙️"),
            discord.SelectOption(label="Partidas", value="matches", emoji="🎮"),
            discord.SelectOption(label="Cargos", value="roles", emoji="👥"),
            discord.SelectOption(label="Sistema de Logs", value="logs", emoji="📋"),
        ]
    )
    async def select_menu(self, interaction: discord.Interaction, select: discord.ui.Select):
        await interaction.response.defer()
        
        guild = get_or_create_guild(self.guild_id)
        
        if select.values[0] == "general":
            embed = create_general_config_embed(guild)
            view = GeneralConfigView(self.guild_id)
            await interaction.followup.send(embed=embed, view=view, ephemeral=True)
        
        elif select.values[0] == "matches":
            embed = create_matches_config_embed(guild)
            view = MatchesConfigView(self.guild_id)
            await interaction.followup.send(embed=embed, view=view, ephemeral=True)
        
        elif select.values[0] == "roles":
            embed = create_roles_config_embed(guild)
            view = RolesConfigView(self.guild_id)
            await interaction.followup.send(embed=embed, view=view, ephemeral=True)
        
        elif select.values[0] == "logs":
            embed = create_logs_config_embed(guild)
            view = LogsConfigView(self.guild_id)
            await interaction.followup.send(embed=embed, view=view, ephemeral=True)


class GeneralConfigView(discord.ui.View):
    """View para configurações gerais"""
    
    def __init__(self, guild_id: str):
        super().__init__(timeout=None)
        self.guild_id = guild_id
    
    @discord.ui.button(label="Valor Sala", style=discord.ButtonStyle.primary, emoji="💰")
    async def room_value_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        modal = RoomValueModal(self.guild_id)
        await interaction.response.send_modal(modal)
    
    @discord.ui.button(label="Valores das embeds", style=discord.ButtonStyle.primary, emoji="💵")
    async def bet_values_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="💵 Valores de Aposta",
            description="Valores disponíveis para apostas",
            color=discord.Color.gold()
        )
        
        values_text = ", ".join([f"R$ {v:.2f}" for v in BET_VALUES])
        embed.add_field(name="Valores", value=values_text, inline=False)
        
        view = BetValuesView(self.guild_id)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
    
    @discord.ui.button(label="Voltar", style=discord.ButtonStyle.danger, emoji="↩️")
    async def back_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = create_central_embed()
        view = CentralView(self.guild_id)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)


class RoomValueModal(discord.ui.Modal, title="Editar Valor da Sala"):
    """Modal para editar valor da sala"""
    
    value = discord.ui.TextInput(
        label="Novo valor (R$)",
        placeholder="0.40",
        required=True
    )
    
    def __init__(self, guild_id: str):
        super().__init__()
        self.guild_id = guild_id
    
    async def on_submit(self, interaction: discord.Interaction):
        try:
            new_value = float(self.value.value)
            
            session = get_session()
            try:
                guild = session.query(Guild).filter_by(guild_id=str(self.guild_id)).first()
                if guild:
                    guild.room_price = new_value
                    session.commit()
                    
                    log_action(
                        self.guild_id,
                        str(interaction.user.id),
                        "room_price_updated",
                        details=f"Novo valor: R$ {new_value:.2f}"
                    )
                    
                    await interaction.response.send_message(
                        f"✅ Valor da sala atualizado para R$ {new_value:.2f}",
                        ephemeral=True
                    )
            finally:
                session.close()
        
        except ValueError:
            await interaction.response.send_message(
                "❌ Valor inválido. Digite um número válido.",
                ephemeral=True
            )


class BetValuesView(discord.ui.View):
    """View para gerenciar valores de aposta"""
    
    def __init__(self, guild_id: str):
        super().__init__(timeout=None)
        self.guild_id = guild_id
    
    @discord.ui.button(label="Adicionar", style=discord.ButtonStyle.success, emoji="➕")
    async def add_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        modal = AddBetValueModal(self.guild_id)
        await interaction.response.send_modal(modal)
    
    @discord.ui.button(label="Remover", style=discord.ButtonStyle.danger, emoji="➖")
    async def remove_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        options = [
            discord.SelectOption(label=f"R$ {v:.2f}", value=str(v))
            for v in BET_VALUES
        ]
        
        select = discord.ui.Select(
            placeholder="Escolha um valor para remover",
            options=options
        )
        
        async def select_callback(select_interaction: discord.Interaction):
            # Implementar remoção de valor
            await select_interaction.response.send_message(
                "❌ Remoção de valores ainda não implementada",
                ephemeral=True
            )
        
        select.callback = select_callback
        view = discord.ui.View()
        view.add_item(select)
        
        await interaction.response.send_message(
            "Escolha um valor para remover:",
            view=view,
            ephemeral=True
        )
    
    @discord.ui.button(label="Voltar", style=discord.ButtonStyle.danger, emoji="↩️")
    async def back_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = create_general_config_embed(get_or_create_guild(self.guild_id))
        view = GeneralConfigView(self.guild_id)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)


class AddBetValueModal(discord.ui.Modal, title="Adicionar Valor de Aposta"):
    """Modal para adicionar novo valor de aposta"""
    
    value = discord.ui.TextInput(
        label="Novo valor (R$)",
        placeholder="25.00",
        required=True
    )
    
    def __init__(self, guild_id: str):
        super().__init__()
        self.guild_id = guild_id
    
    async def on_submit(self, interaction: discord.Interaction):
        try:
            new_value = float(self.value.value)
            
            if new_value not in BET_VALUES:
                BET_VALUES.append(new_value)
                BET_VALUES.sort()
                
                await interaction.response.send_message(
                    f"✅ Valor R$ {new_value:.2f} adicionado com sucesso",
                    ephemeral=True
                )
            else:
                await interaction.response.send_message(
                    f"⚠️ Valor R$ {new_value:.2f} já existe",
                    ephemeral=True
                )
        
        except ValueError:
            await interaction.response.send_message(
                "❌ Valor inválido. Digite um número válido.",
                ephemeral=True
            )


class MatchesConfigView(discord.ui.View):
    """View para configurações de partidas"""
    
    def __init__(self, guild_id: str):
        super().__init__(timeout=None)
        self.guild_id = guild_id
    
    @discord.ui.button(label="Coins", style=discord.ButtonStyle.primary, emoji="🪙")
    async def coins_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        modal = CoinsModal(self.guild_id)
        await interaction.response.send_modal(modal)
    
    @discord.ui.select(
        placeholder="Escolha uma modalidade",
        options=[
            discord.SelectOption(label="Mobile", value="Mobile", emoji="📱"),
            discord.SelectOption(label="Emulador", value="Emulador", emoji="💻"),
            discord.SelectOption(label="Misto", value="Misto", emoji="🔀"),
        ]
    )
    async def modality_select(self, interaction: discord.Interaction, select: discord.ui.Select):
        modality_name = select.values[0]
        embed = create_modality_config_embed(modality_name)
        view = ModalityConfigView(self.guild_id, modality_name)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
    
    @discord.ui.button(label="Voltar", style=discord.ButtonStyle.danger, emoji="↩️")
    async def back_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = create_central_embed()
        view = CentralView(self.guild_id)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)


class CoinsModal(discord.ui.Modal, title="Configurar Coins"):
    """Modal para configurar coins de vencedor/perdedor"""
    
    winner_coins = discord.ui.TextInput(
        label="Coins para vencedor",
        placeholder="1",
        required=True
    )
    
    loser_coins = discord.ui.TextInput(
        label="Coins para perdedor",
        placeholder="0",
        required=True
    )
    
    def __init__(self, guild_id: str):
        super().__init__()
        self.guild_id = guild_id
    
    async def on_submit(self, interaction: discord.Interaction):
        try:
            winner = int(self.winner_coins.value)
            loser = int(self.loser_coins.value)
            
            session = get_session()
            try:
                guild = session.query(Guild).filter_by(guild_id=str(self.guild_id)).first()
                if guild:
                    guild.coins_winner = winner
                    guild.coins_loser = loser
                    session.commit()
                    
                    await interaction.response.send_message(
                        f"✅ Coins atualizados:\n• Vencedor: {winner}\n• Perdedor: {loser}",
                        ephemeral=True
                    )
            finally:
                session.close()
        
        except ValueError:
            await interaction.response.send_message(
                "❌ Valores inválidos. Digite números inteiros.",
                ephemeral=True
            )


class ModalityConfigView(discord.ui.View):
    """View para configuração de modalidade"""
    
    def __init__(self, guild_id: str, modality_name: str):
        super().__init__(timeout=None)
        self.guild_id = guild_id
        self.modality_name = modality_name
    
    @discord.ui.button(label="Status ✅", style=discord.ButtonStyle.success, emoji="🔄")
    async def status_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Implementar toggle de status
        MODALITIES[self.modality_name]['enabled'] = not MODALITIES[self.modality_name]['enabled']
        status = "ativada" if MODALITIES[self.modality_name]['enabled'] else "desativada"
        
        await interaction.response.send_message(
            f"✅ Modalidade {self.modality_name} {status}",
            ephemeral=True
        )
    
    @discord.ui.button(label="Voltar", style=discord.ButtonStyle.danger, emoji="↩️")
    async def back_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = create_matches_config_embed(get_or_create_guild(self.guild_id))
        view = MatchesConfigView(self.guild_id)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)


class RolesConfigView(discord.ui.View):
    """View para configuração de cargos"""
    
    def __init__(self, guild_id: str):
        super().__init__(timeout=None)
        self.guild_id = guild_id
    
    @discord.ui.select(
        placeholder="Escolha o cargo de Mediador",
        min_values=1,
        max_values=1
    )
    async def mediator_role_select(self, interaction: discord.Interaction, select: discord.ui.Select):
        role_id = select.values[0]
        
        session = get_session()
        try:
            guild = session.query(Guild).filter_by(guild_id=str(self.guild_id)).first()
            if guild:
                guild.mediator_role_id = role_id
                session.commit()
                
                await interaction.response.send_message(
                    f"✅ Cargo de Mediador definido",
                    ephemeral=True
                )
        finally:
            session.close()
    
    @discord.ui.button(label="Voltar", style=discord.ButtonStyle.danger, emoji="↩️")
    async def back_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = create_central_embed()
        view = CentralView(self.guild_id)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)


class LogsConfigView(discord.ui.View):
    """View para configuração de logs"""
    
    def __init__(self, guild_id: str):
        super().__init__(timeout=None)
        self.guild_id = guild_id
    
    @discord.ui.button(label="Voltar", style=discord.ButtonStyle.danger, emoji="↩️")
    async def back_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = create_central_embed()
        view = CentralView(self.guild_id)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)


class Central(commands.Cog):
    """Cog para o comando /central"""
    
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="central", description="Abre a central de configurações da organização")
    async def central(self, interaction: discord.Interaction):
        """Comando /central - Abre a central de configurações"""
        
        # Verificar permissões (apenas admin)
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message(
                "❌ Você precisa ser administrador para usar este comando",
                ephemeral=True
            )
            return
        
        guild_id = str(interaction.guild.id)
        get_or_create_guild(guild_id)
        
        embed = create_central_embed()
        view = CentralView(guild_id)
        
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
        
        log_action(guild_id, str(interaction.user.id), "central_opened")


async def setup(bot):
    """Setup da cog"""
    await bot.add_cog(Central(bot))
