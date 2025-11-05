# job_fetcher.py
import requests
from bs4 import BeautifulSoup
from datetime import datetime

USER_AGENT = "Mozilla/5.0 (compatible; MithleshAgent/2.0; +https://github.com/)"
HEADERS = {"User-Agent": USER_AGENT}

# keywords you care about
KEYWORDS = ["full stack", "full-stack", "fullstack", "react", "node", "php", "laravel", "aws", "typescript", "next.js", "frontend", "backend"]

# allowed / blocked regions
ALLOWED_COUNTRIES = [
    "remote", "india", "china", "uk", "england", "germany", "australia",
    "canada", "usa", "united states", "europe", "singapore", "malaysia", "uae"
]
BLOCKED_COUNTRIES = ["pakistan", "turkey"]

def text_match(title, desc):
    txt = (title + " " + desc).lower()
    return any(k in txt for k in KEYWORDS)

def region_ok(location):
    loc = (location or "").lower()
    if any(b in loc for b in BLOCKED_COUNTRIES):
        return False
    if any(a in loc for a in ALLOWED_COUNTRIES):
        return True
    # if no location given, but mentions remote, still accept
    return "remote" in loc or loc.strip() == ""

# -------------------------------
# Fetch from RemoteOK API (JSON)
# -------------------------------
def fetch_remoteok(max_results=10):
    print("Fetching jobs from RemoteOK...")
    jobs = []
    try:
        resp = requests.get("https://remoteok.com/api", headers=HEADERS, timeout=20)
        data = resp.json()
        for job in data[1:]:
            title = job.get("position") or job.get("title", "")
            company = job.get("company", "")
            location = job.get("location", "") or "remote"
            url = job.get("url", "")
            desc = job.get("description", "")
            if not text_match(title, desc):
                continue
            if not region_ok(location):
                continue
            jobs.append({
                "source": "RemoteOK",
                "title": title,
                "company": company,
                "url": url,
                "location": location,
                "date": datetime.utcnow().isoformat()
            })
            if len(jobs) >= max_results:
                break
    except Exception as e:
        print("❌ RemoteOK error:", e)
    print(f"✅ RemoteOK: {len(jobs)} jobs")
    return jobs


# -------------------------------
# Fetch from WeWorkRemotely
# -------------------------------
def fetch_weworkremotely(max_results=10):
    print("Fetching jobs from WeWorkRemotely...")
    url = "https://weworkremotely.com/categories/remote-programming-jobs"
    jobs = []
    try:
        resp = requests.get(url, headers=HEADERS, timeout=20)
        soup = BeautifulSoup(resp.text, "html.parser")
        posts = soup.select("section.jobs article li a")
        for a in posts:
            try:
                title_el = a.select_one("span.title")
                company_el = a.select_one("span.company")
                if not title_el:
                    continue
                title_txt = title_el.get_text(strip=True)
                company_txt = company_el.get_text(strip=True) if company_el else "Unknown"
                href = a.get('href') or ''
                if href and not href.startswith('http'):
                    href = 'https://weworkremotely.com' + href
                # fetch location snippet
                desc = ""
                try:
                    d = requests.get(href, headers=HEADERS, timeout=10)
                    desc = d.text[:1500]
                except Exception:
                    desc = ""
                if not text_match(title_txt, desc):
                    continue
                # extract location from description or skip if blocked
                loc = "remote"
                if any(b in desc.lower() for b in BLOCKED_COUNTRIES):
                    continue
                jobs.append({
                    "source": "WeWorkRemotely",
                    "title": title_txt,
                    "company": company_txt,
                    "url": href,
                    "location": loc,
                    "date": datetime.utcnow().isoformat()
                })
                if len(jobs) >= max_results:
                    break
            except Exception:
                continue
    except Exception as e:
        print("❌ WeWorkRemotely error:", e)
    print(f"✅ WeWorkRemotely: {len(jobs)} jobs")
    return jobs


# -------------------------------
# Combine + dedupe
# -------------------------------
def fetch_all(max_results=10):
    print("🔎 Starting job aggregation...")
    jobs = []
    jobs += fetch_remoteok(max_results=max_results)
    if len(jobs) < max_results:
        jobs += fetch_weworkremotely(max_results=max_results - len(jobs))

    # dedupe by URL
    seen = set()
    unique = []
    for j in jobs:
        if j["url"] in seen:
            continue
        seen.add(j["url"])
        unique.append(j)

    print(f"✅ Total unique jobs: {len(unique)}")
    return unique[:max_results]


if __name__ == "__main__":
    jobs = fetch_all(10)
    for job in jobs:
        print(f"{job['company']} | {job['title']} | {job['location']} | {job['url']}")
