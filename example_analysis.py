"""
Beispiel-Skript zur Demonstration der refaktorierten Funktionen.

Dieses Skript zeigt, wie die verschiedenen Module zusammen verwendet werden.
"""

from pathlib import Path
import sys

# Pfad zum src-Verzeichnis hinzufügen
project_root = Path(__file__).parent
src_path = project_root / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

# Alle benötigten Funktionen importieren
from rewe.data import (
    load_hitlisten_tables,
    transpose_group_table,
    analyze_group_sizes,
    aggregate_groups
)
from rewe.statistics import (
    power_analysis,
    print_power_analysis,
    print_group_analysis
)
from rewe.visualization import (
    plot_group_comparison,
    print_comparison_stats
)


def main():
    """Hauptfunktion für die Beispiel-Analyse."""
    
    print("=" * 80)
    print("REWE COPILOT ANALYSE - BEISPIEL")
    print("=" * 80)
    print()
    
    # 1. Daten laden
    print("1. Lade Hitlisten-Tabellen...")
    hitlisten_tables = load_hitlisten_tables()
    print(f"   ✓ {len(hitlisten_tables)} Tabellen geladen\n")
    
    # 2. Erste Tabelle teilen
    print("2. Teile erste Tabelle...")
    table_0 = hitlisten_tables[0].iloc[[0]]
    table_1 = hitlisten_tables[0].iloc[1:]
    hitlisten_tables = [table_0, table_1] + hitlisten_tables[1:]
    print(f"   ✓ Tabellenliste aktualisiert: {len(hitlisten_tables)} Tabellen\n")
    
    # 3. Tabelle 2 transponieren
    print("3. Transponiere Tabelle 2...")
    table_2 = hitlisten_tables[2]
    table_2_transposed, group_names = transpose_group_table(table_2)
    print(f"   ✓ {len(group_names)} Gruppen erkannt\n")
    
    # 4. Gruppengrößen analysieren
    print("4. Analysiere Gruppengrößen...")
    analysis = analyze_group_sizes(table_2_transposed, group_names, threshold=30)
    print_group_analysis(analysis['sizes'], threshold=30, show_percentages=True)
    print()
    
    # 5. Gruppen aggregieren
    print("5. Aggregiere Gruppen...")
    aggregation_mapping = {
        'IT, Daten, Analytics - Fachrolle': 'IT & Daten',
        'Leitung und Geschäftsführung - Führung': 'Führung (alle)',
        'Sonstiges - Führung': 'Führung (alle)',
        'Produktmanagement & Agile': 'Produktmanagement & Agile (alle)',
        'Produktmanagement & Agile - Projekt-, \nProgrammleitung, Koordination und PMO': 'Produktmanagement & Agile (alle)',
        'Sonstiges - Projekt-, Programmleitung, \nKoordination und PMO': 'Produktmanagement & Agile (alle)',
        'Sonstiges - Fachrolle': 'Sonstige (Fach)',
        'HR - Fachrolle': 'HR',
        'Finanzen & Controlling': 'Finanzen & Controlling',
        'Logistik & Einkauf & Beschaffung': 'Logistik & Einkauf',
        'Vertrieb': 'Vertrieb'
    }
    
    temp_groups = aggregate_groups(analysis['sizes'], aggregation_mapping)
    
    # Finale Aggregation mit Restgruppe
    aggregated_groups = {
        'IT & Daten': temp_groups.get('IT & Daten', 0),
        'Führung (alle)': temp_groups.get('Führung (alle)', 0),
        'Produktmanagement & Agile (alle)': temp_groups.get('Produktmanagement & Agile (alle)', 0)
    }
    
    restgruppe_sources = ['Sonstige (Fach)', 'HR', 'Finanzen & Controlling', 
                          'Logistik & Einkauf', 'Vertrieb']
    restgruppe_size = sum(temp_groups.get(name, 0) for name in restgruppe_sources)
    aggregated_groups['Restgruppe (Sonstige & kleine Gruppen)'] = restgruppe_size
    
    print(f"   ✓ {len(aggregated_groups)} aggregierte Gruppen erstellt\n")
    
    # 6. Power-Analyse
    print("6. Führe Power-Analyse durch...")
    power_results = power_analysis(aggregated_groups, effect_size=0.5, alpha=0.05)
    print_power_analysis(power_results)
    print()
    
    # 7. Vergleichsstatistik
    print("7. Zeige Vergleichsstatistik...")
    print_comparison_stats(analysis['sizes'], aggregated_groups, threshold=30)
    print()
    
    # 8. Visualisierung
    print("8. Erstelle Visualisierung...")
    import matplotlib.pyplot as plt
    fig = plot_group_comparison(analysis['sizes'], aggregated_groups, threshold=30)
    
    # Speichere Visualisierung
    output_file = project_root / "group_comparison.png"
    fig.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"   ✓ Visualisierung gespeichert: {output_file}\n")
    
    plt.show()
    
    print("=" * 80)
    print("ANALYSE ABGESCHLOSSEN")
    print("=" * 80)


if __name__ == "__main__":
    main()
