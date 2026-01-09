"""Modul za rad s podacima."""

from .generator import DataGenerator
from .loader import DataLoader
from .models import StudentRecord, ExamData

__all__ = ["DataGenerator", "DataLoader", "StudentRecord", "ExamData"]
