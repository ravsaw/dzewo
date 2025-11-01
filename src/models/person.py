"""
Model osoby
"""

from dataclasses import dataclass
from typing import Optional
from datetime import date


@dataclass
class Person:
    """Model danych osoby"""
    
    id: Optional[int] = None
    imie: str = ""
    nazwisko: str = ""
    data_urodzenia: Optional[str] = None
    data_smierci: Optional[str] = None
    plec: Optional[str] = None
    miejsce_urodzenia: Optional[str] = None
    miejsce_smierci: Optional[str] = None
    notatki: Optional[str] = None
    zdjecie_sciezka: Optional[str] = None
    
    def get_full_name(self) -> str:
        """Zwraca pełne imię i nazwisko"""
        return f"{self.imie} {self.nazwisko}"
    
    def get_birth_year(self) -> Optional[int]:
        """Zwraca rok urodzenia jeśli dostępny"""
        if self.data_urodzenia:
            try:
                return int(self.data_urodzenia.split('-')[0])
            except (ValueError, IndexError):
                return None
        return None
    
    def get_death_year(self) -> Optional[int]:
        """Zwraca rok śmierci jeśli dostępny"""
        if self.data_smierci:
            try:
                return int(self.data_smierci.split('-')[0])
            except (ValueError, IndexError):
                return None
        return None
    
    def is_alive(self) -> bool:
        """Sprawdza czy osoba żyje"""
        return self.data_smierci is None or self.data_smierci == ""
    
    def to_dict(self) -> dict:
        """Konwertuje obiekt Person do słownika"""
        return {
            'id': self.id,
            'imie': self.imie,
            'nazwisko': self.nazwisko,
            'data_urodzenia': self.data_urodzenia,
            'data_smierci': self.data_smierci,
            'plec': self.plec,
            'miejsce_urodzenia': self.miejsce_urodzenia,
            'miejsce_smierci': self.miejsce_smierci,
            'notatki': self.notatki,
            'zdjecie_sciezka': self.zdjecie_sciezka
        }
    
    @staticmethod
    def from_dict(data: dict) -> 'Person':
        """Tworzy obiekt Person ze słownika"""
        return Person(
            id=data.get('id'),
            imie=data.get('imie', ''),
            nazwisko=data.get('nazwisko', ''),
            data_urodzenia=data.get('data_urodzenia'),
            data_smierci=data.get('data_smierci'),
            plec=data.get('plec'),
            miejsce_urodzenia=data.get('miejsce_urodzenia'),
            miejsce_smierci=data.get('miejsce_smierci'),
            notatki=data.get('notatki'),
            zdjecie_sciezka=data.get('zdjecie_sciezka')
        )
