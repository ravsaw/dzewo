"""
Testy jednostkowe dla DatabaseManager
"""

import unittest
import os
import tempfile
from src.database.db_manager import DatabaseManager


class TestDatabaseManager(unittest.TestCase):
    """Testy dla klasy DatabaseManager"""
    
    def setUp(self):
        """Przygotowanie przed każdym testem"""
        # Utwórz tymczasowy plik bazy danych
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        self.db_manager = DatabaseManager(self.temp_db.name)
    
    def tearDown(self):
        """Sprzątanie po każdym teście"""
        self.db_manager.close()
        if os.path.exists(self.temp_db.name):
            os.unlink(self.temp_db.name)
    
    def test_add_person(self):
        """Test dodawania osoby"""
        person_id = self.db_manager.add_person(
            'Jan', 'Kowalski', '1990-01-01', None, 'M'
        )
        self.assertIsNotNone(person_id)
        self.assertGreater(person_id, 0)
    
    def test_get_person(self):
        """Test pobierania osoby"""
        person_id = self.db_manager.add_person(
            'Anna', 'Nowak', '1985-05-15', None, 'K'
        )
        person = self.db_manager.get_person(person_id)
        
        self.assertIsNotNone(person)
        self.assertEqual(person['imie'], 'Anna')
        self.assertEqual(person['nazwisko'], 'Nowak')
        self.assertEqual(person['data_urodzenia'], '1985-05-15')
        self.assertEqual(person['plec'], 'K')
    
    def test_update_person(self):
        """Test aktualizacji danych osoby"""
        person_id = self.db_manager.add_person(
            'Piotr', 'Wiśniewski', '2000-12-31', None, 'M'
        )
        
        self.db_manager.update_person(
            person_id, 'Piotr', 'Kowalski', '2000-12-31', None, 'M'
        )
        
        person = self.db_manager.get_person(person_id)
        self.assertEqual(person['nazwisko'], 'Kowalski')
    
    def test_delete_person(self):
        """Test usuwania osoby"""
        person_id = self.db_manager.add_person(
            'Maria', 'Zielińska', '1975-03-20', None, 'K'
        )
        
        self.db_manager.delete_person(person_id)
        person = self.db_manager.get_person(person_id)
        
        self.assertIsNone(person)
    
    def test_get_all_persons(self):
        """Test pobierania wszystkich osób"""
        self.db_manager.add_person('Jan', 'Kowalski', None, None, 'M')
        self.db_manager.add_person('Anna', 'Nowak', None, None, 'K')
        
        persons = self.db_manager.get_all_persons()
        self.assertEqual(len(persons), 2)
    
    def test_add_relation(self):
        """Test dodawania relacji"""
        parent_id = self.db_manager.add_person('Jan', 'Kowalski', '1960-01-01', None, 'M')
        child_id = self.db_manager.add_person('Anna', 'Kowalska', '1990-01-01', None, 'K')
        
        relation_id = self.db_manager.add_relation(parent_id, child_id, 'rodzic')
        
        self.assertIsNotNone(relation_id)
        self.assertGreater(relation_id, 0)
    
    def test_get_relations(self):
        """Test pobierania relacji"""
        parent_id = self.db_manager.add_person('Jan', 'Kowalski', '1960-01-01', None, 'M')
        child_id = self.db_manager.add_person('Anna', 'Kowalska', '1990-01-01', None, 'K')
        
        self.db_manager.add_relation(parent_id, child_id, 'rodzic')
        
        relations = self.db_manager.get_relations(parent_id)
        self.assertEqual(len(relations), 1)
        self.assertEqual(relations[0]['rodzaj_relacji'], 'rodzic')
    
    def test_search_persons(self):
        """Test wyszukiwania osób"""
        self.db_manager.add_person('Jan', 'Kowalski', None, None, 'M')
        self.db_manager.add_person('Anna', 'Kowalska', None, None, 'K')
        self.db_manager.add_person('Piotr', 'Nowak', None, None, 'M')
        
        results = self.db_manager.search_persons('Kowal')
        self.assertEqual(len(results), 2)
        
        results = self.db_manager.search_persons('Nowak')
        self.assertEqual(len(results), 1)


if __name__ == '__main__':
    unittest.main()
