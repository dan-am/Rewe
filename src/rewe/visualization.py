"""
Visualization utilities for the Rewe project.

This module contains functions for creating standard visualizations.
"""

import matplotlib.pyplot as plt
import seaborn as sns


def set_style(style: str = "whitegrid") -> None:
    """
    Set the default plotting style.
    
    Args:
        style: Seaborn style name
    """
    sns.set_style(style)
    plt.rcParams["figure.figsize"] = (12, 6)
    plt.rcParams["font.size"] = 10


# Add your visualization functions here
