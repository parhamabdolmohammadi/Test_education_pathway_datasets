import requests
from xml.etree import ElementTree
import pandas as pd
from requests.auth import HTTPBasicAuth

CSV_PATH = "Occupations.csv"
df = pd.read_csv(CSV_PATH, skiprows=3)  # skip metadata rows if needed

USERNAME = "gibsub_ai"
PASSWORD = "2533qxz"



def print_culomns():
    print("=== ALL FEATURE (COLUMN) NAMES IN THE DATASET ===\n")
    for i, col in enumerate(df.columns, start=1):
        print(f"{i}. {col}")

def get_career_by_soc(soc_code):
    """
    Look up a career and description by SOC code.
    Example: get_career_by_soc("15-1252.00")
    """
    # Normalize SOC code input
    soc_code = soc_code.strip()

    # Filter matching rows
    result = df[df["O*NET-SOC"].astype(str).str.strip() == soc_code]

    if result.empty:
        print(f"❌ No occupation found for SOC code: {soc_code}")
        return None

    row = result.iloc[0]
    career = row["Career"]
    description = row["Description"]

    print(f"✅ Found occupation for {soc_code}:")
    print(f"🎓 Career: {career}")
    print(f"📝 Description: {description}")

    return {"soc": soc_code, "career": career, "description": description}



def get_soc_by_career(career_name):
    """
    Look up SOC code(s) and description(s) by career name.
    Example: get_soc_by_career("Software Developer")
    """
    career_name = career_name.strip()

    # Find partial matches, case-insensitive
    matches = df[df["O*NET-SOC 2019 Title"].astype(str).str.contains(career_name, case=False, na=False)]

    if matches.empty:
        print(f"❌ No matches found for career: '{career_name}'")
        return None

    print(f"✅ Found {len(matches)} match(es) for '{career_name}':\n")

    results = []
    for _, row in matches.iterrows():
        soc = row["O*NET-SOC 2019 Code"]
        career = row["O*NET-SOC 2019 Title"]
        desc = row["O*NET-SOC 2019 Description"]

        print(f"🔹 SOC: {soc}")
        print(f"🎓 Career: {career}")
        print(f"📝 Description: {desc}\n")

        results.append({"soc": soc, "career": career, "description": desc})

    return results



# def get_soc_code(job_title):
#     """Search O*NET for SOC code(s) given a job title."""
#     url = f"https://services.onetcenter.org/ws/online/occupations/?keyword={job_title}"
#     url = f"https://services.onetcenter.org/ws/online/crosswalks/soc?keyword=[title or code]"
#     response = requests.get(url, auth=(USERNAME, PASSWORD))
#
#     if response.status_code != 200:
#         print(f"❌ Error {response.status_code}: {response.text}")
#         return None
#
#     tree = ElementTree.fromstring(response.text)
#     occupations = tree.findall(".//occupation")
#
#     if not occupations:
#         print("❌ No SOC code found for that job title.")
#         return None
#
#     print(f"\n🔍 Found {len(occupations)} related occupations:\n")
#     for i, occ in enumerate(occupations, start=1):
#         title = occ.findtext("title")
#         code = occ.findtext("code")
#         print(f"{i}. {title} → {code}")
#
#     # Try to find the one that closely matches the user's title
#     best_match = None
#     for occ in occupations:
#         title = occ.findtext("title") or ""
#         if job_title.lower() in title.lower():
#             best_match = occ
#             break
#
#     # If no close match found, pick the first one
#     if not best_match:
#         best_match = occupations[0]
#
#     title = best_match.findtext("title")
#     code = best_match.findtext("code")
#     print(f"\n Selected: {title} → {code}")
#     return code





#NOT WORKING CORRECTLY
def get_skills_summary(soc_code):
    """Get top skill descriptions for a given SOC code."""
    # url = f"https://services.onetcenter.org/v1.9/ws/online/occupations/{soc_code}/summary/skills?display=long"
    # url =   f"https://services.onetcenter.org/v1.9/ws/online/occupations/17-3019.00/summary/skills"
    url = f"https://services.onetcenter.org/ws/mnm/careers/29-1141.00/skills"
    response = requests.get(url, auth=(USERNAME, PASSWORD))

    if response.status_code != 200:
        print(f"❌ Error {response.status_code}: {response.text}")
        return None

    # data = response.json()
    print(f"\nTop skills for {soc_code}:\n")
    print(response.text)
    # for skill in data.get("element", []):
    #     print(f"• {skill['name']}: {skill['description']}")
    return response

def get_skills_for_soc(soc_code):
    url = f"https://services.onetcenter.org/v1.9/ws/mnm/careers/{soc_code}/skills"
    headers = {"Accept": "application/json"}  # Force JSON
    res = requests.get(url, auth=HTTPBasicAuth(USERNAME, PASSWORD), headers=headers)

    if res.status_code != 200:
        print(f"❌ Failed to retrieve skills ({res.status_code}): {res.text[:500]}")
        return None

    try:
        data = res.json()
    except Exception:
        print("⚠️ Response not JSON, showing XML instead:")
        print(res.text[:500])
        return None

    print(f"\n🧩 Skills for {data.get('career', {}).get('title', 'Unknown')} ({soc_code}):\n")
    for skill in data.get("skills", []):
        print(f"• {skill['name']} (Category: {skill.get('category')}, Importance: {skill.get('importance', 'N/A')})")

    return data


if __name__ == "__main__":
    print_culomns()
    print(get_soc_by_career("Software developer"))
    # soc = get_soc_code("Software Developer")
    # if soc:
    print("hi")
    print(get_skills_for_soc("29-2061.00"))








