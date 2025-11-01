"""
GedcomHandler - Obsługuje import i eksport danych w formacie GEDCOM
"""


class GedcomHandler:
    """Obsługuje import i eksport danych genealogicznych w formacie GEDCOM"""
    
    def __init__(self, db_manager):
        """
        Inicjalizacja handlera GEDCOM
        
        Args:
            db_manager: Instancja DatabaseManager
        """
        self.db_manager = db_manager
    
    def import_file(self, filename: str):
        """
        Importuje dane z pliku GEDCOM
        
        Args:
            filename: Ścieżka do pliku GEDCOM
            
        Note:
            To jest uproszczona implementacja. Pełna implementacja GEDCOM
            wymagałaby bardziej zaawansowanego parsera.
        """
        # Uproszczona implementacja - w pełnej wersji należałoby użyć
        # dedykowanej biblioteki do parsowania GEDCOM
        
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Podstawowe parsowanie
        lines = content.split('\n')
        current_person = None
        person_map = {}  # Mapowanie GEDCOM ID -> DB ID
        
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            
            if not line:
                i += 1
                continue
            
            parts = line.split(' ', 2)
            
            if len(parts) >= 2 and parts[1] == 'INDI':
                # Rozpoczęcie nowej osoby
                gedcom_id = parts[0].strip('@')
                current_person = {
                    'gedcom_id': gedcom_id,
                    'imie': '',
                    'nazwisko': '',
                    'data_urodzenia': None,
                    'data_smierci': None,
                    'plec': None
                }
                
                # Parsuj dane osoby
                i += 1
                while i < len(lines):
                    sub_line = lines[i].strip()
                    if not sub_line or sub_line[0] == '0':
                        break
                    
                    sub_parts = sub_line.split(' ', 2)
                    
                    if len(sub_parts) >= 2:
                        if sub_parts[1] == 'NAME' and len(sub_parts) >= 3:
                            # Parsuj imię i nazwisko
                            name = sub_parts[2].replace('/', '').strip()
                            name_parts = name.split()
                            if name_parts:
                                current_person['imie'] = name_parts[0]
                                if len(name_parts) > 1:
                                    current_person['nazwisko'] = ' '.join(name_parts[1:])
                        
                        elif sub_parts[1] == 'SEX' and len(sub_parts) >= 3:
                            sex = sub_parts[2].strip()
                            current_person['plec'] = 'M' if sex == 'M' else 'K' if sex == 'F' else None
                        
                        elif sub_parts[1] == 'BIRT':
                            # Data urodzenia w następnej linii
                            i += 1
                            if i < len(lines):
                                date_line = lines[i].strip()
                                if 'DATE' in date_line:
                                    date_str = date_line.split('DATE', 1)[1].strip()
                                    current_person['data_urodzenia'] = self._parse_gedcom_date(date_str)
                        
                        elif sub_parts[1] == 'DEAT':
                            # Data śmierci w następnej linii
                            i += 1
                            if i < len(lines):
                                date_line = lines[i].strip()
                                if 'DATE' in date_line:
                                    date_str = date_line.split('DATE', 1)[1].strip()
                                    current_person['data_smierci'] = self._parse_gedcom_date(date_str)
                    
                    i += 1
                
                # Zapisz osobę do bazy
                if current_person['imie'] and current_person['nazwisko']:
                    person_id = self.db_manager.add_person(
                        current_person['imie'],
                        current_person['nazwisko'],
                        current_person['data_urodzenia'],
                        current_person['data_smierci'],
                        current_person['plec']
                    )
                    person_map[current_person['gedcom_id']] = person_id
                
                continue
            
            i += 1
        
        # W drugiej iteracji dodaj relacje
        # To jest uproszczone - pełna implementacja wymagałaby parsowania rekordów FAM
    
    def export_file(self, filename: str):
        """
        Eksportuje dane do pliku GEDCOM
        
        Args:
            filename: Ścieżka do pliku GEDCOM
        """
        persons = self.db_manager.get_all_persons()
        relations = self.db_manager.get_all_relations()
        
        lines = []
        
        # Nagłówek
        lines.append("0 HEAD")
        lines.append("1 SOUR Drzewo Genealogiczne")
        lines.append("1 GEDC")
        lines.append("2 VERS 5.5.1")
        lines.append("2 FORM LINEAGE-LINKED")
        lines.append("1 CHAR UTF-8")
        
        # Eksport osób
        for person in persons:
            person_id = f"@I{person['id']}@"
            
            lines.append(f"0 {person_id} INDI")
            lines.append(f"1 NAME {person['imie']} /{person['nazwisko']}/")
            
            if person.get('plec'):
                sex = 'M' if person['plec'] == 'M' else 'F'
                lines.append(f"1 SEX {sex}")
            
            if person.get('data_urodzenia'):
                lines.append("1 BIRT")
                lines.append(f"2 DATE {self._format_gedcom_date(person['data_urodzenia'])}")
                
                if person.get('miejsce_urodzenia'):
                    lines.append(f"2 PLAC {person['miejsce_urodzenia']}")
            
            if person.get('data_smierci'):
                lines.append("1 DEAT")
                lines.append(f"2 DATE {self._format_gedcom_date(person['data_smierci'])}")
                
                if person.get('miejsce_smierci'):
                    lines.append(f"2 PLAC {person['miejsce_smierci']}")
            
            if person.get('notatki'):
                lines.append(f"1 NOTE {person['notatki']}")
        
        # Eksport rodzin (relacji)
        family_counter = 1
        processed_couples = set()
        
        for relation in relations:
            if relation['rodzaj_relacji'] == 'małżonek':
                couple_key = tuple(sorted([relation['osoba1_id'], relation['osoba2_id']]))
                
                if couple_key not in processed_couples:
                    processed_couples.add(couple_key)
                    
                    family_id = f"@F{family_counter}@"
                    family_counter += 1
                    
                    lines.append(f"0 {family_id} FAM")
                    lines.append(f"1 HUSB @I{relation['osoba1_id']}@")
                    lines.append(f"1 WIFE @I{relation['osoba2_id']}@")
                    
                    # Znajdź dzieci tego małżeństwa
                    for rel in relations:
                        if rel['rodzaj_relacji'] == 'rodzic':
                            if rel['osoba1_id'] in couple_key:
                                lines.append(f"1 CHIL @I{rel['osoba2_id']}@")
        
        # Zakończenie
        lines.append("0 TRLR")
        
        # Zapisz do pliku
        with open(filename, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
    
    def _parse_gedcom_date(self, date_str: str) -> str:
        """
        Parsuje datę z formatu GEDCOM do formatu YYYY-MM-DD
        
        Args:
            date_str: Data w formacie GEDCOM
            
        Returns:
            Data w formacie YYYY-MM-DD lub None
        """
        # Uproszczone parsowanie - obsługuje tylko format "DD MMM YYYY"
        months = {
            'JAN': '01', 'FEB': '02', 'MAR': '03', 'APR': '04',
            'MAY': '05', 'JUN': '06', 'JUL': '07', 'AUG': '08',
            'SEP': '09', 'OCT': '10', 'NOV': '11', 'DEC': '12'
        }
        
        parts = date_str.strip().split()
        
        if len(parts) >= 3:
            try:
                day = parts[0].zfill(2)
                month = months.get(parts[1].upper(), '01')
                year = parts[2]
                return f"{year}-{month}-{day}"
            except (ValueError, IndexError):
                pass
        elif len(parts) == 1:
            # Tylko rok
            try:
                return f"{parts[0]}-01-01"
            except ValueError:
                pass
        
        return None
    
    def _format_gedcom_date(self, date_str: str) -> str:
        """
        Formatuje datę z formatu YYYY-MM-DD do formatu GEDCOM
        
        Args:
            date_str: Data w formacie YYYY-MM-DD
            
        Returns:
            Data w formacie GEDCOM
        """
        months = [
            'JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN',
            'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC'
        ]
        
        try:
            parts = date_str.split('-')
            if len(parts) == 3:
                year, month, day = parts
                month_name = months[int(month) - 1]
                return f"{int(day)} {month_name} {year}"
        except (ValueError, IndexError):
            pass
        
        return date_str
