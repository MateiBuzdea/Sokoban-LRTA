from typing import Tuple, Optional, List
from collections import defaultdict

from sokoban.map import Map
from sokoban.moves import *

from search_methods.heuristics import *
from search_methods.utils import *

def lrta_star_agent(
        s: Map,
        h: callable,
        c: callable,
        H: StateDict,
        s_prev: Optional[Map] = None,
        visited: Optional[dict] = None,
    ) -> int:
    """Returns the action to execute in the current state of the map using the LRTA* algorithm."""

    def _cost(s: Map, a: str, s_prime: Optional[Map]):
        """Returns the cost of executing action a in state s."""
        if s_prime is None or s_prime not in H:
            s_prime = result(s, a)
            return h(s_prime, visited) + c(s, a, s_prime, visited)

        return c(s, a, s_prime, visited) + H[s_prime] + 50

    if s.is_solved():
        return None
    
    if s not in H:
        H[s] = h(s, visited)

    if s_prev:
        H[s_prev] = min([_cost(s_prev, b, result(s_prev, b)) for b in s_prev.filter_possible_moves()])

    a = min([b for b in s.filter_possible_moves()], key=lambda b: _cost(s, b, result(s, b)))

    moved_box = box_was_moved(s_prev, s)
    if moved_box:
        # If a box was moved, update the heuristic for the new state
        visited[(moved_box.name, moved_box.xy)] += 1

    return a

def lrta_star(
        s: Map,
        h: Optional[callable] = h3,
        c: Optional[callable] = c3
    ) -> Tuple[List[Map], int, int]:
    """Solves the map using the LRTA* algorithm."""

    count = 0
    pulls = 0
    s_prev = s.copy()
    H = StateDict(hash)
    visited = defaultdict(lambda: 0)
    states = [s.copy()]

    while True:
        a = lrta_star_agent(s, h, c, H, s_prev, visited)
        if a is None:
            break

        s_prev = s.copy()
        s.apply_move(a)

        if box_was_pulled(s_prev, s):
            pulls += 1

        states.append(s.copy())
        count += 1

    return states, count, pulls
