"""
Datenverarbeitungsfunktionen für das Rewe-Projekt.

Dieses Modul enthält Funktionen zum Laden und Verarbeiten von Excel-Daten,
insbesondere für die REWE Copilot Hitlisten-Analyse.
"""

from __future__ import annotations

import re
from pathlib import Path

import pandas as pd

from rewe.utils import get_project_root


def load_hitlisten_tables(
    filename: str = "REWE_Copilot_2025_Hitlisten_251105.xlsx",
    *,
    data_dir: Path | None = None,
    header_row_span: tuple[int, int] = (2, 20),
    expected_tables: int = 6,
) -> list[pd.DataFrame]:
    """
    Lädt und teilt die REWE Copilot Hitlisten-Arbeitsmappe in mehrere Tabellen.

    Die Arbeitsmappe enthält mehrzeilige Kopfzeilen in den Excel-Zeilen 3–20
    (0-indiziert Zeilen 2:20), gefolgt von sechs Tabellen mit identischen Schemas.
    Leere Zeilen trennen die Tabellen.

    Args:
        filename: Excel-Dateiname relativ zu ``data/raw``, falls ``data_dir`` nicht
            angegeben ist.
        data_dir: Optionales Verzeichnis, das ``filename`` enthält. Standard ist
            das Repository-Verzeichnis ``data/raw``.
        header_row_span: Tupel ``(start, stop)`` zur Auswahl der Kopfzeilen.
            ``stop`` ist exklusiv. Standard ``(2, 20)`` erfasst Excel-Zeilen 3–20.
        expected_tables: Erwartete Anzahl Tabellen in der Arbeitsmappe.
            Wird zur Strukturprüfung verwendet.

    Returns:
        Liste von DataFrames in der Reihenfolge wie in der Arbeitsmappe.
        Die erste Spalte enthält Kategorielabels (Strings), alle anderen
        Spalten sind numerisch.

    Raises:
        FileNotFoundError: Wenn die Excel-Datei nicht gefunden wird.
        ValueError: Wenn Kopfzeilen nicht abgeleitet werden können oder sich
            das Arbeitsmappen-Layout geändert hat.
    """

    if data_dir is None:
        data_dir = get_project_root() / "data" / "raw"

    excel_path = Path(filename) if Path(filename).is_absolute() else data_dir / filename

    if not excel_path.exists():
        raise FileNotFoundError(f"Excel-Datei nicht gefunden: {excel_path}")

    header_start, header_stop = header_row_span
    if header_start < 0 or header_stop <= header_start:
        raise ValueError("header_row_span muss ein Tupel aus Ganzzahlen sein, wobei start < stop")

    # Excel-Datei ohne Kopfzeile laden
    raw = pd.read_excel(excel_path, header=None)

    # Kopfzeilen erstellen und kombinieren
    header_rows = raw.iloc[header_start:header_stop]
    headers = _build_headers(header_rows)
    if not headers:
        raise ValueError("Konnte keine Spaltenkopfzeilen aus der Arbeitsmappe erstellen.")
    if not headers[0]:
        headers[0] = "category"

    # Datenteil extrahieren
    data = raw.iloc[header_stop:].copy().reset_index(drop=True)
    data.columns = headers

    # Tabellen anhand leerer Zeilen trennen
    separator_mask = data.isna().all(axis=1)
    tables: list[pd.DataFrame] = []
    start_idx = 0
    
    for idx, is_separator in enumerate(separator_mask):
        if is_separator and start_idx < idx:
            tables.append(data.iloc[start_idx:idx].copy())
            start_idx = idx + 1
    
    if start_idx < len(data):
        tables.append(data.iloc[start_idx:].copy())

    if len(tables) != expected_tables:
        raise ValueError(
            f"Arbeitsmappen-Struktur geändert: erwartet {expected_tables} Tabellen, "
            f"gefunden {len(tables)}"
        )

    # Tabellen bereinigen
    return [_clean_table(table) for table in tables]


