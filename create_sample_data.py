#!/usr/bin/env python3
"""
Przykładowy skrypt demonstracyjny - dodaje przykładowe dane do bazy
"""

import os
from src.database.db_manager import DatabaseManager
from src.business_logic.relationship_calculator import RelationshipCalculator


def create_sample_data():
    """Tworzy przykładowe dane w bazie"""
    
    # Ścieżka do bazy danych
    db_path = os.path.join('data', 'family_tree.db')
    
    # Tworzenie katalogu jeśli nie istnieje
    os.makedirs('data', exist_ok=True)
    
    # Inicjalizacja bazy danych
    db = DatabaseManager(db_path)
    
    print("=== Tworzenie przykładowych danych ===\n")
    
    # Sprawdź czy baza już zawiera dane
    existing_persons = db.get_all_persons()
    if existing_persons:
        print(f"Baza danych już zawiera {len(existing_persons)} osób.")
        response = input("Czy chcesz dodać więcej przykładowych danych? (t/n): ")
        if response.lower() != 't':
            db.close()
            return
    
    # Dodawanie osób - starsze pokolenie (dziadkowie)
    print("Dodawanie dziadków...")
    jan_kowalski_id = db.add_person(
        'Jan', 'Kowalski', '1940-05-15', '2015-12-20', 'M',
        'Warszawa', 'Warszawa', 'Dziadek ze strony ojca'
    )
    
    maria_kowalska_id = db.add_person(
        'Maria', 'Kowalska', '1942-08-10', None, 'K',
        'Kraków', None, 'Babcia ze strony ojca'
    )
    
    # Dodawanie rodziców
    print("Dodawanie rodziców...")
    anna_nowak_id = db.add_person(
        'Anna', 'Kowalska', '1950-03-20', None, 'K',
        'Kraków', None, 'Matka'
    )
    
    piotr_nowak_id = db.add_person(
        'Piotr', 'Nowak', '1948-12-01', None, 'M',
        'Gdańsk', None, 'Ojciec'
    )
    
    # Dodawanie dzieci
    print("Dodawanie dzieci...")
    maria_nowak_id = db.add_person(
        'Maria', 'Nowak', '1975-08-10', None, 'K',
        'Warszawa', None, 'Córka'
    )
    
    tomasz_nowak_id = db.add_person(
        'Tomasz', 'Nowak', '1977-12-25', None, 'M',
        'Warszawa', None, 'Syn'
    )
    
    # Dodawanie wnuków
    print("Dodawanie wnuków...")
    kasia_kowalska_id = db.add_person(
        'Katarzyna', 'Kowalska', '2000-06-15', None, 'K',
        'Warszawa', None, 'Wnuczka'
    )
    
    jakub_kowalski_id = db.add_person(
        'Jakub', 'Kowalski', '2002-09-03', None, 'M',
        'Warszawa', None, 'Wnuk'
    )
    
    # Dodawanie relacji małżeńskich
    print("\nDodawanie relacji małżeńskich...")
    db.add_relation(jan_kowalski_id, maria_kowalska_id, 'małżonek')
    db.add_relation(piotr_nowak_id, anna_nowak_id, 'małżonek')
    
    # Dodawanie relacji rodzic-dziecko (pierwsze pokolenie -> drugie)
    print("Dodawanie relacji rodzic-dziecko...")
    db.add_relation(jan_kowalski_id, piotr_nowak_id, 'rodzic')
    db.add_relation(maria_kowalska_id, piotr_nowak_id, 'rodzic')
    
    # Relacje rodzic-dziecko (drugie -> trzecie pokolenie)
    db.add_relation(piotr_nowak_id, maria_nowak_id, 'rodzic')
    db.add_relation(anna_nowak_id, maria_nowak_id, 'rodzic')
    db.add_relation(piotr_nowak_id, tomasz_nowak_id, 'rodzic')
    db.add_relation(anna_nowak_id, tomasz_nowak_id, 'rodzic')
    
    # Relacje rodzic-dziecko (trzecie -> czwarte pokolenie)
    db.add_relation(maria_nowak_id, kasia_kowalska_id, 'rodzic')
    db.add_relation(maria_nowak_id, jakub_kowalski_id, 'rodzic')
    
    print("\n=== Podsumowanie ===")
    
    # Podsumowanie
    all_persons = db.get_all_persons()
    all_relations = db.get_all_relations()
    
    print(f"\nDodano {len(all_persons)} osób:")
    for person in all_persons:
        status = "żyje" if not person['data_smierci'] else f"zm. {person['data_smierci']}"
        print(f"  - {person['imie']} {person['nazwisko']} (ur. {person['data_urodzenia']}, {status})")
    
    print(f"\nDodano {len(all_relations)} relacji:")
    for rel in all_relations:
        print(f"  - {rel['osoba1_imie']} {rel['osoba1_nazwisko']} ({rel['rodzaj_relacji']}) {rel['osoba2_imie']} {rel['osoba2_nazwisko']}")
    
    # Test kalkulatora relacji
    print("\n=== Test kalkulatora relacji ===")
    calc = RelationshipCalculator(db)
    
    print(f"\nDzieci Piotra Nowaka: {[p['imie'] for p in calc.get_children(piotr_nowak_id)]}")
    print(f"Rodzice Marii Nowak: {[p['imie'] for p in calc.get_parents(maria_nowak_id)]}")
    print(f"Małżonek Piotra Nowaka: {calc.get_spouse(piotr_nowak_id)['imie'] if calc.get_spouse(piotr_nowak_id) else 'brak'}")
    print(f"Rodzeństwo Marii Nowak: {[p['imie'] for p in calc.get_siblings(maria_nowak_id)]}")
    
    ancestors = calc.get_ancestors(kasia_kowalska_id)
    print(f"\nPrzodkowie Katarzyny Kowalskiej ({len(ancestors)} pokoleń):")
    for ancestor, generation in ancestors:
        print(f"  Pokolenie {generation}: {ancestor['imie']} {ancestor['nazwisko']}")
    
    descendants = calc.get_descendants(jan_kowalski_id)
    print(f"\nPotomkowie Jana Kowalskiego ({len(descendants)} pokoleń):")
    for descendant, generation in descendants:
        print(f"  Pokolenie {generation}: {descendant['imie']} {descendant['nazwisko']}")
    
    print("\n✓ Przykładowe dane zostały pomyślnie dodane do bazy!")
    print(f"✓ Baza danych znajduje się w: {db_path}")
    print(f"✓ Uruchom aplikację: python main.py")
    
    # Zamknij połączenie
    db.close()


if __name__ == "__main__":
    create_sample_data()
