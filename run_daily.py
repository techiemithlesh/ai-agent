# run_daily.py

from dotenv import load_dotenv
load_dotenv()
import os

from job_fetcher import fetch_all
from cover_letter_gen import generate_cover
from sheets_logger import append_job
from notifier import send_msg

MAX = int(os.environ.get('MAX_RESULTS', '8'))

def main():
    jobs = fetch_all(MAX)
    print(f"Fetched {len(jobs)} jobs")

    # If no jobs found, insert a test one manually
    if len(jobs) == 0:
        print("⚠️  No jobs fetched, adding a sample job for testing.")
        jobs = [{
            "source": "ManualTest",
            "company": "Sample Corp",
            "title": "Remote Full Stack Developer",
            "url": "https://example.com/job/123"
        }]

    summary = []
    for j in jobs:
        cover = generate_cover(j['title'], j['company'])
        j['cover'] = cover
        try:
            append_job(j)
            summary.append(f"{j['company']} - {j['title']}\n{j['url']}")
        except Exception as e:
            summary.append(f"(Failed to log) {j['company']} - {j['title']}: {e}")

    if summary:
        msg = "New jobs added:\n\n" + "\n\n".join(summary[:20])
        send_msg(msg)
    else:
        send_msg('No new jobs matched today.')

    print('Done')


if __name__ == '__main__':
    main()
