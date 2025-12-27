"""
Testes básicos para o Bot Esquilo Aposta
"""

import unittest
from unittest.mock import Mock, patch
from pix_utils import generate_room_id, generate_room_password, mount_pix_string, calculate_crc16
from utils import generate_room_id as util_room_id, generate_room_password as util_password
from config import BET_VALUES, MODALITIES

class TestPixUtils(unittest.TestCase):
    """Testes para utilitários de Pix"""
    
    def test_generate_room_id(self):
        """Testa geração de ID de sala"""
        room_id = generate_room_id()
        self.assertEqual(len(room_id), 6)
        self.assertTrue(room_id.isupper() or room_id.isdigit())
    
    def test_generate_room_password(self):
        """Testa geração de senha de sala"""
        password = generate_room_password()
        self.assertEqual(len(password), 4)
        self.assertTrue(password.isdigit())
    
    def test_mount_pix_string(self):
        """Testa montagem da string Pix"""
        pix_string = mount_pix_string(
            pix_key="test@email.com",
            amount=10.00,
            description="Teste",
            merchant_name="Test Merchant",
            merchant_city="Sao Paulo"
        )
        
        self.assertIsInstance(pix_string, str)
        self.assertIn("br.gov.bcb.pix", pix_string)
    
    def test_calculate_crc16(self):
        """Testa cálculo de CRC16"""
        data = "00020126360014br.gov.bcb.pix"
        crc = calculate_crc16(data)
        
        self.assertIsInstance(crc, int)
        self.assertGreaterEqual(crc, 0)
        self.assertLess(crc, 65536)  # CRC16 é 16 bits


class TestConfig(unittest.TestCase):
    """Testes para configurações"""
    
    def test_bet_values(self):
        """Testa valores de aposta"""
        self.assertIsInstance(BET_VALUES, list)
        self.assertGreater(len(BET_VALUES), 0)
        
        # Verificar se está em ordem crescente
        for i in range(len(BET_VALUES) - 1):
            self.assertLess(BET_VALUES[i], BET_VALUES[i + 1])
    
    def test_modalities(self):
        """Testa modalidades"""
        self.assertIsInstance(MODALITIES, dict)
        
        expected_modalities = ['Mobile', 'Emulador', 'Misto']
        for modality in expected_modalities:
            self.assertIn(modality, MODALITIES)
            self.assertIn('modes', MODALITIES[modality])
            self.assertIn('enabled', MODALITIES[modality])
    
    def test_modality_modes(self):
        """Testa modos de cada modalidade"""
        # Mobile e Emulador devem ter 1v1, 2v2, 3v3, 4v4
        for modality in ['Mobile', 'Emulador']:
            modes = MODALITIES[modality]['modes']
            self.assertIn('1v1', modes)
            self.assertIn('2v2', modes)
            self.assertIn('3v3', modes)
            self.assertIn('4v4', modes)
        
        # Misto deve ter 2v2, 3v3, 4v4 (sem 1v1)
        misto_modes = MODALITIES['Misto']['modes']
        self.assertNotIn('1v1', misto_modes)
        self.assertIn('2v2', misto_modes)
        self.assertIn('3v3', misto_modes)
        self.assertIn('4v4', misto_modes)


class TestUtils(unittest.TestCase):
    """Testes para utilitários gerais"""
    
    def test_util_room_id(self):
        """Testa geração de ID de sala em utils"""
        room_id = util_room_id()
        self.assertEqual(len(room_id), 6)
    
    def test_util_password(self):
        """Testa geração de senha em utils"""
        password = util_password()
        self.assertEqual(len(password), 4)
        self.assertTrue(password.isdigit())
    
    def test_unique_room_ids(self):
        """Testa se IDs de sala são únicos"""
        ids = set()
        for _ in range(100):
            room_id = generate_room_id()
            ids.add(room_id)
        
        # Deve ter pelo menos 95 IDs únicos em 100 tentativas
        self.assertGreater(len(ids), 95)


class TestModels(unittest.TestCase):
    """Testes para modelos do banco de dados"""
    
    def test_models_import(self):
        """Testa se os modelos podem ser importados"""
        try:
            from models import (
                Base, Guild, User, Match, MatchParticipant,
                Modality, Mode, Log, BetValue
            )
            self.assertIsNotNone(Base)
        except ImportError as e:
            self.fail(f"Erro ao importar modelos: {e}")


def run_tests():
    """Executa todos os testes"""
    unittest.main(argv=[''], exit=False, verbosity=2)


if __name__ == '__main__':
    run_tests()
