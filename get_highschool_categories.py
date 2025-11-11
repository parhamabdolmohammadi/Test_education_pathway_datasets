import pandas as pd
from get_cip_from_noc import get_cip_codes
from rapidfuzz import fuzz, process


def get_highschool_categories(noc_code):
    cip_list = get_cip_codes(noc_code)
    highschool_csvs = ["highschool_closed_courses.csv", "highschool_open_courses.csv"]

    matching_main_cats = set()
    matching_sub_cats = set()
    matching_courses = set()

    for file in highschool_csvs:
        print(f"🔍 Checking {file} ...")
        df = pd.read_csv(file)
        course_titles = df["Course Title"].str.lower().to_list()
        for cip in cip_list:
            cip_description = cip[6:].lower()
            matches = process.extract(
                cip_description, course_titles, scorer=fuzz.partial_ratio, limit=1
            )
            matches = [m for m in matches if m[1] >= 80]
            for course, score, _ in matches:
                row = df[df["Course Title"].str.contains(course.strip(), case=False, na=False, regex=False)]
                if not row.empty:
                    course_name = row.iloc[0]["Course Title"]
                    main_cat = row.iloc[0]["HST Main Category"]
                    sub_cat = row.iloc[0]["HST Sub Category"]
                    if course_name not in matching_courses:
                        matching_courses.add(course_name)
                    if main_cat not in matching_main_cats:
                        matching_main_cats.add(main_cat)
                    if sub_cat not in matching_sub_cats:
                        matching_sub_cats.add(sub_cat)

    return [list(matching_courses), list(matching_main_cats), list(matching_sub_cats)]

