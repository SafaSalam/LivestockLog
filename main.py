import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

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

def update_costs(animal_id, food_cost, hr_cost):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE animals
        SET total_food_cost = total_food_cost + ?,
            total_hr_cost = total_hr_cost + ?
        WHERE animal_id = ?
    ''', (food_cost, hr_cost, animal_id))
    conn.commit()
    conn.close()

def finalize_animal(animal_id, final_weight, final_cost):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE animals
        SET final_weight = ?, final_cost = ?
        WHERE animal_id = ?
    ''', (final_weight, final_cost, animal_id))
    conn.commit()
    conn.close()

def fetch_data():
    conn = connect_db()
    df = pd.read_sql_query('SELECT * FROM animals', conn)
    conn.close()
    return df

# Streamlit App
st.title("Livestock Log")

tab1, tab2, tab3, tab4, tab5 = st.tabs(["Add Animal", "Daily Costs", "Finalize Animal", "View Summary","Delete Animal"])


with tab1:
    st.header("Add a New Animal")
    animal_id = st.text_input("Animal ID")
    weight = st.number_input("Initial Weight (kg)", min_value=0.0)
    cost = st.number_input("Initial Cost (PKR)", min_value=0.0)
    date = st.date_input("Purchase Date")
    if st.button("Add Animal"):
        add_animal(animal_id, weight, cost, date)
        st.success("Animal added successfully!")

with tab2:
    st.header("Add Daily Costs")
    animal_id = st.text_input("Enter Animal ID")
    food_cost = st.number_input("Daily Food Cost (PKR)", min_value=0.0)
    hr_cost = st.number_input("Daily HR Cost (PKR)", min_value=0.0)
    if st.button("Update Costs"):
        update_costs(animal_id, food_cost, hr_cost)
        st.success("Costs updated successfully!")

with tab3:
    st.header("Finalize Animal")
    animal_id = st.text_input("Animal ID to Finalize")
    final_weight = st.number_input("Final Weight (kg)", min_value=0.0)
    final_cost = st.number_input("Final Cost (PKR)", min_value=0.0)
    if st.button("Finalize"):
        finalize_animal(animal_id, final_weight, final_cost)
        st.success("Animal finalized successfully!")

with tab4:
    st.header("Animal Summary and Profit")
    df = fetch_data()
    
    if not df.empty:
        df['Total Expenses'] = df['initial_cost'] + df['total_food_cost'] + df['total_hr_cost']
        df['Profit'] = df['final_cost'] - df['Total Expenses']
        
        st.write(df)

        st.subheader("Profit Overview")
        fig = px.bar(df, x='animal_id', y='Profit', title="Profit per Animal", labels={'animal_id': 'Animal ID', 'Profit': 'Profit (PKR)'})
        st.plotly_chart(fig)

        st.subheader("Total Expenses vs Final Cost")
        fig2 = px.scatter(df, x='Total Expenses', y='final_cost', color='Profit', hover_data=['animal_id'],
                          title="Comparison of Total Expenses and Final Cost")
        st.plotly_chart(fig2)

        st.download_button("Download Data as CSV", df.to_csv(index=False), file_name="farm_data.csv")
    else:
        st.info("No data available.")


with tab5:
    st.header("Delete Animal")
    animal_id_to_delete = st.text_input("Enter Animal ID to Delete")
    if st.button("Delete Animal"):
        delete_animal(animal_id_to_delete)
        st.success(f"Animal with ID {animal_id_to_delete} deleted successfully!")