from data.employees import employees_data

def get_leave_balance(employee_id):
    emp_id = int(employee_id)
    results = employees_data.get(emp_id)
    return results

