import os
import ssl
import smtplib
from flask import Flask, render_template, request, jsonify, abort
from flask_cors import CORS
from dotenv import load_dotenv

# ─────────────────────────────────────────────────────────────────────────────
# 1) Load environment
# ─────────────────────────────────────────────────────────────────────────────
load_dotenv()  # reads .env in project root

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
EMAIL_TO   = os.getenv("EMAIL_TO")

if not (EMAIL_USER and EMAIL_PASS and EMAIL_TO):
    raise RuntimeError("Missing EMAIL_USER, EMAIL_PASS, or EMAIL_TO in .env")

# ─────────────────────────────────────────────────────────────────────────────
# 2) Your “database” of content
#    (you can edit titles, slugs, descriptions, features, etc. as you like)
# ─────────────────────────────────────────────────────────────────────────────
SERVICES = [
    {"slug": "network-engineering", "title": "Network Engineering", "content": "We design and optimize your enterprise networks…"},
    {"slug": "devops",               "title": "DevOps & Platform Engineering", "content": "CI/CD pipelines, infrastructure as code, and more."},
    {"slug": "cloud",                "title": "Cloud Solutions (AWS, Azure)", "content": "Public, private, and hybrid cloud migrations & ops."},
    {"slug": "cybersecurity",        "title": "Cyber Security & Compliance", "content": "Vulnerability assessments, audits, policy."},
    {"slug": "it-support",           "title": "IT Support & Managed Services", "content": "24/7 helpdesk, system monitoring, SLAs."},
    {"slug": "automation",           "title": "Automation (CI/CD, Infra, Workflows)", "content": "End-to-end automation of your processes."},
    {"slug": "data-iot",             "title": "Data Analytics & IoT", "content": "Collect, analyze, visualize real-time data."},
    {"slug": "web-mobile",           "title": "Web & Mobile Development", "content": "Custom web apps, mobile apps, responsive UI."},
    {"slug": "consulting",           "title": "Digital Transformation Consulting", "content": "Strategy, roadmaps, change management."},
    {"slug": "training",             "title": "Training & Workshops", "content": "Hands-on courses in DevOps, cloud, security."},
]

INDUSTRIES = [
    {
      "slug": "finance",
      "title": "Finance",
      "description": "Solutions tailored to banks, fintechs, and payment processors.",
      "features": ["High-availability networks", "PCI-DSS compliance", "Real-time analytics"]
    },
    {
      "slug": "healthcare",
      "title": "Healthcare",
      "description": "HIPAA-ready, secure patient data management & telehealth.",
      "features": ["Encrypted data flows", "24/7 monitoring", "Disaster recovery"]
    },
    {
      "slug": "retail-ecommerce",
      "title": "Retail & E-commerce",
      "description": "Scaleable platforms for omni-channel shopping experiences.",
      "features": ["High-traffic architectures", "Inventory & IoT integrations"]
    },
    {
      "slug": "manufacturing",
      "title": "Manufacturing",
      "description": "Smart factory automation and Industrial IoT integration.",
      "features": ["Edge computing", "Predictive maintenance"]
    },
    {
      "slug": "startups",
      "title": "Startups",
      "description": "MVP builds, cloud cost optimization, and agile ops.",
      "features": ["Rapid prototyping", "DevOps bootcamps"]
    },
    {
      "slug": "government",
      "title": "Government",
      "description": "Secure, compliant infrastructure for public sector.",
      "features": ["Strict security controls", "Audit trails"]
    },
    {
      "slug": "telecom",
      "title": "Telecom",
      "description": "Carrier-grade networking, OSS/BSS automations.",
      "features": ["High throughput", "24/7 SLAs"]
    },
    {
      "slug": "smart-buildings",
      "title": "Smart Buildings",
      "description": "IoT, BMS integrations, energy-saving automations.",
      "features": ["Sensor networks", "Dashboard analytics"]
    },
    {
      "slug": "education",
      "title": "Education",
      "description": "E-learning platforms, campus networking, remote labs.",
      "features": ["Secure access", "Scalable video streaming"]
    },
    {
      "slug": "digitalization",
      "title": "Any business ready to digitalize!",
      "description": "We can help nearly any industry go digital, fast, securely.",
      "features": []
    },
]

