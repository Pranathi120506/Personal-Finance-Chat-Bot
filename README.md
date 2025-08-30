Personal Finance Chatbot
Project Description
The "Personal Finance Chatbot" is an intelligent conversational AI system built with Streamlit and Python. It leverages the concept of using advanced AI models (simulating IBM Granite) to provide personalized financial guidance on savings, taxes, and investments.

The application offers generated budget summaries from user-uploaded data, suggests actionable spending insights, and adapts its tone and complexity to suit different user demographics (Students vs. Professionals).

Features
Personalized Financial Guidance: Delivers customized advice based on user profiles.

AI-Generated Budget Summaries: Automatically generates budget summaries from uploaded CSV files.

Spending Insights: Provides actionable insights on spending habits.

Demographic-Aware Communication: Adjusts its tone and advice for Students vs. Professionals.

Multi-Page Interface: A seamless user experience with clear navigation between different financial tools.

Technologies & Tools
Frontend: Streamlit

Data Manipulation: Pandas

AI/NLP (Simulated): HuggingFace (IBM Granite)

Programming Language: Python

Getting Started
Prerequisites
Python 3.8+

pip for package management

Installation
Clone the repository:

git clone <repository_url>
cd personal-finance-chatbot

Create and activate a virtual environment (recommended):

python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

Install the required packages:

pip install -r requirements.txt

Set up environment variables:
Create a .env file in the root directory by copying the example:

cp .env.example .env

Add your HuggingFace API key to the .env file (Note: The current version simulates the API call, but this is good practice for future development).

HF_API_KEY="your_huggingface_api_key_here"

Running the Application
Execute the following command in your terminal from the root directory of the project:

streamlit run app.py

The application will open in your default web browser.

********Demo Credentials
You can use the following credentials to log in: *********

Student Login:

Username: student

Password: pass123

Professional Login:

Username: professional

Password: pass456
