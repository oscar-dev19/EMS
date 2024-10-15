from dataclasses import dataclass
from datetime import datetime


@dataclass
class Employee:
    firstName: str
    lastName: str
    hire_date: datetime
    salary: float


