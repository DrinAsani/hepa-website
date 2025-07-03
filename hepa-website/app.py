import os
import smtplib
from flask import Flask, render_template, request, jsonify, abort, url_for
from flask_cors import CORS
from dotenv import load_dotenv

# ──────────────────────────── load env ────────────────────────────
load_dotenv()
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
EMAIL_TO   = os.getenv("EMAIL_TO")
if not all((EMAIL_USER, EMAIL_PASS, EMAIL_TO)):
    raise RuntimeError("Missing EMAIL_USER / EMAIL_PASS / EMAIL_TO in .env")

# ──────────────────────────── flask setup ────────────────────────────
app = Flask(__name__)
CORS(app)

# ──────────────────────────── your data ────────────────────────────
# Slugs must match the detail‐page URLs below.
SERVICES = [
    {"slug":"network-engineering",
     "title":"Network Engineering",
     "description":"Scalable, secure networks built to last.",
     "features":["LAN/WAN design","BGP & OSPF peering","High-availability"]},
    {"slug":"devops",
     "title":"DevOps & Platform Engineering",
     "description":"CI/CD, automation & cloud-native workflows.",
     "features":["GitLab pipelines","Terraform modules","Docker orchestration"]},
    {"slug":"cloud",
     "title":"Cloud Solutions (AWS, Azure)",
     "description":"End-to-end cloud migrations & architectures.",
     "features":["VPC design","IAM best practices","Cost optimization"]},
    {"slug":"cybersecurity",
     "title":"Cyber Security & Compliance",
     "description":"Pen-testing, audits & security hardening.",
     "features":["Vulnerability scans","SIEM integration","ISO27001"]},
    {"slug":"it-support",
     "title":"IT Support & Managed Services",
     "description":"24/7 helpdesk, monitoring & on-site support.",
     "features":["Ticketing system","SLA management","Remote troubleshooting"]},
    {"slug":"automation",
     "title":"Automation (CI/CD, Infra, Workflows)",
     "description":"Automate deployments & infrastructure tasks.",
     "features":["Ansible playbooks","GitOps workflows","Webhook triggers"]},
    {"slug":"data-iot",
     "title":"Data Analytics & IoT",
     "description":"Transform sensor data into business insights.",
     "features":["Kafka pipelines","Dashboards (Plotly)","Edge compute"]},
    {"slug":"web-mobile",
     "title":"Web & Mobile Development",
     "description":"Responsive front-ends & robust back-ends.",
     "features":["React/Angular","RESTful APIs","Push notifications"]},
    {"slug":"consulting",
     "title":"Digital Transformation Consulting",
     "description":"Strategy, roadmaps & change management.",
     "features":["Maturity assessments","KPI definition","Workshops"]},
    {"slug":"training",
     "title":"Training & Workshops",
     "description":"Hands-on courses in networking, DevOps & cloud.",
     "features":["Certification prep","Lab environments","Custom curricula"]},
]

INDUSTRIES = [
    {"slug":"finance",     "title":"Finance","description":"Secure trading platforms, risk analytics."},
    {"slug":"healthcare",  "title":"Healthcare","description":"HIPAA-compliant EHR & telemedicine."},
    {"slug":"retail-ecom", "title":"Retail & E-commerce","description":"Scalable storefronts & payment integration."},
    {"slug":"manufacturing","title":"Manufacturing","description":"Smart factory & IIoT solutions."},
    {"slug":"startups",    "title":"Startups","description":"MVPs, rapid prototyping & scale-up."},
    {"slug":"government",  "title":"Government","description":"Citizen portals & secure infrastructure."},
    {"slug":"telecom",     "title":"Telecom","description":"5G backhaul & network orchestration."},
    {"slug":"smart-buildings","title":"Smart Buildings","description":"IoT sensors & energy management."},
    {"slug":"education",   "title":"Education","description":"E-learning platforms & virtual labs."},
    {"slug":"digitalization","title":"Digitalization","description":"End-to-end digital transformation."},
]

PROJECTS = [
    {"slug":"dc-automation-platform", "title":"DC Automation Platform"},
    {"slug":"hybrid-cloud-migration", "title":"Hybrid Cloud Migration"},
    {"slug":"network-overhaul-smb",   "title":"Network Overhaul for SMB"},
    {"slug":"secure-iot-rollout",     "title":"Secure IoT Rollout"},
    {"slug":"custom-web-dashboard",   "title":"Custom Web Dashboard"},
]

TECH_STACK = [
    {"slug":"cisco",      "title":"Cisco","logo":"cisco.svg"},
    {"slug":"aws",        "title":"AWS","logo":"aws_logo_smile_1200x630.png"},
    {"slug":"azure",      "title":"Azure","logo":"azure-original.svg"},
    {"slug":"kubernetes", "title":"Kubernetes","logo":"kubernetes-plain.svg"},
    {"slug":"linux",      "title":"Linux","logo":"linux-original.svg"},
    {"slug":"python",     "title":"Python","logo":"python-original.svg"},
    {"slug":"ansible",    "title":"Ansible","logo":"ansible-original.svg"},
]

# ──────────────────────────── email helper ────────────────────────────
def _send_email(sender, password, recipient, subject, body):
    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.starttls()
        smtp.login(sender, password)
        # minimal RFC-822 header
        msg = f"Subject: {subject}\n\n{body}"
        smtp.sendmail(sender, recipient, msg)

# ──────────────────────────── routes ────────────────────────────
@app.route("/")
def index():
    return render_template(
        "index.html",
        services  = SERVICES,
        industries= INDUSTRIES,
        projects  = PROJECTS,
        techs     = TECH_STACK,
    )

@app.route("/submit_contact", methods=["POST"])
def submit_contact():
    data = request.get_json() or {}
    name    = data.get("name","")
    email   = data.get("email","")
    message = data.get("message","")
    try:
        _send_email(
            sender    = EMAIL_USER,
            password  = EMAIL_PASS,
            recipient = EMAIL_TO,
            subject   = f"New message from {name}",
            body      = f"Name: {name}\nEmail: {email}\n\n{message}"
        )
        return jsonify({"success":True,"message":"Email sent."}), 200
    except Exception as e:
        print("Email error:", e)
        return jsonify({"success":False,"message":"Failed to send email."}), 500

# Detail‐page helpers
def _find(lst, slug):
    return next((i for i in lst if i["slug"]==slug), None)

@app.route("/services/<slug>")
def service_detail(slug):
    svc = _find(SERVICES, slug)
    if not svc: abort(404)
    return render_template("service_detail.html", service=svc)

@app.route("/industries/<slug>")
def industry_detail(slug):
    ind = _find(INDUSTRIES, slug)
    if not ind: abort(404)
    return render_template("industry_detail.html", industry=ind)

@app.route("/projects/<slug>")
def project_detail(slug):
    prj = _find(PROJECTS, slug)
    if not prj: abort(404)
    return render_template("project_detail.html", project=prj)

@app.route("/tech/<slug>")
def tech_detail(slug):
    tech = _find(TECH_STACK, slug)
    if not tech: abort(404)
    return render_template("tech_detail.html", tech=tech)

# ──────────────────────────── launch ────────────────────────────
if __name__ == "__main__":
    app.run(debug=True)
