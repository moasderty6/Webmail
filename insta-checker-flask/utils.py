import subprocess
import itertools
import string

def generate_emails(masked_email):
    prefix, domain = masked_email.split("@")

    # استخراج مواقع النجوم
    star_indices = [i for i, c in enumerate(prefix) if c == '*']
    num_stars = len(star_indices)

    if num_stars == 0:
        return [masked_email]  # لا حاجة للتخمين

    chars = string.ascii_lowercase + string.digits
    combinations = itertools.product(chars, repeat=num_stars)

    emails = []
    for combo in combinations:
        guess = list(prefix)
        for idx, char in zip(star_indices, combo):
            guess[idx] = char
        email = ''.join(guess) + '@' + domain
        emails.append(email)
        if len(emails) >= 30:
            break
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
        except Exception:
            continue
    return results
