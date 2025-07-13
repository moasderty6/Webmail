import itertools
import asyncio
import subprocess

CHARS = "abcdefghijklmnopqrstuvwxyz0123456789_."  # 38 حرفًا

def generate_emails(masked_email, limit=100000):
    prefix, domain = masked_email.split("@")
    star_indices = [i for i, c in enumerate(prefix) if c == '*']
    if not star_indices:
        yield masked_email
        return

    combos = itertools.islice(itertools.product(CHARS, repeat=len(star_indices)), limit)
    for combo in combos:
        guess = list(prefix)
        for i, char in zip(star_indices, combo):
            guess[i] = char
        yield ''.join(guess) + "@" + domain


async def run_check(email):
    try:
        output = await asyncio.to_thread(subprocess.check_output, ["python3", "holehe_wrapper/run.py", email], text=True, timeout=5)
        if "Instagram" in output:
            return email
    except:
        return None


async def check_email_with_holehe(email_generator, username):
    results = []

    async def process_batch(batch):
        tasks = [run_check(email) for email in batch]
        batch_results = await asyncio.gather(*tasks)
        for result in batch_results:
            if result:
                return result
        return None

    batch = []
    counter = 0
    async for email in async_gen_wrapper(email_generator):
        batch.append(email)
        counter += 1
        if len(batch) >= 1000:
            print(f"🚀 Checking batch {counter}...")
            found = await process_batch(batch)
            if found:
                return found
            batch = []

    # آخر دفعة
    if batch:
        found = await process_batch(batch)
        if found:
            return found

    return None


async def async_gen_wrapper(generator):
    for item in generator:
        yield item
