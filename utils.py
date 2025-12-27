import discord
import random
import string
from datetime import datetime
from models import get_session, Guild, User, Log
from config import MODALITIES, BET_VALUES

def generate_room_id() -> str:
    """Gera um ID único para a sala"""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

def generate_room_password() -> str:
    """Gera uma senha aleatória para a sala"""
    return ''.join(random.choices(string.digits, k=4))

def get_or_create_guild(guild_id: str) -> 'Guild':
    """Obtém ou cria uma guilda no banco de dados"""
    session = get_session()
    try:
        guild = session.query(Guild).filter_by(guild_id=str(guild_id)).first()
        if not guild:
            guild = Guild(guild_id=str(guild_id))
            session.add(guild)
            session.commit()
        return guild
    finally:
        session.close()

def get_or_create_user(user_id: str, guild_id: str, username: str) -> 'User':
    """Obtém ou cria um usuário no banco de dados"""
    session = get_session()
    try:
        user = session.query(User).filter_by(
            user_id=str(user_id),
            guild_id=str(guild_id)
        ).first()
        
        if not user:
            user = User(
                user_id=str(user_id),
                guild_id=str(guild_id),
                username=username
            )
            session.add(user)
            session.commit()
        return user
    finally:
        session.close()

def log_action(guild_id: str, user_id: str, action: str, match_id: str = None, details: str = None):
    """Registra uma ação no banco de dados"""
    session = get_session()
    try:
        log = Log(
            guild_id=str(guild_id),
            user_id=str(user_id),
            action=action,
            match_id=match_id,
            details=details
        )
        session.add(log)
        session.commit()
    finally:
        session.close()

def create_central_embed() -> discord.Embed:
    """Cria o embed da central de configurações"""
    embed = discord.Embed(
        title="🐿️ Central da Org Esquilo",
        description="Tudo o que você precisa para administrar a org está aqui.\nUse o menu abaixo para acessar as configurações disponíveis.",
        color=discord.Color.brown()
    )
    embed.set_footer(text="🐿️ Esquilo Aposta")
    embed.timestamp = datetime.utcnow()
    return embed

def create_general_config_embed(guild: 'Guild') -> discord.Embed:
    """Cria o embed de configurações gerais"""
    embed = discord.Embed(
        title="⚙️ Configurações Gerais",
        description="Configure as opções gerais da organização",
        color=discord.Color.blue()
    )
    
    embed.add_field(
        name="📍 Canal das Threads",
        value=f"<#{guild.queue_channel_id}>" if guild.queue_channel_id else "Não configurado",
        inline=False
    )
    
    embed.add_field(
        name="💰 Valor da Sala",
        value=f"R$ {guild.room_price:.2f}",
        inline=True
    )
    
    embed.add_field(
        name="🎯 Valores de Aposta",
        value=", ".join([f"R$ {v:.2f}" for v in BET_VALUES]),
        inline=False
    )
    
    embed.set_footer(text="🐿️ Esquilo Aposta")
    embed.timestamp = datetime.utcnow()
    return embed

def create_matches_config_embed(guild: 'Guild') -> discord.Embed:
    """Cria o embed de configuração de partidas"""
    embed = discord.Embed(
        title="🎮 Configurações da Fila",
        description="Configure as modalidades e filas de partidas",
        color=discord.Color.purple()
    )
    
    # Adicionar status das modalidades
    for modality_name, modality_config in MODALITIES.items():
        status = "✅" if modality_config['enabled'] else "❌"
        modes = ", ".join(modality_config['modes'])
        embed.add_field(
            name=f"{status} {modality_name}",
            value=modes,
            inline=False
        )
    
    embed.add_field(
        name="🪙 Coins - Vencedor",
        value=f"{guild.coins_winner} coin",
        inline=True
    )
    
    embed.add_field(
        name="🪙 Coins - Perdedor",
        value=f"{guild.coins_loser} coin",
        inline=True
    )
    
    embed.set_footer(text="🐿️ Esquilo Aposta • Esquilo Aposta")
    embed.timestamp = datetime.utcnow()
    return embed

