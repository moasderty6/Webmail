import subprocess
import re

def generate_emails(masked_email):
    chars = "abcdefghijklmnopqrstuvwxyz0123456789._"
    prefix, domain = masked_email.split("@")
    emails = []

    for c1 in chars:
        for c2 in chars:
            for c3 in chars:
                for c4 in chars:
                    for c5 in chars:
                        guess = f"{prefix[0]}{c1}{c2}{c3}{c4}{c5}{prefix[-1]}"
                        emails.append(f"{guess}@{domain}")
                        if len(emails) >= 100:  # عدّل هذا الرقم حسب ما تريد
                            return emails
    return emails

async def check_email_with_holehe(emails, username):
    for email in emails:
        try:
            output = subprocess.check_output(["python3", "holehe_wrapper/run.py", email], text=True)
            if "Instagram" in output:
                return email
        except Exception:
            continue
    return None
