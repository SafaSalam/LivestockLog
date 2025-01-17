import streamlit as st
import sqlite3
import pandas as pd

def connect_db():
    conn = sqlite3.connect('farm.db')
    return conn

def add_animal(animal_id, weight, cost, date):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO animals (animal_id, initial_weight, initial_cost, purchase_date)
        VALUES (?, ?, ?, ?)
    ''', (animal_id, weight, cost, date))
    conn.commit()
    conn.close()