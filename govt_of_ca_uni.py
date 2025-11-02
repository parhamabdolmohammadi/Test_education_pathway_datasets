import pandas as pd

# === Load CSV ===
DATA_PATH = "program.csv"  # change if needed
df = pd.read_csv(DATA_PATH)

OUTPUT_FILE = "result.csv"

# === Helper: save results and print ===
def save_and_show(results, title="Results"):
    """Save DataFrame to CSV and print to console."""
    results.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")
    print(f"\n=== {title} ===")
    print(results if not results.empty else "(No results found)")
    print(f"\n {len(results)} record(s) saved to '{OUTPUT_FILE}'.\n")
    return results

# === Display all column names ===
def print_columns():
    print("=== ALL FEATURE (COLUMN) NAMES IN THE DATASET ===\n")
    for i, col in enumerate(df.columns, start=1):
        print(f"{i}. {col}")

# === Search functions (each prints + saves results) ===
def search_by_academic_level_area_of_study_e(keyword):
    results = df[df["academic_level_area_of_study_e"].str.contains(keyword, case=False, na=False)]
    return save_and_show(results, f"academic_level_area_of_study_e contains '{keyword}'")

def search_by_academic_level_area_of_study_f(keyword):
    results = df[df["academic_level_area_of_study_f"].str.contains(keyword, case=False, na=False)]
    return save_and_show(results, f"academic_level_area_of_study_f contains '{keyword}'")

def search_by_program_of_study_e(keyword):
    results = df[df["program_of_study_e"].str.contains(keyword, case=False, na=False)]
    return save_and_show(results, f"program_of_study_e contains '{keyword}'")

def search_by_program_of_study_f(keyword):
    results = df[df["program_of_study_f"].str.contains(keyword, case=False, na=False)]
    return save_and_show(results, f"program_of_study_f contains '{keyword}'")

def search_by_program_length_e(keyword):
    results = df[df["program_length_e"].str.contains(keyword, case=False, na=False)]
    return save_and_show(results, f"program_length_e contains '{keyword}'")

def search_by_program_length_f(keyword):
    results = df[df["program_length_f"].str.contains(keyword, case=False, na=False)]
    return save_and_show(results, f"program_length_f contains '{keyword}'")

def search_by_duration_of_term_e(keyword):
    results = df[df["duration_of_term_e"].str.contains(keyword, case=False, na=False)]
    return save_and_show(results, f"duration_of_term_e contains '{keyword}'")

def search_by_duration_of_term_f(keyword):
    results = df[df["duration_of_term_f"].str.contains(keyword, case=False, na=False)]
    return save_and_show(results, f"duration_of_term_f contains '{keyword}'")

def search_by_institution_name_e(keyword):
    results = df[df["institution_name_e"].str.contains(keyword, case=False, na=False)]
    return save_and_show(results, f"institution_name_e contains '{keyword}'")

def search_by_institution_name_f(keyword):
    results = df[df["institution_name_f"].str.contains(keyword, case=False, na=False)]
    return save_and_show(results, f"institution_name_f contains '{keyword}'")

def search_by_contact(keyword):
    results = df[df["contact"].str.contains(keyword, case=False, na=False)]
    return save_and_show(results, f"contact contains '{keyword}'")

def search_by_contact_email(keyword):
    results = df[df["contact_email"].str.contains(keyword, case=False, na=False)]
    return save_and_show(results, f"contact_email contains '{keyword}'")

def search_by_program_type_e(keyword):
    results = df[df["program_type_e"].str.contains(keyword, case=False, na=False)]
    return save_and_show(results, f"program_type_e contains '{keyword}'")

def search_by_program_type_f(keyword):
    results = df[df["program_type_f"].str.contains(keyword, case=False, na=False)]
    return save_and_show(results, f"program_type_f contains '{keyword}'")

def search_by_specialization_e(keyword):
    results = df[df["specialization_e"].str.contains(keyword, case=False, na=False)]
    return save_and_show(results, f"specialization_e contains '{keyword}'")

def search_by_specialization_f(keyword):
    results = df[df["specialization_f"].str.contains(keyword, case=False, na=False)]
    return save_and_show(results, f"specialization_f contains '{keyword}'")

# === Combined search ===
def search_combined(program_keyword=None, academic_keyword=None, institution_keyword=None):
    filtered = df.copy()

    if program_keyword:
        filtered = filtered[
            filtered["program_of_study_e"].str.contains(program_keyword, case=False, na=False)
        ]
    if academic_keyword:
        filtered = filtered[
            filtered["academic_level_area_of_study_e"].str.contains(academic_keyword, case=False, na=False)
        ]
    if institution_keyword:
        filtered = filtered[
            filtered["institution_name_e"].str.contains(institution_keyword, case=False, na=False)
        ]

    return save_and_show(filtered, f"Combined search: {program_keyword}, {academic_keyword}, {institution_keyword}")

# === Example usage ===
if __name__ == "__main__":
    print_columns()
    # Example: run one of the searches below
    # search_by_program_of_study_e("Computer Systems")
    # search_by_institution_name_e("McGill")
    search_combined("Computer Science", academic_keyword="diploma")


