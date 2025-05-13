import pandas as pd

class User:
    def __init__(self, username, role):
        self.username = username
        self.role = role

    def perform_action(self, action, patient_db, extra=None):
        if action == "add_patient":
            patient_id = input("Enter Patient ID: ")
            patient_db.add_patient_visit(patient_id)
        elif action == "remove_patient":
            patient_id = input("Enter Patient ID to remove: ")
            patient_db.remove_patient(patient_id)
        elif action == "retrieve_patient":
            patient_id = input("Enter Patient ID: ")
            info = input("What information do you need? (all, basic, complaints): ")
            patient_db.retrieve_patient(patient_id, info)
        elif action == "count_visits":
            date = extra if extra else input("Enter date (YYYY-MM-DD): ")
            patient_db.count_visits(date)
        elif action == "view_note":
            date = input("Enter date (YYYY-MM-DD): ")
            patient_db.view_note(date)
        else:
            print("Invalid action.")


class AdminUser(User):
    def perform_action(self, action, patient_db, extra=None):
        if action == "count_visits":
            date = extra if extra else input("Enter date (YYYY-MM-DD): ")
            patient_db.count_visits(date)
        else:
            print("Admin role can only perform count_visits.")


class ManagementUser(User):
    pass  # All logic is handled in main for management users


def authenticate_user(username, password):
    try:
        df = pd.read_csv("./Credentials.csv")
    except FileNotFoundError:
        print("Credentials file not found.")
        return None

    user_row = df[(df['username'] == username) & (df['password'] == password)]
    if user_row.empty:
        return None

    role = user_row.iloc[0]['role']
    if role == "admin":
        return AdminUser(username, role)
    elif role == "management":
        return ManagementUser(username, role)
    else:
        return User(username, role)
