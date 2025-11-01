"""
PersonSelectorDialog - Dialog do wyboru osoby z listy
"""

from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QListWidget,
                            QPushButton, QLineEdit, QLabel, QMessageBox,
                            QListWidgetItem)
from PyQt6.QtCore import Qt


class PersonSelectorDialog(QDialog):
    """Dialog do wyboru osoby z listy"""
    
    def __init__(self, db_manager, exclude_person_id=None, parent=None):
        """
        Inicjalizacja dialogu
        
        Args:
            db_manager: Instancja DatabaseManager
            exclude_person_id: ID osoby do wykluczenia z listy
            parent: Widget rodzica
        """
        super().__init__(parent)
        self.db_manager = db_manager
        self.exclude_person_id = exclude_person_id
        self.selected_person_id = None
        
        self.init_ui()
        self.load_persons()
    
    def init_ui(self):
        """Inicjalizacja interfejsu użytkownika"""
        self.setWindowTitle("Wybierz osobę")
        self.setMinimumSize(400, 500)
        
        layout = QVBoxLayout(self)
        
        # Wyszukiwanie
        search_layout = QHBoxLayout()
        search_layout.addWidget(QLabel("Szukaj:"))
        
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Wpisz imię lub nazwisko...")
        self.search_edit.textChanged.connect(self.search_persons)
        search_layout.addWidget(self.search_edit)
        
        layout.addLayout(search_layout)
        
        # Lista osób
        self.persons_list = QListWidget()
        self.persons_list.itemDoubleClicked.connect(self.on_item_double_clicked)
        layout.addWidget(self.persons_list)
        
        # Przyciski
        button_layout = QHBoxLayout()
        
        self.select_button = QPushButton("Wybierz")
        self.select_button.clicked.connect(self.on_select_clicked)
        button_layout.addWidget(self.select_button)
        
        self.cancel_button = QPushButton("Anuluj")
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)
        
        layout.addLayout(button_layout)
    
    def load_persons(self, persons=None):
        """
        Ładuje listę osób
        
        Args:
            persons: Lista osób do wyświetlenia (None = wszystkie)
        """
        if persons is None:
            persons = self.db_manager.get_all_persons()
        
        self.persons_list.clear()
        
        for person in persons:
            if self.exclude_person_id and person['id'] == self.exclude_person_id:
                continue
            
            birth_year = person['data_urodzenia'].split('-')[0] if person['data_urodzenia'] else '?'
            text = f"{person['imie']} {person['nazwisko']} ({birth_year})"
            
            item = QListWidgetItem(text)
            item.setData(Qt.ItemDataRole.UserRole, person['id'])
            self.persons_list.addItem(item)
    
    def search_persons(self, query):
        """
        Wyszukuje osoby
        
        Args:
            query: Fraza do wyszukania
        """
        if query.strip():
            persons = self.db_manager.search_persons(query.strip())
        else:
            persons = self.db_manager.get_all_persons()
        
        self.load_persons(persons)
    
    def get_selected_person_id(self):
        """
        Zwraca ID wybranej osoby
        
        Returns:
            ID osoby lub None
        """
        return self.selected_person_id
    
    def on_item_double_clicked(self, item):
        """Obsługa podwójnego kliknięcia na element"""
        self.selected_person_id = item.data(Qt.ItemDataRole.UserRole)
        self.accept()
    
    def on_select_clicked(self):
        """Obsługa kliknięcia przycisku Wybierz"""
        current_item = self.persons_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "Błąd", "Nie wybrano żadnej osoby")
            return
        
        self.selected_person_id = current_item.data(Qt.ItemDataRole.UserRole)
        self.accept()
