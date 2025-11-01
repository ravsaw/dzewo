"""
RelationshipCalculator - Oblicza relacje między osobami w drzewie genealogicznym
"""

from typing import List, Dict, Set, Optional, Tuple
from collections import deque


class RelationshipCalculator:
    """Oblicza relacje i zależności między osobami w drzewie genealogicznym"""
    
    def __init__(self, db_manager):
        """
        Inicjalizacja kalkulatora relacji
        
        Args:
            db_manager: Instancja DatabaseManager
        """
        self.db_manager = db_manager
    
    def get_parents(self, person_id: int) -> List[dict]:
        """
        Pobiera rodziców osoby
        
        Args:
            person_id: ID osoby
            
        Returns:
            Lista rodziców
        """
        parents = []
        relations = self.db_manager.get_relations(person_id)
        
        for rel in relations:
            if rel['rodzaj_relacji'] == 'rodzic' and rel['osoba2_id'] == person_id:
                parent = self.db_manager.get_person(rel['osoba1_id'])
                if parent:
                    parents.append(parent)
            elif rel['rodzaj_relacji'] == 'dziecko' and rel['osoba1_id'] == person_id:
                parent = self.db_manager.get_person(rel['osoba2_id'])
                if parent:
                    parents.append(parent)
        
        return parents
    
    def get_children(self, person_id: int) -> List[dict]:
        """
        Pobiera dzieci osoby
        
        Args:
            person_id: ID osoby
            
        Returns:
            Lista dzieci
        """
        children = []
        relations = self.db_manager.get_relations(person_id)
        
        for rel in relations:
            if rel['rodzaj_relacji'] == 'rodzic' and rel['osoba1_id'] == person_id:
                child = self.db_manager.get_person(rel['osoba2_id'])
                if child:
                    children.append(child)
            elif rel['rodzaj_relacji'] == 'dziecko' and rel['osoba2_id'] == person_id:
                child = self.db_manager.get_person(rel['osoba1_id'])
                if child:
                    children.append(child)
        
        return children
    
    def get_spouse(self, person_id: int) -> Optional[dict]:
        """
        Pobiera małżonka osoby
        
        Args:
            person_id: ID osoby
            
        Returns:
            Małżonek lub None
        """
        relations = self.db_manager.get_relations(person_id)
        
        for rel in relations:
            if rel['rodzaj_relacji'] == 'małżonek':
                if rel['osoba1_id'] == person_id:
                    return self.db_manager.get_person(rel['osoba2_id'])
                elif rel['osoba2_id'] == person_id:
                    return self.db_manager.get_person(rel['osoba1_id'])
        
        return None
    
    def get_siblings(self, person_id: int) -> List[dict]:
        """
        Pobiera rodzeństwo osoby
        
        Args:
            person_id: ID osoby
            
        Returns:
            Lista rodzeństwa
        """
        siblings = []
        parents = self.get_parents(person_id)
        
        for parent in parents:
            children = self.get_children(parent['id'])
            for child in children:
                if child['id'] != person_id and child not in siblings:
                    siblings.append(child)
        
        return siblings
    
    def get_ancestors(self, person_id: int, max_generations: int = 10) -> List[Tuple[dict, int]]:
        """
        Pobiera wszystkich przodków osoby
        
        Args:
            person_id: ID osoby
            max_generations: Maksymalna liczba pokoleń do sprawdzenia
            
        Returns:
            Lista krotek (osoba, pokolenie)
        """
        ancestors = []
        visited = set()
        queue = deque([(person_id, 0)])
        
        while queue and max_generations > 0:
            current_id, generation = queue.popleft()
            
            if current_id in visited or generation >= max_generations:
                continue
            
            visited.add(current_id)
            parents = self.get_parents(current_id)
            
            for parent in parents:
                if parent['id'] not in visited:
                    ancestors.append((parent, generation + 1))
                    queue.append((parent['id'], generation + 1))
        
        return ancestors
    
    def get_descendants(self, person_id: int, max_generations: int = 10) -> List[Tuple[dict, int]]:
        """
        Pobiera wszystkich potomków osoby
        
        Args:
            person_id: ID osoby
            max_generations: Maksymalna liczba pokoleń do sprawdzenia
            
        Returns:
            Lista krotek (osoba, pokolenie)
        """
        descendants = []
        visited = set()
        queue = deque([(person_id, 0)])
        
        while queue and max_generations > 0:
            current_id, generation = queue.popleft()
            
            if current_id in visited or generation >= max_generations:
                continue
            
            visited.add(current_id)
            children = self.get_children(current_id)
            
            for child in children:
                if child['id'] not in visited:
                    descendants.append((child, generation + 1))
                    queue.append((child['id'], generation + 1))
        
        return descendants
    
    def find_relationship_path(self, person1_id: int, person2_id: int) -> Optional[List[dict]]:
        """
        Znajduje najkrótszą ścieżkę relacji między dwiema osobami
        
        Args:
            person1_id: ID pierwszej osoby
            person2_id: ID drugiej osoby
            
        Returns:
            Lista osób na ścieżce lub None jeśli nie ma połączenia
        """
        if person1_id == person2_id:
            person = self.db_manager.get_person(person1_id)
            return [person] if person else None
        
        visited = set()
        queue = deque([(person1_id, [person1_id])])
        
        while queue:
            current_id, path = queue.popleft()
            
            if current_id in visited:
                continue
            
            visited.add(current_id)
            
            # Sprawdź wszystkie połączone osoby
            related_persons = []
            related_persons.extend(self.get_parents(current_id))
            related_persons.extend(self.get_children(current_id))
            spouse = self.get_spouse(current_id)
            if spouse:
                related_persons.append(spouse)
            
            for related in related_persons:
                if related['id'] == person2_id:
                    # Znaleziono ścieżkę
                    full_path = []
                    for pid in path + [person2_id]:
                        person = self.db_manager.get_person(pid)
                        if person:
                            full_path.append(person)
                    return full_path
                
                if related['id'] not in visited:
                    queue.append((related['id'], path + [related['id']]))
        
        return None
    
    def calculate_relation_degree(self, person1_id: int, person2_id: int) -> Optional[str]:
        """
        Oblicza stopień pokrewieństwa między dwiema osobami
        
        Args:
            person1_id: ID pierwszej osoby
            person2_id: ID drugiej osoby
            
        Returns:
            Opis relacji lub None jeśli osoby nie są spokrewnione
        """
        path = self.find_relationship_path(person1_id, person2_id)
        
        if not path or len(path) < 2:
            return None
        
        if len(path) == 2:
            # Bezpośrednia relacja
            relations = self.db_manager.get_relations(person1_id)
            for rel in relations:
                if (rel['osoba1_id'] == person2_id or rel['osoba2_id'] == person2_id):
                    return rel['rodzaj_relacji']
        
        # Pośrednia relacja
        distance = len(path) - 1
        
        # Sprawdź czy to relacja w linii prostej (przodek-potomek)
        is_ancestor = all(
            p2['id'] in [c['id'] for c in self.get_children(p1['id'])]
            for p1, p2 in zip(path[:-1], path[1:])
        )
        
        if is_ancestor:
            if distance == 2:
                return "wnuk/wnuczka"
            elif distance == 3:
                return "prawnuk/prawnuczka"
            else:
                return f"potomek ({distance} pokoleń)"
        
        is_descendant = all(
            p2['id'] in [p['id'] for p in self.get_parents(p1['id'])]
            for p1, p2 in zip(path[:-1], path[1:])
        )
        
        if is_descendant:
            if distance == 2:
                return "dziadek/babcia"
            elif distance == 3:
                return "pradziadek/prababcia"
            else:
                return f"przodek ({distance} pokoleń)"
        
        # Inne relacje
        return f"krewny ({distance} stopni oddalenia)"
