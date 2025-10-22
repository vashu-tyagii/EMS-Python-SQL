# import specific mysql error classes for exception handling
import mysql.connector
import datetime  # for date handling (e.g., today)
from os import system  # to call system clear/cls for console UI
import mysql.connector  # main MySQL connector library
import sys  # to check platform for clearing screen

conn = mysql.connector.connect(
    host="localhost",  # database host
    user="root",  # database user
    password="Vashu@Tyagi",  # database password (consider moving to env var)
    database="employee_management_system"  # database name
)

cursor = conn.cursor()  # create a cursor object for executing queries


def init_db():
    # create the employees table if it doesn't exist
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS employees (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                age INT,
                department VARCHAR(100),
                position VARCHAR(100),
                salary DECIMAL(12,2),
                hired DATE
            )
        """)
        conn.commit()  # commit schema change
    except mysql.connector.errors.Error as e:
        print("Database error:", e)  # print error if table creation fails
        raise  # re-raise to allow outer handlers to respond


def add_employee():
    # clear screen at function start
    system("cls" if sys.platform == "win32" else "clear")
    try:
        name = input("Name: ").strip()  # prompt for name and strip whitespace
        age = input("Age: ").strip()  # prompt for age (may be empty)
        dept = input("Department: ").strip()  # prompt for department
        position = input("Position: ").strip()  # prompt for position
        salary = input("Salary: ").strip()  # prompt for salary
        hired = input(
            # optional hired date
            "Hired date (YYYY-MM-DD) [leave empty = today]: ").strip()
        if not hired:
            hired = datetime.date.today().isoformat()  # default to today's date if empty
        # insert new employee, converting inputs to proper types or None when empty
        cursor.execute(
            "INSERT INTO employees (name, age, department, position, salary, hired) VALUES (%s, %s, %s, %s, %s, %s)",
            (name or None, int(age) if age else None, dept or None,
             position or None, float(salary) if salary else None, hired or None)
        )
        conn.commit()  # commit the insert
        print("Employee added with id :", cursor.lastrowid)  # show new id
        # pause so user can read result
        press = input("\nPress Enter to continue...")
        # clear screen after pause
        system("cls" if sys.platform == "win32" else "clear")
    except Exception as e:
        conn.rollback()  # rollback on error
        print("Failed to add employee:", e)  # show error
        press = input("\nPress Enter to continue...")  # pause before returning
        system("cls" if sys.platform == "win32" else "clear")  # clear screen


def view_employees():
    system("cls" if sys.platform == "win32" else "clear")  # clear screen
    try:
        cursor.execute(
            # FIX 1: Change 'hired_date' to 'hired'
            "SELECT id, name, age, department, position, salary, hired FROM employees ORDER BY id")
        rows = cursor.fetchall()  # get all rows

        if not rows:
            print("No employees found.")  # inform if none
            press = input("\nPress Enter to continue...")  # pause
            system("cls" if sys.platform == "win32" else "clear")  # clear
            return  # return to menu

        # FIX 2: Add 'Position' and 'Hired' to the header
        print("{:<5} {:<20} {:<5} {:<15} {:<15} {:<10} {:<12}".format(
            "ID", "Name", "Age", "Department", "Position", "Salary", "Hired"))

        for r in rows:
            hired_date_str = str(r[6]) if r[6] else ""  # r[6] is 'hired'
            # FIX 3: Output all 7 fields (r[6] for hired date)
            print("{:<5} {:<20} {:<5} {:<15} {:<15} {:<10} {:<12}".format(
                r[0], r[1] or "", r[2] or "", r[3] or "", r[4] or "", r[5] or "", hired_date_str))

        press = input("\nPress Enter to continue...")  # pause after listing
        system("cls" if sys.platform == "win32" else "clear")  # clear screen

    except Exception as e:
        print("Failed to fetch employees:", e)  # show error
        press = input("\nPress Enter to continue...")  # pause
        system("cls" if sys.platform == "win32" else "clear")  # clear


def search_employee():
    system("cls" if sys.platform == "win32" else "clear")  # clear screen
    term = input("Search by name or department: ").strip()  # get search term
    try:
        like = "%" + term + "%"  # prepare LIKE pattern
        cursor.execute(
            # FIX 1: Add 'position' back and change 'hired_date' to 'hired'
            "SELECT id, name, age, department, position, salary, hired FROM employees WHERE name LIKE %s OR department LIKE %s", (like, like))
        rows = cursor.fetchall()  # fetch matches

        if not rows:
            print("No matches.")  # inform if none
            press = input("\nPress Enter to continue...")  # pause
            system("cls" if sys.platform == "win32" else "clear")  # clear
            return

        # FIX 2: Adjust header for all 7 selected columns
        print("{:<5} {:<20} {:<5} {:<15} {:<15} {:<10} {:<12}".format(
            "ID", "Name", "Age", "Department", "Position", "Salary", "Hired"))

        for r in rows:
            hired_date_str = str(r[6]) if r[6] else ""  # r[6] is 'hired'
            # FIX 3: Output all 7 fields
            print("{:<5} {:<20} {:<5} {:<15} {:<15} {:<10} {:<12}".format(
                r[0], r[1] or "", r[2] or "", r[3] or "", r[4] or "", r[5] or "", hired_date_str))

        # pause after showing results
        press = input("\nPress Enter to continue...")
        system("cls" if sys.platform == "win32" else "clear")  # clear screen
    except Exception as e:
        print("Search failed:", e)  # show error
        press = input("\nPress Enter to continue...")  # pause
        system("cls" if sys.platform == "win32" else "clear")  # clear


def update_employee():
    system("cls" if sys.platform == "win32" else "clear")  # clear screen
    try:
        # get employee id to update
        eid = input("Employee ID to update: ").strip()
        if not eid.isdigit():
            print("Invalid ID")  # validate id is numeric
            press = input("\nPress Enter to continue...")  # pause
            system("cls" if sys.platform == "win32" else "clear")
            return

        cursor.execute("SELECT id FROM employees WHERE id=%s",
                       (int(eid),))  # check existence

        if not cursor.fetchone():
            print("Employee not found.")  # inform if missing
            press = input("\nPress Enter to continue...")  # pause
            system("cls" if sys.platform == "win32" else "clear")
            return

        # prompt for new values (blank -> keep current)
        name = input("New name [leave blank to keep]: ").strip()
        age = input("New age [leave blank to keep]: ").strip()
        dept = input("New department [leave blank to keep]: ").strip()
        # FIX: Add position update prompt (missing from your original function)
        position = input("New position [leave blank to keep]: ").strip()
        salary = input("New salary [leave blank to keep]: ").strip()
        hired = input(
            "New hired date (YYYY-MM-DD) [leave blank to keep]: ").strip()

        fields, vals = [], []  # prepare parts of the SET clause and values

        if name:
            fields.append("name=%s")
            vals.append(name)
        if age:
            fields.append("age=%s")
            vals.append(int(age))
        if dept:
            fields.append("department=%s")
            vals.append(dept)
        # FIX: Include logic for updating the 'position' column
        if position:
            fields.append("position=%s")
            vals.append(position)
        if salary:
            fields.append("salary=%s")
            vals.append(float(salary))
        if hired:
            # FIX 4: Change 'hired_date=%s' to 'hired=%s'
            fields.append("hired=%s")
            vals.append(hired)

        if not fields:
            print("Nothing to update.")  # nothing provided -> abort
            press = input("\nPress Enter to continue...")  # pause
            system("cls" if sys.platform == "win32" else "clear")
            return

        vals.append(int(eid))  # add id for WHERE clause
        sql = "UPDATE employees SET " + \
            ", ".join(fields) + " WHERE id=%s"  # build update SQL

        cursor.execute(sql, tuple(vals))  # execute update
        conn.commit()  # commit changes
        print("Updated.")  # success message
        press = input("\nPress Enter to continue...")  # pause
        system("cls" if sys.platform == "win32" else "clear")  # clear screen

    except Exception as e:
        conn.rollback()  # rollback on error
        print("Update failed:", e)  # show error
        press = input("\nPress Enter to continue...")  # pause
        system("cls" if sys.platform == "win32" else "clear")  # clear


def delete_employee():
    system("cls" if sys.platform == "win32" else "clear")  # clear screen
    try:
        eid = input("Employee ID to delete: ").strip()  # prompt for id
        if not eid.isdigit():
            print("Invalid ID")  # validate
            press = input("\nPress Enter to continue...")  # pause
            system("cls" if sys.platform == "win32" else "clear")
            return
        confirm = input(
            # confirm destructive action
            f"Are you sure you want to delete employee {eid}? (y/N): ").strip().lower()
        if confirm != "y":
            print("Aborted.")  # if not confirmed, abort
            press = input("\nPress Enter to continue...")  # pause
            system("cls" if sys.platform == "win32" else "clear")
            return
        cursor.execute("DELETE FROM employees WHERE id=%s",
                       (int(eid),))  # perform delete
        conn.commit()  # commit deletion
        # indicate completion (may not have existed)
        print("Deleted (if existed).")
        press = input("\nPress Enter to continue...")  # pause
        system("cls" if sys.platform == "win32" else "clear")  # clear screen
    except Exception as e:
        conn.rollback()  # rollback on error
        print("Delete failed:", e)  # show error
        press = input("\nPress Enter to continue...")  # pause
        system("cls" if sys.platform == "win32" else "clear")  # clear


def main():
    # clear on program start
    system("cls" if sys.platform == "win32" else "clear")
    try:
        init_db()  # ensure DB table exists
        while True:
            # print menu
            print("|----------------------------|")
            print("| EMPLOYEE MANAGEMENT SYSTEM |")
            print("|----------------------------|")
            print("1) Add employee")
            print("2) View employees")
            print("3) Search employees")
            print("4) Update employee")
            print("5) Delete employee")
            print("0) Exit")
            choice = input("Choose: ").strip()  # get user choice
            if choice == "1":
                add_employee()  # add
            elif choice == "2":
                view_employees()  # view
            elif choice == "3":
                search_employee()  # search
            elif choice == "4":
                update_employee()  # update
            elif choice == "5":
                delete_employee()  # delete
            elif choice == "0":
                system("cls" if sys.platform == "win32" else "clear")  # clear
                break  # exit loop/program
            else:
                print("Invalid option.")  # invalid input -> show message
    finally:
        try:
            cursor.close()  # try to close cursor
            conn.close()  # try to close connection
        except:
            pass  # ignore any errors while closing


if __name__ == "__main__":
    main()  # run main when executed as a script
