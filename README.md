
# HI 741 Final Project – Clinical Data Management System (GUI)

This project is a Tkinter-based GUI application for managing patient data in a clinical data warehouse. It supports role-based login, patient management, clinical note integration, and automated statistics generation.

## 🧠 Features

- 🔐 **User Login with Role Validation**
- 👩‍⚕️ **Clinician/Nurse Functions**:
  - Add Patient (with clinical notes)
  - Remove Patient
  - Retrieve Latest Visit Info
  - View All Notes by Patient
  - Count Visits by Date
- 🧑‍💼 **Admin Function**:
  - Count visits by date only
- 📊 **Management Function**:
  - Generate statistics from patient data (charts saved to `plots/`)
- 📁 All changes are saved to `Patient_data.csv` and `Notes.csv`
- 🗒️ Usage logs recorded in `usage_log.csv`

## 🚀 How to Run

1. Clone or download the repo
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the app:
   ```bash
   python gui.py
   ```

## 🔐 User Roles

| Role        | Actions Allowed                                |
|-------------|-------------------------------------------------|
| `clinician` | All functions                                   |
| `nurse`     | All functions                                   |
| `admin`     | Count visits only                               |
| `management`| Generate key statistics only                    |

## 📂 Project Structure

```
.
├── gui.py                  # Main GUI application
├── patients.py             # PatientDatabase class
├── stats.py                # Statistics plotting
├── user.py                 # User authentication & roles
├── Patient_data.csv        # Patient visit records
├── Notes.csv               # Clinical notes
├── Credentials.csv         # Login credentials (username, password, role)
├── usage_log.csv           # Logs of logins and role access
├── plots/                  # Output charts from statistics
├── requirements.txt        # Python dependencies
├── UML_Diagram.pdf         # Class structure diagram
└── README.md               # You're here
```

## 📈 Statistics Output

Charts generated for:
- Monthly visit trends
- Visits by gender, race, insurance, department

Saved in `plots/` folder as `.png` files.

## ✅ Dependencies

- `tkinter`
- `pandas`
- `matplotlib`

Use:
```bash
pip install -r requirements.txt
```

## 📌 Notes

- All files must be in the same directory as `gui.py`
- `Notes.csv` is updated only when a new patient with a note is added
- `usage_log.csv` logs every login attempt (success or failed)

## 👨‍💻 Author

Sai Veganti — HI 741 Spring 2025

## 📅 Due Date

🗓️  May 12, 2025 — 11:59 PM CT
