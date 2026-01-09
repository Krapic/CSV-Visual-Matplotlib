"""Definicije tema za aplikaciju (light/dark mode)."""

from dataclasses import dataclass, field
from typing import ClassVar


@dataclass(frozen=True)
class Theme:
    """Definicija teme za GUI i grafove."""

    name: str

    # GUI boje
    bg_primary: str
    bg_secondary: str
    bg_tertiary: str
    fg_primary: str
    fg_secondary: str
    fg_muted: str
    accent: str
    accent_hover: str
    border: str

    # Grafovi
    graph_bg: str
    graph_fg: str
    graph_grid: str

    # Statistika
    stats_bg: str
    stats_fg: str

    # Buttons
    btn_primary_bg: str
    btn_primary_fg: str
    btn_secondary_bg: str
    btn_secondary_fg: str

    # Grafovi - s defaultom
    graph_colors: tuple[str, ...] = field(default_factory=tuple)

    # Status boje
    success: str = "#22c55e"
    warning: str = "#f59e0b"
    error: str = "#ef4444"
    info: str = "#3b82f6"


LIGHT_THEME = Theme(
    name="light",

    # GUI
    bg_primary="#ffffff",
    bg_secondary="#f8fafc",
    bg_tertiary="#f1f5f9",
    fg_primary="#0f172a",
    fg_secondary="#334155",
    fg_muted="#64748b",
    accent="#2563eb",
    accent_hover="#1d4ed8",
    border="#e2e8f0",

    # Grafovi
    graph_bg="#ffffff",
    graph_fg="#0f172a",
    graph_grid="#e2e8f0",
    graph_colors=(
        "#2563eb",  # Blue
        "#dc2626",  # Red
        "#16a34a",  # Green
        "#d97706",  # Amber
        "#7c3aed",  # Violet
        "#0891b2",  # Cyan
        "#c026d3",  # Fuchsia
        "#059669",  # Emerald
    ),

    # Statistika
    stats_bg="#ffffff",
    stats_fg="#334155",

    # Buttons
    btn_primary_bg="#2563eb",
    btn_primary_fg="#ffffff",
    btn_secondary_bg="#f1f5f9",
    btn_secondary_fg="#334155",
)


DARK_THEME = Theme(
    name="dark",

    # GUI
    bg_primary="#0f172a",
    bg_secondary="#1e293b",
    bg_tertiary="#334155",
    fg_primary="#f8fafc",
    fg_secondary="#cbd5e1",
    fg_muted="#64748b",
    accent="#3b82f6",
    accent_hover="#60a5fa",
    border="#334155",

    # Grafovi
    graph_bg="#1e293b",
    graph_fg="#f8fafc",
    graph_grid="#334155",
    graph_colors=(
        "#60a5fa",  # Blue
        "#f87171",  # Red
        "#4ade80",  # Green
        "#fbbf24",  # Amber
        "#a78bfa",  # Violet
        "#22d3ee",  # Cyan
        "#e879f9",  # Fuchsia
        "#34d399",  # Emerald
    ),

    # Statistika
    stats_bg="#1e293b",
    stats_fg="#cbd5e1",

    # Buttons
    btn_primary_bg="#3b82f6",
    btn_primary_fg="#ffffff",
    btn_secondary_bg="#334155",
    btn_secondary_fg="#cbd5e1",
)


class ThemeManager:
    """Upravlja temama aplikacije."""

    _themes: ClassVar[dict[str, Theme]] = {
        "light": LIGHT_THEME,
        "dark": DARK_THEME,
    }
    _current: ClassVar[Theme] = LIGHT_THEME
    _listeners: ClassVar[list["Callable[[Theme], None]"]] = []
    _initialized: ClassVar[bool] = False

    @classmethod
    def _ensure_initialized(cls) -> None:
        """Osigurava da su listeneri inicijalizirani kao nova lista."""
        if not cls._initialized:
            cls._listeners = []
            cls._initialized = True

    @classmethod
    def get_current(cls) -> Theme:
        """Vraća trenutnu temu."""
        return cls._current

    @classmethod
    def set_theme(cls, name: str) -> None:
        """Postavlja temu po imenu."""
        if name not in cls._themes:
            raise ValueError(f"Nepoznata tema: {name}")
        cls._current = cls._themes[name]
        cls._notify_listeners()

    @classmethod
    def toggle(cls) -> Theme:
        """Prebacuje između light i dark teme."""
        new_name = "dark" if cls._current.name == "light" else "light"
        cls.set_theme(new_name)
        return cls._current

    @classmethod
    def add_listener(cls, callback) -> None:
        """Dodaje listener za promjene teme."""
        cls._ensure_initialized()
        if callback not in cls._listeners:
            cls._listeners.append(callback)

    @classmethod
    def remove_listener(cls, callback) -> None:
        """Uklanja listener."""
        cls._ensure_initialized()
        try:
            cls._listeners.remove(callback)
        except ValueError:
            pass  # Listener već uklonjen

    @classmethod
    def _notify_listeners(cls) -> None:
        """Obavještava sve listenere o promjeni teme."""
        cls._ensure_initialized()
        # Kopiraj listu da izbjegnemo probleme s modifikacijom tijekom iteracije
        for callback in cls._listeners[:]:
            try:
                callback(cls._current)
            except Exception:
                # Listener možda više ne postoji (widget uništen)
                pass

    @classmethod
    def get_available_themes(cls) -> list[str]:
        """Vraća listu dostupnih tema."""
        return list(cls._themes.keys())
