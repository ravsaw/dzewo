"""
MainWindow - Główne okno aplikacji
"""

from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                            QPushButton, QTabWidget, QMessageBox, QFileDialog,
                            QMenuBar, QMenu, QStatusBar, QToolBar, QLabel)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QAction, QIcon

from .person_list_widget import PersonListWidget
from .person_dialog import PersonDialog
from .ancestor_tree_widget import AncestorTreeWidget
from .descendant_tree_widget import DescendantTreeWidget
from .full_tree_widget import FullTreeWidget
from .timeline_widget import TimelineWidget
from ..business_logic.relationship_calculator import RelationshipCalculator


class MainWindow(QMainWindow):
    """Główne okno aplikacji Drzewo Genealogiczne"""
    
    def __init__(self, db_manager):
        """
        Inicjalizacja głównego okna
        
        Args:
            db_manager: Instancja DatabaseManager
        """
        super().__init__()
        self.db_manager = db_manager
        self.relationship_calc = RelationshipCalculator(db_manager)
        self.current_person_id = None
        
        self.init_ui()
        self.load_data()
    
    def init_ui(self):
        """Inicjalizacja interfejsu użytkownika"""
        self.setWindowTitle("Drzewo Genealogiczne")
        self.setMinimumSize(1000, 700)
        
        # Menu
        self.create_menu()
        
        # Toolbar
        self.create_toolbar()
        
        # Centralny widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout główny
        main_layout = QVBoxLayout(central_widget)
        
        # Tabs
        self.tabs = QTabWidget()
        
        # Tab - Lista osób
        self.person_list_widget = PersonListWidget(self.db_manager)
        self.person_list_widget.person_selected.connect(self.on_person_selected)
        self.person_list_widget.person_edited.connect(self.on_edit_person)
        self.person_list_widget.person_deleted.connect(self.on_delete_person)
        self.tabs.addTab(self.person_list_widget, "Lista Osób")
        
        # Tab - Drzewo przodków
        self.ancestor_tree_widget = AncestorTreeWidget(self.db_manager, self.relationship_calc)
        self.tabs.addTab(self.ancestor_tree_widget, "Drzewo Przodków")
        
        # Tab - Drzewo potomków
        self.descendant_tree_widget = DescendantTreeWidget(self.db_manager, self.relationship_calc)
        self.tabs.addTab(self.descendant_tree_widget, "Drzewo Potomków")
        
        # Tab - Pełne drzewo
        self.full_tree_widget = FullTreeWidget(self.db_manager, self.relationship_calc)
        self.tabs.addTab(self.full_tree_widget, "Pełne Drzewo")
        
        # Tab - Oś czasu
        self.timeline_widget = TimelineWidget(self.db_manager)
        self.tabs.addTab(self.timeline_widget, "Oś Czasu")
        
        main_layout.addWidget(self.tabs)
        
        # Status bar
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("Gotowy")
    
    def create_menu(self):
        """Tworzy menu aplikacji"""
        menubar = self.menuBar()
        
        # Menu Plik
        file_menu = menubar.addMenu("&Plik")
        
        # Import GEDCOM
        import_action = QAction("&Importuj GEDCOM", self)
        import_action.setStatusTip("Importuj dane z pliku GEDCOM")
        import_action.triggered.connect(self.import_gedcom)
        file_menu.addAction(import_action)
        
        # Eksport GEDCOM
        export_action = QAction("&Eksportuj GEDCOM", self)
        export_action.setStatusTip("Eksportuj dane do pliku GEDCOM")
        export_action.triggered.connect(self.export_gedcom)
        file_menu.addAction(export_action)
        
        file_menu.addSeparator()
        
        # Wyjście
        exit_action = QAction("&Wyjdź", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.setStatusTip("Wyjdź z aplikacji")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Menu Osoby
        person_menu = menubar.addMenu("&Osoby")
        
        # Dodaj osobę
        add_person_action = QAction("&Dodaj osobę", self)
        add_person_action.setShortcut("Ctrl+N")
        add_person_action.setStatusTip("Dodaj nową osobę")
        add_person_action.triggered.connect(self.on_add_person)
        person_menu.addAction(add_person_action)
        
        # Edytuj osobę
        edit_person_action = QAction("&Edytuj osobę", self)
        edit_person_action.setShortcut("Ctrl+E")
        edit_person_action.setStatusTip("Edytuj wybraną osobę")
        edit_person_action.triggered.connect(self.on_edit_selected_person)
        person_menu.addAction(edit_person_action)
        
        # Usuń osobę
        delete_person_action = QAction("&Usuń osobę", self)
        delete_person_action.setShortcut("Delete")
        delete_person_action.setStatusTip("Usuń wybraną osobę")
        delete_person_action.triggered.connect(self.on_delete_selected_person)
        person_menu.addAction(delete_person_action)
        
        # Menu Pomoc
        help_menu = menubar.addMenu("&Pomoc")
        
        # O aplikacji
        about_action = QAction("&O aplikacji", self)
        about_action.setStatusTip("Informacje o aplikacji")
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def create_toolbar(self):
        """Tworzy pasek narzędzi"""
        toolbar = QToolBar("Główny pasek narzędzi")
        toolbar.setIconSize(QSize(24, 24))
        self.addToolBar(toolbar)
        
        # Dodaj osobę
        add_action = QAction("Dodaj", self)
        add_action.setStatusTip("Dodaj nową osobę")
        add_action.triggered.connect(self.on_add_person)
        toolbar.addAction(add_action)
        
        # Edytuj osobę
        edit_action = QAction("Edytuj", self)
        edit_action.setStatusTip("Edytuj wybraną osobę")
        edit_action.triggered.connect(self.on_edit_selected_person)
        toolbar.addAction(edit_action)
        
        # Usuń osobę
        delete_action = QAction("Usuń", self)
        delete_action.setStatusTip("Usuń wybraną osobę")
        delete_action.triggered.connect(self.on_delete_selected_person)
        toolbar.addAction(delete_action)
        
        toolbar.addSeparator()
        
        # Odśwież
        refresh_action = QAction("Odśwież", self)
        refresh_action.setStatusTip("Odśwież dane")
        refresh_action.triggered.connect(self.load_data)
        toolbar.addAction(refresh_action)
    
    def load_data(self):
        """Ładuje dane do wszystkich widgetów"""
        self.person_list_widget.load_persons()
        self.timeline_widget.load_timeline()
        self.full_tree_widget.load_tree()
        
        if self.current_person_id:
            self.ancestor_tree_widget.load_tree(self.current_person_id)
            self.descendant_tree_widget.load_tree(self.current_person_id)
        
        # Aktualizacja statusu
        person_count = len(self.db_manager.get_all_persons())
        self.statusBar.showMessage(f"Załadowano {person_count} osób")
    
    def on_person_selected(self, person_id: int):
        """
        Obsługa wyboru osoby z listy
        
        Args:
            person_id: ID wybranej osoby
        """
        self.current_person_id = person_id
        self.ancestor_tree_widget.load_tree(person_id)
        self.descendant_tree_widget.load_tree(person_id)
        
        person = self.db_manager.get_person(person_id)
        if person:
            self.statusBar.showMessage(f"Wybrano: {person['imie']} {person['nazwisko']}")
    
    def on_add_person(self):
        """Obsługa dodawania nowej osoby"""
        dialog = PersonDialog(self.db_manager, parent=self)
        if dialog.exec():
            self.load_data()
            QMessageBox.information(self, "Sukces", "Osoba została dodana")
    
    def on_edit_person(self, person_id: int):
        """
        Obsługa edycji osoby
        
        Args:
            person_id: ID osoby do edycji
        """
        dialog = PersonDialog(self.db_manager, person_id, parent=self)
        if dialog.exec():
            self.load_data()
            QMessageBox.information(self, "Sukces", "Dane osoby zostały zaktualizowane")
    
    def on_edit_selected_person(self):
        """Obsługa edycji wybranej osoby"""
        if self.current_person_id:
            self.on_edit_person(self.current_person_id)
        else:
            QMessageBox.warning(self, "Błąd", "Nie wybrano żadnej osoby")
    
    def on_delete_person(self, person_id: int):
        """
        Obsługa usuwania osoby
        
        Args:
            person_id: ID osoby do usunięcia
        """
        person = self.db_manager.get_person(person_id)
        if not person:
            return
        
        reply = QMessageBox.question(
            self,
            "Potwierdzenie",
            f"Czy na pewno chcesz usunąć osobę {person['imie']} {person['nazwisko']}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.db_manager.delete_person(person_id)
            if self.current_person_id == person_id:
                self.current_person_id = None
            self.load_data()
            QMessageBox.information(self, "Sukces", "Osoba została usunięta")
    
    def on_delete_selected_person(self):
        """Obsługa usuwania wybranej osoby"""
        if self.current_person_id:
            self.on_delete_person(self.current_person_id)
        else:
            QMessageBox.warning(self, "Błąd", "Nie wybrano żadnej osoby")
    
    def import_gedcom(self):
        """Importuje dane z pliku GEDCOM"""
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Importuj GEDCOM",
            "",
            "Pliki GEDCOM (*.ged);;Wszystkie pliki (*)"
        )
        
        if filename:
            try:
                from ..utils.gedcom_handler import GedcomHandler
                handler = GedcomHandler(self.db_manager)
                handler.import_file(filename)
                self.load_data()
                QMessageBox.information(self, "Sukces", "Dane zostały zaimportowane")
            except Exception as e:
                QMessageBox.critical(self, "Błąd", f"Nie udało się zaimportować pliku: {str(e)}")
    
    def export_gedcom(self):
        """Eksportuje dane do pliku GEDCOM"""
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Eksportuj GEDCOM",
            "",
            "Pliki GEDCOM (*.ged);;Wszystkie pliki (*)"
        )
        
        if filename:
            try:
                from ..utils.gedcom_handler import GedcomHandler
                handler = GedcomHandler(self.db_manager)
                handler.export_file(filename)
                QMessageBox.information(self, "Sukces", "Dane zostały wyeksportowane")
            except Exception as e:
                QMessageBox.critical(self, "Błąd", f"Nie udało się wyeksportować pliku: {str(e)}")
    
    def show_about(self):
        """Wyświetla okno O aplikacji"""
        QMessageBox.about(
            self,
            "O aplikacji",
            "<h2>Drzewo Genealogiczne</h2>"
            "<p>Wersja 1.0.0</p>"
            "<p>Aplikacja desktopowa do zarządzania drzewem genealogicznym</p>"
            "<p><b>Technologie:</b></p>"
            "<ul>"
            "<li>Python 3.10+</li>"
            "<li>PyQt6</li>"
            "<li>SQLite</li>"
            "<li>matplotlib</li>"
            "</ul>"
        )
