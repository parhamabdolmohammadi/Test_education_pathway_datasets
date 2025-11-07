import pandas as pd

# === CONFIGURATION ===
with open("./cip-noc/cip_noc_file_paths.txt") as f:
    csv_files = [line.strip() for line in f if line.strip()]

noc_target = "21231"   # NOC code to search for

# === CONSTANTS ===
start_row = 17        # skip first 17 lines → start at row 18
n_rows = 818          # read rows 18–835 inclusive
noc_col_index = 0     # first column = NOC codes
gender_col_index = 4  # fifth column = Total-Gender values
cip_row = 11          # row 12 (0-based index)
cip_col = 4           # fifth column in that row (CIP designation)

# === STORAGE ===
matching_cips = set()

# === PROCESS EACH FILE ===
for file in csv_files:
    print(f"🔍 Checking {file} ...")

    try:
        # Step 1 — Read CIP code from row 12, column 5
        cip_value = pd.read_csv(file, skiprows=cip_row, nrows=1, header=None).iloc[0, cip_col]

        # Step 2 — Read rows 18 → 835 for NOC + Total-Gender
        df = pd.read_csv(file, skiprows=start_row, nrows=n_rows, header=None, dtype=str)

        # Step 3 — Convert column 5 (Total-Gender) to numeric
        df[gender_col_index] = pd.to_numeric(df.iloc[:, gender_col_index], errors='coerce').fillna(0)

        # Step 4 — Find rows where first column matches NOC and Total-Gender > 0
        match_rows = df[
            (df.iloc[:, noc_col_index].astype(str).str.contains(fr"\b{noc_target}\b", na=False)) &
            (df.iloc[:, gender_col_index] > 500) # This line can be changed to set the threshold of users
            #i.e. 500 means more than 500 people with NOC code studied that field
        ]

        # Step 5 — If any match found, record the CIP code
        if not match_rows.empty:
            matching_cips.add(str(cip_value))
            print(f"✅ Found match: {cip_value}")
        else:
            print("— No valid match found.")

    except Exception as e:
        print(f"⚠️ Error processing {file}: {e}")

# === FINAL OUTPUT ===
print("\n=== CIP CODES WITH MATCHING NOC ===")
for cip in sorted(matching_cips):
    print(cip)

print(f"\nTotal unique CIP matches: {len(matching_cips)}")

# # Optional: save results
# pd.Series(sorted(matching_cips), name="Matching CIP Codes").to_csv("matched_cips.csv", index=False)
# print("💾 Saved results to matched_cips.csv")
