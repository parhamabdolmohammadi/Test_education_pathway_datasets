import pandas as pd

# === Load your Excel file ===
input_path = "2019_Occupations.xlsx"      # path to your file
output_path = "Occupations.csv"           # desired CSV file name

# Read the first sheet of the Excel file
df = pd.read_excel(input_path)

# Optional: preview column names and rows
print("✅ Columns detected:", df.columns.tolist())
print(df.head())

# Save to CSV (UTF-8, no index column)
df.to_csv(output_path, index=False, encoding="utf-8-sig")

print(f"🎉 Successfully converted '{input_path}' → '{output_path}'")
