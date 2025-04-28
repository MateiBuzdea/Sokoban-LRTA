from typing import Tuple
from collections import defaultdict

from sokoban.map import Map
from sokoban.dummy import Dummy
from sokoban.box import Box
from sokoban.moves import *

from search_methods.utils import *


class StateDict:
    """A dictionary that stores the state of the map"""
    def __init__(self, function: callable):
        self.state = defaultdict(lambda: 0)
        self.function = function

    def __getitem__(self, key):
        return self.state[self.function(key)]

    def __setitem__(self, key, value):
        self.state[self.function(key)] = value

    def __contains__(self, key):
        return self.function(key) in self.state and self.state[self.function(key)] != 0

    def __delitem__(self, key):
        del self.state[self.function(key)]

    def __len__(self):
        return len(self.state)
    
    def __iter__(self):
        return iter(self.state)
    
    def __str__(self):
        return str(self.state)


def get_boxes_and_goals(s: Map):
    """Returns a list of boxes and a list of goals not yet satisfied"""
    boxes_to_check = list(s.boxes.values()).copy()
    targets_remaining = s.targets.copy()

    for box in s.boxes.values():
        if box.xy in s.targets:
            boxes_to_check.remove(box)
            targets_remaining.remove(box.xy)

    return boxes_to_check, targets_remaining

def manhattan(a: Dummy | Tuple, b: Dummy | Tuple) -> int:
    """Returns the manhattan distance between two points"""
    if isinstance(a, Dummy):
        a = a.xy
    if isinstance(b, Dummy):
        b = b.xy
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def sign(x: int) -> int:
    """Returns the sign of a number"""
    return 1 if x > 0 else -1 if x < 0 else 0

def corner(pos: Dummy | Tuple, walls: list[Tuple[int, int]]) -> bool:
    """Returns True if the position is a corner"""
    if isinstance(pos, Dummy):
        pos = pos.xy
    x, y = pos
    return ((x - 1, y) in walls and (x, y - 1) in walls) or \
           ((x + 1, y) in walls and (x, y - 1) in walls) or \
           ((x - 1, y) in walls and (x, y + 1) in walls) or \
           ((x + 1, y) in walls and (x, y + 1) in walls)

def get_walls(s: Map) -> list[Tuple[int, int]]:
    """Returns the walls of the map including the borders"""
    walls = s.obstacles.copy()
    walls += [(-1, y) for y in range(s.width)]
    walls += [(s.length, y) for y in range(s.width)]
    walls += [(x, -1) for x in range(s.length)]
    walls += [(x, s.width) for x in range(s.length)]

    return walls

def box_was_moved(s: Map, s_prime: Map) -> Box:
    """Returns the box that was moved"""
    s_pos = s.boxes.values()
    s_prime_pos = s_prime.boxes.values()

    for box in s_prime_pos:
        if box.xy not in [b.xy for b in s_pos]:
            return box
    return None
            
def box_was_pulled(s: Map, s_prime: Map) -> bool:
    """Returns True if a box was pulled"""
    player_pos = (s.player.x, s.player.y)
    for box in s_prime.boxes.values():
        if player_pos == box.xy:
            return True
    return False

def box_reached_goal(s: Map, s_prime: Map) -> bool:
    """Returns True if a box reached a goal"""
    s_boxes, _ = get_boxes_and_goals(s)
    s_prime_boxes, _ = get_boxes_and_goals(s_prime)

    if len(s_boxes) > len(s_prime_boxes):
        return True
    return False

def result(s: Map, a: str):
    """Returns the result of executing action a in state s."""
    s_prime = s.copy()
    s_prime.apply_move(a)
    return s_prime

