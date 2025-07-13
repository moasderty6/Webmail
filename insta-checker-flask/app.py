from flask import Flask, request, render_template
import asyncio
from utils import generate_emails, check_email_with_holehe

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    results = None
    if request.method == "POST":
        masked_email = request.form.get("email")
        username = request.form.get("username")

        candidates = generate_emails(masked_email)
        results = asyncio.run(check_email_with_holehe(candidates, username))

    return render_template("index.html", results=results)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
