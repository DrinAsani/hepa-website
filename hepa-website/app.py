import os
import smtplib
from email.message import EmailMessage
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# ─── Load environment variables from .env ────────────────────────────────
load_dotenv()  # looks for .env in project root

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
EMAIL_TO   = os.getenv("EMAIL_TO")

if not (EMAIL_USER and EMAIL_PASS and EMAIL_TO):
    raise RuntimeError("Missing EMAIL_USER, EMAIL_PASS, or EMAIL_TO in .env")

# ─── Flask setup ────────────────────────────────────────────────────────
app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app)

# ─── Email helper ───────────────────────────────────────────────────────
def _send_email(subject: str, body: str):
    """
    Send an email via Gmail SMTP with STARTTLS.
    Raises on failure.
    """
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"]    = EMAIL_USER
    msg["To"]      = EMAIL_TO
    msg.set_content(body)

    server = smtplib.SMTP("smtp.gmail.com", 587, timeout=10)
    try:
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.send_message(msg)
    finally:
        server.quit()

# ─── Routes ─────────────────────────────────────────────────────────────
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/submit_contact", methods=["POST"])
def submit_contact():
    data = request.get_json(silent=True) or {}
    name    = data.get("name", "").strip()
    email   = data.get("email", "").strip()
    message = data.get("message", "").strip()

    # Basic validation
    if not (name and email and message):
        return jsonify(success=False, message="All fields are required."), 400

    subject = f"New message from {name}"
    body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"

    try:
        _send_email(subject, body)
    except Exception as e:
        # Print the full exception for debugging
        print("⚠️  Email error:", repr(e))
        return jsonify(success=False, message="Failed to send email."), 500

    return jsonify(success=True, message="Thank you! We received your message.")

# ─── Run ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app.run(debug=True)