def _clean_table(table: pd.DataFrame) -> pd.DataFrame:
    """Bereinigt eine einzelne Tabelle: füllt Kategorien, konvertiert Zahlen."""
    table = table.copy()
    
    # Kategoriespalte forward-fill
    table.iloc[:, 0] = table.iloc[:, 0].ffill()

    # Numerische Spalten konvertieren
    numeric_columns = table.columns[1:]
    table[numeric_columns] = table[numeric_columns].apply(
        lambda col: pd.to_numeric(
            col.mask(col.astype(str).str.fullmatch(r"-"), pd.NA),
            errors="coerce",
        )
    )

    # Leere Zeilen entfernen
    table = table.dropna(subset=numeric_columns, how="all")
    table = table.dropna(subset=[table.columns[0]])
    table.iloc[:, 0] = table.iloc[:, 0].astype(str).str.strip()

    return table.reset_index(drop=True)


def _build_headers(header_rows: pd.DataFrame) -> list[str]:
    """Kombiniert mehrzeilige Kopfzeilen zu einer Kopfzeile."""
    headers: list[str] = []
    for column in header_rows:
        parts = header_rows[column].dropna().astype(str)
        header = " ".join(part.strip() for part in parts if part.strip())
        headers.append(_normalise_header_text(header))
    return headers


def _normalise_header_text(text: str) -> str:
    """Normalisiert Kopfzeilentext: entfernt Zeilenumbrüche und Bindestriche."""
    text = text.replace("\n", " ")
    text = re.sub(r"(?<=\w)-\s+(?=\w)", "", text)  # Bindestriche in Wörtern entfernen
    text = re.sub(r"\s+", " ", text)  # Mehrfache Leerzeichen entfernen
    return text.strip()


def transpose_group_table(table: pd.DataFrame) -> tuple[pd.DataFrame, list[str]]:
    """
    Transponiert eine Gruppentabelle und extrahiert Gruppennamen.
    
    Args:
        table: DataFrame mit Gruppen als Zeilen
        
    Returns:
        Tupel aus (transponierter DataFrame, Liste der Gruppennamen)
    """
    # Transponieren
    transposed = table.T.reset_index()
    
    # Gruppennamen aus erster Zeile extrahieren
    group_names = transposed.iloc[0, 1:].tolist()
    
    # Spalten benennen
    new_columns = ['Question'] + group_names
    transposed.columns = new_columns
    
    # Erste Zeile entfernen (war nur für Spaltennamen)
    transposed = transposed.drop(0).reset_index(drop=True)
    
    return transposed, group_names


def analyze_group_sizes(
    transposed_table: pd.DataFrame, 
    group_names: list[str],
    threshold: int = 30
) -> dict:
    """
    Analysiert Gruppengrößen und identifiziert kleine Gruppen.
    
    Args:
        transposed_table: Transponierte Gruppentabelle
        group_names: Liste der Gruppennamen
        threshold: Schwellenwert für kleine Gruppen (Standard: 30)
        
    Returns:
        Dictionary mit Analyseergebnissen:
        - 'sizes': Dict mit Gruppennamen und Größen
        - 'total': Gesamtzahl der Antworten
        - 'small_groups': Liste der Gruppen mit n < threshold
        - 'sorted': Nach Größe sortierte Liste von (name, size) Tupeln
    """
    first_row = transposed_table.iloc[0]
    
    sizes = {}
    for group in group_names:
        try:
            sizes[group] = int(float(first_row[group]))
        except (ValueError, TypeError):
            sizes[group] = None
    
    # Sortieren nach Größe
    sorted_groups = sorted(
        [(g, s) for g, s in sizes.items() if s is not None],
        key=lambda x: x[1],
        reverse=True
    )
    
    total = sum(s for s in sizes.values() if s is not None)
    small_groups = [(g, s) for g, s in sizes.items() if s is not None and s < threshold]
    
    return {
        'sizes': sizes,
        'total': total,
        'small_groups': small_groups,
        'sorted': sorted_groups
    }


def aggregate_groups(group_sizes: dict, aggregation_mapping: dict) -> dict:
    """
    Aggregiert Gruppen gemäß einer Zuordnung.
    
    Args:
        group_sizes: Dictionary mit Gruppennamen und Größen
        aggregation_mapping: Dictionary, das Original-Gruppennamen auf
            aggregierte Gruppennamen mappt
            
    Returns:
        Dictionary mit aggregierten Gruppennamen und Größen
    """
    aggregated = {}
    
    for original_group, aggregated_name in aggregation_mapping.items():
        if original_group in group_sizes and group_sizes[original_group] is not None:
            size = group_sizes[original_group]
            aggregated[aggregated_name] = aggregated.get(aggregated_name, 0) + size
    
    return aggregated
