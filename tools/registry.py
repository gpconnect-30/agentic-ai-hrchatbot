from tools.leave_tools import get_leave_balance

tools_registry = {
    "leave_balance": {
        "description": "Returns the remaining leave balance for a given employee.",
        "function": get_leave_balance
    }
}