PROJECTS = [
    {"slug": "dc-automation-platform",    "title": "DC Automation Platform",    "content": "Automated provisioning across VLANs & data centers."},
    {"slug": "hybrid-cloud-migration",    "title": "Hybrid Cloud Migration",    "content": "On-prem → cloud, zero-downtime or burst-to-cloud."},
    {"slug": "network-overhaul-for-smb",  "title": "Network Overhaul for SMB",  "content": "Affordable, secure network redesign."},
    {"slug": "secure-iot-rollout",        "title": "Secure IoT Rollout",        "content": "End-to-end IoT security for smart devices."},
    {"slug": "custom-web-dashboard",      "title": "Custom Web Dashboard",      "content": "Real-time metrics & alerts in a single pane."},
]

TECH_LIST = [
    {"slug": "cisco",       "title": "Cisco",       "logo": "cisco.png"},
    {"slug": "aws",         "title": "AWS",         "logo": "aws.svg"},
    {"slug": "azure",       "title": "Azure",       "logo": "azure-original.svg"},
    {"slug": "kubernetes",  "title": "Kubernetes",  "logo": "kubernetes-plain.svg"},
    {"slug": "linux",       "title": "Linux",       "logo": "linux-original.svg"},
    {"slug": "python",      "title": "Python",      "logo": "python-original.svg"},
    {"slug": "ansible",     "title": "Ansible",     "logo": "ansible-original.svg"},
]

# ─────────────────────────────────────────────────────────────────────────────
# 3) Email helper
# ─────────────────────────────────────────────────────────────────────────────
def _send_email(sender, password, recipient, subject, body):
    msg = f"Subject: {subject}\n\n{body}"
    ctx = ssl.create_default_context()
    with smtplib.SMTP("smtp.gmail.com", 587) as s:
        s.starttls(context=ctx)
        s.login(sender, password)
        s.sendmail(sender, recipient, msg)

# ─────────────────────────────────────────────────────────────────────────────
# 4) Flask app and routes
# ─────────────────────────────────────────────────────────────────────────────
app = Flask(__name__)
CORS(app)


@app.route("/")
def index():
    return render_template(
        "index.html",
        services=SERVICES,
        industries=INDUSTRIES,
        projects=PROJECTS,
        techs=TECH_LIST
    )


@app.route("/services/<slug>")
def service_detail(slug):
    item = next((s for s in SERVICES if s["slug"] == slug), None)
    if not item:
        abort(404)
    return render_template("service_detail.html", service=item)


@app.route("/industries/<slug>")
def industry_detail(slug):
    item = next((i for i in INDUSTRIES if i["slug"] == slug), None)
    if not item:
        abort(404)
    return render_template("industry_detail.html", industry=item)


@app.route("/projects/<slug>")
def project_detail(slug):
    item = next((p for p in PROJECTS if p["slug"] == slug), None)
    if not item:
        abort(404)
    return render_template("project_detail.html", project=item)


@app.route("/tech/<slug>")
def tech_detail(slug):
    item = next((t for t in TECH_LIST if t["slug"] == slug), None)
    if not item:
        abort(404)
    return render_template("tech_detail.html", tech=item)


@app.route("/submit_contact", methods=["POST"])
def submit_contact():
    data = request.get_json() or {}
    name    = data.get("name", "").strip()
    email   = data.get("email", "").strip()
    message = data.get("message", "").strip()

    if not (name and email and message):
        return jsonify(success=False, message="All fields are required."), 400

    try:
        _send_email(
            sender    = EMAIL_USER,
            password  = EMAIL_PASS,
            recipient = EMAIL_TO,
            subject   = f"New message from {name}",
            body      = f"Name: {name}\nEmail: {email}\n\n{message}"
        )
        return jsonify(success=True, message="Message sent successfully.")
    except Exception as e:
        app.logger.error(f"Email error: {e!r}")
        return jsonify(success=False, message="Failed to send email."), 500


if __name__ == "__main__":
    app.run(debug=True)
