"""
Hilfsfunktionen für das Rewe-Projekt.

Dieses Modul enthält allgemeine Hilfsfunktionen für das gesamte Projekt.
"""

from pathlib import Path
from typing import Optional

from dotenv import load_dotenv


def get_project_root() -> Path:
    """
    Gibt das Stammverzeichnis des Projekts zurück.
    
    Returns:
        Pfad zum Projekt-Stammverzeichnis
    """
    return Path(__file__).parents[2]


def load_environment(env_file: Optional[str] = None) -> None:
    """
    Lädt Umgebungsvariablen aus einer .env-Datei.
    
    Args:
        env_file: Pfad zur .env-Datei. Falls None, wird im Projekt-Stammverzeichnis
            nach .env gesucht
    """
    if env_file is None:
        env_file = get_project_root() / ".env"
    
    load_dotenv(env_file)


def get_data_path(data_type: str = "raw") -> Path:
    """
    Gibt den Pfad zu einem Datenverzeichnis zurück.
    
    Args:
        data_type: Typ des Datenverzeichnisses ('raw', 'processed', 'interim', 'external')
        
    Returns:
        Pfad zum Datenverzeichnis
        
    Raises:
        ValueError: Wenn ein ungültiger data_type angegeben wird
    """
    valid_types = ["raw", "processed", "interim", "external"]
    if data_type not in valid_types:
        raise ValueError(f"data_type muss einer von {valid_types} sein")
    
    return get_project_root() / "data" / data_type
