from sokoban import Map
from search_methods.solver import Solver
from search_methods.lrta_star import *

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

__all__ = ['MAP_NAMES', 'MAPS', 'plot_single_characteristic', 'plot_all_characteristics', 'plot_single_result']

MAP_NAMES = [
    'easy_map1',
    'easy_map2',
    'medium_map1',
    'medium_map2',
    'large_map1',
    'large_map2',
    'hard_map1',
    'hard_map2'
]

MAPS = {name: Map.from_yaml(f'tests/{name}.yaml') for name in MAP_NAMES}


def plot_single_characteristic(results1, results2, characteristic, heuristic_names=None, title=None, log_scale=True, figsize=(12, 6), color_scheme=None):
    """
    Creates a bar plot comparing a single characteristic between two heuristics across different maps.
    """
    if heuristic_names is None:
        heuristic_names = ('Heuristic 1', 'Heuristic 2')
    
    if color_scheme is None:
        color_scheme = ('#4287f5', '#2c5aa0')
    
    # Set default title based on characteristic if not provided
    if title is None:
        title_map = {
            'count': 'Move Count Comparison',
            'duration': 'Duration Comparison',
            'pulls': 'Box Pulls Comparison'
        }
        title = title_map.get(characteristic, f'{characteristic.capitalize()} Comparison')
    
    # Get the y-axis label based on characteristic
    ylabel_map = {
        'count': 'Number of Moves',
        'duration': 'Time (seconds)',
        'pulls': 'Number of Pulls'
    }
    ylabel = ylabel_map.get(characteristic, characteristic.capitalize())
    
    # Extract data
    map_names = list(results1.keys())
    values1 = [v[characteristic] for v in results1.values()]
    values2 = [v[characteristic] for v in results2.values()]
    
    # Create figure
    fig, ax = plt.subplots(figsize=figsize)
    
    # Set up bar positions
    x = np.arange(len(map_names))
    width = 0.35  # the width of the bars
    
    # Create bars
    ax.bar(x - width/2, values1, width, label=heuristic_names[0], color=color_scheme[0], 
           edgecolor='black', linewidth=0.5)
    ax.bar(x + width/2, values2, width, label=heuristic_names[1], color=color_scheme[1], 
           edgecolor='black', linewidth=0.5)
    
    # Set log scale if requested
    if log_scale:
        ax.set_yscale('log', base=10)
    
    # Add labels, title and legend
    ax.set_xlabel('Maps', fontweight='bold')
    ax.set_ylabel(ylabel, fontweight='bold')
    ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(map_names)
    ax.tick_params(axis='x', rotation=45)
    
    # Add grid for better readability
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Add value labels on top of bars
    def add_value_labels(bars):
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height:.1f}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom',
                        fontsize=8, rotation=0)
    
    add_value_labels(ax.patches[:len(map_names)])
    add_value_labels(ax.patches[len(map_names):])

    ax.legend(loc='upper right', frameon=True, framealpha=0.9, edgecolor='black')
    plt.tight_layout()
    
    return fig, ax


def plot_all_characteristics(results1, results2, heuristic_names=None, title=None, 
                             log_scale=True, figsize=(18, 6), color_schemes=None):
    """
    Creates a figure with 3 bar plots comparing counts, durations, and pulls between two heuristics.
    """
    if heuristic_names is None:
        heuristic_names = ('Heuristic 1', 'Heuristic 2')

    if title is None:
        title = 'Sokoban Level Performance Metrics'
    
    if color_schemes is None:
        color_schemes = (
            ('#4287f5', '#2c5aa0'),
            ('#42c86b', '#1a7431'),
            ('#f54242', '#8f2020')
        )
    
    # Extract data
    map_names = list(results1.keys())
    
    counts1 = [v['count'] for v in results1.values()]
    durations1 = [v['duration'] for v in results1.values()]
    pulls1 = [v['pulls'] for v in results1.values()]
    
    counts2 = [v['count'] for v in results2.values()]
    durations2 = [v['duration'] for v in results2.values()]
    pulls2 = [v['pulls'] for v in results2.values()]
    
    # Create figure with 3 subplots
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=figsize)
    fig.suptitle(title, fontsize=16, fontweight='bold', y=0.98)

    x = np.arange(len(map_names))
    width = 0.35

    def _setup_subplot(ax, values1, values2, title, ylabel, color_scheme):
        ax.set_xticks(x)
        ax.set_xticklabels(map_names)
        ax.bar(x - width/2, values1, width, label=heuristic_names[0], color=color_scheme[0], 
               edgecolor='black', linewidth=0.5)
        ax.bar(x + width/2, values2, width, label=heuristic_names[1], color=color_scheme[1], 
               edgecolor='black', linewidth=0.5)
        ax.set_title(title, fontsize=14, fontweight='bold', pad=10)
        ax.set_ylabel(ylabel, fontweight='bold')
        ax.tick_params(axis='x', rotation=45)
        
        if log_scale:
            ax.set_yscale('log', base=10)
        
        ax.grid(axis='y', linestyle='--', alpha=0.7)
        ax.legend(loc='upper right', frameon=True, framealpha=0.9, edgecolor='black')
    
    # Set up each subplot
    _setup_subplot(ax1, counts1, counts2, 'Move Count', 'Number of Moves', color_schemes[0])
    _setup_subplot(ax2, durations1, durations2, 'Duration', 'Time (seconds)', color_schemes[1])
    _setup_subplot(ax3, pulls1, pulls2, 'Box Pulls', 'Number of Pulls', color_schemes[2])
    
    plt.tight_layout()
    fig.subplots_adjust(top=0.85)
    
    return fig, (ax1, ax2, ax3)


def plot_single_result(results, characteristic, heuristic_name='Heuristic', title=None, log_scale=True, 
                      figsize=(12, 6), color='#4287f5'):
    """
    Creates a bar plot showing a single characteristic for one heuristic across different maps.
    """
    # Set default title based on characteristic if not provided
    if title is None:
        title_map = {
            'count': f'Move Count - {heuristic_name}',
            'duration': f'Duration - {heuristic_name}',
            'pulls': f'Box Pulls - {heuristic_name}'
        }
        title = title_map.get(characteristic, f'{characteristic.capitalize()} - {heuristic_name}')
    
    # Get the appropriate axis label based on characteristic
    ylabel_map = {
        'count': 'Number of Moves',
        'duration': 'Time (seconds)',
        'pulls': 'Number of Pulls'
    }
    value_label = ylabel_map.get(characteristic, characteristic.capitalize())
    
    # Extract data
    map_names = list(results.keys())
    values = [v[characteristic] for v in results.values()]

    # Create figure
    fig, ax = plt.subplots(figsize=figsize)

    bars = ax.bar(range(len(map_names)), values, color=color, edgecolor='black', linewidth=0.5)
    ax.set_xticks(range(len(map_names)))
    ax.set_xticklabels(map_names, rotation=45, ha='right')
    ax.set_ylabel(value_label, fontweight='bold')
    ax.set_xlabel('Maps', fontweight='bold')
    
    if log_scale and all(v > 0 for v in values):
        ax.set_yscale('log', base=10)
    
    # Add title
    ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
    
    # Add grid for better readability
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        label_y = height * 1.01 if not log_scale else height * 1.1
        ax.annotate(f'{height:.1f}',
                    xy=(bar.get_x() + bar.get_width()/2, label_y),
                    ha='center', va='bottom', fontsize=9)
    
    fig.text(0.02, 0.02, f"Heuristic: {heuristic_name}", fontsize=8, color='gray')
    
    plt.tight_layout()
    
    return fig, ax