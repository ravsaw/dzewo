# CHANGELOG - Nowe funkcjonalności

## Wersja 1.1.0 - Nowe funkcje genealogiczne

### Dodano nazwisko panieńskie

**Opis:** Dodano pole "nazwisko panieńskie" do danych osoby, które umożliwia przechowywanie informacji o nazwisku przed ślubem.

**Gdzie znajdziesz tę funkcję:**
- W formularzu dodawania/edycji osoby znajduje się nowe pole "Nazwisko panieńskie"
- Pole jest opcjonalne i pojawia się między polem "Nazwisko" a "Płeć"
- Nazwisko panieńskie jest wyświetlane w pełnym drzewie genealogicznym pod nazwiskiem aktualnym

**Przykład użycia:**
- Osoba: Anna Kowalska
- Nazwisko panieńskie: Nowak
- Wyświetlanie: Anna Kowalska (Nowak)

**Szczegóły techniczne:**
- Pole `nazwisko_panienskie` dodane do tabeli `osoby` w bazie danych
- Automatyczna migracja bazy danych - istniejące bazy zostaną zaktualizowane przy pierwszym uruchomieniu
- Wsparcie w eksporcie/imporcie GEDCOM (tag _MARNM)

### Pełne drzewo genealogiczne

**Opis:** Nowa zakładka "Pełne Drzewo" wyświetla wszystkie osoby i relacje w bazie danych w jednym widoku.

**Gdzie znajdziesz tę funkcję:**
- Nowa zakładka "Pełne Drzewo" w głównym oknie aplikacji
- Zakładka znajduje się między "Drzewo Potomków" a "Oś Czasu"

**Co pokazuje:**
- Wszystkie osoby w bazie danych
- Relacje rodzic-dziecko (linie czarne)
- Relacje małżeńskie (linie czerwone przerywane)
- Osoby bez rodziców na górze (osoby startowe)
- Kolejne pokolenia ułożone poziomo od góry do dołu

**Kolory węzłów:**
- Niebieski - mężczyźni (M)
- Różowy - kobiety (K)
- Szary - płeć nieokreślona

**Informacje wyświetlane:**
- Imię i nazwisko osoby
- Nazwisko panieńskie (jeśli jest)
- Rok urodzenia

**Automatyczne odświeżanie:**
- Pełne drzewo jest automatycznie odświeżane po dodaniu/edycji/usunięciu osoby

### Dodawanie rodziców przy tworzeniu osoby

**Opis:** Przy dodawaniu nowej osoby można opcjonalnie od razu wybrać jej rodziców.

**Gdzie znajdziesz tę funkcję:**
- W formularzu dodawania nowej osoby (nie w edycji)
- Pod polem "Notatki" znajdują się dwa nowe pola:
  - "Matka (opcjonalnie)" - lista kobiet z bazy danych
  - "Ojciec (opcjonalnie)" - lista mężczyzn z bazy danych

**Jak to działa:**
1. Wypełnij podstawowe dane nowej osoby
2. Opcjonalnie wybierz matkę z listy (pokazuje tylko osoby z płcią K)
3. Opcjonalnie wybierz ojca z listy (pokazuje tylko osoby z płcią M)
4. Kliknij "Zapisz"
5. Nowa osoba zostanie dodana wraz z automatycznie utworzonymi relacjami rodzic-dziecko

**Lista rodziców:**
- Pokazuje: Imię Nazwisko (Rok urodzenia)
- Automatycznie filtruje po płci
- Domyślna opcja: "Nie wybrano"

**Korzyści:**
- Szybsze tworzenie drzewa genealogicznego
- Mniej kroków - nie trzeba osobno dodawać relacji
- Automatyczne tworzenie dwukierunkowych relacji

### Migracja istniejących baz danych

Aplikacja automatycznie aktualizuje istniejące bazy danych:
- Dodaje kolumnę `nazwisko_panienskie` jeśli nie istnieje
- Istniejące dane nie są modyfikowane
- Proces migracji jest bezpieczny i automatyczny

### Backward Compatibility

Wszystkie nowe funkcje są w pełni zgodne wstecznie:
- Istniejące bazy danych działają bez zmian
- Nazwisko panieńskie jest opcjonalne
- Wybór rodziców jest opcjonalny
- Stare eksporty GEDCOM nadal się importują

### Uwagi dla użytkowników

1. **Nazwisko panieńskie:**
   - To pole jest przeznaczone głównie dla kobiet, ale może być użyte dla każdej osoby
   - Pojawia się w pełnym drzewie genealogicznym w nawiasach
   - Jest eksportowane do GEDCOM jako niestandardowy tag _MARNM

2. **Pełne drzewo:**
   - Przy dużej liczbie osób (>50) drzewo może być trudne do odczytania
   - Używaj przybliżania/oddalania w przeglądarce wykresu
   - Dla szczegółowej analizy użyj zakładek "Drzewo Przodków" i "Drzewo Potomków"

3. **Dodawanie rodziców:**
   - Opcja dostępna tylko przy tworzeniu nowej osoby
   - Aby dodać rodziców do istniejącej osoby, użyj "Zarządzaj relacjami"
   - Lista rodziców zawiera wszystkie osoby odpowiedniej płci

### Przykładowy workflow

**Budowanie drzewa genealogicznego od podstaw:**

1. Dodaj najstarsze osoby (dziadkowie):
   - Jan Kowalski (1920)
   - Anna Kowalska (1922, nazwisko panieńskie: Nowak)

2. Dodaj ich dzieci z wyborem rodziców:
   - Maria Wiśniewska (1945)
   - Matka: Anna Kowalska
   - Ojciec: Jan Kowalski
   
3. Zobacz pełne drzewo:
   - Przejdź do zakładki "Pełne Drzewo"
   - Zobaczysz wszystkie osoby i ich połączenia

4. Eksportuj do GEDCOM:
   - Plik → Eksportuj GEDCOM
   - Wszystkie dane włącznie z nazwiskami panieńskimi zostaną wyeksportowane

### Testy

Wszystkie nowe funkcje są pokryte testami jednostkowymi:
- `test_add_person_with_maiden_name` - test nazwiska panieńskiego
- `test_update_person_with_maiden_name` - test aktualizacji nazwiska panieńskiego
- Migracja bazy danych testowana automatycznie przy każdym uruchomieniu testów

### Co dalej?

Planowane rozszerzenia:
- Wyszukiwanie po nazwisku panieńskim
- Więcej opcji w pełnym drzewie (filtry, zoom)
- Historia zmian nazwiska
- Wsparcie dla wielu nazwisk panieńskich (dla osób w wielu małżeństwach)
