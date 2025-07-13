from flask import Flask, request, render_template
import asyncio
from utils import generate_emails, check_email_with_holehe

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        masked_email = request.form.get("email")
        username = request.form.get("username")

        email_generator = generate_emails(masked_email)
        result = asyncio.run(check_email_with_holehe(email_generator, username))

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
