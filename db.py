import sqlite3

conn = sqlite3.connect('farm.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS animals (
    id INTEGER PRIMARY KEY,
    animal_id TEXT,
    initial_weight REAL,
    initial_cost REAL,
    purchase_date TEXT,
    total_food_cost REAL DEFAULT 0,
    total_hr_cost REAL DEFAULT 0,
    final_weight REAL DEFAULT NULL,
    final_cost REAL DEFAULT NULL
)
''')
conn.commit()
conn.close()