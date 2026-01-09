"""Postavke aplikacije."""

from dataclasses import dataclass, field
from pathlib import Path
import json
from typing import ClassVar


@dataclass
class Settings:
    """Glavne postavke aplikacije."""

    # Putanje
    default_csv_path: str = "studenti_ispit.csv"
    last_opened_path: str | None = None
    last_save_path: str | None = None

    # Generiranje podataka
    default_student_count: int = 50
    max_student_count: int = 500

    # Ispitni termini
    exam_terms: list[str] = field(default_factory=lambda: [
        "2025-01", "2025-02", "2025-06", "2025-09"
    ])

    # Ocjene pragovi
    grade_thresholds: dict[int, int] = field(default_factory=lambda: {
        5: 90,
        4: 80,
        3: 65,
        2: 50,
        1: 0
    })

    # GUI
    window_width: int = 1500
    window_height: int = 900
    min_width: int = 1200
    min_height: int = 700
    theme: str = "light"

    # Export
    default_dpi: int = 150
    default_format: str = "png"

    # Imena za generiranje
    male_names: list[str] = field(default_factory=lambda: [
        "Luka", "Ivan", "Marko", "Petar", "Josip", "Matej", "Filip", "Ante", "Tomislav",
        "Karlo", "Leon", "David", "Antonio", "Nikola", "Fran", "Lovro", "Borna", "Domagoj",
        "Tin", "Jan", "Roko", "Matija", "Jakov", "Andrija", "Marin", "Bruno", "Leo"
    ])

    female_names: list[str] = field(default_factory=lambda: [
        "Ana", "Marija", "Ivana", "Petra", "Lucija", "Maja", "Sara", "Lana", "Eva",
        "Ema", "Mia", "Nika", "Lara", "Nina", "Tea", "Lea", "Paula", "Helena",
        "Karla", "Marta", "Katarina", "Valentina", "Klara", "Gabriela", "Nikolina"
    ])

    surnames: list[str] = field(default_factory=lambda: [
        "Horvat", "Kovačević", "Babić", "Marić", "Novak", "Jurić", "Kovač", "Knežević",
        "Vuković", "Božić", "Blažević", "Perić", "Tomić", "Matić", "Pavlović", "Radić",
        "Šimić", "Nikolić", "Grgić", "Filipović", "Barić", "Lončar", "Pavić", "Šarić",
        "Jakić", "Klarić", "Vidović", "Mihaljević", "Tadić", "Lovrić", "Petrović"
    ])

    # Distribucija bodova (granica, mean, std, min, max)
    score_distribution: list[tuple[float, int, int, int, int]] = field(default_factory=lambda: [
        (0.15, 25, 10, 0, 49),
        (0.30, 55, 8, 50, 64),
        (0.55, 70, 6, 65, 79),
        (0.80, 85, 5, 80, 89),
        (1.00, 93, 4, 90, 100),
    ])

    _config_path: ClassVar[Path] = Path.home() / ".csv_visualizer" / "settings.json"

    def save(self) -> None:
        """Sprema postavke u JSON datoteku."""
        self._config_path.parent.mkdir(parents=True, exist_ok=True)

        data = {
            "default_csv_path": self.default_csv_path,
            "last_opened_path": self.last_opened_path,
            "last_save_path": self.last_save_path,
            "default_student_count": self.default_student_count,
            "window_width": self.window_width,
            "window_height": self.window_height,
            "theme": self.theme,
            "default_dpi": self.default_dpi,
            "default_format": self.default_format,
        }

        with open(self._config_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    @classmethod
    def load(cls) -> "Settings":
        """Učitava postavke iz JSON datoteke."""
        settings = cls()

        if cls._config_path.exists():
            try:
                with open(cls._config_path, "r", encoding="utf-8") as f:
                    data = json.load(f)

                for key, value in data.items():
                    if hasattr(settings, key):
                        setattr(settings, key, value)
            except (json.JSONDecodeError, IOError):
                pass

        return settings


_settings: Settings | None = None


def get_settings() -> Settings:
    """Vraća globalnu instancu postavki (singleton)."""
    global _settings
    if _settings is None:
        _settings = Settings.load()
    return _settings
