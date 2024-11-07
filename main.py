# main.py

import streamlit as st
from data_handler import (
    process_uploaded_data,
    download_template
)
from forecasting import apply_forecasting  # Import apply_forecasting for forecasting options
from streamlit_option_menu import option_menu
from auth import register_user, login_user  # Assuming you have an auth.py for authentication

# Initialize session state variables
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'selected_data_type' not in st.session_state:
    st.session_state.selected_data_type = None
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Home"  # Default to the Home page
if 'data' not in st.session_state:
    st.session_state.data = None
if 'auth_mode' not in st.session_state:
    st.session_state.auth_mode = "Login"  # Default to Login

def show_login_page():
    st.title("Login or Sign Up")
    if st.session_state.auth_mode == "Login":
        show_login_form()
    elif st.session_state.auth_mode == "Sign Up":
        show_signup_form()

def show_login_form():
    st.subheader("Login to Your Account")
    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", type="password", key="login_password")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Login", key="login_button"):
            result = login_user(email, password)
            if result:
                st.session_state.authenticated = True
                st.session_state.user_id = result['response'].user.id
                st.session_state.role = result.get('role', 'user')
                st.success(f"Logged in successfully as {st.session_state.role}!")
                st.session_state.current_page = "Home"
                st.rerun()
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
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Sign Up", key="signup_button"):
            response = register_user(email, password)
            if response.get("success"):
                st.success(response.get("message"))
                st.session_state.authenticated = True
                st.session_state.user_id = response['user'].id
                st.session_state.role = response.get('role', 'user')
                st.session_state.current_page = "Home"
                st.rerun()
            else:
                st.error(response.get("message"))
    with col2:
        if st.button("Login", key="switch_to_login"):
            st.session_state.auth_mode = "Login"
            st.rerun()

def show_sidebar_menu():
    col1, col2 = st.columns([1, 4])
    with col1:
        st.image("fintastic_logo.png", width=195)
    with col2:
        st.markdown("<h1 style='text-align: left; margin-top: 40px;'>Sales Forecasting App</h1>", unsafe_allow_html=True)
    with st.sidebar:
        menu_icons = {
            "Home": "house",
            "Upload Data": "cloud-upload",
            "Data Analysis": "bar-chart-line",
            "Forecasting": "graph-up",
            "Real-Time Insights": "eye",
            "Adjust Predictions": "wrench",
            "Reports": "file-earmark-text",
        }
        # Update current page based on the menu selection
        selected_menu = option_menu(
            menu_title=None,
            options=list(menu_icons.keys()),
            icons=[menu_icons[page] for page in menu_icons.keys()],
            menu_icon="cast",
            default_index=0
        )
        st.session_state.current_page = selected_menu

        if st.button("Logout", key="logout_button"):
            st.session_state.authenticated = False
            st.session_state.user_id = ''
            st.session_state.role = ''
            st.session_state.selected_data_type = None
            st.session_state.current_page = "Home"
            st.session_state.data = None
            st.session_state.auth_mode = "Login"
            st.rerun()

def show_home_page():
    st.title("Welcome to the Sales Forecasting App!")
    st.write("This is the home page where you can find an overview of the app features and navigate to different sections using the sidebar.")

def show_upload_page():
    st.header("Upload Data")
    st.subheader("Select the Type of Data You Want to Forecast")
    
    # Data type selection buttons
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("Sales"):
            st.session_state.selected_data_type = "Sales"
            st.session_state.pop('data', None)  # Reset data when data type changes
    with col2:
        if st.button("Stocks"):
            st.session_state.selected_data_type = "Stocks"
            st.session_state.pop('data', None)
    with col3:
        if st.button("Commodities"):
            st.session_state.selected_data_type = "Commodities"
            st.session_state.pop('data', None)
    with col4:
        if st.button("Custom"):
            st.session_state.selected_data_type = "Custom"
            st.session_state.pop('data', None)
    
    if st.session_state.selected_data_type:
        st.subheader(f"{st.session_state.selected_data_type} Data - Template Download & Upload")
        
        # Template download button
        if st.button("Download Template"):
            template_buffer = download_template(st.session_state.selected_data_type)
            st.download_button(
                label="Download CSV Template",
                data=template_buffer,
                file_name=f"{st.session_state.selected_data_type}_template.csv",
                mime="text/csv"
            )
    
        # File uploader for user data
        file = st.file_uploader("Choose a CSV or Excel file", type=['csv', 'xlsx'], key="file_uploader")
        if file:
            st.write("Processing the uploaded data...")
            cleaned_data = process_uploaded_data(file)
            if cleaned_data is not None:
                st.session_state.data = cleaned_data
                st.success("Data processed successfully.")
                st.dataframe(cleaned_data.head())

def show_forecasting_page():
    st.header("Forecasting")
    if st.session_state.data is not None:
        apply_forecasting(st.session_state.data)
    else:
        st.warning("Please upload data in the 'Upload Data' section before accessing forecasting.")

def main():
    if not st.session_state.authenticated:
        show_login_page()
    else:
        show_sidebar_menu()

        # Display the selected page content based on sidebar menu
        if st.session_state.current_page == "Home":
            show_home_page()
        elif st.session_state.current_page == "Upload Data":
            show_upload_page()
        elif st.session_state.current_page == "Data Analysis":
            st.write("Data Analysis page under construction.")
        elif st.session_state.current_page == "Forecasting":
            show_forecasting_page()
        elif st.session_state.current_page == "Real-Time Insights":
            st.write("Real-Time Insights page under construction.")
        elif st.session_state.current_page == "Adjust Predictions":
            st.write("Adjust Predictions page under construction.")
        elif st.session_state.current_page == "Reports":
            st.write("Reports page under construction.")
        else:
            st.error("Page not found.")

if __name__ == "__main__":
    main()
