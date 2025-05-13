import argparse
from Users import authenticate_user
from patients import PatientDatabase
from stats import generate_statistics


def main():
    parser = argparse.ArgumentParser(description="Hospital System Login")
    parser.add_argument("-username", required=True, help="Username")
    parser.add_argument("-password", required=True, help="Password")
    args = parser.parse_args()

    user = authenticate_user(args.username, args.password)

    if not user:
        print("Invalid credentials. Access denied.")
        return

    print(f"Welcome {user.username}! Your role is: {user.role}")

    if user.role in ["clinician", "nurse"]:
        patient_db = PatientDatabase("./Patient_data.csv", "./Notes.csv")
        while True:
            action = input("\nEnter action (add_patient, remove_patient, retrieve_patient, count_visits, view_note, Stop): ").strip()
            if action == "Stop":
                break
            user.perform_action(action, patient_db)

    elif user.role == "admin":
        date = input("Enter date to count visits (YYYY-MM-DD): ")
        patient_db = PatientDatabase("./Patient_data.csv", "./Notes.csv")
        user.perform_action("count_visits", patient_db, date)

    elif user.role == "management":
        patient_db = PatientDatabase("./Patient_data.csv", "./Notes.csv")
        generate_statistics(patient_db.df)


if __name__ == "__main__":
    main()
