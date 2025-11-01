#!/usr/bin/env python3
"""
Verification script - checks all implemented components
"""

import sys
import os

print("=" * 60)
print("VERIFICATION: Drzewo Genealogiczne Application")
print("=" * 60)
print()

# Test 1: Module imports
print("✓ Testing module imports...")
try:
    from src.database.db_manager import DatabaseManager
    from src.models.person import Person
    from src.models.relation import Relation
    from src.business_logic.relationship_calculator import RelationshipCalculator
    from src.utils.gedcom_handler import GedcomHandler
    print("  ✅ All core modules import successfully")
except ImportError as e:
    print(f"  ❌ Import error: {e}")
    sys.exit(1)

# Test 2: Database operations
print("✓ Testing database operations...")
try:
    import tempfile
    temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
    temp_db.close()
    
    db = DatabaseManager(temp_db.name)
    
    # Add person
    person_id = db.add_person('Test', 'Person', '1990-01-01', None, 'M')
    assert person_id > 0, "Person ID should be positive"
    
    # Get person
    person = db.get_person(person_id)
    assert person['imie'] == 'Test', "Person name should match"
    
    # Search
    results = db.search_persons('Test')
    assert len(results) == 1, "Should find one person"
    
    # Relations
    person2_id = db.add_person('Test2', 'Person2', '2020-01-01', None, 'K')
    rel_id = db.add_relation(person_id, person2_id, 'rodzic')
    assert rel_id > 0, "Relation ID should be positive"
    
    db.close()
    os.unlink(temp_db.name)
    
    print("  ✅ Database operations working correctly")
except Exception as e:
    print(f"  ❌ Database error: {e}")
    sys.exit(1)

# Test 3: Models
print("✓ Testing data models...")
try:
    person = Person(
        id=1, 
        imie='Jan', 
        nazwisko='Kowalski',
        data_urodzenia='1950-01-01',
        plec='M'
    )
    
    assert person.get_full_name() == 'Jan Kowalski'
    assert person.get_birth_year() == 1950
    assert person.is_alive() == True
    
    person_dict = person.to_dict()
    person2 = Person.from_dict(person_dict)
    assert person2.imie == person.imie
    
    print("  ✅ Data models working correctly")
except Exception as e:
    print(f"  ❌ Model error: {e}")
    sys.exit(1)

# Test 4: Relationship calculator
print("✓ Testing relationship calculator...")
try:
    temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
    temp_db.close()
    
    db = DatabaseManager(temp_db.name)
    calc = RelationshipCalculator(db)
    
    parent_id = db.add_person('Parent', 'Test', '1960-01-01', None, 'M')
    child_id = db.add_person('Child', 'Test', '1990-01-01', None, 'K')
    db.add_relation(parent_id, child_id, 'rodzic')
    
    children = calc.get_children(parent_id)
    assert len(children) == 1, "Should have one child"
    
    parents = calc.get_parents(child_id)
    assert len(parents) == 1, "Should have one parent"
    
    path = calc.find_relationship_path(parent_id, child_id)
    assert len(path) == 2, "Path should have 2 persons"
    
    db.close()
    os.unlink(temp_db.name)
    
    print("  ✅ Relationship calculator working correctly")
except Exception as e:
    print(f"  ❌ Calculator error: {e}")
    sys.exit(1)

# Test 5: Unit tests
print("✓ Running unit tests...")
try:
    import unittest
    loader = unittest.TestLoader()
    suite = loader.discover('tests', pattern='test_*.py')
    runner = unittest.TextTestRunner(verbosity=0)
    result = runner.run(suite)
    
    if result.wasSuccessful():
        print(f"  ✅ All {result.testsRun} unit tests passed")
    else:
        print(f"  ❌ Some tests failed: {len(result.failures)} failures, {len(result.errors)} errors")
        sys.exit(1)
except Exception as e:
    print(f"  ❌ Test error: {e}")
    sys.exit(1)

# Summary
print()
print("=" * 60)
print("✅ ALL VERIFICATION CHECKS PASSED")
print("=" * 60)
print()
print("Application is ready for use!")
print()
print("Next steps:")
print("  1. Run: python main.py")
print("  2. Or add sample data: python create_sample_data.py")
print()

