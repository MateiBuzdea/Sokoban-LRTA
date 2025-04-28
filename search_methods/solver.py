import time
from typing import Tuple, List

from sokoban.map import Map
from search_methods.lrta_star import lrta_star
from search_methods.beam_search import beam_search

from search_methods.heuristics import h3, c3


class Solver:
    """Solver class that uses different search algorithms to solve the map."""

    def __init__(self, map: Map, algorithm: str) -> None:
        self.algorithm = algorithm
        self.map = map
        self.h = h3
        self.c = c3
        self.K = 6  # Beam search parameter

        if algorithm not in ['lrta_star', 'beam_search']:
            raise ValueError(f"Unknown algorithm: {algorithm}")

    def solve(self, display = False) -> Tuple[List[Map], int, float, int]:
        """Solves the map using the selected algorithm."""
        start_time = time.time()

        if self.algorithm == 'beam_search':
            fun = beam_search
            args = (self.K, self.h, self.c)
        else:
            fun = lrta_star
            args = (self.h, self.c)

        states, count, pulls = fun(self.map.copy(), *args)
        end_time = time.time()

        duration = end_time - start_time

        if display:
            print(f"Algorithm: {self.algorithm}")
            print(f"States explored: {count}")
            print(f"Duration: {duration:.4f} seconds")
            print(f"Pulls: {pulls}")
            print(f"Solution found: {states[-1].is_solved()}")

        return states, count, duration, pulls
