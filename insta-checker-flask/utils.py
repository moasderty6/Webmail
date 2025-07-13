import random
import subprocess
import asyncio

def generate_emails(masked_email):
    chars = "abcdefghijklmnopqrstuvwxyz0123456789_."
    prefix, domain = masked_email.split("@")
    first = prefix[0]
    last = prefix[-1]

    emails = []
    for c1 in chars:
        for c2 in chars:
            for c3 in chars:
                for c4 in chars:
                    guess = f"{first}{c1}{c2}{c3}{c4}{last}"
                    emails.append(f"{guess}@{domain}")
                    if len(emails) >= 100000:  # 100 ألف احتمال
                        return emails
    return emails

def load_proxies():
    try:
        with open("proxies.txt") as f:
            return [line.strip() for line in f if line.strip()]
    except:
        return []

async def run_check(email):
    proxy_list = load_proxies()
    proxy = random.choice(proxy_list) if proxy_list else None
    cmd = ["python3", "holehe_wrapper/run.py", email]
    if proxy:
        cmd += ["--proxy", proxy]
    try:
        output = await asyncio.to_thread(subprocess.check_output, cmd, text=True, timeout=10)
        if "Instagram" in output:
            return email
    except:
        pass
    return None

async def check_email_with_holehe(email_generator, username):
    MAX_PARALLEL = 500

    async def process_batch(batch):
        tasks = [run_check(email) for email in batch]
        results = await asyncio.gather(*tasks)
        for r in results:
            if r:
                return r
        return None

    batch = []
    for email in email_generator:
        batch.append(email)
        if len(batch) >= MAX_PARALLEL:
            result = await process_batch(batch)
            if result:
                return result
            batch = []
    if batch:
        return await process_batch(batch)
    return None
