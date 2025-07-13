import os
import asyncio
from flask import Flask, request, render_template
from utils import generate_emails, check_email_with_holehe

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        email = request.form.get("email")
        username = request.form.get("username")

        if not email or not username:
            return render_template("index.html", error="يرجى إدخال البريد واسم المستخدم")

        candidates = generate_emails(email)
        result, checked = asyncio.run(run_check(candidates, username))

        if result:
            return render_template("index.html", result=result, checked=checked)
        else:
            return render_template("index.html", error="لم يتم العثور على نتيجة", checked=checked)
    return render_template("index.html")

async def run_check(candidates, username):
    results = await check_email_with_holehe(candidates, username)
    return results, candidates
