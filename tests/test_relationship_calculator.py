"""
Testy jednostkowe dla RelationshipCalculator
"""

import unittest
import os
import tempfile
from src.database.db_manager import DatabaseManager
from src.business_logic.relationship_calculator import RelationshipCalculator


class TestRelationshipCalculator(unittest.TestCase):
    """Testy dla klasy RelationshipCalculator"""
    
    def setUp(self):
        """Przygotowanie przed każdym testem"""
        # Utwórz tymczasowy plik bazy danych
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        self.db_manager = DatabaseManager(self.temp_db.name)
        self.calc = RelationshipCalculator(self.db_manager)
        
        # Utwórz przykładowe dane
        self.grandparent_id = self.db_manager.add_person('Jan', 'Kowalski', '1940-01-01', None, 'M')
        self.parent_id = self.db_manager.add_person('Anna', 'Kowalska', '1965-01-01', None, 'K')
        self.child_id = self.db_manager.add_person('Piotr', 'Nowak', '1990-01-01', None, 'M')
        
        self.db_manager.add_relation(self.grandparent_id, self.parent_id, 'rodzic')
        self.db_manager.add_relation(self.parent_id, self.child_id, 'rodzic')
    
    def tearDown(self):
        """Sprzątanie po każdym teście"""
        self.db_manager.close()
        if os.path.exists(self.temp_db.name):
            os.unlink(self.temp_db.name)
    
    def test_get_parents(self):
        """Test pobierania rodziców"""
        parents = self.calc.get_parents(self.child_id)
        self.assertEqual(len(parents), 1)
        self.assertEqual(parents[0]['id'], self.parent_id)
    
    def test_get_children(self):
        """Test pobierania dzieci"""
        children = self.calc.get_children(self.parent_id)
        self.assertEqual(len(children), 1)
        self.assertEqual(children[0]['id'], self.child_id)
    
    def test_get_ancestors(self):
        """Test pobierania przodków"""
        ancestors = self.calc.get_ancestors(self.child_id, max_generations=5)
        
        # Powinniśmy mieć 2 przodków: rodzica i dziadka
        self.assertEqual(len(ancestors), 2)
        
        # Sprawdź czy są we właściwych pokoleniach
        ancestor_ids = [a[0]['id'] for a in ancestors]
        self.assertIn(self.parent_id, ancestor_ids)
        self.assertIn(self.grandparent_id, ancestor_ids)
    
    def test_get_descendants(self):
        """Test pobierania potomków"""
        descendants = self.calc.get_descendants(self.grandparent_id, max_generations=5)
        
        # Powinniśmy mieć 2 potomków: dziecko i wnuka
        self.assertEqual(len(descendants), 2)
        
        # Sprawdź czy są we właściwych pokoleniach
        descendant_ids = [d[0]['id'] for d in descendants]
        self.assertIn(self.parent_id, descendant_ids)
        self.assertIn(self.child_id, descendant_ids)
    
    def test_find_relationship_path(self):
        """Test znajdowania ścieżki relacji"""
        path = self.calc.find_relationship_path(self.grandparent_id, self.child_id)
        
        self.assertIsNotNone(path)
        self.assertEqual(len(path), 3)
        self.assertEqual(path[0]['id'], self.grandparent_id)
        self.assertEqual(path[1]['id'], self.parent_id)
        self.assertEqual(path[2]['id'], self.child_id)


if __name__ == '__main__':
    unittest.main()
