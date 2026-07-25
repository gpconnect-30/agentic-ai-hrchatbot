from tools.leave_tools import get_leave_balance

tools_registry = {
    "leave_balance": {
        "description": """Get remaining vacation/sick leave days for an employee. Use when employee asks about available days, balance, or how many leaves left.
        Use when query contains: 'balance', 'available days', 'how many leaves', 'remaining leave'.
        DO NOT use for policy questions about rules, eligibility, or procedures.
        """,
        "function": get_leave_balance
    }
}