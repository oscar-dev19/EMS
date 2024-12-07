from dataclasses import dataclass, field
from datetime import datetime
from typing import List


@dataclass
class Employee:
    emp_id : str
    firstName: str
    lastName: str
    hire_date: datetime
    salary: float


    @property
    def tenure(self) -> int:
        return datetime.now.year() - self.hire_date.year

    def __repr__(self):
        return (
        f"ID: {emp_id[:8]}...\n"  # Display the first 8 characters of the ID
        f"Name: {self.firstName} {self.lastName}\n"
        f"Salary: ${self.salary:.2f}\n"
        f"Hire Date: {self.hire_date.strftime('%Y-%m-%d')}\n"  # Format the hire date
        f"Tenure: {tenure} years"
        )

@dataclass
class Manager(Employee):
    department: str
    managed_employees: List[Employee] = field(default_factory=list)



