# sheets_logger.py
import os, base64, json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()


# Load Sheet ID from environment
SHEET_ID = os.environ.get('SHEET_ID', '1031509104')

def get_client_from_json(json_path=None):
    """Authorize Google Sheets API client using either base64 env or a JSON file."""
    creds_b64 = os.environ.get('GOOGLE_SHEETS_CREDENTIALS_JSON')
    if creds_b64:
        creds_json = json.loads(base64.b64decode(creds_b64).decode())
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_json, scopes=[
            'https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive'
        ])
    elif json_path:
        creds = ServiceAccountCredentials.from_json_keyfile_name(json_path, scopes=[
            'https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive'
        ])
    else:
        raise Exception('Provide GOOGLE_SHEETS_CREDENTIALS_JSON env or json path')
    client = gspread.authorize(creds)
    return client


def append_job(job):
    """Append job info to Google Sheet and log to local file for debugging."""
    print("Attempting to append job:", job.get('title'))
    client = get_client_from_json()
    sh = client.open_by_key(SHEET_ID)
    ws = sh.sheet1

    # Row data for sheet
    row = [
        datetime.now().strftime('%Y-%m-%d'),
        job.get('company',''),
        job.get('title',''),
        job.get('source',''),
        'Remote',
        'Applied',
        '',
        job.get('url','')
    ]

    print("Appending row to sheet now...")

    # Try writing to Google Sheet
    try:
        ws.append_row(row, value_input_option='RAW')
        print("✅ Row appended successfully.")
    except Exception as e:
        print("❌ Failed to write to Google Sheet:", e)

    # Always write to a local log file too
    try:
        with open("local_job_log.txt", "a", encoding="utf-8") as f:
            f.write(f"{datetime.now()} | {job.get('company')} | {job.get('title')} | {job.get('url')}\n")
        print("🗒️ Logged locally in local_job_log.txt")
    except Exception as e:
        print("⚠️ Could not write local log file:", e)

    return True


if __name__ == '__main__':
    sample = {
        "company": "TestCo",
        "title": "Full Stack Developer",
        "source": "Upwork",
        "url": "https://codewithmithelsh"
    }
    print('Appending sample (ensure env vars are set)')
    append_job(sample)
