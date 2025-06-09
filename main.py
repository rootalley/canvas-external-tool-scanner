"""
main.py

Entry point for the Canvas Tool Checker CLI script.
Loads environment variables using python-dotenv.
"""


import os
import argparse
from dotenv import load_dotenv


def parse_args():
    parser = argparse.ArgumentParser(description="Scan Canvas courses for enabled external tools.")
    parser.add_argument(
        "--tool-id",
        required=True,
        help="Canvas external tool tab ID (e.g., context_external_tool_36409)",
    )
    parser.add_argument(
        "--term-ids",
        required=True,
        help="Comma-separated list of SIS term IDs (e.g., 2024-30,2024-40,2025-20)",
    )
    parser.add_argument(
        "--output",
        default="output/enabled_courses.csv",
        help="Output CSV file path (default: output/enabled_courses.csv)",
    )
    return parser.parse_args()

def load_env_vars() -> None:
    """
    Load environment variables from a .env file and the OS environment.
    Raises an error if required variables are missing.
    """
    load_dotenv()
    required_vars = ["CANVAS_ACCESS_TOKEN", "CANVAS_PROD_HOSTNAME"]
    missing = [var for var in required_vars if not os.getenv(var)]
    if missing:
        raise EnvironmentError(f"Missing required environment variables: {', '.join(missing)}")


def main():
    args = parse_args()
    load_env_vars()
    print("Environment variables loaded successfully.")

    # Canvas API setup
    access_token = os.getenv("CANVAS_ACCESS_TOKEN")
    hostname = os.getenv("CANVAS_PROD_HOSTNAME")
    account_id = os.getenv("CANVAS_ROOT_ACCOUNT_ID")
    term_ids = [tid.strip() for tid in args.term_ids.split(",") if tid.strip()]
    headers = {"Authorization": f"Bearer {access_token}"}

    # Debug: Show loaded environment variables (mask token)
    print(f"[DEBUG] CANVAS_ACCESS_TOKEN: {access_token[:6]}...{access_token[-4:]}")
    print(f"[DEBUG] CANVAS_PROD_HOSTNAME: {hostname}")
    print(f"[DEBUG] CANVAS_ROOT_ACCOUNT_ID: {account_id}")
    print(f"[DEBUG] TOOL_ID: {args.tool_id}")
    print(f"[DEBUG] TERM_IDS: {term_ids}")
    print(f"[DEBUG] OUTPUT: {args.output}")

    def get_courses_for_term(term_id: str):
        """
        Fetch all courses for a given term_id, handling pagination.
        """
        import requests
        courses = []
        url = f"https://{hostname}/api/v1/accounts/{account_id}/courses?enrollment_term_id=sis_term_id:{term_id}&per_page=100"
        print(f"[DEBUG] Requesting: {url}")
        while url:
            resp = requests.get(url, headers=headers)
            print(f"[DEBUG] Response status: {resp.status_code}")
            if resp.status_code != 200:
                print(f"[DEBUG] Response text: {resp.text}")
                print(f"Failed to fetch courses for term {term_id}: {resp.status_code}")
                break
            data = resp.json()
            courses.extend(data)
            # Handle pagination
            next_url = None
            if 'link' in resp.headers:
                links = resp.headers['link'].split(',')
                for link in links:
                    if 'rel="next"' in link:
                        next_url = link[link.find('<')+1:link.find('>')]
                        break
            url = next_url
        return courses

    all_courses = []
    for term_id in term_ids:
        print(f"Fetching courses for term {term_id}...")
        courses = get_courses_for_term(term_id)
        print(f"  Found {len(courses)} courses.")
        for course in courses:
            course['term_id'] = term_id  # Track term for later
        all_courses.extend(courses)

    print(f"Total courses fetched: {len(all_courses)}")

    # Step 2: Check for the specified external tool in each course
    import requests
    TOOL_ID = args.tool_id
    enabled_courses = []
    for course in all_courses:
        course_id = course.get("id")
        course_name = course.get("name", "")
        term_id = course.get("term_id", "")
        tabs_url = f"https://{hostname}/api/v1/courses/{course_id}/tabs"
        print(f"[DEBUG] Checking course {course_id} ({course_name}) tabs...")
        resp = requests.get(tabs_url, headers=headers)
        if resp.status_code != 200:
            print(f"[DEBUG] Failed to fetch tabs for course {course_id}: {resp.status_code}")
            continue
        tabs = resp.json()
        for tab in tabs:
            if tab.get("id") == TOOL_ID and tab.get("visibility") == "public":
                print(f"[DEBUG] Tool enabled in course {course_id} ({course_name})")
                enabled_courses.append({
                    "term_id": term_id,
                    "course_id": course_id,
                    "course_name": course_name
                })
                break
    print(f"Courses with tool {TOOL_ID} enabled: {len(enabled_courses)}")

    # Step 3: Write results to CSV
    import csv
    output_file = args.output
    output_dir = os.path.dirname(output_file)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
    with open(output_file, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["term_id", "course_id", "course_name"])
        writer.writeheader()
        for row in enabled_courses:
            writer.writerow(row)
    print(f"Wrote results to {output_file}")


if __name__ == "__main__":
    main()
