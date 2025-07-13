import sys

email = sys.argv[1]

# سكربت وهمي: بدّله لاحقًا بـ holehe الحقيقي
if "insta" in email or "gram" in email:
    print("Found on Instagram")
else:
    print("Not found")
