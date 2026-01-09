"""Učitavanje i validacija CSV podataka."""

import pandas as pd
from pathlib import Path
from typing import ClassVar

from .models import ExamData


class DataValidationError(Exception):
    """Greška pri validaciji podataka."""
    pass


class DataLoader:
    """Učitava i validira CSV podatke studenata."""

    REQUIRED_COLUMNS: ClassVar[set[str]] = {
        "student_id", "ime", "prezime", "termin", "bodovi", "ocjena"
    }

    COLUMN_ALIASES: ClassVar[dict[str, list[str]]] = {
        "student_id": ["id", "student_id", "studentid", "šifra"],
        "ime": ["ime", "first_name", "firstname", "name"],
        "prezime": ["prezime", "last_name", "lastname", "surname"],
        "termin": ["termin", "term", "datum", "date", "ispitni_rok"],
        "bodovi": ["bodovi", "score", "points", "bod"],
        "ocjena": ["ocjena", "grade", "ocj"],
    }

    @classmethod
    def _normalize_columns(cls, df: pd.DataFrame) -> pd.DataFrame:
        """Normalizira nazive stupaca."""
        column_mapping = {}
        df_columns_lower = {col.lower(): col for col in df.columns}

        for standard_name, aliases in cls.COLUMN_ALIASES.items():
            for alias in aliases:
                if alias.lower() in df_columns_lower:
                    original_col = df_columns_lower[alias.lower()]
                    column_mapping[original_col] = standard_name
                    break

        return df.rename(columns=column_mapping)

    @classmethod
    def _validate(cls, df: pd.DataFrame, path: str) -> None:
        """Validira DataFrame."""
        # Provjeri da postoje svi potrebni stupci
        missing = cls.REQUIRED_COLUMNS - set(df.columns)
        if missing:
            raise DataValidationError(
                f"Nedostaju stupci u '{path}': {', '.join(missing)}\n"
                f"Potrebni stupci: {', '.join(cls.REQUIRED_COLUMNS)}\n"
                f"Pronađeni stupci: {', '.join(df.columns)}"
            )

        # Provjeri tipove podataka
        if df["bodovi"].dtype not in ["int64", "float64", "int32", "float32"]:
            try:
                df["bodovi"] = pd.to_numeric(df["bodovi"], errors="coerce")
                if df["bodovi"].isna().any():
                    raise DataValidationError(
                        f"Stupac 'bodovi' sadrži nevažeće vrijednosti."
                    )
            except Exception as e:
                raise DataValidationError(f"Stupac 'bodovi' mora biti numerički: {e}")

        if df["ocjena"].dtype not in ["int64", "int32"]:
            try:
                df["ocjena"] = df["ocjena"].astype(int)
            except Exception as e:
                raise DataValidationError(f"Stupac 'ocjena' mora biti cijeli broj: {e}")

        # Provjeri raspon vrijednosti
        if (df["bodovi"] < 0).any() or (df["bodovi"] > 100).any():
            raise DataValidationError("Bodovi moraju biti u rasponu 0-100.")

        if (df["ocjena"] < 1).any() or (df["ocjena"] > 5).any():
            raise DataValidationError("Ocjene moraju biti u rasponu 1-5.")

        # Provjeri praznine
        for col in ["ime", "prezime", "termin"]:
            if df[col].isna().any() or (df[col] == "").any():
                raise DataValidationError(f"Stupac '{col}' ne smije imati prazne vrijednosti.")

    @classmethod
    def load(cls, path: str) -> ExamData:
        """
        Učitava CSV datoteku.

        Args:
            path: Putanja do CSV datoteke

        Returns:
            ExamData objekt s učitanim podacima

        Raises:
            FileNotFoundError: Ako datoteka ne postoji
            DataValidationError: Ako su podaci neispravni
        """
        path_obj = Path(path)

        if not path_obj.exists():
            raise FileNotFoundError(f"Datoteka '{path}' ne postoji.")

        if not path_obj.suffix.lower() == ".csv":
            raise DataValidationError(f"Datoteka mora biti CSV format, ne '{path_obj.suffix}'.")

        try:
            df = pd.read_csv(path, encoding="utf-8")
        except UnicodeDecodeError:
            # Pokušaj s drugim encodingom
            df = pd.read_csv(path, encoding="latin-1")
        except Exception as e:
            raise DataValidationError(f"Greška pri čitanju CSV datoteke: {e}")

        if df.empty:
            raise DataValidationError("CSV datoteka je prazna.")

        # Normaliziraj nazive stupaca
        df = cls._normalize_columns(df)

        # Validiraj
        cls._validate(df, path)

        # Osiguraj tipove
        df["bodovi"] = df["bodovi"].astype(int)
        df["ocjena"] = df["ocjena"].astype(int)

        return ExamData(df, path)

    @classmethod
    def can_load(cls, path: str) -> tuple[bool, str]:
        """
        Provjerava može li se datoteka učitati.

        Returns:
            Tuple (uspjeh, poruka)
        """
        try:
            cls.load(path)
            return True, "OK"
        except FileNotFoundError as e:
            return False, str(e)
        except DataValidationError as e:
            return False, str(e)
        except Exception as e:
            return False, f"Neočekivana greška: {e}"
