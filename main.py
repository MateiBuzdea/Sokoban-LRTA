import sys

from sokoban import Map
from search_methods.solver import Solver
from search_methods.lrta_star import *
from analysis.utils import *
from sokoban.gif import *

import matplotlib.pyplot as plt
import numpy as np

algorithm = sys.argv[1] if len(sys.argv) > 1 else 'lrta_star'

map = MAPS['easy_map1']
solver = Solver(map.copy(), algorithm)
solver.h = h3
solver.c = c3

states, count, duration, pulls = solver.solve(display=True)

# Animate the solution
save_images(states, 'images/map1_images/')
# create_gif('images/map1_images/', 'solution', 'images') # Sometimes not working

results = {}
for map_name, map in MAPS.items():
    print(f"Solving {map_name}...")
    solver = Solver(map.copy(), algorithm)
    solver.h = h3
    solver.c = c3
    s, count, duration, pulls = solver.solve(display=False)

    results[map_name] = {
        'count': count,
        'duration': duration,
        'pulls': pulls
    }

fig, axes = plot_single_result(
    results,
    characteristic='count',
    heuristic_name=algorithm,
    title=f'Solution Steps per Map for {algorithm}',
    log_scale=True
)
plt.show()