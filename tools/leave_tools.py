from data.employees import employees_data

def get_leave_balance(employee_id):
    results = employees_data.get(employee_id)
    return results

