# cover_letter_gen.py
import os, json
import openai

openai.api_key = os.environ.get('OPENAI_API_KEY')

BASE_PROMPT = """You are an assistant that writes a concise tailored application blurb for a Senior Full Stack Developer.
User details:
- Name: Mithlesh Patel
- Title: Senior Full Stack Web Developer (React, Node, PHP, AWS, Docker)
- Experience: 4+ years, 40+ projects, DevOps + AWS deployments
Write:
1) A short 3-4 sentence cover message optimized for remote job applications (friendly, concise).
2) A one-line "top skill fit" summary for the resume (bullet).
Output JSON with keys: cover, resume_bullet
"""

def generate_cover(job_title, company, responsibilities_snippet=""):
    prompt = BASE_PROMPT + f"\nJob title: {job_title}\nCompany: {company}\nResponsibilities snippet: {responsibilities_snippet}\n\nRespond with JSON with keys: cover, resume_bullet"
    try:
        resp = openai.ChatCompletion.create(
            model=os.environ.get('OPENAI_MODEL','gpt-4o-mini'),
            messages=[{"role":"user","content":prompt}],
            max_tokens=250,
            temperature=0.2
        )
        text = resp['choices'][0]['message']['content']
        # try to parse JSON
        try:
            parsed = json.loads(text)
            return parsed
        except Exception:
            return {"cover": text, "resume_bullet": ""}
    except Exception as e:
        return {"cover": f"Error generating cover: {e}", "resume_bullet": ""}

if __name__ == '__main__':
    print(generate_cover('Full Stack Developer', 'Acme Ltd'))
