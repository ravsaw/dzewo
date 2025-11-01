"""
FullTreeWidget - Widget do wyświetlania pełnego drzewa genealogicznego
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QPen, QBrush, QColor, QFont
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.patches as mpatches


class FullTreeWidget(QWidget):
    """Widget do wizualizacji pełnego drzewa genealogicznego"""
    
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
        
        self.init_ui()
    
    def init_ui(self):
        """Inicjalizacja interfejsu użytkownika"""
        layout = QVBoxLayout(self)
        
        # Etykieta informacyjna
        self.info_label = QLabel("Pełne drzewo genealogiczne - wszystkie osoby i relacje")
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.info_label)
        
        # Canvas matplotlib
        self.figure = Figure(figsize=(14, 10))
        self.canvas = FigureCanvas(self.figure)
        
        # Scroll area
        scroll = QScrollArea()
        scroll.setWidget(self.canvas)
        scroll.setWidgetResizable(True)
        layout.addWidget(scroll)
        
        # Załaduj drzewo przy inicjalizacji
        self.load_tree()
    
    def load_tree(self):
        """
        Ładuje i wyświetla pełne drzewo genealogiczne
        """
        # Pobierz wszystkie osoby i relacje
        all_persons = self.db_manager.get_all_persons()
        all_relations = self.db_manager.get_all_relations()
        
        # Wyczyść figurę
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        
        if not all_persons:
            ax.text(0.5, 0.5, 'Brak osób w bazie danych',
                   ha='center', va='center', fontsize=12)
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.axis('off')
            self.canvas.draw()
            return
        
        # Znajdź osoby bez rodziców (osoby startowe)
        persons_with_parents = set()
        for rel in all_relations:
            if rel['rodzaj_relacji'] == 'dziecko':
                persons_with_parents.add(rel['osoba1_id'])
        
        root_persons = [p for p in all_persons if p['id'] not in persons_with_parents]
        
        if not root_persons:
            # Jeśli wszystkie mają rodziców, wybierz najstarszą osobę
            root_persons = sorted(all_persons, 
                                 key=lambda p: p.get('data_urodzenia') or '9999-99-99')[:1]
        
        # Organizacja osób według pokoleń i rodzin
        generations = self._organize_by_generations(root_persons, all_relations)
        
        # Pozycje węzłów
        positions = self._calculate_positions(generations)
        
        # Rysowanie linii połączeń
        self._draw_connections(ax, positions, all_relations)
        
        # Rysowanie węzłów
        self._draw_nodes(ax, positions, generations)
        
        # Ustawienia osi
        if positions:
            all_x = [pos[0] for pos in positions.values()]
            all_y = [pos[1] for pos in positions.values()]
            margin = 0.1
            ax.set_xlim(min(all_x) - margin, max(all_x) + margin)
            ax.set_ylim(min(all_y) - margin, max(all_y) + margin)
        
        ax.axis('off')
        ax.set_aspect('equal')
        
        # Informacja o liczbie osób
        person_count = len(all_persons)
        self.info_label.setText(f"Pełne drzewo genealogiczne - {person_count} osób")
        
        self.figure.tight_layout()
        self.canvas.draw()
    
    def _organize_by_generations(self, root_persons, relations):
        """
        Organizuje osoby według pokoleń
        
        Args:
            root_persons: Lista osób bez rodziców
            relations: Wszystkie relacje
            
        Returns:
            Słownik: generacja -> lista osób
        """
        generations = {0: root_persons}
        processed = set(p['id'] for p in root_persons)
        
        # Buduj słownik relacji dla szybkiego dostępu
        children_map = {}
        for rel in relations:
            if rel['rodzaj_relacji'] == 'rodzic':
                if rel['osoba1_id'] not in children_map:
                    children_map[rel['osoba1_id']] = []
                children_map[rel['osoba1_id']].append(rel['osoba2_id'])
        
        # Przetwarzaj pokolenia
        gen = 0
        while True:
            current_gen = generations.get(gen, [])
            if not current_gen:
                break
            
            next_gen = []
            for person in current_gen:
                children_ids = children_map.get(person['id'], [])
                for child_id in children_ids:
                    if child_id not in processed:
                        child = self.db_manager.get_person(child_id)
                        if child:
                            next_gen.append(child)
                            processed.add(child_id)
            
            if next_gen:
                generations[gen + 1] = next_gen
                gen += 1
            else:
                break
        
        return generations
    
    def _calculate_positions(self, generations):
        """
        Oblicza pozycje węzłów na wykresie
        
        Args:
            generations: Słownik: generacja -> lista osób
            
        Returns:
            Słownik: person_id -> (x, y)
        """
        positions = {}
        max_generation = max(generations.keys()) if generations else 0
        
        for gen, persons in generations.items():
            count = len(persons)
            for i, person in enumerate(persons):
                # Pozycja x: rozłożenie równomierne
                if count == 1:
                    x = 0.5
                else:
                    x = i / (count - 1)
                
                # Pozycja y: od góry do dołu
                y = 1 - (gen / (max_generation + 1)) if max_generation > 0 else 0.5
                
                positions[person['id']] = (x, y)
        
        return positions
    
    def _draw_connections(self, ax, positions, relations):
        """
        Rysuje linie połączeń między osobami
        
        Args:
            ax: Matplotlib axes
            positions: Słownik pozycji
            relations: Lista relacji
        """
        # Rysuj relacje rodzic-dziecko
        for rel in relations:
            if rel['rodzaj_relacji'] == 'rodzic':
                parent_id = rel['osoba1_id']
                child_id = rel['osoba2_id']
                
                if parent_id in positions and child_id in positions:
                    x1, y1 = positions[parent_id]
                    x2, y2 = positions[child_id]
                    ax.plot([x1, x2], [y1, y2], 'k-', alpha=0.3, linewidth=1.5)
        
        # Rysuj relacje małżeńskie
        for rel in relations:
            if rel['rodzaj_relacji'] == 'małżonek':
                spouse1_id = rel['osoba1_id']
                spouse2_id = rel['osoba2_id']
                
                if spouse1_id in positions and spouse2_id in positions:
                    x1, y1 = positions[spouse1_id]
                    x2, y2 = positions[spouse2_id]
                    ax.plot([x1, x2], [y1, y2], 'r-', alpha=0.5, linewidth=2, linestyle='--')
    
    def _draw_nodes(self, ax, positions, generations):
        """
        Rysuje węzły reprezentujące osoby
        
        Args:
            ax: Matplotlib axes
            positions: Słownik pozycji
            generations: Słownik pokoleń
        """
        for gen, persons in generations.items():
            for person in persons:
                if person['id'] not in positions:
                    continue
                    
                x, y = positions[person['id']]
                
                # Kolor w zależności od płci
                if person.get('plec') == 'M':
                    color = 'lightblue'
                elif person.get('plec') == 'K':
                    color = 'pink'
                else:
                    color = 'lightgray'
                
                # Rysowanie prostokąta
                width = 0.08
                height = 0.05
                rect = mpatches.Rectangle((x - width/2, y - height/2), width, height,
                                         facecolor=color, edgecolor='black', linewidth=1.5)
                ax.add_patch(rect)
                
                # Tekst
                name = f"{person['imie']} {person['nazwisko']}"
                if person.get('nazwisko_panienskie'):
                    name += f"\n({person['nazwisko_panienskie']})"
                
                birth_year = person['data_urodzenia'][:4] if person.get('data_urodzenia') else '?'
                
                # Skrócony tekst dla małych węzłów
                ax.text(x, y, f"{person['imie']}\n{person['nazwisko']}\n({birth_year})",
                       ha='center', va='center', fontsize=7, weight='bold')
