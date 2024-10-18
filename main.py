import streamlit as st
import pandas as pd
from auth import register_user, login_user
from data_handler import process_sales_data
from streamlit_option_menu import option_menu
from data_handler import fetch_user_sales_data, display_user_data



# Initialize session state variables
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

def show_login_page():
    st.title("Login or Sign Up")

    if 'auth_mode' not in st.session_state:
        st.session_state.auth_mode = "Login"  # Default to Login

    if st.session_state.auth_mode == "Login":
        show_login_form()
    elif st.session_state.auth_mode == "Sign Up":
        show_signup_form()

def show_login_form():
    st.subheader("Login to Your Account")
    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", type="password", key="login_password")

    # Move Login/Sign Up buttons below the inputs and use unique keys
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Login", key="login_button"):
            result = login_user(email, password)
            if result:
                st.session_state.authenticated = True
                st.session_state.user_id = result['response'].user.id  # Save the user ID in session state
                st.session_state.role = result.get('role', 'user')
                st.success(f"Logged in successfully as {st.session_state.role}!")
                st.rerun()  # Refresh the page after login
            else:
                st.error("Login failed. Please check your credentials.")

    with col2:
        if st.button("Sign Up", key="switch_to_signup"):
            st.session_state.auth_mode = "Sign Up"
            st.rerun()

def show_signup_form():
    st.subheader("Create New Account")
    email = st.text_input("Email", key="signup_email")
    password = st.text_input("Password", type="password", key="signup_password")

    # Move Sign Up/Login buttons below the inputs and use unique keys
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Sign Up", key="signup_button"):
            response = register_user(email, password)
            if response.get("success"):
                st.success(response.get("message"))
            else:
                st.error(response.get("message"))

    with col2:
        if st.button("Login", key="switch_to_login"):
            st.session_state.auth_mode = "Login"
            st.rerun()

def show_sidebar_menu():
    # Add a header with logo and title side by side
    col1, col2 = st.columns([1, 4])  # Adjust the ratio as needed

    with col1:
        st.image("fintastic_logo.png", width=195)  # Adjust width as per your preference

    with col2:
        st.markdown(
            "<h1 style='text-align: left; margin-top: 40px; color: #FFFFFF;'>Sales Forecasting App</h1>",
            unsafe_allow_html=True
        )

    # Sidebar menu with icons
    with st.sidebar:
        menu_icons = {
            "Upload Data": "cloud-upload",
            "Data Analysis": "bar-chart-line",
            "Forecasting": "graph-up",
            "Real-Time Insights": "eye",
            "Adjust Predictions": "wrench",
            "Reports": "file-earmark-text",
        }

        menu = option_menu(
            menu_title=None,
            options=list(menu_icons.keys()),
            icons=[menu_icons[page] for page in menu_icons.keys()],
            menu_icon="cast",
            default_index=0,
        )

        if st.button("Logout", key="logout_button"):
            st.session_state.authenticated = False
            st.session_state.user_id = ''
            st.session_state.role = ''
            st.rerun()

    # Implement the page navigation based on 'menu'
    if menu == "Upload Data":
        show_upload_page()
    elif menu == "Data Analysis":
        show_data_analysis_page()
    elif menu == "Forecasting":
        show_forecasting_page()
    elif menu == "Real-Time Insights":
        show_real_time_insights_page()
    elif menu == "Adjust Predictions":
        show_adjust_predictions_page()
    elif menu == "Reports":
        show_reports_page()

# Placeholder functions for each menu option
def show_upload_page():
    st.subheader("Upload Your Sales Data")
    file = st.file_uploader("Choose a CSV or Excel file", type=['csv', 'xlsx'])
    if file and st.button("Upload", key="upload_button"):
        user_id = st.session_state.user_id
        response = process_sales_data(file, user_id)
        if response.get("success"):
            st.success(response.get("message"))
        else:
            st.error(response.get("message"))


def show_data_analysis_page():
    st.subheader("Data Analysis")
    st.write("Tools for data cleaning, transformation, and visualization.")
    
    if 'user_id' in st.session_state:
        user_id = st.session_state.user_id
        display_user_data(
            user_id=user_id,
            section_title="Here is your uploaded sales data:",
            no_data_message="No sales data found. Please upload some data to get started."
        )
    else:
        st.warning("Please log in to view your data.")

def show_forecasting_page():
    st.subheader("Forecasting")
    st.write("Select and fine-tune forecasting models (ARIMA, Prophet, LSTM).")

    if 'user_id' in st.session_state:
        user_id = st.session_state.user_id
        display_user_data(
            user_id=user_id,
            section_title="Data for Forecasting:",
            no_data_message="No data available for forecasting. Please upload your sales data."
        )
    else:
        st.warning("Please log in to use forecasting.")

def show_real_time_insights_page():
    st.subheader("Real-Time Insights")
    st.write("Integrate real-time data to adjust predictions dynamically.")

    if 'user_id' in st.session_state:
        user_id = st.session_state.user_id
        display_user_data(
            user_id=user_id,
            section_title="Data for Real-Time Insights:",
            no_data_message="No data available for insights. Please upload your sales data."
        )
    else:
        st.warning("Please log in to view real-time insights.")

def show_adjust_predictions_page():
    st.subheader("Adjust Predictions")
    st.write("Adjust forecasts based on external factors and re-run predictions.")

    if 'user_id' in st.session_state:
        user_id = st.session_state.user_id
        display_user_data(
            user_id=user_id,
            section_title="Data for Adjusting Predictions:",
            no_data_message="No data available for adjustments. Please upload your sales data."
        )
    else:
        st.warning("Please log in to adjust predictions.")

def show_reports_page():
    st.subheader("Reports")
    st.write("Generate and download analysis reports.")

    if 'user_id' in st.session_state:
        user_id = st.session_state.user_id
        display_user_data(
            user_id=user_id,
            section_title="Data for Reports:",
            no_data_message="No data available for reports. Please upload your sales data."
        )
    else:
        st.warning("Please log in to view reports.")


def main():
    if not st.session_state.authenticated:
        show_login_page()
    else:
        show_sidebar_menu()

if __name__ == "__main__":
    main()
