import asyncio
import subprocess
from itertools import product

# 🧠 توليد كل الإيميلات من البريد المخفي
def generate_emails(masked_email):
    chars = "abcdefghijklmnopqrstuvwxyz0123456789._"
    prefix, domain = masked_email.split("@")

    star_count = prefix.count("*")
    fixed_start = prefix.split("*")[0]
    fixed_end = prefix.split("*")[-1]

    emails = []
    for combo in product(chars, repeat=star_count):
        middle = "".join(combo)
        guess = f"{fixed_start}{middle}{fixed_end}@{domain}"
        emails.append(guess)

    return emails

# 🚀 دالة فحص إيميل واحد باستخدام holehe
async def run_holehe(email):
    try:
        output = subprocess.check_output(
            ["python3", "holehe_wrapper/run.py", email],
            text=True,
            stderr=subprocess.DEVNULL  # إخفاء التحذيرات
        )
        if "Instagram" in output:
            return email
    except Exception:
        return None

# ⚡ فحص الإيميلات بشكل متوازي
async def check_email_with_holehe(emails, username):
    tasks = [run_holehe(email) for email in emails]
    results = await asyncio.gather(*tasks)
    return [email for email in results if email is not None]
