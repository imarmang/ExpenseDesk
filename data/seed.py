import sqlite3
import random
from faker import Faker
from datetime import datetime, timedelta

fake = Faker()
conn = sqlite3.connect( "database.db" )
cursor = conn.cursor()

# Drop existing tables
cursor.executescript("""
    DROP TABLE IF EXISTS approvals;
    DROP TABLE IF EXISTS expenses;
    DROP TABLE IF EXISTS vendors;
    DROP TABLE IF EXISTS categories;
    DROP TABLE IF EXISTS employees;
    DROP TABLE IF EXISTS departments;
""")

# Schema
cursor.executescript("""
    CREATE TABLE IF NOT EXISTS departments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        manager_id INTEGER
    );

    CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        department_id INTEGER,
        role TEXT,
        FOREIGN KEY (department_id) REFERENCES departments(id)
    );

    CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        budget_limit REAL
    );

    CREATE TABLE IF NOT EXISTS vendors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        contact TEXT,
        payment_terms TEXT
    );

    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        employee_id INTEGER,
        amount REAL NOT NULL,
        category_id INTEGER,
        status TEXT DEFAULT 'pending',
        date TEXT,
        description TEXT,
        FOREIGN KEY (employee_id) REFERENCES employees(id),
        FOREIGN KEY (category_id) REFERENCES categories(id)
    );

    CREATE TABLE IF NOT EXISTS approvals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        expense_id INTEGER,
        approving_employee_id INTEGER,
        approved_at TEXT,
        FOREIGN KEY (expense_id) REFERENCES expenses(id),
        FOREIGN KEY (approving_employee_id) REFERENCES employees(id)
    );
""")

# Config
NUM_DEPARTMENTS  = 20
NUM_EMPLOYEES    = 1500
NUM_CATEGORIES   = 20
NUM_VENDORS      = 1500
NUM_EXPENSES     = 1500
NUM_APPROVALS    = 1500

STATUSES         = ["pending", "approved", "rejected", "under_review"]
PAYMENT_TERMS    = ["Net 15", "Net 30", "Net 45", "Net 60", "Due on receipt"]
EXPENSE_DESCS    = [
    "Flight to client meeting", "Hotel stay for conference",
    "Team lunch", "Office supplies order", "Software subscription",
    "Client dinner", "Equipment purchase", "Training course",
    "Marketing materials", "Travel reimbursement",
    "Cloud service subscription", "Consulting fees",
    "Conference registration", "Team building activity",
    "Printer cartridges", "Standing desk purchase",
    "Monitor purchase", "Keyboard and mouse", "Uber to airport",
    "Train tickets", "Airbnb for offsite", "Catering for meeting",
]

# Departments
department_names = [
    "Engineering", "Marketing", "Sales", "HR", "Finance",
    "Operations", "Legal", "Product", "Design", "Data Science",
    "Customer Success", "IT", "Security", "Research", "DevOps",
    "Business Development", "Procurement", "Compliance", "Support", "Executive"
]

print("Seeding departments...")
for name in department_names[:NUM_DEPARTMENTS]:
    cursor.execute("INSERT INTO departments (name) VALUES (?)", (name,))
conn.commit()
department_ids = [row[0] for row in cursor.execute("SELECT id FROM departments").fetchall()]

# Employees
print("Seeding employees...")
roles = [
    "Software Engineer", "Senior Engineer", "Engineering Manager",
    "Marketing Specialist", "Marketing Manager", "Sales Rep",
    "Sales Manager", "HR Specialist", "HR Manager", "Financial Analyst",
    "Finance Manager", "Product Manager", "Product Designer",
    "Data Scientist", "Data Analyst", "DevOps Engineer",
    "Security Engineer", "Legal Counsel", "Operations Manager",
    "Executive Assistant"
]

employees = []
for _ in range(NUM_EMPLOYEES):
    name = fake.name()
    dept_id = random.choice(department_ids)
    role = random.choice(roles)
    cursor.execute(
        "INSERT INTO employees (name, department_id, role) VALUES (?, ?, ?)",
        (name, dept_id, role)
    )
    employees.append(cursor.lastrowid)
conn.commit()
employee_ids = employees

# Categories
print("Seeding categories...")
category_data = [
    ("Travel",              5000.00),
    ("Office Supplies",      500.00),
    ("Software",            2000.00),
    ("Meals",                300.00),
    ("Equipment",           3000.00),
    ("Training",            1500.00),
    ("Marketing",           4000.00),
    ("Consulting",          8000.00),
    ("Cloud Services",      6000.00),
    ("Legal",               5000.00),
    ("Subscriptions",       1000.00),
    ("Conferences",         3000.00),
    ("Utilities",            800.00),
    ("Printing",             200.00),
    ("Catering",             600.00),
    ("Shipping",             400.00),
    ("Security",            2500.00),
    ("Research",            4500.00),
    ("Recruitment",         3500.00),
    ("Miscellaneous",       1000.00),
]

for name, limit in category_data[:NUM_CATEGORIES]:
    cursor.execute(
        "INSERT INTO categories (name, budget_limit) VALUES (?, ?)",
        (name, limit)
    )
conn.commit()
category_ids = [row[0] for row in cursor.execute("SELECT id FROM categories").fetchall()]

# Vendors
print("Seeding vendors...")
vendors = []
for _ in range(NUM_VENDORS):
    name = fake.company()
    contact = fake.email()
    terms = random.choice(PAYMENT_TERMS)
    cursor.execute(
        "INSERT INTO vendors (name, contact, payment_terms) VALUES (?, ?, ?)",
        (name, contact, terms)
    )
    vendors.append(cursor.lastrowid)
conn.commit()

# Expenses
print("Seeding expenses...")
start_date = datetime(2023, 1, 1)
end_date   = datetime(2025, 1, 1)
date_range = (end_date - start_date).days

expense_ids = []
for _ in range(NUM_EXPENSES):
    employee_id = random.choice(employee_ids)
    amount      = round(random.uniform(10.00, 5000.00), 2)
    category_id = random.choice(category_ids)
    status      = random.choice(STATUSES)
    date        = (start_date + timedelta(days=random.randint(0, date_range))).strftime("%Y-%m-%d")
    description = random.choice(EXPENSE_DESCS)

    cursor.execute(
        "INSERT INTO expenses (employee_id, amount, category_id, status, date, description) VALUES (?, ?, ?, ?, ?, ?)",
        (employee_id, amount, category_id, status, date, description)
    )
    expense_ids.append(cursor.lastrowid)
conn.commit()

# ── Approvals ─────────────────────────────────────────────────
print("Seeding approvals...")
approved_expenses = [eid for eid in expense_ids if random.random() > 0.4][:NUM_APPROVALS]

for expense_id in approved_expenses:
    approving_employee_id = random.choice(employee_ids)
    approved_at = fake.date_time_between(
        start_date="-2y", end_date="now"
    ).strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute(
        "INSERT INTO approvals (expense_id, approving_employee_id, approved_at) VALUES (?, ?, ?)",
        (expense_id, approving_employee_id, approved_at)
    )
conn.commit()
conn.close()

# Summary
print("\n✅ Database seeded successfully")
print(f"   departments  → {NUM_DEPARTMENTS} rows")
print(f"   employees    → {NUM_EMPLOYEES} rows")
print(f"   categories   → {NUM_CATEGORIES} rows")
print(f"   vendors      → {NUM_VENDORS} rows")
print(f"   expenses     → {NUM_EXPENSES} rows")
print(f"   approvals    → up to {NUM_APPROVALS} rows")