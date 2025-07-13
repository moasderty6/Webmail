import subprocess
import itertools
import string

def generate_emails(masked_email):
    prefix, domain = masked_email.split("@")

    # أين توجد النجوم؟ وبكم عددها؟
    star_indices = [i for i, c in enumerate(prefix) if c == '*']
    num_stars = len(star_indices)

    if num_stars == 0:
        return [masked_email]  # لا يوجد تخمين مطلوب

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
