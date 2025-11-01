"""
DatabaseManager - Zarządza połączeniem z bazą danych i operacjami CRUD
"""

import sqlite3
from typing import List, Optional, Tuple
from datetime import datetime


class DatabaseManager:
    """Zarządza połączeniem z bazą danych SQLite i operacjami CRUD"""
    
    def __init__(self, db_path: str):
        """
        Inicjalizacja managera bazy danych
        
        Args:
            db_path: Ścieżka do pliku bazy danych SQLite
        """
        self.db_path = db_path
        self.connection = None
        self.cursor = None
        self._connect()
        self._create_tables()
    
    def _connect(self):
        """Nawiązuje połączenie z bazą danych"""
        self.connection = sqlite3.connect(self.db_path)
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()
    
    def _create_tables(self):
        """Tworzy tabele w bazie danych jeśli nie istnieją"""
        # Tabela osób
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS osoby (
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
        ''')
        
        # Tabela relacji
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS relacje (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                osoba1_id INTEGER NOT NULL,
                osoba2_id INTEGER NOT NULL,
                rodzaj_relacji TEXT NOT NULL,
                FOREIGN KEY (osoba1_id) REFERENCES osoby (id) ON DELETE CASCADE,
                FOREIGN KEY (osoba2_id) REFERENCES osoby (id) ON DELETE CASCADE
            )
        ''')
        
        self.connection.commit()
    
    def add_person(self, imie: str, nazwisko: str, data_urodzenia: Optional[str] = None,
                   data_smierci: Optional[str] = None, plec: Optional[str] = None,
                   miejsce_urodzenia: Optional[str] = None, miejsce_smierci: Optional[str] = None,
                   notatki: Optional[str] = None, zdjecie_sciezka: Optional[str] = None) -> int:
        """
        Dodaje osobę do bazy danych
        
        Args:
            imie: Imię osoby
            nazwisko: Nazwisko osoby
            data_urodzenia: Data urodzenia (YYYY-MM-DD)
            data_smierci: Data śmierci (YYYY-MM-DD)
            plec: Płeć (M/K)
            miejsce_urodzenia: Miejsce urodzenia
            miejsce_smierci: Miejsce śmierci
            notatki: Notatki o osobie
            zdjecie_sciezka: Ścieżka do zdjęcia
            
        Returns:
            ID dodanej osoby
        """
        self.cursor.execute('''
            INSERT INTO osoby (imie, nazwisko, data_urodzenia, data_smierci, plec,
                             miejsce_urodzenia, miejsce_smierci, notatki, zdjecie_sciezka)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (imie, nazwisko, data_urodzenia, data_smierci, plec,
              miejsce_urodzenia, miejsce_smierci, notatki, zdjecie_sciezka))
        
        self.connection.commit()
        return self.cursor.lastrowid
    
    def update_person(self, person_id: int, imie: str, nazwisko: str,
                     data_urodzenia: Optional[str] = None, data_smierci: Optional[str] = None,
                     plec: Optional[str] = None, miejsce_urodzenia: Optional[str] = None,
                     miejsce_smierci: Optional[str] = None, notatki: Optional[str] = None,
                     zdjecie_sciezka: Optional[str] = None):
        """
        Aktualizuje dane osoby
        
        Args:
            person_id: ID osoby do aktualizacji
            imie: Imię osoby
            nazwisko: Nazwisko osoby
            data_urodzenia: Data urodzenia
            data_smierci: Data śmierci
            plec: Płeć
            miejsce_urodzenia: Miejsce urodzenia
            miejsce_smierci: Miejsce śmierci
            notatki: Notatki
            zdjecie_sciezka: Ścieżka do zdjęcia
        """
        self.cursor.execute('''
            UPDATE osoby
            SET imie = ?, nazwisko = ?, data_urodzenia = ?, data_smierci = ?,
                plec = ?, miejsce_urodzenia = ?, miejsce_smierci = ?,
                notatki = ?, zdjecie_sciezka = ?
            WHERE id = ?
        ''', (imie, nazwisko, data_urodzenia, data_smierci, plec,
              miejsce_urodzenia, miejsce_smierci, notatki, zdjecie_sciezka, person_id))
        
        self.connection.commit()
    
    def delete_person(self, person_id: int):
        """
        Usuwa osobę z bazy danych
        
        Args:
            person_id: ID osoby do usunięcia
        """
        # Najpierw usuń relacje
        self.cursor.execute('DELETE FROM relacje WHERE osoba1_id = ? OR osoba2_id = ?',
                          (person_id, person_id))
        # Następnie usuń osobę
        self.cursor.execute('DELETE FROM osoby WHERE id = ?', (person_id,))
        self.connection.commit()
    
    def get_person(self, person_id: int) -> Optional[dict]:
        """
        Pobiera dane osoby po ID
        
        Args:
            person_id: ID osoby
            
        Returns:
            Słownik z danymi osoby lub None jeśli nie znaleziono
        """
        self.cursor.execute('SELECT * FROM osoby WHERE id = ?', (person_id,))
        row = self.cursor.fetchone()
        return dict(row) if row else None
    
    def get_all_persons(self) -> List[dict]:
        """
        Pobiera wszystkie osoby z bazy danych
        
        Returns:
            Lista słowników z danymi osób
        """
        self.cursor.execute('SELECT * FROM osoby ORDER BY nazwisko, imie')
        return [dict(row) for row in self.cursor.fetchall()]
    
    def add_relation(self, osoba1_id: int, osoba2_id: int, rodzaj_relacji: str) -> int:
        """
        Dodaje relację między dwiema osobami
        
        Args:
            osoba1_id: ID pierwszej osoby
            osoba2_id: ID drugiej osoby
            rodzaj_relacji: Rodzaj relacji (rodzic, małżonek, dziecko)
            
        Returns:
            ID dodanej relacji
        """
        self.cursor.execute('''
            INSERT INTO relacje (osoba1_id, osoba2_id, rodzaj_relacji)
            VALUES (?, ?, ?)
        ''', (osoba1_id, osoba2_id, rodzaj_relacji))
        
        self.connection.commit()
        return self.cursor.lastrowid
    
    def delete_relation(self, relation_id: int):
        """
        Usuwa relację
        
        Args:
            relation_id: ID relacji do usunięcia
        """
        self.cursor.execute('DELETE FROM relacje WHERE id = ?', (relation_id,))
        self.connection.commit()
    
    def get_relations(self, person_id: int) -> List[dict]:
        """
        Pobiera wszystkie relacje osoby
        
        Args:
            person_id: ID osoby
            
        Returns:
            Lista słowników z relacjami
        """
        self.cursor.execute('''
            SELECT r.*, o1.imie as osoba1_imie, o1.nazwisko as osoba1_nazwisko,
                   o2.imie as osoba2_imie, o2.nazwisko as osoba2_nazwisko
            FROM relacje r
            JOIN osoby o1 ON r.osoba1_id = o1.id
            JOIN osoby o2 ON r.osoba2_id = o2.id
            WHERE r.osoba1_id = ? OR r.osoba2_id = ?
        ''', (person_id, person_id))
        
        return [dict(row) for row in self.cursor.fetchall()]
    
    def get_all_relations(self) -> List[dict]:
        """
        Pobiera wszystkie relacje z bazy danych
        
        Returns:
            Lista słowników z relacjami
        """
        self.cursor.execute('''
            SELECT r.*, o1.imie as osoba1_imie, o1.nazwisko as osoba1_nazwisko,
                   o2.imie as osoba2_imie, o2.nazwisko as osoba2_nazwisko
            FROM relacje r
            JOIN osoby o1 ON r.osoba1_id = o1.id
            JOIN osoby o2 ON r.osoba2_id = o2.id
        ''')
        
        return [dict(row) for row in self.cursor.fetchall()]
    
    def search_persons(self, query: str) -> List[dict]:
        """
        Wyszukuje osoby po imieniu lub nazwisku
        
        Args:
            query: Fraza do wyszukania
            
        Returns:
            Lista słowników z danymi osób
        """
        search_pattern = f'%{query}%'
        self.cursor.execute('''
            SELECT * FROM osoby
            WHERE imie LIKE ? OR nazwisko LIKE ?
            ORDER BY nazwisko, imie
        ''', (search_pattern, search_pattern))
        
        return [dict(row) for row in self.cursor.fetchall()]
    
    def close(self):
        """Zamyka połączenie z bazą danych"""
        if self.connection:
            self.connection.close()
