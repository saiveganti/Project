import pandas as pd
import random

class PatientDatabase:
    def __init__(self, data_file, notes_file):
        self.data_file = data_file
        self.notes_file = notes_file
        self.df = pd.read_csv(self.data_file)
        self.notes_df = pd.read_csv(self.notes_file)

        self.df['Visit_time'] = pd.to_datetime(self.df['Visit_time'], format='mixed', errors='coerce').dt.strftime('%Y-%m-%d')


    def save_data(self):
        self.df.to_csv(self.data_file, index=False)

    def add_patient_visit(self, patient_id):
        visit_id = random.randint(100000, 999999)
        visit_time = input("Enter visit date (YYYY-MM-DD): ")
        department = input("Enter department: ")
        gender = input("Enter gender: ")
        race = input("Enter race: ")
        age = int(input("Enter age: "))
        ethnicity = input("Enter ethnicity: ")
        insurance = input("Enter insurance: ")
        zip_code = input("Enter zip code: ")
        complaint = input("Enter chief complaint: ")
        note_id = random.randint(100000, 999999)

        new_record = {
            "Patient_ID": patient_id,
            "Visit_ID": visit_id,
            "Visit_time": visit_time,
            "Visit_department": department,
            "Race": race,
            "Gender": gender,
            "Ethnicity": ethnicity,
            "Age": age,
            "Zip_code": zip_code,
            "Insurance": insurance,
            "Chief_complaint": complaint,
            "Note_ID": note_id,
            "Note_type": "N/A"  # Placeholder since Note_type isn't in the notes file
        }

        self.df = pd.concat([self.df, pd.DataFrame([new_record])], ignore_index=True)
        self.save_data()
        print("Visit added successfully.")

    def remove_patient(self, patient_id):
        if patient_id not in self.df['Patient_ID'].astype(str).values:
            print("Patient ID not found.")
            return
        self.df = self.df[self.df['Patient_ID'].astype(str) != str(patient_id)]
        self.save_data()
        print("Patient removed.")

    def retrieve_patient(self, patient_id, info_type="all"):
        patient_records = self.df[self.df['Patient_ID'].astype(str) == str(patient_id)]
        if patient_records.empty:
            print("Patient ID not found.")
            return

        if info_type == "basic":
            print(patient_records[['Patient_ID', 'Age', 'Gender', 'Race', 'Ethnicity']])
        elif info_type == "complaints":
            print(patient_records[['Visit_time', 'Chief_complaint']])
        else:
            print(patient_records)

    def count_visits(self, date):
        count = self.df[self.df['Visit_time'] == date].shape[0]
        print(f"Total visits on {date}: {count}")


    def view_note(self, date):
        try:
            date = pd.to_datetime(date).strftime('%Y-%m-%d')
        except Exception as e:
            print(f"Invalid date format: {e}")
            return

        self.df['Note_ID'] = self.df['Note_ID'].astype(str)
        self.notes_df['Note_ID'] = self.notes_df['Note_ID'].astype(str)

        note_ids = self.df[self.df['Visit_time'] == date]['Note_ID']
        if note_ids.empty:
            print("No visits found on this date.")
            return

        notes = self.notes_df[self.notes_df['Note_ID'].isin(note_ids)]

        if notes.empty:
            print("No notes found for visits on this date.")
        else:
            pd.set_option('display.max_colwidth', None)
            print("Clinical notes for the date:")
            print(notes[['Note_ID', 'Note_text']])
            pd.reset_option('display.max_colwidth') 




