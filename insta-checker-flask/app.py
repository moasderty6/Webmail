from utils import generate_emails, check_email_with_holehe

masked_email = "x*****9@gmail.com"
username = "target_username"

async def main():
    print("🔢 Generating...")
    emails = generate_emails(masked_email, limit=100000)
    print("🚀 Running checks...")
    result = await check_email_with_holehe(emails, username)
    if result:
        print(f"✅ Found match: {result}")
    else:
        print("❌ No matching email found.")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
