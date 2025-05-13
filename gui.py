import tkinter as tk
from tkinter import messagebox
import pandas as pd
from datetime import datetime
from Users import authenticate_user
import random
from patients import PatientDatabase
from stats import generate_statistics

USAGE_LOG = "usage_log.csv"

def log_usage(username, role, status):
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = pd.DataFrame([{
        "Username": username,
        "Role": role if role else "Unknown",
        "Login_Time": time,
        "Status": status
    }])
    try:
        log_entry.to_csv(USAGE_LOG, mode='a', index=False, header=not pd.io.common.file_exists(USAGE_LOG))
    except Exception as e:
        print(f"Failed to log usage: {e}")

class LoginApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Hospital System Login")
        self.master.geometry("420x260")
        self.master.configure(bg="#f4edfa")
        self.master.resizable(False, False)

        frame = tk.Frame(master, bg="#f4edfa", padx=20, pady=20)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(frame, text="Welcome to Hospital Portal", font=("Helvetica", 16, "bold"),
                 bg="#f4edfa", fg="#5f4b8b").grid(row=0, columnspan=2, pady=(0, 15))

        tk.Label(frame, text="Username:", bg="#f4edfa", fg="#3f2b63", font=("Helvetica", 10)).grid(row=1, column=0, sticky="e", pady=5)
        self.username_entry = tk.Entry(frame, width=28)
        self.username_entry.grid(row=1, column=1, pady=5)

        tk.Label(frame, text="Password:", bg="#f4edfa", fg="#3f2b63", font=("Helvetica", 10)).grid(row=2, column=0, sticky="e", pady=5)
        self.password_entry = tk.Entry(frame, show="*", width=28)
        self.password_entry.grid(row=2, column=1, pady=5)

        login_btn = tk.Button(frame, text="Log In", command=self.authenticate, bg="#7e57c2", fg="white",
                              font=("Helvetica", 10, "bold"), width=20, relief="flat", activebackground="#9575cd")
        login_btn.grid(row=3, columnspan=2, pady=20)

    def authenticate(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        user = authenticate_user(username, password)
        if user:
            log_usage(username, user.role, "Success")
            messagebox.showinfo("Login Successful", f"Welcome {user.username} ({user.role})")
            self.master.withdraw()
            self.open_menu(user)
        else:
            log_usage(username, None, "Failed")
            messagebox.showerror("Login Failed", "Invalid credentials")

    def open_menu(self, user):
        menu = tk.Toplevel()
        menu.title(f"{user.role.capitalize()} Menu")
        menu.geometry("360x400")
        menu.configure(bg="#f8f5fc")

        tk.Label(menu, text=f"{user.role.capitalize()} Actions", font=("Helvetica", 14, "bold"),
                 bg="#f8f5fc", fg="#5f4b8b").pack(pady=15)

        role = user.role
        if role in ["nurse", "clinician"]:
            actions = ["Retrieve_patient", "Add_patient", "Remove_patient", "Count_visits", "View_note", "Exit"]
        elif role == "admin":
            actions = ["Count_visits", "Exit"]
        elif role == "management":
            actions = ["Generate_key_statistics", "Exit"]
        else:
            messagebox.showerror("Error", "Unknown user role")
            menu.destroy()
            return

        for action in actions:
            tk.Button(menu, text=action.replace("_", " "), width=25, bg="#7e57c2", fg="white",
                      font=("Helvetica", 10, "bold"), relief="flat", activebackground="#9575cd",
                      command=lambda act=action: self.handle_action(act, user, menu)).pack(pady=8)

    def handle_action(self, action, user, window):
        if action == "Exit":
            window.destroy()
            self.master.destroy()
        elif action == "Add_patient":
            db = PatientDatabase("./Patient_data.csv", "./Notes.csv")
            AddPatientForm(window, db)
        elif action == "Retrieve_patient":
            db = PatientDatabase("./Patient_data.csv", "./Notes.csv")
            RetrievePatientForm(window, db)
        elif action == "Remove_patient":
            db = PatientDatabase("./Patient_data.csv", "./Notes.csv")
            RemovePatientForm(window, db)
        elif action == "Count_visits":
            db = PatientDatabase("./Patient_data.csv", "./Notes.csv")
            CountVisitsForm(window, db)
        elif action == "View_note":
            db = PatientDatabase("./Patient_data.csv", "./Notes.csv")
            ViewNoteForm(window, db)
        elif action == "Generate_key_statistics":
            db = PatientDatabase("./Patient_data.csv", "./Notes.csv")
            GenerateStatisticsForm(window, db)
        else:
            messagebox.showinfo("Action Triggered", f"'{action}' will be implemented in the next steps.")

class AddPatientForm:
    def __init__(self, parent, patient_db):
        self.patient_db = patient_db
        self.window = tk.Toplevel(parent)
        self.window.title("Add Patient")
        self.window.configure(bg="#f8f5fc")
        self.window.geometry("470x700")

        self.entries = {}

        fields = [
            "Patient_ID",
            "Visit_time (YYYY-MM-DD)",
            "Visit_department",
            "Gender",
            "Race",
            "Ethnicity",
            "Age",
            "Zip_code",
            "Insurance",
            "Chief_complaint",
            "Note_type"
        ]

        tk.Label(self.window, text="Add Patient Visit", font=("Helvetica", 14, "bold"),
                 bg="#f8f5fc", fg="#5f4b8b").pack(pady=10)

        form_frame = tk.Frame(self.window, bg="#f8f5fc")
        form_frame.pack(padx=20, pady=10)

        for idx, label in enumerate(fields):
            tk.Label(form_frame, text=label + ":", anchor="w", bg="#f8f5fc", fg="#3f2b63",
                     font=("Helvetica", 10)).grid(row=idx, column=0, sticky="w", pady=4)
            entry = tk.Entry(form_frame, width=30)
            entry.grid(row=idx, column=1, pady=4)
            self.entries[label] = entry

        # Add multi-line text for Note_text
        tk.Label(form_frame, text="Note_text:", anchor="nw", bg="#f8f5fc", fg="#3f2b63",
                 font=("Helvetica", 10)).grid(row=len(fields), column=0, sticky="nw", pady=4)
        self.note_text = tk.Text(form_frame, height=6, width=30, wrap="word")
        self.note_text.grid(row=len(fields), column=1, pady=4)

        tk.Button(self.window, text="Submit", bg="#7e57c2", fg="white",
                  font=("Helvetica", 10, "bold"), width=20, relief="flat",
                  command=self.submit).pack(pady=15)

    def submit(self):
        data = {}
        for label, entry in self.entries.items():
            data[label] = entry.get().strip()

        note_text = self.note_text.get("1.0", tk.END).strip()

        if not data["Patient_ID"]:
            messagebox.showerror("Input Error", "Patient_ID is required.")
            return

        if not note_text:
            messagebox.showerror("Input Error", "Note_text is required.")
            return

        visit_id = random.randint(100000, 999999)
        note_id = random.randint(100000, 999999)

        df = self.patient_db.df
        patient_id = data["Patient_ID"]
        exists = str(patient_id) in df["Patient_ID"].astype(str).values

        if exists:
            if not data["Visit_time (YYYY-MM-DD)"]:
                messagebox.showerror("Input Error", "Visit time is required for existing patients.")
                return
            new_record = {
                "Patient_ID": patient_id,
                "Visit_ID": visit_id,
                "Visit_time": data["Visit_time (YYYY-MM-DD)"],
                "Visit_department": "N/A",
                "Race": "N/A",
                "Gender": "N/A",
                "Ethnicity": "N/A",
                "Age": "N/A",
                "Zip_code": "N/A",
                "Insurance": "N/A",
                "Chief_complaint": "N/A",
                "Note_ID": note_id,
                "Note_type": "N/A"
            }
        else:
            try:
                new_record = {
                    "Patient_ID": patient_id,
                    "Visit_ID": visit_id,
                    "Visit_time": data["Visit_time (YYYY-MM-DD)"],
                    "Visit_department": data["Visit_department"],
                    "Race": data["Race"],
                    "Gender": data["Gender"],
                    "Ethnicity": data["Ethnicity"],
                    "Age": int(data["Age"]),
                    "Zip_code": data["Zip_code"],
                    "Insurance": data["Insurance"],
                    "Chief_complaint": data["Chief_complaint"],
                    "Note_ID": note_id,
                    "Note_type": data["Note_type"]
                }
            except ValueError:
                messagebox.showerror("Input Error", "Invalid Age format.")
                return

        self.patient_db.df = pd.concat([self.patient_db.df, pd.DataFrame([new_record])], ignore_index=True)
        self.patient_db.save_data()

        note_entry = pd.DataFrame([{
            "Patient_ID": patient_id,
            "Visit_ID": visit_id,
            "Note_ID": note_id,
            "Note_text": note_text
        }])

        try:
            notes_df = pd.read_csv("Notes.csv")
            notes_df = pd.concat([notes_df, note_entry], ignore_index=True)
        except FileNotFoundError:
            notes_df = note_entry

        notes_df.to_csv("Notes.csv", index=True)


        messagebox.showinfo("Success", f"Visit and note saved for Patient_ID: {patient_id}")
        self.window.destroy()

class RetrievePatientForm:
    def __init__(self, parent, patient_db):
        self.patient_db = patient_db
        self.window = tk.Toplevel(parent)
        self.window.title("Retrieve Patient")
        self.window.configure(bg="#f8f5fc")
        self.window.geometry("520x420")

        tk.Label(self.window, text="Retrieve Patient Info", font=("Helvetica", 14, "bold"),
                 bg="#f8f5fc", fg="#5f4b8b").pack(pady=10)

        form_frame = tk.Frame(self.window, bg="#f8f5fc")
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="Patient_ID:", bg="#f8f5fc", fg="#3f2b63",
                 font=("Helvetica", 10)).grid(row=0, column=0, sticky="e", pady=5)

        self.patient_id_entry = tk.Entry(form_frame, width=30)
        self.patient_id_entry.grid(row=0, column=1, pady=5)

        tk.Button(self.window, text="Retrieve", bg="#7e57c2", fg="white", font=("Helvetica", 10, "bold"),
                  width=20, relief="flat", command=self.retrieve).pack(pady=10)

        self.output = tk.Text(self.window, width=65, height=15, wrap="word", font=("Courier", 10))
        self.output.pack(pady=5)

    def retrieve(self):
        patient_id = self.patient_id_entry.get().strip()
        if not patient_id:
            messagebox.showerror("Error", "Please enter a Patient_ID.")
            return

        df = self.patient_db.df
        records = df[df["Patient_ID"].astype(str) == str(patient_id)]

        if records.empty:
            self.output.delete("1.0", tk.END)
            self.output.insert(tk.END, "⚠️ Patient ID not found.")
            return

        records = records.sort_values("Visit_time", ascending=False)
        latest = records.iloc[0]

        output = (
            f"📄 Patient ID: {latest['Patient_ID']}\n"
            f"🕒 Visit Date: {latest['Visit_time']}\n"
            f"🏥 Department: {latest['Visit_department']}\n"
            f"🎂 Age: {latest['Age']}\n"
            f"👤 Gender: {latest['Gender']}\n"
            f"🌍 Race: {latest['Race']}\n"
            f"🌎 Ethnicity: {latest['Ethnicity']}\n"
            f"🏠 Zip Code: {latest['Zip_code']}\n"
            f"💳 Insurance: {latest['Insurance']}\n"
            f"❗ Complaint: {latest['Chief_complaint']}\n"
            f"🧾 Visit ID: {latest['Visit_ID']}\n"
            f"🗒️Note ID: {latest['Note_ID']}"
        )

        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, output)

