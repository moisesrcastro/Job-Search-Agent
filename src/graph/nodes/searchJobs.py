import httpx
import html
import re


def clean_text(text):
    unescaped = html.unescape(text)
    return re.sub(r"<[^>]+>|&nbsp;|&amp;", "", unescaped)


async def getJobs(role, COMPANIES, max_jobs=20):

    role = role.lower()
    all_jobs = []

    async with httpx.AsyncClient() as client:

        for company in COMPANIES:

            r = await client.get(
                f"https://boards-api.greenhouse.io/v1/boards/{company}/jobs"
            )

            if r.status_code != 200:
                continue

            for job in r.json().get("jobs", []):
                title = job["title"].lower()
                location = job["location"]["name"].lower()

                if role in title and "brazil" in location:
                    job["company"] = company
                    all_jobs.append(job)

    all_jobs = all_jobs[:max_jobs]

    async with httpx.AsyncClient() as client:

        for job in all_jobs:

            company = job["company"]
            job_id = job["id"]

            r = await client.get(
                f"https://boards-api.greenhouse.io/v1/boards/{company}/jobs/{job_id}"
            )

            if r.status_code != 200:
                continue

            content = r.json().get("content", "")
            job["description"] = clean_text(content)

    return all_jobs