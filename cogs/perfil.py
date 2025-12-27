import discord
from discord.ext import commands
from utils import get_or_create_user, create_profile_embed, log_action
from models import get_session, User
import logging

logger = logging.getLogger(__name__)

class Perfil(commands.Cog):
    """Cog para comando de perfil"""
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="p", description="Mostra o perfil de um usuário")
    async def perfil(self, ctx, user: discord.User = None):
        """Comando .p @usuario - Mostra o perfil do usuário"""
        
        if user is None:
            user = ctx.author
        
        guild_id = str(ctx.guild.id)
        
        session = get_session()
        try:
            db_user = session.query(User).filter_by(
                user_id=str(user.id),
                guild_id=guild_id
            ).first()
            
            if not db_user:
                db_user = User(
                    user_id=str(user.id),
                    guild_id=guild_id,
                    username=user.name
                )
                session.add(db_user)
                session.commit()
            
            embed = create_profile_embed(db_user)
            
            await ctx.send(embed=embed)
            
            log_action(
                guild_id,
                str(ctx.author.id),
                "profile_viewed",
                details=f"Perfil de {user.name}"
            )
        
        finally:
            session.close()


async def setup(bot):
    """Setup da cog"""
    await bot.add_cog(Perfil(bot))