class RemovePatientForm:
    def __init__(self, parent, patient_db):
        self.patient_db = patient_db
        self.window = tk.Toplevel(parent)
        self.window.title("Remove Patient")
        self.window.configure(bg="#f8f5fc")
        self.window.geometry("400x200")

        tk.Label(self.window, text="Remove Patient Record", font=("Helvetica", 14, "bold"),
                 bg="#f8f5fc", fg="#5f4b8b").pack(pady=15)

        form_frame = tk.Frame(self.window, bg="#f8f5fc")
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="Patient_ID:", bg="#f8f5fc", fg="#3f2b63",
                 font=("Helvetica", 10)).grid(row=0, column=0, sticky="e", pady=5)

        self.patient_id_entry = tk.Entry(form_frame, width=30)
        self.patient_id_entry.grid(row=0, column=1, pady=5)

        tk.Button(self.window, text="Remove", bg="#7e57c2", fg="white", font=("Helvetica", 10, "bold"),
                  width=20, relief="flat", command=self.remove).pack(pady=15)

    def remove(self):
        patient_id = self.patient_id_entry.get().strip()
        if not patient_id:
            messagebox.showerror("Input Error", "Please enter a Patient_ID.")
            return

        df = self.patient_db.df
        exists = patient_id in df["Patient_ID"].astype(str).values

        if not exists:
            messagebox.showerror("Not Found", "Patient ID not found.")
            return

        confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete Patient_ID {patient_id}?")
        if not confirm:
            return

        self.patient_db.df = df[df["Patient_ID"].astype(str) != patient_id]
        self.patient_db.save_data()

        messagebox.showinfo("Deleted", f"Patient {patient_id} removed successfully.")
        self.window.destroy()

