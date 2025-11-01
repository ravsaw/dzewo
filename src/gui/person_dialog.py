"""
PersonDialog - Dialog do edycji danych osoby
"""

from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
                            QLineEdit, QTextEdit, QDateEdit, QComboBox,
                            QPushButton, QLabel, QFileDialog, QMessageBox)
from PyQt6.QtCore import QDate, Qt
from PyQt6.QtGui import QPixmap
import os
import shutil


class PersonDialog(QDialog):
    """Dialog do dodawania i edycji danych osoby"""
    
    def __init__(self, db_manager, person_id=None, parent=None):
        """
        Inicjalizacja dialogu
        
        Args:
            db_manager: Instancja DatabaseManager
            person_id: ID osoby do edycji (None dla nowej osoby)
            parent: Widget rodzica
        """
        super().__init__(parent)
        self.db_manager = db_manager
        self.person_id = person_id
        self.photo_path = None
        
        self.init_ui()
        
        if person_id:
            self.load_person_data()
    
    def init_ui(self):
        """Inicjalizacja interfejsu użytkownika"""
        title = "Edytuj osobę" if self.person_id else "Dodaj osobę"
        self.setWindowTitle(title)
        self.setMinimumWidth(500)
        
        layout = QVBoxLayout(self)
        
        # Formularz
        form_layout = QFormLayout()
        
        # Imię
        self.imie_edit = QLineEdit()
        form_layout.addRow("Imię*:", self.imie_edit)
        
        # Nazwisko
        self.nazwisko_edit = QLineEdit()
        form_layout.addRow("Nazwisko*:", self.nazwisko_edit)
        
        # Płeć
        self.plec_combo = QComboBox()
        self.plec_combo.addItems(["", "M", "K"])
        form_layout.addRow("Płeć:", self.plec_combo)
        
        # Data urodzenia
        self.data_urodzenia_edit = QDateEdit()
        self.data_urodzenia_edit.setCalendarPopup(True)
        self.data_urodzenia_edit.setDate(QDate.currentDate())
        self.data_urodzenia_edit.setDisplayFormat("yyyy-MM-dd")
        self.data_urodzenia_check = QComboBox()
        self.data_urodzenia_check.addItems(["Brak", "Znana"])
        self.data_urodzenia_check.currentTextChanged.connect(self.toggle_birth_date)
        form_layout.addRow("Data urodzenia:", self.data_urodzenia_check)
        form_layout.addRow("", self.data_urodzenia_edit)
        self.data_urodzenia_edit.setEnabled(False)
        
        # Data śmierci
        self.data_smierci_edit = QDateEdit()
        self.data_smierci_edit.setCalendarPopup(True)
        self.data_smierci_edit.setDate(QDate.currentDate())
        self.data_smierci_edit.setDisplayFormat("yyyy-MM-dd")
        self.data_smierci_check = QComboBox()
        self.data_smierci_check.addItems(["Żyje", "Zmarła"])
        self.data_smierci_check.currentTextChanged.connect(self.toggle_death_date)
        form_layout.addRow("Status:", self.data_smierci_check)
        form_layout.addRow("Data śmierci:", self.data_smierci_edit)
        self.data_smierci_edit.setEnabled(False)
        
        # Miejsce urodzenia
        self.miejsce_urodzenia_edit = QLineEdit()
        form_layout.addRow("Miejsce urodzenia:", self.miejsce_urodzenia_edit)
        
        # Miejsce śmierci
        self.miejsce_smierci_edit = QLineEdit()
        form_layout.addRow("Miejsce śmierci:", self.miejsce_smierci_edit)
        
        # Zdjęcie
        photo_layout = QHBoxLayout()
        self.photo_label = QLabel("Brak zdjęcia")
        self.photo_label.setFixedSize(100, 100)
        self.photo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.photo_label.setStyleSheet("border: 1px solid gray;")
        photo_layout.addWidget(self.photo_label)
        
        self.photo_button = QPushButton("Wybierz zdjęcie")
        self.photo_button.clicked.connect(self.choose_photo)
        photo_layout.addWidget(self.photo_button)
        photo_layout.addStretch()
        
        form_layout.addRow("Zdjęcie:", photo_layout)
        
        # Notatki
        self.notatki_edit = QTextEdit()
        self.notatki_edit.setMaximumHeight(100)
        form_layout.addRow("Notatki:", self.notatki_edit)
        
        layout.addLayout(form_layout)
        
        # Przyciski
        button_layout = QHBoxLayout()
        
        self.save_button = QPushButton("Zapisz")
        self.save_button.clicked.connect(self.save_person)
        button_layout.addWidget(self.save_button)
        
        self.cancel_button = QPushButton("Anuluj")
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)
        
        layout.addLayout(button_layout)
    
    def toggle_birth_date(self, text):
        """Włącza/wyłącza pole daty urodzenia"""
        self.data_urodzenia_edit.setEnabled(text == "Znana")
    
    def toggle_death_date(self, text):
        """Włącza/wyłącza pole daty śmierci"""
        self.data_smierci_edit.setEnabled(text == "Zmarła")
    
    def choose_photo(self):
        """Wybiera zdjęcie osoby"""
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Wybierz zdjęcie",
            "",
            "Obrazy (*.png *.jpg *.jpeg *.bmp);;Wszystkie pliki (*)"
        )
        
        if filename:
            self.photo_path = filename
            pixmap = QPixmap(filename)
            scaled_pixmap = pixmap.scaled(
                100, 100,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.photo_label.setPixmap(scaled_pixmap)
    
    def load_person_data(self):
        """Ładuje dane osoby do edycji"""
        person = self.db_manager.get_person(self.person_id)
        if not person:
            return
        
        self.imie_edit.setText(person['imie'])
        self.nazwisko_edit.setText(person['nazwisko'])
        
        if person['plec']:
            index = self.plec_combo.findText(person['plec'])
            if index >= 0:
                self.plec_combo.setCurrentIndex(index)
        
        if person['data_urodzenia']:
            self.data_urodzenia_check.setCurrentText("Znana")
            date = QDate.fromString(person['data_urodzenia'], "yyyy-MM-dd")
            self.data_urodzenia_edit.setDate(date)
        
        if person['data_smierci']:
            self.data_smierci_check.setCurrentText("Zmarła")
            date = QDate.fromString(person['data_smierci'], "yyyy-MM-dd")
            self.data_smierci_edit.setDate(date)
        
        if person['miejsce_urodzenia']:
            self.miejsce_urodzenia_edit.setText(person['miejsce_urodzenia'])
        
        if person['miejsce_smierci']:
            self.miejsce_smierci_edit.setText(person['miejsce_smierci'])
        
        if person['notatki']:
            self.notatki_edit.setText(person['notatki'])
        
        if person['zdjecie_sciezka'] and os.path.exists(person['zdjecie_sciezka']):
            self.photo_path = person['zdjecie_sciezka']
            pixmap = QPixmap(person['zdjecie_sciezka'])
            scaled_pixmap = pixmap.scaled(
                100, 100,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.photo_label.setPixmap(scaled_pixmap)
    
    def save_person(self):
        """Zapisuje dane osoby"""
        imie = self.imie_edit.text().strip()
        nazwisko = self.nazwisko_edit.text().strip()
        
        if not imie or not nazwisko:
            QMessageBox.warning(self, "Błąd", "Imię i nazwisko są wymagane")
            return
        
        plec = self.plec_combo.currentText() if self.plec_combo.currentText() else None
        
        data_urodzenia = None
        if self.data_urodzenia_check.currentText() == "Znana":
            data_urodzenia = self.data_urodzenia_edit.date().toString("yyyy-MM-dd")
        
        data_smierci = None
        if self.data_smierci_check.currentText() == "Zmarła":
            data_smierci = self.data_smierci_edit.date().toString("yyyy-MM-dd")
        
        miejsce_urodzenia = self.miejsce_urodzenia_edit.text().strip() or None
        miejsce_smierci = self.miejsce_smierci_edit.text().strip() or None
        notatki = self.notatki_edit.toPlainText().strip() or None
        
        # Kopiuj zdjęcie do katalogu data/photos
        zdjecie_sciezka = None
        if self.photo_path and os.path.exists(self.photo_path):
            try:
                photos_dir = os.path.join('data', 'photos')
                os.makedirs(photos_dir, exist_ok=True)
                
                filename = os.path.basename(self.photo_path)
                dest_path = os.path.join(photos_dir, filename)
                
                # Jeśli plik już istnieje i nie jest tym samym plikiem
                if self.photo_path != dest_path:
                    shutil.copy2(self.photo_path, dest_path)
                
                zdjecie_sciezka = dest_path
            except Exception as e:
                QMessageBox.warning(self, "Ostrzeżenie", f"Nie udało się skopiować zdjęcia: {str(e)}")
        
        try:
            if self.person_id:
                # Edycja istniejącej osoby
                self.db_manager.update_person(
                    self.person_id, imie, nazwisko, data_urodzenia, data_smierci,
                    plec, miejsce_urodzenia, miejsce_smierci, notatki, zdjecie_sciezka
                )
            else:
                # Dodanie nowej osoby
                self.db_manager.add_person(
                    imie, nazwisko, data_urodzenia, data_smierci,
                    plec, miejsce_urodzenia, miejsce_smierci, notatki, zdjecie_sciezka
                )
            
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Błąd", f"Nie udało się zapisać danych: {str(e)}")
