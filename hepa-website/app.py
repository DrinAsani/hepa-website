import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ─── Load ENV ──────────────────────────────────────────────────────────────────
load_dotenv()  # expects a .env in your project root

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
EMAIL_TO   = os.getenv("EMAIL_TO")

if not all([EMAIL_USER, EMAIL_PASS, EMAIL_TO]):
    raise RuntimeError("Missing EMAIL_USER, EMAIL_PASS, or EMAIL_TO in .env")

# ─── App Setup ─────────────────────────────────────────────────────────────────
app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app)

# ─── Data Tables ────────────────────────────────────────────────────────────────
services = {
    "network-engineering": {
        "slug": "network-engineering",
        "title": "Network Engineering",
        "description": "We design, build and maintain scalable, secure enterprise networks using the latest routing, switching and SD-WAN technologies."
    },
    "devops-platform-engineering": {
        "slug": "devops-platform-engineering",
        "title": "DevOps & Platform Engineering",
        "description": "From CI/CD pipelines to Kubernetes clusters, we automate your entire software delivery lifecycle for speed and reliability."
    },
    "cloud-solutions": {
        "slug": "cloud-solutions",
        "title": "Cloud Solutions (AWS, Azure)",
        "description": "Architecture, migration and managed services for public and hybrid clouds—optimizing cost, performance and compliance."
    },
    # … add the rest …
}

industries = {
    "finance": {
        "slug": "finance",
        "title": "Finance",
        "description": "Secure, compliant IT and network solutions for banks, payments, and fintech startups."
    },
    "healthcare": {
        "slug": "healthcare",
        "title": "Healthcare",
        "description": "EHR integrations, secure telemedicine networks, and HIPAA-compliant infrastructure."
    },
    # … add the rest …
}

projects = {
    "dc-automation-platform": {
        "slug": "dc-automation-platform",
        "title": "DC Automation Platform",
        "description": "Automated provisioning and configuration of multi-site data center fabrics using GitLab CI and Arista EOS templates."
    },
    "hybrid-cloud-migration": {
        "slug": "hybrid-cloud-migration",
        "title": "Hybrid Cloud Migration",
        "description": "Seamless migration of workloads from legacy on-prem to AWS and Azure with minimal downtime."
    },
    # … add the rest …
}

tech = {
    "cisco": {
        "slug": "cisco",
        "title": "Cisco",
        "description": "Expertise in Cisco routers, switches, and data center fabrics (ACI, NX-OS)."
    },
    "aws": {
        "slug": "aws",
        "title": "AWS",
        "description": "Design and management of EC2, EKS, VPC, IAM, and serverless architectures."
    },
    "kubernetes": {
        "slug": "kubernetes",
        "title": "Kubernetes",
        "description": "Production-grade Kubernetes clusters, Helm charts, and GitOps workflows."
    },
    # … add the rest …
}

# ─── Email Helper ────────────────────────────────────────────────────────────────
def _send_email(sender, password, recipient, subject, body):
    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = recipient
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.ehlo()
        server.starttls()
        server.login(sender, password)
        server.send_message(msg)

# ─── Routes ─────────────────────────────────────────────────────────────────────
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/services/<slug>")
def service_detail(slug):
    svc = services.get(slug)
    if not svc:
        return "Not found", 404
    return render_template("service_detail.html", service=svc)

@app.route("/industries/<slug>")
def industry_detail(slug):
    ind = industries.get(slug)
    if not ind:
        return "Not found", 404
    return render_template("industry_detail.html", industry=ind)

@app.route("/projects/<slug>")
def project_detail(slug):
    prj = projects.get(slug)
    if not prj:
        return "Not found", 404
    return render_template("project_detail.html", project=prj)

@app.route("/tech/<slug>")
def tech_detail(slug):
    t = tech.get(slug)
    if not t:
        return "Not found", 404
    return render_template("tech_detail.html", tech=t)

@app.route("/submit_contact", methods=["POST"])
def submit_contact():
    data = request.json or {}
    name    = data.get("name", "")
    email   = data.get("email", "")
    message = data.get("message", "")

    try:
        _send_email(
            sender   = EMAIL_USER,
            password = EMAIL_PASS,
            recipient= EMAIL_TO,
            subject  = f"New Contact: {name}",
            body     = f"Name: {name}\nEmail: {email}\n\n{message}"
        )
        return jsonify(success=True, message="Thank you! Your message has been sent.")
    except Exception as e:
        app.logger.error("Email error: %s", e)
        return jsonify(success=False, message="Failed to send email."), 500

# ─── Run ────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app.run(debug=True)
