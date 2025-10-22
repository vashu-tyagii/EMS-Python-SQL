# Employee Management System (CLI)

## Overview

This is a simple Command-Line Interface (CLI) application for managing employee records. It connects to a **MySQL** database to perform standard CRUD operations (Create, Read, Update, Delete) on employee data.

The application is written in Python and uses the `mysql.connector` library for database interaction.

---

## Features

* **Add Employee:** Records new employees, defaulting the `hired` date to the current day if none is provided.
* **View Employees:** Displays a table of all employees, including their ID, name, department, position, salary, and hire date.
* **Search Employees:** Allows searching records by name or department.
* **Update Employee:** Modifies employee records based on ID.
* **Delete Employee:** Permanently removes an employee record.

---

## Setup and Prerequisites

To run this application, you must have **Python 3** and a running **MySQL server** instance.

### 1. Database Configuration

The script connects to a database named `employee_management_system` using hardcoded credentials. **You must ensure your MySQL server is running** and that a user with the specified credentials exists.

**Current Hardcoded Connection Details:**

| Parameter | Value |
| :--- | :--- |
| **Host** | `localhost` |
| **User** | `root` |
| **Password** | `Vashu@Tyagi` |
| **Database** | `employee_management_system` |

**You must manually create the database first:**

```sql
CREATE DATABASE employee_management_system;