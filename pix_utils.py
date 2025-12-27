import qrcode
import io
from datetime import datetime
import uuid
from config import PIX_KEY, PIX_BANK_CODE, PIX_ACCOUNT_HOLDER, PIX_ACCOUNT_NUMBER

def generate_pix_qrcode(amount: float, description: str = None) -> io.BytesIO:
    """
    Gera um QR Code Pix com os dados da transação.
    
    Args:
        amount: Valor da transação em reais
        description: Descrição da transação (opcional)
    
    Returns:
        BytesIO object com a imagem PNG do QR Code
    """
    
    # Estrutura do Pix Copia e Cola (EMV)
    # Formato: 00020126360014br.gov.bcb.pix...
    
    if not PIX_KEY:
        raise ValueError("PIX_KEY não configurada no arquivo .env")
    
    # Gerar ID único para a transação
    transaction_id = str(uuid.uuid4())[:8].upper()
    
    # Montar a string Pix
    pix_string = mount_pix_string(
        pix_key=PIX_KEY,
        amount=amount,
        description=description or f"Aposta Esquilo - {transaction_id}",
        merchant_name=PIX_ACCOUNT_HOLDER or "Bot Esquilo",
        merchant_city="Sao Paulo"
    )
    
    # Gerar QR Code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=2,
    )
    qr.add_data(pix_string)
    qr.make(fit=True)
    
    # Criar imagem
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Converter para BytesIO
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    
    return img_bytes


def mount_pix_string(pix_key: str, amount: float, description: str, 
                     merchant_name: str, merchant_city: str) -> str:
    """
    Monta a string Pix no formato EMV (Copia e Cola).
    
    Args:
        pix_key: Chave Pix (CPF, CNPJ, Email ou Telefone)
        amount: Valor em reais
        description: Descrição da transação
        merchant_name: Nome do recebedor
        merchant_city: Cidade do recebedor
    
    Returns:
        String Pix formatada
    """
    
    # Formato EMV Pix
    payload = "00020126360014br.gov.bcb.pix"
    
    # Adicionar chave Pix
    payload += f"0136{len(pix_key):02d}{pix_key}"
    
    # Adicionar informações do merchant
    merchant_info = f"5204{merchant_name[:25]}"
    payload += f"52{len(merchant_info):02d}{merchant_info}"
    
    # Adicionar cidade
    city_info = f"05{len(merchant_city):02d}{merchant_city}"
    payload += f"50{len(city_info):02d}{city_info}"
    
    # Adicionar valor (se houver)
    if amount > 0:
        amount_str = f"{amount:.2f}".replace(".", "")
        payload += f"54{len(amount_str):02d}{amount_str}"
    
    # Adicionar descrição
    if description:
        desc_info = f"05{len(description):02d}{description}"
        payload += f"62{len(desc_info):02d}{desc_info}"
    
    # Adicionar checksum (CRC16)
    payload += "63"
    crc = calculate_crc16(payload + "0000")
    payload += f"{crc:04X}"
    
    return payload


def calculate_crc16(data: str) -> int:
    """
    Calcula o CRC16 para validação da string Pix.
    
    Args:
        data: String a ser validada
    
    Returns:
        Valor CRC16
    """
    crc = 0xFFFF
    
    for byte in data.encode():
        crc ^= byte << 8
        for _ in range(8):
            crc <<= 1
            if crc & 0x10000:
                crc ^= 0x1021
            crc &= 0xFFFF
    
    return crc


def create_pix_embed(amount: float, match_id: str, mediator_name: str):
    """
    Cria um embed Discord com informações de pagamento Pix.
    
    Args:
        amount: Valor em reais
        match_id: ID da partida
        mediator_name: Nome do mediador
    
    Returns:
        Dicionário com dados do embed
    """
    
    import discord
    
    embed = discord.Embed(
        title="💰 Pagamento Pix",
        description=f"Escaneie o QR Code abaixo para confirmar o pagamento",
        color=discord.Color.green()
    )
    
    embed.add_field(
        name="💵 Valor",
        value=f"R$ {amount:.2f}",
        inline=True
    )
    
    embed.add_field(
        name="🎮 ID da Sala",
        value=match_id,
        inline=True
    )
    
    embed.add_field(
        name="👤 Mediador",
        value=mediator_name,
        inline=True
    )
    
    embed.add_field(
        name="🔑 Chave Pix",
        value=f"`{PIX_KEY}`",
        inline=False
    )
    
    embed.set_footer(text="🐿️ Esquilo Aposta")
    embed.timestamp = datetime.utcnow()
    
    return embed
