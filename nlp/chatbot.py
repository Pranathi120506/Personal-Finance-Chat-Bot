def get_financial_advice(query: str, user_type: str) -> str:
    """
    Simulates a call to an IBM Granite model on HuggingFace.

    This function provides canned responses tailored to the user's demographic
    to demonstrate the personalized advice capability of the application.
    In a real-world scenario, this would make an API call.

    Args:
        query (str): The user's financial question.
        user_type (str): The user's demographic ('Student' or 'Professional').

    Returns:
        str: A tailored financial advice response.
    """
    query = query.lower()

    # Generic Welcome
    if "hello" in query or "hi" in query:
        return "Hello! I'm FinBot. How can I help you with your financial questions today?"

    # --- Student-Specific Logic ---
    if user_type == "Student":
        if "save money" in query:
            return (
                "As a student, saving can be powerful, even in small amounts. Here are a few tips:\n"
                "- **Automate Savings:** Set up an automatic transfer of a small amount (even $10) to a savings account each week.\n"
                "- **Use Student Discounts:** Always ask for student discounts on food, tech, and entertainment.\n"
                "- **Budget for Fun:** Allocate a specific amount for social activities so you don't overspend."
            )
        elif "investment" in query or "investing" in query:
            return (
                "That's a great question for a student! Starting early is key.\n"
                "- **Consider a Roth IRA:** If you have any part-time income, a Roth IRA is a fantastic way to start investing for retirement with tax-free growth.\n"
                "- **Low-Cost Index Funds:** You can start with a small amount in a broad-market index fund (like one tracking the S&P 500). It's a simple way to get diversified exposure to the stock market.\n"
                "- **Learn First:** Use this time to learn about different investment types. Don't invest in anything you don't understand."
            )
        elif "taxes" in query:
            return (
                "For students, taxes can be straightforward. If you have a part-time job, your employer will likely withhold taxes. You may be able to claim education credits like the American Opportunity Tax Credit if you or your parents are paying for tuition. It's often beneficial for your parents to claim you as a dependent."
            )

    # --- Professional-Specific Logic ---
    elif user_type == "Professional":
        if "save money" in query:
            return (
                "For professionals, optimizing savings is key to achieving long-term goals. Let's look at some strategies:\n"
                "- **Maximize 401(k) Match:** Ensure you are contributing enough to your employer's 401(k) to get the full company match. It's free money!\n"
                "- **High-Yield Savings Account (HYSA):** Don't let your emergency fund sit in a low-interest account. An HYSA will give you a much better return.\n"
                "- **Review Major Expenses:** Periodically review your biggest expenses (housing, transportation) to see if there are opportunities to reduce costs."
            )
        elif "investment" in query or "investing" in query:
            return (
                "As a professional, your investment strategy should align with your career stage and risk tolerance.\n"
                "- **Diversification is Crucial:** Beyond your 401(k), consider a diversified portfolio of stocks and bonds through ETFs or mutual funds. \n"
                "- **Tax-Advantaged Accounts:** After your 401(k), look into a Roth or Traditional IRA, and potentially a Health Savings Account (HSA) if you have a high-deductible health plan.\n"
                "- **Consider Your Goals:** Are you investing for retirement, a down payment, or another major purchase? The timeline for your goal should dictate your investment choices."
            )
        elif "taxes" in query:
            return (
                "For professionals, tax planning is crucial. Beyond standard deductions, consider:\n"
                "- **Tax-Loss Harvesting:** If you have a brokerage account, you can sell investments at a loss to offset gains.\n"
                "- **Itemizing Deductions:** If you have significant expenses like mortgage interest or state and local taxes, itemizing might be better than taking the standard deduction.\n"
                "- **Consult a Professional:** As your income grows, it's often wise to consult with a Certified Public Accountant (CPA) to create a personalized tax strategy."
            )

    # Default fallback response
    return "I can provide guidance on topics like saving money, investing, and taxes. Please ask me about one of those areas, and I'll do my best to provide a tailored response."