def highschool_bucket_mapping(main_cats):
    hst_to_bucket = {
        # 1️⃣ AGRICULTURE / ENVIRONMENT
        "01 AGRIBUSINESS AND AGRICULTURAL PRODUCTION": "Agriculture & Environment",
        "02 AGRICULTURAL SCIENCES": "Agriculture & Environment",
        "03 RENEWABLE NATURAL RESOURCES": "Agriculture & Environment",

        # 2️⃣ ARCHITECTURE / ENGINEERING / TRADES
        "04 ARCHITECTURE AND ENVIRONMENTAL DESIGN": "Engineering & Trades",
        "14 ENGINEERING": "Engineering & Trades",
        "15 ENGINEERING AND ENGINEERING-RELATED TECHNOLOGIES": "Engineering & Trades",
        "46 CONSTRUCTION TRADES": "Engineering & Trades",
        "47 MECHANICS AND REPAIRERS": "Engineering & Trades",
        "48 PRECISION PRODUCTION": "Engineering & Trades",
        "49 TRANSPORTATION AND MATERIAL MOVING": "Engineering & Trades",
        "21 INDUSTRIAL ARTS": "Engineering & Trades",

        # 3️⃣ ARTS / DESIGN / HUMANITIES
        "05 AREA AND ETHNIC STUDIES": "Arts, Design & Humanities",
        "50 VISUAL AND PERFORMING ARTS": "Arts, Design & Humanities",
        "38 PHILOSOPY AND RELIGION": "Arts, Design & Humanities",
        "04 ARCHITECTURE AND ENVIRONMENTAL DESIGN": "Arts, Design & Humanities",  # overlaps okay

        # 4️⃣ BUSINESS / COMMERCE / MANAGEMENT
        "06 BUSINESS AND MANAGEMENT": "Business & Commerce",
        "07 BUSINESS AND OFFICE": "Business & Commerce",
        "08 MARKETING AND DISTRIBUTION": "Business & Commerce",
        "52 GENERAL (INCLUDING PRE-VOCATIONAL PROGRAMS) EMH": "Business & Commerce",

        # 5️⃣ COMMUNICATIONS / MEDIA / TECHNOLOGY
        "09 COMMUNICATIONS": "Communications & Media",
        "10 COMMUNICATION TECHNOLOGIES": "Communications & Media",
        "11 COMPUTER AND INFORMATION SCIENCES": "Communications & Media",

        # 6️⃣ CONSUMER / PERSONAL / HOME ECONOMICS
        "12 CONSUMER, PERSONAL, AND MISCELLANEOUS SERVICES": "Home Economics & Life Skills",
        "19 HOME ECONOMICS.": "Home Economics & Life Skills",
        "20 VOCATIONAL HOME ECONOMICS": "Home Economics & Life Skills",
        "37 PERSONAL AWARENESS.": "Home Economics & Life Skills",

        # 7️⃣ EDUCATION / BASIC SKILLS
        "13 EDUCATION": "Education & Basic Skills",
        "32 BASIC SKILLS": "Education & Basic Skills",

        # 8️⃣ FOREIGN LANGUAGES / ENGLISH / COMMUNICATION
        "16 FOREIGN LANGUAGES": "Languages & Literature",
        "23 LETTERS/ENGLISH": "Languages & Literature",

        # 9️⃣ HEALTH / LIFE SCIENCES
        "17 ALLIED HEALTH": "Health & Life Sciences",
        "18 HEALTH SCIENCES": "Health & Life Sciences",
        "26 LIFE SCIENCES": "Health & Life Sciences",
        "34 HEALTH RELATED ACTIVITIES": "Health & Life Sciences",

        # 🔟 MATHEMATICS / SCIENCE / TECHNOLOGY
        "27 MATHEMATICS": "Science, Technology, Engineering & Math (STEM)",
        "40 PHYSICAL SCIENCES": "Science, Technology, Engineering & Math (STEM)",
        "41 SCIENCE TECHNOLOGIES": "Science, Technology, Engineering & Math (STEM)",
        "30 MULTI/INTERDISCIPLINARY STUDIES": "Science, Technology, Engineering & Math (STEM)",

        # 11️⃣ SOCIAL SCIENCES / LAW / CIVICS
        "22 LAW": "Social Sciences & Civics",
        "24 LIBERAL/GENERAL STUDIES": "Social Sciences & Civics",
        "28 MILITARY SCIENCES": "Social Sciences & Civics",
        "33 CITIZENSHIP/CIVIC ACTIVITIES": "Social Sciences & Civics",
        "35 INTERPERSONAL SKILLS": "Social Sciences & Civics",
        "42 PSYCHOLOGY": "Social Sciences & Civics",
        "43 PROTECTIVE SERVICES": "Social Sciences & Civics",
        "45 SOCIAL SCIENCES": "Social Sciences & Civics",

        # 12️⃣ PHYSICAL EDUCATION / RECREATION
        "31 PARKS AND RECREATION": "Physical Education & Recreation",
        "36 LEISURE AND RECREATIONAL ACTIVITIES": "Physical Education & Recreation",

        # SPECIAL EDUCATION catch-all
        "54 SPECIAL EDUCATION -": "Special Education & Support",
        "56 SPECIAL EDUCATION - RESOURCE CURRICULUM - SUBJECT AREA SERVICES": "Special Education & Support",
    }
    final_buckets = set()
    for category in main_cats:
        bucket = hst_to_bucket.get(category)
        if bucket not in final_buckets:
            final_buckets.add(bucket)

    return final_buckets


highschool_data = get_highschool_categories(21231)

buckets = highschool_bucket_mapping(highschool_data[1])

print("\nFinal High School Buckets")
for bucket in buckets:
    print(bucket)

# List of Buckets for formating front end:
# Agriculture & Environment
# Engineering & Trades
# Arts, Design & Humanities
# Business & Commerce
# Communications & Media
# Home Economics & Life Skills
# Education & Basic Skills
# Languages & Literature
# Health & Life Sciences
# Science, Technology, Engineering & Math (STEM)
# Social Sciences & Civics
# Physical Education & Recreation
# Special Education & Support
