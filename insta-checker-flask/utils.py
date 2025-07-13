import subprocess
import itertools

def generate_emails(masked_email):
    prefix, domain = masked_email.split("@")
    star_indices = [i for i, c in enumerate(prefix) if c == '*']
    num_stars = len(star_indices)

    if num_stars == 0:
        yield masked_email
        return

    chars = 'abcdefghijklmnopqrstuvwxyz0123456789_.'
    combinations = itertools.product(chars, repeat=num_stars)

    for combo in combinations:
        guess = list(prefix)
        for idx, char in zip(star_indices, combo):
            guess[idx] = char
        email = ''.join(guess) + '@' + domain
        yield email

async def check_email_with_holehe(email_generator, username):
    for i, email in enumerate(email_generator):
        if i > 50:
            print("⏹️ تجاوزنا الحد التجريبي (50 احتمال). أوقفنا الفحص.")
            break

        print(f"🔍 تجربة: {email}")
        try:
            output = subprocess.check_output(
                ["python3", "holehe_wrapper/run.py", email],
                text=True,
                timeout=5
            )
            print(f"📤 النتيجة: {output.strip()}")
            if "Instagram" in output:
                print(f"✅ تم إيجاد: {email}")
                return email
        except subprocess.TimeoutExpired:
            print(f"⚠️ تجاوز الوقت في: {email}")
        except Exception as e:
            print(f"❌ خطأ في {email}: {e}")
            continue

    return None
