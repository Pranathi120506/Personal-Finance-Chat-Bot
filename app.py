from transformers import pipeline
from nlp.chatbot import get_financial_advice
from finance.analysis import (
    generate_budget_summary,
    generate_spending_insights,
    prepare_chart_data,
)
from utils.auth import login_user
import streamlit as st
import pandas as pd
from PIL import Image
import os
from dotenv import load_dotenv
from huggingface_hub import login
from transformers import pipeline


@st.cache_resource
def load_model():
    generator = pipeline(
        "text-generation",
        model="ibm-granite/granite-3b-instruct",
        token="HF_API_KEY"
    )
    return generator


# Import custom modules for different functionalities

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="FinBot: Your Personal Finance Advisor",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- SESSION STATE INITIALIZATION ---
# This is crucial for creating a multi-page experience in a single script.
if "page" not in st.session_state:
    st.session_state.page = "Select User Type"
if "user_type" not in st.session_state:
    st.session_state.user_type = None
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "df" not in st.session_state:
    st.session_state.df = None


# --- STYLING ---
# Custom CSS to inject for advanced styling, matching the color palette.
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


local_css(".streamlit/style.css")


# --- PAGE RENDERING FUNCTIONS ---
def render_user_type_selection():
    """Displays the initial page for the user to select their demographic."""
    st.title("Welcome to FinBot 🤖")
    st.header("Your Intelligent Guide for Savings, Taxes, and Investments")
    st.markdown(
        """
        To provide you with the most tailored financial advice, please select your profile.
        This helps us adjust the complexity and focus of our recommendations.
        """
    )

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🎓 I am a Student"):
            st.session_state.user_type = "Student"
            st.session_state.page = "Login"
            st.rerun()
    with col2:
        if st.button("💼 I am a Professional"):
            st.session_state.user_type = "Professional"
            st.session_state.page = "Login"
            st.rerun()


def render_login_page():
    """Displays the login form for the user."""
    st.title(f"Welcome, {st.session_state.user_type}!")

    with st.form("login_form"):
        username = st.text_input("Username or Email")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")

        if submitted:
            if login_user(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.page = "Dashboard"
                st.rerun()
            else:
                st.error("Invalid username or password")


def render_dashboard():
    """
    The main dashboard shown after a successful login.
    It includes a sidebar for navigation between different financial tools.
    """
    st.sidebar.success(
        f"Logged in as {st.session_state.username} ({st.session_state.user_type})")

    page_options = [
        "📊 Budget Tracking",
        "📈 Graphical Representation",
        "💡 Spending Insights",
        "🏦 Taxes and Investments",
    ]

    # Use a query param to decide which page to show
    page = st.sidebar.radio("Navigation", page_options)

    st.sidebar.markdown("---")
    if st.sidebar.button("Logout"):
        # Reset session state on logout
        for key in st.session_state.keys():
            del st.session_state[key]
        st.session_state.page = "Select User Type"
        st.rerun()

    st.title(page)

    if page == "📊 Budget Tracking":
        render_budget_tracking_page()
    elif page == "📈 Graphical Representation":
        render_graphical_representation_page()
    elif page == "💡 Spending Insights":
        render_spending_insights_page()
    elif page == "🏦 Taxes and Investments":
        render_taxes_and_investments_page()


def render_budget_tracking_page():
    """Handles file upload and displays the budget summary."""
    st.header("Upload Your Expense File")
    st.markdown(
        """
        Upload a CSV file with your recent transactions to get started.  
        The file should contain at least these columns: `Date`, `Category`, and `Amount`.  
        Or, you can use our **demo file** to explore the app.
        """
    )

    uploaded_file = st.file_uploader(
        "Choose a CSV file", type="csv", label_visibility="collapsed"
    )

    # --- Case 1: User uploads a file ---
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            required_cols = {"Date", "Category", "Amount"}
            if not required_cols.issubset(df.columns):
                st.error(
                    f"CSV must contain the following columns: {', '.join(required_cols)}"
                )
            else:
                st.session_state.df = df
                st.success("File uploaded successfully!")
        except Exception as e:
            st.error(f"An error occurred while processing the file: {e}")

    # --- Case 2: No file uploaded → Use demo file ---
    elif st.button("Use Demo File"):
        try:
            df = pd.read_csv("data/expense_data_1.csv")
            st.session_state.df = df
            st.success("Demo file loaded successfully!")
        except Exception as e:
            st.error(f"Could not load demo file: {e}")

    # --- Display results if dataframe is available ---
    if st.session_state.df is not None:
        st.markdown("---")
        st.subheader("Budget Summary")
        summary = generate_budget_summary(st.session_state.df)
        for key, value in summary.items():
            st.metric(label=key.replace("_", " ").title(), value=value)

        st.subheader("Recent Transactions")
        st.dataframe(st.session_state.df.tail())


def render_graphical_representation_page():
    """Displays charts and graphs based on the uploaded data."""
    if st.session_state.df is None:
        st.warning(
            "Please upload your expense file on the 'Budget Tracking' page first.")
        return

    st.subheader("Spending by Category")
    category_chart_data = prepare_chart_data(st.session_state.df, "Category")
    st.bar_chart(category_chart_data, x="Category", y="Amount")

    st.subheader("Spending Over Time")
    time_chart_data = prepare_chart_data(st.session_state.df, "Date")
    st.line_chart(time_chart_data, x="Date", y="Amount")


def render_spending_insights_page():
    """Provides actionable insights based on spending habits."""
    if st.session_state.df is None:
        st.warning(
            "Please upload your expense file on the 'Budget Tracking' page first.")
        return

    st.subheader("Actionable Spending Insights")
    insights = generate_spending_insights(
        st.session_state.df, st.session_state.user_type)
    for insight in insights:
        st.info(insight)


def render_taxes_and_investments_page():
    """A chatbot interface for getting financial advice."""
    st.subheader("Ask FinBot for Financial Advice")
    st.markdown(
        "Ask questions about savings, tax strategies, or investment options. Our AI, powered by IBM Granite, will provide guidance tailored to you."
    )

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # React to user input
    if prompt := st.chat_input("What would you like to ask?"):
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Get AI response
        with st.spinner("FinBot is thinking..."):
            response = get_financial_advice(prompt, st.session_state.user_type)

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(response)

        # Add assistant response to chat history
        st.session_state.messages.append(
            {"role": "assistant", "content": response})


# --- MAIN ROUTER ---
# This logic determines which page to show based on the session state.
if st.session_state.page == "Select User Type":
    render_user_type_selection()
elif st.session_state.page == "Login":
    render_login_page()
elif st.session_state.page == "Dashboard":
    render_dashboard()
