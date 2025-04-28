from typing import Tuple, Optional

from sokoban.map import Map
from sokoban.dummy import Dummy
from sokoban.moves import *

from search_methods.utils import *

def h1(s: Map, visited: Optional[dict] = None) -> int:
    """Basic manhattan distance heuristic."""
    return (
        # distance from player to closest box
        min(manhattan(s.player, box) for box in s.boxes.values()) +

        # distance from each box to its nearest goal
        sum(min(manhattan(box, goal) for goal in s.targets) for box in s.boxes.values())
    )

def c1(s: Map, a: int, s_prime: Optional[Map], visited: Optional[dict] = None) -> int:
    """Returns the cost of executing action a in state s."""
    return 1


def h2(s: Map, visited: Optional[dict] = None) -> int:
    """
    Heuristic that considers the distance from the player to his required position
    and the distance from the box to the goal.
    """
    total = 0

    # Match each box with a random goal
    for box, goal in zip(s.boxes.values(), s.targets):
        # Add the manhattan distance from the box to the goal
        total += manhattan(box, goal)

    # Now get the closest box to the player
    box = min(s.boxes.values(), key=lambda box: manhattan(s.player, box))
    goal = min(s.targets, key=lambda goal: manhattan(box, goal))

    # Now check the direction in which the box should be pushed, so that the player
    # should go behind the direction of the box as much as possible
    diff = (box.x - goal[0], box.y - goal[1])
    if abs(diff[0]) > abs(diff[1]):
        direction = (sign(diff[0]), 0)
    else:
        direction = (0, sign(diff[1]))

    required_player_pos = (box.x + direction[0], box.y + direction[1])

    # Add the manhattan distance from the player to the required position
    total += manhattan(s.player, required_player_pos)

    return total

def c2(s: Map, a: int, s_prime: Optional[Map], visited: Optional[dict] = None) -> int:
    """Returns the cost of executing action a in state s."""
    return 1


def h3(s: Map, visited: Optional[dict] = None) -> int:
    """Heuristic that considers the distance from the boxes to their goals."""
    total = 0
    walls = get_walls(s)
    boxes_to_check, targets_remaining = get_boxes_and_goals(s)

    # If all boxes are in their goals, return 0
    if len(boxes_to_check) == 0:
        return 0

    for box in boxes_to_check:
        # Match each box with a goal
        goal = min(targets_remaining, key=lambda goal: manhattan(box, Dummy(*goal)))

        # Add the manhattan distance from the box to the goal
        total += manhattan(box, goal)

        # Check if the box is in a corner and penalize it
        if corner(box, walls):
            total += 100

        # Check if the box was previosuly here and penalize it
        if visited is not None and visited[(box.name, box.xy)]:
            total += 10 * visited[(box.name, box.xy)]

    return total

def c3(s: Map, a: int, s_prime: Optional[Map] = None, visited: Optional[dict] = None) -> int:
    """Returns the cost of executing action a in state s."""

    def _best_move(s: Map, visited: Optional[dict] = None) -> Tuple[dict, dict]:
        # Get where the box should go next and where the player should be placed
        # to push the box in the right direction
        walls = get_walls(s)
        boxes_to_check, targets_remaining = get_boxes_and_goals(s)

        # If all boxes are in their goals, return None
        if len(boxes_to_check) == 0:
            return None, None
        
        # For each box, get the closest goal and the direction in which the box should be pushed
        boxes = {}
        players = {}
        for box, goal in zip(boxes_to_check, targets_remaining):
            diff = (-(box.x - goal[0]), -(box.y - goal[1]))

            if abs(diff[0]) > abs(diff[1]):
                directions = [(sign(diff[0]), 0), (0, sign(diff[1])), (0, -sign(diff[1])), (-sign(diff[0]), 0)]
            else:
                directions = [(0, sign(diff[1])), (sign(diff[0]), 0), (-sign(diff[0]), 0), (0, -sign(diff[1]))]

            # Filter out directions that are not valid
            directions = [d for d in directions.copy() if (box.x + d[0], box.y + d[1]) not in walls]
            directions = [d for d in directions.copy() if not corner((box.x + d[0], box.y + d[1]), walls)]
            directions = [d for d in directions.copy() if (box.x + d[0], box.y + d[1]) not in s.positions_of_boxes.keys()]

            if visited is not None:
                aux = [d for d in directions.copy() if visited[(box.name, (box.x + d[0], box.y + d[1]))] == 0]
                if len(aux) > 0:
                    directions = aux

            # Now for each possible direction, check if the player can push or pull the box
            for d in directions:
                player_pos = (box.x - d[0], box.y - d[1])
                if (player_pos[0], player_pos[1]) not in walls:
                    players[box.name] = Dummy(*player_pos)
                    boxes[box.name] = Dummy(box.x + d[0], box.y + d[1])
                    break

            if box.name in boxes:
                continue

            for d in directions:
                player_pos = (box.x + d[0], box.y + d[1])
                if (player_pos[0], player_pos[1]) not in walls:
                    players[box.name] = Dummy(*player_pos)
                    boxes[box.name] = Dummy(box.x + d[0], box.y + d[1])
                    break

        return boxes, players
    
    if not s_prime:
        s_prime = result(s, a)

    boxes1, _ = get_boxes_and_goals(s)
    boxes2, _ = get_boxes_and_goals(s_prime)

    if len(boxes1) < len(boxes2):
        return 50

    best_boxes, best_players = _best_move(s, visited)
    for box, best_pos in best_boxes.items():
        if s_prime.boxes[box].x == best_pos.x and s_prime.boxes[box].y == best_pos.y:
            # If the box is in the right position, return 0
            return 0

    # If the box is not in the right position, return the manhattan distance
    # from player to his closest position
    aux = [manhattan(s_prime.player, player) for player in best_players.values()]
    if len(aux) == 0:
        return min(manhattan(s_prime.player, box) for box in s.boxes.values())

    return min(aux)
