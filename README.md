# Mithlesh Job Agent - Full Integration

This repository contains a full AI Agent MVP that:
- fetches remote job postings from public job boards (RemoteOK, WeWorkRemotely)
- generates a short tailored cover blurb using OpenAI
- logs found jobs to your Google Sheet tracker (SHEET_ID default set)
- sends a Telegram summary (optional)

**Important:** This agent *does not auto-submit applications*. It prepares everything so you can complete an apply in 30-90s.

---
## What's included
- job_fetcher.py -- scrapes job boards and filters by keywords
- cover_letter_gen.py -- uses OpenAI to produce a short cover message and a resume bullet
- sheets_logger.py -- appends found jobs to your Google Sheet (default SHEET_ID=1031509104)
- notifier.py -- sends Telegram notifications (optional)
- run_daily.py -- orchestration script
- requirements.txt -- Python dependencies
- .github_workflow_daily.yml -- sample GitHub Actions workflow

## Setup (quick)
1. Create a Google Service Account and share your Job Tracker sheet with the service account email.
   - Google Cloud Console -> IAM & Admin -> Service Accounts -> Create -> Key (JSON)
   - Copy the JSON, base64-encode it: `base64 service_account.json | pbcopy` (or use Linux `base64`)
   - Add that base64 string to GitHub Secrets as `GOOGLE_SHEETS_CREDENTIALS_JSON` or set it in your environment.
2. If you want to use the provided default SHEET_ID, ensure the sheet ID is numeric and the service account has access.
   The default SHEET_ID in this repo is set to: 1031509104
3. Add `OPENAI_API_KEY` to GitHub Secrets.
4. (Optional) Create a Telegram bot via @BotFather and set `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID`.
5. Push this repo to GitHub and enable Actions, or run locally:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   export OPENAI_API_KEY='sk-...'
   export SHEET_ID='1031509104'
   export GOOGLE_SHEETS_CREDENTIALS_JSON='(base64 json)'
   python run_daily.py
   ```

## Security notes
- Never commit your service account JSON or API keys to the repo.
- Use GitHub Secrets for storing credentials when using Actions.

## Next steps
- Test run locally with `python run_daily.py` after setting env vars.
- If everything works, push to GitHub and enable the workflow.