def create_roles_config_embed(guild: 'Guild') -> discord.Embed:
    """Cria o embed de configuração de cargos"""
    embed = discord.Embed(
        title="👥 Central de Cargos",
        description="Configure agora os cargos",
        color=discord.Color.orange()
    )
    
    embed.add_field(
        name="🎖️ Mediador",
        value=f"<@&{guild.mediator_role_id}>" if guild.mediator_role_id else "Não configurado",
        inline=False
    )
    
    embed.add_field(
        name="📊 Analista",
        value=f"<@&{guild.analyst_role_id}>" if guild.analyst_role_id else "Não configurado",
        inline=False
    )
    
    embed.set_footer(text="🐿️ Esquilo Aposta")
    embed.timestamp = datetime.utcnow()
    return embed

def create_logs_config_embed(guild: 'Guild') -> discord.Embed:
    """Cria o embed de configuração de logs"""
    embed = discord.Embed(
        title="📋 Sistema de Logs",
        description="Configure os canais de logs",
        color=discord.Color.green()
    )
    
    embed.add_field(
        name="🎖️ Mediador",
        value=f"<#{guild.mediator_log_channel_id}>" if guild.mediator_log_channel_id else "Não configurado",
        inline=False
    )
    
    embed.add_field(
        name="🎮 Partida",
        value=f"<#{guild.match_log_channel_id}>" if guild.match_log_channel_id else "Não configurado",
        inline=False
    )
    
    embed.set_footer(text="🐿️ Esquilo Aposta")
    embed.timestamp = datetime.utcnow()
    return embed

def create_modality_config_embed(modality_name: str) -> discord.Embed:
    """Cria o embed de configuração de modalidade"""
    embed = discord.Embed(
        title=f"📱 Canal {modality_name}",
        description="Configure canal e botões da embed de partida",
        color=discord.Color.blue()
    )
    
    modes = MODALITIES[modality_name]['modes']
    embed.add_field(
        name="🎮 Modos Disponíveis",
        value=", ".join(modes),
        inline=False
    )
    
    embed.set_footer(text="🐿️ Esquilo Aposta")
    embed.timestamp = datetime.utcnow()
    return embed

def create_match_embed(modality: str, mode: str, price: float, players: list = None) -> discord.Embed:
    """Cria o embed de partida"""
    if players is None:
        players = []
    
    embed = discord.Embed(
        title=modality,
        description=f"{modality} {mode}\nR$ {price:.2f}",
        color=discord.Color.random()
    )
    
    # Adicionar jogadores
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
    embed.timestamp = datetime.utcnow()
    return embed

def create_mediator_panel_embed() -> discord.Embed:
    """Cria o embed do painel de mediador"""
    embed = discord.Embed(
        title="🎖️ Painel de Mediador",
        description="Entre já como Mediador",
        color=discord.Color.gold()
    )
    
    embed.set_footer(text="🐿️ Esquilo Aposta")
    embed.timestamp = datetime.utcnow()
    return embed

def create_room_info_embed(room_id: str, room_password: str) -> discord.Embed:
    """Cria o embed com informações da sala"""
    embed = discord.Embed(
        title="🔑 Dados da Sala",
        description="Compartilhe essas informações com os jogadores",
        color=discord.Color.green()
    )
    
    embed.add_field(
        name="🆔 ID da Sala",
        value=f"`{room_id}`",
        inline=False
    )
    
    embed.add_field(
        name="🔐 Senha",
        value=f"`{room_password}`",
        inline=False
    )
    
    embed.set_footer(text="🐿️ Esquilo Aposta")
    embed.timestamp = datetime.utcnow()
    return embed

def create_profile_embed(user: 'User') -> discord.Embed:
    """Cria o embed do perfil do usuário"""
    embed = discord.Embed(
        title=f"👤 Perfil de {user.username}",
        color=discord.Color.blue()
    )
    
    embed.add_field(
        name="🏆 Vitórias",
        value=str(user.wins),
        inline=True
    )
    
    embed.add_field(
        name="💔 Derrotas",
        value=str(user.losses),
        inline=True
    )
    
    embed.add_field(
        name="🪙 Coins",
        value=f"{user.coins:.2f}",
        inline=True
    )
    
    if user.wins + user.losses > 0:
        win_rate = (user.wins / (user.wins + user.losses)) * 100
        embed.add_field(
            name="📊 Taxa de Vitória",
            value=f"{win_rate:.1f}%",
            inline=True
        )
    
    embed.set_footer(text="🐿️ Esquilo Aposta")
    embed.timestamp = datetime.utcnow()
    return embed
