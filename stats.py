import pandas as pd
import matplotlib.pyplot as plt
import os

def generate_statistics(df):
    os.makedirs("plots", exist_ok=True)

    df['Visit_time'] = pd.to_datetime(df['Visit_time'], errors='coerce')
    df = df.dropna(subset=['Visit_time'])

    if df.empty:
        print("No valid visit data found.")
        return

    # 1. Monthly Visit Trend
    df['Visit_month'] = df['Visit_time'].dt.to_period('Y')
    visit_trend = df.groupby('Visit_month').size()
    ax = visit_trend.plot(kind='line', title='Yearly Visit Trend')
    ax.set_xlabel("Year")
    ax.set_ylabel("Number of Visits")
    plt.tight_layout()
    plt.savefig("plots/visit_trend.png")
    plt.show()

    # 2. Insurance Type vs Number of Visits
    insurance_counts = df['Insurance'].value_counts()
    ax = insurance_counts.plot(kind='bar', title='Visits by Insurance Type')
    ax.set_xlabel("Insurance Type")
    ax.set_ylabel("Number of Visits")
    plt.tight_layout()
    plt.savefig("plots/insurance_type.png")
    plt.show()

    # 3. Gender vs Number of Visits
    gender_counts = df['Gender'].value_counts()
    ax = gender_counts.plot(kind='bar', title='Visits by Gender')
    ax.set_xlabel("Gender")
    ax.set_ylabel("Number of Visits")
    plt.tight_layout()
    plt.savefig("plots/gender.png")
    plt.show()

    # 4. Race vs Number of Visits
    race_counts = df['Race'].value_counts()
    ax = race_counts.plot(kind='bar', title='Visits by Race')
    ax.set_xlabel("Race")
    ax.set_ylabel("Number of Visits")
    plt.tight_layout()
    plt.savefig("plots/race.png")
    plt.show()

    # 5. Department vs Number of Visits
    dept_counts = df['Visit_department'].value_counts()
    ax = dept_counts.plot(kind='bar', title='Visits by Department')
    ax.set_xlabel("Department")
    ax.set_ylabel("Number of Visits")
    plt.tight_layout()
    plt.savefig("plots/departments.png")
    plt.show()

    print("All categorical plots shown and saved!")
