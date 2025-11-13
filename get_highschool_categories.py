import pandas as pd
from get_cip_from_noc import get_cip_codes
from rapidfuzz import fuzz, process
from collections import defaultdict


def get_highschool_categories(noc_code):
    cip_list = get_cip_codes(noc_code)
    highschool_csvs = ["highschool_closed_courses.csv", "highschool_open_courses.csv"]

    matching_courses = set()
    main_to_subs = defaultdict(set)
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
                    matching_courses.add(course_name)
                    main_to_subs[main_cat].add(sub_cat)
    main_to_subs = {
        main: sorted(subs) for main, subs in main_to_subs.items()
    }

    return matching_courses, main_to_subs

def highschool_bucket_mapping(main_to_subs):
    hst_to_bucket = {
        # 1️⃣ AGRICULTURE / ENVIRONMENT
        "01 AGRIBUSINESS AND AGRICULTURAL PRODUCTION": "Agriculture",
        "02 AGRICULTURAL SCIENCES": "Agriculture",
        "03 RENEWABLE NATURAL RESOURCES": "Agriculture",

        # 2️⃣ ARCHITECTURE / ENGINEERING / TRADES
        "04 ARCHITECTURE AND ENVIRONMENTAL DESIGN": "Engineering",
        "14 ENGINEERING": "Engineering",
        "15 ENGINEERING AND ENGINEERING-RELATED TECHNOLOGIES": "Engineering",
        "46 CONSTRUCTION TRADES": "Engineering",
        "47 MECHANICS AND REPAIRERS": "Engineering",
        "48 PRECISION PRODUCTION": "Engineering",
        "49 TRANSPORTATION AND MATERIAL MOVING": "Engineering",
        "21 INDUSTRIAL ARTS": "Engineering",

        # 3️⃣ ARTS / DESIGN / HUMANITIES
        "05 AREA AND ETHNIC STUDIES": "Arts",
        "50 VISUAL AND PERFORMING ARTS": "Arts",
        "38 PHILOSOPY AND RELIGION": "Arts",
        "04 ARCHITECTURE AND ENVIRONMENTAL DESIGN": "Arts",  # overlaps okay

        # 4️⃣ BUSINESS / COMMERCE / MANAGEMENT
        "06 BUSINESS AND MANAGEMENT": "Business",
        "07 BUSINESS AND OFFICE": "Business",
        "08 MARKETING AND DISTRIBUTION": "Business",
        "52 GENERAL (INCLUDING PRE-VOCATIONAL PROGRAMS) EMH": "Business",

        # 5️⃣ COMMUNICATIONS / MEDIA / TECHNOLOGY
        "09 COMMUNICATIONS": "Communications",
        "10 COMMUNICATION TECHNOLOGIES": "Communications",
        "11 COMPUTER AND INFORMATION SCIENCES": "Communications",

        # 6️⃣ CONSUMER / PERSONAL / HOME ECONOMICS
        "12 CONSUMER, PERSONAL, AND MISCELLANEOUS SERVICES": "Home Economics",
        "19 HOME ECONOMICS.": "Home Economics",
        "20 VOCATIONAL HOME ECONOMICS": "Home Economics",
        "37 PERSONAL AWARENESS.": "Home Economics",

        # 7️⃣ EDUCATION / BASIC SKILLS
        "13 EDUCATION": "General",
        "32 BASIC SKILLS": "General",

        # 8️⃣ FOREIGN LANGUAGES / ENGLISH / COMMUNICATION
        "16 FOREIGN LANGUAGES": "Languages",
        "23 LETTERS/ENGLISH": "Languages",

        # 9️⃣ HEALTH / LIFE SCIENCES
        "17 ALLIED HEALTH": "Health",
        "18 HEALTH SCIENCES": "Health",
        "26 LIFE SCIENCES": "Health",
        "34 HEALTH RELATED ACTIVITIES": "Health",

        # 🔟 MATHEMATICS / SCIENCE / TECHNOLOGY
        "27 MATHEMATICS": "STEM",
        "40 PHYSICAL SCIENCES": "STEM",
        "41 SCIENCE TECHNOLOGIES": "STEM",
        "30 MULTI/INTERDISCIPLINARY STUDIES": "STEM",

        # 11️⃣ SOCIAL SCIENCES / LAW / CIVICS
        "22 LAW": "Social Studies",
        "24 LIBERAL/GENERAL STUDIES": "Social Studies",
        "28 MILITARY SCIENCES": "Social Studies",
        "33 CITIZENSHIP/CIVIC ACTIVITIES": "Social Studies",
        "35 INTERPERSONAL SKILLS": "Social Studies",
        "42 PSYCHOLOGY": "Social Studies",
        "43 PROTECTIVE SERVICES": "Social Studies",
        "45 SOCIAL SCIENCES": "Social Studies",

        # 12️⃣ PHYSICAL EDUCATION / RECREATION
        "31 PARKS AND RECREATION": "Physical Education",
        "36 LEISURE AND RECREATIONAL ACTIVITIES": "Physical Education",

        # SPECIAL EDUCATION catch-all
        "54 SPECIAL EDUCATION -": "Special Education",
        "56 SPECIAL EDUCATION - RESOURCE CURRICULUM - SUBJECT AREA SERVICES": "Special Education",
    }
    example_buckets = ["Agriculture", "Engineering", "Arts", "Business", "Communications", "Home Economics", "General",
                       "Languages", "Health", "STEM", "Social Studies", "Physical Education", "Special Education"]
    final_buckets = set()
    buckets_count = [0] * len(example_buckets)
    subcats_by_bucket = [[] for _ in example_buckets]

    for main_cat, subcats in main_to_subs.items():
        bucket = hst_to_bucket.get(main_cat)
        if not bucket:
            continue

        final_buckets.add(bucket)
        idx = example_buckets.index(bucket)
        buckets_count[idx] = 1

        for sub_cat in subcats:
            if sub_cat not in subcats_by_bucket[idx]:
                subcats_by_bucket[idx].append(sub_cat[3:])

    return final_buckets, buckets_count, subcats_by_bucket


highschool_data = get_highschool_categories(21231)

buckets, counts, subcats = highschool_bucket_mapping(highschool_data[1])

print("\nFinal High School Buckets")
for bucket in buckets:
    print(bucket)

print("\nBucket Indicators")
print(counts)

print("\nSub Categories in each bucket")
for name, subs in zip(
    ["Agriculture", "Engineering", "Arts", "Business", "Communications",
     "Home Economics", "General", "Languages", "Health", "STEM",
     "Social Studies", "Physical Education", "Special Education"],
    subcats,
):
    print(name, "→", subs)
