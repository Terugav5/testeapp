from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
from config import DATABASE_URL

Base = declarative_base()

class Guild(Base):
    __tablename__ = 'guilds'
    
    id = Column(Integer, primary_key=True)
    guild_id = Column(String(50), unique=True, nullable=False)
    queue_channel_id = Column(String(50))
    mediator_panel_channel_id = Column(String(50))
    mediator_log_channel_id = Column(String(50))
    match_log_channel_id = Column(String(50))
    mediator_role_id = Column(String(50))
    analyst_role_id = Column(String(50))
    room_price = Column(Float, default=0.40)
    coins_winner = Column(Integer, default=1)
    coins_loser = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    matches = relationship('Match', back_populates='guild')
    modalities = relationship('Modality', back_populates='guild')
    users = relationship('User', back_populates='guild')
    logs = relationship('Log', back_populates='guild')


class Modality(Base):
    __tablename__ = 'modalities'
    
    id = Column(Integer, primary_key=True)
    guild_id = Column(String(50), ForeignKey('guilds.guild_id'))
    name = Column(String(50), nullable=False)  # Mobile, Emulador, Misto
    enabled = Column(Boolean, default=True)
    queue_channel_id = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    guild = relationship('Guild', back_populates='modalities')
    modes = relationship('Mode', back_populates='modality')
    matches = relationship('Match', back_populates='modality')


class Mode(Base):
    __tablename__ = 'modes'
    
    id = Column(Integer, primary_key=True)
    modality_id = Column(Integer, ForeignKey('modalities.id'))
    name = Column(String(10), nullable=False)  # 1v1, 2v2, etc
    enabled = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    modality = relationship('Modality', back_populates='modes')
    matches = relationship('Match', back_populates='mode')


class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(String(50), nullable=False)
    guild_id = Column(String(50), ForeignKey('guilds.guild_id'))
    username = Column(String(100), nullable=False)
    wins = Column(Integer, default=0)
    losses = Column(Integer, default=0)
    coins = Column(Float, default=0.0)
    is_mediator = Column(Boolean, default=False)
    pix_key = Column(String(100))
    pix_bank = Column(String(10))
    pix_account_holder = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    guild = relationship('Guild', back_populates='users')
    matches_as_mediator = relationship('Match', foreign_keys='Match.mediator_id', back_populates='mediator')
    participants = relationship('MatchParticipant', back_populates='user')


class Match(Base):
    __tablename__ = 'matches'
    
    id = Column(Integer, primary_key=True)
    guild_id = Column(String(50), ForeignKey('guilds.guild_id'))
    modality_id = Column(Integer, ForeignKey('modalities.id'))
    mode_id = Column(Integer, ForeignKey('modes.id'))
    mediator_id = Column(String(50), ForeignKey('users.user_id'))
    thread_id = Column(String(50))
    match_id = Column(String(20), unique=True)  # ID da sala
    match_password = Column(String(20))  # Senha da sala
    bet_value = Column(Float, nullable=False)
    status = Column(String(20), default='waiting')  # waiting, full, confirmed, completed, cancelled
    winner_team = Column(String(10))  # team1 ou team2
    created_at = Column(DateTime, default=datetime.utcnow)
    confirmed_at = Column(DateTime)
    completed_at = Column(DateTime)
    
    guild = relationship('Guild', back_populates='matches')
    modality = relationship('Modality', back_populates='matches')
    mode = relationship('Mode', back_populates='matches')
    mediator = relationship('User', foreign_keys=[mediator_id], back_populates='matches_as_mediator')
    participants = relationship('MatchParticipant', back_populates='match')


class MatchParticipant(Base):
    __tablename__ = 'match_participants'
    
    id = Column(Integer, primary_key=True)
    match_id = Column(Integer, ForeignKey('matches.id'))
    user_id = Column(String(50), ForeignKey('users.user_id'))
    team = Column(String(10))  # team1 ou team2
    joined_at = Column(DateTime, default=datetime.utcnow)
    
    match = relationship('Match', back_populates='participants')
    user = relationship('User', back_populates='participants')


class Log(Base):
    __tablename__ = 'logs'
    
    id = Column(Integer, primary_key=True)
    guild_id = Column(String(50), ForeignKey('guilds.guild_id'))
    user_id = Column(String(50))
    action = Column(String(50), nullable=False)  # join_queue, leave_queue, match_confirmed, etc
    match_id = Column(String(20))
    details = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    guild = relationship('Guild', back_populates='logs')


class BetValue(Base):
    __tablename__ = 'bet_values'
    
    id = Column(Integer, primary_key=True)
    guild_id = Column(String(50), unique=True, nullable=False)
    values = Column(Text, nullable=False)  # JSON string of bet values
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


# Create engine and session
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)

def get_session():
    """Get database session"""
    return SessionLocal()
