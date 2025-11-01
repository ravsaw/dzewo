# Drzewo Genealogiczne

Aplikacja desktopowa do zarządzania drzewem genealogicznym, która umożliwia użytkownikom dodawanie osób, definiowanie relacji rodzinnych oraz wizualizację drzewa genealogicznego.

## Opis projektu

Drzewo Genealogiczne to kompleksowa aplikacja pozwalająca na:
- Zarządzanie danymi osobowymi członków rodziny
- Definiowanie relacji rodzinnych (rodzice, dzieci, małżonkowie)
- Wizualizację drzewa przodków i potomków
- Wyświetlanie osi czasu życia osób
- Import i eksport danych w formacie GEDCOM

## Technologie

- **Python 3.10+** - język programowania
- **PyQt6** - framework GUI
- **SQLite** - baza danych
- **matplotlib** - wizualizacje i wykresy
- **Pillow** - obsługa zdjęć

## Struktura projektu

```
dzewo/
├── src/                          # Kod źródłowy aplikacji
│   ├── database/                 # Warstwa bazy danych
│   │   └── db_manager.py         # Manager bazy danych
│   ├── models/                   # Modele danych
│   │   ├── person.py             # Model osoby
│   │   └── relation.py           # Model relacji
│   ├── business_logic/           # Logika biznesowa
│   │   └── relationship_calculator.py  # Kalkulator relacji
│   ├── gui/                      # Interfejs użytkownika
│   │   ├── main_window.py        # Główne okno
│   │   ├── person_dialog.py      # Dialog osoby
│   │   ├── person_list_widget.py # Lista osób
│   │   ├── relation_dialog.py    # Dialog relacji
│   │   ├── person_selector_dialog.py  # Wybór osoby
│   │   ├── ancestor_tree_widget.py    # Drzewo przodków
│   │   ├── descendant_tree_widget.py  # Drzewo potomków
│   │   └── timeline_widget.py    # Oś czasu
│   └── utils/                    # Narzędzia pomocnicze
│       └── gedcom_handler.py     # Obsługa GEDCOM
├── tests/                        # Testy jednostkowe
├── data/                         # Dane aplikacji
│   ├── family_tree.db           # Baza danych (generowana)
│   └── photos/                  # Zdjęcia osób
├── docs/                         # Dokumentacja
├── main.py                       # Punkt wejścia aplikacji
├── requirements.txt              # Zależności
└── README.md                     # Ten plik

```

## Instalacja

### Wymagania wstępne

- Python 3.10 lub nowszy
- pip (menedżer pakietów Python)

### Kroki instalacji

1. Sklonuj repozytorium na lokalny dysk:
```bash
git clone https://github.com/ravsaw/dzewo.git
cd dzewo
```

2. (Opcjonalnie) Utwórz wirtualne środowisko Python:
```bash
python -m venv venv
source venv/bin/activate  # Na Windows: venv\Scripts\activate
```

3. Zainstaluj wymagane biblioteki:
```bash
pip install -r requirements.txt
```

## Jak uruchomić

Uruchom aplikację za pomocą polecenia:

```bash
python main.py
```

Przy pierwszym uruchomieniu aplikacja automatycznie utworzy:
- Katalog `data/` do przechowywania bazy danych
- Katalog `data/photos/` do przechowywania zdjęć
- Plik bazy danych `data/family_tree.db`

## Funkcjonalności

### 1. Zarządzanie osobami

- **Dodawanie nowych osób** - wprowadzanie danych personalnych (imię, nazwisko, nazwisko panieńskie, daty, miejsca, notatki)
- **Wybór rodziców** - opcjonalne dodawanie rodziców przy tworzeniu nowej osoby
- **Edycja danych** - aktualizacja informacji o osobach
- **Usuwanie osób** - usuwanie wraz z relacjami
- **Wyszukiwanie** - szybkie znajdowanie osób po imieniu lub nazwisku
- **Zdjęcia** - możliwość dodawania zdjęć do profili osób

### 2. Zarządzanie relacjami

- **Rodzice** - definiowanie relacji rodzic-dziecko
- **Dzieci** - automatyczne tworzenie relacji dwukierunkowych
- **Małżonkowie** - określanie związków małżeńskich
- **Usuwanie relacji** - zarządzanie istniejącymi relacjami
- **Automatyczne relacje** - przy dodawaniu osoby można od razu wybrać rodziców

### 3. Wizualizacje

#### Drzewo przodków
- Graficzna reprezentacja przodków wybranej osoby
- Wyświetlanie do 5 pokoleń wstecz
- Kodowanie kolorami według płci

#### Drzewo potomków
- Graficzna reprezentacja potomków wybranej osoby
- Wyświetlanie do 5 pokoleń w przód
- Kodowanie kolorami według płci

