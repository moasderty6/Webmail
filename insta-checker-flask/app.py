from flask import Flask, request, render_template
from utils import generate_emails, check_email_with_holehe
import os
import asyncio

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        email = request.form.get("email")
        username = request.form.get("username")

        if not email or not username:
            return render_template("index.html", error="يرجى إدخال البريد واسم المستخدم")

        candidates = generate_emails(email)
        result = asyncio.run(check_email_with_holehe(candidates, username))

        if result:
            return render_template("index.html", result=result)
        else:
            return render_template("index.html", error="لم يتم العثور على نتيجة")
    return render_template("index.html")

if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
