# Solution Outline

## Goal
Generate a CSV report of all Canvas courses in the specified SIS terms where a given external tool is enabled in the course navigation.

## Steps

1. Load API credentials from the OS or a `.env` file using `dotenv`
2. Parse command-line arguments for tool ID, SIS term IDs, and output file path
3. For each SIS term ID provided:
   - Fetch all courses using the Canvas API (GET /api/v1/accounts/:account_id/courses?enrollment_term_id=sis_term_id:{:sis_term_id})
   - Handle pagination using `rel="next"` headers
4. For each course:
   - Fetch course navigation menu items (GET /api/v1/courses/:course_id/tabs)
   - Check if the specified tool is present (by tab ID) and enabled (visibility: `public`)
5. If tool is enabled:
   - Append course info (term_id, course_id, course_name) to results list
6. Write results to the specified output CSV file