class CountVisitsForm:
    def __init__(self, parent, patient_db):
        self.patient_db = patient_db
        self.window = tk.Toplevel(parent)
        self.window.title("Count Visits")
        self.window.configure(bg="#f8f5fc")
        self.window.geometry("400x220")

        tk.Label(self.window, text="Count Visits on a Date", font=("Helvetica", 14, "bold"),
                 bg="#f8f5fc", fg="#5f4b8b").pack(pady=15)

        form_frame = tk.Frame(self.window, bg="#f8f5fc")
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="Date (YYYY-MM-DD):", bg="#f8f5fc", fg="#3f2b63",
                 font=("Helvetica", 10)).grid(row=0, column=0, sticky="e", pady=5)

        self.date_entry = tk.Entry(form_frame, width=30)
        self.date_entry.grid(row=0, column=1, pady=5)

        tk.Button(self.window, text="Count", bg="#7e57c2", fg="white", font=("Helvetica", 10, "bold"),
                  width=20, relief="flat", command=self.count).pack(pady=15)

        self.output_label = tk.Label(self.window, text="", bg="#f8f5fc", font=("Helvetica", 11, "bold"))
        self.output_label.pack()

    def count(self):
        date = self.date_entry.get().strip()
        if not date:
            messagebox.showerror("Input Error", "Please enter a date.")
            return

        df = self.patient_db.df.copy()
        df["Visit_time"] = pd.to_datetime(df["Visit_time"], errors="coerce").dt.strftime("%Y-%m-%d")

        if date not in df["Visit_time"].values:
            self.output_label.config(text="No visits on this date.", fg="#c62828")
            return

        count = df[df["Visit_time"] == date].shape[0]
        self.output_label.config(text=f"Total visits on {date}: {count}", fg="#2e7d32")

