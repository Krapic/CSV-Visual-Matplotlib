"""Generator sintetičkih podataka studenata."""

import random
import numpy as np
import pandas as pd
from pathlib import Path

from ..config import get_settings
from .models import ExamData


class DataGenerator:
    """Generira sintetičke podatke o studentima."""

    def __init__(self):
        self.settings = get_settings()

    def _score_to_grade(self, score: int) -> int:
        """Pretvara bodove u ocjenu."""
        thresholds = self.settings.grade_thresholds
        for grade in sorted(thresholds.keys(), reverse=True):
            if score >= thresholds[grade]:
                return grade
        return 1

    def generate(
        self,
        count: int | None = None,
        save_path: str | None = None
    ) -> ExamData:
        """
        Generira podatke studenata.

        Args:
            count: Broj studenata (koristi default ako nije navedeno)
            save_path: Putanja za spremanje CSV-a (opcionalno)

        Returns:
            ExamData objekt s generiranim podacima

        Raises:
            ValueError: Ako je broj studenata prevelik za jedinstvena imena
        """
        if count is None:
            count = self.settings.default_student_count

        all_names = self.settings.male_names + self.settings.female_names
        max_combinations = len(all_names) * len(self.settings.surnames)

        if count > max_combinations:
            raise ValueError(
                f"Broj studenata ({count}) premašuje maksimalan broj "
                f"jedinstvenih kombinacija imena ({max_combinations})."
            )

        records = []
        used_names: set[str] = set()

        for i in range(1, count + 1):
            # Generiraj jedinstveno ime
            for _ in range(1000):
                if random.random() < 0.5:
                    first_name = random.choice(self.settings.male_names)
                else:
                    first_name = random.choice(self.settings.female_names)
                last_name = random.choice(self.settings.surnames)
                full_name = f"{first_name} {last_name}"

                if full_name not in used_names:
                    used_names.add(full_name)
                    break
            else:
                raise RuntimeError(
                    f"Nije moguće generirati jedinstveno ime nakon 1000 pokušaja."
                )

            # Odaberi termin
            term = random.choice(self.settings.exam_terms)

            # Generiraj bodove prema distribuciji
            roll = random.random()
            for threshold, mean, std, min_score, max_score in self.settings.score_distribution:
                if roll < threshold:
                    score = int(np.clip(np.random.normal(mean, std), min_score, max_score))
                    break

            grade = self._score_to_grade(score)

            records.append({
                "student_id": i,
                "ime": first_name,
                "prezime": last_name,
                "termin": term,
                "bodovi": score,
                "ocjena": grade,
            })

        df = pd.DataFrame(records)

        # Spremi ako je navedena putanja
        actual_path = save_path
        if save_path:
            try:
                df.to_csv(save_path, index=False)
            except (IOError, OSError) as e:
                raise IOError(f"Nije moguće spremiti CSV na '{save_path}': {e}") from e

        return ExamData(df, actual_path)

    def generate_and_save(self, path: str | None = None, count: int | None = None) -> ExamData:
        """
        Generira i sprema podatke.

        Args:
            path: Putanja za spremanje (koristi default ako nije navedeno)
            count: Broj studenata

        Returns:
            ExamData objekt
        """
        if path is None:
            path = self.settings.default_csv_path
        return self.generate(count=count, save_path=path)
