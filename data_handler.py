import streamlit as st
import pandas as pd
from supabase_client import get_supabase_client

supabase = get_supabase_client()

def process_sales_data(file, user_id):
    try:
        # Read the uploaded file into a DataFrame
        if file.name.endswith('.csv'):
            data = pd.read_csv(file)
        elif file.name.endswith('.xlsx'):
            data = pd.read_excel(file)
        else:
            return {"success": False, "message": "Unsupported file format"}

        # Ensure the file has the necessary columns
        required_columns = ['date', 'product', 'quantity', 'price']
        if not all(column in data.columns for column in required_columns):
            return {"success": False, "message": "File is missing required columns"}

        # Insert data into the `sales_data` table, linked by `user_id`
        for _, row in data.iterrows():
            supabase.table('sales_data').insert({
                "user_id": user_id,
                "date": row['date'],
                "product": row['product'],
                "quantity": row['quantity'],
                "price": row['price']
            }).execute()

        return {"success": True, "message": "Sales data uploaded successfully"}
    except Exception as e:
        print(f"Error: {e}")
        return {"success": False, "message": str(e)}

def fetch_user_sales_data(user_id):
    try:
        # Fetch sales data only for the logged-in user
        response = supabase.table('sales_data').select("*").eq("user_id", user_id).execute()
        return response.data
    except Exception as e:
        print(f"Error: {e}")
        return []

def display_user_data(user_id, section_title, no_data_message):
    """
    Fetches and displays data specific to the logged-in user.
    
    Args:
        user_id (str): ID of the logged-in user.
        section_title (str): Title to display before showing data.
        no_data_message (str): Message to show if no data is found.
    
    Returns:
        DataFrame if data is found, otherwise None.
    """
    data = fetch_user_sales_data(user_id)
    if data:
        df = pd.DataFrame(data)
        st.write(section_title)
        st.dataframe(df)
        return df
    else:
        st.write(no_data_message)
        return None
