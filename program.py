import pandas as pd

# === Load your CSV file ===
DATA_PATH = "program.csv"  # change to your actual file name
df = pd.read_csv(DATA_PATH)


def print_culomns():
    print("=== ALL FEATURE (COLUMN) NAMES IN THE DATASET ===\n")
    for i, col in enumerate(df.columns, start=1):
        print(f"{i}. {col}")


# === Helper ===
def search_by_column(column_name, keyword):
    """Generic search across one column (case-insensitive)."""
    if column_name not in df.columns:
        raise ValueError(f"Column '{column_name}' not found in dataset.")
    return df[df[column_name].astype(str).str.contains(keyword, case=False, na=False)]

# === Query Functions for each major field ===

# --- Academic level / area of study ---
def search_by_academic_level(keyword):
    """Search by academic level or area of study."""
    return pd.concat([
        search_by_column('academic_level_area_of_study_e', keyword),
        search_by_column('academic_level_area_of_study_f', keyword)
    ]).drop_duplicates()

# --- Program name ---
def search_by_program(keyword):
    """Search by program name."""
    return pd.concat([
        search_by_column('program_of_study_e', keyword),
        search_by_column('program_of_study_f', keyword)
    ]).drop_duplicates()

# --- Program length ---
def search_by_program_length(keyword):
    """Search by overall program length."""
    return pd.concat([
        search_by_column('program_length_e', keyword),
        search_by_column('program_length_f', keyword)
    ]).drop_duplicates()

# --- Duration of term ---
def search_by_term_duration(keyword):
    """Search by duration of each term (semester)."""
    return pd.concat([
        search_by_column('duration_of_term_e', keyword),
        search_by_column('duration_of_term_f', keyword)
    ]).drop_duplicates()

# --- Institution ---
def search_by_institution(keyword):
    """Search by institution name."""
    return pd.concat([
        search_by_column('institution_name_e', keyword),
        search_by_column('institution_name_f', keyword)
    ]).drop_duplicates()

# --- Contact info ---
def search_by_contact_name(keyword):
    """Search by contact person name."""
    return search_by_column('contact', keyword)

def search_by_contact_email(keyword):
    """Search by contact email address."""
    return search_by_column('contact_email', keyword)

# --- Program type ---
def search_by_program_type(keyword):
    """Search by program type (e.g., CO-OP, Internship)."""
    return pd.concat([
        search_by_column('program_type_e', keyword),
        search_by_column('program_type_f', keyword)
    ]).drop_duplicates()

# --- Specialization ---
def search_by_specialization(keyword):
    """Search by specialization or field of study."""
    return pd.concat([
        search_by_column('specialization_e', keyword),
        search_by_column('specialization_f', keyword)
    ]).drop_duplicates()

# --- Combined filter example ---
def search_combined(program=None, institution=None, level=None, specialization=None):
    """Search combining multiple filters."""
    result = df.copy()

    if program:
        result = result[result['program_of_study_e'].astype(str).str.contains(program, case=False, na=False)]
    if institution:
        result = result[result['institution_name_e'].astype(str).str.contains(institution, case=False, na=False)]
    if level:
        result = result[result['academic_level_area_of_study_e'].astype(str).str.contains(level, case=False, na=False)]
    if specialization:
        result = result[result['specialization_e'].astype(str).str.contains(specialization, case=False, na=False)]

    return result

# === Example usage ===
if __name__ == "__main__":
    print_culomns()
    # print("=== Example Queries ===")
    #
    # # Example 1: Find all Bachelor-level programs
    # print("\n--- Bachelor Programs ---")
    # print(search_by_academic_level("Bachelor")[['institution_name_e', 'program_of_study_e']].head())
    #
    # # Example 2: Find all Engineering programs
    # print("\n--- Engineering Programs ---")
    # print(search_by_specialization("Computer Science")[['institution_name_e', 'program_of_study_e', 'specialization_e']].head())
    #
    # # Example 3: Find programs by specific institution
    print("\n--- Programs at BCIT ---")
    print(search_by_institution("British Columbia Institute of technology")[['institution_name_e', 'program_of_study_f']].head())
    #
    # # Example 4: Combined search
    print("\n--- Bachelor in Computer-related fields ---")
    combined = search_combined(program="nursing", level="Doctorate")
    print(combined[['institution_name_e', 'program_of_study_e', 'academic_level_area_of_study_e']].head())
