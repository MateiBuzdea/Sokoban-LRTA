from sokoban import Map
from search_methods.solver import Solver
from search_methods.lrta_star import *
from analysis.utils import *

import matplotlib.pyplot as plt
import numpy as np


results1 = {}
results2 = {}

for map_name, map in MAPS.items():
    print(f"Solving {map_name}...")
    solver1 = Solver(map.copy(), 'lrta_star')
    solver1.h = h1
    solver1.c = c1
    s1, count1, duration1, pulls1 = solver1.solve()

    solver2 = Solver(map.copy(), 'lrta_star')
    solver2.h = h3
    solver2.c = c3
    s2, count2, duration2, pulls2 = solver2.solve()

    results1[map_name] = {
        'count': count1,
        'duration': duration1,
        'pulls': pulls1
    }
    results2[map_name] = {
        'count': count2,
        'duration': duration2,
        'pulls': pulls2
    }

fig, axes = plot_all_characteristics(
    results1,
    results2,
    heuristic_names=('h1', 'h3'),
    title='Performance Comparison: LRTA* h1 vs h3',
    log_scale=True
)
plt.show()
