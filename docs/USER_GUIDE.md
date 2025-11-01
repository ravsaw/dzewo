# Przewodnik użytkownika - Drzewo Genealogiczne

## Rozpoczęcie pracy

### 1. Pierwsze uruchomienie

Po zainstalowaniu aplikacji (patrz README.md), uruchom ją poleceniem:

```bash
python main.py
```

Przy pierwszym uruchomieniu aplikacja automatycznie:
- Utworzy katalog `data/` 
- Utworzy pustą bazę danych `data/family_tree.db`
- Utworzy katalog `data/photos/` na zdjęcia

### 2. Dodawanie przykładowych danych

Aby przetestować aplikację z przykładowymi danymi, uruchom:

```bash
python create_sample_data.py
```

To doda przykładową rodzinę obejmującą 4 pokolenia (dziadkowie, rodzice, dzieci, wnuki).

## Praca z osobami

### Dodawanie nowej osoby

1. Kliknij przycisk **"Dodaj"** na pasku narzędzi lub wybierz menu **Osoby → Dodaj osobę**
2. Wypełnij formularz:
   - **Imię*** - wymagane
   - **Nazwisko*** - wymagane
   - **Płeć** - opcjonalne (M/K)
   - **Data urodzenia** - zaznacz "Znana" i wybierz datę
   - **Status** - wybierz "Żyje" lub "Zmarła"
   - **Data śmierci** - dostępna jeśli status to "Zmarła"
   - **Miejsce urodzenia/śmierci** - opcjonalne
   - **Zdjęcie** - kliknij "Wybierz zdjęcie" aby dodać fotografię
   - **Notatki** - dowolne informacje tekstowe
3. Kliknij **"Zapisz"**

### Edycja osoby

**Opcja 1:** Dwukrotnie kliknij na osobę w liście

**Opcja 2:** 
1. Wybierz osobę z listy (pojedyncze kliknięcie)
2. Kliknij przycisk **"Edytuj"** lub wybierz menu **Osoby → Edytuj osobę**

### Usuwanie osoby

1. Wybierz osobę z listy
2. Kliknij przycisk **"Usuń"** lub naciśnij klawisz **Delete**
3. Potwierdź operację

⚠️ **Uwaga:** Usunięcie osoby spowoduje również usunięcie wszystkich jej relacji.

### Wyszukiwanie osób

1. W zakładce **"Lista Osób"** znajdź pole "Szukaj:" u góry
2. Wpisz imię lub nazwisko
3. Lista zostanie automatycznie przefiltrowana

## Zarządzanie relacjami

### Dodawanie relacji

1. Wybierz osobę z listy
2. Kliknij przycisk **"Zarządzaj relacjami"**
3. W oknie relacji wybierz typ relacji do dodania:
   - **Dodaj rodzica** - wybierz osobę, która jest rodzicem
   - **Dodaj dziecko** - wybierz osobę, która jest dzieckiem
   - **Dodaj małżonka** - wybierz małżonka/małżonkę
4. Z listy wybierz odpowiednią osobę
5. Relacja zostanie automatycznie zapisana

### Typy relacji

- **Rodzic** - relacja rodzic-dziecko (automatycznie tworzona dwukierunkowo)
- **Dziecko** - odwrotność relacji rodzic
- **Małżonek** - związek małżeński (relacja symetryczna)

### Usuwanie relacji

1. W oknie **"Zarządzaj relacjami"** wybierz relację do usunięcia
2. Kliknij **"Usuń relację"**
3. Potwierdź operację

## Wizualizacje

### Drzewo przodków

1. Wybierz osobę z listy w zakładce **"Lista Osób"**
2. Przejdź do zakładki **"Drzewo Przodków"**
3. Zobaczysz graficzną reprezentację przodków do 5 pokoleń wstecz

**Legenda kolorów:**
- 🔵 Niebieski - mężczyźni
- 🔴 Różowy - kobiety
- ⚪ Szary - płeć nieokreślona

### Drzewo potomków

1. Wybierz osobę z listy
2. Przejdź do zakładki **"Drzewo Potomków"**
3. Zobaczysz graficzną reprezentację potomków do 5 pokoleń w przód

### Oś czasu

1. Przejdź do zakładki **"Oś Czasu"**
2. Zobaczysz chronologiczną wizualizację życia wszystkich osób w bazie
3. Pasek pokazuje lata życia każdej osoby
4. Oś czasu jest posortowana według daty urodzenia

## Import i eksport danych

### Import z pliku GEDCOM

1. Wybierz menu **Plik → Importuj GEDCOM**
2. Wybierz plik `.ged` z dysku
3. Dane zostaną zaimportowane do bazy

⚠️ **Uwaga:** Import GEDCOM jest obecnie w wersji podstawowej i obsługuje:
- Podstawowe dane osobowe (imię, nazwisko, daty, płeć)
- Relacje rodzinne

### Eksport do pliku GEDCOM

1. Wybierz menu **Plik → Eksportuj GEDCOM**
2. Podaj nazwę pliku do zapisania
3. Wszystkie dane zostaną wyeksportowane w formacie GEDCOM 5.5.1

Wyeksportowany plik można otworzyć w innych programach genealogicznych.

## Skróty klawiaturowe

- **Ctrl+N** - Dodaj nową osobę
- **Ctrl+E** - Edytuj wybraną osobę
- **Delete** - Usuń wybraną osobę
- **Ctrl+Q** - Wyjdź z aplikacji

## Wskazówki

### Organizacja danych

1. **Rozpocznij od najstarszego pokolenia** - dodaj najpierw przodków, następnie potomków
2. **Dodawaj relacje małżeńskie** przed dodaniem dzieci
3. **Używaj dat** - ułatwia to sortowanie i wizualizację na osi czasu
4. **Dodawaj zdjęcia** - sprawiają, że drzewo jest bardziej osobiste

### Wydajność

- Aplikacja działa sprawnie z setkami osób
- Dla bardzo dużych drzew (>1000 osób) wizualizacje mogą być mniej czytelne
- Używaj funkcji wyszukiwania dla szybkiego odnalezienia osób

### Backup danych

**Ważne:** Regularnie twórz kopie zapasowe bazy danych!

Kopia zapasowa to prosty plik:
```bash
cp data/family_tree.db data/family_tree_backup_$(date +%Y%m%d).db
```

Lub użyj eksportu GEDCOM jako formy backupu.

## Rozwiązywanie problemów

### Aplikacja nie uruchamia się

1. Sprawdź czy zainstalowano wszystkie zależności: `pip install -r requirements.txt`
2. Sprawdź wersję Pythona: `python --version` (wymagane 3.10+)

### Nie widzę drzew przodków/potomków

1. Upewnij się, że wybrano osobę z listy
2. Sprawdź czy dodano relacje rodzinne dla tej osoby

### Import GEDCOM nie działa

1. Upewnij się, że plik jest w formacie GEDCOM (.ged)
2. Sprawdź czy plik nie jest uszkodzony
3. Import obsługuje podstawowe funkcje - niektóre zaawansowane dane mogą nie zostać zaimportowane

## Pomoc

W razie problemów:
1. Sprawdź dokumentację w katalogu `docs/`
2. Otwórz issue na GitHubie
3. Sprawdź logi błędów w konsoli

---

**Miłego używania aplikacji Drzewo Genealogiczne!** 🌳
