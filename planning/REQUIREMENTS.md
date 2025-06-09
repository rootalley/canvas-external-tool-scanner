# Requirements

## Functional
- Load `CANVAS_ACCESS_TOKEN`, `CANVAS_PROD_HOSTNAME`, and `CANVAS_ROOT_ACCOUNT_ID` from OS environment variables or a .env file
- Accept tool ID, term IDs, and output file path as command-line arguments
- Query all courses in the specified SIS term IDs
- For each course, check if the specified external tool ID is enabled in the navigation menu
- For each match, write a CSV file listing: term_id, course_id, course_name

## Non-Functional
- Check `rel="next"` on all API responses to handle Canvas pagination
- Fail gracefully on API errors
- Output CSV to the specified output file (default: `output/enabled_courses.csv`)
