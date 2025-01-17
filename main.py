import streamlit as st
import sqlite3
import pandas as pd

def connect_db():
    conn = sqlite3.connect('farm.db')
    return conn
