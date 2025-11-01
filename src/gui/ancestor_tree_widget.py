"""
AncestorTreeWidget - Widget do wyświetlania drzewa przodków
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QPen, QBrush, QColor, QFont
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.patches as mpatches


class AncestorTreeWidget(QWidget):
    """Widget do wizualizacji drzewa przodków"""
    
    def __init__(self, db_manager, relationship_calc, parent=None):
        """
        Inicjalizacja widgetu
        
        Args:
            db_manager: Instancja DatabaseManager
            relationship_calc: Instancja RelationshipCalculator
            parent: Widget rodzica
        """
        super().__init__(parent)
        self.db_manager = db_manager
        self.relationship_calc = relationship_calc
        self.person_id = None
        
        self.init_ui()
    
    def init_ui(self):
        """Inicjalizacja interfejsu użytkownika"""
        layout = QVBoxLayout(self)
        
        # Etykieta informacyjna
        self.info_label = QLabel("Wybierz osobę z listy, aby wyświetlić drzewo przodków")
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.info_label)
        
        # Canvas matplotlib
        self.figure = Figure(figsize=(10, 8))
        self.canvas = FigureCanvas(self.figure)
        
        # Scroll area
        scroll = QScrollArea()
        scroll.setWidget(self.canvas)
        scroll.setWidgetResizable(True)
        layout.addWidget(scroll)
    
    def load_tree(self, person_id):
        """
        Ładuje i wyświetla drzewo przodków
        
        Args:
            person_id: ID osoby
        """
        self.person_id = person_id
        person = self.db_manager.get_person(person_id)
        
        if not person:
            return
        
        self.info_label.setText(f"Drzewo przodków: {person['imie']} {person['nazwisko']}")
        
        # Pobierz przodków
        ancestors = self.relationship_calc.get_ancestors(person_id, max_generations=5)
        
        # Wyczyść figurę
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        
        if not ancestors:
            ax.text(0.5, 0.5, 'Brak przodków w bazie danych',
                   ha='center', va='center', fontsize=12)
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.axis('off')
            self.canvas.draw()
            return
        
        # Organizacja przodków według pokoleń
        generations = {}
        for ancestor, generation in ancestors:
            if generation not in generations:
                generations[generation] = []
            generations[generation].append(ancestor)
        
        # Dodaj osobę bazową (generacja 0)
        generations[0] = [person]
        
        # Rysowanie drzewa
        max_generation = max(generations.keys())
        
        # Pozycje węzłów
        positions = {}
        
        for gen in range(max_generation + 1):
            persons_in_gen = generations.get(gen, [])
            count = len(persons_in_gen)
            
            for i, p in enumerate(persons_in_gen):
                x = (i + 1) / (count + 1)
                y = 1 - (gen / (max_generation + 1))
                positions[p['id']] = (x, y)
        
        # Rysowanie linii
        for gen in range(1, max_generation + 1):
            persons_in_gen = generations.get(gen, [])
            for p in persons_in_gen:
                children = self.relationship_calc.get_children(p['id'])
                for child in children:
                    if child['id'] in positions:
                        x1, y1 = positions[p['id']]
                        x2, y2 = positions[child['id']]
                        ax.plot([x1, x2], [y1, y2], 'k-', alpha=0.3, linewidth=1)
        
        # Rysowanie węzłów
        for gen in range(max_generation + 1):
            persons_in_gen = generations.get(gen, [])
            for p in persons_in_gen:
                x, y = positions[p['id']]
                
                # Kolor w zależności od płci
                if p.get('plec') == 'M':
                    color = 'lightblue'
                elif p.get('plec') == 'K':
                    color = 'pink'
                else:
                    color = 'lightgray'
                
                # Rysowanie prostokąta
                width = 0.12
                height = 0.06
                rect = mpatches.Rectangle((x - width/2, y - height/2), width, height,
                                         facecolor=color, edgecolor='black', linewidth=1.5)
                ax.add_patch(rect)
                
                # Tekst
                name = f"{p['imie']} {p['nazwisko']}"
                birth_year = p['data_urodzenia'].split('-')[0] if p.get('data_urodzenia') else '?'
                
                ax.text(x, y, f"{name}\n({birth_year})",
                       ha='center', va='center', fontsize=8, weight='bold')
        
        ax.set_xlim(-0.1, 1.1)
        ax.set_ylim(-0.1, 1.1)
        ax.axis('off')
        ax.set_aspect('equal')
        
        self.figure.tight_layout()
        self.canvas.draw()
