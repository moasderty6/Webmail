import itertools
import asyncio
import subprocess

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
        yield ''.join(guess) + '@' + domain

async def run_check(email):
    try:
        output = subprocess.check_output(
            ["python3", "holehe_wrapper/run.py", email],
            text=True,
            timeout=5
        )
        if "Instagram" in output:
            return email
    except:
        return None

async def check_email_with_holehe(email_generator, username):
    MAX_PARALLEL = 50
    tasks = []

    async def process_batch(batch):
        results = await asyncio.gather(*[run_check(email) for email in batch])
        for r in results:
            if r:
                return r
        return None

    batch = []
    for email in email_generator:
        batch.append(email)
        if len(batch) == MAX_PARALLEL:
            result = await process_batch(batch)
            if result:
                return result
            batch = []

    # Process any remaining emails
    if batch:
        result = await process_batch(batch)
        if result:
            return result

    return None
