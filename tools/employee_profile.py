from data.employees import employee_profile

def get_employee_profile(employee_id):
    emp_id = int(employee_id)
    profile = employee_profile.get(emp_id)
    return profile