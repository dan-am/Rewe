"""
Utility functions for the Rewe project.

This module contains helper functions used across the project.
"""

import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv


def get_project_root() -> Path:
    """
    Get the root directory of the project.
    
    Returns:
        Path to the project root
    """
    return Path(__file__).parents[2]


def load_environment(env_file: Optional[str] = None) -> None:
    """
    Load environment variables from .env file.
    
    Args:
        env_file: Path to .env file. If None, looks for .env in project root
    """
    if env_file is None:
        env_file = get_project_root() / ".env"
    
    load_dotenv(env_file)


def get_data_path(data_type: str = "raw") -> Path:
    """
    Get the path to a data directory.
    
    Args:
        data_type: Type of data directory ('raw', 'processed', 'interim', 'external')
        
    Returns:
        Path to the data directory
    """
    valid_types = ["raw", "processed", "interim", "external"]
    if data_type not in valid_types:
        raise ValueError(f"data_type must be one of {valid_types}")
    
    return get_project_root() / "data" / data_type
