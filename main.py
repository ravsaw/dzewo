#!/usr/bin/env python3
"""
Drzewo Genealogiczne - Aplikacja Desktopowa
Główny punkt wejścia aplikacji
"""

import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from src.gui.main_window import MainWindow
from src.database.db_manager import DatabaseManager

def main():
    """Główna funkcja uruchamiająca aplikację"""
    
    # Tworzenie katalogu data jeśli nie istnieje
    if not os.path.exists('data'):
        os.makedirs('data')
    
    if not os.path.exists('data/photos'):
        os.makedirs('data/photos')
    
    # Inicjalizacja aplikacji
    app = QApplication(sys.argv)
    app.setApplicationName("Drzewo Genealogiczne")
    app.setOrganizationName("DzevoApp")
    app.setOrganizationDomain("dzewo.app")
    
    # Inicjalizacja bazy danych
    db_path = os.path.join('data', 'family_tree.db')
    db_manager = DatabaseManager(db_path)
    
    # Utworzenie i wyświetlenie głównego okna
    window = MainWindow(db_manager)
    window.show()
    
    # Uruchomienie pętli zdarzeń
    exit_code = app.exec()
    
    # Zamknięcie połączenia z bazą danych
    db_manager.close()
    
    sys.exit(exit_code)

if __name__ == "__main__":
    main()