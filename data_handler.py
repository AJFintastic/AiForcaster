import streamlit as st
import pandas as pd
import numpy as np
from io import StringIO
from forecasting import apply_forecasting

# Templates for Forecasting Data
TEMPLATES = {
    "Sales": pd.DataFrame({"date": [], "product": [], "sales_quantity": [], "price": []}),
    "Stocks": pd.DataFrame({"date": [], "ticker": [], "open": [], "close": [], "volume": []}),
    "Commodities": pd.DataFrame({"date": [], "commodity": [], "price": [], "volume": []}),
    "Custom": pd.DataFrame({"date": [], "category": [], "value": []})
}

# Section for Downloading Data Templates
def display_template_download_section():
    st.subheader("Download Data Template")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.download_button("Download Sales Template", data=download_template("Sales"), file_name="Sales_template.csv", mime="text/csv")
    with col2:
        st.download_button("Download Stocks Template", data=download_template("Stocks"), file_name="Stocks_template.csv", mime="text/csv")
    with col3:
        st.download_button("Download Commodities Template", data=download_template("Commodities"), file_name="Commodities_template.csv", mime="text/csv")
    with col4:
        st.download_button("Download Custom Template", data=download_template("Custom"), file_name="Custom_template.csv", mime="text/csv")

# Helper function to download template
def download_template(template_name):
    buffer = StringIO()
    TEMPLATES[template_name].to_csv(buffer, index=False)
    buffer.seek(0)
    return buffer.getvalue()

# Main function to handle data transformations
def process_uploaded_data(file):
    if file.name.endswith('.csv'):
        data = pd.read_csv(file)
    elif file.name.endswith('.xlsx'):
        data = pd.read_excel(file)
    else:
        st.error("Unsupported file format. Please upload a CSV or Excel file.")
        return None

    # Initial data cleaning
    data.dropna(how='all', inplace=True)
    data.drop_duplicates(inplace=True)
    data.reset_index(drop=True, inplace=True)

    st.subheader("Data Cleaning and Transformation Options")
    operations = ["Fill Missing Values", "Remove Blanks", "Remove Columns",
                  "Add Column(s)", "Add Calculations", "Normalize Data",
                  "Calculate Statistics", "Transform Dates", "Rename Columns"]

    # Display transformation options in rows of 3
    for i in range(0, len(operations), 3):
        cols = st.columns(3)
        for idx, op in enumerate(operations[i:i + 3]):
            with cols[idx]:
                if st.button(op):
                    if op == "Fill Missing Values":
                        data = fill_missing_values(data)
                    elif op == "Remove Blanks":
                        data = remove_blanks(data)
                    elif op == "Remove Columns":
                        data = remove_columns(data)
                    elif op == "Add Column(s)":
                        data = add_columns(data)
                    elif op == "Add Calculations":
                        data = add_calculations(data)
                    elif op == "Normalize Data":
                        data = normalize_data(data)
                        st.success("Data normalized.")
                    elif op == "Calculate Statistics":
                        calculate_statistics(data)
                    elif op == "Transform Dates":
                        data = transform_dates(data)
                    elif op == "Rename Columns":
                        data = rename_columns(data)

                    st.write("Transformed Data Preview:")
                    st.dataframe(data.head())

    # Forecasting options - models only run when "Run Model" is clicked
    st.subheader("Forecasting Options")
    apply_forecasting(data)

    return data

# Transformation functions remain the same
def fill_missing_values(data):
    st.subheader("Fill Missing Values")
    fill_method = st.selectbox("Fill method", ["Mean", "Median", "Mode", "Custom Value"])
    numeric_cols = data.select_dtypes(include=[np.number]).columns

    if fill_method == "Custom Value":
        fill_value = st.text_input("Enter custom fill value:")
        if st.button("Apply Custom Fill"):
            data.fillna(fill_value, inplace=True)
    else:
        if st.button(f"Apply {fill_method} Fill"):
            if fill_method == "Mean":
                data[numeric_cols] = data[numeric_cols].fillna(data[numeric_cols].mean())
            elif fill_method == "Median":
                data[numeric_cols] = data[numeric_cols].fillna(data[numeric_cols].median())
            elif fill_method == "Mode":
                data = data.fillna(data.mode().iloc[0])
    return data

# Other transformation functions (remove_blanks, remove_columns, add_columns, etc.) remain unchanged


def remove_blanks(data):
    if st.button("Remove Blank Rows and Columns"):
        data.dropna(how='all', inplace=True)
        data.dropna(axis=1, how='all', inplace=True)
        st.success("All blank rows and columns removed.")
    return data

def remove_columns(data):
    cols_to_remove = st.multiselect("Select columns to remove", data.columns)
    if st.button("Remove Selected Columns"):
        data.drop(columns=cols_to_remove, inplace=True)
        st.success("Selected columns removed.")
    return data

def add_columns(data):
    new_col_name = st.text_input("New column name")
    default_value = st.text_input("Default value for new column")
    if st.button("Add Column"):
        data[new_col_name] = default_value
        st.success(f"Column '{new_col_name}' added with default value '{default_value}'.")
    return data

def add_calculations(data):
    calc_type = st.selectbox("Choose calculation type", ["Rolling Average", "Growth Percentage", "Cumulative Sum"])
    numeric_cols = data.select_dtypes(include=[np.number]).columns
    target_col = st.selectbox("Select target column for calculation", numeric_cols)

    if calc_type == "Rolling Average":
        window = st.number_input("Window size", min_value=1, step=1, value=3)
        if st.button("Apply Rolling Average"):
            data[f"{target_col}_rolling_avg"] = data[target_col].rolling(window=window).mean()
            st.success(f"Rolling average with window size {window} added to '{target_col}'.")
    elif calc_type == "Growth Percentage":
        if st.button("Calculate Growth Percentage"):
            data[f"{target_col}_growth_pct"] = data[target_col].pct_change() * 100
            st.success(f"Growth percentage calculated for '{target_col}'.")
    elif calc_type == "Cumulative Sum":
        if st.button("Calculate Cumulative Sum"):
            data[f"{target_col}_cumsum"] = data[target_col].cumsum()
            st.success(f"Cumulative sum calculated for '{target_col}'.")
    return data

def normalize_data(data):
    numeric_cols = data.select_dtypes(include=[np.number]).columns
    data[numeric_cols] = (data[numeric_cols] - data[numeric_cols].mean()) / data[numeric_cols].std()
    st.success("Data normalized.")
    return data

def calculate_statistics(data):
    st.write("Statistical Summary:")
    st.write(data.describe())
    return data  # No modification, but return data for consistency

def transform_dates(data):
    date_cols = data.select_dtypes(include=['object', 'datetime']).columns
    if len(date_cols) > 0:
        selected_col = st.selectbox("Select date column to transform", date_cols)
        if st.button("Transform Date Column"):
            data[selected_col] = pd.to_datetime(data[selected_col], errors='coerce')
            st.success(f"Date column '{selected_col}' transformed to datetime.")
    else:
        st.warning("No date columns available to transform.")
    return data

def rename_columns(data):
    selected_col = st.selectbox("Select column to rename", data.columns)
    new_name = st.text_input("New column name")
    if st.button("Rename Column"):
        data.rename(columns={selected_col: new_name}, inplace=True)
        st.success(f"Column '{selected_col}' renamed to '{new_name}'.")
    return data
