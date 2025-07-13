import subprocess
import itertools

def generate_emails(masked_email):
    prefix, domain = masked_email.split("@")

    # حدد مواقع النجوم
    star_indices = [i for i, c in enumerate(prefix) if c == '*']
    num_stars = len(star_indices)

    if num_stars == 0:
        yield masked_email
        return

    # توليد كل الاحتمالات: أحرف + أرقام + _ .
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789_.'
    combinations = itertools.product(chars, repeat=num_stars)

    for combo in combinations:
        guess = list(prefix)
        for idx, char in zip(star_indices, combo):
            guess[idx] = char
        email = ''.join(guess) + '@' + domain
        yield email
