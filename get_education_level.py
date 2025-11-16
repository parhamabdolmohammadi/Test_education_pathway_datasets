from rapidfuzz import fuzz, process

# --- Define fuzzy-ranking of education levels ---
EDU_LEVELS = {
    "PhD": 100,
    "Doctorate": 100,
    "MD": 95,
    "JD": 95,
    "Master": 80,
    "MSc": 80,
    "MA": 80,
    "MBA": 75,
    "Bachelor": 60,
    "BSc": 60,
    "BA": 60,
    "Associate": 45,
    "Diploma": 40,
    "Certificate": 35,
    "Trade Qualification": 32,
    "High School": 10,
    "GED": 8,
}

def get_highest_education(education_list):
    """
    Find the highest education entry using fuzzy matching.
    """
    best_entry = None
    best_score = -1

    for entry in education_list:
        degree_text = (entry.get("degree") or "").lower()

        # Fuzzy match against the defined education levels
        match, score, _ = process.extractOne(
            degree_text,
            EDU_LEVELS.keys(),
            scorer=fuzz.partial_ratio
        )

        # Weighted score = fuzzy match * hierarchy score
        weighted = score * EDU_LEVELS[match]

        if weighted > best_score:
            best_score = weighted
            best_entry = {
                "matched_level": match,
                "hierarchy_score": EDU_LEVELS[match],
                "fuzzy_score": score,
                "combined_score": weighted,
                "entry": entry
            }

    return best_entry

# --- Example usage ---

education_data = [
    {
        "id": "edu_1",
        "degree": "Diploma or Certificate in Machining, Manufacturing Technology, or equivalent trade qualification",
        "institution": "Unknown Institution",
        "graduation_date": None,
        "gpa": None,
        "location": None,
        "relevant_courses": [],
        "confidence": 0.7
    },
    {
        "id": "edu_2",
        "degree": "Bachelor of Applied Science in Mechanical Engineering",
        "institution": "University of Example",
        "graduation_date": "2019-06-01",
        "gpa": 3.2,
        "location": "Vancouver",
        "relevant_courses": [],
        "confidence": 0.9
    }
]

highest = get_highest_education(education_data)
print(highest["matched_level"])
