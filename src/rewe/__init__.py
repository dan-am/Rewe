"""
Rewe-Projekt: Analyse der REWE Copilot Daten.

Dieses Paket enthält Funktionen zum Laden, Verarbeiten, Analysieren und
Visualisieren der REWE Copilot Hitlisten-Daten.
"""

__version__ = "0.1.0"

from rewe.data import (
    load_hitlisten_tables,
    transpose_group_table,
    analyze_group_sizes,
    aggregate_groups,
)

from rewe.statistics import (
    calculate_power,
    power_analysis,
    print_power_analysis,
    print_group_analysis,
)

from rewe.visualization import (
    set_style,
    plot_group_comparison,
    print_comparison_stats,
)

from rewe.utils import (
    get_project_root,
    load_environment,
    get_data_path,
)

__all__ = [
    # Datenverarbeitung
    'load_hitlisten_tables',
    'transpose_group_table',
    'analyze_group_sizes',
    'aggregate_groups',
    # Statistik
    'calculate_power',
    'power_analysis',
    'print_power_analysis',
    'print_group_analysis',
    # Visualisierung
    'set_style',
    'plot_group_comparison',
    'print_comparison_stats',
    # Hilfsfunktionen
    'get_project_root',
    'load_environment',
    'get_data_path',
]
