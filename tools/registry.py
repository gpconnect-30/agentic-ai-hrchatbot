from tools.leave_tools import get_leave_balance
from tools.employee_profile import get_employee_profile
from tools.holiday_calendar import get_holidays

tools_registry = {
    "leave_balance": {
        "description": """Get remaining vacation/sick leave days for an employee. Use when employee asks about available days, balance, or how many leaves left.
        Use when query contains: 'balance', 'available days', 'how many leaves', 'remaining leave'.
        DO NOT use for policy questions about rules, eligibility, or procedures.
        """,
        "parameters": {
                    "employee_id": "Require the employee_id in interger"
        },
        "function": get_leave_balance
    },
    "get_holidays": {
        "description": "Returns company holiday calendar information.",
        "parameters": {
            "month": "Optional 2-digit month string (e.g. '01' for Jan, '08' for Aug). Set if user asks for a specific month.",
            "upcoming_only": "Optional boolean (true/false). Set true if user asks for upcoming, remaining, or next holidays."
        },
        "function": get_holidays
    },
    "employee_profile": {
        "description": """Returns employee profile information including manager name, email, department, title, joining date and employment status.
Use when the user asks about their manager, reporting manager, email, title, department or profile.""",
        "parameters": {
            "employee_id": "Require the employee_id in interger"
        },
        "function": get_employee_profile
    }
}