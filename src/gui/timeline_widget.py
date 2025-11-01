"""
TimelineWidget - Widget do wizualizacji osi czasu
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea
from PyQt6.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.patches as mpatches
from datetime import datetime


class TimelineWidget(QWidget):
    """Widget do wizualizacji osi czasu życia osób"""
    
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
    
    def init_ui(self):
        """Inicjalizacja interfejsu użytkownika"""
        layout = QVBoxLayout(self)
        
        # Etykieta informacyjna
        self.info_label = QLabel("Oś czasu - wizualizacja życia osób")
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.info_label)
        
        # Canvas matplotlib
        self.figure = Figure(figsize=(12, 8))
        self.canvas = FigureCanvas(self.figure)
        
        # Scroll area
        scroll = QScrollArea()
        scroll.setWidget(self.canvas)
        scroll.setWidgetResizable(True)
        layout.addWidget(scroll)
    
    def load_timeline(self):
        """Ładuje i wyświetla oś czasu"""
        persons = self.db_manager.get_all_persons()
        
        # Wyczyść figurę
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        
        if not persons:
            ax.text(0.5, 0.5, 'Brak osób w bazie danych',
                   ha='center', va='center', fontsize=12)
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.axis('off')
            self.canvas.draw()
            return
        
        # Filtruj osoby z datami urodzenia
        persons_with_dates = []
        for p in persons:
            if p.get('data_urodzenia'):
                try:
                    birth_year = int(p['data_urodzenia'].split('-')[0])
                    death_year = None
                    if p.get('data_smierci'):
                        death_year = int(p['data_smierci'].split('-')[0])
                    else:
                        death_year = datetime.now().year
                    
                    persons_with_dates.append({
                        'person': p,
                        'birth_year': birth_year,
                        'death_year': death_year
                    })
                except (ValueError, IndexError):
                    pass
        
        if not persons_with_dates:
            ax.text(0.5, 0.5, 'Brak osób z datami urodzenia',
                   ha='center', va='center', fontsize=12)
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.axis('off')
            self.canvas.draw()
            return
        
        # Sortuj osoby według roku urodzenia
        persons_with_dates.sort(key=lambda x: x['birth_year'])
        
        # Znajdź zakres lat
        min_year = min(p['birth_year'] for p in persons_with_dates)
        max_year = max(p['death_year'] for p in persons_with_dates)
        
        # Dodaj margines
        year_margin = max(10, (max_year - min_year) * 0.05)
        min_year -= year_margin
        max_year += year_margin
        
        # Rysowanie osi czasu
        y_pos = 0
        y_spacing = 1
        
        for data in persons_with_dates:
            p = data['person']
            birth_year = data['birth_year']
            death_year = data['death_year']
            
            # Kolor w zależności od płci
            if p.get('plec') == 'M':
                color = 'lightblue'
            elif p.get('plec') == 'K':
                color = 'pink'
            else:
                color = 'lightgray'
            
            # Rysowanie linii życia
            ax.barh(y_pos, death_year - birth_year, left=birth_year,
                   height=0.5, color=color, edgecolor='black', linewidth=0.5)
            
            # Etykieta
            name = f"{p['imie']} {p['nazwisko']}"
            ax.text(min_year - 5, y_pos, name,
                   va='center', ha='right', fontsize=8)
            
            # Lata
            years_text = f"{birth_year}"
            if p.get('data_smierci'):
                years_text += f"-{death_year}"
            else:
                years_text += "-"
            
            ax.text(max_year + 5, y_pos, years_text,
                   va='center', ha='left', fontsize=7, style='italic')
            
            y_pos += y_spacing
        
        # Ustawienia osi
        ax.set_xlim(min_year - 50, max_year + 50)
        ax.set_ylim(-y_spacing, y_pos)
        ax.set_xlabel('Rok', fontsize=10)
        ax.set_yticks([])
        ax.grid(True, axis='x', alpha=0.3)
        ax.set_title('Oś czasu życia osób', fontsize=12, weight='bold')
        
        self.figure.tight_layout()
        self.canvas.draw()
        
        self.info_label.setText(f"Oś czasu - {len(persons_with_dates)} osób")
