import os
from flask import Flask, request, jsonify
from utils import generate_emails, check_email_with_holehe

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return "✅ Insta-Checker is running."

@app.route("/check", methods=["POST"])
def check():
    data = request.get_json()
    masked_email = data.get("email")
    username = data.get("username")

    if not masked_email or not username:
        return jsonify({"error": "Missing email or username"}), 400

    email_list = generate_emails(masked_email)

    # تشغيل الفحص مع asyncio
    import asyncio
    result = asyncio.run(check_email_with_holehe(email_list, username))

    return jsonify({
        "status": "success",
        "matched_email": result if result else None
    })

if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
