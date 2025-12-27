import os
from dotenv import load_dotenv

load_dotenv()

# Discord Configuration
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
DISCORD_GUILD_ID = int(os.getenv('DISCORD_GUILD_ID', 0))

# Database Configuration
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', '')
DB_NAME = os.getenv('DB_NAME', 'bot_esquilo_aposta')
DB_PORT = int(os.getenv('DB_PORT', 3306))

# Database URL for SQLAlchemy
DATABASE_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Pix Configuration
PIX_KEY = os.getenv('PIX_KEY')
PIX_BANK_CODE = os.getenv('PIX_BANK_CODE', '001')
PIX_ACCOUNT_HOLDER = os.getenv('PIX_ACCOUNT_HOLDER')
PIX_ACCOUNT_NUMBER = os.getenv('PIX_ACCOUNT_NUMBER')

# Bot Configuration
BOT_PREFIX = os.getenv('BOT_PREFIX', '.')
ROOM_PRICE = float(os.getenv('ROOM_PRICE', 0.40))
COINS_WINNER = int(os.getenv('COINS_WINNER', 1))
COINS_LOSER = int(os.getenv('COINS_LOSER', 0))

# Modalities Configuration
MODALITIES = {
    'Mobile': {
        'modes': ['1v1', '2v2', '3v3', '4v4'],
        'enabled': True
    },
    'Emulador': {
        'modes': ['1v1', '2v2', '3v3', '4v4'],
        'enabled': True
    },
    'Misto': {
        'modes': ['2v2', '3v3', '4v4'],
        'enabled': True
    }
}

# Bet Values
BET_VALUES = [1.00, 2.00, 3.00, 5.00, 10.00, 20.00, 30.00, 50.00, 100.00]
