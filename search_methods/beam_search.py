from typing import Tuple

from search_methods.utils import *
from sokoban.map import Map
from sokoban.moves import *
from search_methods.lrta_star import *

def beam_search(
        s: Map,
        K: int,
        h: callable,
        c: callable
    ) -> Tuple[List[Map], int, int]:
    steps = 0
    pulls = 0

    visited = StateDict(hash)
    s_list = [(s, float('inf'))]

    while True:
        cand_list = []
        for crt_s, _ in s_list:
            moves = crt_s.filter_possible_moves()
            for move in moves:
                new_s = result(crt_s, move)
                if new_s in visited:
                    continue

                cand_list.append((new_s, h(new_s) + c(crt_s, move, new_s)))
                visited[new_s] = 1

            for (test, h_value) in cand_list:
                if test.is_solved():
                    # Skip saving all the states, for beam_search the rpresentation is not
                    # very useful
                    return [test], steps, pulls

        cand_list.sort(key=lambda x: x[1])

        # Make sure that the selected candidates are unique
        s_list = []
        for cand in cand_list:
            if hash(cand[0]) not in [hash(s) for s, _ in s_list]:
                s_list.append(cand)

        s_list = s_list[:K]

        steps += len(s_list)
