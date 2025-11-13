import pandas as pd

def clean_num(x):
    if isinstance(x, str):
        return x.replace(",", "").replace("\u202f", "").strip()
    return x

def get_cip_codes(noc_code):

    # === CONFIGURATION ===
    with open("./cip-noc/cip_noc_file_paths.txt") as f:
        csv_files = [line.strip() for line in f if line.strip()]

    noc_target = noc_code   # NOC code to search for

    # === CONSTANTS ===
    start_row = 17        # skip first 17 lines → start at row 18
    n_rows = 818          # read rows 18–835 inclusive
    noc_col_index = 0     # first column = NOC codes
    gender_col_index = 4  # fifth column = Total-Gender values for that Field of Study
    cip_row = 11          # row 12 (0-based index)
    cip_col = 4           # fifth column in that row (CIP designation)
    total_col_index = 1   # first column = Total Gender for that NOC code

    # === STORAGE ===
    matching_cips = set()

    # === PROCESS EACH FILE ===
    for file in csv_files:
        print(f"🔍 Checking {file} ...")

        try:
            # Step 1 — Read CIP code from row 12, column 5
            cip_value = pd.read_csv(file, skiprows=cip_row, nrows=1, header=None).iloc[0, cip_col]

            # Step 2 — Read rows 18 → 835 for NOC + Total-Gender
            df = pd.read_csv(file, skiprows=start_row, nrows=n_rows, header=None, thousands=",",
                             converters={
                                 noc_col_index: str,
                                 gender_col_index: clean_num,
                                 total_col_index: clean_num
                             })

            # Step 3 — Convert column 5 (Total-Gender - Field) to numeric
            df[gender_col_index] = pd.to_numeric(df.iloc[:, gender_col_index], errors='coerce').fillna(0)

            # Step 4 - Convert column 1 (Total-Gender) to numeric
            df[total_col_index] = pd.to_numeric(df.iloc[:, total_col_index], errors='coerce').fillna(0)

            # Step 5 — Find rows where first column matches NOC and Total-Gender > 0

            match_rows = df[
                (df.iloc[:, noc_col_index].astype(str).str.startswith(str(noc_target))) &
                (df.iloc[:, gender_col_index] / df.iloc[:, total_col_index] >= 0.01) # This version compares
                # users to the population of that noc code.  0.03 seems small, but could represent 20,600 out of
                # 617,425 samples in that noc code. Where 500 would only be 0.0008 of the population
            ]

            # Step 6 — If any match found, record the CIP code
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

    return matching_cips

# # Optional: save results
# pd.Series(sorted(matching_cips), name="Matching CIP Codes").to_csv("matched_cips.csv", index=False)
# print("💾 Saved results to matched_cips.csv")

#print(get_cip_codes(21231))

if __name__ == "__main__":
    main()
