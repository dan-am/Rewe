"""
Visualisierungsfunktionen für das Rewe-Projekt.

Dieses Modul enthält Funktionen zur Erstellung standardisierter Visualisierungen.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


def set_style(style: str = "whitegrid") -> None:
    """
    Setzt den Standard-Plotstil.
    
    Args:
        style: Seaborn-Stilname (Standard: "whitegrid")
    """
    sns.set_style(style)
    plt.rcParams["figure.figsize"] = (12, 6)
    plt.rcParams["font.size"] = 10


def plot_group_comparison(
    original_groups: dict,
    aggregated_groups: dict,
    threshold: int = 30,
    figsize: tuple = (16, 7)
) -> plt.Figure:
    """
    Erstellt einen Vergleich zwischen Original- und aggregierten Gruppen.
    
    Args:
        original_groups: Dictionary mit Original-Gruppennamen und Größen
        aggregated_groups: Dictionary mit aggregierten Gruppennamen und Größen
        threshold: Schwellenwert für farbliche Markierung (Standard: 30)
        figsize: Größe der Figur (Standard: (16, 7))
        
    Returns:
        matplotlib Figure-Objekt
    """
    fig, axes = plt.subplots(1, 2, figsize=figsize)
    
    # Original-Gruppen vorbereiten
    sorted_original = sorted(
        [(g, s) for g, s in original_groups.items() if s is not None],
        key=lambda x: x[1],
        reverse=True
    )
    orig_names = [g for g, _ in sorted_original]
    orig_sizes = [s for _, s in sorted_original]
    colors_orig = ['red' if s < threshold else 'green' for s in orig_sizes]
    
    # Aggregierte Gruppen vorbereiten
    sorted_agg = sorted(aggregated_groups.items(), key=lambda x: x[1], reverse=True)
    agg_names = [g for g, _ in sorted_agg]
    agg_sizes = [s for _, s in sorted_agg]
    colors_agg = ['red' if s < threshold else 'green' for s in agg_sizes]
    
    # Subplot 1: Original
    ax1 = axes[0]
    bars1 = ax1.barh(range(len(orig_names)), orig_sizes, color=colors_orig, 
                     alpha=0.7, edgecolor='black')
    ax1.set_yticks(range(len(orig_names)))
    ax1.set_yticklabels(orig_names, fontsize=9)
    ax1.set_xlabel('Anzahl Teilnehmer (n)', fontsize=11, fontweight='bold')
    
    small_count = sum(1 for s in orig_sizes if s < threshold)
    ax1.set_title(f'ORIGINAL\n{len(orig_names)} Gruppen ({small_count} mit n<{threshold})',
                  fontsize=12, fontweight='bold')
    ax1.axvline(x=threshold, color='orange', linestyle='--', linewidth=2,
                label=f'Schwellenwert n={threshold}')
    ax1.legend(fontsize=9)
    ax1.grid(axis='x', alpha=0.3)
    
    # Werte hinzufügen
    for bar, val in zip(bars1, orig_sizes):
        ax1.text(val + 2, bar.get_y() + bar.get_height() / 2,
                f'n={val}', va='center', fontsize=9, fontweight='bold')
    
    # Subplot 2: Aggregiert
    ax2 = axes[1]
    bars2 = ax2.barh(range(len(agg_names)), agg_sizes, color=colors_agg,
                     alpha=0.7, edgecolor='black')
    ax2.set_yticks(range(len(agg_names)))
    ax2.set_yticklabels(agg_names, fontsize=9)
    ax2.set_xlabel('Anzahl Teilnehmer (n)', fontsize=11, fontweight='bold')
    
    small_count_agg = sum(1 for s in agg_sizes if s < threshold)
    ax2.set_title(f'AGGREGIERT\n{len(agg_names)} Gruppen ({small_count_agg} mit n<{threshold})',
                  fontsize=12, fontweight='bold')
    ax2.axvline(x=threshold, color='orange', linestyle='--', linewidth=2,
                label=f'Schwellenwert n={threshold}')
    ax2.legend(fontsize=9)
    ax2.grid(axis='x', alpha=0.3)
    
    # Werte hinzufügen
    for bar, val in zip(bars2, agg_sizes):
        ax2.text(val + 2, bar.get_y() + bar.get_height() / 2,
                f'n={val}', va='center', fontsize=9, fontweight='bold')
    
    plt.suptitle('GRUPPENSTRUKTUR: Vergleich Original vs. Aggregation',
                 fontsize=14, fontweight='bold', y=0.98)
    plt.tight_layout()
    
    return fig


def print_comparison_stats(original_groups: dict, aggregated_groups: dict, threshold: int = 30) -> None:
    """
    Gibt eine formatierte Vergleichsstatistik aus.
    
    Args:
        original_groups: Dictionary mit Original-Gruppennamen und Größen
        aggregated_groups: Dictionary mit aggregierten Gruppennamen und Größen
        threshold: Schwellenwert für Gruppengröße (Standard: 30)
    """
    orig_sizes = [s for s in original_groups.values() if s is not None]
    agg_sizes = list(aggregated_groups.values())
    
    small_orig = sum(1 for s in orig_sizes if s < threshold)
    small_agg = sum(1 for s in agg_sizes if s < threshold)
    
    print("\n" + "=" * 80)
    print("VERGLEICHSSTATISTIK: ORIGINAL vs. AGGREGIERT")
    print("=" * 80)
    
    print(f"\nORIGINAL:")
    print(f"  Anzahl Gruppen:              {len(orig_sizes)}")
    print(f"  Gruppen mit n < {threshold}:          {small_orig} ({small_orig/len(orig_sizes)*100:.0f}%)")
    print(f"  Gruppen mit n ≥ {threshold}:          {len(orig_sizes) - small_orig} ({(len(orig_sizes) - small_orig)/len(orig_sizes)*100:.0f}%)")
    print(f"  Kleinste Gruppe:             n = {min(orig_sizes)}")
    print(f"  Größte Gruppe:               n = {max(orig_sizes)}")
    
    print(f"\nAGGREGIERT:")
    print(f"  Anzahl Gruppen:              {len(agg_sizes)}")
    print(f"  Gruppen mit n < {threshold}:          {small_agg} ({small_agg/len(agg_sizes)*100:.0f}%)")
    print(f"  Gruppen mit n ≥ {threshold}:          {len(agg_sizes) - small_agg} ({(len(agg_sizes) - small_agg)/len(agg_sizes)*100:.0f}%)")
    print(f"  Kleinste Gruppe:             n = {min(agg_sizes)}")
    print(f"  Größte Gruppe:               n = {max(agg_sizes)}")
    
    improvement = small_orig - small_agg
    print(f"\n✓ VERBESSERUNG: {improvement} Gruppen wurden auf n≥{threshold} gebracht!")
    print(f"✓ REDUKTION: {len(orig_sizes) - len(agg_sizes)} Gruppen aggregiert")
    print("=" * 80)

