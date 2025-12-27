import discord
from discord.ext import commands
from discord import app_commands
from utils import (
    get_or_create_guild, get_or_create_user, log_action
)
from models import get_session, Match, MatchParticipant, User
from pix_utils import generate_pix_qrcode, create_pix_embed
import logging
from io import BytesIO

logger = logging.getLogger(__name__)

class MatchConfirmationView(discord.ui.View):
    """View para confirmação de partida"""
    
    def __init__(self, match_id: int, mediator_id: str):
        super().__init__(timeout=None)
        self.match_id = match_id
        self.mediator_id = mediator_id
        self.confirmations = set()
    
    @discord.ui.button(label="Confirmar", style=discord.ButtonStyle.success, emoji="✅")
    async def confirm_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Botão para confirmar partida"""
        
        self.confirmations.add(str(interaction.user.id))
        
        await interaction.response.defer()
        
        session = get_session()
        try:
            match = session.query(Match).filter_by(id=self.match_id).first()
            
            if not match:
                await interaction.followup.send(
                    "❌ Partida não encontrada",
                    ephemeral=True
                )
                return
            
            # Verificar se todos confirmaram
            participants = session.query(MatchParticipant).filter_by(match_id=self.match_id).all()
            participant_ids = {p.user_id for p in participants}
            
            if participant_ids.issubset(self.confirmations):
                # Todos confirmaram
                match.status = 'confirmed'
                session.commit()
                
                # Gerar QR Code Pix
                try:
                    qr_code_bytes = generate_pix_qrcode(match.bet_value, f"Aposta {match.match_id}")
                    
                    # Criar arquivo
                    file = discord.File(qr_code_bytes, filename="pix_qrcode.png")
                    
                    # Mediador
                    mediator = session.query(User).filter_by(user_id=self.mediator_id).first()
                    mediator_name = mediator.username if mediator else "Mediador"
                    
                    # Criar embed
                    embed = create_pix_embed(match.bet_value, match.match_id, mediator_name)
                    
                    # Enviar QR Code
                    await interaction.channel.send(
                        embed=embed,
                        file=file
                    )
                    
                    log_action(
                        str(interaction.guild.id),
                        str(interaction.user.id),
                        "match_confirmed",
                        match_id=match.match_id
                    )
                
                except Exception as e:
                    logger.error(f"Erro ao gerar QR Code: {e}")
                    await interaction.channel.send(
                        f"❌ Erro ao gerar QR Code: {str(e)}"
                    )
            else:
                await interaction.followup.send(
                    f"✅ Você confirmou! Aguardando confirmação dos outros jogadores...",
                    ephemeral=True
                )
        
        finally:
            session.close()
    
    @discord.ui.button(label="Encerrar", style=discord.ButtonStyle.danger, emoji="❌")
    async def cancel_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Botão para encerrar partida"""
        
        # Apenas mediador pode encerrar
        if str(interaction.user.id) != self.mediator_id:
            await interaction.response.send_message(
                "❌ Apenas o mediador pode encerrar a partida",
                ephemeral=True
            )
            return
        
        session = get_session()
        try:
            match = session.query(Match).filter_by(id=self.match_id).first()
            
            if match:
                match.status = 'cancelled'
                session.commit()
                
                await interaction.response.send_message(
                    "❌ Partida encerrada pelo mediador",
                    ephemeral=False
                )
                
                log_action(
                    str(interaction.guild.id),
                    str(interaction.user.id),
                    "match_cancelled",
                    match_id=match.match_id
                )
        
        finally:
            session.close()


class MatchFlow(commands.Cog):
    """Cog para fluxo de partida"""
    
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="confirmar-partida", description="Cria painel de confirmação de partida")
    @app_commands.describe(
        match_id="ID da partida",
        mediador="Mediador da partida"
    )
    async def confirmar_partida(
        self,
        interaction: discord.Interaction,
        match_id: str,
        mediador: discord.User
    ):
        """Comando para criar painel de confirmação"""
        
        guild_id = str(interaction.guild.id)
        
        session = get_session()
        try:
            match = session.query(Match).filter_by(match_id=match_id).first()
            
            if not match:
                await interaction.response.send_message(
                    "❌ Partida não encontrada",
                    ephemeral=True
                )
                return
            
            # Criar embed de confirmação
            embed = discord.Embed(
                title="🎮 Confirmação de Partida",
                description=f"Clique em **Confirmar** para iniciar a partida",
                color=discord.Color.blue()
            )
            
            embed.add_field(
                name="📱 Modalidade",
                value=match.modality.name if match.modality else "N/A",
                inline=True
            )
            
            embed.add_field(
                name="🎯 Modo",
                value=match.mode.name if match.mode else "N/A",
                inline=True
            )
            
            embed.add_field(
                name="💰 Valor",
                value=f"R$ {match.bet_value:.2f}",
                inline=True
            )
            
            embed.add_field(
                name="🆔 ID da Sala",
                value=f"`{match.match_id}`",
                inline=False
            )
            
            embed.add_field(
                name="🔐 Senha",
                value=f"`{match.match_password}`",
                inline=False
            )
            
            embed.set_footer(text="🐿️ Esquilo Aposta")
            
            # Criar view
            view = MatchConfirmationView(match.id, str(mediador.id))
            
            await interaction.response.send_message(embed=embed, view=view)
            
            log_action(
                guild_id,
                str(interaction.user.id),
                "match_confirmation_panel_created",
                match_id=match_id
            )
        
        finally:
            session.close()
    
    @app_commands.command(name="resultado", description="Registra o resultado da partida")
    @app_commands.describe(
        match_id="ID da partida",
        vencedor="Time vencedor (team1 ou team2)"
    )
    async def resultado(
        self,
        interaction: discord.Interaction,
        match_id: str,
        vencedor: str
    ):
        """Comando para registrar resultado"""
        
        if vencedor not in ['team1', 'team2']:
            await interaction.response.send_message(
                "❌ Vencedor inválido. Use 'team1' ou 'team2'",
                ephemeral=True
            )
            return
        
        guild_id = str(interaction.guild.id)
        
        session = get_session()
        try:
            match = session.query(Match).filter_by(match_id=match_id).first()
            
            if not match:
                await interaction.response.send_message(
                    "❌ Partida não encontrada",
                    ephemeral=True
                )
                return
            
            match.status = 'completed'
            match.winner_team = vencedor
            
            # Atualizar estatísticas dos jogadores
            participants = session.query(MatchParticipant).filter_by(match_id=match.id).all()
            
            for participant in participants:
                user = session.query(User).filter_by(user_id=participant.user_id).first()
                
                if user:
                    if participant.team == vencedor:
                        user.wins += 1
                        user.coins += match.bet_value
                    else:
                        user.losses += 1
            
            session.commit()
            
            await interaction.response.send_message(
                f"✅ Resultado registrado! Time {vencedor} venceu!",
                ephemeral=True
            )
            
            log_action(
                guild_id,
                str(interaction.user.id),
                "match_result_registered",
                match_id=match_id,
                details=f"Vencedor: {vencedor}"
            )
        
        finally:
            session.close()


async def setup(bot):
    """Setup da cog"""
    await bot.add_cog(MatchFlow(bot))