class ViewNoteForm:
    def __init__(self, parent, patient_db):
        self.patient_db = patient_db
        self.window = tk.Toplevel(parent)
        self.window.title("View Clinical Notes")
        self.window.configure(bg="#f8f5fc")
        self.window.geometry("550x400")

        tk.Label(self.window, text="View Notes for Patient", font=("Helvetica", 14, "bold"),
                 bg="#f8f5fc", fg="#5f4b8b").pack(pady=10)

        form_frame = tk.Frame(self.window, bg="#f8f5fc")
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="Patient_ID:", bg="#f8f5fc", fg="#3f2b63", font=("Helvetica", 10)).grid(row=0, column=0, sticky="e", pady=5)
        self.patient_id_entry = tk.Entry(form_frame, width=30)
        self.patient_id_entry.grid(row=0, column=1, pady=5)

        tk.Button(self.window, text="View Notes", bg="#7e57c2", fg="white", font=("Helvetica", 10, "bold"),
                  width=20, relief="flat", command=self.view_notes).pack(pady=10)

        self.output = tk.Text(self.window, width=65, height=15, wrap="word", font=("Courier", 10))
        self.output.pack(pady=5)

    def view_notes(self):
        patient_id = self.patient_id_entry.get().strip()

        if not patient_id:
            messagebox.showerror("Input Error", "Patient_ID is required.")
            return

        df_visits = self.patient_db.df.copy()
        df_visits["Note_ID"] = df_visits["Note_ID"].astype(str)

        notes_df = self.patient_db.notes_df.copy()
        notes_df["Note_ID"] = notes_df["Note_ID"].astype(str)

        matching = df_visits[df_visits["Patient_ID"].astype(str) == patient_id]

        if matching.empty:
            self.output.delete("1.0", tk.END)
            self.output.insert(tk.END, "No visits found for this patient.")
            return

        note_ids = matching["Note_ID"].tolist()
        matching_notes = notes_df[notes_df["Note_ID"].isin(note_ids)]

        if matching_notes.empty:
            self.output.delete("1.0", tk.END)
            self.output.insert(tk.END, "No clinical notes found for this patient.")
            return

        self.output.delete("1.0", tk.END)
        for _, row in matching_notes.iterrows():
            self.output.insert(tk.END, f"🗒️ Note ID: {row['Note_ID']}\n")
            self.output.insert(tk.END, f"{row['Note_text']}\n\n")

class GenerateStatisticsForm:
    def __init__(self, parent, patient_db):
        self.window = tk.Toplevel(parent)
        self.window.title("Generate Statistics")
        self.window.configure(bg="#f8f5fc")
        self.window.geometry("400x180")

        tk.Label(self.window, text="Generate Key Statistics", font=("Helvetica", 14, "bold"),
                 bg="#f8f5fc", fg="#5f4b8b").pack(pady=15)

        tk.Label(self.window, text="This will generate plots\nand save them to the 'plots/' folder.",
                 bg="#f8f5fc", fg="#3f2b63", font=("Helvetica", 10)).pack(pady=5)

        tk.Button(self.window, text="Generate", bg="#7e57c2", fg="white", font=("Helvetica", 10, "bold"),
                  width=20, relief="flat", command=lambda: self.generate(patient_db)).pack(pady=15)

    def generate(self, patient_db):
        try:
            generate_statistics(patient_db.df)
            messagebox.showinfo("Success", "Statistics generated and saved to 'plots/' folder.")
            self.window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate statistics:\n{str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = LoginApp(root)
    root.mainloop()
