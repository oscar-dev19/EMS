from dataclasses import dataclass, field
from datetime import datetime
from typing import List


@dataclass
class Employee:
    firstName: str
    lastName: str
    hire_date: datetime
    salary: float



@dataclass
class Manager(Employee):
    department: str
    managed_employees: List[Employee] = field(default_factory=list)



