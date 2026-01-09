"""Podatkovni modeli."""

from dataclasses import dataclass, field
from typing import Iterator
import pandas as pd


@dataclass
class StudentRecord:
    """Predstavlja jedan zapis studenta."""

    student_id: int
    first_name: str
    last_name: str
    term: str
    score: int
    grade: int

    @property
    def full_name(self) -> str:
        """Puno ime studenta."""
        return f"{self.first_name} {self.last_name}"

    @property
    def passed(self) -> bool:
        """Je li student položio."""
        return self.grade >= 2

    def to_dict(self) -> dict:
        """Pretvara zapis u rječnik."""
        return {
            "student_id": self.student_id,
            "ime": self.first_name,
            "prezime": self.last_name,
            "termin": self.term,
            "bodovi": self.score,
            "ocjena": self.grade,
        }


@dataclass
class ExamData:
    """Wrapper za podatke ispita s pomoćnim metodama."""

    _df: pd.DataFrame
    _source_path: str | None = None

    @property
    def dataframe(self) -> pd.DataFrame:
        """Vraća DataFrame."""
        return self._df

    @property
    def source_path(self) -> str | None:
        """Vraća putanju izvora podataka."""
        return self._source_path

    @property
    def student_count(self) -> int:
        """Broj studenata."""
        return len(self._df)

    @property
    def average_score(self) -> float:
        """Prosječni bodovi."""
        return float(self._df["bodovi"].mean())

    @property
    def average_grade(self) -> float:
        """Prosječna ocjena."""
        return float(self._df["ocjena"].mean())

    @property
    def pass_rate(self) -> float:
        """Prolaznost u postocima."""
        if len(self._df) == 0:
            return 0.0
        passed = (self._df["ocjena"] >= 2).sum()
        return (passed / len(self._df)) * 100

    @property
    def terms(self) -> list[str]:
        """Lista svih termina."""
        return sorted(self._df["termin"].unique().tolist())

    @property
    def grades(self) -> list[int]:
        """Lista svih ocjena."""
        return sorted(self._df["ocjena"].unique().tolist())

    def get_grade_distribution(self) -> dict[int, int]:
        """Vraća distribuciju ocjena."""
        counts = self._df["ocjena"].value_counts().to_dict()
        return {int(k): int(v) for k, v in counts.items()}

    def get_term_stats(self, term: str) -> dict:
        """Vraća statistiku za određeni termin."""
        term_df = self._df[self._df["termin"] == term]
        if len(term_df) == 0:
            return {"count": 0, "avg_score": 0, "avg_grade": 0, "pass_rate": 0}

        passed = (term_df["ocjena"] >= 2).sum()
        return {
            "count": len(term_df),
            "avg_score": float(term_df["bodovi"].mean()),
            "avg_grade": float(term_df["ocjena"].mean()),
            "pass_rate": (passed / len(term_df)) * 100,
        }

    def filter_by_term(self, term: str) -> "ExamData":
        """Filtrira podatke po terminu."""
        filtered_df = self._df[self._df["termin"] == term].copy()
        return ExamData(filtered_df, self._source_path)

    def filter_by_grade(self, grade: int) -> "ExamData":
        """Filtrira podatke po ocjeni."""
        filtered_df = self._df[self._df["ocjena"] == grade].copy()
        return ExamData(filtered_df, self._source_path)

    def filter_by_score_range(self, min_score: int, max_score: int) -> "ExamData":
        """Filtrira podatke po rasponu bodova."""
        filtered_df = self._df[
            (self._df["bodovi"] >= min_score) & (self._df["bodovi"] <= max_score)
        ].copy()
        return ExamData(filtered_df, self._source_path)

    def search(self, query: str) -> "ExamData":
        """Pretražuje po imenu ili prezimenu."""
        query = query.lower()
        filtered_df = self._df[
            self._df["ime"].str.lower().str.contains(query, na=False) |
            self._df["prezime"].str.lower().str.contains(query, na=False)
        ].copy()
        return ExamData(filtered_df, self._source_path)

    def __iter__(self) -> Iterator[StudentRecord]:
        """Iterira kroz sve zapise."""
        for _, row in self._df.iterrows():
            yield StudentRecord(
                student_id=int(row["student_id"]),
                first_name=str(row["ime"]),
                last_name=str(row["prezime"]),
                term=str(row["termin"]),
                score=int(row["bodovi"]),
                grade=int(row["ocjena"]),
            )

    def __len__(self) -> int:
        return len(self._df)

    def get_statistics(self) -> dict:
        """Vraća kompletnu statistiku."""
        df = self._df

        # Prazan DataFrame - vrati default vrijednosti
        if len(df) == 0:
            return {
                "count": 0,
                "avg_grade": 0.0,
                "avg_score": 0.0,
                "std_score": 0.0,
                "min_score": 0,
                "max_score": 0,
                "median_score": 0.0,
                "pass_rate": 0.0,
                "passed_count": 0,
                "failed_count": 0,
                "grade_distribution": {},
                "term_stats": {},
            }

        passed = (df["ocjena"] >= 2).sum()

        return {
            "count": len(df),
            "avg_grade": float(df["ocjena"].mean()),
            "avg_score": float(df["bodovi"].mean()),
            "std_score": float(df["bodovi"].std()) if len(df) > 1 else 0.0,
            "min_score": int(df["bodovi"].min()),
            "max_score": int(df["bodovi"].max()),
            "median_score": float(df["bodovi"].median()),
            "pass_rate": (passed / len(df)) * 100,
            "passed_count": int(passed),
            "failed_count": len(df) - int(passed),
            "grade_distribution": self.get_grade_distribution(),
            "term_stats": {term: self.get_term_stats(term) for term in self.terms},
        }
