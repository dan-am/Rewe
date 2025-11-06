"""
Statistische Analysefunktionen für das Rewe-Projekt.

Dieses Modul enthält Funktionen für Power-Analyse und statistische Tests.
"""

from __future__ import annotations

import numpy as np
from scipy import stats


def calculate_power(
    n: int,
    effect_size: float = 0.5,
    alpha: float = 0.05
) -> float:
    """
    Berechnet die statistische Power für einen t-Test.
    
    Args:
        n: Stichprobengröße
        effect_size: Cohen's d (0.2=klein, 0.5=mittel, 0.8=groß)
        alpha: Signifikanzniveau (Standard: 0.05)
        
    Returns:
        Statistische Power (zwischen 0 und 1)
    """
    # Kritischer Wert für zweiseitigen Test
    z_alpha = stats.norm.ppf(1 - alpha / 2)
    
    # Non-centrality Parameter
    delta = effect_size * np.sqrt(n / 2)
    
    # Power berechnen
    power = 1 - stats.norm.cdf(z_alpha - delta) + stats.norm.cdf(-z_alpha - delta)
    
    return power


def power_analysis(
    group_sizes: dict,
    effect_size: float = 0.5,
    alpha: float = 0.05
) -> dict:
    """
    Führt Power-Analyse für mehrere Gruppen durch.
    
    Args:
        group_sizes: Dictionary mit Gruppennamen und Größen
        effect_size: Cohen's d (Standard: 0.5 = mittlerer Effekt)
        alpha: Signifikanzniveau (Standard: 0.05)
        
    Returns:
        Dictionary mit Ergebnissen:
        - 'powers': Dict mit Gruppennamen und Power-Werten
        - 'avg_power': Durchschnittliche Power
        - 'min_power': Minimale Power
        - 'max_power': Maximale Power
        - 'ratings': Dict mit Bewertungen ('sehr_gut', 'akzeptabel', 'unzureichend')
    """
    powers = {}
    ratings = {}
    
    for group, size in group_sizes.items():
        if size is not None:
            power = calculate_power(size, effect_size, alpha)
            powers[group] = power
            
            # Bewertung
            if power >= 0.80:
                ratings[group] = 'sehr_gut'
            elif power >= 0.60:
                ratings[group] = 'akzeptabel'
            else:
                ratings[group] = 'unzureichend'
    
    power_values = list(powers.values())
    
    return {
        'powers': powers,
        'avg_power': np.mean(power_values) if power_values else 0,
        'min_power': min(power_values) if power_values else 0,
        'max_power': max(power_values) if power_values else 0,
        'ratings': ratings
    }


def print_group_analysis(
    group_sizes: dict,
    threshold: int = 30,
    show_percentages: bool = True
) -> None:
    """
    Gibt eine formatierte Gruppenanalyse aus.
    
    Args:
        group_sizes: Dictionary mit Gruppennamen und Größen
        threshold: Schwellenwert für kleine Gruppen
        show_percentages: Ob Prozentanteile angezeigt werden sollen
    """
    print("=" * 80)
    print("GRUPPENGRÖSSENANALYSE")
    print("=" * 80)
    
    # Nach Größe sortieren
    sorted_groups = sorted(
        [(g, s) for g, s in group_sizes.items() if s is not None],
        key=lambda x: x[1],
        reverse=True
    )
    
    total = sum(s for _, s in sorted_groups)
    
    print(f"\nGruppengröße (Anzahl Antworten):")
    print("-" * 80)
    
    for group, size in sorted_groups:
        marker = "✓" if size >= threshold else "⚠"
        if show_percentages and total > 0:
            percent = (size / total) * 100
            print(f"{marker} {group:60s}: n = {size:4d} ({percent:5.1f}%)")
        else:
            print(f"{marker} {group:60s}: n = {size:4d}")
    
    print(f"\n{'Gesamt:':62s}  n = {total:4d}")
    
    # Kleine Gruppen identifizieren
    small_groups = [s for _, s in sorted_groups if s < threshold]
    
    print(f"\n{'Gruppen mit n < ' + str(threshold) + ':':62s}  {len(small_groups)}")
    print(f"{'Gruppen mit n ≥ ' + str(threshold) + ':':62s}  {len(sorted_groups) - len(small_groups)}")
    print("=" * 80)


def print_power_analysis(power_results: dict) -> None:
    """
    Gibt eine formatierte Power-Analyse aus.
    
    Args:
        power_results: Ergebnis-Dictionary von power_analysis()
    """
    print("=" * 80)
    print("POWER-ANALYSE")
    print("=" * 80)
    
    print(f"\n{'Gruppe':<45s} {'Power':>8s} {'Bewertung':<20s}")
    print("-" * 80)
    
    # Nach Power sortieren
    sorted_powers = sorted(
        power_results['powers'].items(),
        key=lambda x: x[1],
        reverse=True
    )
    
    for group, power in sorted_powers:
        rating = power_results['ratings'][group]
        
        if rating == 'sehr_gut':
            marker = "✓"
            rating_text = "Sehr gut"
        elif rating == 'akzeptabel':
            marker = "○"
            rating_text = "Akzeptabel"
        else:
            marker = "✗"
            rating_text = "Unzureichend"
        
        print(f"{marker} {group:<43s} {power:>7.1%} {rating_text:<20s}")
    
    print("-" * 80)
    print(f"\nDurchschnittliche Power: {power_results['avg_power']:.1%}")
    print(f"Minimale Power:          {power_results['min_power']:.1%}")
    print(f"Maximale Power:          {power_results['max_power']:.1%}")
    print("=" * 80)
