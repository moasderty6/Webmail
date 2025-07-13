import subprocess

def generate_emails(masked_email):
    prefix = masked_email.split("@")[0]
    domain = masked_email.split("@")[1]
    chars = "abcdefghijklmnopqrstuvwxyz0123456789"
    emails = []

    for c1 in chars:
        for c2 in chars:
            guess = f"{prefix[0]}{c1}{c2}{prefix[-1]}"
            emails.append(f"{guess}@{domain}")
            if len(emails) >= 30:
                return emails
    return emails

async def check_email_with_holehe(emails, username):
    results = []
    for email in emails:
        try:
            output = subprocess.check_output(
                ["python3", "holehe_wrapper/run.py", email],
                text=True
            )
            if "Instagram" in output:
                results.append(email)
        except Exception as e:
            continue
    return results
