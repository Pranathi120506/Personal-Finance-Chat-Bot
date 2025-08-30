import pandas as pd


def generate_budget_summary(df: pd.DataFrame) -> dict:
    """Summarize budget with total, average, and count of transactions."""
    return {
        "total_expenses": df["Amount"].sum(),
        "average_expense": df["Amount"].mean(),
        "transaction_count": len(df),
    }


def generate_spending_insights(df: pd.DataFrame, user_type: str) -> list[str]:
    """Provide insights based on spending patterns and user type."""
    insights = []
    if df.empty:
        return ["No spending data available yet."]

    top_category = df.groupby("Category")["Amount"].sum().idxmax()
    top_value = df.groupby("Category")["Amount"].sum().max()

    insights.append(
        f"Your highest spending is in **{top_category}**: {top_value:.2f}."
    )

    if user_type == "Student":
        insights.append(
            "Consider setting aside more for savings and tuition-related costs.")
    elif user_type == "Professional":
        insights.append(
            "Look into tax-saving investment options to reduce liabilities.")

    return insights


def prepare_chart_data(df: pd.DataFrame, group_by: str) -> pd.DataFrame:
    """Aggregate data for charts by category or date."""
    if group_by == "Category":
        return df.groupby("Category")["Amount"].sum().reset_index()
    elif group_by == "Date":
        df["Date"] = pd.to_datetime(df["Date"])
        return df.groupby("Date")["Amount"].sum().reset_index()
    return df
