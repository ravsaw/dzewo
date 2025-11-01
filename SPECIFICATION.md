# SPECYFIKACJA APLIKACJI

## Opis projektu
Aplikacja desktopowa do budowy drzewa genealogicznego, która umożliwia użytkownikom zarządzanie danymi o osobach oraz ich relacjach.

## Stos technologiczny
- Python 3.10+
- PyQt6
- SQLite
- matplotlib
- Pillow

## Szczegółowa struktura projektu
- /src - kod źródłowy aplikacji
- /tests - testy jednostkowe
- /data - przykładowe dane
- /docs - dokumentacja

## Schemat bazy danych
### Tabela osób
- id: INTEGER PRIMARY KEY
- imię: TEXT
- nazwisko: TEXT
- data_urodzenia: DATE

### Tabela relacji
- id: INTEGER PRIMARY KEY
- osoba1_id: INTEGER
- osoba2_id: INTEGER
- rodzaj_relacji: TEXT

## Szczegółowe specyfikacje modułów
### DatabaseManager
Zarządza połączeniem z bazą danych i operacjami CRUD.

### Models
Definiuje modele danych dla osób i relacji.

### RelationshipCalculator
Oblicza relacje między osobami.

### MainWindow
Główne okno aplikacji.

### PersonDialog
Dialog do edycji danych osoby.

### PersonListWidget
Widget wyświetlający listę osób.

### AncestorTreeWidget
Widget do wyświetlania drzewa przodków.

### DescendantTreeWidget
Widget do wyświetlania drzewa potomków.

### TimelineWidget
Widget do wizualizacji osi czasu.

### GedcomHandler
Obsługuje import i eksport danych w formacie GEDCOM.

## Lista priorytetów funkcji
1. Zarządzanie osobami
2. Wizualizacja relacji
3. Generowanie raportów
4. Import/eksport GEDCOM
5. Wsparcie dla multimediów

## Wymagania dotyczące jakości kodu
- Przestrzeganie zasad PEP 8
- Testy jednostkowe dla wszystkich modułów
- Dokumentacja kodu

## Instrukcje instalacji
1. Skopiuj repozytorium na lokalny dysk.
2. Zainstaluj wymagane biblioteki: `pip install -r requirements.txt`.
3. Uruchom aplikację: `python main.py`.

## Szablon README.md
```markdown
# Nazwa projektu
Opis projektu.

## Technologie
- Python 3.10+
- PyQt6
- SQLite

## Jak uruchomić
Instrukcje uruchomienia aplikacji.

## Wkład
Informacje o wkładzie do projektu.
```

## Przykładowe dane testowe
- Osoby: Anna Kowalska, Jan Nowak
- Relacje: Anna Kowalska - Jan Nowak (małżeństwo)

## Fazy implementacji
1. Faza 1: Podstawa (stworzenie struktury projektu)
2. Faza 2: Implementacja funkcji zarządzania osobami
3. Faza 3: Wizualizacja relacji
4. Faza 4: Integracja z bazą danych
5. Faza 5: Polerowanie i testowanie

## Przypadki testowe
- Sprawdzenie dodawania, edytowania, usuwania osób.
- Weryfikacja poprawności relacji między osobami.

## Znane ograniczenia i przyszłe rozszerzenia
- Ograniczenia w ilości danych do załadowania.
- Możliwość dodania wsparcia dla różnych formatów danych genealogicznych.