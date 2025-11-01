"""
RelationDialog - Dialog do zarządzania relacjami osoby
"""

from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QListWidget,
                            QPushButton, QComboBox, QLabel, QMessageBox,
                            QListWidgetItem)
from PyQt6.QtCore import Qt


class RelationDialog(QDialog):
    """Dialog do zarządzania relacjami osoby"""
    
    def __init__(self, db_manager, person_id, parent=None):
        """
        Inicjalizacja dialogu
        
        Args:
            db_manager: Instancja DatabaseManager
            person_id: ID osoby
            parent: Widget rodzica
        """
        super().__init__(parent)
        self.db_manager = db_manager
        self.person_id = person_id
        
        person = self.db_manager.get_person(person_id)
        self.person_name = f"{person['imie']} {person['nazwisko']}" if person else "Nieznana"
        
        self.init_ui()
        self.load_relations()
    
    def init_ui(self):
        """Inicjalizacja interfejsu użytkownika"""
        self.setWindowTitle(f"Relacje - {self.person_name}")
        self.setMinimumSize(600, 400)
        
        layout = QVBoxLayout(self)
        
        # Informacja
        info_label = QLabel(f"<b>Zarządzanie relacjami dla:</b> {self.person_name}")
        layout.addWidget(info_label)
        
        # Lista relacji
        self.relations_list = QListWidget()
        layout.addWidget(self.relations_list)
        
        # Przyciski relacji
        relation_layout = QHBoxLayout()
        
        self.add_parent_button = QPushButton("Dodaj rodzica")
        self.add_parent_button.clicked.connect(lambda: self.add_relation('rodzic'))
        relation_layout.addWidget(self.add_parent_button)
        
        self.add_child_button = QPushButton("Dodaj dziecko")
        self.add_child_button.clicked.connect(lambda: self.add_relation('dziecko'))
        relation_layout.addWidget(self.add_child_button)
        
        self.add_spouse_button = QPushButton("Dodaj małżonka")
        self.add_spouse_button.clicked.connect(lambda: self.add_relation('małżonek'))
        relation_layout.addWidget(self.add_spouse_button)
        
        self.delete_relation_button = QPushButton("Usuń relację")
        self.delete_relation_button.clicked.connect(self.delete_relation)
        relation_layout.addWidget(self.delete_relation_button)
        
        layout.addLayout(relation_layout)
        
        # Przycisk zamknij
        close_layout = QHBoxLayout()
        close_layout.addStretch()
        
        self.close_button = QPushButton("Zamknij")
        self.close_button.clicked.connect(self.accept)
        close_layout.addWidget(self.close_button)
        
        layout.addLayout(close_layout)
    
    def load_relations(self):
        """Ładuje relacje osoby"""
        self.relations_list.clear()
        relations = self.db_manager.get_relations(self.person_id)
        
        for rel in relations:
            if rel['osoba1_id'] == self.person_id:
                other_name = f"{rel['osoba2_imie']} {rel['osoba2_nazwisko']}"
                relation_type = rel['rodzaj_relacji']
            else:
                other_name = f"{rel['osoba1_imie']} {rel['osoba1_nazwisko']}"
                # Odwróć relację dla wyświetlenia
                if rel['rodzaj_relacji'] == 'rodzic':
                    relation_type = 'dziecko'
                elif rel['rodzaj_relacji'] == 'dziecko':
                    relation_type = 'rodzic'
                else:
                    relation_type = rel['rodzaj_relacji']
            
            item = QListWidgetItem(f"{relation_type}: {other_name}")
            item.setData(Qt.ItemDataRole.UserRole, rel['id'])
            self.relations_list.addItem(item)
    
    def add_relation(self, relation_type):
        """
        Dodaje nową relację
        
        Args:
            relation_type: Typ relacji (rodzic, dziecko, małżonek)
        """
        from .person_selector_dialog import PersonSelectorDialog
        
        dialog = PersonSelectorDialog(self.db_manager, self.person_id, parent=self)
        if dialog.exec():
            selected_person_id = dialog.get_selected_person_id()
            if selected_person_id:
                try:
                    # Określ kierunek relacji
                    if relation_type == 'rodzic':
                        # Wybrana osoba jest rodzicem bieżącej osoby
                        self.db_manager.add_relation(selected_person_id, self.person_id, 'rodzic')
                    elif relation_type == 'dziecko':
                        # Bieżąca osoba jest rodzicem wybranej osoby
                        self.db_manager.add_relation(self.person_id, selected_person_id, 'rodzic')
                    else:
                        # Małżonek - relacja symetryczna
                        self.db_manager.add_relation(self.person_id, selected_person_id, relation_type)
                    
                    self.load_relations()
                    QMessageBox.information(self, "Sukces", "Relacja została dodana")
                except Exception as e:
                    QMessageBox.critical(self, "Błąd", f"Nie udało się dodać relacji: {str(e)}")
    
    def delete_relation(self):
        """Usuwa wybraną relację"""
        current_item = self.relations_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "Błąd", "Nie wybrano żadnej relacji")
            return
        
        relation_id = current_item.data(Qt.ItemDataRole.UserRole)
        
        reply = QMessageBox.question(
            self,
            "Potwierdzenie",
            "Czy na pewno chcesz usunąć tę relację?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.db_manager.delete_relation(relation_id)
                self.load_relations()
                QMessageBox.information(self, "Sukces", "Relacja została usunięta")
            except Exception as e:
                QMessageBox.critical(self, "Błąd", f"Nie udało się usunąć relacji: {str(e)}")
