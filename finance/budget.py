import pandas as pd
import numpy as np


def generate_budget_summary(df: pd.DataFrame) -> dict:
    """
    Generates a high-level summary of the financial data.

    Args:
        df (pd.DataFrame): DataFrame with financial transactions.

    Returns:
        dict: A dictionary containing key financial metrics.
    """
    if df is None or df.empty:
        return {
            "Total Spending": "$0.00",
            "Total Transactions": 0,
            "Average Transaction": "$0.00"
        }

    total_spending = df['Amount'].sum()
    total_transactions = len(df)
    average_transaction = df['Amount'].mean()

    # Identify top spending category
    if 'Category' in df.columns:
        top_category = df.groupby('Category')['Amount'].sum().idxmax()
    else:
        top_category = "N/A"

    return {
        "Total Spending": f"${total_spending:,.2f}",
        "Total Transactions": total_transactions,
        "Average Transaction": f"${average_transaction:,.2f}",
        "Top Spending Category": top_category
    }


def prepare_chart_data(df: pd.DataFrame, group_by_col: str) -> pd.DataFrame:
    """
    Prepares data for charting by grouping and summing amounts.

    Args:
        df (pd.DataFrame): DataFrame with financial transactions.
        group_by_col (str): The column to group by (e.g., 'Category', 'Date').

    Returns:
        pd.DataFrame: A DataFrame ready for plotting.
    """
    if df is None or df.empty or group_by_col not in df.columns:
        return pd.DataFrame({'Amount': []})

    if group_by_col == 'Date':
        # Ensure 'Date' is a datetime object for proper sorting and grouping
        df['Date'] = pd.to_datetime(df['Date'])
        # Resample by month to make the chart cleaner if there's a lot of data
        chart_data = df.set_index('Date').resample(
            'M')['Amount'].sum().reset_index()
        chart_data['Date'] = chart_data['Date'].dt.strftime(
            '%Y-%m')  # Format date for readability
        return chart_data

    # Group by the specified column and sum the amounts
    chart_data = df.groupby(group_by_col)['Amount'].sum().reset_index()
    return chart_data.sort_values(by='Amount', ascending=False)


def generate_spending_insights(df: pd.DataFrame, user_type: str) -> list:
    """
    Generates personalized spending insights based on user type.

    Args:
        df (pd.DataFrame): DataFrame with financial transactions.
        user_type (str): The user's demographic ('Student' or 'Professional').

    Returns:
        list: A list of string insights.
    """
    if df is None or df.empty:
        return ["No data available to generate insights."]

    insights = []

    # General insights
    top_category = df.groupby('Category')['Amount'].sum().idxmax()
    top_category_spend = df.groupby('Category')['Amount'].sum().max()
    total_spend = df['Amount'].sum()

    insights.append(
        f"Your top spending category is **{top_category}**, where you spent ${top_category_spend:,.2f}.")

    # User-type specific insights
    if user_type == "Student":
        if top_category in ["Food", "Dining", "Restaurants"]:
            insights.append(
                "Insight for Students: A significant portion of your budget goes to food. Consider exploring campus meal plans or cooking at home to save money.")
        if "Subscriptions" in df['Category'].unique():
            insights.append(
                "Insight for Students: Review your subscriptions. Services like Spotify and Netflix often offer student discounts.")

    elif user_type == "Professional":
        if top_category in ["Travel", "Flights", "Hotels"]:
            insights.append(
                "Insight for Professionals: Your travel expenses are high. Look into loyalty programs or travel credit cards to maximize rewards on your spending.")
        if "Transportation" in df['Category'].unique():
            transport_spend = df[df['Category'] ==
                                 'Transportation']['Amount'].sum()
            if (transport_spend / total_spend) > 0.15:  # If more than 15% of spend is on transport
                insights.append(
                    "Insight for Professionals: You spend a notable amount on transportation. If you're commuting, consider pre-tax commuter benefits if your employer offers them.")

    return insights