#### Pełne drzewo (NOWOŚĆ!)
- Graficzna reprezentacja wszystkich osób i relacji w bazie danych
- Wyświetlanie całej rodziny w jednym widoku
- Pokazuje relacje rodzic-dziecko i małżeńskie
- Kodowanie kolorami według płci
- Wyświetlanie nazwisk panieńskich

#### Oś czasu
- Chronologiczne przedstawienie życia wszystkich osób
- Wizualizacja dat urodzenia i śmierci
- Sortowanie według dat urodzenia

### 4. Import/Eksport GEDCOM

- **Import** - wczytywanie danych z plików GEDCOM
- **Eksport** - zapisywanie danych do standardu GEDCOM
- Zgodność z formatem GEDCOM 5.5.1
- Wsparcie dla nazwisk panieńskich (tag _MARNM)

## Użytkowanie

### Dodawanie osoby

1. Kliknij przycisk "Dodaj" lub wybierz menu Osoby → Dodaj osobę
2. Wypełnij formularz z danymi osoby
3. (Opcjonalnie) Dodaj zdjęcie
4. Kliknij "Zapisz"

### Definiowanie relacji

1. Wybierz osobę z listy
2. Kliknij "Zarządzaj relacjami"
3. Użyj przycisków "Dodaj rodzica", "Dodaj dziecko" lub "Dodaj małżonka"
4. Wybierz odpowiednią osobę z listy
5. Relacja zostanie automatycznie zapisana

### Przeglądanie drzew genealogicznych

1. Wybierz osobę z listy
2. Przejdź do zakładki "Drzewo Przodków" lub "Drzewo Potomków"
3. Drzewo zostanie automatycznie wygenerowane

### Import danych GEDCOM

1. Wybierz menu Plik → Importuj GEDCOM
2. Wybierz plik .ged
3. Dane zostaną zaimportowane do bazy

### Eksport danych GEDCOM

1. Wybierz menu Plik → Eksportuj GEDCOM
2. Podaj nazwę pliku
3. Dane zostaną wyeksportowane

## Przykładowe dane testowe

Aplikacja może być przetestowana z następującymi danymi:

**Osoby:**
- Anna Kowalska (ur. 1950)
- Jan Nowak (ur. 1948)
- Maria Nowak (ur. 1975)
- Piotr Nowak (ur. 1977)

**Relacje:**
- Anna Kowalska - Jan Nowak (małżeństwo)
- Jan Nowak - Maria Nowak (rodzic-dziecko)
- Jan Nowak - Piotr Nowak (rodzic-dziecko)

## Rozwój i testowanie

### Uruchamianie testów

```bash
# Uruchomienie wszystkich testów
python -m pytest tests/

# Uruchomienie z pokryciem kodu
python -m pytest tests/ --cov=src
```

### Standardy kodu

Projekt przestrzega standardu PEP 8. Sprawdzenie stylu kodu:

```bash
flake8 src/
```

## Znane ograniczenia

- Wydajność może się pogorszyć przy bardzo dużej liczbie osób (>10000)
- Import GEDCOM obsługuje podstawowe funkcje (pełna implementacja w przyszłych wersjach)
- Brak wsparcia dla wielu języków (tylko polski)

## Przyszłe rozszerzenia

- Wsparcie dla wielu formatów genealogicznych (Family Tree Maker, Legacy)
- Integracja z zewnętrznymi bazami danych genealogicznymi
- Export do PDF i innych formatów raportów
- Zaawansowana wizualizacja z możliwością edycji
- Synchronizacja w chmurze
- Aplikacja mobilna

## Wkład do projektu

Projekt jest otwarty na współpracę. Jeśli chcesz pomóc w rozwoju:

1. Sforkuj repozytorium
2. Utwórz branch dla swojej funkcjonalności (`git checkout -b feature/AmazingFeature`)
3. Commituj zmiany (`git commit -m 'Add some AmazingFeature'`)
4. Push do brancha (`git push origin feature/AmazingFeature`)
5. Otwórz Pull Request

## Licencja

Ten projekt jest dostępny na licencji MIT.

## Kontakt

W razie pytań lub problemów, otwórz issue na GitHubie.

## Autorzy

- Zespół deweloperski Drzewo Genealogiczne

---

**Wersja:** 1.1.0  
**Data ostatniej aktualizacji:** 2025-11-01

## Nowe w wersji 1.1.0

- ✨ **Nazwisko panieńskie** - możliwość dodania nazwiska przed ślubem
- 🌳 **Pełne drzewo genealogiczne** - wizualizacja wszystkich osób i relacji w jednym widoku
- 👨‍👩‍👧 **Wybór rodziców przy dodawaniu osoby** - szybsze tworzenie drzewa genealogicznego
- 🔄 **Automatyczna migracja bazy danych** - bezproblemowa aktualizacja istniejących baz

Zobacz [CHANGELOG.md](CHANGELOG.md) dla pełnej listy zmian.
