import pandas as pd
import matplotlib.pyplot as plt
import ast
from collections import Counter

df = pd.read_csv("/content/extracted_predictions.csv")

# Columns to evaluate
eval_columns = [
    "Age", "Gender", "Symptoms / Chief Complaints",
    "Diagnosis", "Lab Tests / Investigations", "Medicines"
]

# Age Distribution
print("Age Distribution (non-null):")

age_df = df[df["Age"].notnull() & (df["Age"] != "null")]

age_df["Age"] = pd.to_numeric(age_df["Age"], errors="coerce")
age_df = age_df.dropna(subset=["Age"])
plt.figure(figsize=(12, 4))
plt.plot(sorted(age_df["Age"]), 'o')
plt.title("Patient Age Distribution")
plt.xlabel("Patient Index")
plt.ylabel("Age")
plt.grid(True)
plt.show()

# Gender Distribution
print("\nGender Distribution:")

gender_counts = df["Gender"].fillna("null").replace("", "null").value_counts()
print(gender_counts)

# Symptoms Frequency
print("\nUnique Symptoms / Chief Complaints:")

symptoms = df["Symptoms / Chief Complaints"]
symptoms_clean = symptoms[symptoms.notnull() & (symptoms != "null") & (symptoms != "")]
symptom_counts = symptoms_clean.value_counts()
print(symptom_counts)

# Diagnosis Frequency
print("\nUnique Diagnoses:")

diagnosis = df["Diagnosis"]
diagnosis_clean = diagnosis[diagnosis.notnull() & (diagnosis != "null") & (diagnosis != "")]
diagnosis_counts = diagnosis_clean.value_counts()
print(diagnosis_counts)

# Lab Tests Frequency
print("\nUnique Lab Tests / Investigations:")

tests = df["Lab Tests / Investigations"]
tests_clean = tests[tests.notnull() & (tests != "null") & (tests != "")]
tests_counts = tests_clean.value_counts()
print(tests_counts)

# Medicines Analysis
print("\nUnique Medicine Names and Route Frequencies:")

med_names = []
routes = []

for entry in df["Medicines"]:
    if pd.isnull(entry) or entry == "null":
        continue
    try:
        meds = ast.literal_eval(entry)
        for med in meds:
            if isinstance(med, dict):
                name = med.get("name", "").strip().lower()
                route = med.get("route", "").strip().lower()
                if name:
                    med_names.append(name)
                if route:
                    routes.append(route)
    except Exception as e:
        continue

# Count frequencies
name_counts = Counter(med_names)
route_counts = Counter(routes)

print("\nTop 10 Medicines:")
print(name_counts.most_common(10))

print("\nTop Routes:")
print(route_counts.most_common())

# Coverage Calculation
print("\nField Coverage:")

coverage = {}
for col in eval_columns:
    valid = df[col].notnull() & (df[col] != "null") & (df[col] != "")
    coverage[col] = round(valid.sum() / len(df) * 100, 2)

coverage_df = pd.DataFrame(list(coverage.items()), columns=["Field", "Coverage (%)"])
print(coverage_df)

# Count Rows Where All Fields Are Null
print("\nRows where ALL fields are null:")

null_rows = df[eval_columns].applymap(lambda x: x == "null" or pd.isnull(x) or x == "").all(axis=1)
print("Total rows where all evaluated fields are null:", null_rows.sum())
