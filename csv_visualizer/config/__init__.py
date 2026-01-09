"""Konfiguracija aplikacije."""

from .settings import Settings, get_settings
from .themes import Theme, ThemeManager, LIGHT_THEME, DARK_THEME

__all__ = ["Settings", "get_settings", "Theme", "ThemeManager", "LIGHT_THEME", "DARK_THEME"]
