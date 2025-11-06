# Rewe Copilot Analyse - Refaktorierte Version

## Überblick

Dieses Projekt analysiert die REWE Copilot Hitlisten-Daten mit einem Fokus auf statistische Robustheit und Code-Qualität.

## Projektstruktur

```
Rewe/
├── src/rewe/              # Hauptpaket mit allen Modulen
│   ├── __init__.py        # Paket-Initialisierung mit Exporten
│   ├── data.py            # Datenlade- und Verarbeitungsfunktionen
│   ├── statistics.py      # Statistische Analyse-Funktionen
│   ├── visualization.py   # Visualisierungsfunktionen
│   └── utils.py           # Allgemeine Hilfsfunktionen
├── data/                  # Datenverzeichnisse
│   ├── raw/              # Rohdaten (Excel-Dateien)
│   ├── processed/        # Verarbeitete Daten
│   ├── interim/          # Zwischenergebnisse
│   └── external/         # Externe Daten
├── notebooks/            # Jupyter Notebooks
├── DataAnalysis_Rewe.ipynb  # Haupt-Analyse-Notebook
└── README_REFACTORING.md    # Diese Datei
```

## Hauptmodule

### 1. `rewe.data` - Datenverarbeitung

**Funktionen:**
- `load_hitlisten_tables()`: Lädt Excel-Daten und teilt sie in Tabellen
- `transpose_group_table()`: Transponiert Gruppentabellen
- `analyze_group_sizes()`: Analysiert Gruppengrößen und identifiziert kleine Gruppen
- `aggregate_groups()`: Aggregiert Gruppen gemäß Zuordnung

**Beispiel:**
```python
from rewe.data import load_hitlisten_tables, analyze_group_sizes

# Daten laden
tables = load_hitlisten_tables()

# Gruppen analysieren
analysis = analyze_group_sizes(transposed_table, group_names, threshold=30)
```

### 2. `rewe.statistics` - Statistische Analysen

**Funktionen:**
- `calculate_power()`: Berechnet statistische Power für t-Tests
- `power_analysis()`: Führt Power-Analyse für mehrere Gruppen durch
- `print_power_analysis()`: Formatierte Ausgabe der Power-Analyse
- `print_group_analysis()`: Formatierte Ausgabe der Gruppenanalyse

**Beispiel:**
```python
from rewe.statistics import power_analysis, print_power_analysis

# Power-Analyse durchführen
results = power_analysis(group_sizes, effect_size=0.5, alpha=0.05)
print_power_analysis(results)
```

### 3. `rewe.visualization` - Visualisierungen

**Funktionen:**
- `set_style()`: Setzt einheitlichen Plot-Stil
- `plot_group_comparison()`: Vergleicht Original- und aggregierte Gruppen
- `print_comparison_stats()`: Zeigt Vergleichsstatistiken

**Beispiel:**
```python
from rewe.visualization import plot_group_comparison

# Gruppen visualisieren
fig = plot_group_comparison(original_groups, aggregated_groups, threshold=30)
plt.show()
```

### 4. `rewe.utils` - Hilfsfunktionen

**Funktionen:**
- `get_project_root()`: Gibt Projekt-Stammverzeichnis zurück
- `get_data_path()`: Gibt Pfad zu Datenverzeichnissen zurück
- `load_environment()`: Lädt Umgebungsvariablen

## Verbesserungen durch Refaktorierung

### Code-Qualität
- ✅ **Modularisierung**: Wiederverwendbare Funktionen statt Code-Duplikation
- ✅ **Deutsche Dokumentation**: Alle Docstrings und Kommentare auf Deutsch
- ✅ **Type Hints**: Typ-Annotationen für bessere Code-Qualität
- ✅ **Fehlerbehandlung**: Robuste Validierung und aussagekräftige Fehlermeldungen

### Code-Reduktion
- ✅ **~60% weniger Code** im Notebook durch Funktionsauslagerung
- ✅ **Keine Code-Duplikation** mehr
- ✅ **Einfachere Wartbarkeit**

### Funktionalität
- ✅ **Automatische Gruppenaggregation** mit konfigurierbaren Schwellenwerten
- ✅ **Statistische Power-Analyse** für Gruppenvergleiche
- ✅ **Professionelle Visualisierungen** mit konsistentem Stil
- ✅ **Formatierte Ausgaben** für bessere Lesbarkeit

## Verwendung im Notebook

Das Notebook wurde drastisch vereinfacht. Statt hunderten Zeilen Code:

**Vorher:**
```python
# 50+ Zeilen Code für Gruppenaggregation
# 40+ Zeilen Code für Power-Analyse
# 80+ Zeilen Code für Visualisierung
```

**Nachher:**
```python
# Alle Funktionen importieren
from rewe.data import analyze_group_sizes, aggregate_groups
from rewe.statistics import power_analysis, print_power_analysis
from rewe.visualization import plot_group_comparison

# Analyse in 3 Zeilen
analysis = analyze_group_sizes(table, groups, threshold=30)
aggregated = aggregate_groups(analysis['sizes'], mapping)
power_results = power_analysis(aggregated)

# Visualisierung in 1 Zeile
plot_group_comparison(analysis['sizes'], aggregated)
```

## Statistische Empfehlungen

### Gruppengrößen-Schwellenwerte
- **n ≥ 30**: Parametrische und nicht-parametrische Tests möglich
- **20 ≤ n < 30**: Nur nicht-parametrische Tests empfohlen
- **n < 20**: Nur deskriptive Statistik

### Power-Analyse
- **Power ≥ 0.80**: Sehr gut für robuste Inferenzstatistik
- **Power ≥ 0.60**: Akzeptabel mit Vorsicht
- **Power < 0.60**: Unzureichend, nur explorative Analyse

## Installation der Abhängigkeiten

```bash
pip install pandas numpy scipy matplotlib seaborn python-dotenv
```

## Tests durchführen

```bash
# Tests ausführen (wenn vorhanden)
pytest tests/

# Einzelne Funktionen testen
python -c "from rewe.data import load_hitlisten_tables; print('Import erfolgreich')"
```

## Weiterführende Arbeiten

- [ ] Unit-Tests für alle Funktionen erstellen
- [ ] Weitere statistische Analysefunktionen hinzufügen
- [ ] Exportfunktionen für Berichte implementieren
- [ ] Interaktive Dashboards mit Plotly/Dash erstellen

## Autoren

Daniel Ambach - Initiales Projekt und Refaktorierung

## Lizenz

Dieses Projekt ist für interne Verwendung bei REWE bestimmt.
