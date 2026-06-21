from sqlmodel import create_engine
from sqlalchemy import text
from dotenv import load_dotenv
import os

load_dotenv()

engine = create_engine(os.getenv("PG_DSN"))
print("Engine created:", engine)

with engine.connect() as conn:
    conn.execute(text("""
    CREATE TABLE IF NOT EXISTS departments(
        id SERIAL PRIMARY KEY,
        name VARCHAR(50) NOT NULL,
        location VARCHAR(50) NOT NULL
        );
    """))
    conn.commit()

print("departments table created.")

with engine.connect() as conn:
    conn.execute(text("""
    CREATE TABLE IF NOT EXISTS hw_employees (
        id SERIAL PRIMARY KEY,
        full_name VARCHAR(100) NOT NULL,
        department_id INTEGER REFERENCES departments(id),
        salary INTEGER NOT NULL CHECK (salary > 0),
        country VARCHAR(50) NOT NULL
    );
    """))
    conn.commit()

print("hw_employees table created.")


with engine.connect() as conn:
    conn.execute(text("""
        INSERT INTO departments (name, location) VALUES
        ('Engineering', 'Istanbul'),
        ('Sales', 'Ankara'),
        ('Finance', 'Izmir'),
        ('HR', 'Bursa');
     """))
    conn.commit()
    print("departments seeded.")

with engine.connect() as conn:
    conn.execute(text("""
        INSERT INTO hw_employees (full_name, department_id, salary, country) VALUES
        ('Alice Johnson', 1, 95000, 'Turkey'),
        ('Bob Smith', 1, 110000, 'Turkey'),
        ('Diana Prince', 1, 125000, 'USA'),
        ('Charlie Brown', 2, 70000, 'Turkey'),
        ('Eve Adams', 2, 82000, 'Germany'),
        ('Frank Castle', 3, 98000, 'USA'),
        ('Grace Hopper', 3, 115000, 'USA'),
        ('Henry Ford', 4, 67000, 'Turkey'),
        ('Ivy Chen', 4, 71000, 'Canada');
    """))
    conn.commit()

print("hw_employees seeded.")