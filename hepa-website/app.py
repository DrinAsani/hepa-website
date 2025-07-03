import os
from flask import Flask, render_template, request, jsonify, abort
from flask_cors import CORS
from smtplib import SMTP_SSL
from email.message import EmailMessage
from dotenv import load_dotenv

# ─── Load environment ─────────────────────────────────────────────────────────
load_dotenv()  # expects a .env in your project root
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
EMAIL_TO   = os.getenv("EMAIL_TO")
if not EMAIL_USER or not EMAIL_PASS or not EMAIL_TO:
    raise RuntimeError("Missing EMAIL_USER, EMAIL_PASS, or EMAIL_TO in .env")

# ─── Email helper ─────────────────────────────────────────────────────────────
def _send_email(sender, password, recipient, subject, body):
    msg = EmailMessage()
    msg["From"] = sender
    msg["To"]   = recipient
    msg["Subject"] = subject
    msg.set_content(body)
    with SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(sender, password)
        smtp.send_message(msg)

# ─── Flask app setup ─────────────────────────────────────────────────────────
app = Flask(__name__)
CORS(app)

# ─── Your content definitions ─────────────────────────────────────────────────
SERVICES = [
    {"slug": "network-engineering",       "title": "Network Engineering", "description": "…your copy here…"},
    {"slug": "devops",                     "title": "DevOps & Platform Engineering", "description": "…"},
    {"slug": "cloud",                      "title": "Cloud Solutions (AWS, Azure)",    "description": "…"},
    {"slug": "cybersecurity",              "title": "Cyber Security & Compliance",      "description": "…"},
    {"slug": "it-support",                 "title": "IT Support & Managed Services",    "description": "…"},
    {"slug": "automation",                 "title": "Automation (CI/CD, Infra, Workflows)", "description": "…"},
    {"slug": "data-iot",                   "title": "Data Analytics & IoT",             "description": "…"},
    {"slug": "web-mobile",                 "title": "Web & Mobile Development",         "description": "…"},
    {"slug": "consulting",                 "title": "Digital Transformation Consulting", "description": "…"},
    {"slug": "training",                   "title": "Training & Workshops",             "description": "…"},
]

INDUSTRIES = [
    {"slug": "finance",       "title": "Finance",       "description": "…"},
    {"slug": "healthcare",    "title": "Healthcare",    "description": "…"},
    {"slug": "retail",        "title": "Retail & E-commerce", "description": "…"},
    {"slug": "manufacturing", "title": "Manufacturing", "description": "…"},
    {"slug": "startups",      "title": "Startups",      "description": "…"},
    {"slug": "government",    "title": "Government",    "description": "…"},
    {"slug": "telecom",       "title": "Telecom",       "description": "…"},
    {"slug": "smart-buildings","title": "Smart Buildings","description": "…"},
    {"slug": "education",     "title": "Education",     "description": "…"},
]

PROJECTS = [
    {"slug": "dc-automation-platform","title": "DC Automation Platform","description": "…"},
    {"slug": "hybrid-cloud-migration","title": "Hybrid Cloud Migration","description": "…"},
    {"slug": "network-overhaul-smb",  "title": "Network Overhaul for SMB","description": "…"},
    {"slug": "secure-iot-rollout",    "title": "Secure IoT Rollout",    "description": "…"},
    {"slug": "custom-web-dashboard",  "title": "Custom Web Dashboard",  "description": "…"},
]

TECHS = [
    {"slug": "cisco",       "title": "Cisco",       "description": "…"},
    {"slug": "aws",         "title": "AWS",         "description": "…"},
    {"slug": "azure",       "title": "Azure",       "description": "…"},
    {"slug": "kubernetes",  "title": "Kubernetes",  "description": "…"},
    {"slug": "linux",       "title": "Linux",       "description": "…"},
    {"slug": "python",      "title": "Python",      "description": "…"},
    {"slug": "ansible",     "title": "Ansible",     "description": "…"},
]

# ─── Routes ───────────────────────────────────────────────────────────────────
@app.route("/")
def home():
    return render_template(
        "index.html",
        services=SERVICES,
        industries=INDUSTRIES,
        projects=PROJECTS,
        techs=TECHS
    )

@app.route("/services/<slug>")
def service_detail(slug):
    svc = next((x for x in SERVICES if x["slug"] == slug), None)
    if not svc:
        abort(404)
    return render_template("service_detail.html", service=svc)

@app.route("/industries/<slug>")
def industry_detail(slug):
    ind = next((x for x in INDUSTRIES if x["slug"] == slug), None)
    if not ind:
        abort(404)
    return render_template("industry_detail.html", industry=ind)

@app.route("/projects/<slug>")
def project_detail(slug):
    pj = next((x for x in PROJECTS if x["slug"] == slug), None)
    if not pj:
        abort(404)
    return render_template("project_detail.html", project=pj)

@app.route("/tech/<slug>")
def tech_detail(slug):
    tech = next((x for x in TECHS if x["slug"] == slug), None)
    if not tech:
        abort(404)
    return render_template("tech_detail.html", tech=tech)

@app.route("/submit_contact", methods=["POST"])
def submit_contact():
    data = request.json or {}
    name    = data.get("name")
    email   = data.get("email")
    message = data.get("message")
    if not (name and email and message):
        return jsonify(success=False, message="Missing fields"), 400

    # send email
    try:
        _send_email(
            sender    = EMAIL_USER,
            password  = EMAIL_PASS,
            recipient = EMAIL_TO,
            subject   = f"New message from {name}",
            body      = f"Name: {name}\nEmail: {email}\n\n{message}"
        )
    except Exception as e:
        app.logger.error("Email error: %s", e)
        return jsonify(success=False, message="Failed to send email."), 500

    return jsonify(success=True, message="Thank you! Your message has been received.")

# ─── Boot ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app.run(debug=True)
