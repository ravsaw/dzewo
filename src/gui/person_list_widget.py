"""
PersonListWidget - Widget wyświetlający listę osób
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget,
                            QTableWidgetItem, QPushButton, QLineEdit, QLabel,
                            QHeaderView, QAbstractItemView)
from PyQt6.QtCore import Qt, pyqtSignal


class PersonListWidget(QWidget):
    """Widget wyświetlający listę osób z funkcją wyszukiwania"""
    
    person_selected = pyqtSignal(int)  # Signal emitowany gdy osoba jest wybrana
    person_edited = pyqtSignal(int)    # Signal emitowany gdy należy edytować osobę
    person_deleted = pyqtSignal(int)   # Signal emitowany gdy należy usunąć osobę
    
    def __init__(self, db_manager, parent=None):
        """
        Inicjalizacja widgetu
        
        Args:
            db_manager: Instancja DatabaseManager
            parent: Widget rodzica
        """
        super().__init__(parent)
        self.db_manager = db_manager
        
        self.init_ui()
        self.load_persons()
    
    def init_ui(self):
        """Inicjalizacja interfejsu użytkownika"""
        layout = QVBoxLayout(self)
        
        # Wyszukiwanie
        search_layout = QHBoxLayout()
        search_layout.addWidget(QLabel("Szukaj:"))
        
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Wpisz imię lub nazwisko...")
        self.search_edit.textChanged.connect(self.search_persons)
        search_layout.addWidget(self.search_edit)
        
        layout.addLayout(search_layout)
        
        # Tabela osób
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "ID", "Imię", "Nazwisko", "Data urodzenia", "Płeć", "Miejsce urodzenia"
        ])
        
        # Ustawienia tabeli
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setSortingEnabled(True)
        
        # Rozciąganie kolumn
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.Stretch)
        
        # Podwójne kliknięcie na wiersz
        self.table.doubleClicked.connect(self.on_row_double_clicked)
        
        # Kliknięcie na wiersz
        self.table.itemSelectionChanged.connect(self.on_selection_changed)
        
        layout.addWidget(self.table)
        
        # Przyciski
        button_layout = QHBoxLayout()
        
        self.add_button = QPushButton("Dodaj")
        self.add_button.clicked.connect(self.on_add_clicked)
        button_layout.addWidget(self.add_button)
        
        self.edit_button = QPushButton("Edytuj")
        self.edit_button.clicked.connect(self.on_edit_clicked)
        self.edit_button.setEnabled(False)
        button_layout.addWidget(self.edit_button)
        
        self.delete_button = QPushButton("Usuń")
        self.delete_button.clicked.connect(self.on_delete_clicked)
        self.delete_button.setEnabled(False)
        button_layout.addWidget(self.delete_button)
        
        self.relations_button = QPushButton("Zarządzaj relacjami")
        self.relations_button.clicked.connect(self.on_relations_clicked)
        self.relations_button.setEnabled(False)
        button_layout.addWidget(self.relations_button)
        
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
    
    def load_persons(self, persons=None):
        """
        Ładuje listę osób do tabeli
        
        Args:
            persons: Lista osób do wyświetlenia (None = wszystkie)
        """
        if persons is None:
            persons = self.db_manager.get_all_persons()
        
        self.table.setRowCount(0)
        self.table.setSortingEnabled(False)
        
        for person in persons:
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            
            self.table.setItem(row_position, 0, QTableWidgetItem(str(person['id'])))
            self.table.setItem(row_position, 1, QTableWidgetItem(person['imie']))
            self.table.setItem(row_position, 2, QTableWidgetItem(person['nazwisko']))
            self.table.setItem(row_position, 3, QTableWidgetItem(person['data_urodzenia'] or ''))
            self.table.setItem(row_position, 4, QTableWidgetItem(person['plec'] or ''))
            self.table.setItem(row_position, 5, QTableWidgetItem(person['miejsce_urodzenia'] or ''))
        
        self.table.setSortingEnabled(True)
    
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
        selected_rows = self.table.selectedItems()
        if selected_rows:
            row = selected_rows[0].row()
            person_id = int(self.table.item(row, 0).text())
            return person_id
        return None
    
    def on_selection_changed(self):
        """Obsługa zmiany zaznaczenia"""
        has_selection = len(self.table.selectedItems()) > 0
        self.edit_button.setEnabled(has_selection)
        self.delete_button.setEnabled(has_selection)
        self.relations_button.setEnabled(has_selection)
        
        if has_selection:
            person_id = self.get_selected_person_id()
            if person_id:
                self.person_selected.emit(person_id)
    
    def on_row_double_clicked(self, index):
        """Obsługa podwójnego kliknięcia na wiersz"""
        person_id = self.get_selected_person_id()
        if person_id:
            self.person_edited.emit(person_id)
    
    def on_add_clicked(self):
        """Obsługa kliknięcia przycisku Dodaj"""
        from .person_dialog import PersonDialog
        dialog = PersonDialog(self.db_manager, parent=self)
        if dialog.exec():
            self.load_persons()
    
    def on_edit_clicked(self):
        """Obsługa kliknięcia przycisku Edytuj"""
        person_id = self.get_selected_person_id()
        if person_id:
            self.person_edited.emit(person_id)
    
    def on_delete_clicked(self):
        """Obsługa kliknięcia przycisku Usuń"""
        person_id = self.get_selected_person_id()
        if person_id:
            self.person_deleted.emit(person_id)
    
    def on_relations_clicked(self):
        """Obsługa kliknięcia przycisku Zarządzaj relacjami"""
        person_id = self.get_selected_person_id()
        if person_id:
            from .relation_dialog import RelationDialog
            dialog = RelationDialog(self.db_manager, person_id, parent=self)
            if dialog.exec():
                self.load_persons()
