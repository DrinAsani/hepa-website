import os
import ssl
import smtplib
from flask import Flask, render_template, abort, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# ─── CONFIG & ENV ────────────────────────────────────────────────────────────────

load_dotenv()  # pull in EMAIL_USER, EMAIL_PASS, EMAIL_TO from .env

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
EMAIL_TO   = os.getenv("EMAIL_TO")

if not (EMAIL_USER and EMAIL_PASS and EMAIL_TO):
    raise RuntimeError("Missing EMAIL_USER / EMAIL_PASS / EMAIL_TO in .env")

# ─── DATA ─────────────────────────────────────────────────────────────────────────

# Homepage data lists—each dict needs at least 'slug', 'title', 'description', and optional 'features' list
SERVICES = [
    {
        "slug": "network-engineering",
        "title": "Network Engineering",
        "description": "Design, build & maintain scalable enterprise networks.",
        "features": [
            "LAN/WAN design",
            "BGP, OSPF & static routing",
            "High-availability topologies"
        ]
    },
    {
        "slug": "devops",
        "title": "DevOps & Platform Engineering",
        "description": "CI/CD, infrastructure as code, and platform reliability.",
        "features": [
            "GitLab/GitHub pipelines",
            "Terraform & Ansible automation",
            "Container orchestration"
        ]
    },
    # … add your other services here …
]

INDUSTRIES = [
    {
        "slug": "finance",
        "title": "Finance",
        "description": "Secure, compliant IT solutions for banks, fintechs, and insurers.",
        "features": ["PCI-DSS compliance","Encrypted communications","Audit-ready logs"]
    },
    {
        "slug": "healthcare",
        "title": "Healthcare",
        "description": "HIPAA-aligned networks and private cloud for patient data.",
        "features": ["Data encryption","Access auditing","24/7 monitoring"]
    },
    # … more industries …
]

PROJECTS = [
    {
        "slug": "dc-automation-platform",
        "title": "DC Automation Platform",
        "description": "Automated bare-metal bring-up with Tinkerbell, PXE, BGP and GitOps pipelines.",
        "features": ["70% time savings","EKS & bare-metal hybrid","Git-driven diagrams"]
    },
    {
        "slug": "hybrid-cloud-migration",
        "title": "Hybrid Cloud Migration",
        "description": "Seamless lift-and-shift into AWS with zero-downtime cutover.",
        "features": ["VPC design","Data replication","Blue/green deployments"]
    },
    # … more projects …
]

TECHS = [
    {
        "slug": "cisco",
        "title": "Cisco",
        "description": "Enterprise-grade switching & routing hardware."
    },
    {
        "slug": "aws",
        "title": "AWS",
        "description": "Global cloud infrastructure & managed services."
    },
    {
        "slug": "azure",
        "title": "Azure",
        "description": "Microsoft’s enterprise cloud platform."
    },
    {
        "slug": "kubernetes",
        "title": "Kubernetes",
        "description": "Container orchestration for scale & resilience."
    },
    # … more tech logos …
]

# ─── EMAIL HELPER ────────────────────────────────────────────────────────────────

def _send_email(sender, password, recipient, subject, body):
    """Send a simple SMTP email via Gmail STARTTLS."""
    context = ssl.create_default_context()
    message = f"Subject: {subject}\n\n{body}"
    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.starttls(context=context)
        smtp.login(sender, password)
        smtp.sendmail(sender, recipient, message)

# ─── APP SETUP ───────────────────────────────────────────────────────────────────

app = Flask(__name__)
CORS(app)

# ─── ROUTES ──────────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template(
        "index.html",
        services=SERVICES,
        industries=INDUSTRIES,
        projects=PROJECTS,
        techs=TECHS,
    )

@app.route("/services/<slug>")
def service_detail(slug):
    svc = next((s for s in SERVICES if s["slug"] == slug), None)
    if not svc: abort(404)
    return render_template("service_detail.html", service=svc)

@app.route("/industries/<slug>")
def industry_detail(slug):
    ind = next((i for i in INDUSTRIES if i["slug"] == slug), None)
    if not ind: abort(404)
    return render_template("industry_detail.html", industry=ind)

@app.route("/projects/<slug>")
def project_detail(slug):
    prj = next((p for p in PROJECTS if p["slug"] == slug), None)
    if not prj: abort(404)
    return render_template("project_detail.html", project=prj)

@app.route("/tech/<slug>")
def tech_detail(slug):
    t = next((t for t in TECHS if t["slug"] == slug), None)
    if not t: abort(404)
    return render_template("tech_detail.html", tech=t)

@app.route("/submit_contact", methods=["POST"])
def submit_contact():
    name    = request.form.get("name", "").strip()
    email   = request.form.get("email", "").strip()
    message = request.form.get("message", "").strip()

    subject = f"New message from {name or 'anonymous'}"
    body    = f"Name: {name}\nEmail: {email}\n\n{message}"

    try:
        _send_email(
            sender    = EMAIL_USER,
            password  = EMAIL_PASS,
            recipient = EMAIL_TO,
            subject   = subject,
            body      = body,
        )
        return jsonify({"success": True, "message": "Email sent!"})
    except Exception as e:
        app.logger.error("Email error:", exc_info=e)
        return jsonify({"success": False, "message": "Failed to send email."}), 500

# ─── RUN ─────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app.run(debug=True)
