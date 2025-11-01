"""
Model relacji między osobami
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Relation:
    """Model relacji między dwiema osobami"""
    
    id: Optional[int] = None
    osoba1_id: int = 0
    osoba2_id: int = 0
    rodzaj_relacji: str = ""
    
    # Dodatkowe pola do wyświetlania
    osoba1_imie: Optional[str] = None
    osoba1_nazwisko: Optional[str] = None
    osoba2_imie: Optional[str] = None
    osoba2_nazwisko: Optional[str] = None
    
    def get_relation_description(self) -> str:
        """Zwraca opis relacji"""
        if self.osoba1_imie and self.osoba2_imie:
            return f"{self.osoba1_imie} {self.osoba1_nazwisko} - {self.rodzaj_relacji} - {self.osoba2_imie} {self.osoba2_nazwisko}"
        return f"Osoba {self.osoba1_id} - {self.rodzaj_relacji} - Osoba {self.osoba2_id}"
    
    def to_dict(self) -> dict:
        """Konwertuje obiekt Relation do słownika"""
        return {
            'id': self.id,
            'osoba1_id': self.osoba1_id,
            'osoba2_id': self.osoba2_id,
            'rodzaj_relacji': self.rodzaj_relacji,
            'osoba1_imie': self.osoba1_imie,
            'osoba1_nazwisko': self.osoba1_nazwisko,
            'osoba2_imie': self.osoba2_imie,
            'osoba2_nazwisko': self.osoba2_nazwisko
        }
    
    @staticmethod
    def from_dict(data: dict) -> 'Relation':
        """Tworzy obiekt Relation ze słownika"""
        return Relation(
            id=data.get('id'),
            osoba1_id=data.get('osoba1_id', 0),
            osoba2_id=data.get('osoba2_id', 0),
            rodzaj_relacji=data.get('rodzaj_relacji', ''),
            osoba1_imie=data.get('osoba1_imie'),
            osoba1_nazwisko=data.get('osoba1_nazwisko'),
            osoba2_imie=data.get('osoba2_imie'),
            osoba2_nazwisko=data.get('osoba2_nazwisko')
        )
