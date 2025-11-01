# Dokumentacja Drzewo Genealogiczne

## Architektura aplikacji

### Warstwa danych (Database Layer)
- **DatabaseManager**: Zarządza połączeniem z bazą SQLite i operacjami CRUD

### Warstwa modeli (Models Layer)
- **Person**: Model reprezentujący osobę w drzewie genealogicznym
- **Relation**: Model reprezentujący relację między osobami

### Warstwa logiki biznesowej (Business Logic Layer)
- **RelationshipCalculator**: Oblicza relacje między osobami (przodkowie, potomkowie, ścieżki)

### Warstwa prezentacji (Presentation Layer)
- **MainWindow**: Główne okno aplikacji z menu, paskiem narzędzi i zakładkami
- **PersonListWidget**: Widget do wyświetlania i zarządzania listą osób
- **PersonDialog**: Dialog do dodawania/edycji danych osoby
- **RelationDialog**: Dialog do zarządzania relacjami osoby
- **PersonSelectorDialog**: Dialog do wyboru osoby z listy
- **AncestorTreeWidget**: Wizualizacja drzewa przodków
- **DescendantTreeWidget**: Wizualizacja drzewa potomków
- **TimelineWidget**: Wizualizacja osi czasu życia osób

### Warstwa narzędzi (Utils Layer)
- **GedcomHandler**: Import i eksport danych w formacie GEDCOM

## Schemat bazy danych

### Tabela `osoby`
```sql
CREATE TABLE osoby (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    imie TEXT NOT NULL,
    nazwisko TEXT NOT NULL,
    data_urodzenia DATE,
    data_smierci DATE,
    plec TEXT,
    miejsce_urodzenia TEXT,
    miejsce_smierci TEXT,
    notatki TEXT,
    zdjecie_sciezka TEXT
)
```

### Tabela `relacje`
```sql
CREATE TABLE relacje (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    osoba1_id INTEGER NOT NULL,
    osoba2_id INTEGER NOT NULL,
    rodzaj_relacji TEXT NOT NULL,
    FOREIGN KEY (osoba1_id) REFERENCES osoby (id) ON DELETE CASCADE,
    FOREIGN KEY (osoba2_id) REFERENCES osoby (id) ON DELETE CASCADE
)
```

## Rodzaje relacji

- **rodzic**: osoba1_id jest rodzicem osoby osoba2_id
- **dziecko**: osoba1_id jest dzieckiem osoby osoba2_id (odwrotność rodzica)
- **małżonek**: osoba1_id i osoba2_id są małżonkami (relacja symetryczna)

## Przepływ danych

1. Użytkownik wprowadza dane przez interfejs GUI
2. GUI wywołuje metody DatabaseManager
3. DatabaseManager wykonuje operacje na bazie SQLite
4. RelationshipCalculator analizuje dane i oblicza relacje
5. Widgety wizualizacyjne rysują drzewa i wykresy używając matplotlib

## API głównych klas

### DatabaseManager
```python
add_person(imie, nazwisko, ...) -> int
update_person(person_id, imie, nazwisko, ...)
delete_person(person_id)
get_person(person_id) -> dict
get_all_persons() -> List[dict]
search_persons(query) -> List[dict]
add_relation(osoba1_id, osoba2_id, rodzaj_relacji) -> int
delete_relation(relation_id)
get_relations(person_id) -> List[dict]
```

### RelationshipCalculator
```python
get_parents(person_id) -> List[dict]
get_children(person_id) -> List[dict]
get_spouse(person_id) -> Optional[dict]
get_siblings(person_id) -> List[dict]
get_ancestors(person_id, max_generations) -> List[Tuple[dict, int]]
get_descendants(person_id, max_generations) -> List[Tuple[dict, int]]
find_relationship_path(person1_id, person2_id) -> Optional[List[dict]]
calculate_relation_degree(person1_id, person2_id) -> Optional[str]
```

## Konfiguracja matplotlib

- Używamy backendu Qt5Agg dla integracji z PyQt6
- Wykresy są osadzone w widgetach QScrollArea
- Kodowanie kolorami: niebieski (M), różowy (K), szary (nieokreślone)

## Testowanie

Testy jednostkowe znajdują się w katalogu `tests/`:
- `test_database.py`: Testy DatabaseManager
- `test_relationship_calculator.py`: Testy RelationshipCalculator

Uruchomienie testów:
```bash
python -m unittest discover tests/
```
