import sqlite3
from staff import Employee
from datetime import datetime
import hashlib

# Database operations
#--------------------------------------------------------------------------------------------
def init_db(db_name):
    connection = sqlite3.connect(db_name)
    return connection

# Employee Operations
#--------------------------------------------------------------------------------------------
def add_employee(employee, connection):
    cursor = connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS employees (
        id TEXT PRIMARY KEY,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        salary REAL NOT NULL,
        hire_date DATE NOT NULL,
        tenure INTEGER NOT NULL
    )
    ''')

    tenure = datetime.now().year - employee.hire_date.year

    with connection:  # Automatically commits the transaction
        cursor.execute('''
            INSERT INTO employees (id, first_name, last_name, salary, hire_date, tenure)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (create_id(employee), employee.firstName, employee.lastName, employee.salary, employee.hire_date, tenure))     

def print_all_employees(connection):
    cursor = connection.cursor()
    cursor.execute('''SELECT * FROM employees''')
    employees = cursor.fetchall()

    if not employees:
        print("No employees found in the database.")
        return

    print("\n=== Employee Database ===")
    for employee in employees:
        id, first_name, last_name, salary, hire_date, tenure = employee
 
        print(f"ID: {id[:8]}...")  # Display first 8 characters of the ID
        print(f"Name: {first_name} {last_name}")
        print(f"Salary: ${salary:.2f}")
        print(f"Hire Date: {hire_date.split()[0]}")  # Only display the date part
        print(f"Tenure: {tenure} years")
        print("-" * 30)

    print(f"Total Employees: {len(employees)}")

def delete_employee(connection, partial_id):
    cursor = connection.cursor()
    cursor.execute('''
    DELETE FROM employees
    WHERE id LIKE ?
    ''', (partial_id + '%',))
    
    if cursor.rowcount == 0:
        print(f"No employee found with ID starting with {partial_id}")
    else:
        print(f"Employee with ID starting with {partial_id} has been deleted")
    
    connection.commit()

# Employee operations
def create_employee():
    print("Creating New Employee:")
    f_name = input("Enter New Employee's first Name: ")
    l_name = input("Enter New Employee's last name: ")
    hire_date = input("Enter New Employee's hire date (mm/dd/yyyy): ")
    salary = float(input("Enter New Employee's salary: $"))  # Cast salary to float

    hire_date = datetime.strptime(hire_date,'%m/%d/%Y')

    newEmp = Employee(firstName=f_name, lastName=l_name, salary=salary, hire_date=hire_date)

    return newEmp

def create_id(employee):
    # Using SHA256 to generate a stable hash for employee IDs
    full_name = employee.firstName + employee.lastName
    return hashlib.sha256(full_name.encode()).hexdigest()

# User interface operations
def print_prompt():
    print('''
    ===============================================================
    ||  Welcome to Oskur's Superior Employee Management System!  ||
    ===============================================================
    ||  Enter from the following choices:                        ||
    ||  1) View Employee Database                                ||
    ||  2) Add New Employee                                      ||
    ||  3) Delete Employee                                       ||
    ||  4) Exit                                                  ||
    ===============================================================
    ''')

def get_user_choice():
    while True:
        try:
            choice = int(input())
            return choice
        except ValueError:
            print('Please enter a valid numerical choice from the given options!')

# Main program flow
def main():
    conn = init_db('staff.db')
    try:
        while True:  # Loop to return to the menu after each operation
            print_prompt()
            choice = get_user_choice()
            if choice == 1:
                print_all_employees(conn)
            elif choice == 2:
                new_employee = create_employee()
                add_employee(new_employee, conn)
            elif choice == 3:
                partial_id = input("Enter the first 8 characters of the employee ID to delete: ")
                delete_employee(conn, partial_id)
            elif choice == 4:
                print("Exiting the Employee Management System. Goodbye!")
                break
            else:
                print("Invalid choice. Please select from the available options.")
    finally:
        conn.close()  # Ensure the connection is always closed

if __name__ == '__main__':
    main()
